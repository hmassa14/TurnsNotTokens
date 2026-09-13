#!/usr/bin/env python3
"""Render one or more runs as a step-by-step storyboard: the prompt, then for every API request what the
model was given, what it decided, what Claude Code did (including the hook), and what came back, with
tokens and an approximate cost per step.

Usage: storyboard.py <run-dir> [<run-dir> ...] > storyboard.html
Each run dir needs meta.json, result.json and transcript_parsed.json (as written by report.py or the
results/ folders). Output is a self-contained HTML fragment (no <html>/<body>), suitable for the
figures page or for rendering to PNG.
"""
import html
import json
import os
import sys

RATES = {"haiku": (1.0, 5.0), "sonnet": (2.0, 10.0), "opus": (5.0, 25.0), "fable": (10.0, 50.0)}


def rate(model):
    for k, v in RATES.items():
        if k in (model or ""):
            return v
    return (2.0, 10.0)


def step_cost_cents(model, u, first):
    i, o = rate(model)
    cw_rate = i * 2.0 if first else i * 1.25          # first request writes the system prompt at the 1-hour rate
    return (u.get("input_tokens", 0) * i + u.get("cache_creation_input_tokens", 0) * cw_rate
            + u.get("cache_read_input_tokens", 0) * i * 0.1 + u.get("output_tokens", 0) * o) / 1e4


def short_path(p):
    return os.path.basename(p) if p else ""


def describe_decision(t):
    n, i = t["name"], t["input"]
    if n == "Read":
        if "offset" in i or "limit" in i:
            return f"Read `{short_path(i.get('file_path'))}` lines {i.get('offset', 1)} to {i.get('offset', 1) + i.get('limit', 0)}"
        return f"Read `{short_path(i.get('file_path'))}`, the whole file"
    if n == "Grep":
        return f"Grep for `{str(i.get('pattern', ''))[:60]}`" + (f" in `{short_path(str(i.get('path', '')))}`" if i.get("path") else "")
    if n == "Bash":
        return f"Bash: `{i.get('command', '')[:90]}`"
    if n == "Agent":
        return f"Agent, subagent_type `{i.get('subagent_type')}`: {str(i.get('description', ''))[:70]}"
    if n == "Skill":
        return f"Skill `{i.get('skill')}`"
    if n in ("Edit", "Write"):
        return f"{n} `{short_path(i.get('file_path'))}`"
    return n


def describe_result(t):
    head = (t.get("result_head") or "").strip()
    if "hook_blocked" in t.get("flags", []):
        return ("hook", head)
    if t.get("is_error"):
        return ("error", head)
    if t["name"] == "Read":
        return ("ok", f"{t.get('result_lines', 0)} numbered lines of the file")
    return ("ok", head)


def parse_rows(spec):
    """'2' or '3-6,10-11' -> set of 1-based request numbers; None means all."""
    if not spec:
        return None
    out = set()
    for part in spec.split(","):
        a, _, b = part.partition("-")
        out.update(range(int(a), int(b or a) + 1))
    return out


def render_run(run_dir, rows=None, tokens=True, label=None):
    meta = json.load(open(os.path.join(run_dir, "meta.json")))
    res = json.load(open(os.path.join(run_dir, "result.json")))
    tp = json.load(open(os.path.join(run_dir, "transcript_parsed.json")))
    grade = json.load(open(os.path.join(run_dir, "grade.json"))) if os.path.isfile(os.path.join(run_dir, "grade.json")) else {}
    reqs = sorted(tp["requests"], key=lambda r: r["first_ts"] or "")
    tools = {t["request_id"]: t for t in tp["tool_calls"] if t.get("agent", "main") == "main"}
    model = meta["main_model"]
    arm = meta["arm"]
    color = "stock" if arm == "stock" else "hook"
    out = []
    p = out.append
    total = 0.0
    p(f'<section class="run {color}">')
    p(f'<h3><span class="arm">{html.escape(label or arm)}</span> {len(reqs)} requests · ${res.get("total_cost_usd", 0):.3f} · {meta.get("wall_ms", 0) / 1000:.0f} s · {"pass" if grade.get("pass") else "fail"}</h3>')
    if rows is None or 1 in rows:
        p('<div class="prompt"><span class="lbl">The question, exactly as sent</span>' + html.escape(meta["prompt"]) + '</div>')
    shown_any = False
    pending = "system prompt (about 24k tokens of instructions and tool definitions) + the question"
    for n, r in enumerate(reqs, 1):
        u = r["usage"]
        c = step_cost_cents(model, u, n == 1)
        total += c
        t = tools.get(r["request_id"])
        sent = u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0) + u.get("input_tokens", 0)
        thinking = "thinking" in r.get("blocks", [])
        if rows is not None and n not in rows:
            # keep the running total and the "sent" description moving even for hidden rows
            if t:
                kind, _ = describe_result(t)
                pending = "everything above + " + ({"hook": "the hook's message", "error": "the error"}.get(kind, f"that {t['name']} result"))
            if shown_any and (n + 1 in rows or n == len(reqs)):
                p(f'<div class="skip">… request {n} skipped … running total {total:.1f}¢</div>')
            continue
        shown_any = True
        p('<div class="step">')
        p(f'<div class="n">{n}</div>')
        p('<div class="cols">')
        meta_sent = f'<div class="meta">{sent:,} tokens in total, of which {u.get("cache_read_input_tokens", 0):,} already cached</div>' if tokens else ""
        p(f'<div class="col"><span class="lbl">Sent to the model</span>{html.escape(pending)}{meta_sent}</div>')
        if t:
            dec = describe_decision(t)
            p(f'<div class="col"><span class="lbl">Model decided</span>{"(thought first) " if thinking else ""}{html.escape(dec)}<div class="meta">{u.get("output_tokens", 0)} output tokens</div></div>')
            kind, text = describe_result(t)
            if kind == "hook":
                p(f'<div class="col hook-hit"><span class="lbl">Hook intervened</span>PreToolUse ran <code>wc -l</code>, saw 770 &gt; 350, and refused the read. The model got this instead of the file:<div class="quote">{html.escape(text)}</div></div>')
            elif kind == "error":
                p(f'<div class="col"><span class="lbl">Tool returned an error</span><div class="quote">{html.escape(text[:240])}</div></div>')
            else:
                p(f'<div class="col"><span class="lbl">Came back</span><div class="quote">{html.escape(text[:240])}</div><div class="meta">{t.get("result_chars", 0):,} chars, {t.get("latency_ms", 0)} ms</div></div>')
            pending = "everything above + " + ({"hook": "the hook's message", "error": "the error"}.get(kind, f"that {t['name']} result"))
        else:
            ans = (res.get("result") or "")[:260].replace("\n", " ")
            p(f'<div class="col"><span class="lbl">Model decided</span>(thought first) write the answer<div class="meta">{u.get("output_tokens", 0)} output tokens</div></div>')
            p(f'<div class="col"><span class="lbl">The answer begins</span><div class="quote">{html.escape(ans)}…</div></div>')
        p('</div>')
        p(f'<div class="cost">running cost ≈ {total:.1f}¢</div>')
        p('</div>')
    p('</section>')
    return "\n".join(out)


CSS = """
<style>
.sb { font-family: "IBM Plex Sans", system-ui, sans-serif; font-size: 13px; color: var(--ink, #1B1F1D); }
.sb .run { border: 1px solid var(--line, #D6DAD3); border-radius: 8px; padding: 14px 16px; margin: 0 0 22px; background: var(--surface, #fff); }
.sb h3 { margin: 0 0 10px; font-size: 1rem; }
.sb .arm { font-family: "IBM Plex Mono", monospace; text-transform: uppercase; letter-spacing: .06em; font-size: .78rem; padding: 2px 8px; border-radius: 999px; margin-right: 8px; }
.sb .run.stock .arm { background: #DCEFEC; color: #0A9385; } .sb .run.hook .arm { background: #F5E3D8; color: #B84E28; }
.sb .prompt { background: var(--soft, #ECEEE9); border-radius: 6px; padding: 10px 12px; margin-bottom: 14px; font-size: .92rem; }
.sb .lbl { display: block; font-family: "IBM Plex Mono", monospace; font-size: .68rem; letter-spacing: .07em; text-transform: uppercase; color: var(--ink-3, #7B857F); margin-bottom: 3px; }
.sb .step { display: grid; grid-template-columns: 28px 1fr; gap: 0 10px; padding: 10px 0; border-top: 1px solid var(--line, #D6DAD3); }
.sb .n { font-family: "IBM Plex Mono", monospace; font-weight: 600; color: var(--ink-3, #7B857F); padding-top: 2px; }
.sb .cols { display: grid; grid-template-columns: 1.1fr 1.1fr 1.4fr; gap: 12px; }
.sb .col { min-width: 0; overflow-wrap: anywhere; }
.sb .col.hook-hit { background: #F5E3D8; border-radius: 6px; padding: 8px 10px; margin: -8px -10px; }
.sb .quote { font-family: "IBM Plex Mono", monospace; font-size: .74rem; background: var(--soft, #ECEEE9); border-radius: 4px; padding: 6px 8px; margin-top: 4px; white-space: pre-wrap; word-break: break-word; max-height: 72px; overflow: hidden; }
.sb .meta { color: var(--ink-3, #7B857F); font-size: .78rem; margin-top: 3px; }
.sb .skip { font-family: "IBM Plex Mono", monospace; font-size: .76rem; color: var(--ink-3, #7B857F); padding: 8px 0 8px 38px; border-top: 1px dashed var(--line, #D6DAD3); }
.sb .cost { grid-column: 2; font-family: "IBM Plex Mono", monospace; font-size: .76rem; color: var(--ink-2, #4A5350); margin-top: 6px; }
@media (max-width: 720px) { .sb .cols { grid-template-columns: 1fr; } }
</style>
"""


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", help="run dir, optionally run_dir:ROWS:LABEL e.g. results/03/R1-shunt:3-6:Spotify's hook")
    ap.add_argument("--no-tokens", action="store_true", help="omit token counts (Figure 3 carries them)")
    ap.add_argument("--no-css", action="store_true")
    args = ap.parse_args()
    if not args.no_css:
        print(CSS)
    print('<div class="sb">')
    for spec in args.runs:
        parts = spec.split(":")
        run_dir = parts[0]
        rows = parse_rows(parts[1]) if len(parts) > 1 and parts[1] else None
        label = parts[2] if len(parts) > 2 else None
        print(render_run(run_dir, rows=rows, tokens=not args.no_tokens, label=label))
    print('</div>')


if __name__ == "__main__":
    main()
