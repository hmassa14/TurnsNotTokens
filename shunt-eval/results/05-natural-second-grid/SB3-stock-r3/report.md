# Run report: `SB3__natural__stock__r3__20260914-202550`

Task **SB3** (spotify-benchmark-1to1), prompt variant **natural**, arm **stock**, model `claude-sonnet-5`, Claude Code 2.1.270 (Claude Code), Kafka `0ffb4f5dd5`, started 2026-09-14T20:25:55.560049+00:00.

## 1. Headline numbers

| Metric | Value | Source |
|---|---|---|
| Cost, main session (list price) | $0.1179 | result.json `total_cost_usd` |
| Cost, worker calls | $0.0000 (0 calls) | worker/*.json |
| **Cost, total** | **$0.1179** | sum |
| Grade | score 0.867 , pass = True | grade.json (key_list) |
| Target file found | True via Bash:Filter.java, Bash:InsertHeaderTest.java, Bash:Filter.java | transcript tool calls |
| Finding phase | 2 requests, $0.0308 | requests before the first touch of the target file |
| Answering phase | 6 requests, $0.0872 | requests from the first touch onward |
| Wall clock | 37429 ms (harness), 35407 ms (CLI) | meta.json / result.json |
| Time waiting on API | 32386 ms | result.json `duration_api_ms` |
| Turns | 9 | result.json |
| API requests | 8 (main 8) | transcript, deduped by requestId |
| Tool calls | 8 : {"Bash": 6, "Read": 2} | transcript |
| Models used | claude-sonnet-5 | transcript `message.model` |
| Subagents spawned | 0 {} | result.json |
| Exit / timeout | 0 / False | meta.json |

## 2. Tokens and price per token

Main session, from result.json `usage`. Cache writes are split by TTL: the 1-hour entries (system prompt and tools) cost 2x input, the 5-minute entries (file contents and tool results) cost 1.25x input.

| Bucket | Tokens | Rate ($/M) | Cost |
|---|---|---|---|
| input (uncached) | 16 | 2.0 | $0.0000 |
| cache write, 1h TTL | 0 | 4.0 | $0.0000 |
| cache write, 5m TTL | 14,902 | 2.5 | $0.0373 |
| cache read | 249,974 | 0.2 | $0.0500 |
| output | 3,063 | 10.0 | $0.0306 |

Recomputed from tokens: $0.1179 vs reported $0.1179.
Cache TTL split: 5m = 14,902, 1h = 0. Thinking tokens: 1,063.

Per model, from result.json `modelUsage`:

| Model | Input | Output | Cache write | Cache read | Cost |
|---|---|---|---|---|---|
| claude-sonnet-5 | 16 | 3,063 | 14,902 | 249,974 | $0.1179 |

Cross-check, transcript usage summed once per requestId:

| Model | Requests | Input | Cache write | Cache read | Output |
|---|---|---|---|---|---|
| claude-sonnet-5 | 8 | 16 | 14,902 | 249,974 | 3,063 |

Cross-check, OpenTelemetry `claude_code.token.usage`:

| model | type | tokens |
|---|---|---|
| claude-sonnet-5 | input | 16 |
| claude-sonnet-5 | output | 3,063 |
| claude-sonnet-5 | cacheRead | 249,974 |
| claude-sonnet-5 | cacheCreation | 14,902 |

OTel `claude_code.cost.usage`: {"claude-sonnet-5": 0.11791180000000001}

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
| 1 | 0.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 5,592 / 23,949 / 300 |  |
| 2 | 0.9 | tool | Bash `find / -maxdepth 6 -iname "*kafka*" -type d 2>/dev/null \| grep -v proc \| head -50`  -> 217 chars | | 672 ms |
| 3 | 2.7 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 482 / 29,541 / 186 | 1131 ms api gap |
| 4 | 3.6 | tool | Bash `find /tmp/kafka-src -iname "Filter.java" -path "*transforms*"; find /tmp/kafka-src -iname `  -> 31 chars | | 123 ms |
| 5 | 5.6 | API request | `claude-sonnet-5` blocks=tool_use | 2 / 240 / 30,023 / 168 | 1851 ms api gap |
| 6 | 5.6 | tool | Bash `ls /tmp/kafka-src \| head -50; echo ---; find /tmp/kafka-src -iname "*Filter*" 2>/dev/null;`  -> 235 chars | | 118 ms |
| 7 | 7.2 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 352 / 30,263 / 235 | 1546 ms api gap |
| 8 | 8.3 | tool | Bash `cat /tmp/kafka-src/AGENTS.md 2>/dev/null \| head -50; echo ---; find / -iname "InsertHeader`  -> 8333 chars | | 1911 ms |
| 9 | 11.2 | API request | `claude-sonnet-5` blocks=text,tool_use | 2 / 3,196 / 30,615 / 194 | 984 ms api gap |
| 10 | 12.2 | tool | Bash `find /home/user/WackyWords/shunt-eval/runs/_ws/SB3__natural__stock__r3__20260914-202550/co`  -> 173 chars | | 59 ms |
| 11 | 13.4 | API request | `claude-sonnet-5` blocks=text,tool_use,tool_use | 2 / 324 / 33,811 / 290 | 1172 ms api gap |
| 12 | 14.1 | tool | Read `Filter.java` (whole)  -> 63 lines | | 29 ms |
| 13 | 14.8 | tool | Read `InsertHeaderTest.java` (whole)  -> 126 lines | | 13 ms |
| 14 | 24.0 | API request | `claude-sonnet-5` blocks=thinking,tool_use | 2 / 3,502 / 34,135 / 947 | 9232 ms api gap |
| 15 | 24.9 | tool | Bash `find /home/user/WackyWords/shunt-eval/runs/_ws/SB3__natural__stock__r3__20260914-202550/co`  -> 164 chars | | 62 ms |
| 16 | 32.0 | API request | `claude-sonnet-5` blocks=text | 2 / 1,214 / 37,637 / 743 | 7060 ms api gap |

## 5. OpenTelemetry events

Event counts: {"user_prompt": 1, "tool_decision": 8, "api_request": 8, "tool_result": 8, "assistant_response": 3}. Metrics seen: {"claude_code.session.count": 1, "claude_code.cost.usage": 8, "claude_code.token.usage": 8, "claude_code.active_time.total": 1}. Spans: {}.

API requests per OTel: 8, latency p50 2644.0 ms, max 10011.0 ms.

Tool decisions:

| tool | decision | source |
|---|---|---|
| Bash | accept | config |
| Bash | accept | config |
| Bash | accept | config |
| Bash | accept | config |
| Bash | accept | config |
| Read | accept | config |
| Read | accept | config |
| Bash | accept | config |

Per-request `api_request` events:

| model | duration_ms | input | output | cache_read | cache_creation | cost_usd |
|---|---|---|---|---|---|---|
| claude-sonnet-5 | 4153 | 2 | 300 | 23949 | 5592 | 0.0217738 |
| claude-sonnet-5 | 2077 | 2 | 186 | 29541 | 482 | 0.008977200000000001 |
| claude-sonnet-5 | 1886 | 2 | 168 | 30023 | 240 | 0.0082886 |
| claude-sonnet-5 | 2644 | 2 | 235 | 30263 | 352 | 0.0092866 |
| claude-sonnet-5 | 1958 | 2 | 194 | 30615 | 3196 | 0.016057000000000002 |
| claude-sonnet-5 | 2548 | 2 | 290 | 33811 | 324 | 0.0104762 |
| claude-sonnet-5 | 10011 | 2 | 947 | 34135 | 3502 | 0.025056000000000002 |
| claude-sonnet-5 | 7079 | 2 | 743 | 37637 | 1214 | 0.0179964 |

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
  "Bash:Filter.java",
  "Bash:InsertHeaderTest.java",
  "Bash:Filter.java",
  "Bash:InsertHeaderTest.java",
  "Read (content entered context):Filter.java",
  "Read (content entered context):InsertHeaderTest.java"
 ],
 "first_target_touch_ts": "2026-09-14T20:26:04.067Z",
 "finding_requests": 2,
 "finding_cost_usd": 0.0308,
 "answering_requests": 6,
 "answering_cost_usd": 0.0872,
 "other_files_read": [],
 "target_read_lines_main": 189,
 "target_read_chars_main": 7755,
 "target_grep_chars_main": 8537,
 "target_content_chars_any_tool": 16292,
 "target_content_tokens_est": 4073,
 "cost_recomputed_usd": 0.117912,
 "spotify_style_tokens_avoided": 0,
 "lucky": false,
 "cost_billed_main_usd": 0.11791180000000001,
 "cost_recon_diff_usd": 0.0
}
```

## 7. Final answer text

```
This confirms `Transformation<R>` declares `apply`, `config`, `close`, plus `configure`/`version` from its parent interfaces (`Configurable`, `Versioned`). No need to read it further — I have what's needed.

## Filter's methods

`Filter<R>` implements `Transformation<R>`, which pulls in five methods:

- `apply(R record)` — returns `null` unconditionally (drops the record)
- `version()` — delegates to `AppInfoParser.getVersion()`
- `config()` — returns the (empty) `CONFIG_DEF`
- `close()` — no-op
- `configure(Map<String, ?> configs)` — no-op

## What InsertHeaderTest's pattern covers

`InsertHeaderTest` exercises exactly three kinds of things:
1. **configure() + apply() together** — build a config, call `configure`, call `apply`, assert on the result (the three `insertion*` tests)
2. **configure() validation failures** — assert `configure` throws `ConfigException` on bad input (the two `configRejects*` tests)
3. **version()** — asserted directly against `AppInfoParser.getVersion()`

`close()` and `config()` are never called or asserted on anywhere in `InsertHeaderTest`.

## Applying that pattern to Filter

- `apply()` — **covered**: configure with the empty config, call `apply` on some record, assert the result is `null` (and unaffected by input).
- `version()` — **covered**: same direct `assertEquals(AppInfoParser.getVersion(), xform.version())` test translates directly.
- `configure()` — **partially covered**: it gets exercised as setup in the `apply` test, but the `configRejects*`-style tests don't translate, since `Filter.CONFIG_DEF` is empty and `configure()` has nothing to validate/reject.

## Left untested by this pattern

- **`close()`** — never invoked in InsertHeaderTest, so a Filter test following the same pattern wouldn't invoke it either.
- **`config()`** — never invoked in InsertHeaderTest, so it wouldn't be asserted for Filter either (e.g., that `config()` returns the empty `CONFIG_DEF`).
```

