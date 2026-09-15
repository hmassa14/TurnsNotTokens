# Run report: `SC3__natural__shunt__r1__20260915-010113`

Task **SC3** (spotify-shape-scaled), prompt variant **natural**, arm **shunt**, model `claude-sonnet-5`, Claude Code 2.1.271 (Claude Code), Kafka `0ffb4f5dd5`, started 2026-09-15T01:01:21.596967+00:00.

## 1. Headline numbers

| Metric | Value | Source |
|---|---|---|
| Cost, main session (list price) | $0.1113 | result.json `total_cost_usd` |
| Cost, worker calls | $0.0000 (0 calls) | worker/*.json |
| **Cost, total** | **$0.1113** | sum |
| Grade | score 1.0 , pass = True | grade.json (key_list) |
| Target file found | True via Glob:BatchAccumulator.java, Glob:BatchAccumulatorTest.java, Read:BatchAccumulator.java | transcript tool calls |
| Finding phase | 1 requests, $0.0202 | requests before the first touch of the target file |
| Answering phase | 8 requests, $0.0911 | requests from the first touch onward |
| Wall clock | 35951 ms (harness), 34108 ms (CLI) | meta.json / result.json |
| Time waiting on API | 33734 ms | result.json `duration_api_ms` |
| Turns | 9 | result.json |
| API requests | 9 (main 9) | transcript, deduped by requestId |
| Tool calls | 8 : {"Bash": 1, "Glob": 1, "Read": 2, "Grep": 4} | transcript |
| Models used | claude-sonnet-5 | transcript `message.model` |
| Subagents spawned | 0 {} | result.json |
| Exit / timeout | 0 / False | meta.json |

## 2. Tokens and price per token

Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.

| Bucket | Tokens | Rate ($/M) | Cost |
|---|---|---|---|
| input (uncached) | 18 | 2.0 | $0.0000 |
| cache write, 1h TTL | 0 | 4.0 | $0.0000 |
| cache write, 5m TTL | 13,248 | 2.5 | $0.0331 |
| cache read | 276,129 | 0.2 | $0.0552 |
| output | 2,296 | 10.0 | $0.0230 |

Recomputed from tokens: $0.1113 vs reported $0.1113.
Cache TTL split: 5m = 13,248, 1h = 0. Thinking tokens: 206.

Per model, from result.json `modelUsage`:

| Model | Input | Output | Cache write | Cache read | Cost |
|---|---|---|---|---|---|
| claude-sonnet-5 | 18 | 2,296 | 13,248 | 276,129 | $0.1113 |

Cross-check, transcript usage summed once per requestId:

| Model | Requests | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|
| claude-sonnet-5 | 9 | 18 | 13,248 | 276,129 | 2,296 |

Cross-check, OpenTelemetry `claude_code.token.usage`:

| model | type | tokens |
|---|---|---|
| claude-sonnet-5 | input | 18 |
| claude-sonnet-5 | output | 2,296 |
| claude-sonnet-5 | cacheRead | 276,129 |
| claude-sonnet-5 | cacheCreation | 13,248 |

OTel `claude_code.cost.usage`: {"claude-sonnet-5": 0.11134180000000002}

## 3. Reading behavior

| Counter | Value |
|---|---|
| reads_total | 2 |
| reads_whole_file | 1 |
| reads_targeted | 1 |
| reads_blocked_by_hook | 1 |
| reads_gated_by_stock | 0 |
| reads_dedup_reminders | 0 |
| hook_bypass_via_paging | 1 |
| bash_reads | 0 |
| agent_spawns | 0 |
| agent_spawn_models | [] |
| skill_invocations | 0 |
| worker_calls | 0 |
| reread_after_delegation | 0 |
| edits | 0 |
| lines_entered_context | 110 |
| files_read | ['BatchAccumulator.java'] |

## 4. Timeline

Every API request and tool call in order. Latency for a tool is tool_use timestamp to tool_result timestamp. The `api gap` on a request is the time since the previous tool result landed, which approximates the API round trip.

| # | t+ (s) | Kind | Detail | Tokens (in / cw / cr / out) | Latency |
|---|---|---|---|---|---|
| 1 | 0.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 5,665 / 23,995 / 125 |  |
| 2 | 0.4 | tool | Bash `find / -iname "BatchAccumulator*.java" 2>/dev/null` ERROR **sandbox_blocked** -> 160 chars | | 36 ms |
| 3 | 2.2 | API request | `claude-sonnet-5` blocks=tool_use | 2 / 238 / 29,660 / 61 | 1817 ms api gap |
| 4 | 2.2 | tool | Glob {"pattern": "**/BatchAccumulator*.java"}  -> 149 chars | | 63 ms |
| 5 | 4.4 | API request | `claude-sonnet-5` blocks=tool_use | 2 / 178 / 29,898 / 116 | 2131 ms api gap |
| 6 | 4.4 | tool | Read `BatchAccumulator.java` (whole) ERROR **hook_blocked** -> 223 chars | | 29 ms |
| 7 | 6.7 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 241 / 30,076 / 232 | 2271 ms api gap |
| 8 | 7.6 | tool | Grep `public\s+[\w<>\[\],? ]+\s+\w+\(` in `BatchAccumulator.java`  -> 840 chars | | 38 ms |
| 9 | 10.5 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 603 / 30,317 / 282 | 2797 ms api gap |
| 10 | 11.4 | tool | Grep `^public class|^public final class|class CompletedB` in `BatchAccumulator.java`  -> 138 chars | | 36 ms |
| 11 | 13.5 | API request | `claude-sonnet-5` blocks=text,tool_use | 2 / 381 / 30,920 / 187 | 2013 ms api gap |
| 12 | 14.4 | tool | Read `BatchAccumulator.java` offset=81 limit=110  -> 110 lines | | 36 ms |
| 13 | 16.6 | API request | `claude-sonnet-5` blocks=text,tool_use | 2 / 1,924 / 31,301 / 330 | 2128 ms api gap |
| 14 | 19.1 | tool | Grep `\.(append|allowDrain|appendControlMessages|appendV` in `BatchAccumulatorTest.java`  -> 7057 chars | | 36 ms |
| 15 | 22.5 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 3,512 / 33,225 / 313 | 3345 ms api gap |
| 16 | 24.4 | tool | Grep `appendVotersRecord|appendSnapshotHeaderRecord|appe` in `BatchAccumulatorTest.java`  -> 16 chars | | 32 ms |
| 17 | 30.8 | API request | `claude-sonnet-5` blocks=text | 2 / 506 / 36,737 / 650 | 6385 ms api gap |

## 5. OpenTelemetry events

Event counts: {"hook_registered": 4, "user_prompt": 1, "hook_execution_start": 8, "hook_execution_complete": 8, "tool_decision": 8, "api_request": 9, "tool_result": 6, "assistant_response": 3}. Metrics seen: {"claude_code.session.count": 1, "claude_code.cost.usage": 9, "claude_code.token.usage": 9, "claude_code.active_time.total": 1}. Spans: {}.

API requests per OTel: 9, latency p50 3588.0 ms, max 6404.0 ms.

Tool decisions:

| tool | decision | source |
|---|---|---|
| Bash | reject | hook |
| Glob | accept | config |
| Read | reject | hook |
| Grep | accept | config |
| Grep | accept | config |
| Read | accept | config |
| Grep | accept | config |
| Grep | accept | config |

Per-request `api_request` events:

| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|
| claude-sonnet-5 | 3588 | 2 | 125 | 23995 | 5665 | 0.0202155 |
| claude-sonnet-5 | 1808 | 2 | 61 | 29660 | 238 | 0.007141 |
| claude-sonnet-5 | 2132 | 2 | 116 | 29898 | 178 | 0.007588600000000001 |
| claude-sonnet-5 | 3173 | 2 | 232 | 30076 | 241 | 0.0089417 |
| claude-sonnet-5 | 3784 | 2 | 282 | 30317 | 603 | 0.0103949 |
| claude-sonnet-5 | 2913 | 2 | 187 | 30920 | 381 | 0.009010500000000001 |
| claude-sonnet-5 | 4719 | 2 | 330 | 31301 | 1924 | 0.0143742 |
| claude-sonnet-5 | 5187 | 2 | 313 | 33225 | 3512 | 0.018559 |
| claude-sonnet-5 | 6404 | 2 | 650 | 36737 | 506 | 0.0151164 |

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
  "Glob:BatchAccumulator.java",
  "Glob:BatchAccumulatorTest.java",
  "Read:BatchAccumulator.java",
  "Grep:BatchAccumulator.java",
  "Grep:BatchAccumulator.java",
  "Read (content entered context):BatchAccumulator.java"
 ],
 "first_target_touch_ts": "2026-09-15T01:01:28.564Z",
 "finding_requests": 1,
 "finding_cost_usd": 0.0202,
 "answering_requests": 8,
 "answering_cost_usd": 0.0911,
 "other_files_read": [],
 "target_read_lines_main": 110,
 "target_read_chars_main": 4672,
 "target_grep_chars_main": 8051,
 "target_content_chars_any_tool": 12723,
 "target_content_tokens_est": 3180,
 "cost_recomputed_usd": 0.111342,
 "spotify_style_tokens_avoided": 0,
 "lucky": false,
 "cost_billed_main_usd": 0.11134180000000002,
 "cost_recon_diff_usd": 0.0
}
```

## 7. Final answer text

```
Confirmed — no calls to those four methods anywhere in the test file. Here's the full picture of `BatchAccumulator`'s public API (top-level class; I've excluded the nested `CompletedBatch` class methods since the question is about `BatchAccumulator` itself, but noted them too):

**`BatchAccumulator<T>` public methods:**

| Method | Exercised by test? |
|---|---|
| `append(int, List<T>, boolean)` | ✅ yes |
| `allowDrain()` | ✅ yes |
| `appendControlMessages(MemoryRecordsCreator)` | ✅ yes |
| `appendVotersRecord(...)` | ❌ **no** |
| `appendLeaderChangeMessage(...)` | ✅ yes |
| `appendSnapshotHeaderRecord(...)` | ❌ **no** |
| `appendSnapshotFooterRecord(...)` | ❌ **no** |
| `forceDrain()` | ✅ yes |
| `needsDrain(long)` | ✅ yes |
| `timeUntilDrain(long)` | ✅ yes |
| `epoch()` | ❌ **no** |
| `drain()` | ✅ yes |
| `isEmpty()` | ✅ yes |
| `close()` | ✅ yes |

(The nested `CompletedBatch<T>` class's public methods — `sizeInBytes()`, `release()`, `appendTimestamp()`, `drainable(long)` — are all exercised, except `drainable(long)`, which is never called in the test.)

**Public methods never exercised by `BatchAccumulatorTest`:**
- `appendVotersRecord(...)`
- `appendSnapshotHeaderRecord(...)`
- `appendSnapshotFooterRecord(...)`
- `epoch()`
- (bonus, on the nested `CompletedBatch` class) `drainable(long)`
```

