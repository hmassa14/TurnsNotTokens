#!/usr/bin/env python3
"""Render one run as a Markdown trace report.

Usage: report.py runs/<run-id> tasks/<id>.json [otel_dump_dir] > report.md
Runs parse_transcript, parse_otel and grade if their outputs are missing.
"""
import json
import os
import subprocess
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))

# Anthropic first-party list price per token; cache write at the 1-hour TTL (2x), cache read 0.1x (0.025x on Fable 5.1)
RATES = {
    "haiku": (1.00, 5.00, 2.00, 0.10),
    "sonnet-5": (2.00, 10.00, 4.00, 0.20),
    "opus": (5.00, 25.00, 10.00, 0.50),
    "fable": (10.00, 50.00, 20.00, 0.25),
}


def rate_for(model):
    for k, v in RATES.items():
        if k in (model or ""):
            return v
    return None


def cost_of(model, u):
    r = rate_for(model)
    if not r:
        return None
    i, o, w1h, c = r
    ttl = u.get("cache_creation", {}) or {}
    w5m_tokens = ttl.get("ephemeral_5m_input_tokens", 0)
    w1h_tokens = ttl.get("ephemeral_1h_input_tokens", u.get("cache_creation_input_tokens", 0) - w5m_tokens)
    return (u.get("input_tokens", 0) * i + u.get("output_tokens", 0) * o
            + w5m_tokens * i * 1.25 + w1h_tokens * w1h + u.get("cache_read_input_tokens", 0) * c) / 1e6


def ts(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def ensure(run_dir, task_path, otel_dir):
    if not os.path.isfile(os.path.join(run_dir, "transcript_parsed.json")):
        subprocess.run([sys.executable, os.path.join(HERE, "parse_transcript.py"), run_dir], stdout=subprocess.DEVNULL, check=True)
    if otel_dir and not os.path.isfile(os.path.join(run_dir, "otel_parsed.json")):
        subprocess.run([sys.executable, os.path.join(HERE, "parse_otel.py"), otel_dir, os.path.basename(run_dir.rstrip("/")),
                        os.path.join(run_dir, "otel_parsed.json")], stdout=subprocess.DEVNULL, check=True)
    if not os.path.isfile(os.path.join(run_dir, "grade.json")):
        subprocess.run([sys.executable, os.path.join(HERE, "grade.py"), run_dir, task_path], stdout=subprocess.DEVNULL, check=True)


def main():
    run_dir, task_path = sys.argv[1], sys.argv[2]
    otel_dir = sys.argv[3] if len(sys.argv) > 3 else None
    ensure(run_dir, task_path, otel_dir)
    meta = json.load(open(os.path.join(run_dir, "meta.json")))
    res = json.load(open(os.path.join(run_dir, "result.json")))
    tp = json.load(open(os.path.join(run_dir, "transcript_parsed.json")))
    grade = json.load(open(os.path.join(run_dir, "grade.json")))
    otel = json.load(open(os.path.join(run_dir, "otel_parsed.json"))) if os.path.isfile(os.path.join(run_dir, "otel_parsed.json")) else None
    s = tp["summary"]
    u = res.get("usage", {})
    out = []
    p = out.append

    p(f"# Run report: `{meta['run_id']}`\n")
    p(f"Task **{meta['task_id']}** ({meta['category']}), arm **{meta['arm']}**, model `{meta['main_model']}`, Claude Code {meta['claude_code_version']}, Kafka `{meta['kafka_commit'][:10]}`, started {meta['started_at']}.\n")

    p("## 1. Headline numbers\n")
    p("| Metric | Value | Source |\n|---|---|---|")
    p(f"| Cost, main session (list price) | ${res.get('total_cost_usd', 0):.4f} | result.json `total_cost_usd` |")
    worker_files = [f for f in os.listdir(os.path.join(run_dir, "worker")) if f.endswith(".json")] if os.path.isdir(os.path.join(run_dir, "worker")) else []
    worker_cost = 0.0
    for f in worker_files:
        try:
            worker_cost += json.load(open(os.path.join(run_dir, "worker", f))).get("total_cost_usd", 0)
        except Exception:
            pass
    p(f"| Cost, worker calls | ${worker_cost:.4f} ({len(worker_files)} calls) | worker/*.json |")
    p(f"| **Cost, total** | **${res.get('total_cost_usd', 0) + worker_cost:.4f}** | sum |")
    p(f"| Grade | score {grade.get('score')} , pass = {grade.get('pass')} | grade.json ({grade.get('grader')}) |")
    p(f"| Wall clock | {meta.get('wall_ms')} ms (harness), {res.get('duration_ms')} ms (CLI) | meta.json / result.json |")
    p(f"| Time waiting on API | {res.get('duration_api_ms')} ms | result.json `duration_api_ms` |")
    p(f"| Turns | {res.get('num_turns')} | result.json |")
    p(f"| API requests | {s['requests_total']} (main {s['requests_main']}) | transcript, deduped by requestId |")
    p(f"| Tool calls | {s['tool_calls_total']} : {json.dumps(s['tool_mix'])} | transcript |")
    p(f"| Models used | {', '.join(s['models'])} | transcript `message.model` |")
    p(f"| Subagents spawned | {res.get('subagent_stats', {}).get('spawned', 0)} {json.dumps(res.get('subagent_stats', {}).get('by_type', {}))} | result.json |")
    p(f"| Exit / timeout | {meta.get('exit_code')} / {meta.get('timeout')} | meta.json |\n")

    p("## 2. Tokens and price per token\n")
    p("Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.\n")
    p("| Bucket | Tokens | Rate ($/M) | Cost |\n|---|---|---|---|")
    model = meta["main_model"]
    r = rate_for(model)
    ttl0 = u.get("cache_creation", {}) or {}
    rows = [("input (uncached)", u.get("input_tokens", 0), r[0] if r else None),
            ("cache write, 1h TTL", ttl0.get("ephemeral_1h_input_tokens", 0), r[2] if r else None),
            ("cache write, 5m TTL", ttl0.get("ephemeral_5m_input_tokens", 0), round(r[0] * 1.25, 3) if r else None),
            ("cache read", u.get("cache_read_input_tokens", 0), r[3] if r else None),
            ("output", u.get("output_tokens", 0), r[1] if r else None)]
    for name, n, rate in rows:
        p(f"| {name} | {n:,} | {rate if rate is not None else '?'} | ${(n * rate / 1e6) if rate else 0:.4f} |")
    recomputed = cost_of(model, u)
    p(f"\nRecomputed from tokens: ${recomputed:.4f} vs reported ${res.get('total_cost_usd', 0):.4f}." if recomputed is not None else "")
    ttl = u.get("cache_creation", {})
    p(f"Cache TTL split: 5m = {ttl.get('ephemeral_5m_input_tokens', 0):,}, 1h = {ttl.get('ephemeral_1h_input_tokens', 0):,}. Thinking tokens: {u.get('output_tokens_details', {}).get('thinking_tokens', 0):,}.\n")
    p("Per model, from result.json `modelUsage`:\n")
    p("| Model | Input | Output | Cache write | Cache read | Cost |\n|---|---|---|---|---|---|")
    for m, v in res.get("modelUsage", {}).items():
        p(f"| {m} | {v.get('inputTokens', 0):,} | {v.get('outputTokens', 0):,} | {v.get('cacheCreationInputTokens', 0):,} | {v.get('cacheReadInputTokens', 0):,} | ${v.get('costUSD', 0):.4f} |")
    p("\nCross-check, transcript usage summed once per requestId:\n")
    p("| Model | Requests | Input | Cache write | Cache read | Output |\n|---|---|---|---|---|---|")
    for m, v in s["usage_by_model"].items():
        p(f"| {m} | {v.get('requests', 0)} | {v.get('input_tokens', 0):,} | {v.get('cache_creation_input_tokens', 0):,} | {v.get('cache_read_input_tokens', 0):,} | {v.get('output_tokens', 0):,} |")
    if otel:
        p("\nCross-check, OpenTelemetry `claude_code.token.usage`:\n")
        p("| model | type | tokens |\n|---|---|---|")
        for k, v in otel["summary"]["tokens_by_model_type"].items():
            m, t = k.split("|")
            p(f"| {m} | {t} | {int(v):,} |")
        p(f"\nOTel `claude_code.cost.usage`: {json.dumps(otel['summary']['cost_by_model_usd'])}\n")

    p("## 3. Reading behavior\n")
    p("| Counter | Value |\n|---|---|")
    for k in ("reads_total", "reads_whole_file", "reads_targeted", "reads_blocked_by_hook", "reads_gated_by_stock",
              "reads_dedup_reminders", "hook_bypass_via_paging", "bash_reads", "agent_spawns", "agent_spawn_models",
              "skill_invocations", "worker_calls", "reread_after_delegation", "edits", "lines_entered_context", "files_read"):
        p(f"| {k} | {s.get(k)} |")
    p("")

    p("## 4. Timeline\n")
    p("Every API request and tool call in order. Latency for a tool is tool_use timestamp to tool_result timestamp. The `api gap` on a request is the time since the previous tool result landed, which approximates the API round trip.\n")
    p("| # | t+ (s) | Kind | Detail | Tokens (in / cw / cr / out) | Latency |\n|---|---|---|---|---|---|")
    events = []
    for r_ in tp["requests"]:
        events.append((ts(r_["first_ts"]), "request", r_))
    for t in tp["tool_calls"]:
        events.append((ts(t["ts_use"]), "tool", t))
    events = [e for e in events if e[0]]
    events.sort(key=lambda e: e[0])
    t0 = events[0][0] if events else None
    result_times = sorted(ts(t["ts_result"]) for t in tp["tool_calls"] if t.get("ts_result"))
    n = 0
    for when, kind, obj in events:
        n += 1
        dt = (when - t0).total_seconds() if t0 else 0
        if kind == "request":
            uu = obj["usage"]
            prev = [x for x in result_times if x <= when]
            gap = f"{int((when - prev[-1]).total_seconds() * 1000)} ms api gap" if prev else ""
            agent = "" if obj["agent"] == "main" else f" [{obj['agent']}]"
            p(f"| {n} | {dt:.1f} | API request{agent} | `{obj['model']}` blocks={','.join(obj['blocks'])} | {uu.get('input_tokens', 0):,} / {uu.get('cache_creation_input_tokens', 0):,} / {uu.get('cache_read_input_tokens', 0):,} / {uu.get('output_tokens', 0):,} | {gap} |")
        else:
            inp = obj["input"]
            if obj["name"] == "Read":
                d = f"Read `{os.path.basename(inp.get('file_path', ''))}`" + (f" offset={inp.get('offset')} limit={inp.get('limit')}" if ("offset" in inp or "limit" in inp) else " (whole)")
            elif obj["name"] == "Bash":
                d = "Bash `" + inp.get("command", "")[:90].replace("|", "\\|") + "`"
            elif obj["name"] == "Grep":
                d = f"Grep `{str(inp.get('pattern', ''))[:50]}` in `{os.path.basename(str(inp.get('path', '') or '.'))}`"
            elif obj["name"] == "Agent":
                d = f"Agent subagent_type={inp.get('subagent_type')} : {str(inp.get('description', ''))[:60]}"
            else:
                d = f"{obj['name']} " + json.dumps({k: str(v)[:40] for k, v in list(inp.items())[:3]}).replace("|", "\\|")
            flags = " ".join(f"**{f}**" for f in obj.get("flags", []) if f not in ("read_whole", "read_targeted"))
            err = " ERROR" if obj.get("is_error") else ""
            lines = f"{obj.get('result_lines', 0)} lines" if obj["name"] == "Read" and not obj.get("is_error") else f"{obj.get('result_chars', 0)} chars"
            agent = "" if obj["agent"] == "main" else f" [{obj['agent']}]"
            p(f"| {n} | {dt:.1f} | tool{agent} | {d}{err} {flags} -> {lines} | | {obj.get('latency_ms')} ms |")
    p("")

    if otel:
        p("## 5. OpenTelemetry events\n")
        o = otel["summary"]
        p(f"Event counts: {json.dumps(o['event_counts'])}. Metrics seen: {json.dumps(o['metric_names'])}. Spans: {json.dumps(o['span_counts'])}.\n")
        p(f"API requests per OTel: {o['api_requests']}, latency p50 {o['api_latency_ms_p50']} ms, max {o['api_latency_ms_max']} ms.\n")
        p("Tool decisions:\n")
        p("| tool | decision | source |\n|---|---|---|")
        for d in o["tool_decisions"]:
            p(f"| {d['tool']} | {d['decision']} | {d['source']} |")
        api = [e for e in otel["events"] if e["event"] == "api_request"]
        if api:
            p("\nPer-request `api_request` events:\n")
            p("| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |\n|---|---|---|---|---|---|---|")
            for e in api:
                a = e["attrs"]
                p(f"| {a.get('model')} | {a.get('duration_ms')} | {a.get('input_tokens')} | {a.get('output_tokens')} | {a.get('cache_read_tokens')} | {a.get('cache_creation_tokens')} | {a.get('cost_usd')} |")
        p("")

    p("## 6. Grade\n")
    p("```json\n" + json.dumps(grade, indent=1) + "\n```\n")
    p("## 7. Final answer text\n")
    p("```\n" + (res.get("result") or "")[:6000] + "\n```\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
