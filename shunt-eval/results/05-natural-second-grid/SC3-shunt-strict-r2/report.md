# Run report: `SC3__natural__shunt-strict__r2__20260914-211151`

Task **SC3** (spotify-shape-scaled), prompt variant **natural**, arm **shunt-strict**, model `claude-sonnet-5`, Claude Code 2.1.270 (Claude Code), Kafka `0ffb4f5dd5`, started 2026-09-14T21:11:53.731514+00:00.

## 1. Headline numbers

| Metric | Value | Source |
|---|---|---|
| Cost, main session (list price) | $0.2012 | result.json `total_cost_usd` |
| Cost, worker calls | $0.0000 (0 calls) | worker/*.json |
| **Cost, total** | **$0.2012** | sum |
| Grade | score 1.0 , pass = True | grade.json (key_list) |
| Target file found | True via Bash:BatchAccumulatorTest.java, Read:BatchAccumulator.java, Grep:BatchAccumulator.java | transcript tool calls |
| Finding phase | 1 requests, $0.0215 | requests before the first touch of the target file |
| Answering phase | 12 requests, $0.1797 | requests from the first touch onward |
| Wall clock | 61372 ms (harness), 59297 ms (CLI) | meta.json / result.json |
| Time waiting on API | 57611 ms | result.json `duration_api_ms` |
| Turns | 25 | result.json |
| API requests | 13 (main 13) | transcript, deduped by requestId |
| Tool calls | 24 : {"Bash": 2, "Read": 2, "Grep": 20} | transcript |
| Models used | claude-sonnet-5 | transcript `message.model` |
| Subagents spawned | 0 {} | result.json |
| Exit / timeout | 0 / False | meta.json |

## 2. Tokens and price per token

Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.

| Bucket | Tokens | Rate ($/M) | Cost |
|---|---|---|---|
| input (uncached) | 26 | 2.0 | $0.0001 |
| cache write, 1h TTL | 0 | 4.0 | $0.0000 |
| cache write, 5m TTL | 18,068 | 2.5 | $0.0452 |
| cache read | 443,378 | 0.2 | $0.0887 |
| output | 6,729 | 10.0 | $0.0673 |

Recomputed from tokens: $0.2012 vs reported $0.2012.
Cache TTL split: 5m = 18,068, 1h = 0. Thinking tokens: 1,294.

Per model, from result.json `modelUsage`:

| Model | Input | Output | Cache write | Cache read | Cost |
|---|---|---|---|---|---|
| claude-sonnet-5 | 26 | 6,729 | 18,068 | 443,378 | $0.2012 |

Cross-check, transcript usage summed once per requestId:

| Model | Requests | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|
| claude-sonnet-5 | 13 | 26 | 18,068 | 443,378 | 6,729 |

Cross-check, OpenTelemetry `claude_code.token.usage`:

| model | type | tokens |
|---|---|---|
| claude-sonnet-5 | input | 26 |
| claude-sonnet-5 | output | 6,729 |
| claude-sonnet-5 | cacheRead | 443,378 |
| claude-sonnet-5 | cacheCreation | 18,068 |

OTel `claude_code.cost.usage`: {"claude-sonnet-5": 0.2011876}

## 3. Reading behavior

| Counter | Value |
|---|---|
| reads_total | 2 |
| reads_whole_file | 1 |
| reads_targeted | 1 |
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
| files_read | ['BatchAccumulator.java'] |

## 4. Timeline

Every API request and tool call in order. Latency for a tool is tool_use timestamp to tool_result timestamp. The `api gap` on a request is the time since the previous tool result landed, which approximates the API round trip.

| # | t+ (s) | Kind | Detail | Tokens (in / cw / cr / out) | Latency |
|---|---|---|---|---|---|
| 1 | 0.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 5,691 / 23,949 / 246 |  |
| 2 | 0.7 | tool | Bash `find / -iname "BatchAccumulator*.java" 2>/dev/null`  -> 3465 chars | | 1269 ms |
| 3 | 2.9 | API request | `claude-sonnet-5` blocks=text,tool_use | 2 / 2,104 / 29,640 / 144 | 934 ms api gap |
| 4 | 3.6 | tool | Read `BatchAccumulator.java` (whole) ERROR **hook_blocked** -> 124 chars | | 31 ms |
| 5 | 4.8 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 242 / 31,744 / 216 | 1179 ms api gap |
| 6 | 6.0 | tool | Grep `public\s+[\w<>\[\],? ]+\s+\w+\s*\(` in `BatchAccumulator.java`  -> 85 chars | | 32 ms |
| 7 | 7.3 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 302 / 31,986 / 260 | 1260 ms api gap |
| 8 | 8.5 | tool | Grep `public\s+[\w<>\[\],? ]+\s+\w+\s*\(` in `BatchAccumulator.java`  -> 840 chars | | 32 ms |
| 9 | 11.7 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 631 / 32,288 / 434 | 3161 ms api gap |
| 10 | 13.3 | tool | Grep `^\s*(public|private|protected)\s+.*(class|interfac` in `BatchAccumulator.java`  -> 893 chars | | 29 ms |
| 11 | 15.4 | API request | `claude-sonnet-5` blocks=text,tool_use | 2 / 835 / 32,919 / 289 | 2065 ms api gap |
| 12 | 16.4 | tool | Read `BatchAccumulator.java` offset=100 limit=120 ERROR **hook_blocked** -> 124 chars | | 33 ms |
| 13 | 19.2 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 387 / 33,754 / 332 | 2781 ms api gap |
| 14 | 20.2 | tool | Bash `sed -n '100,240p' "/home/user/WackyWords/shunt-eval/runs/_ws/SC3__natural__shunt-strict__r`  -> 5288 chars | | 95 ms |
| 15 | 21.6 | API request | `claude-sonnet-5` blocks=text,tool_use | 2 / 2,128 / 34,141 / 320 | 1286 ms api gap |
| 16 | 23.2 | tool | Grep `\.(append|allowDrain|appendControlMessages|appendV` in `BatchAccumulatorTest.java`  -> 122 chars | | 24 ms |
| 17 | 26.6 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 565 / 36,269 / 400 | 3379 ms api gap |
| 18 | 27.6 | tool | Grep `\.append\(` in `BatchAccumulatorTest.java`  -> 122 chars | | 19 ms |
| 19 | 29.7 | API request | `claude-sonnet-5` blocks=tool_use,tool_use,tool_use,tool_use,tool_use,tool_use,tool_use,tool_use,tool_use,tool_use,tool_use,tool_use,tool_use | 2 / 501 / 36,834 / 2,418 | 2035 ms api gap |
| 20 | 29.7 | tool | Grep `\.allowDrain\(` in `BatchAccumulatorTest.java`  -> 119 chars | | 18 ms |
| 21 | 30.7 | tool | Grep `\.appendControlMessages\(` in `BatchAccumulatorTest.java`  -> 120 chars | | 17 ms |
| 22 | 31.8 | tool | Grep `\.appendVotersRecord\(` in `BatchAccumulatorTest.java`  -> 59 chars | | 17 ms |
| 23 | 32.9 | tool | Grep `\.appendLeaderChangeMessage\(` in `BatchAccumulatorTest.java`  -> 120 chars | | 19 ms |
| 24 | 34.0 | tool | Grep `\.appendSnapshotHeaderRecord\(` in `BatchAccumulatorTest.java`  -> 59 chars | | 20 ms |
| 25 | 35.1 | tool | Grep `\.appendSnapshotFooterRecord\(` in `BatchAccumulatorTest.java`  -> 59 chars | | 19 ms |
| 26 | 36.1 | tool | Grep `\.forceDrain\(` in `BatchAccumulatorTest.java`  -> 120 chars | | 19 ms |
| 27 | 37.2 | tool | Grep `\.needsDrain\(` in `BatchAccumulatorTest.java`  -> 122 chars | | 18 ms |
| 28 | 38.3 | tool | Grep `\.timeUntilDrain\(` in `BatchAccumulatorTest.java`  -> 122 chars | | 24 ms |
| 29 | 39.5 | tool | Grep `\.epoch\(` in `BatchAccumulatorTest.java`  -> 59 chars | | 18 ms |
| 30 | 40.4 | tool | Grep `\.drain\(` in `BatchAccumulatorTest.java`  -> 122 chars | | 17 ms |
| 31 | 41.5 | tool | Grep `\.isEmpty\(` in `BatchAccumulatorTest.java`  -> 120 chars | | 26 ms |
| 32 | 42.5 | tool | Grep `\.close\(` in `BatchAccumulatorTest.java`  -> 120 chars | | 36 ms |
| 33 | 48.4 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 3,521 / 37,335 / 758 | 5887 ms api gap |
| 34 | 49.6 | tool | Grep `epoch\(\)` in `BatchAccumulatorTest.java`  -> 16 chars | | 18 ms |
| 35 | 51.1 | API request | `claude-sonnet-5` blocks=text,tool_use | 2 / 807 / 40,856 / 305 | 1464 ms api gap |
| 36 | 52.6 | tool | Grep `appendVotersRecord|appendSnapshotHeaderRecord|appe` in `BatchAccumulatorTest.java`  -> 16 chars | | 19 ms |
| 37 | 57.2 | API request | `claude-sonnet-5` blocks=text | 2 / 354 / 41,663 / 607 | 4613 ms api gap |

## 5. OpenTelemetry events

Event counts: {"hook_registered": 2, "user_prompt": 1, "hook_execution_start": 4, "api_request": 13, "hook_execution_complete": 4, "tool_decision": 24, "tool_result": 22, "assistant_response": 5}. Metrics seen: {"claude_code.session.count": 1, "claude_code.cost.usage": 13, "claude_code.token.usage": 13, "claude_code.active_time.total": 1}. Spans: {}.

API requests per OTel: 13, latency p50 3006.0 ms, max 14841.0 ms.

Tool decisions:

| tool | decision | source |
|---|---|---|
| Bash | accept | config |
| Read | reject | hook |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Read | reject | hook |
| Bash | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |
| Grep | accept | config |

Per-request `api_request` events:

| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|
| claude-sonnet-5 | 2619 | 2 | 246 | 23949 | 5691 | 0.021481300000000002 |
| claude-sonnet-5 | 1670 | 2 | 144 | 29640 | 2104 | 0.012632 |
| claude-sonnet-5 | 2380 | 2 | 216 | 31744 | 242 | 0.0091178 |
| claude-sonnet-5 | 2497 | 2 | 260 | 31986 | 302 | 0.009756200000000001 |
| claude-sonnet-5 | 4755 | 2 | 434 | 32288 | 631 | 0.0123791 |
| claude-sonnet-5 | 2989 | 2 | 289 | 32919 | 835 | 0.0115653 |
| claude-sonnet-5 | 3821 | 2 | 332 | 33754 | 387 | 0.0110423 |
| claude-sonnet-5 | 2956 | 2 | 320 | 34141 | 2128 | 0.0153522 |
| claude-sonnet-5 | 4355 | 2 | 400 | 36269 | 565 | 0.012670300000000002 |
| claude-sonnet-5 | 14841 | 2 | 2418 | 36834 | 501 | 0.03280330000000001 |
| claude-sonnet-5 | 7071 | 2 | 758 | 37335 | 3521 | 0.0238535 |
| claude-sonnet-5 | 3006 | 2 | 305 | 40856 | 807 | 0.013242700000000001 |
| claude-sonnet-5 | 4603 | 2 | 607 | 41663 | 354 | 0.0152916 |

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
  "Grep:BatchAccumulator.java",
  "Grep:BatchAccumulator.java",
  "Grep:BatchAccumulator.java",
  "Read:BatchAccumulator.java"
 ],
 "first_target_touch_ts": "2026-09-14T21:11:57.955Z",
 "finding_requests": 1,
 "finding_cost_usd": 0.0215,
 "answering_requests": 12,
 "answering_cost_usd": 0.1797,
 "other_files_read": [],
 "target_read_lines_main": 0,
 "target_read_chars_main": 0,
 "target_grep_chars_main": 12168,
 "target_content_chars_any_tool": 12168,
 "target_content_tokens_est": 3042,
 "cost_recomputed_usd": 0.201188,
 "spotify_style_tokens_avoided": 0,
 "lucky": false,
 "cost_billed_main_usd": 0.2011876,
 "cost_recon_diff_usd": 0.0
}
```

## 7. Final answer text

```
Confirmed — none of these four appear anywhere in the test file at all.

## `BatchAccumulator<T>` public methods vs. `BatchAccumulatorTest`

| Method | Called in test? |
|---|---|
| `append(int, List<T>, boolean)` | ✅ Yes |
| `allowDrain()` | ✅ Yes |
| `appendControlMessages(MemoryRecordsCreator)` | ✅ Yes |
| `appendVotersRecord(...)` | ❌ **Never called** |
| `appendLeaderChangeMessage(...)` | ✅ Yes |
| `appendSnapshotHeaderRecord(...)` | ❌ **Never called** |
| `appendSnapshotFooterRecord(...)` | ❌ **Never called** |
| `forceDrain()` | ✅ Yes |
| `needsDrain(long)` | ✅ Yes |
| `timeUntilDrain(long)` | ✅ Yes |
| `epoch()` | ❌ **Never called** |
| `drain()` | ✅ Yes |
| `isEmpty()` | ✅ Yes |
| `close()` | ✅ Yes |

(Note: `MemoryRecordsCreator` is a public nested interface, and `CompletedBatch` has its own public methods (`sizeInBytes()`, `release()`, `appendTimestamp()`, `drainable()`) — those belong to the `CompletedBatch` inner class, not `BatchAccumulator` itself, so I excluded them from this list.)

**Four public methods of `BatchAccumulator` are never exercised by the unit test:** `appendVotersRecord`, `appendSnapshotHeaderRecord`, `appendSnapshotFooterRecord`, and `epoch()`.
```

