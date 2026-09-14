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

## Metrics, per hypothesis

| Group | Metric | Source | Note |
|---|---|---|---|
| Performance | pass, score | grader | unchanged |
| Performance | target file found | transcript | a pass without the target is a miss |
| Tokens (Spotify's metric) | **target-file content entering frontier context via any tool** | transcript: `Read` lines + `Grep`/`Bash` result chars that hit the target, converted at chars/4 | replaces `lines_entered_context`, which counted `Read` only |
| Tokens | Spotify's own formula, for comparison | corpus chars/4 minus summary chars/4 | reported beside, never instead |
| Cost | total at list price, **cache TTL pinned** | result.json, recomputed | `CLAUDE_CODE_PROMPT_CACHE_TTL=5m` on every run so both arms are billed at one rate |
| Cost | finding / answering split | first touch of target | unchanged |
| Latency | wall, api_requests | meta, transcript | requests is the mechanism metric for M |
| Behavior | blocks, bypasses, skill invocations, worker calls, greps | transcript | skill invocations counted separately from worker calls |

## Controls that the first grid lacked

1. **Block message.** Arm B uses Spotify's message verbatim. The strict arm's message must not name an alternative tool. Text: `File is N lines (threshold: 350). Use the /bulk-reader skill to delegate this read.` Nothing about offset, limit, or grep. Whether the model greps is then its choice, not ours.
2. **Cache TTL.** Pinned to 5m on every run via the env var. The first grid straddled Claude Code's automatic switch to 1h and billed the strict arm at the higher rate on all twelve runs.
3. **Repetitions.** Three per cell for H1 and H2 read tasks. One run per cell gave a 35% gap as billed and a 21 to 27% gap normalized, on 9 of 12 tasks; that is a direction, not a result.
4. **Interleaving.** Arms alternate per task so time of day and subscription state never line up with one arm.
5. **Worker.** Haiku through headless Claude Code stands in for Portal. Documented; if the worker is never called it does not matter, if it is called its cost is in the ledger.
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
