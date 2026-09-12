#!/usr/bin/env python3
"""Parse OTLP JSON dumps for one run id.

Usage: parse_otel.py <otel_dump_dir> <run_id> [out.json]
Groups by resource attribute run.id; sums claude_code.token.usage / cost.usage; lists log events.
"""
import glob
import json
import os
import sys
from collections import Counter, defaultdict


# Account identifiers Claude Code stamps on every record; dropped so parsed output can be committed.
REDACT = {"user.email", "user.id", "user.account_id", "user.account_uuid", "organization.id", "ccr.session.id"}


def attrs(lst):
    out = {}
    for a in lst or []:
        if a.get("key") in REDACT:
            continue
        v = a.get("value", {})
        out[a.get("key")] = next(iter(v.values())) if v else None
    return out


def num(dp):
    if "asDouble" in dp:
        return float(dp["asDouble"])
    if "asInt" in dp:
        return float(dp["asInt"])
    return 0.0


def main():
    dump_dir, run_id = sys.argv[1], sys.argv[2]
    out_path = sys.argv[3] if len(sys.argv) > 3 else None
    tokens = defaultdict(float)   # (model,type) -> tokens
    cost = defaultdict(float)     # model -> usd
    metric_names = Counter()
    events = []
    spans = []
    seen_points = set()
    for path in sorted(glob.glob(os.path.join(dump_dir, "*.json"))):
        try:
            doc = json.load(open(path))
        except Exception:
            continue
        for rm in doc.get("resourceMetrics", []):
            ra = attrs(rm.get("resource", {}).get("attributes"))
            if ra.get("run.id") != run_id:
                continue
            for sm in rm.get("scopeMetrics", []):
                for met in sm.get("metrics", []):
                    name = met.get("name")
                    metric_names[name] += 1
                    data = met.get("sum") or met.get("gauge") or {}
                    for dp in data.get("dataPoints", []):
                        a = attrs(dp.get("attributes"))
                        key = (name, dp.get("timeUnixNano"), json.dumps(a, sort_keys=True))
                        if key in seen_points:
                            continue
                        seen_points.add(key)
                        if name == "claude_code.token.usage":
                            tokens[(a.get("model"), a.get("type"))] += num(dp)
                        elif name == "claude_code.cost.usage":
                            cost[a.get("model")] += num(dp)
        for rl in doc.get("resourceLogs", []):
            ra = attrs(rl.get("resource", {}).get("attributes"))
            if ra.get("run.id") != run_id:
                continue
            for sl in rl.get("scopeLogs", []):
                for rec in sl.get("logRecords", []):
                    a = attrs(rec.get("attributes"))
                    body = rec.get("body", {}).get("stringValue")
                    events.append({"event": a.get("event.name") or body, "ts": rec.get("timeUnixNano"), "attrs": a})
        for rs in doc.get("resourceSpans", []):
            ra = attrs(rs.get("resource", {}).get("attributes"))
            if ra.get("run.id") != run_id:
                continue
            for ss in rs.get("scopeSpans", []):
                for sp in ss.get("spans", []):
                    a = attrs(sp.get("attributes"))
                    dur = (int(sp.get("endTimeUnixNano", 0)) - int(sp.get("startTimeUnixNano", 0))) / 1e6
                    spans.append({"name": sp.get("name"), "duration_ms": round(dur, 1), "attrs": a})

    ev_counts = Counter(e["event"] for e in events)
    api = [e for e in events if e["event"] == "api_request"]
    lat = sorted(float(e["attrs"].get("duration_ms") or 0) for e in api)
    tool_decisions = [e for e in events if e["event"] == "tool_decision"]
    summary = {
        "metric_names": dict(metric_names),
        "tokens_by_model_type": {f"{m}|{t}": v for (m, t), v in tokens.items()},
        "cost_by_model_usd": dict(cost),
        "event_counts": dict(ev_counts),
        "api_requests": len(api),
        "api_latency_ms_p50": lat[len(lat) // 2] if lat else None,
        "api_latency_ms_max": lat[-1] if lat else None,
        "tool_decisions": [{"tool": e["attrs"].get("tool_name"), "decision": e["attrs"].get("decision"), "source": e["attrs"].get("source")} for e in tool_decisions],
        "span_counts": dict(Counter(s["name"] for s in spans)),
        "hook_ms_total": round(sum(s["duration_ms"] for s in spans if s["name"] == "claude_code.hook"), 1),
    }
    out = {"summary": summary, "events": events, "spans": spans}
    if out_path:
        json.dump(out, open(out_path, "w"), indent=1)
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
