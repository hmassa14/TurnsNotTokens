#!/usr/bin/env python3
"""Grade one run against its task's grader spec. Writes runs/<run-id>/grade.json.

Usage: grade.py runs/<run-id> tasks/<id>.json
Graders: key_list, bug_report, exact_diff, compile_and_checklist (compile step is optional here).
"""
import json
import os
import re
import subprocess
import sys


def load_result_text(run_dir):
    try:
        o = json.loads(open(os.path.join(run_dir, "result.json")).read())
        return o.get("result") or ""
    except Exception:
        return ""


def has(text, ident):
    """Case-insensitive match of an identifier on word boundaries (so BeginControlledShutdownEvent does not match ControlledShutdownEvent)."""
    return re.search(r"(?<![A-Za-z0-9_])" + re.escape(ident.strip()) + r"(?![A-Za-z0-9_])", text, re.I) is not None


def key_list(text, g):
    low = text.lower()
    found = [k for k in g["required"] if has(text, k)]
    missing = [k for k in g["required"] if not has(text, k)]
    invented = [k for k in g.get("deny", []) if has(text, k)]
    recall = len(found) / len(g["required"])
    extra = 0.0
    extra_notes = []
    for grp in g.get("weighted_groups", []):
        hits = [k for k in grp["items"] if has(text, k)]
        extra += grp["weight"] * len(hits) / len(grp["items"])
        extra_notes.append(f"{grp['name']}: {len(hits)}/{len(grp['items'])}")
    base_w = g.get("required_weight", 1.0)
    score = base_w * recall + extra - g.get("penalty", 0.05) * len(invented)
    score = max(0.0, min(1.0, score))
    passed = recall >= g.get("pass_recall", 0.9) and len(invented) <= g.get("max_invented", 1)
    return {"score": round(score, 3), "pass": passed, "recall": round(recall, 3), "missing": missing,
            "invented": invented, "groups": extra_notes}


def bug_report(text, g):
    low = text.lower()
    method_ok = any(m.lower() in low for m in g["methods"])
    lines = [int(x) for x in re.findall(r"\b(\d{2,5})\b", text)]
    lo, hi, tol = g["line_range"][0] - g.get("line_tolerance", 10), g["line_range"][1] + g.get("line_tolerance", 10), 0
    line_ok = any(lo <= n <= hi for n in lines)
    race_ok = any(k.lower() in low for k in g["race_keywords"])
    fps = [m for m in g.get("false_positive_methods", []) if m.lower() in low]
    passed = method_ok and line_ok and race_ok
    return {"score": 1.0 if passed else 0.0, "pass": passed, "method_named": method_ok, "line_in_range": line_ok,
            "race_described": race_ok, "false_positives_mentioned": fps}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def exact_diff(run_dir, g):
    diff = open(os.path.join(run_dir, "diff.patch")).read()
    changed = [l for l in diff.splitlines() if (l.startswith("+") or l.startswith("-")) and not l.startswith(("+++", "---"))]
    exp_minus = [norm(l) for l in g["expected_removed"]]
    exp_plus = [norm(l) for l in g["expected_added"]]
    got_minus = [norm(l[1:]) for l in changed if l.startswith("-")]
    got_plus = [norm(l[1:]) for l in changed if l.startswith("+")]
    exact = sorted(got_minus) == sorted(exp_minus) and sorted(got_plus) == sorted(exp_plus)
    right_line_changed = all(m in got_minus for m in exp_minus) and all(p in got_plus for p in exp_plus)
    score = 1.0 if exact else (0.5 if right_line_changed else 0.0)
    return {"score": score, "pass": exact, "changed_lines": len(changed), "extra_changes": len(changed) - len(exp_minus) - len(exp_plus)}


def compile_and_checklist(run_dir, g):
    files = [f for f in os.listdir(run_dir) if f.startswith("output_")]
    if not files:
        return {"score": 0.0, "pass": False, "note": "output file missing"}
    src = open(os.path.join(run_dir, files[0])).read()
    checks = {pat: bool(re.search(pat, src)) for pat in g["required_regex"]}
    counts_ok = {pat: len(re.findall(pat, src)) >= n for pat, n in g.get("min_counts", {}).items()}
    compiled = None
    ws = open(os.path.join(run_dir, "workspace-path.txt")).read().strip()
    if g.get("gradle_module") and os.path.isdir(ws):
        r = subprocess.run(["./gradlew", f"{g['gradle_module']}:compileJava", "--offline", "-q"], cwd=ws,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=1800)
        compiled = r.returncode == 0
    allc = list(checks.values()) + list(counts_ok.values()) + ([compiled] if compiled is not None else [])
    score = sum(1 for c in allc if c) / len(allc)
    if compiled is False:
        score = 0.0
    return {"score": round(score, 3), "pass": all(allc), "compiled": compiled,
            "failed_checks": [p for p, ok in {**checks, **counts_ok}.items() if not ok]}


def main():
    run_dir, task_path = sys.argv[1], sys.argv[2]
    task = json.load(open(task_path))
    g = task["grader"]
    kind = g["type"]
    if kind == "key_list":
        res = key_list(load_result_text(run_dir), g)
    elif kind == "bug_report":
        res = bug_report(load_result_text(run_dir), g)
    elif kind == "exact_diff":
        res = exact_diff(run_dir, g)
    elif kind == "compile_and_checklist":
        res = compile_and_checklist(run_dir, g)
    else:
        raise SystemExit("unknown grader " + kind)
    res["grader"] = kind
    json.dump(res, open(os.path.join(run_dir, "grade.json"), "w"), indent=2)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
