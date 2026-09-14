# Run report: `SB3__natural__shunt-strict__r3__20260914-202636`

Task **SB3** (spotify-benchmark-1to1), prompt variant **natural**, arm **shunt-strict**, model `claude-sonnet-5`, Claude Code 2.1.270 (Claude Code), Kafka `0ffb4f5dd5`, started 2026-09-14T20:26:40.134655+00:00.

## 1. Headline numbers

| Metric | Value | Source |
|---|---|---|
| Cost, main session (list price) | $0.1640 | result.json `total_cost_usd` |
| Cost, worker calls | $0.0000 (0 calls) | worker/*.json |
| **Cost, total** | **$0.1640** | sum |
| Grade | score 0.867 , pass = True | grade.json (key_list) |
| Target file found | True via Agent:Filter.java, Agent:InsertHeaderTest.java, Glob@subagent:agent-ad1e2b6f97e4bfee4:Filter.java | transcript tool calls |
| Finding phase | 1 requests, $0.0250 | requests before the first touch of the target file |
| Answering phase | 7 requests, $0.1390 | requests from the first touch onward |
| Wall clock | 63168 ms (harness), 8972 ms (CLI) | meta.json / result.json |
| Time waiting on API | 62518 ms | result.json `duration_api_ms` |
| Turns | 1 | result.json |
| API requests | 8 (main 3) | transcript, deduped by requestId |
| Tool calls | 11 : {"Agent": 1, "Bash": 2, "Glob": 4, "Read": 4} | transcript |
| Models used | claude-sonnet-5 | transcript `message.model` |
| Subagents spawned | 1 {"Explore": 1} | result.json |
| Exit / timeout | 0 / False | meta.json |

## 2. Tokens and price per token

Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.

| Bucket | Tokens | Rate ($/M) | Cost |
|---|---|---|---|
| input (uncached) | 2 | 2.0 | $0.0000 |
| cache write, 1h TTL | 0 | 4.0 | $0.0000 |
| cache write, 5m TTL | 3,264 | 2.5 | $0.0082 |
| cache read | 30,717 | 0.2 | $0.0061 |
| output | 601 | 10.0 | $0.0060 |

Recomputed from tokens: $0.0203 vs reported $0.1640.
Cache TTL split: 5m = 3,264, 1h = 0. Thinking tokens: 0.

Per model, from result.json `modelUsage`:

| Model | Input | Output | Cache write | Cache read | Cost |
|---|---|---|---|---|---|
| claude-sonnet-5 | 16 | 5,126 | 32,607 | 156,047 | $0.1640 |

Cross-check, transcript usage summed once per requestId:

| Model | Requests | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|
| claude-sonnet-5 | 8 | 16 | 32,607 | 156,047 | 5,126 |

Cross-check, OpenTelemetry `claude_code.token.usage`:

| model | type | tokens |
|---|---|---|
| claude-sonnet-5 | input | 16 |
| claude-sonnet-5 | output | 5,126 |
| claude-sonnet-5 | cacheRead | 156,047 |
| claude-sonnet-5 | cacheCreation | 32,607 |

OTel `claude_code.cost.usage`: {"claude-sonnet-5": 0.16401889999999997}

## 3. Reading behavior

| Counter | Value |
|---|---|
| reads_total | 4 |
| reads_whole_file | 4 |
| reads_targeted | 0 |
| reads_blocked_by_hook | 0 |
| reads_gated_by_stock | 0 |
| reads_dedup_reminders | 0 |
| hook_bypass_via_paging | 0 |
| bash_reads | 0 |
| agent_spawns | 1 |
| agent_spawn_models | ['claude-sonnet-5'] |
| skill_invocations | 0 |
| worker_calls | 0 |
| reread_after_delegation | 0 |
| edits | 0 |
| lines_entered_context | 0 |
| files_read | ['Filter.java', 'InsertHeader.java', 'InsertHeaderTest.java', 'Transformation.java'] |

## 4. Timeline

Every API request and tool call in order. Latency for a tool is tool_use timestamp to tool_result timestamp. The `api gap` on a request is the time since the previous tool result landed, which approximates the API round trip.

| # | t+ (s) | Kind | Detail | Tokens (in / cw / cr / out) | Latency |
|---|---|---|---|---|---|
| 1 | 0.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 5,715 / 23,949 / 596 |  |
| 2 | 5.0 | tool | Agent subagent_type=Explore : Find Kafka Connect Filter transform and InsertHeader test pa **agent_spawn** -> 1112 chars | | 23 ms |
| 3 | 7.2 | API request [subagent:agent-ad1e2b6f97e4bfee4] | `claude-sonnet-5` blocks=thinking,tool_use,tool_use,tool_use,tool_use | 2 / 14,626 / 0 / 315 | 2190 ms api gap |
| 4 | 7.5 | API request | `claude-sonnet-5` blocks=text | 2 / 1,053 / 29,664 / 60 | 2528 ms api gap |
| 5 | 8.7 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Bash `find /home/user/WackyWords/shunt-eval/runs/_ws/SB3__natural__shunt-strict__r3__20260914-20`  -> 578 chars | | 414 ms |
| 6 | 8.9 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Glob {"pattern": "**/Filter.java"}  -> 80 chars | | 45 ms |
| 7 | 9.8 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Glob {"pattern": "**/InsertHeader*.java"}  -> 177 chars | | 55 ms |
| 8 | 9.8 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Glob {"pattern": "**/FilterTest.java"}  -> 14 chars | | 42 ms |
| 9 | 11.9 | API request [subagent:agent-ad1e2b6f97e4bfee4] | `claude-sonnet-5` blocks=text,tool_use,tool_use,tool_use | 2 / 863 / 14,626 / 422 | 2025 ms api gap |
| 10 | 13.5 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Read `Filter.java` (whole)  -> 63 lines | | 49 ms |
| 11 | 14.0 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Read `InsertHeader.java` (whole)  -> 84 lines | | 42 ms |
| 12 | 14.6 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Read `InsertHeaderTest.java` (whole)  -> 126 lines | | 41 ms |
| 13 | 18.2 | API request [subagent:agent-ad1e2b6f97e4bfee4] | `claude-sonnet-5` blocks=thinking,tool_use,tool_use | 2 / 5,055 / 15,489 / 375 | 3583 ms api gap |
| 14 | 20.1 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Bash `find /home/user/WackyWords/shunt-eval/runs/_ws/SB3__natural__shunt-strict__r3__20260914-20`  -> 31 chars | | 88 ms |
| 15 | 20.4 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Glob {"pattern": "**/Transformation.java"}  -> 81 chars | | 39 ms |
| 16 | 23.5 | API request [subagent:agent-ad1e2b6f97e4bfee4] | `claude-sonnet-5` blocks=tool_use | 2 / 514 / 20,544 / 129 | 3121 ms api gap |
| 17 | 23.5 | tool [subagent:agent-ad1e2b6f97e4bfee4] | Read `Transformation.java` (whole)  -> 74 lines | | 53 ms |
| 18 | 48.2 | API request [subagent:agent-ad1e2b6f97e4bfee4] | `claude-sonnet-5` blocks=text | 2 / 1,517 / 21,058 / 2,628 | 24613 ms api gap |
| 19 | 57.3 | API request | `claude-sonnet-5` blocks=text | 2 / 3,264 / 30,717 / 601 | 33692 ms api gap |

## 5. OpenTelemetry events

Event counts: {"hook_registered": 2, "user_prompt": 2, "tool_decision": 11, "tool_result": 11, "api_request": 8, "assistant_response": 4, "hook_execution_start": 6, "hook_execution_complete": 6, "subagent_completed": 1}. Metrics seen: {"claude_code.session.count": 1, "claude_code.cost.usage": 8, "claude_code.token.usage": 8, "claude_code.active_time.total": 2}. Spans: {}.

API requests per OTel: 8, latency p50 5693.0 ms, max 24459.0 ms.

Tool decisions:

| tool | decision | source |
|---|---|---|
| Agent | accept | config |
| Bash | accept | config |
| Glob | accept | config |
| Glob | accept | config |
| Glob | accept | config |
| Read | accept | config |
| Read | accept | config |
| Read | accept | config |
| Bash | accept | config |
| Glob | accept | config |
| Read | accept | config |

Per-request `api_request` events:

| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|
| claude-sonnet-5 | 8029 | 2 | 596 | 23949 | 5715 | 0.0250413 |
| claude-sonnet-5 | 2512 | 2 | 60 | 29664 | 1053 | 0.0091693 |
| claude-sonnet-5 | 4801 | 2 | 315 | 0 | 14626 | 0.039719 |
| claude-sonnet-5 | 4722 | 2 | 422 | 14626 | 863 | 0.0093067 |
| claude-sonnet-5 | 5693 | 2 | 375 | 15489 | 5055 | 0.0194893 |
| claude-sonnet-5 | 3317 | 2 | 129 | 20544 | 514 | 0.006687800000000001 |
| claude-sonnet-5 | 24459 | 2 | 2628 | 21058 | 1517 | 0.0342881 |
| claude-sonnet-5 | 8939 | 2 | 601 | 30717 | 3264 | 0.0203174 |

## 6. Grade

```json
{
 "score": 0.867,
 "pass": true,
 "recall": 1.0,
 "missing": [],
 "invented": [],
 "groups": [
  "pattern: 2/3"
 ],
 "grader": "key_list",
 "content_score": 0.867,
 "content_pass": true,
 "target_found": true,
 "target_files_found": [
  "Filter.java",
  "InsertHeaderTest.java"
 ],
 "target_files_missing": [],
 "found_via": [
  "Agent:Filter.java",
  "Agent:InsertHeaderTest.java",
  "Glob@subagent:agent-ad1e2b6f97e4bfee4:Filter.java",
  "Glob@subagent:agent-ad1e2b6f97e4bfee4:InsertHeaderTest.java",
  "Read@subagent:agent-ad1e2b6f97e4bfee4 (content entered context):Filter.java",
  "Read@subagent:agent-ad1e2b6f97e4bfee4 (content entered context):InsertHeaderTest.java"
 ],
 "first_target_touch_ts": "2026-09-14T20:26:50.426Z",
 "finding_requests": 1,
 "finding_cost_usd": 0.025,
 "answering_requests": 7,
 "answering_cost_usd": 0.139,
 "other_files_read": [
  "InsertHeader.java",
  "Transformation.java"
 ],
 "target_read_lines_main": 0,
 "target_read_chars_main": 0,
 "target_grep_chars_main": 0,
 "target_content_chars_any_tool": 0,
 "target_content_tokens_est": 0,
 "cost_recomputed_usd": 0.164019,
 "spotify_style_tokens_avoided": 1238,
 "lucky": false,
 "cost_billed_main_usd": 0.16401889999999997,
 "cost_recon_diff_usd": 0.0
}
```

## 7. Final answer text

```
## Filter's methods

`Filter<R extends ConnectRecord<R>>` implements `Transformation<R>` and defines just five methods, all trivial (no branches):

| Method | Behavior |
|---|---|
| `apply(R record)` | Always returns `null` — unconditionally drops every record. |
| `version()` | Returns `AppInfoParser.getVersion()`. |
| `config()` | Returns a static empty `ConfigDef`. |
| `close()` | No-op. |
| `configure(Map<String, ?> configs)` | No-op — ignores the argument, no validation. |

(There's no `FilterTest.java` in the repo currently — it's untested entirely.)

## InsertHeaderTest's pattern

`InsertHeaderTest` tests by: instantiating the transform, calling `configure(...)`, then either calling `apply(record)` and asserting the result, or asserting `configure` throws `ConfigException` on bad input — plus one dedicated test asserting `version()` matches `AppInfoParser.getVersion()`. Notably, it **never calls `config()` or `close()`** even for InsertHeader.

## What that pattern would cover for Filter, and what it'd miss

**Covered:** `apply` (single scenario suffices — always returns `null`, no branches to exercise), `configure` (no-op, no validation logic to trigger `ConfigException` on), `version` (identical `assertEquals(AppInfoParser.getVersion(), ...)` check).

**Left untested:** `config()` and `close()` — the InsertHeaderTest pattern doesn't exercise either of these interface methods at all, so following it verbatim for Filter would leave both untested (that `config()` returns the empty `CONFIG_DEF`, and that `close()` is a safe no-op).
```

