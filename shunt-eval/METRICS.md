# Metrics deep dive: what to pull, from where, and how to price it

This is the extraction plan for every number the write-up needs: tools used, models used, tokens consumed, price per token, latency, and whether the output was correct. It is written against Claude Code v2.1.269 and checked against real records from two headless runs in this environment. Where a field name appears, it is the actual field name observed, not a guess.

Two worked examples run through the whole document: **R1**, a bulk-read question (the reading workflow), and **D1**, the planted concurrency bug (the debugging workflow). Both are defined in `TASKS.md`.

## 1. The three data sources and what each one is good for

| Source | Where it comes from | Best for | Weakness |
|---|---|---|---|
| **Result JSON** | stdout of `claude -p ... --output-format json` | Totals: cost, per-model tokens, turns, wall time, subagent counts, the final answer text | No per-call detail, no tool list |
| **Transcript JSONL** | `~/.claude/projects/<encoded cwd>/<session-id>.jsonl` plus `<session-id>/subagents/agent-*.jsonl` | Every tool call with its input and result, per-request usage and model, timestamps, hook denials, subagent transcripts | Needs deduplication (section 3.2); no dollar figure |
| **OpenTelemetry** | OTLP export to a local receiver | Cross-check of tokens and cost, hook decisions as first-class events, per-API-call latency, hook execution time | Extra moving part; if it fails the run is still complete from the other two |

Plus one source the harness creates itself: **worker JSON files** in arm B, one per `claude -p --model haiku` call the shunt scripts make, since those are separate processes the main session knows nothing about.

## 2. Result JSON: the totals

Observed on a real run (Haiku, two turns, one blocked Read):

```json
{
  "duration_ms": 6082,
  "duration_api_ms": 961,
  "num_turns": 2,
  "total_cost_usd": 0.015891,
  "usage": {
    "input_tokens": 18,
    "cache_creation_input_tokens": 5029,
    "cache_read_input_tokens": 35550,
    "output_tokens": 452,
    "cache_creation": {"ephemeral_1h_input_tokens": 5029, "ephemeral_5m_input_tokens": 0}
  },
  "modelUsage": {
    "claude-haiku-4-5-20251001": {
      "inputTokens": 18, "outputTokens": 452,
      "cacheReadInputTokens": 35550, "cacheCreationInputTokens": 5029,
      "costUSD": 0.015891, "costBasis": "list", "provider": "firstParty"
    }
  },
  "subagent_stats": {"spawned": 0, "completed": 0, "by_type": {}},
  "permission_denials": [],
  "result": "The tool returned an error: ..."
}
```

What each field feeds:

- `total_cost_usd` is `cost_usd_main`. It is computed locally at list price (`costBasis: "list"`), so it is the same number whether the account is on a subscription or API billing.
- `modelUsage` is the per-model breakdown. In arm C the Haiku Explore subagent shows up here as a second key, so main-vs-worker cost in arm C comes straight from this object. In arm B it does not, because the worker is a separate process.
- `usage` splits input into three buckets that are priced differently (section 4).
- `cache_creation.ephemeral_1h_input_tokens` and `ephemeral_5m_input_tokens` split cache writes by TTL. Claude Code writes the system prompt and tools with the 1-hour TTL and the conversation body (file contents, tool results) with the 5-minute TTL. The two are priced differently, so the split is needed to recompute cost (section 4).
- `subagent_stats.by_type` gives Agent spawns per subagent type; `spawned` and `completed` give counts.
- `permission_denials` lists tool calls a permission rule denied. Hook denials do not appear here; they show up in the transcript as tool results (section 3.4).
- `result` is the final answer text. This is what the `key_list` and `bug_report` graders read.
- `duration_ms` is wall time inside the CLI; `duration_api_ms` is time spent waiting on the API. Their difference is tool execution plus overhead.

## 3. Transcript JSONL: the per-call detail

### 3.1 Record types

Each line is a JSON object with a `type`. The ones that matter:

- `type: "user"` with a string `message.content` is the task prompt.
- `type: "assistant"` is one content block of a model response. `message.model` names the model, `message.usage` carries the usage for the whole API request, `requestId` identifies the request, `timestamp` is when the block landed. `message.content[0].type` is `thinking`, `text`, or `tool_use`. For `tool_use`, `message.content[0].name` is the tool and `.input` is its arguments.
- `type: "user"` with a list `message.content` containing `tool_result` blocks is a tool result. Each block has `tool_use_id` (links to the `tool_use` block's `id`), `is_error`, and `content`. The record also carries `toolUseResult`, a structured version of the result, and `timestamp`.
- `type: "attachment"`, `queue-operation`, `last-prompt`, `atis-latch` are bookkeeping and can be skipped.

### 3.2 The double-count trap

One API request produces one `assistant` record per content block, and every one of them repeats the same `usage`. Observed: a request that returned a thinking block and a tool_use block wrote two records, both with `input_tokens: 10, cache_creation_input_tokens: 4702, cache_read_input_tokens: 15424, output_tokens: 228` and both with `requestId: req_011CeyoW56LpKh9rqkuqGPX3`.

So the parser must group `assistant` records by `requestId` and count usage once per request. Summing across records overstates tokens by the average number of blocks per response, which is 2 to 3 on an agentic run. This is the single most likely way to get the token numbers wrong.

### 3.3 Tools used

For each `assistant` record whose content block is `tool_use`:

- `name` is the tool: `Read`, `Grep`, `Glob`, `Bash`, `Edit`, `Write`, `Agent`, `Skill`, and so on.
- `input` is the arguments. For `Read`: `file_path`, optional `offset`, optional `limit`. For `Bash`: `command`. For `Agent`: `subagent_type`, `prompt`, `description`. For `Skill`: `skill`, `args`.
- The block's `id` (a `toolu_...` string) is the join key to its result.

Derived per run:

| Metric | Rule |
|---|---|
| `reads_total` | count of `Read` tool_use |
| `reads_targeted` | `Read` with `offset` or `limit` present |
| `reads_whole_file` | `Read` with neither |
| `bash_reads` | `Bash` whose command starts with `cat`, `head`, `tail`, `less`, `more` (Spotify's own regex) |
| `agent_spawns` | count of `Agent` tool_use; `subagent_type` gives the type |
| `skill_invocations` | count of `Skill` tool_use; in arm B, `skill == "bulk-reader"` or `"code-writer"` |
| `worker_calls` (arm B) | `Bash` whose command contains `scripts/bulk-read` or `scripts/code-write`, cross-checked against worker JSON files |
| `edits` | count of `Edit` plus `Write` |
| `tool_mix` | histogram of `name` |

### 3.4 Tool results and what they reveal

Join each `tool_result` to its `tool_use` by id. Then classify the result content:

| Signal | Match on result content | Meaning |
|---|---|---|
| Hook denial (arm B, C) | starts with `File is N lines (threshold: 350)` (Spotify's block reason) and `is_error` true | the hook fired |
| Stock byte gate | contains `exceeds maximum allowed size (256KB)` | stock Claude Code refused the read |
| Stock token page | contains `[Truncated: PARTIAL view` | stock returned the first page only |
| Re-read dedupe | starts with `<system-reminder>This file is already in your context` or `File unchanged since last read` | Claude tried to re-read; nothing new entered context |
| Successful read | `cat -n` style numbered lines | count the lines that entered context |

Observed example of the byte gate, verbatim: `File content (457.8KB) exceeds maximum allowed size (256KB). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.` with `is_error: true`.

Derived:

- `reads_blocked_by_hook`, `reads_gated_by_stock`, `reads_dedup_reminders`.
- `hook_bypass_via_paging`: a hook denial or stock gate on file F, followed within the next 3 tool calls by a `Read` of F with `offset` or `limit`. This is the interaction between Spotify's allow-rule and Claude Code's own gates.
- `reread_after_delegation`: file F was sent to the worker (arm B, from the bulk-read command's `--paths`) or to Explore (arm C, from the Agent prompt text), and later F appears in a `Read` by the main agent. This is the "did not trust the summary" signal.
- `lines_entered_context`: for every successful `Read`, the count of numbered lines in the result. Summed, this is the ledger version of what Spotify estimates as characters / 4.

### 3.5 Per-tool latency

`tool_use` record timestamp to its `tool_result` record timestamp. Observed: a blocked Read went from `15:44:05.179Z` to `15:44:05.195Z`, 16 ms. A worker call in arm B will be tens of seconds, and this is where that shows up.

Per-API-call latency: the gap between the last `tool_result` timestamp and the first `assistant` record of the next `requestId`. OTel's `api_request` event has the exact figure; the transcript gives an approximation good to about 100 ms.

### 3.6 Models used

`message.model` on each `assistant` record. Group by `requestId` and by model to get requests per model and tokens per model. The main transcript has the main model; each file under `subagents/` has its own model on its own `assistant` records. In arm C, the Explore subagent's file should show `claude-haiku-4-5-...` if the `Explore.md` override took effect. If it shows the main model, the override did not apply and the arm is invalid. Check this on the first pilot run.

### 3.7 Subagent transcripts

`<session-id>/subagents/agent-<id>.jsonl` has the same record shape as the main transcript. Parse it the same way. The subagent's tokens are already included in the main run's `modelUsage` and `total_cost_usd`; parse the file for its tool list and read counts, not to add its cost again.

## 4. Price per token and the cost formula

Rate card, Anthropic first-party list price per million tokens. Cache write is 1.25x input on the 5-minute TTL and 2x on the 1-hour TTL. Cache read is 0.1x input, except Fable 5.1 at 0.025x.

| Model | Input | Output | Cache write, 1h TTL | Cache read |
|---|---|---|---|---|
| claude-haiku-4-5 | $1.00 | $5.00 | $2.00 | $0.10 |
| claude-sonnet-5 | $2.00 | $10.00 | $4.00 | $0.20 |
| claude-opus-5 | $5.00 | $25.00 | $10.00 | $0.50 |
| claude-fable-5-1 | $10.00 | $50.00 | $20.00 | $0.25 |

Cost of one request:

```
cost = input_tokens                      * input_rate
     + cache_write_tokens_1h_ttl         * 2.00 * input_rate
     + cache_write_tokens_5m_ttl         * 1.25 * input_rate
     + cache_read_input_tokens           * 0.10 * input_rate   (0.025 on Fable 5.1)
     + output_tokens                     * output_rate
```

The TTL split comes from `usage.cache_creation.ephemeral_1h_input_tokens` and `ephemeral_5m_input_tokens`. Claude Code writes the system prompt and tool definitions with the 1-hour TTL and the conversation body (file contents, tool results) with the 5-minute TTL, and the two are priced differently. Ignoring the split overstates cost: on the R1 baseline run the naive all-at-2x formula gave $0.2224 against a reported $0.2017; with the split it gives $0.2017 exactly.

Check against real runs:

| Run | Model | Input | Write 1h | Write 5m | Read | Output | Recomputed | Reported |
|---|---|---|---|---|---|---|---|---|
| smoke | haiku-4-5 | 10 | 5,162 | 0 | 27,808 | 43 | $0.013330 | $0.0133298 |
| R1 stock | sonnet-5 | 6 | 29,487 | 13,771 | 59,364 | 3,744 | $0.2017 | $0.2017 |
| D1 stock | sonnet-5 | 4 | 5,577 | 17,954 | 53,225 | 4,741 | $0.1253 | $0.1253 |

So `total_cost_usd` is "list price with the correct TTL multipliers", and the harness recomputes it from tokens as a check on every run.

Why this matters for the experiment: a big file read in Claude Code is paid **twice the input rate** the first time (cache write) and **a tenth of the input rate** on every later turn that carries it (cache read). Spotify's characters / 4 estimate prices every token at 1x. That mismatch is the JetBrains finding in miniature and the harness reports both numbers side by side.

Worker cost in arm B: each worker JSON file has its own `total_cost_usd` and `usage`. Sum them into `cost_usd_worker`. The worker runs Haiku with a system prompt that is the same on every call, so expect `cache_read_input_tokens` to climb after the first call and the file contents to land in `input_tokens` at 1x.

## 5. OpenTelemetry: the cross-check and the per-call clock

Enable with `CLAUDE_CODE_ENABLE_TELEMETRY=1`, `OTEL_METRICS_EXPORTER=otlp`, `OTEL_LOGS_EXPORTER=otlp`, `OTEL_EXPORTER_OTLP_PROTOCOL=http/json`, `OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318`, short export intervals, and `OTEL_LOG_TOOL_DETAILS=1` so tool parameters are included. Tag every run with `OTEL_RESOURCE_ATTRIBUTES=run.id=<run-id>`.

Metrics (from the binary and the monitoring docs):

- `claude_code.token.usage` with attributes `type` (input, output, cacheRead, cacheCreation) and `model`. Summed per run and per model this must match section 2. If it does not, the transcript dedupe is wrong or a worker process was missed.
- `claude_code.cost.usage` in USD, attribute `model`.

Log events:

- `tool_decision` with `decision` (accept or reject), `source` (which rule or hook decided), `tool_name`, `tool_use_id`, `tool_parameters`. In arms B and C, a rejected Read with a source naming the hook is `reads_blocked_by_hook`, counted independently of the transcript.
- `tool_result` with `success` and `duration_ms`.
- `api_request` with `model`, `duration_ms`, and token counts: the exact per-call latency, and the source for `api_latency_ms_p50` and `api_latency_ms_max`.

Spans: `claude_code.llm_request`, `claude_code.tool.execution`, `claude_code.hook` (hook execution time, arms B and C), `claude_code.subagent.spawn`.

The receiver is a small HTTP server that writes each POST body to disk. The parser groups by `run.id`. If the OTel path fails on a run, the row is still complete from the JSON and the transcript; OTel confirms them and adds the latency detail.

## 6. Correct output: the four graders

| Grader | Input | Output | Used by |
|---|---|---|---|
| `key_list` | `result` text from result JSON | recall over required identifiers, penalty per invented item, pass at 0.9 | R1 to R4 |
| `compile_and_checklist` | workspace after the run | compile exit code plus regex checklist, pass if all pass | W1 to W3 |
| `exact_diff` | `git diff` of the workspace | binary: exactly the expected hunk and nothing else | E1 to E3 |
| `bug_report` | `result` text | binary: right method, a line within tolerance, a race description, no credit for listed false positives | D1, D2 |

`key_list` matching is case-insensitive substring on identifiers. Invented items are checked against a per-task deny list built from things in the same file that look right but are wrong, so a hallucinated helper name or a private method listed as public is caught. Every grader is self-tested against a right and a wrong answer before the grid.

Quality summary per task and arm: pass rate over three reps, and pass^3 (all three passed), which is the number that shows variance an enforcement mechanism is supposed to remove.

## 7. Worked example: R1, the reading workflow

Task: list the twelve event classes in `BrokerLifecycleManager.java` (770 lines, 33 KB) and the states they set.

**Arm A, stock.** Expected shape: Claude reads the file whole with one `Read` (770 lines is under the 2,000-line default page and under the 25k-token cap), maybe a `Grep` for `implements EventQueue.Event` first. The transcript shows one or two `tool_use` blocks, `reads_whole_file` = 1, `lines_entered_context` = 770. Cost is one request that writes about 10k tokens of file to cache at 2x, plus one or two follow-up requests that read them back at 0.1x. Answer text is graded by `key_list`.

**Arm B, shunt.** Expected shape: Claude calls `Read`, the hook denies it, the transcript shows a `tool_result` starting `File is 770 lines (threshold: 350)`. Claude invokes the `bulk-reader` skill, then runs `scripts/bulk-read --question ... --paths server/.../BrokerLifecycleManager.java` through `Bash`. That script writes `worker/1.json` with the Haiku call's cost, and the tool result is Haiku's bullet summary. `reads_blocked_by_hook` = 1, `worker_calls` = 1, `lines_entered_context` = 0 from this file, `spotify_style_tokens_avoided` = 33,318 / 4 minus the summary's length / 4. If Claude then reads the file anyway with an offset (`hook_bypass_via_paging`) or after the summary (`reread_after_delegation`), those counters catch it, and the cost includes both the worker call and the read.

**Arm C, hook plus Haiku Explore.** Same denial, then an `Agent` tool_use with `subagent_type: "Explore"`. The subagent file under `subagents/` shows Haiku reading the file; the main transcript shows only the returned text. `agent_spawns` = 1, `modelUsage` has two keys, and the Explore file's `model` field is the check that the pin worked.

The numbers to put side by side for R1: `cost_usd_total` per arm, `tokens_main_cache_creation` (the ledger version of "what Claude read"), `spotify_style_tokens_avoided`, `wall_ms`, and `score`. The prediction from section 4 is that B's main-model savings are real but B's worker cost plus the 10 to 30 second delegation partly cancel them, and that the quality gap depends on whether Haiku preserved the odd names.

## 8. Worked example: D1, the debugging workflow

Task: find the planted race in `StateDirectory.java` (1,019 lines, 46 KB) after `synchronized` was removed from `lock`.

**Arm A.** Claude reads the file whole, or greps for `synchronized` and `lockedTasksToOwner` and then reads around the hits. The answer needs the `get` at 509 and the `put` at 523 in view together, and the fact that `unlock` is still synchronized. `bug_report` checks for `lock`, a line near 504 to 525, and a race description.

**Arm B.** The hook denies the whole-file read. Claude asks the bulk-reader "what thread-safety problems are in this file". Haiku's summary either names the missing `synchronized` on `lock` or it does not. Spotify's own account is that the worker missed exactly this kind of bug. If the summary misses it, Claude either accepts the summary (fail, and `reread_after_delegation` = 0) or distrusts it and pages through the file with offset reads (`hook_bypass_via_paging` counts them, cost goes up, and the run may still pass). Both outcomes are findings. The per-run row records which one happened.

**Arm C.** Same, with Haiku Explore in the worker seat, and the Explore prompt is the main agent's own question rather than Spotify's mode instructions.

The numbers to put side by side for D1: `pass` per arm and per rep, `pass^3`, `cost_usd_total`, `reread_after_delegation`, `hook_bypass_via_paging`, and `lines_entered_context`. The claim being tested is Spotify's own: that reasoning tasks cannot be delegated to the cheap model. The interesting result is whether the hook makes Claude worse at the task, or just more expensive at it.

## 9. Per-run row

Everything above lands in one JSON row in `results/runs.jsonl`. Field list, grouped:

```
identity:   run_id task_id category arm rep main_model claude_code_version kafka_commit started_at
cost:       cost_usd_main cost_usd_worker cost_usd_total cost_usd_by_model
tokens:     tokens_main_input_uncached tokens_main_cache_creation tokens_main_cache_read
            tokens_main_output tokens_worker_input tokens_worker_output tokens_by_model
            spotify_style_tokens_avoided lines_entered_context
latency:    wall_ms duration_ms duration_api_ms api_calls api_latency_ms_p50 api_latency_ms_max
            hook_ms_total worker_ms_total time_to_first_delegation_ms
behavior:   num_turns tool_mix reads_total reads_targeted reads_whole_file reads_blocked_by_hook
            reads_gated_by_stock hook_bypass_via_paging bash_reads_blocked agent_spawns
            agent_spawn_models skill_invocations worker_calls reread_after_delegation
            reads_dedup_reminders edits timeout max_turns_hit is_error
quality:    score pass grader_notes
```

## 10. Validation before trusting any of it

1. On one stock run, compare token totals three ways: result JSON `usage`, transcript summed by `requestId`, OTel `claude_code.token.usage`. All three must agree. If the transcript is high, the dedupe is broken.
2. Recompute `total_cost_usd` from tokens and the rate card. Must match to the fifth decimal, as it did on the smoke run.
3. On one arm B run, confirm `worker/*.json` files exist and their count equals `worker_calls` from the transcript.
4. On one arm C run, open the subagent transcript and confirm `model` is Haiku.
5. Run each grader on its answer key and on a wrong answer.
