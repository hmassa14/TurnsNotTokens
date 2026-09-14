# Run report: `SB3__natural__shunt-strict__r2__20260914-202515`

Task **SB3** (spotify-benchmark-1to1), prompt variant **natural**, arm **shunt-strict**, model `claude-sonnet-5`, Claude Code 2.1.270 (Claude Code), Kafka `0ffb4f5dd5`, started 2026-09-14T20:25:18.204469+00:00.

## 1. Headline numbers

| Metric | Value | Source |
|---|---|---|
| Cost, main session (list price) | $0.0776 | result.json `total_cost_usd` |
| Cost, worker calls | $0.0000 (0 calls) | worker/*.json |
| **Cost, total** | **$0.0776** | sum |
| Grade | score 0.733 , pass = True | grade.json (key_list) |
| Target file found | True via Grep:InsertHeaderTest.java, Read (content entered context):Filter.java, Read (content entered context):InsertHeaderTest.java | transcript tool calls |
| Finding phase | 1 requests, $0.0217 | requests before the first touch of the target file |
| Answering phase | 3 requests, $0.0560 | requests from the first touch onward |
| Wall clock | 29035 ms (harness), 26916 ms (CLI) | meta.json / result.json |
| Time waiting on API | 26331 ms | result.json `duration_api_ms` |
| Turns | 6 | result.json |
| API requests | 4 (main 4) | transcript, deduped by requestId |
| Tool calls | 5 : {"Grep": 2, "Read": 2, "Bash": 1} | transcript |
| Models used | claude-sonnet-5 | transcript `message.model` |
| Subagents spawned | 0 {} | result.json |
| Exit / timeout | 0 / False | meta.json |

## 2. Tokens and price per token

Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.

| Bucket | Tokens | Rate ($/M) | Cost |
|---|---|---|---|
| input (uncached) | 8 | 2.0 | $0.0000 |
| cache write, 1h TTL | 0 | 4.0 | $0.0000 |
| cache write, 5m TTL | 11,320 | 2.5 | $0.0283 |
| cache read | 117,906 | 0.2 | $0.0236 |
| output | 2,575 | 10.0 | $0.0257 |

Recomputed from tokens: $0.0776 vs reported $0.0776.
Cache TTL split: 5m = 11,320, 1h = 0. Thinking tokens: 1,154.

Per model, from result.json `modelUsage`:

| Model | Input | Output | Cache write | Cache read | Cost |
|---|---|---|---|---|---|
| claude-sonnet-5 | 8 | 2,575 | 11,320 | 117,906 | $0.0776 |

Cross-check, transcript usage summed once per requestId:

| Model | Requests | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|
| claude-sonnet-5 | 4 | 8 | 11,320 | 117,906 | 2,575 |

Cross-check, OpenTelemetry `claude_code.token.usage`:

| model | type | tokens |
|---|---|---|
| claude-sonnet-5 | input | 8 |
| claude-sonnet-5 | output | 2,575 |
| claude-sonnet-5 | cacheRead | 117,906 |
| claude-sonnet-5 | cacheCreation | 11,320 |

OTel `claude_code.cost.usage`: {"claude-sonnet-5": 0.0776472}

## 3. Reading behavior

| Counter | Value |
|---|---|
| reads_total | 2 |
| reads_whole_file | 2 |
| reads_targeted | 0 |
| reads_blocked_by_hook | 0 |
| reads_gated_by_stock | 0 |
| reads_dedup_reminders | 0 |
| hook_bypass_via_paging | 0 |
| bash_reads | 0 |
| agent_spawns | 0 |
| agent_spawn_models | [] |
| skill_invocations | 0 |
| worker_calls | 0 |
| reread_after_delegation | 0 |
| edits | 0 |
| lines_entered_context | 189 |
| files_read | ['Filter.java', 'InsertHeaderTest.java'] |

## 4. Timeline

Every API request and tool call in order. Latency for a tool is tool_use timestamp to tool_result timestamp. The `api gap` on a request is the time since the previous tool result landed, which approximates the API round trip.

| # | t+ (s) | Kind | Detail | Tokens (in / cw / cr / out) | Latency |
|---|---|---|---|---|---|
| 1 | 0.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use,tool_use | 2 / 5,715 / 23,949 / 257 |  |
| 2 | 0.8 | tool | Grep `class Filter` in `.`  -> 776 chars | | 65 ms |
| 3 | 1.4 | tool | Grep `class InsertHeaderTest` in `.`  -> 103 chars | | 55 ms |
| 4 | 3.0 | API request | `claude-sonnet-5` blocks=tool_use,tool_use | 2 / 745 / 29,664 / 263 | 1599 ms api gap |
| 5 | 3.0 | tool | Read `Filter.java` (whole)  -> 63 lines | | 53 ms |
| 6 | 3.8 | tool | Read `InsertHeaderTest.java` (whole)  -> 126 lines | | 51 ms |
| 7 | 16.9 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 3,475 / 30,409 / 1,257 | 13121 ms api gap |
| 8 | 17.8 | tool | Bash `find /home/user/WackyWords/shunt-eval/runs/_ws/SB3__natural__shunt-strict__r2__20260914-20`  -> 170 chars | | 421 ms |
| 9 | 25.5 | API request | `claude-sonnet-5` blocks=text | 2 / 1,385 / 33,884 / 798 | 7356 ms api gap |

## 5. OpenTelemetry events

Event counts: {"hook_registered": 2, "user_prompt": 1, "tool_decision": 5, "tool_result": 5, "api_request": 4, "hook_execution_start": 3, "hook_execution_complete": 3, "assistant_response": 1}. Metrics seen: {"claude_code.session.count": 1, "claude_code.cost.usage": 4, "claude_code.token.usage": 4, "claude_code.active_time.total": 1}. Spans: {}.

API requests per OTel: 4, latency p50 7399.0 ms, max 13955.0 ms.

Tool decisions:

| tool | decision | source |
|---|---|---|
| Grep | accept | config |
| Grep | accept | config |
| Read | accept | config |
| Read | accept | config |
| Bash | accept | config |

Per-request `api_request` events:

| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|
| claude-sonnet-5 | 2615 | 2 | 257 | 23949 | 5715 | 0.0216513 |
| claude-sonnet-5 | 2347 | 2 | 263 | 29664 | 745 | 0.010429299999999999 |
| claude-sonnet-5 | 13955 | 2 | 1257 | 30409 | 3475 | 0.0273433 |
| claude-sonnet-5 | 7399 | 2 | 798 | 33884 | 1385 | 0.018223299999999998 |

## 6. Grade

```json
{
 "score": 0.733,
 "pass": true,
 "recall": 1.0,
 "missing": [],
 "invented": [],
 "groups": [
  "pattern: 1/3"
 ],
 "grader": "key_list",
 "content_score": 0.733,
 "content_pass": true,
 "target_found": true,
 "target_files_found": [
  "Filter.java",
  "InsertHeaderTest.java"
 ],
 "target_files_missing": [],
 "found_via": [
  "Grep:InsertHeaderTest.java",
  "Read (content entered context):Filter.java",
  "Read (content entered context):InsertHeaderTest.java",
  "Bash:Filter.java"
 ],
 "first_target_touch_ts": "2026-09-14T20:25:22.444Z",
 "finding_requests": 1,
 "finding_cost_usd": 0.0217,
 "answering_requests": 3,
 "answering_cost_usd": 0.056,
 "other_files_read": [],
 "target_read_lines_main": 189,
 "target_read_chars_main": 7755,
 "target_grep_chars_main": 273,
 "target_content_chars_any_tool": 8028,
 "target_content_tokens_est": 2007,
 "cost_recomputed_usd": 0.077647,
 "spotify_style_tokens_avoided": 0,
 "lucky": false,
 "cost_billed_main_usd": 0.0776472,
 "cost_recon_diff_usd": -0.0
}
```

## 7. Final answer text

```
No existing `FilterTest` — confirmed there's nothing to cross-check against.

**Filter's methods** (from `Filter<R>` implementing `Transformation<R>`):
- `apply(R record)`
- `version()`
- `config()`
- `close()`
- `configure(Map<String, ?> configs)`

**What `InsertHeaderTest`'s pattern actually exercises:**
- A dedicated `version()` test (`testInsertHeaderVersionRetrievedFromAppInfoParser`) — checks it against `AppInfoParser.getVersion()`.
- `apply()` — exercised indirectly through the functional scenario tests (`insertionWithExistingOtherHeader`, etc.), which call `configure(...)` then `apply(...)` and assert on the result.
- `configure()` — exercised only via its *validation* branches (`configRejectsNullHeaderKey`, `configRejectsNullHeaderValue`), i.e. because InsertHeader's `configure()` does real work (validates required config fields). It's also invoked as setup in every functional test, but never asserted on for its own sake.
- `config()` and `close()` — **never called anywhere in the file.**

**Applying that same pattern to `Filter`:**
- `apply()` → covered (there'd be an obvious test asserting `xform.apply(record)` returns `null`).
- `version()` → covered (same `AppInfoParser.getVersion()` check would port over directly).
- `configure()` → **not meaningfully covered.** Filter's `configure()` is a no-op with no validation logic, so there's nothing analogous to `configRejectsNullHeaderKey`/`configRejectsNullHeaderValue` to write, and the pattern doesn't call `configure()` for its own sake — only as setup before `apply()`, which Filter's `apply()` doesn't even need.
- `config()` → **left untested**, exactly as in InsertHeaderTest.
- `close()` → **left untested**, exactly as in InsertHeaderTest.

**Bottom line:** following the InsertHeaderTest pattern verbatim would give you tests for `apply()` and `version()` only. `config()`, `close()`, and `configure()` would all go untested — the first two because the pattern never touches them for InsertHeader either, and `configure()` because Filter has no validation logic for the pattern's exception-style tests to latch onto.
```

