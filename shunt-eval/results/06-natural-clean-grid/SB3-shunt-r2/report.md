# Run report: `SB3__natural__shunt__r2__20260915-000706`

Task **SB3** (spotify-benchmark-1to1), prompt variant **natural**, arm **shunt**, model `claude-sonnet-5`, Claude Code 2.1.271 (Claude Code), Kafka `0ffb4f5dd5`, started 2026-09-15T00:07:15.121483+00:00.

## 1. Headline numbers

| Metric | Value | Source |
|---|---|---|
| Cost, main session (list price) | $0.0780 | result.json `total_cost_usd` |
| Cost, worker calls | $0.0000 (0 calls) | worker/*.json |
| **Cost, total** | **$0.0780** | sum |
| Grade | score 0.733 , pass = True | grade.json (key_list) |
| Target file found | True via Grep:Filter.java, Grep:InsertHeaderTest.java, Read (content entered context):Filter.java | transcript tool calls |
| Finding phase | 1 requests, $0.0215 | requests before the first touch of the target file |
| Answering phase | 4 requests, $0.0565 | requests from the first touch onward |
| Wall clock | 22144 ms (harness), 20392 ms (CLI) | meta.json / result.json |
| Time waiting on API | 20123 ms | result.json `duration_api_ms` |
| Turns | 7 | result.json |
| API requests | 5 (main 5) | transcript, deduped by requestId |
| Tool calls | 6 : {"Grep": 4, "Read": 2} | transcript |
| Models used | claude-sonnet-5 | transcript `message.model` |
| Subagents spawned | 0 {} | result.json |
| Exit / timeout | 0 / False | meta.json |

## 2. Tokens and price per token

Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.

| Bucket | Tokens | Rate ($/M) | Cost |
|---|---|---|---|
| input (uncached) | 10 | 2.0 | $0.0000 |
| cache write, 1h TTL | 0 | 4.0 | $0.0000 |
| cache write, 5m TTL | 10,739 | 2.5 | $0.0268 |
| cache read | 151,998 | 0.2 | $0.0304 |
| output | 2,071 | 10.0 | $0.0207 |

Recomputed from tokens: $0.0780 vs reported $0.0780.
Cache TTL split: 5m = 10,739, 1h = 0. Thinking tokens: 643.

Per model, from result.json `modelUsage`:

| Model | Input | Output | Cache write | Cache read | Cost |
|---|---|---|---|---|---|
| claude-sonnet-5 | 10 | 2,071 | 10,739 | 151,998 | $0.0780 |

Cross-check, transcript usage summed once per requestId:

| Model | Requests | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|
| claude-sonnet-5 | 5 | 10 | 10,739 | 151,998 | 2,071 |

Cross-check, OpenTelemetry `claude_code.token.usage`:

| model | type | tokens |
|---|---|---|
| claude-sonnet-5 | input | 10 |
| claude-sonnet-5 | output | 2,071 |
| claude-sonnet-5 | cacheRead | 151,998 |
| claude-sonnet-5 | cacheCreation | 10,739 |

OTel `claude_code.cost.usage`: {"claude-sonnet-5": 0.07797710000000001}

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
| 1 | 0.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use,tool_use | 2 / 5,689 / 23,995 / 248 |  |
| 2 | 0.8 | tool | Grep `class Filter` in `.`  -> 93 chars | | 52 ms |
| 3 | 1.4 | tool | Grep `class InsertHeaderTest|class InsertHeader` in `.`  -> 191 chars | | 76 ms |
| 4 | 2.8 | API request | `claude-sonnet-5` blocks=tool_use,tool_use | 2 / 469 / 29,684 / 235 | 1342 ms api gap |
| 5 | 2.8 | tool | Read `Filter.java` (whole)  -> 63 lines | | 41 ms |
| 6 | 3.5 | tool | Read `InsertHeaderTest.java` (whole)  -> 126 lines | | 33 ms |
| 7 | 10.2 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 3,447 / 30,153 / 793 | 6685 ms api gap |
| 8 | 11.3 | tool | Grep `interface Transformation` in `Transformation.java` ERROR  -> 269 chars | | 30 ms |
| 9 | 12.5 | API request | `claude-sonnet-5` blocks=tool_use | 2 / 966 / 33,600 / 83 | 1183 ms api gap |
| 10 | 12.5 | tool | Grep `interface Transformation` in `.`  -> 94 chars | | 61 ms |
| 11 | 19.1 | API request | `claude-sonnet-5` blocks=text | 2 / 168 / 34,566 / 712 | 6506 ms api gap |

## 5. OpenTelemetry events

Event counts: {"hook_registered": 4, "user_prompt": 1, "hook_execution_start": 6, "hook_execution_complete": 6, "tool_decision": 6, "tool_result": 6, "api_request": 5, "assistant_response": 1}. Metrics seen: {"claude_code.session.count": 1, "claude_code.cost.usage": 5, "claude_code.token.usage": 5, "claude_code.active_time.total": 1}. Spans: {}.

API requests per OTel: 5, latency p50 2588.0 ms, max 7757.0 ms.

Tool decisions:

| tool | decision | source |
|---|---|---|
| Grep | accept | config |
| Grep | accept | config |
| Read | accept | config |
| Read | accept | config |
| Grep | accept | config |
| Grep | accept | config |

Per-request `api_request` events:

| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|
| claude-sonnet-5 | 2588 | 2 | 248 | 23995 | 5689 | 0.0215055 |
| claude-sonnet-5 | 2032 | 2 | 235 | 29684 | 469 | 0.009463300000000001 |
| claude-sonnet-5 | 7757 | 2 | 793 | 30153 | 3447 | 0.0225821 |
| claude-sonnet-5 | 1180 | 2 | 83 | 33600 | 966 | 0.009969 |
| claude-sonnet-5 | 6550 | 2 | 712 | 34566 | 168 | 0.0144572 |

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
  "Grep:Filter.java",
  "Grep:InsertHeaderTest.java",
  "Read (content entered context):Filter.java",
  "Read (content entered context):InsertHeaderTest.java"
 ],
 "first_target_touch_ts": "2026-09-15T00:07:18.652Z",
 "finding_requests": 1,
 "finding_cost_usd": 0.0215,
 "answering_requests": 4,
 "answering_cost_usd": 0.0565,
 "other_files_read": [],
 "target_read_lines_main": 189,
 "target_read_chars_main": 7755,
 "target_grep_chars_main": 284,
 "target_content_chars_any_tool": 8039,
 "target_content_tokens_est": 2009,
 "cost_recomputed_usd": 0.077977,
 "spotify_style_tokens_avoided": 0,
 "lucky": false,
 "cost_billed_main_usd": 0.07797710000000001,
 "cost_recon_diff_usd": -0.0
}
```

## 7. Final answer text

```
This confirms the interface — no need to read further, the `Filter` class already shows the concrete overrides.

**Filter's methods** (all overrides of `Transformation<R>`):

- `apply(R record)` — returns `null` unconditionally
- `version()` — returns `AppInfoParser.getVersion()`
- `config()` — returns the (empty) `CONFIG_DEF`
- `close()` — no-op
- `configure(Map<String, ?> configs)` — no-op

**What the `InsertHeaderTest` pattern actually exercises:**

- `apply()` — yes, via the `insertionWith*` tests, which build a record, call `xform.apply(...)`, and assert on the result
- `version()` — yes, via `testInsertHeaderVersionRetrievedFromAppInfoParser`, asserting `xform.version()` equals `AppInfoParser.getVersion()`
- `configure()` — only indirectly, and only because `InsertHeader` has config fields to validate (`configRejectsNullHeaderKey`, `configRejectsNullHeaderValue`). It's invoked as setup in every test, but never itself the subject of a meaningful assertion beyond those two rejection cases.

**Left untested by that pattern:**

- `config()` — `InsertHeaderTest` never calls `xform.config()`; for `Filter` there'd be nothing analogous to assert either, since `CONFIG_DEF` is empty.
- `close()` — never invoked/asserted anywhere in `InsertHeaderTest`.
- `configure()` in any meaningful sense — since `Filter.CONFIG_DEF` has no fields, there's no equivalent to the null-key/null-value rejection tests to port over. Following the pattern strictly, a `Filter` test would likely just call `configure(Collections.emptyMap())` as setup, without any dedicated assertion on `configure()`'s behavior.

So a `FilterTest` written by mimicking `InsertHeaderTest` would meaningfully cover only `apply()` and `version()`, leaving `config()`, `close()`, and any real validation of `configure()` untested.
```

