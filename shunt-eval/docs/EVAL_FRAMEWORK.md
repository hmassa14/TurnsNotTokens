# Evaluation framework

The framework the task set has to serve. Written after the first grid exposed three problems: the task set had no needle-shaped read task even though that is the case Spotify's motivation describes; the strict hook's block message suggested grep, which confounds "the model never delegates"; and the headline token metric counted only `Read` output, so grep results that carried most of a file into context were invisible. Everything below is designed so those cannot happen again.

## The claim, and the two hypotheses it splits into

Spotify's claim: block reads of files over 350 lines, hand them to a cheap worker, and the frontier model consumes about 90% fewer tokens. Their post treats that as a cost saving.

That splits into two testable hypotheses, and the task set has to cover both.

| | Hypothesis | Task cells | What "supported" means |
|---|---|---|---|
| H1 | On the workloads shunt targets, the hook reduces frontier tokens **and** dollar cost, at equal correctness. | H1a to H1e below | Hook run passes at the same rate as stock; frontier-context tokens fall; cost falls on a majority of paired reps. |
| H2 | On workloads shunt does not target, where the hook still fires because the file is big, it does **not** reduce correctness and does **not** raise cost. | H2a, H2b | Pass rate unchanged; cost within noise of stock. A cost increase here is harm, not neutral. |
| M | Any cost difference is explained by request count (turns) times cached resend, not by per-token price. | all | Cost tracks `api_requests`, not `tokens_saved`. |

A task that does not sit in one of these cells does not belong in the grid.

## Task cells

Two things decide a cell: whether Spotify expects improvement, and the shape of the read. Shape matters because Spotify's motivation ("read 700 lines to check a pattern") is needle-shaped, while every task in their benchmark file is exhaustive-shaped ("list every export"). Both shapes are H1; they can come out differently.

| Cell | Shape | Spotify source | Existing tasks | Status |
|---|---|---|---|---|
| H1a | Exhaustive read of one big file | benchmark #1 `single-large-file` | R1, R2 | ok |
| H1b | Cross-read across files | benchmark #2 `multi-file-cross-read` | R3 | ok |
| H1c | Source plus its test | benchmark #3 `source-plus-test` | R4 | ok |
| H1d | **Needle read**: question answerable from under 10% of a big file, no edit | post motivation, not in their benchmark | none | **missing, add 4** |
| H1e | Templated code-gen from a reference | benchmark #4 `code-generation` | W1, W2, W3 | W1/W2 references are under 350 lines, hook never fires: keep as no-fire controls, not as H1e evidence. W3 fires. Add 1 with a big reference. |
| H2a | Precise edit in a big file (needs exact text) | post's stated limit: editing needs exact content | E1, E2, E3 | ok |
| H2b | Reasoning over a big file (debugging) | post's stated limit: a summary cannot reason | D1, D2 | ok |
| C0 | Small file, hook never fires | control: plugin overhead only | W1, W2 | ok |

Needle tasks to add (H1d), each on a file over 350 lines, answer in one method or one block:

- N1 `RecordAccumulator.java` (1,500 lines): what does `ready()` return when no batch is full and no linger has expired. Key: the exact return expression and the two fields it reads.
- N2 `NetworkClient.java` (1,879 lines): what condition triggers a rebootstrap. Key: the boolean expression in `handleApiVersionsResponse`.
- N3 `LocalLog.java` (1,072 lines): what the KAFKA-6388 special case in `roll()` checks for. Key: the guard expression.
- N4 `StateDirectory.java` (1,019 lines): which exception `lock()` throws when the directory is already locked by another process. Key: the exception class and the message.

Every key is a literal expression or identifier, graded exact-match with an alias list, so a summary from a worker can pass only if it preserved the literal.

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

| Arms | Tasks | Reps | Runs |
|---|---|---|---|
| stock, shunt-strict (neutral message) | R1 to R4, N1 to N4, W3 plus one new code-write, E1 to E3, D1, D2 | 3 | 14 x 2 x 3 = 84 |
| stock, shunt-strict | W1, W2 (no-fire controls) | 1 | 4 |

At the first grid's mean of about $0.18 per run, roughly $16 at list price. Arm B (shipped message, paging exception open) is not re-run: its result, bypass on every block, is established and is the sidebar.

## What the first grid still supports

- Spotify's benchmark never runs Claude Code; it calls the worker script directly. Their 90% presupposes delegation. Verified from `evals/run.sh`.
- With the paging exception open, the model paged around every block (9 of 9). The shipped message tells it to.
- Request count is the cost driver: 6.8 per run under stock, 11.0 under the strict hook.
- Skills were loaded (first-request system prompt is 120 tokens larger in every shunt run, matching two skill entries) and the Skill tool was allowed. Zero invocations in 60 runs is real behavior, but under a message that offered an alternative.

What it does not support until the grid above runs: that the model refuses to delegate when the message offers nothing else; the size of the cost gap; and anything about needle-shaped reads.
