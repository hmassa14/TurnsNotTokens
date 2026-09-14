# Evaluation framework

The framework the task set has to serve. Written after the first grid exposed three problems: the task set had no needle-shaped read task even though that is the case Spotify's motivation describes; the strict hook's block message suggested grep, which confounds "the model never delegates"; and the headline token metric counted only `Read` output, so grep results that carried most of a file into context were invisible. Everything below is designed so those cannot happen again.

## The claim, and the two hypotheses it splits into

Spotify's claim: block reads of files over 350 lines, hand them to a cheap worker, and the frontier model consumes about 90% fewer tokens. Their post treats that as a cost saving.

That splits into two testable hypotheses, and the task set has to cover both.

| | Hypothesis | Task cells | What "supported" means |
|---|---|---|---|
| H1 | On the workloads shunt targets, the hook reduces frontier tokens **and** dollar cost, at equal correctness. | part 1 rows 1 to 4; needle, scaled, second-sample rows in part 2 | Hook run passes at the same rate as stock; frontier-context tokens fall; cost falls on a majority of paired reps. |
| H2 | On workloads shunt does not target, where the hook still fires because the file is big, it does **not** reduce correctness and does **not** raise cost. | harm rows in part 2 | Pass rate unchanged; cost within noise of stock. A cost increase here is harm, not neutral. |
| M | Any cost difference is explained by request count (turns) times cached resend, not by per-token price. | all | Cost tracks `api_requests`, not `tokens_saved`. |

A task that does not sit in one of these cells does not belong in the grid.

## Tasks, part 1: one-to-one with Spotify's benchmark

Their benchmark file (`plugins/shunt/evals/benchmarks.json`) has four rows. Their fixtures: `websocket-handler.ts` 602 lines, `user-service.ts` 35, `order-service.test.ts` 55. Only rows 1 and 2 contain a file over the 350-line threshold; rows 3 and 4 never would have tripped the hook. Their scoring calls the worker script directly and never runs Claude Code, so that did not matter to them. It matters to us, because ours run through Claude Code and the hook.

Each row gets an exact analog on Kafka, matched on question shape and on file-size band, so the comparison is theirs first and ours second.

| Their row | Their question (verbatim) | Their files | Our 1:1 | Our files | Hook fires? |
|---|---|---|---|---|---|
| 1 `single-large-file` | "What are all the exported items and what do they do?" | 602 lines | **R2** every config key with type and default | `RemoteLogManagerConfig.java` 616 | yes |
| 2 `multi-file-cross-read` | "Which classes and interfaces are exported across these files, and how do they relate to each other?" | 602 + 35 + 55 | **R5 (new)** one big file plus two small related files, how they relate | `BrokerLifecycleManager.java` 770 + `BrokerState.java` 108 + one more small related file, to select | yes, on the big one |
| 3 `source-plus-test` | "What methods does UserService have, and which ones would be covered if we wrote tests following the OrderService test pattern?" | 35 + 55 | **R6 (new)** what methods does `Filter` have, which would be covered following `InsertHeaderTest`'s pattern | `Filter.java` 62 (no test exists) + `InsertHeaderTest.java` 125 | **no**, same as theirs |
| 4 `code-generation` | "Write unit tests for UserService following the exact same patterns, structure, and assertions as the OrderService tests." | ref 55, ctx 35 | **W4 (new)** write `FilterTest` following `InsertHeaderTest` exactly | ref `InsertHeaderTest.java` 125, ctx `Filter.java` 62 | **no**, same as theirs |

Code-gen (rows 4 and its scaled versions) is a **skill-uptake test, not a hook test**: no hook intercepts a write, so the code-writer path runs only if the model volunteers the skill. Its result is reported on its own and never folded into the hook's cost figure.

Rows 3 and 4 are kept small on purpose. That is what they tested, and running them shows the reader that half of Spotify's own benchmark is below the hook's threshold. Code-gen is graded two ways: as they scored it (spec sent, file written, Claude never reads it back) and as their skill instructs (Claude reviews the output), because the second is what a real session does.

## Tasks, part 2: what their benchmark does not cover

Each addition names the gap it fills.

| Gap in their benchmark | Cell | Tasks | Files | Hook fires? |
|---|---|---|---|---|
| Their read rows are all "list every X." The motivation is "read 700 lines to check one thing." The saving from a summary is file size minus answer size, so this is the hook's best case and they never test it. | Needle read | **N1 to N4 (new)**: what `ready()` returns when nothing is ready; what condition triggers rebootstrap; what the KAFKA-6388 guard in `roll()` checks; what `lock()` throws when already locked | `RecordAccumulator` 1,500; `NetworkClient` 1,879; `LocalLog` 1,072; `StateDirectory` 1,019 | yes |
| One sample per shape. | Second sample of row 1 | R1 every event class and its state | `BrokerLifecycleManager` 770 | yes |
| Rows 2 to 4 never trip the hook, so they say nothing about it. | Same shapes, scaled into the hook's band | R3 (two big files), R4 (big source + big test), W3 (config class from a 616-line reference), **W5 (new)** tests for `TimestampRouter` following `TimestampConverterTest` (739-line reference) | as listed | yes |
| Nothing tests a task the post itself says the approach is unsuited to. The hook fires on line count alone, so it fires on these anyway. | Harm: precise edit | E1, E2, E3 | 985 to 1,879 | yes |
| Same. | Harm: reasoning | D1, D2 | 1,019; 1,500 | yes |
| No control for the plugin's fixed cost (two skill descriptions in the system prompt every turn) or for unprompted skill uptake. | Small-file control | R6, W4 from part 1; W1, W2; **S1 (new)** a needle question on a file under 350 lines | under 350 | no |

Every key is derived mechanically from the code, as in `docs/TASKS.md`. Needle keys are a literal expression or identifier with an alias list, so a lossy summary fails.

## Metrics

Spotify's benchmark measured one deterministic path, so it had two numbers: corpus size and summary size. A Claude Code session is a sequence of requests the model chooses, so every metric here is defined per request, summed per run, and kept separate for the main model and the worker. Three sources, reconciled on every run: the JSON Claude Code prints, the transcript it writes, and the OpenTelemetry export. A number that does not match across all three is not reported.

Three prongs decide whether the hook belongs in a real deployment. A fourth group, tokens, is Spotify's own metric and is reported beside cost, never instead of it. A fifth, behavior, explains the other four.

### Performance: did it get the right answer

| Metric | Definition | Source |
|---|---|---|
| pass | grader verdict at the task's threshold | grade.json |
| score | the grader's continuous score, for partial credit | grade.json |
| target found | the session read, grepped, or delegated the target file at least once; a pass without it is scored as a miss | transcript |
| pass^k | all k reps passed; the number to report, since one lucky run is not a pass | grade.json over reps |

Graders by category: SB and SC reads, and ND, use key lists derived from the code (recall over names, exact match for needle literals, with alias lists). HM edits use exact diff with decoy lines that must be untouched; HM debugging names the method, a line in range, and the race. Code-gen (SB4, SC4, SC5, CT1, CT2) is graded by **compiling and running the generated tests with Gradle**, not by a regex checklist; the first grid's W2 failed a checklist regex on all arms, which is a grader bug, not a finding. Code-gen is graded twice from the same run: as Spotify scored it (the file is written, the model never reads it back) and with the review step their skill instructs.

What "good" means: for SB, ND, SC and CT, hook pass rate equal to stock. For HM, hook pass rate not below stock. A cost saving on a task that stopped passing is not a saving.

### Cost: what it cost

| Metric | Definition | Source |
|---|---|---|
| total | main model + worker + subagents, at list price, from tokens | result.json usage, worker/*.json, recomputed |
| by bucket | uncached input, cache write, cache read, output, each at its rate | result.json usage |
| by phase | finding (requests before the first touch of the target) and answering (from the first touch on) | transcript |
| by request | the per-request series, for the trace figures | transcript |
| resend bill | sum over requests of cached tokens re-sent, at the cache-read rate; the mechanism metric for M | transcript |

Rules. Cache TTL is pinned to 5m on every run (`CLAUDE_CODE_PROMPT_CACHE_TTL=5m`), so both arms pay one rate; the first grid straddled Claude Code's automatic switch to 1h and charged the strict arm 2x on writes. Every recomputed total is checked against Claude Code's own `total_cost_usd` and must match to four decimals. Cost is reported at equal correctness: the headline figure is over tasks both arms passed, with the all-tasks figure beside it.

Comparison. Paired per task, three reps: per-task mean and range, then the paired difference across tasks with an interval, and a sign test. The number to publish is a percentage change with an interval, per category, not one point for the whole grid.

### Latency: how long it took

| Metric | Definition | Source |
|---|---|---|
| wall | harness start to exit | meta.json |
| requests | API requests in the run; the turn count | transcript |
| per-request duration, time to first token | from `api_request` events | OpenTelemetry |
| time in tools | sum of tool latencies | transcript |
| time in worker | the worker call's own duration, when one happens | worker/*.json |

Reported as median and p90 across reps. Latency is the prong Spotify's own post flags (10 to 30 seconds per delegation), so in SB, ND and SC a hook run that delegates is expected to be slower and the question is by how much; in HM and CT it should match stock.

### Tokens: Spotify's metric, done inside Claude Code

| Metric | Definition | Note |
|---|---|---|
| target content in frontier context | target-file text that reached the main model through **any** tool: `Read` lines, plus `Grep` and `Bash` results that hit the target, at chars/4 | replaces the first grid's `lines_entered_context`, which counted `Read` only and so missed the 31k characters R1's greps brought in |
| Spotify's formula | corpus chars/4 minus summary chars/4, computed only when a worker call happened | zero worker calls means this metric is undefined, which is itself the finding |
| frontier input tokens | every input token the main model was billed for, cached or not | what their post's "tokens" would mean if it were a bill |

### Behavior: why the numbers came out that way

Per run: hook blocks, blocks followed by a paged read, skill invocations, worker calls, `Grep` calls on the target, re-reads of the target after a delegation, subagent spawns. Skill invocations and worker calls are counted separately, because a skill can be opened without the script being run. In SB, ND and SC, worker calls above zero is the precondition for any of Spotify's claimed saving; zero means the mechanism never engaged and the cost result is about the model's fallback, not about delegation.

### Success criteria, per category

| Category | Performance | Cost | Latency | Tokens |
|---|---|---|---|---|
| SB, ND, SC (helps?) | equal pass rate | lower, with interval excluding zero | slower allowed; report by how much | lower, on the any-tool metric |
| HM (hurts?) | not lower | not higher | not slower | reported, not a criterion |
| CT (overhead) | equal | equal within the plugin's fixed system-prompt cost | equal | equal |

## Controls that the first grid lacked

1. **Block message.** Arm B uses Spotify's message verbatim. The strict arm's message must not name an alternative tool. Text: `File is N lines (threshold: 350). Use the /bulk-reader skill to delegate this read.` Nothing about offset, limit, or grep. Whether the model greps is then its choice, not ours.
2. **Cache TTL.** Pinned to 5m on every run via the env var. The first grid straddled Claude Code's automatic switch to 1h and billed the strict arm at the higher rate on all twelve runs.
3. **Repetitions.** Three per cell for H1 and H2 read tasks. One run per cell gave a 35% gap as billed and a 21 to 27% gap normalized, on 9 of 12 tasks; that is a direction, not a result.
4. **Interleaving.** Arms alternate per task so time of day and subscription state never line up with one arm.
5. **Worker.** Haiku stands in for Portal's Gemini. With `ANTHROPIC_API_KEY` set, the worker is one Messages API call: Spotify's mode instructions as the system prompt, no tools, temperature 0.2 as upstream sets. Without a key (subscription-only auth), it is a one-turn headless Claude Code call with `--tools ""`, so no tool definitions enter the worker's prompt. The first grid's worker carried about 25k tokens of tool definitions per call; that is gone on both paths. Every call records transport, usage, cost and duration.
6. **Thinking is not persisted.** Claude Code writes empty thinking blocks to the transcript. The model's reasons for a choice cannot be recovered after the fact; behavior has to be inferred from calls only. Design messages so the inference is clean.

## Grid to run

| Block | Tasks | Arms | Reps | Runs |
|---|---|---|---|---|
| 1:1 with Spotify | R2, R5, R6, W4 | stock, shunt-strict (neutral message) | 3 | 24 |
| Needle reads | N1, N2, N3, N4 | same | 3 | 24 |
| Scaled and second-sample | R1, R3, R4, W3, W5 | same | 3 | 30 |
| Harm | E1, E2, E3, D1, D2 | same | 3 | 30 |
| Small-file controls | S1, W1, W2 | same | 1 | 6 |
| | | | | **114** |

At the first grid's mean of about $0.18 per run, about $21 at list price. W4 and W5 are each graded twice from one run (as Spotify scored it, and with the review step), so they do not add runs. Arm B (shipped message, paging exception open) is not re-run: bypass on every block is established and stays as the sidebar.

Order of work: write the new tasks and derive their keys (R5, R6, W4, W5, N1 to N4, S1), then the neutral-message strict arm, then the TTL flag in `run.py`, then the new token metric in `parse_transcript.py`, then a smoke run of one task per block before the grid.

## What the first grid still supports

- Spotify's benchmark never runs Claude Code; it calls the worker script directly. Their 90% presupposes delegation. Verified from `evals/run.sh`.
- With the paging exception open, the model paged around every block (9 of 9). The shipped message tells it to.
- Request count is the cost driver: 6.8 per run under stock, 11.0 under the strict hook.
- Skills were loaded (first-request system prompt is 120 tokens larger in every shunt run, matching two skill entries) and the Skill tool was allowed. Zero invocations in 60 runs is real behavior, but under a message that offered an alternative.

What it does not support until the grid above runs: that the model refuses to delegate when the message offers nothing else; the size of the cost gap; and anything about needle-shaped reads.
