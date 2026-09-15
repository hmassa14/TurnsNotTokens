# Run report: `CT3__natural__shunt-strict__r2__20260915-134303`

Task **CT3** (small-file-control), prompt variant **natural**, arm **shunt-strict**, model `claude-sonnet-5`, Claude Code 2.1.272 (Claude Code), Kafka `0ffb4f5dd5`, started 2026-09-15T13:43:11.554721+00:00.

## 1. Headline numbers

| Metric | Value | Source |
|---|---|---|
| Cost, main session (list price) | $0.0400 | result.json `total_cost_usd` |
| Cost, worker calls | $0.0000 (0 calls) | worker/*.json |
| **Cost, total** | **$0.0400** | sum |
| Grade | score 1.0 , pass = True | grade.json (needle) |
| Target file found | True via Read (content entered context):BrokerState.java | transcript tool calls |
| Finding phase | 1 requests, $0.0205 | requests before the first touch of the target file |
| Answering phase | 2 requests, $0.0195 | requests from the first touch onward |
| Wall clock | 7288 ms (harness), 5399 ms (CLI) | meta.json / result.json |
| Time waiting on API | 5208 ms | result.json `duration_api_ms` |
| Turns | 3 | result.json |
| API requests | 3 (main 3) | transcript, deduped by requestId |
| Tool calls | 2 : {"Grep": 1, "Read": 1} | transcript |
| Models used | claude-sonnet-5 | transcript `message.model` |
| Subagents spawned | 0 {} | result.json |
| Exit / timeout | 0 / False | meta.json |

## 2. Tokens and price per token

Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.

| Bucket | Tokens | Rate ($/M) | Cost |
|---|---|---|---|
| input (uncached) | 6 | 2.0 | $0.0000 |
| cache write, 1h TTL | 0 | 4.0 | $0.0000 |
| cache write, 5m TTL | 7,909 | 2.5 | $0.0198 |
| cache read | 84,104 | 0.2 | $0.0168 |
| output | 335 | 10.0 | $0.0034 |

Recomputed from tokens: $0.0400 vs reported $0.0400.
Cache TTL split: 5m = 7,909, 1h = 0. Thinking tokens: 28.

Per model, from result.json `modelUsage`:

| Model | Input | Output | Cache write | Cache read | Cost |
|---|---|---|---|---|---|
| claude-sonnet-5 | 6 | 335 | 7,909 | 84,104 | $0.0400 |

Cross-check, transcript usage summed once per requestId:

| Model | Requests | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|
| claude-sonnet-5 | 3 | 6 | 7,909 | 84,104 | 335 |

Cross-check, OpenTelemetry `claude_code.token.usage`:

| model | type | tokens |
|---|---|---|
| claude-sonnet-5 | input | 6 |
| claude-sonnet-5 | output | 335 |
| claude-sonnet-5 | cacheRead | 84,104 |
| claude-sonnet-5 | cacheCreation | 7,909 |

OTel `claude_code.cost.usage`: {"claude-sonnet-5": 0.0399553}

## 3. Reading behavior

| Counter | Value |
|---|---|
| reads_total | 1 |
| reads_whole_file | 1 |
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
| lines_entered_context | 108 |
| files_read | ['BrokerState.java'] |

## 4. Timeline

Every API request and tool call in order. Latency for a tool is tool_use timestamp to tool_result timestamp. The `api gap` on a request is the time since the previous tool result landed, which approximates the API round trip.

| # | t+ (s) | Kind | Detail | Tokens (in / cw / cr / out) | Latency |
|---|---|---|---|---|---|
| 1 | 0.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 5,694 / 23,995 / 145 |  |
| 2 | 0.7 | tool | Grep `PENDING_CONTROLLED_SHUTDOWN` in `.`  -> 1123 chars | | 78 ms |
| 3 | 2.4 | API request | `claude-sonnet-5` blocks=tool_use | 2 / 731 / 29,689 / 115 | 1616 ms api gap |
| 4 | 2.4 | tool | Read `BrokerState.java` (whole)  -> 108 lines | | 39 ms |
| 5 | 3.8 | API request | `claude-sonnet-5` blocks=text | 2 / 1,484 / 30,420 / 75 | 1354 ms api gap |

## 5. OpenTelemetry events

Event counts: {"hook_registered": 4, "user_prompt": 1, "hook_execution_start": 2, "api_request": 3, "hook_execution_complete": 2, "tool_decision": 2, "tool_result": 2, "assistant_response": 1}. Metrics seen: {"claude_code.session.count": 1, "claude_code.cost.usage": 3, "claude_code.token.usage": 3, "claude_code.active_time.total": 1}. Spans: {}.

API requests per OTel: 3, latency p50 1668.0 ms, max 1998.0 ms.

Tool decisions:

| tool | decision | source |
|---|---|---|
| Grep | accept | config |
| Read | accept | config |

Per-request `api_request` events:

| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|
| claude-sonnet-5 | 1998 | 2 | 145 | 23995 | 5694 | 0.020488 |
| claude-sonnet-5 | 1668 | 2 | 115 | 29689 | 731 | 0.0089193 |
| claude-sonnet-5 | 1324 | 2 | 75 | 30420 | 1484 | 0.010548 |

## 6. Grade

```json
{
 "score": 1.0,
 "pass": true,
 "pass_lenient": true,
 "strict_match": true,
 "identifiers_missing": [],
 "grader": "needle",
 "content_score": 1.0,
 "content_pass": true,
 "target_found": true,
 "target_files_found": [
  "BrokerState.java"
 ],
 "target_files_missing": [],
 "found_via": [
  "Read (content entered context):BrokerState.java"
 ],
 "first_target_touch_ts": "2026-09-15T13:43:16.997Z",
 "finding_requests": 1,
 "finding_cost_usd": 0.0205,
 "answering_requests": 2,
 "answering_cost_usd": 0.0195,
 "other_files_read": [],
 "target_read_lines_main": 108,
 "target_read_chars_main": 3054,
 "target_grep_chars_main": 0,
 "target_content_chars_any_tool": 3054,
 "target_content_tokens_est": 763,
 "cost_recomputed_usd": 0.039955,
 "spotify_style_tokens_avoided": 0,
 "lucky": false,
 "cost_billed_main_usd": 0.0399553,
 "cost_recon_diff_usd": -0.0
}
```

## 7. Final answer text

```
`PENDING_CONTROLLED_SHUTDOWN` carries the byte value `6`. For unrecognized values, `BrokerState.fromValue` returns the `UNKNOWN` constant (value `127`).
```

