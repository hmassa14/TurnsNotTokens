#!/usr/bin/env python3
"""Run the evaluation grid: tasks x arms x reps for one prompt variant, interleaved across arms.

Usage:
  grid.py --tasks R1,D1 --arms stock,shunt,hook-explore --variant natural --reps 1 \
          --model claude-sonnet-5 --repo /path/to/kafka [--runs-dir runs] [--otlp-port 4318]

For each cell: run.py -> report.py (which runs parse_transcript, parse_otel, grade) -> append a row
to results/runs.jsonl. Cells that already have a graded run directory are skipped, so the grid is
resumable. Order is task-major, then rep, then arm, so time-of-day never lines up with one arm.
Assumes the OTLP receiver is already listening (bin/otlp_receiver.py runs/_otel <port>).
"""
import argparse
import glob
import json
import os
import socket
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def receiver_up(port):
    try:
        socket.create_connection(("127.0.0.1", port), timeout=0.5).close()
        return True
    except OSError:
        return False


def existing(runs_dir, task, variant, arm, rep):
    for d in sorted(glob.glob(os.path.join(runs_dir, f"{task}__{variant}__{arm}__r{rep}__*"))):
        if os.path.isfile(os.path.join(d, "grade.json")):
            return d
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", default="SB1,SB2,SB3,SB4,ND1,ND2,ND3,ND4,SC1,SC2,SC3,SC4,SC5,HM1,HM2,HM3,HM4,HM5")
    ap.add_argument("--arms", default="stock,shunt-strict")
    ap.add_argument("--variant", default="natural", choices=["named", "natural"])
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--model", default="claude-sonnet-5")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--runs-dir", default=os.path.join(ROOT, "runs"))
    ap.add_argument("--otlp-port", type=int, default=4318)
    ap.add_argument("--max-turns", type=int, default=40)
    ap.add_argument("--timeout", type=int, default=900)
    ap.add_argument("--keep-workspace", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    tasks = args.tasks.split(",")
    arms = args.arms.split(",")
    if not args.dry_run and not receiver_up(args.otlp_port):
        print(f"OTLP receiver not listening on {args.otlp_port}; start bin/otlp_receiver.py first", file=sys.stderr)
        sys.exit(2)
    rows_path = os.path.join(ROOT, "results", "runs.jsonl")
    os.makedirs(os.path.dirname(rows_path), exist_ok=True)
    otel_dir = os.path.join(args.runs_dir, "_otel")

    cells = [(t, r, a) for t in tasks for r in range(1, args.reps + 1) for a in arms]
    print(f"{len(cells)} cells: {len(tasks)} tasks x {args.reps} reps x {len(arms)} arms, variant={args.variant}, model={args.model}")
    t_grid = time.time()
    for i, (task, rep, arm) in enumerate(cells, 1):
        task_path = os.path.join(ROOT, "tasks", f"{task}.json")
        done = existing(args.runs_dir, task, args.variant, arm, rep)
        if done:
            print(f"[{i}/{len(cells)}] {task} {args.variant} {arm} r{rep}: already graded at {done}, skipping")
            continue
        if args.dry_run:
            print(f"[{i}/{len(cells)}] would run {task} {args.variant} {arm} r{rep}")
            continue
        t0 = time.time()
        cmd = [sys.executable, os.path.join(HERE, "run.py"), "--task", task_path, "--arm", arm, "--rep", str(rep),
               "--variant", args.variant, "--model", args.model, "--repo", args.repo, "--runs-dir", args.runs_dir,
               "--otlp-port", str(args.otlp_port), "--max-turns", str(args.max_turns), "--timeout", str(args.timeout)]
        if args.keep_workspace:
            cmd.append("--keep-workspace")
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        run_dir = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
        if p.returncode != 0 or not os.path.isdir(run_dir):
            print(f"[{i}/{len(cells)}] {task} {arm} r{rep}: run.py failed\n{p.stderr[-2000:]}", file=sys.stderr)
            continue
        time.sleep(3)  # let the last OTLP export land before parsing
        rep_path = os.path.join(run_dir, "report.md")
        with open(rep_path, "w") as fh:
            r = subprocess.run([sys.executable, os.path.join(HERE, "report.py"), run_dir, task_path, otel_dir],
                               stdout=fh, stderr=subprocess.PIPE, text=True)
        if r.returncode != 0:
            print(f"[{i}/{len(cells)}] report failed: {r.stderr[-1500:]}", file=sys.stderr)
        try:
            grade = json.load(open(os.path.join(run_dir, "grade.json")))
            res = json.load(open(os.path.join(run_dir, "result.json")))
            meta = json.load(open(os.path.join(run_dir, "meta.json")))
            row = {"run_id": os.path.basename(run_dir), "task": task, "variant": args.variant, "arm": arm, "rep": rep,
                   "model": args.model, "pass": grade.get("pass"), "score": grade.get("score"),
                   "target_found": grade.get("target_found"), "cost_usd": res.get("total_cost_usd"),
                   "wall_ms": meta.get("wall_ms"), "num_turns": res.get("num_turns"), "timeout": meta.get("timeout")}
            with open(rows_path, "a") as fh:
                fh.write(json.dumps(row) + "\n")
            print(f"[{i}/{len(cells)}] {task} {args.variant} {arm} r{rep}: pass={row['pass']} score={row['score']} found={row['target_found']} ${row['cost_usd']:.3f} {row['wall_ms']/1000:.0f}s ({time.time()-t0:.0f}s incl. setup)")
        except Exception as e:
            print(f"[{i}/{len(cells)}] {task} {arm} r{rep}: finished but row incomplete: {e}", file=sys.stderr)
    print(f"grid done in {(time.time()-t_grid)/60:.1f} min; tables: python3 bin/table.py {args.runs_dir} --variant {args.variant}")


if __name__ == "__main__":
    main()
