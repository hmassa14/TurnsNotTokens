#!/usr/bin/env python3
"""Build the comparison tables from run directories.

Usage: table.py runs/ [--tasks tasks/] [--arms stock,shunt,hook-explore] [--variant named|natural|all] > results.md

Output: a summary table across all tasks (mean per arm), then one table per task+variant with the
arms as columns and metrics grouped into Performance / Latency / Cost. Repetitions of the same
task+variant+arm are averaged; pass rate and pass^k are shown when k > 1.
"""
import argparse
import glob
import json
import os
import statistics
from collections import defaultdict

ARMS_DEFAULT = ["stock", "shunt", "hook-explore", "shunt-strict", "hook-explore-strict"]
ARM_LABEL = {"stock": "A · stock", "shunt": "B · shunt", "hook-explore": "C · hook + Explore", "shunt-strict": "B' · shunt strict", "hook-explore-strict": "C' · Explore strict"}


def load_run(run_dir):
    try:
        meta = json.load(open(os.path.join(run_dir, "meta.json")))
        res = json.load(open(os.path.join(run_dir, "result.json")))
        grade = json.load(open(os.path.join(run_dir, "grade.json")))
        tp = json.load(open(os.path.join(run_dir, "transcript_parsed.json")))["summary"]
    except Exception:
        return None
    otel = None
    op = os.path.join(run_dir, "otel_parsed.json")
    if os.path.isfile(op):
        otel = json.load(open(op))["summary"]
    worker_dir = os.path.join(run_dir, "worker")
    worker_files = [f for f in os.listdir(worker_dir) if f.endswith(".json")] if os.path.isdir(worker_dir) else []
    worker_cost = worker_ms = 0.0
    for f in worker_files:
        try:
            w = json.load(open(os.path.join(worker_dir, f)))
            worker_cost += w.get("total_cost_usd", 0)
            worker_ms += w.get("duration_ms", 0)
        except Exception:
            pass
    u = res.get("usage", {})
    main_cost = res.get("total_cost_usd", 0)
    sub_cost = sum(v.get("costUSD", 0) for m, v in res.get("modelUsage", {}).items() if m != main_model_key(res, meta))
    tool_ms = sum(tp.get("tool_latency_ms", {}).get(n, 0) * c for n, c in tp.get("tool_mix", {}).items())
    api_max = otel["api_latency_ms_max"] if otel and otel.get("api_latency_ms_max") else tp.get("api_gap_ms_max")
    return {
        "task": meta["task_id"], "variant": meta.get("variant", "named"), "arm": meta["arm"], "rep": meta.get("rep", 1),
        # performance
        "score": grade.get("score", 0), "pass": 1.0 if grade.get("pass") else 0.0,
        "found": 1.0 if grade.get("target_found") else 0.0,
        "lucky": 1.0 if grade.get("lucky") else 0.0,
        "target_tokens_any": grade.get("target_content_tokens_est", 0),
        "lines_in_context": tp.get("lines_entered_context", 0),
        "tool_calls": tp.get("tool_calls_total", 0),
        "reads_whole": tp.get("reads_whole_file", 0), "reads_targeted": tp.get("reads_targeted", 0),
        "reads_blocked": tp.get("reads_blocked_by_hook", 0),
        "bypass": tp.get("hook_bypass_via_paging", 0),
        "lines_sub": tp.get("lines_entered_subagents", 0),
        "delegations": tp.get("agent_spawns", 0) + tp.get("worker_calls", 0),
        "reread": tp.get("reread_after_delegation", 0),
        # latency
        "wall_s": meta.get("wall_ms", 0) / 1000, "api_requests": tp.get("requests_total", 0),
        "longest_api_s": (api_max or 0) / 1000, "tools_s": tool_ms / 1000,
        "delegate_s": worker_ms / 1000,
        # cost
        "cost_total": main_cost + worker_cost, "cost_main": main_cost - sub_cost, "cost_worker": worker_cost + sub_cost,
        "cost_finding": grade.get("finding_cost_usd", 0), "cost_answering": grade.get("answering_cost_usd", 0),
        "tok_input": u.get("input_tokens", 0), "tok_cache_write": u.get("cache_creation_input_tokens", 0),
        "tok_cache_read": u.get("cache_read_input_tokens", 0), "tok_output": u.get("output_tokens", 0),
        "spotify_avoided": grade.get("spotify_style_tokens_avoided", 0),
    }


def main_model_key(res, meta):
    for m in res.get("modelUsage", {}):
        if meta["main_model"].replace("claude-", "") in m:
            return m
    return None


ROWS = [
    ("Performance", None),
    ("Score", "score", "{:.2f}"), ("Pass rate", "pass", "{:.0%}"), ("Found target file", "found", "{:.0%}"),
    ("Lucky passes (right answer, target never found)", "lucky", "{:.0%}"),
    ("Target content into main context, any tool (tokens, chars/4)", "target_tokens_any", "{:,.0f}"),
    ("Lines read into main context (Read only)", "lines_in_context", "{:,.0f}"), ("Lines read by subagent or worker", "lines_sub", "{:,.0f}"), ("Tool calls", "tool_calls", "{:.1f}"),
    ("Reads, whole file", "reads_whole", "{:.1f}"), ("Reads, targeted", "reads_targeted", "{:.1f}"),
    ("Reads blocked by hook", "reads_blocked", "{:.1f}"), ("Hook bypassed via offset/limit", "bypass", "{:.1f}"), ("Subagent or worker calls", "delegations", "{:.1f}"),
    ("Re-read after delegation", "reread", "{:.1f}"),
    ("Latency", None),
    ("Wall clock (s)", "wall_s", "{:.1f}"), ("API requests", "api_requests", "{:.1f}"), ("Longest API call (s)", "longest_api_s", "{:.1f}"),
    ("Time in tools (s)", "tools_s", "{:.1f}"), ("Time in worker or subagent (s)", "delegate_s", "{:.1f}"),
    ("Cost", None),
    ("Total, list price ($)", "cost_total", "{:.3f}"), ("Main model ($)", "cost_main", "{:.3f}"), ("Worker or subagent ($)", "cost_worker", "{:.3f}"),
    ("Finding phase ($)", "cost_finding", "{:.3f}"), ("Answering phase ($)", "cost_answering", "{:.3f}"),
    ("Input tokens, uncached", "tok_input", "{:,.0f}"), ("Cache write tokens", "tok_cache_write", "{:,.0f}"),
    ("Cache read tokens", "tok_cache_read", "{:,.0f}"), ("Output tokens", "tok_output", "{:,.0f}"),
    ("Spotify-style tokens avoided", "spotify_avoided", "{:,.0f}"),
]


def agg(runs, key):
    vals = [r[key] for r in runs if r.get(key) is not None]
    return statistics.mean(vals) if vals else None


def render(title, groups, arms, note=None):
    out = [f"### {title}\n"]
    if note:
        out.append(note + "\n")
    out.append("| | " + " | ".join(ARM_LABEL.get(a, a) for a in arms) + " |")
    out.append("|---|" + "---|" * len(arms))
    for row in ROWS:
        if row[1] is None:
            out.append(f"| **{row[0]}** |" + " |" * len(arms))
            continue
        label, key, fmt = row
        cells = []
        for a in arms:
            runs = groups.get(a, [])
            v = agg(runs, key)
            cells.append(fmt.format(v) if v is not None else "")
        out.append(f"| {label} | " + " | ".join(cells) + " |")
        if key == "pass" and any(len(groups.get(a, [])) > 1 for a in arms):
            cells = []
            for a in arms:
                runs = groups.get(a, [])
                cells.append(("yes" if all(r["pass"] for r in runs) else "no") + f" (k={len(runs)})" if runs else "")
            out.append("| Pass^k (all reps passed) | " + " | ".join(cells) + " |")
    out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("runs_dir")
    ap.add_argument("--arms", default=",".join(ARMS_DEFAULT))
    ap.add_argument("--variant", default="all")
    args = ap.parse_args()
    arms = args.arms.split(",")
    rows = [r for r in (load_run(d) for d in sorted(d for d in glob.glob(os.path.join(args.runs_dir, "*")) if os.path.isfile(os.path.join(d, "meta.json")))) if r]
    rows = [r for r in rows if not r["task"].endswith("SMOKE") and (args.variant == "all" or r["variant"] == args.variant)]
    if not rows:
        print("no graded runs found"); return
    by_arm = defaultdict(list)
    for r in rows:
        by_arm[r["arm"]].append(r)
    n = {a: len(by_arm[a]) for a in arms}
    print("## Summary across all tasks\n")
    print(render("Mean per run, all tasks and variants", by_arm, arms, note="Runs per arm: " + ", ".join(f"{ARM_LABEL.get(a, a)} = {n[a]}" for a in arms)))
    print("## Per example\n")
    keyed = defaultdict(lambda: defaultdict(list))
    for r in rows:
        keyed[(r["task"], r["variant"])][r["arm"]].append(r)
    for (task, variant) in sorted(keyed):
        print(render(f"{task} · {variant} prompt", keyed[(task, variant)], arms))


if __name__ == "__main__":
    main()
