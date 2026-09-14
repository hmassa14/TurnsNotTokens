#!/usr/bin/env python3
"""Parse a run's transcript JSONL (main + subagents) into per-request usage and per-tool-call rows.

Usage: parse_transcript.py runs/<run-id>  -> writes runs/<run-id>/transcript_parsed.json and prints a summary
"""
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

BLOCK_RE = re.compile(r"^File is (\d+) lines \(threshold: (\d+)\)")
STOCK_BYTE_RE = re.compile(r"exceeds maximum allowed size")
STOCK_TOKEN_RE = re.compile(r"exceeds maximum allowed tokens|\[Truncated: PARTIAL view")
DEDUP_RE = re.compile(r"already in your context|File unchanged since last read|Wasted call")
NUMBERED_LINE_RE = re.compile(r"^\s*\d+[\t→]", re.M)
BASH_READ_RE = re.compile(r"^\s*(cat|head|tail|less|more)\s")


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() if s else None


def parse_file(path, agent_label):
    requests = {}        # requestId -> usage/model/first_ts
    tool_uses = {}       # tool_use_id -> row
    order = []
    prompt = None
    final_text = []
    for line in open(path):
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = o.get("type")
        m = o.get("message") or {}
        if t == "assistant":
            rid = o.get("requestId") or o.get("uuid")
            r = requests.setdefault(rid, {"request_id": rid, "model": m.get("model"), "usage": m.get("usage") or {},
                                          "first_ts": o.get("timestamp"), "blocks": [], "agent": agent_label})
            for b in m.get("content") or []:
                r["blocks"].append(b.get("type"))
                if b.get("type") == "tool_use":
                    row = {"tool_use_id": b.get("id"), "name": b.get("name"), "input": b.get("input") or {},
                           "ts_use": o.get("timestamp"), "request_id": rid, "agent": agent_label}
                    tool_uses[b.get("id")] = row
                    order.append(b.get("id"))
                if b.get("type") == "text":
                    final_text.append(b.get("text", ""))
        elif t == "user":
            c = m.get("content")
            if isinstance(c, str):
                prompt = prompt or c
            elif isinstance(c, list):
                for b in c:
                    if b.get("type") == "tool_result":
                        row = tool_uses.get(b.get("tool_use_id"))
                        if row is None:
                            continue
                        cc = b.get("content")
                        s = cc if isinstance(cc, str) else " ".join(x.get("text", "") for x in cc if isinstance(x, dict))
                        row.update({"ts_result": o.get("timestamp"), "is_error": bool(b.get("is_error")),
                                    "result_head": s[:300], "result_chars": len(s),
                                    "result_lines": len(NUMBERED_LINE_RE.findall(s))})
                        row["latency_ms"] = int((ts(row["ts_result"]) - ts(row["ts_use"])) * 1000) if row.get("ts_use") else None
    return requests, [tool_uses[i] for i in order], prompt, final_text


def classify(row):
    name, inp, head = row["name"], row["input"], row.get("result_head", "")
    flags = []
    if name == "Read":
        flags.append("read_targeted" if ("offset" in inp or "limit" in inp) else "read_whole")
        if BLOCK_RE.match(head):
            flags.append("hook_blocked")
        if STOCK_BYTE_RE.search(head):
            flags.append("stock_byte_gate")
        if STOCK_TOKEN_RE.search(head):
            flags.append("stock_token_page")
        if DEDUP_RE.search(head):
            flags.append("dedup_reminder")
    if name == "Bash":
        cmd = inp.get("command", "")
        if BASH_READ_RE.match(cmd) and "|" not in cmd:
            flags.append("bash_read")
        if BLOCK_RE.match(head):
            flags.append("hook_blocked")
        if "scripts/bulk-read" in cmd or "bulk-read " in cmd:
            flags.append("worker_call")
        if "scripts/code-write" in cmd or "code-write " in cmd:
            flags.append("worker_call")
    if name == "Agent":
        flags.append("agent_spawn")
    if name == "Skill":
        flags.append("skill")
    if name in ("Edit", "Write", "MultiEdit"):
        flags.append("edit")
    return flags


def main():
    run_dir = sys.argv[1]
    tdir = os.path.join(run_dir, "transcript")
    files = [(os.path.join(tdir, "main.jsonl"), "main")]
    files += [(p, "subagent:" + os.path.basename(p).replace(".jsonl", "")) for p in sorted(glob.glob(os.path.join(tdir, "subagents", "*.jsonl")))]
    all_req, all_tools = {}, []
    prompt, final_text = None, []
    for path, label in files:
        if not os.path.isfile(path):
            continue
        req, tools, p, ft = parse_file(path, label)
        all_req.update(req)
        all_tools.extend(tools)
        if label == "main":
            prompt, final_text = p, ft
    for row in all_tools:
        row["flags"] = classify(row)

    # usage per model, counted once per requestId
    by_model = defaultdict(lambda: Counter())
    for r in all_req.values():
        u = r["usage"]
        by_model[r["model"]].update({
            "requests": 1,
            "input_tokens": u.get("input_tokens", 0),
            "cache_creation_input_tokens": u.get("cache_creation_input_tokens", 0),
            "cache_read_input_tokens": u.get("cache_read_input_tokens", 0),
            "output_tokens": u.get("output_tokens", 0),
        })

    # behavior counters
    flags = Counter(f for row in all_tools for f in row["flags"])
    tool_mix = Counter(row["name"] for row in all_tools)
    read_files = [row["input"].get("file_path") for row in all_tools if row["name"] == "Read"]
    delegated = set()
    for row in all_tools:
        if "worker_call" in row["flags"]:
            delegated.update(re.findall(r"--paths\s+(\S+)", row["input"].get("command", "")))
        if "agent_spawn" in row["flags"]:
            delegated.update(re.findall(r"[\w/.-]+\.(?:java|scala|ts|py|go)", row["input"].get("prompt", "")))
    # re-read after delegation: a MAIN-agent Read of a delegated file that happens after the delegation call
    deleg_ts = min((row.get("ts_use") or "" for row in all_tools if "worker_call" in row["flags"] or "agent_spawn" in row["flags"]), default=None)
    reread_after_delegation = 0
    if deleg_ts:
        for row in all_tools:
            if row["agent"] == "main" and row["name"] == "Read" and (row.get("ts_use") or "") > deleg_ts and not row.get("is_error"):
                f = row["input"].get("file_path") or ""
                if any(f.endswith(d) or d.endswith(os.path.basename(f)) for d in delegated):
                    reread_after_delegation += 1
    # hook bypass via paging: blocked/gated read of F then targeted read of F within next 3 tool calls
    bypass = 0
    for i, row in enumerate(all_tools):
        if row["name"] == "Read" and any(f in row["flags"] for f in ("hook_blocked", "stock_byte_gate", "stock_token_page")):
            f = row["input"].get("file_path")
            for later in all_tools[i + 1:i + 4]:
                if later["name"] == "Read" and later["input"].get("file_path") == f and "read_targeted" in later["flags"]:
                    bypass += 1
                    break
    # what the main agent did right after each hook block: the fallback distribution
    after_block = Counter()
    main_rows = [r for r in all_tools if r["agent"] == "main"]
    for i, row in enumerate(main_rows):
        if "hook_blocked" not in row["flags"]:
            continue
        nxt = main_rows[i + 1] if i + 1 < len(main_rows) else None
        if nxt is None:
            after_block["(answered)"] += 1
        elif "worker_call" in nxt["flags"]:
            after_block["worker"] += 1
        elif nxt["name"] == "Read" and "read_targeted" in nxt["flags"]:
            after_block["Read(paged)"] += 1
        else:
            after_block[nxt["name"]] += 1
    lines_entered = sum(row.get("result_lines", 0) for row in all_tools if row["name"] == "Read" and not row.get("is_error") and row["agent"] == "main")
    lines_entered_subagents = sum(row.get("result_lines", 0) for row in all_tools if row["name"] == "Read" and not row.get("is_error") and row["agent"] != "main")
    agent_models = sorted({r["model"] for r in all_req.values() if r["agent"] != "main"})

    # api latency approximation: gap between a tool_result ts and the next request's first assistant ts
    req_sorted = sorted(all_req.values(), key=lambda r: r["first_ts"] or "")
    api_gaps = []
    result_ts = sorted(ts(row["ts_result"]) for row in all_tools if row.get("ts_result"))
    for r in req_sorted:
        t = ts(r["first_ts"])
        prev = [x for x in result_ts if x <= t]
        if prev:
            api_gaps.append(int((t - prev[-1]) * 1000))

    summary = {
        "requests_total": len(all_req),
        "requests_main": sum(1 for r in all_req.values() if r["agent"] == "main"),
        "models": sorted({r["model"] for r in all_req.values() if r["model"]}),
        "agent_spawn_models": agent_models,
        "usage_by_model": {k: dict(v) for k, v in by_model.items()},
        "tool_mix": dict(tool_mix),
        "tool_calls_total": len(all_tools),
        "reads_total": tool_mix.get("Read", 0),
        "reads_whole_file": flags.get("read_whole", 0),
        "reads_targeted": flags.get("read_targeted", 0),
        "reads_blocked_by_hook": flags.get("hook_blocked", 0),
        "reads_gated_by_stock": flags.get("stock_byte_gate", 0) + flags.get("stock_token_page", 0),
        "reads_dedup_reminders": flags.get("dedup_reminder", 0),
        "hook_bypass_via_paging": bypass,
        "bash_reads": flags.get("bash_read", 0),
        "agent_spawns": flags.get("agent_spawn", 0),
        "skill_invocations": flags.get("skill", 0),
        "after_block": dict(after_block),
        "worker_calls": flags.get("worker_call", 0),
        "reread_after_delegation": reread_after_delegation,
        "edits": flags.get("edit", 0),
        "lines_entered_context": lines_entered,
        "lines_entered_subagents": lines_entered_subagents,
        "tool_calls_main": sum(1 for row in all_tools if row["agent"] == "main"),
        "files_read": sorted({os.path.basename(f) for f in read_files if f}),
        "tool_latency_ms": {n: int(sum(r.get("latency_ms") or 0 for r in all_tools if r["name"] == n) / max(1, tool_mix[n])) for n in tool_mix},
        "api_gap_ms_p50": sorted(api_gaps)[len(api_gaps) // 2] if api_gaps else None,
        "api_gap_ms_max": max(api_gaps) if api_gaps else None,
        "final_text_chars": sum(len(t) for t in final_text),
    }
    out = {"summary": summary, "requests": list(all_req.values()), "tool_calls": all_tools}
    json.dump(out, open(os.path.join(run_dir, "transcript_parsed.json"), "w"), indent=1, default=str)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
