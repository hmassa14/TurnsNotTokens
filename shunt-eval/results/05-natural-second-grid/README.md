# 05 · natural prompts, second grid: stock vs Spotify's hook enforced, three reps

**Question.** With the confounds of grids 03 and 04 removed, does Spotify's hook lower the bill on the tasks it targets, and does it do harm on the tasks it does not?

**Design.** 21 tasks in five categories (see `docs/EVAL_FRAMEWORK.md`), natural prompts (no file path given), two arms, three repetitions on the 18 main tasks and one on the three small-file controls: 114 runs, interleaved by arm. Main model Sonnet 5; worker Haiku 4.5 through a one-turn headless call with no tools. Cache TTL pinned to 5 minutes on both arms. The strict arm's block message is Spotify's verbatim minus the sentence about the offset exception. Cost is the main model's billed cost at list price plus the worker's own cost; every run's per-request recomputation matches Claude Code's `total_cost_usd` to within $0.000001 (`cost_recon_diff_usd` in each `grade.json`).

**Headline.** Target-file content in the main model's context fell 46% (counted through every tool). Requests per run rose 29%, wall time 46%, cost +16% by means, +18% paired per task (95% bootstrap interval +1% to +35%; sign test p = 0.19). Pass rate 96% stock, 98% hook. The hook was cheaper on 7 of 21 tasks.

**Behavior.** 85 blocks in 41 of 57 hook runs. The model's next call after a block: the bulk-reader skill 9 times, Grep 26, Bash 21, a paged Read 26 (refused by the strict hook every time), a Read of another file 3. 13 worker calls in 9 runs on 5 tasks. Zero bypasses.

| Group | Tasks | Runs | Pass stock / hook | Cost per run stock / hook | Δ of means | Δ paired mean (95% CI) | Hook cheaper | Target tokens in context stock / hook | Requests stock / hook | Wall s stock / hook | Blocks | Worker calls |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| All tasks | 21 | 57+57 | 96% / 98% | $0.140 / $0.162 | +16% | +18% (+1%, +35%) | 7 of 21 | 6,068 / 3,291 | 7.1 / 9.1 | 47 / 68 | 85 | 13 |
| Spotify's four benchmark tasks, one to one | 4 | 12+12 | 92% / 100% | $0.131 / $0.139 | +7% | +5% (-25%, +40%) | 2 of 4 | 5,495 / 2,899 | 6.8 / 6.8 | 48 / 68 | 8 | 3 |
| Needle reads: one fact in a big file | 4 | 12+12 | 100% / 100% | $0.087 / $0.076 | -13% | -8% (-27%, +11%) | 3 of 4 | 1,098 / 1,302 | 6.2 / 5.4 | 28 / 24 | 7 | 0 |
| Spotify's task shapes on files over the threshold | 5 | 15+15 | 100% / 93% | $0.195 / $0.246 | +26% | +37% (+4%, +73%) | 1 of 5 | 11,139 / 4,744 | 8.7 / 13.1 | 58 / 104 | 35 | 9 |
| Harm: precise edits and debugging on big files | 5 | 15+15 | 100% / 100% | $0.135 / $0.162 | +21% | +27% (+18%, +36%) | 0 of 5 | 6,215 / 3,960 | 6.3 / 10.1 | 47 / 69 | 32 | 1 |
| Controls: small files, hook never fires | 3 | 3+3 | 67% / 100% | $0.138 / $0.167 | +21% | +21% (-40%, +103%) | 1 of 3 | 2,156 / 2,199 | 8.0 / 9.3 | 56 / 60 | 3 | 0 |
| tasks where the hook fired at least once | 17 | 47+47 | 98% / 98% | $0.149 / $0.178 | +19% | +26% (+8%, +44%) | 4 of 17 | 6,960 / 3,652 | 7.2 / 10.1 | 48 / 74 | 85 | 13 |
| tasks where the worker was called at least once | 5 | 15+15 | 100% / 93% | $0.173 / $0.259 | +50% | +54% (+34%, +79%) | 0 of 5 | 10,001 / 5,361 | 6.6 / 12.3 | 62 / 124 | 36 | 13 |
| tasks where the hook fired and the worker was never called | 12 | 32+32 | 97% / 100% | $0.138 / $0.139 | +1% | +14% (-4%, +35%) | 4 of 12 | 5,534 / 2,852 | 7.5 / 9.1 | 42 / 51 | 49 | 0 |

**Reading it.** Where the model delegated (five tasks, all of the list-everything-in-a-big-file shape), cost rose by about half and wall time doubled: the worker is cheap ($0.02 to $0.05 a task) and the turns around it are not. Where the hook fired and the model grepped instead (twelve tasks), target content in context fell by half or more and cost was flat on average, with a wide interval. Needle reads came out slightly cheaper under the hook; the harm tasks (precise edits, debugging) came out +27% with correctness unchanged, because each refused slice of the file was a wasted turn.

**Grader notes.**
- ND4's key originally accepted only `StreamsException` from `initializeProcessId`; the prompt's wording also describes the per-task lock path, which throws `LockException`, and every model answer named that one. Both are accepted; all ND4 runs pass on both arms after the correction. Ambiguity in the task, not a finding.
- Code-gen tasks (SB4, SC4, SC5, CT1, CT2) are graded by a checklist of required patterns, not by compiling; the Kafka build does not run offline here. SB4 stock rep 1 missed one pattern (`xform.configure(`), SC4 hook rep 1 missed one (`isRemoteLogDeletionEnabled()`), CT2 stock missed its checklist as it did in the first grid. These are counted as fails in the tables and stated as checklist fails.
- Two runs spawned an Explore subagent under stock; their requests are included in cost and request counts.

**Parser fix made during grading.** Claude Code writes one API response as several transcript lines (thinking, text, tool_use), each carrying a running `output_tokens` count; the parser had kept the first line's count and undercounted output on three runs by up to $0.025. Fixed in `bin/parse_transcript.py` (keep the largest count per request) and every run re-parsed and re-graded before these tables were built.

Files: `tables.md` (from `bin/table.py`), `summary.json` (from `bin/summarize.py`), one folder per run. Raw transcripts and telemetry stay in the gitignored `runs/` tree.
