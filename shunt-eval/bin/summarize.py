#!/usr/bin/env python3
"""Per-category and per-task summary of one archived grid, with paired statistics.

Usage: summarize.py results/05-natural-second-grid [--arms stock,shunt-strict] [--json out.json]

For every task: mean and range per arm of cost, wall time, requests, target tokens in context, blocks,
worker calls, pass count. For every category and overall: mean cost per arm, the paired per-task
percentage difference with a bootstrap 95% interval, a sign test over tasks, pass rates, and the
after-block distribution. Cost is main-model billed cost plus the worker's own cost.
"""
import argparse
import glob
import json
import os
import random
import statistics as st
from collections import Counter, defaultdict
from math import comb

CATS = [("SB", "Spotify's four benchmark tasks, one to one"), ("ND", "Needle reads: one fact in a big file"),
        ("SC", "Spotify's task shapes on files over the threshold"), ("HM", "Harm: precise edits and debugging on big files"),
        ("CT", "Controls: small files, hook never fires")]


def load(d):
    g = json.load(open(os.path.join(d, "grade.json")))
    r = json.load(open(os.path.join(d, "result.json")))
    m = json.load(open(os.path.join(d, "meta.json")))
    t = json.load(open(os.path.join(d, "transcript_parsed.json")))
    s = t.get("summary", t)
    worker = 0.0
    for w in glob.glob(os.path.join(d, "worker", "*.json")):
        try:
            worker += json.load(open(w)).get("total_cost_usd", 0) or 0
        except Exception:
            pass
    return {
        "task": m["task_id"], "arm": m["arm"], "rep": m.get("rep", 1), "cat": m["task_id"][:2],
        "pass": bool(g.get("pass")), "score": g.get("score"), "lucky": bool(g.get("lucky")), "found": g.get("target_found"),
        "cost": (r.get("total_cost_usd") or 0) + worker, "main_cost": r.get("total_cost_usd") or 0, "worker_cost": worker,
        "wall_s": (m.get("wall_ms") or r.get("duration_ms") or 0) / 1000, "requests": len(t.get("requests", [])),
        "tgt_tokens": g.get("target_content_tokens_est") or 0, "blocks": s.get("reads_blocked_by_hook") or 0,
        "worker_calls": s.get("worker_calls") or 0, "skill_calls": s.get("skill_invocations") or 0,
        "after_block": s.get("after_block") or {}, "spotify_avoided": g.get("spotify_style_tokens_avoided") or 0,
        "output_tokens": sum((x.get("usage") or {}).get("output_tokens", 0) for x in t.get("requests", [])),
        "cache_read": sum((x.get("usage") or {}).get("cache_read_input_tokens", 0) for x in t.get("requests", [])),
    }


def sign_test(diffs):
    """Two-sided exact sign test on paired differences (hook minus stock); ties dropped."""
    pos = sum(1 for d in diffs if d > 0)
    neg = sum(1 for d in diffs if d < 0)
    n = pos + neg
    if n == 0:
        return 1.0
    k = min(pos, neg)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def boot_ci(vals, fn=st.mean, n=5000, seed=0):
    if len(vals) < 2:
        return (None, None)
    rnd = random.Random(seed)
    xs = sorted(fn([rnd.choice(vals) for _ in vals]) for _ in range(n))
    return (xs[int(0.025 * n)], xs[int(0.975 * n)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archive")
    ap.add_argument("--arms", default="stock,shunt-strict")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()
    a0, a1 = args.arms.split(",")
    rows = [load(d) for d in sorted(glob.glob(os.path.join(args.archive, "*"))) if os.path.isfile(os.path.join(d, "meta.json"))]
    by = defaultdict(list)
    for x in rows:
        by[(x["task"], x["arm"])].append(x)
    tasks = sorted({x["task"] for x in rows}, key=lambda t: ([c for c, _ in CATS].index(t[:2]), t))

    def agg(xs, k):
        v = [x[k] for x in xs]
        return {"mean": st.mean(v), "min": min(v), "max": max(v), "n": len(v)} if v else None

    per_task = {}
    for t in tasks:
        s0, s1 = by.get((t, a0), []), by.get((t, a1), [])
        if not s0 or not s1:
            continue
        per_task[t] = {
            "cat": t[:2], "n": (len(s0), len(s1)),
            "pass": (sum(x["pass"] for x in s0), sum(x["pass"] for x in s1)),
            "lucky": (sum(x["lucky"] for x in s0), sum(x["lucky"] for x in s1)),
            "cost": (agg(s0, "cost"), agg(s1, "cost")), "wall_s": (agg(s0, "wall_s"), agg(s1, "wall_s")),
            "requests": (agg(s0, "requests"), agg(s1, "requests")), "tgt_tokens": (agg(s0, "tgt_tokens"), agg(s1, "tgt_tokens")),
            "blocks": sum(x["blocks"] for x in s1), "worker_calls": sum(x["worker_calls"] for x in s1),
            "skill_calls": sum(x["skill_calls"] for x in s1), "worker_cost": sum(x["worker_cost"] for x in s1),
            "spotify_avoided": st.mean(x["spotify_avoided"] for x in s1),
            "cost_pct": (st.mean(x["cost"] for x in s1) / st.mean(x["cost"] for x in s0) - 1) * 100,
            "after_block": dict(sum((Counter(x["after_block"]) for x in s1), Counter())),
        }

    def group(ts, label):
        ts = [t for t in ts if t in per_task]
        if not ts:
            return None
        s0 = [x for t in ts for x in by[(t, a0)]]
        s1 = [x for t in ts for x in by[(t, a1)]]
        pct = [per_task[t]["cost_pct"] for t in ts]
        diffs = [per_task[t]["cost"][1]["mean"] - per_task[t]["cost"][0]["mean"] for t in ts]
        ab = sum((Counter(per_task[t]["after_block"]) for t in ts), Counter())
        return {
            "label": label, "tasks": ts, "runs": (len(s0), len(s1)),
            "pass_rate": (st.mean(x["pass"] for x in s0), st.mean(x["pass"] for x in s1)),
            "cost_mean": (st.mean(x["cost"] for x in s0), st.mean(x["cost"] for x in s1)),
            "cost_pct_of_means": (st.mean(x["cost"] for x in s1) / st.mean(x["cost"] for x in s0) - 1) * 100,
            "cost_pct_paired_mean": st.mean(pct), "cost_pct_paired_ci": boot_ci(pct),
            "cost_pct_paired_median": st.median(pct),
            "hook_cheaper_tasks": sum(1 for d in diffs if d < 0), "n_tasks": len(ts), "sign_p": sign_test(diffs),
            "wall_mean": (st.mean(x["wall_s"] for x in s0), st.mean(x["wall_s"] for x in s1)),
            "requests_mean": (st.mean(x["requests"] for x in s0), st.mean(x["requests"] for x in s1)),
            "tgt_tokens_mean": (st.mean(x["tgt_tokens"] for x in s0), st.mean(x["tgt_tokens"] for x in s1)),
            "output_tokens_mean": (st.mean(x["output_tokens"] for x in s0), st.mean(x["output_tokens"] for x in s1)),
            "cache_read_mean": (st.mean(x["cache_read"] for x in s0), st.mean(x["cache_read"] for x in s1)),
            "blocks": sum(x["blocks"] for x in s1), "runs_with_block": sum(1 for x in s1 if x["blocks"]),
            "worker_calls": sum(x["worker_calls"] for x in s1), "runs_with_worker": sum(1 for x in s1 if x["worker_calls"]),
            "skill_calls": sum(x["skill_calls"] for x in s1), "worker_cost": sum(x["worker_cost"] for x in s1),
            "after_block": dict(ab),
        }

    out = {"arms": (a0, a1), "per_task": per_task,
           "by_category": {c: group([t for t in tasks if t.startswith(c)], lbl) for c, lbl in CATS},
           "overall": group(tasks, "all tasks"),
           "big_file_tasks": group([t for t in tasks if per_task.get(t, {}).get("blocks", 0) > 0], "tasks where the hook fired at least once"),
           "delegated_tasks": group([t for t in tasks if per_task.get(t, {}).get("worker_calls", 0) > 0], "tasks where the worker was called at least once"),
           "grep_only_tasks": group([t for t in tasks if per_task.get(t, {}).get("blocks", 0) > 0 and per_task.get(t, {}).get("worker_calls", 0) == 0], "tasks where the hook fired and the worker was never called")}
    if args.json:
        json.dump(out, open(args.json, "w"), indent=1, default=float)

    def pct(v):
        return f"{v:+.0f}%"
    print(f"{'group':52} {'runs':>7} {'pass':>11} {'cost $':>15} {'Δ means':>8} {'Δ paired (95% CI)':>22} {'hook cheaper':>12} {'sign p':>6} {'wall s':>11} {'reqs':>9} {'tgt tok':>13} {'blocks':>6} {'worker':>6}")
    for key in ["overall"] + [c for c, _ in CATS] + ["big_file_tasks", "delegated_tasks", "grep_only_tasks"]:
        g = out["by_category"].get(key) if key in dict(CATS) else out[key]
        if not g:
            continue
        ci = g["cost_pct_paired_ci"]
        cis = f"{pct(g['cost_pct_paired_mean'])} ({pct(ci[0])}, {pct(ci[1])})" if ci[0] is not None else pct(g["cost_pct_paired_mean"])
        print(f"{g['label'][:52]:52} {g['runs'][0]:>3}/{g['runs'][1]:<3} {g['pass_rate'][0]*100:4.0f}%/{g['pass_rate'][1]*100:4.0f}% {g['cost_mean'][0]:7.3f}/{g['cost_mean'][1]:<7.3f} {pct(g['cost_pct_of_means']):>8} {cis:>22} {g['hook_cheaper_tasks']:>5}/{g['n_tasks']:<6} {g['sign_p']:6.2f} {g['wall_mean'][0]:5.0f}/{g['wall_mean'][1]:<5.0f} {g['requests_mean'][0]:4.1f}/{g['requests_mean'][1]:<4.1f} {g['tgt_tokens_mean'][0]:6.0f}/{g['tgt_tokens_mean'][1]:<6.0f} {g['blocks']:>6} {g['worker_calls']:>6}")
    print()
    print(f"{'task':5} {'pass':>7} {'cost $ stock':>19} {'cost $ hook':>19} {'Δ':>6} {'wall s':>9} {'reqs':>9} {'tgt tok':>13} {'blocks':>6} {'skill':>5} {'worker':>6} after block")
    for t, p in per_task.items():
        c0, c1 = p["cost"]
        print(f"{t:5} {p['pass'][0]}/{p['n'][0]} {p['pass'][1]}/{p['n'][1]} {c0['mean']:6.3f} [{c0['min']:.3f}-{c0['max']:.3f}] {c1['mean']:6.3f} [{c1['min']:.3f}-{c1['max']:.3f}] {pct(p['cost_pct']):>6} {p['wall_s'][0]['mean']:4.0f}/{p['wall_s'][1]['mean']:<4.0f} {p['requests'][0]['mean']:4.1f}/{p['requests'][1]['mean']:<4.1f} {p['tgt_tokens'][0]['mean']:6.0f}/{p['tgt_tokens'][1]['mean']:<6.0f} {p['blocks']:>6} {p['skill_calls']:>5} {p['worker_calls']:>6} {p['after_block']}")


if __name__ == "__main__":
    main()
