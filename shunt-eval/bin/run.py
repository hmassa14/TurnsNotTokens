#!/usr/bin/env python3
"""Run one (task, arm, rep) with Claude Code headless and collect every artifact.

Usage: run.py --task tasks/R1.json --arm stock --rep 1 --model claude-sonnet-5 \
              --repo /path/to/kafka --runs-dir runs --otlp-port 4318

Writes runs/<run-id>/{meta.json,result.json,stderr.txt,transcript/,diff.patch,workspace-path.txt}
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def sh(cmd, cwd=None, check=True, env=None, timeout=None):
    return subprocess.run(cmd, cwd=cwd, check=check, env=env, timeout=timeout,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def encoded_project_dir(path):
    # Claude Code encodes the absolute cwd by replacing '/' and '_' with '-' (existing '-' are kept).
    return os.path.abspath(path).replace("/", "-").replace("_", "-")


def find_transcript(session_id):
    # Fallback: search every project dir for the session file.
    base = os.path.expanduser("~/.claude/projects")
    for d in os.listdir(base):
        cand = os.path.join(base, d, session_id + ".jsonl")
        if os.path.isfile(cand):
            return cand
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--arm", required=True)
    ap.add_argument("--rep", type=int, default=1)
    ap.add_argument("--variant", default="named", choices=["named", "natural"],
                    help="named: prompt gives the file path. natural: the question a developer would type, no path")
    ap.add_argument("--model", required=True)
    ap.add_argument("--repo", required=True, help="pinned source tree: a .tar without .git (preferred) or a directory to copy")
    ap.add_argument("--settings", default=os.path.join(ROOT, "harness", "settings.json"),
                    help="harness settings applied to every arm via --settings: offline sandbox hook, WebFetch/WebSearch denied")
    ap.add_argument("--runs-dir", default=os.path.join(ROOT, "runs"))
    ap.add_argument("--work-root", default="/var/tmp/shunt-ws", help="where workspaces are created; outside the harness tree so a run cannot find other runs or results")
    ap.add_argument("--otlp-port", type=int, default=4318)
    ap.add_argument("--max-turns", type=int, default=40)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--keep-workspace", action="store_true")
    ap.add_argument("--permission-mode", default="acceptEdits",
                    help="bypassPermissions is refused when running as root; acceptEdits plus --allowed-tools is the portable choice")
    ap.add_argument("--cache-ttl", default="5m", help="prompt cache TTL for main, subagents and worker; pinned so both arms pay one rate")
    ap.add_argument("--allowed-tools", default="Read,Grep,Glob,Bash,Edit,Write,MultiEdit,Agent,Skill,TodoWrite,TaskCreate,TaskUpdate")
    ap.add_argument("--append-system-prompt", default="Answer from the repository checked out in the working directory. Do not rely on memory of the upstream project or on the internet.",
                    help="harness constraint appended to the system prompt of every arm; the target repo is private in the setting being simulated")
    args = ap.parse_args()

    task = json.load(open(args.task))
    prompt = task["prompts"][args.variant] if "prompts" in task else task["prompt"]
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    run_id = f"{task['id']}__{args.variant}__{args.arm}__r{args.rep}__{stamp}"
    run_dir = os.path.join(args.runs_dir, run_id)
    os.makedirs(run_dir, exist_ok=True)
    work_root = args.work_root
    os.makedirs(work_root, exist_ok=True)
    ws = os.path.abspath(os.path.join(work_root, run_id))

    # 1. Workspace: fresh copy of the pinned tree, task setup patch, then ONE import commit so the
    #    workspace has no history: `git log`/`git show` cannot reveal the setup patch (a planted bug) and
    #    `git diff HEAD` at the end is exactly what the model changed.
    if args.repo.endswith(".tar"):
        import tarfile
        xdir = os.path.join(work_root, "_x_" + run_id)
        with tarfile.open(args.repo) as tf:
            top = tf.getnames()[0].split("/")[0]
            tf.extractall(xdir)
        shutil.move(os.path.join(xdir, top), ws)          # the tar's top-level dir becomes the workspace itself
        shutil.rmtree(xdir, ignore_errors=True)
        assert os.path.isdir(os.path.join(ws, "build.gradle")) or os.path.isfile(os.path.join(ws, "build.gradle")), "workspace layout wrong"
        cf = args.repo[:-4] + ".commit"
        kafka_commit = open(cf).read().strip() if os.path.isfile(cf) else "unknown"
    else:
        shutil.copytree(args.repo, ws, symlinks=True, ignore=shutil.ignore_patterns(".git"))
        kafka_commit = sh(["git", "rev-parse", "HEAD"], cwd=args.repo, check=False).stdout.strip() or "unknown"
    if task.get("setup_patch"):
        patch = os.path.join(ROOT, task["setup_patch"])
        sh(["patch", "-p1", "-s", "-i", patch], cwd=ws)   # no repo yet; plain patch, paths relative to the tree
    genv = {**os.environ, "GIT_AUTHOR_NAME": "eval", "GIT_AUTHOR_EMAIL": "eval@x", "GIT_COMMITTER_NAME": "eval", "GIT_COMMITTER_EMAIL": "eval@x"}
    sh(["git", "init", "-q"], cwd=ws, env=genv)
    sh(["git", "add", "-A"], cwd=ws, env=genv)
    sh(["git", "commit", "-q", "-m", "import"], cwd=ws, env=genv)
    arm_dir = os.path.join(ROOT, "arms", args.arm)
    if os.path.isdir(os.path.join(arm_dir, ".claude")):
        shutil.copytree(os.path.join(arm_dir, ".claude"), os.path.join(ws, ".claude"), dirs_exist_ok=True)
    # Spotify's skills reference ${CLAUDE_PLUGIN_ROOT}; a plugin install resolves that. Here the plugin lives at
    # <workspace>/.claude/shunt, so resolve it the same way at install time and leave the arm's files verbatim.
    for skill in glob.glob(os.path.join(ws, ".claude", "skills", "*", "SKILL.md")):
        txt = open(skill).read()
        if "${CLAUDE_PLUGIN_ROOT}" in txt:
            open(skill, "w").write(txt.replace("${CLAUDE_PLUGIN_ROOT}", os.path.join(ws, ".claude", "shunt")))
    if os.path.isfile(os.path.join(arm_dir, "CLAUDE.md")):
        shutil.copy(os.path.join(arm_dir, "CLAUDE.md"), os.path.join(ws, "CLAUDE.md"))

    session_id = str(uuid.uuid4())
    version = sh(["claude", "--version"]).stdout.strip()
    meta = {
        "run_id": run_id, "task_id": task["id"], "category": task["category"], "arm": args.arm,
        "rep": args.rep, "variant": args.variant, "main_model": args.model, "claude_code_version": version,
        "kafka_commit": kafka_commit, "session_id": session_id, "workspace": ws, "repo": os.path.abspath(args.repo), "settings": os.path.abspath(args.settings), "append_system_prompt": args.append_system_prompt, "target_files": task.get("files", []),
        "started_at": datetime.now(timezone.utc).isoformat(), "prompt": prompt,
    }
    json.dump(meta, open(os.path.join(run_dir, "meta.json"), "w"), indent=2)

    # 2. Env: telemetry on, parent-session markers off.
    env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT")}
    env.update({
        "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
        "OTEL_METRICS_EXPORTER": "otlp",
        "OTEL_LOGS_EXPORTER": "otlp",
        "OTEL_TRACES_EXPORTER": "otlp",
        "OTEL_EXPORTER_OTLP_PROTOCOL": "http/json",
        "OTEL_EXPORTER_OTLP_ENDPOINT": f"http://127.0.0.1:{args.otlp_port}",
        "OTEL_METRIC_EXPORT_INTERVAL": "1000",
        "OTEL_LOGS_EXPORT_INTERVAL": "1000",
        "OTEL_LOG_TOOL_DETAILS": "1",
        "OTEL_RESOURCE_ATTRIBUTES": f"run.id={run_id}",
        "SHUNT_RUN_DIR": run_dir,
        "SHUNT_HARNESS": os.path.dirname(os.path.abspath(args.settings)),
        "CLAUDE_CODE_PROMPT_CACHE_TTL": args.cache_ttl,
        "CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL": args.cache_ttl,
    })
    os.makedirs(os.path.join(run_dir, "worker"), exist_ok=True)

    # 3. Execute.
    cmd = ["claude", "-p", prompt, "--model", args.model, "--session-id", session_id,
           "--permission-mode", args.permission_mode, "--allowedTools", args.allowed_tools,
           "--max-turns", str(args.max_turns), "--output-format", "json", "--settings", args.settings]
    if args.append_system_prompt:
        cmd += ["--append-system-prompt", args.append_system_prompt]
    meta["command"] = cmd
    t0 = time.time()
    timed_out = False
    try:
        p = subprocess.run(cmd, cwd=ws, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE, text=True, timeout=args.timeout)
        out, err, rc = p.stdout, p.stderr, p.returncode
    except subprocess.TimeoutExpired as e:
        out, err, rc, timed_out = (e.stdout or ""), (e.stderr or ""), -1, True
    wall_ms = int((time.time() - t0) * 1000)
    open(os.path.join(run_dir, "result.json"), "w").write(out)
    open(os.path.join(run_dir, "stderr.txt"), "w").write(err)
    meta.update({"wall_ms": wall_ms, "exit_code": rc, "timeout": timed_out,
                 "finished_at": datetime.now(timezone.utc).isoformat()})
    json.dump(meta, open(os.path.join(run_dir, "meta.json"), "w"), indent=2)

    # 4. Collect transcript + subagents, diff, and any new file the task expects.
    proj = os.path.join(os.path.expanduser("~/.claude/projects"), encoded_project_dir(ws))
    tdir = os.path.join(run_dir, "transcript")
    os.makedirs(tdir, exist_ok=True)
    src = os.path.join(proj, session_id + ".jsonl")
    if not os.path.isfile(src):
        found = find_transcript(session_id)
        if found:
            src, proj = found, os.path.dirname(found)
    if os.path.isfile(src):
        shutil.copy(src, os.path.join(tdir, "main.jsonl"))
    sub = os.path.join(proj, session_id, "subagents")
    if os.path.isdir(sub):
        shutil.copytree(sub, os.path.join(tdir, "subagents"), dirs_exist_ok=True)
    open(os.path.join(run_dir, "diff.patch"), "w").write(sh(["git", "diff", "HEAD"], cwd=ws, check=False).stdout)
    open(os.path.join(run_dir, "status.txt"), "w").write(sh(["git", "status", "--porcelain"], cwd=ws, check=False).stdout)
    if task.get("output_file"):
        of = os.path.join(ws, task["output_file"])
        if os.path.isfile(of):
            shutil.copy(of, os.path.join(run_dir, "output_" + os.path.basename(of)))
    open(os.path.join(run_dir, "workspace-path.txt"), "w").write(ws)
    if not args.keep_workspace:
        shutil.rmtree(ws, ignore_errors=True)
    print(run_dir)


if __name__ == "__main__":
    main()
