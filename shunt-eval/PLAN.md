# Evaluation plan: does Spotify's shunt beat what Claude Code already does?

Status: plan, not yet run. Dated 2026-09-12. Everything under "What I verified" was checked in this environment against Claude Code v2.1.269 unless a docs URL is given.

## 1. The question

Spotify's post claims a PreToolUse hook that blocks `Read` on files over 350 lines and redirects to a cheap worker cut Claude Code token usage by 90%. The shunt README's benchmark table, verified from the public `spotify/portal-ai-plugins` repo, is the whole basis for that number: a 162K-line Java monorepo, three bulk-read scenarios (33,684 to 5,737 tokens, 82%; 75,990 to 4,148, 94%; 16,221 to 821, 94%) and one code-write scenario with no percentage. The 90% is the mean of the three bulk-read rows. Tokens are estimated as characters divided by four (`evals/benchmarks.json`: "chars / 4 (conservative approximation for code)"), the worker's own tokens are not tabulated, and no dollar figure or task success rate appears in the repo. The Reddit and Hacker News pushback was that Claude Code already does this by default via subagents. Nobody in that argument measured anything.

The test asks three things, in order of how much they matter:

1. **Dollars, not tokens.** Does the enforced hook + cheap worker reduce the total bill for a task, once the worker's tokens and the main model's cache reads are counted?
2. **Quality.** Does it change whether the task gets done, especially on the two task types Spotify says delegation breaks: edits needing exact line numbers, and reasoning about a subtle bug?
3. **Is enforcement doing anything?** How often does stock Claude Code delegate or narrow reads on its own, and how much does the hook change that behavior?

## 2. What I verified about Claude Code's native approach

This is the part of the argument nobody checked. I pulled these from the installed CLI binary (strings of v2.1.269), the current docs, and a headless smoke test on the Kafka repo.

**Read already has a hard size gate, just a much bigger one than 350 lines.**
- Default read is the first 2,000 lines when no `limit` is given.
- Whole-file reads are capped at 25,000 tokens (`CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS` overrides). Past that the docs say Read returns the first page with a `PARTIAL view` notice telling Claude how to page with `offset`/`limit` (https://code.claude.com/docs/en/tools-reference).
- Files over 256 KB are refused outright. Smoke test on Kafka's 10,072-line `GroupMetadataManager.java` (457.8 KB), stock Read, no offset: the tool returned an error, "File content (457.8KB) exceeds maximum allowed size (256KB). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file." Claude never saw a byte of it.
- The Read tool description tells Claude: "When you already know which part of the file you need, only read that part. This can be important for larger files."

So the comparison is really about the band between 350 lines and roughly 25,000 tokens (about 2,500 to 4,000 lines of Java). Below 350 lines neither system intervenes. Above 25k tokens stock Claude Code already forces paging.

**Re-reads are deduplicated.** A second Read of an unchanged file returns a system reminder instead of the content: "This file is already in your context (see "Contents of …" above) and has not changed on disk. Use that content instead of re-reading." That means one of Spotify's implied savings, repeated reads of the same big file, does not exist in current Claude Code.

**Old tool results are cleared from context before compaction.** The binary has a time-based "microcompact" that replaces old tool results with `[Old tool result content cleared]` once at least 20,000 tokens can be saved, persisting the content to disk. Docs describe this only as "clears older tool outputs first, then summarizes" (https://code.claude.com/docs/en/how-claude-code-works). So a big read's cost is paid once as cache creation, then paid at cache-read rate on subsequent turns until it gets cleared.

**Explore is not Haiku.** The built-in `Explore` agent is defined with `model: "inherit"`. On first-party Anthropic auth there is an inherit cap at `opus`: if the session model is above the haiku/sonnet/opus ladder, Explore runs on Opus; otherwise it runs whatever the session runs. `CLAUDE_CODE_DISABLE_EXPLORE_INHERIT_CAP=1` removes the cap. Explore also does not load CLAUDE.md. `Plan` is also `inherit`. The docs do not state the Explore default at all; they only describe the priority order (per-invocation, agent `model` field, `CLAUDE_CODE_SUBAGENT_MODEL`, main model) at https://code.claude.com/docs/en/sub-agents. The "Claude Code uses Haiku for search" claim in the Reddit thread is wrong for this version.

**What the parent sees from a subagent is only the final text.** Docs: "Only the subagent's final text response comes back to your context, plus a small metadata trailer with token counts and duration" (https://code.claude.com/docs/en/context-window). Explore's own description warns it "reads excerpts rather than whole files and will miss content past its read window." That is the same architecture as Spotify's bulk-reader, with a frontier model in the worker seat.

**Levers that exist for the arms.**
- `CLAUDE_CODE_SUBAGENT_MODEL=haiku` (plus `CLAUDE_CODE_SUBAGENT_MODEL_FORCE=1`) pins every subagent to Haiku.
- A project-level `.claude/agents/Explore.md` with `model: haiku` overrides the built-in Explore (project scope beats built-in).
- `CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1` removes the built-in Explore and Plan agents entirely. `--disallowedTools Agent` removes delegation altogether.
- PreToolUse hooks can `deny` with a reason that goes back to Claude as the tool result, or rewrite `tool_input` via `updatedInput` (https://code.claude.com/docs/en/hooks). A hook that adds `offset`/`limit` instead of denying is a fourth design nobody has tried.

**Measurement surfaces that exist.**
- `claude -p --output-format json` returns `total_cost_usd`, `duration_ms`, `duration_api_ms`, `num_turns`, `usage` with cache creation and cache read split, `modelUsage` per model with `costUSD`, `subagent_stats`, and `permission_denials`. Verified on a smoke run.
- The session transcript JSONL under `~/.claude/projects/<cwd>/<session>.jsonl` records per-message `usage` (input, output, cache_creation, cache_read) and `model`. Subagent transcripts land in `<session>/subagents/agent-<id>.jsonl`. Every tool call and result is there, so blocked reads, offsets, and Agent calls can be counted.
- OpenTelemetry: metrics `claude_code.token.usage` and `claude_code.cost.usage`; log events `tool_decision` (attributes `decision`, `source` such as a hook, `tool_name`, `tool_parameters`), `tool_result` (`success`, `duration_ms`), and `api_request` (per-call latency). Spans exist for `claude_code.llm_request`, `claude_code.tool.execution`, `claude_code.hook`, and `claude_code.subagent.spawn`. Set `CLAUDE_CODE_ENABLE_TELEMETRY=1` and point OTLP at a local receiver.

## 3. Arms

All arms run the same Claude Code version, same main model, same permission mode (`--permission-mode bypassPermissions` with `--disallowedTools` symmetric), same `--max-turns`, fresh clone per run, no CLAUDE.md beyond what the arm needs.

| Arm | What it is | What it tests |
|---|---|---|
| A. Stock | Claude Code as installed. Explore and general-purpose available, model inherit. | The "it already does this" claim. Also gives the delegation rate. |
| B. Shunt rebuild | Spotify's actual shunt plugin, verbatim: the `check-file-size` and `check-bash-read` hooks, the `bulk-read` and `code-write` scripts, and both skills, all Apache 2.0 in `spotify/portal-ai-plugins`. The only change is `scripts/lib/aika.sh`, which is swapped from `portal-cli actions aika:invoke-chat` to `claude -p --model haiku` using the two mode instruction prompts from the README (both modes run at temperature 0.2 on Portal; Claude Code cannot set temperature, so that is noted). | Spotify's architecture with the Portal dependency swapped for a Haiku worker. Worker cost logged separately by the scripts. |
| C. Hook + Haiku Explore | Same two hooks as B, but the deny message points Claude at the Explore subagent, and a project-level `Explore.md` pins it to Haiku. No bash worker. | The five-line version from the HN thread: enforcement plus a cheap model, no outside system. |

Optional D if budget allows: same hooks but the hook rewrites the Read call to `limit: 350` via `updatedInput` instead of denying. Tests whether narrowing beats redirecting.

The worker in B is Haiku, not Gemini 2.5 Flash. That is a deliberate substitution and the write-up says so. Portal's AiKA modes are not reproducible outside Spotify.

**What the hooks actually do, from source.** Both are bash scripts that read the hook JSON from stdin, pull fields with `jq`, and count lines with `wc -l`. The threshold is `SHUNT_MIN_LINES`, default 350, and the block condition is strictly greater than 350. `check-file-size` allows any Read that sets `offset` or `limit` ("Claude already knows what it needs"), and its own evals document that `limit: 0` is a known bypass. `check-bash-read` only inspects commands starting with `cat`, `head`, `tail`, `less`, or `more`, lets anything containing a pipe or a redirect through, and still blocks `head -100 bigfile`. It does not catch `grep`. The block returns the older top-level JSON form, `{"decision": "block", "reason": "File is N lines (threshold: 350). Use the /bulk-reader skill to delegate this read to AiKA instead of reading it directly. If you need exact content for editing, re-read with an offset/limit for just the section you need."}`, not exit code 2 or `hookSpecificOutput.permissionDecision`. The plugin's own delegation timeout is 180 seconds (`SHUNT_TIMEOUT_SECONDS`), not the 30-second Portal cap the post mentions.

Two consequences for the design. First, the offset/limit allow rule means stock Claude Code's own gates can route around the hook: the 25k-token partial view and the 256 KB refusal both tell Claude to retry with offset and limit, and that retry passes the hook untouched. The harness counts these "hook bypass via paging" events. Second, the older `decision`/`reason` output form has to be confirmed to still block in v2.1.269 before the grid runs, since the docs now describe `hookSpecificOutput.permissionDecision`.

## 4. Target repo

Apache Kafka at trunk, shallow clone. Survey from this environment:

| | Kafka (Java + Scala) | Backstage (TS) |
|---|---|---|
| Source files | 6,448 | 7,348 |
| Files over 350 lines | 1,096 (17.0%) | 549 (7.5%) |
| Share of source lines in those files | 63.9% | 37.9% |
| Files over 1,000 lines | 288 | 79 |
| Files over 2,000 lines | 95 | 9 |

Kafka wins: it is a Java monorepo like Spotify's, and most of its code lives in files the hook would catch. The largest main-source file, `GroupMetadataManager.java` at 10,072 lines, is above stock Claude Code's 256 KB refusal, which makes it a useful probe of what each arm does when even stock forces paging.

The clone is 125 MB. Gradle 9.7.1 runs here, so single-module compile and test are available as graders, though a full Kafka test run is too slow to use per trial.

## 5. Tasks

Twelve tasks in four categories, chosen so the hook actually fires. Each task names the files involved so scoring is deterministic.

**Bulk-read questions (4).** Analogues of Spotify's four scenarios. Example: "List every metric name registered in `GroupCoordinatorMetrics` and the record type each one counts." Graded by a key list: recall of required items, plus a penalty for invented items. Files are 500 to 3,000 lines so they sit in the band where arms differ.

**Code-write from spec plus reference (3).** "Write a new `RecordHelpers`-style helper for X following the pattern in `<reference file>`." Graded by `./gradlew :module:compileJava` on the single module plus a checklist of required methods. This is Spotify's code-writer mode, where the output is meant to bypass Claude's context entirely.

**Precise edit (3).** "In `<file>`, change the log level of the message about Y from WARN to DEBUG" in a 1,500-line file where the string appears twice with different context. Graded by diff: exactly the right line changed, nothing else. This is the task Spotify says cannot be delegated because summaries lose line numbers.

**Planted bug (2).** A copy of a 1,000-plus-line class with a subtle concurrency bug introduced (a check-then-act outside the lock, mirroring Spotify's thread-safety example). "Review this class for thread-safety problems." Graded pass/fail on whether the report names the bug's method and line region. This is where the cheap worker is expected to lose.

Three repetitions per task per arm. 12 tasks x 3 arms x 3 reps = 108 runs, plus D if added.

## 6. Metrics, paired per task and repetition

- **Cost in USD**, total, from `total_cost_usd` in arm A and C, and `total_cost_usd` plus the sum of worker-run `total_cost_usd` values in arm B. This is the headline.
- **Main-model input tokens** split into uncached, cache creation, and cache read, from `modelUsage`. This is the number Spotify's 90% is closest to, reported so the two can be compared.
- **Spotify-style estimate**, computed the way the shunt README does it: characters divided by four for the files Claude would have read, against characters divided by four for what actually entered context. Reported next to the ledger number for the same runs so the gap between the two methods is itself a result.
- **Worker tokens and cost**, arm B and C, from the worker's own JSON output and the subagent transcripts.
- **Latency**: wall clock `duration_ms`, API time `duration_api_ms`, and per-call latency from OTel `api_request` events, plus hook execution time from `claude_code.hook` spans in B and C.
- **Turns**: `num_turns`.
- **Behavior counts** from the transcript: Read calls, Read calls with `offset`/`limit`, hook-denied reads, hook bypasses via paging (a denied or gated read followed by an offset/limit read of the same file), Agent spawns and their model, worker invocations, bash reads, re-reads of a file after a delegation for it (the "did not trust the summary" signal), and files that hit the stock 256 KB or 25k-token gate.
- **Quality**: task grader score, and pass^3 across the three repetitions.

Stats: Wilcoxon signed-rank on paired cost and latency, sign test on paired quality, bootstrap confidence intervals on the mean cost difference. Report per-category breakdowns since the expected result differs by category.

## 7. Telemetry pipeline

Three sources, each parsed by its own script and joined on run id.

1. **Headless JSON**: the harness runs `claude -p "<task>" --output-format json` with a per-run `--session-id` and captures stdout. Fields above.
2. **Transcript JSONL**: copied out of `~/.claude/projects/` after each run, along with the `subagents/` directory. Parsed into a per-tool-call table.
3. **OTel**: `CLAUDE_CODE_ENABLE_TELEMETRY=1`, `OTEL_METRICS_EXPORTER=otlp`, `OTEL_LOGS_EXPORTER=otlp`, `OTEL_EXPORTER_OTLP_PROTOCOL=http/json`, `OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318`, `OTEL_METRIC_EXPORT_INTERVAL=1000`, `OTEL_LOGS_EXPORT_INTERVAL=1000`. A small Python receiver writes every OTLP POST to `runs/<run-id>/otel/*.json`. The parser pulls `claude_code.token.usage` by `type` and `model`, `claude_code.cost.usage`, and the `tool_decision` and `api_request` events.

The worker scripts in arm B write their own JSON output to `runs/<run-id>/worker/<n>.json` so worker cost is never lost. Nested `claude -p` runs must unset `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` or they inherit the parent session.

## 8. Protocol controls

- Fresh shallow clone per run, reset to a pinned Kafka commit.
- New session id per run. Prompt cache is shared across runs with the same prefix, so cache reads are reported separately and runs are interleaved across arms rather than blocked by arm.
- Main model fixed for all arms. Recommendation: Sonnet 5 for the full grid, then a 12-run Opus subset on the planted-bug and precise-edit tasks, since those are the ones where the main model's reasoning is the point.
- `--max-turns 40` and a 15-minute timeout per run. Timeouts count as failures and are reported.
- Hooks in B and C must exit non-zero with the reason on stderr, or return the documented deny JSON, so the redirect reaches Claude as a tool result. Verify once by hand before the grid.
- The harness records the Claude Code version, model ids, and Kafka commit into every run's metadata.

## 9. Step 0, before spending anything

Replay existing Claude Code transcripts from `~/.claude/projects/` and compute the share of Read-tool result tokens that came from files over 350 lines. That share is the ceiling on what any 350-line hook can save. The HN commenter who did this got 5.9% of unique reads qualifying. The script for this is the same transcript parser as source 2 above, so it comes free with the harness.

## 10. Budget

Smoke run reference: a two-turn Haiku session on Kafka cost $0.016 and took 6 seconds. Realistic task runs on Sonnet with 10 to 30 turns should land between $0.30 and $1.50. The 108-run grid is roughly $50 to $160, plus a worker overhead in B of a few cents per delegation. JetBrains' 425-trial benchmark cost about $320, so this is in the same range per run.

## 11. Build order

1. Transcript parser and Step 0 replay script. Half a day. Also validates source 2 before anything is spent.
2. OTLP receiver and OTel parser. Half a day. Validate on one stock run.
3. Arm B hooks, scripts, and skills; arm C hook variant and `Explore.md`. One day. Hand-verify a denied Read in each.
4. Task set and graders on Kafka. One day. Run each grader on a known-good answer.
5. Harness runner: clone, run, collect, grade, one JSON row per run. Half a day.
6. Pilot: 4 tasks x 3 arms x 1 rep. Check numbers make sense, fix instrumentation. Then the full grid.
7. Analysis notebook and the write-up as a field dispatch.

## 12. Decisions needed

- Main model for the grid (recommend Sonnet 5, with an Opus subset).
- Whether to include arm D.
- Budget ceiling. Pilot alone is about $10.

## 13. Source verification status

What could be read as primary source from this environment, and what could not. The network policy here blocks engineering.atspotify.com, news.ycombinator.com, reddit.com, blog.jetbrains.com and the archive mirrors, so the post itself was only reachable through domain-restricted search excerpts.

- **Verified verbatim** from the `spotify/portal-ai-plugins` repo: hook source and behavior, the 350 default and env var, the benchmark table and its chars/4 method, both mode prompts including "Output only the code, no explanations, no markdown fences unless asked", temperature 0.2 for both modes, the 180-second plugin timeout, and the "Editing: Claude needs exact content in context" limitation. Both shunt commits are by Dimitri Mazmanov, dated 2026-08-14.
- **Partially verified** (search excerpts attributed to the post's domain, page not viewed): author's title as Principal Product Manager, the September 3 date, Gemini 2.5 Flash as the example worker model, the "advisory, not enforced" CLAUDE.md first version, the thread-safety bug the worker missed, the 10 to 30 second latency and 30-second Portal cap.
- **Not verified**: the Hacker News comment claiming 5 to 7% savings on replayed sessions and 5.9% of unique reads qualifying; anything about the r/ClaudeAI thread; the JetBrains trial count and spend (excerpts conflict between about 240 trials at $106 and 425 at $320). The JetBrains headline result did surface from its own domain: rtk advertised 60 to 90%, measured +7.6% more expensive at low effort and flat at high effort, quality unchanged, with cached re-reads billed at a tenth of the price as the explanation.

Before publishing, open the post, the HN thread, and the Reddit thread from a machine that can reach them and confirm the partial items on the page.

## 14. What would make the result publishable either way

If B or C wins on cost with no quality loss, the post is a copyable pattern with numbers behind it and no Portal dependency. If A wins or ties, the post corrects a story that got a Hacker News front page, and the correction comes with the specific mechanisms above: the 256 KB gate, the 25k-token page, re-read dedupe, and microcompaction. The strongest version of the second outcome is showing that stock Claude Code's own gates were doing most of the work Spotify credited to the hook.
