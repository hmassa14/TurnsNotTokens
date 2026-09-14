# Run report: `SC3__natural__shunt-strict__r1__20260914-211032`

Task **SC3** (spotify-shape-scaled), prompt variant **natural**, arm **shunt-strict**, model `claude-sonnet-5`, Claude Code 2.1.270 (Claude Code), Kafka `0ffb4f5dd5`, started 2026-09-14T21:10:36.700588+00:00.

## 1. Headline numbers

| Metric | Value | Source |
|---|---|---|
| Cost, main session (list price) | $0.0931 | result.json `total_cost_usd` |
| Cost, worker calls | $0.0000 (0 calls) | worker/*.json |
| **Cost, total** | **$0.0931** | sum |
| Grade | score 1.0 , pass = True | grade.json (key_list) |
| Target file found | True via Bash:BatchAccumulatorTest.java, Read:BatchAccumulator.java, Read:BatchAccumulatorTest.java | transcript tool calls |
| Finding phase | 1 requests, $0.0213 | requests before the first touch of the target file |
| Answering phase | 6 requests, $0.0718 | requests from the first touch onward |
| Wall clock | 36724 ms (harness), 34850 ms (CLI) | meta.json / result.json |
| Time waiting on API | 33157 ms | result.json `duration_api_ms` |
| Turns | 8 | result.json |
| API requests | 7 (main 7) | transcript, deduped by requestId |
| Tool calls | 7 : {"Bash": 2, "Read": 2, "Grep": 3} | transcript |
| Models used | claude-sonnet-5 | transcript `message.model` |
| Subagents spawned | 0 {} | result.json |
| Exit / timeout | 0 / False | meta.json |

## 2. Tokens and price per token

Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.

| Bucket | Tokens | Rate ($/M) | Cost |
|---|---|---|---|
| input (uncached) | 14 | 2.0 | $0.0000 |
| cache write, 1h TTL | 0 | 4.0 | $0.0000 |
| cache write, 5m TTL | 10,456 | 2.5 | $0.0261 |
| cache read | 218,074 | 0.2 | $0.0436 |
| output | 2,331 | 10.0 | $0.0233 |

Recomputed from tokens: $0.0931 vs reported $0.0931.
Cache TTL split: 5m = 10,456, 1h = 0. Thinking tokens: 545.

Per model, from result.json `modelUsage`:

| Model | Input | Output | Cache write | Cache read | Cost |
|---|---|---|---|---|---|
| claude-sonnet-5 | 14 | 2,331 | 10,456 | 218,074 | $0.0931 |

Cross-check, transcript usage summed once per requestId:

| Model | Requests | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|
| claude-sonnet-5 | 7 | 14 | 10,456 | 218,074 | 2,331 |

Cross-check, OpenTelemetry `claude_code.token.usage`:

| model | type | tokens |
|---|---|---|
| claude-sonnet-5 | input | 14 |
| claude-sonnet-5 | output | 2,331 |
| claude-sonnet-5 | cacheRead | 218,074 |
| claude-sonnet-5 | cacheCreation | 10,456 |

OTel `claude_code.cost.usage`: {"claude-sonnet-5": 0.0930928}

## 3. Reading behavior

| Counter | Value |
|---|---|
| reads_total | 2 |
| reads_whole_file | 2 |
| reads_targeted | 0 |
| reads_blocked_by_hook | 2 |
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
| lines_entered_context | 0 |
| files_read | ['BatchAccumulator.java', 'BatchAccumulatorTest.java'] |

## 4. Timeline

Every API request and tool call in order. Latency for a tool is tool_use timestamp to tool_result timestamp. The `api gap` on a request is the time since the previous tool result landed, which approximates the API round trip.

| # | t+ (s) | Kind | Detail | Tokens (in / cw / cr / out) | Latency |
|---|---|---|---|---|---|
| 1 | 0.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 5,691 / 23,949 / 223 |  |
| 2 | 0.3 | tool | Bash `find / -iname "BatchAccumulator*.java" 2>/dev/null`  -> 3465 chars | | 1345 ms |
| 3 | 5.8 | API request | `claude-sonnet-5` blocks=text,tool_use,tool_use | 2 / 2,082 / 29,640 / 278 | 4178 ms api gap |
| 4 | 6.5 | tool | Read `BatchAccumulator.java` (whole) ERROR **hook_blocked** -> 124 chars | | 36 ms |
| 5 | 7.2 | tool | Read `BatchAccumulatorTest.java` (whole) ERROR **hook_blocked** -> 124 chars | | 32 ms |
| 6 | 9.8 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 466 / 31,722 / 226 | 2577 ms api gap |
| 7 | 10.5 | tool | Grep `^\s*public\s` in `BatchAccumulator.java`  -> 1206 chars | | 31 ms |
| 8 | 13.8 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 728 / 32,188 / 319 | 3209 ms api gap |
| 9 | 15.1 | tool | Bash `cd /home/user/WackyWords/shunt-eval/runs/_ws/SC3__natural__shunt-strict__r1__20260914-2110`  -> 305 chars | | 145 ms |
| 10 | 19.6 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 676 / 32,916 / 426 | 4443 ms api gap |
| 11 | 20.5 | tool | Grep `epoch\(|appendVotersRecord|appendSnapshotHeaderRec` in `BatchAccumulatorTest.java`  -> 16 chars | | 35 ms |
| 12 | 23.8 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 475 / 33,592 / 265 | 3219 ms api gap |
| 13 | 24.3 | tool | Grep `public long append\(|public boolean append\(` in `BatchAccumulator.java`  -> 76 chars | | 31 ms |
| 14 | 30.8 | API request | `claude-sonnet-5` blocks=text | 2 / 338 / 34,067 / 594 | 6467 ms api gap |

## 5. OpenTelemetry events

Event counts: {"hook_registered": 2, "user_prompt": 1, "hook_execution_start": 4, "hook_execution_complete": 4, "tool_decision": 7, "api_request": 7, "tool_result": 5, "assistant_response": 2}. Metrics seen: {"claude_code.session.count": 1, "claude_code.cost.usage": 7, "claude_code.token.usage": 7, "claude_code.active_time.total": 1}. Spans: {}.

API requests per OTel: 7, latency p50 4488.0 ms, max 6476.0 ms.

Tool decisions:

| tool | decision | source |
|---|---|---|
| Bash | accept | config |
| Read | reject | hook |
| Read | reject | hook |
| Grep | accept | config |
| Bash | accept | config |
| Grep | accept | config |
| Grep | accept | config |

Per-request `api_request` events:

| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|
| claude-sonnet-5 | 4258 | 2 | 223 | 23949 | 5691 | 0.0212513 |
| claude-sonnet-5 | 5538 | 2 | 278 | 29640 | 2082 | 0.013917000000000002 |
| claude-sonnet-5 | 3295 | 2 | 226 | 31722 | 466 | 0.0097734 |
| claude-sonnet-5 | 4488 | 2 | 319 | 32188 | 728 | 0.011451600000000001 |
| claude-sonnet-5 | 5321 | 2 | 426 | 32916 | 676 | 0.012537200000000002 |
| claude-sonnet-5 | 3754 | 2 | 265 | 33592 | 475 | 0.010559899999999999 |
| claude-sonnet-5 | 6476 | 2 | 594 | 34067 | 338 | 0.0136024 |

## 6. Grade

```json
{
 "score": 1.0,
 "pass": true,
 "recall": 1.0,
 "missing": [],
 "invented": [],
 "groups": [
  "never_called: 4/4"
 ],
 "grader": "key_list",
 "content_score": 1.0,
 "content_pass": true,
 "target_found": true,
 "target_files_found": [
  "BatchAccumulator.java",
  "BatchAccumulatorTest.java"
 ],
 "target_files_missing": [],
 "found_via": [
  "Bash:BatchAccumulatorTest.java",
  "Read:BatchAccumulator.java",
  "Read:BatchAccumulatorTest.java",
  "Grep:BatchAccumulator.java",
  "Bash:BatchAccumulatorTest.java",
  "Grep:BatchAccumulatorTest.java"
 ],
 "first_target_touch_ts": "2026-09-14T21:10:42.528Z",
 "finding_requests": 1,
 "finding_cost_usd": 0.0213,
 "answering_requests": 6,
 "answering_cost_usd": 0.0718,
 "other_files_read": [],
 "target_read_lines_main": 0,
 "target_read_chars_main": 0,
 "target_grep_chars_main": 5068,
 "target_content_chars_any_tool": 5068,
 "target_content_tokens_est": 1267,
 "cost_recomputed_usd": 0.093093,
 "spotify_style_tokens_avoided": 0,
 "lucky": false,
 "cost_billed_main_usd": 0.0930928,
 "cost_recon_diff_usd": 0.0
}
```

## 7. Final answer text

```
Only one `append` overload. Here's the full picture of `BatchAccumulator`'s public API (excluding the inner `CompletedBatch` class members, listed separately) and whether the test exercises it:

**Called by the test:**
- `BatchAccumulator(...)` constructor — used to build the accumulator under test
- `append(int epoch, List<T> records, boolean delayDrain)` — called extensively
- `appendControlMessages(MemoryRecordsCreator)` — called
- `appendLeaderChangeMessage(...)` — called
- `allowDrain()` — called
- `forceDrain()` — called
- `needsDrain(long currentTimeMs)` — called
- `timeUntilDrain(long currentTimeMs)` — called
- `drain()` — called
- `isEmpty()` — called
- `close()` — called

**Never called by the test:**
- `appendVotersRecord(...)` — not exercised
- `appendSnapshotHeaderRecord(...)` — not exercised
- `appendSnapshotFooterRecord(...)` — not exercised
- `epoch()` — not exercised (the accumulator's own epoch getter is never invoked, even though epoch values are passed *into* `append`)

**Inner class `CompletedBatch<T>` (also public, technically part of the type's public surface):**
- `sizeInBytes()` — called (1 use)
- `release()` — called
- `appendTimestamp()` — called
- `drainable(long)` — never called

So the gaps are `appendVotersRecord`, `appendSnapshotHeaderRecord`, `appendSnapshotFooterRecord`, and `epoch()` on `BatchAccumulator` itself, plus `CompletedBatch.drainable(long)` on the nested class.
```

