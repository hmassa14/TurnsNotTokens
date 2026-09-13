# Run report: `E1__natural__shunt-strict__r1__20260912-182745`

Task **E1** (precise-edit), prompt variant **natural**, arm **shunt-strict**, model `claude-sonnet-5`, Claude Code 2.1.269 (Claude Code), Kafka `0ffb4f5dd5`, started 2026-09-12T18:27:47.016376+00:00.

## 1. Headline numbers

| Metric | Value | Source |
|---|---|---|
| Cost, main session (list price) | $0.0868 | result.json `total_cost_usd` |
| Cost, worker calls | $0.0000 (0 calls) | worker/*.json |
| **Cost, total** | **$0.0868** | sum |
| Grade | score 1.0 , pass = True | grade.json (exact_diff) |
| Target file found | True via Grep:SharePartitionManager.java, Read:SharePartitionManager.java, Grep:SharePartitionManager.java | transcript tool calls |
| Finding phase | 1 requests, $0.0288 | requests before the first touch of the target file |
| Answering phase | 5 requests, $0.0580 | requests from the first touch onward |
| Wall clock | 18843 ms (harness), 17220 ms (CLI) | meta.json / result.json |
| Time waiting on API | 17031 ms | result.json `duration_api_ms` |
| Turns | 6 | result.json |
| API requests | 6 (main 6) | transcript, deduped by requestId |
| Tool calls | 5 : {"Grep": 3, "Read": 1, "Edit": 1} | transcript |
| Models used | claude-sonnet-5 | transcript `message.model` |
| Subagents spawned | 0 {} | result.json |
| Exit / timeout | 0 / False | meta.json |

## 2. Tokens and price per token

Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.

| Bucket | Tokens | Rate ($/M) | Cost |
|---|---|---|---|
| input (uncached) | 12 | 2.0 | $0.0000 |
| cache write, 1h TTL | 9,942 | 4.0 | $0.0398 |
| cache write, 5m TTL | 0 | 2.5 | $0.0000 |
| cache read | 177,355 | 0.2 | $0.0355 |
| output | 1,154 | 10.0 | $0.0115 |

Recomputed from tokens: $0.0868 vs reported $0.0868.
Cache TTL split: 5m = 0, 1h = 9,942. Thinking tokens: 99.

Per model, from result.json `modelUsage`:

| Model | Input | Output | Cache write | Cache read | Cost |
|---|---|---|---|---|---|
| claude-sonnet-5 | 12 | 1,154 | 9,942 | 177,355 | $0.0868 |

Cross-check, transcript usage summed once per requestId:

| Model | Requests | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|
| claude-sonnet-5 | 6 | 12 | 9,942 | 177,355 | 1,154 |

Cross-check, OpenTelemetry `claude_code.token.usage`:

| model | type | tokens |
|---|---|---|
| claude-sonnet-5 | input | 12 |
| claude-sonnet-5 | output | 1,154 |
| claude-sonnet-5 | cacheRead | 177,355 |
| claude-sonnet-5 | cacheCreation | 9,942 |

OTel `claude_code.cost.usage`: {"claude-sonnet-5": 0.08680299999999999}

## 3. Reading behavior

| Counter | Value |
|---|---|
| reads_total | 1 |
| reads_whole_file | 0 |
| reads_targeted | 1 |
| reads_blocked_by_hook | 1 |
| reads_gated_by_stock | 0 |
| reads_dedup_reminders | 0 |
| hook_bypass_via_paging | 0 |
| bash_reads | 0 |
| agent_spawns | 0 |
| agent_spawn_models | [] |
| skill_invocations | 0 |
| worker_calls | 0 |
| reread_after_delegation | 0 |
| edits | 1 |
| lines_entered_context | 0 |
| files_read | ['SharePartitionManager.java'] |

## 4. Timeline

Every API request and tool call in order. Latency for a tool is tool_use timestamp to tool_result timestamp. The `api gap` on a request is the time since the previous tool result landed, which approximates the API round trip.

| # | t+ (s) | Kind | Detail | Tokens (in / cw / cr / out) | Latency |
|---|---|---|---|---|---|
| 1 | 0.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 5,719 / 23,824 / 117 |  |
| 2 | 0.1 | tool | Grep `no such share session found` in `.`  -> 647 chars | | 51 ms |
| 3 | 1.8 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 369 / 29,543 / 190 | 1634 ms api gap |
| 4 | 3.2 | tool | Read `SharePartitionManager.java` offset=380 limit=260 ERROR **hook_blocked** -> 206 chars | | 29 ms |
| 5 | 6.0 | API request | `claude-sonnet-5` blocks=tool_use | 2 / 314 / 29,912 / 213 | 2775 ms api gap |
| 6 | 6.0 | tool | Grep `void release|private.*release|Share session error|` in `SharePartitionManager.java`  -> 77 chars | | 19 ms |
| 7 | 8.1 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 291 / 30,226 / 296 | 2122 ms api gap |
| 8 | 9.4 | tool | Grep `Share session error` in `SharePartitionManager.java`  -> 6906 chars | | 14 ms |
| 9 | 11.6 | API request | `claude-sonnet-5` blocks=text,tool_use | 2 / 2,816 / 30,517 / 287 | 2161 ms api gap |
| 10 | 13.5 | tool | Edit {"replace_all": "False", "file_path": "/home/user/WackyWords/shunt-eval/runs/_w", "old_string": "        if (cache.remove(key) == null) {"} **edit** -> 259 chars | | 42 ms |
| 11 | 15.3 | API request | `claude-sonnet-5` blocks=text | 2 / 433 / 33,333 / 51 | 1732 ms api gap |

## 5. OpenTelemetry events

Event counts: {"hook_registered": 2, "user_prompt": 1, "tool_decision": 5, "api_request": 6, "tool_result": 4, "hook_execution_start": 1, "hook_execution_complete": 1, "assistant_response": 2}. Metrics seen: {"claude_code.session.count": 1, "claude_code.cost.usage": 6, "claude_code.token.usage": 6, "claude_code.lines_of_code.count": 1, "claude_code.code_edit_tool.decision": 1, "claude_code.active_time.total": 1}. Spans: {}.

API requests per OTel: 6, latency p50 3029.0 ms, max 4092.0 ms.

Tool decisions:

| tool | decision | source |
|---|---|---|
| Grep | accept | config |
| Read | reject | hook |
| Grep | accept | config |
| Grep | accept | config |
| Edit | accept | config |

Per-request `api_request` events:

| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|
| claude-sonnet-5 | 1938 | 2 | 117 | 23824 | 5719 | 0.0288148 |
| claude-sonnet-5 | 3029 | 2 | 190 | 29543 | 369 | 0.0092886 |
| claude-sonnet-5 | 2784 | 2 | 213 | 29912 | 314 | 0.009372400000000001 |
| claude-sonnet-5 | 3432 | 2 | 296 | 30226 | 291 | 0.0101732 |
| claude-sonnet-5 | 4092 | 2 | 287 | 30517 | 2816 | 0.0202414 |
| claude-sonnet-5 | 1740 | 2 | 51 | 33333 | 433 | 0.0089126 |

## 6. Grade

```json
{
 "score": 1.0,
 "pass": true,
 "changed_lines": 2,
 "extra_changes": 0,
 "grader": "exact_diff",
 "content_score": 1.0,
 "content_pass": true,
 "target_found": true,
 "target_files_found": [
  "SharePartitionManager.java"
 ],
 "target_files_missing": [],
 "found_via": [
  "Grep:SharePartitionManager.java",
  "Read:SharePartitionManager.java",
  "Grep:SharePartitionManager.java",
  "Grep:SharePartitionManager.java",
  "Edit:SharePartitionManager.java"
 ],
 "first_target_touch_ts": "2026-09-12T18:27:50.262Z",
 "finding_requests": 1,
 "finding_cost_usd": 0.0288,
 "answering_requests": 5,
 "answering_cost_usd": 0.058,
 "other_files_read": [],
 "spotify_style_tokens_avoided": 0
}
```

## 7. Final answer text

```
Done — line 426 in `releaseSession` now logs at `warn` level; the other two `error` occurrences (line 534, 568) are unchanged.
```

