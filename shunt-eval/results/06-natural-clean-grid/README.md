# 06 · the clean grid: stock, Spotify's hook as shipped, and as described, three reps, offline

**Question.** With every session confined to the repository, does Spotify's hook lower the bill on the tasks it targets, and does it do harm on the tasks it does not? Three setups each one change apart: `stock` (Claude Code as installed, offline), `shunt` (Spotify's plugin as published, offset/limit exception open), `shunt-strict` (the exception removed; block message otherwise Spotify's).

**Design.** 21 tasks in five categories (`docs/EVAL_FRAMEWORK.md`), natural prompts, three repetitions of every cell including the controls, 189 runs, interleaved by setup. Main model Sonnet 5 on Claude Code 2.1.269; worker Haiku 4.5 through a one-turn headless call, no tools, thinking off, file sent with line numbers (`cat -n`). Cache TTL pinned to 5 minutes. Every setup runs under the harness sandbox (`harness/`): web tools denied, network commands and walks from `/` refused, any path outside the workspace refused, a private empty `/tmp` per session, workspaces with a single import commit and no history, and a system-prompt line saying to answer from the repository. Cost is the main model's billed cost plus the worker's; every run's per-request recomputation matches Claude Code's `total_cost_usd` to within $0.000001. Validation of all 189 runs: zero failed sessions, zero timeouts, zero turn-cap hits, transcript token totals equal to Claude Code's per-model totals on every run, no 1-hour cache writes, telemetry present for every run, every target file found, zero web access, zero answers from memory.

The grid ran 2026-09-14 23:47 to 2026-09-15 13:45 UTC with an eleven-hour gap: at 01:15 the subscription hit a usage limit, twenty cells recorded two-second zero-cost failures, and the container restarted. Those cells were discarded and re-run; `bin/grid.py` now discards and retries a zero-cost failed session instead of recording it.

**Headline (means per run, stock / shipped / enforced).**

| | Stock | As shipped | As described |
|---|---|---|---|
| Pass rate | 100% | 98% | 97% |
| Cost per run, worker included | $0.121 | $0.131 (+8%) | $0.144 (+19%) |
| Paired per task, mean of per-task differences (95% bootstrap CI) | | +8% (-1%, +20%) | +22% (+7%, +39%) |
| Cheaper than stock on | | 9 of 21 tasks (sign test p = 0.66) | 7 of 21 (p = 0.19) |
| Lines of the target file read with `Read` | 450 | 232 | 59 |
| Target-file content by any tool, chars/4 | 6,016 | 3,721 | 2,919 |
| Input tokens the frontier model was billed for | 229,697 | 277,146 | 324,523 |
| Output tokens | 3,061 | 3,569 | 3,867 |
| Spotify's formula (file chars/4 minus summary chars/4, only when the worker is called) | 0 | 0 (never called) | 786 averaged; defined on 5 of 63 runs |
| API requests per run | 6.1 | 7.7 | 9.2 |
| Wall clock per run | 39 s | 45 s | 51 s |
| Hook blocks / runs with a block | 0 | 26 / 24 | 96 / 45 |
| Next call after a block | | paged Read, allowed through: 9; Grep: 14; Read of another file: 2 | paged Read, refused: 33; Grep: 41; Bash: 12; bulk-reader skill: 4; other: 3 |
| Worker calls / runs with one | 0 | 0 | 7 / 5 |

| Group | Pass stock / shipped / enforced | Cost per run | Shipped vs stock, paired (95% CI) | Enforced vs stock, paired (95% CI) | Target tokens in context | Requests | Blocks shipped / enforced | Worker calls |
|---|---|---|---|---|---|---|---|---|
| All 21 tasks | 100% / 98% / 97% | $0.121 / $0.131 / $0.144 | +8% (-1%, +20%), cheaper on 9 of 21 | +22% (+7%, +39%), cheaper on 7 of 21 | 6,016 / 3,721 / 2,919 | 6.1 / 7.7 / 9.2 | 26 / 96 | 0 / 7 |
| Spotify's four benchmark tasks, one to one | 100% / 100% / 92% | $0.107 / $0.133 / $0.166 | +25% (-11%, +63%), cheaper on 2 of 4 | +53% (-2%, +108%), cheaper on 1 of 4 | 5,662 / 4,133 / 3,672 | 5.3 / 7.1 / 10.0 | 6 / 18 | 0 / 1 |
| Needle reads: one fact in a big file | 100% / 100% / 100% | $0.060 / $0.061 / $0.069 | +3% (-13%, +14%), cheaper on 1 of 4 | +19% (-20%, +46%), cheaper on 1 of 4 | 1,771 / 2,046 / 1,313 | 4.5 / 4.2 / 5.8 | 0 / 13 | 0 / 0 |
| Spotify's task shapes on files over the threshold | 100% / 93% / 100% | $0.166 / $0.177 / $0.199 | +11% (-9%, +31%), cheaper on 2 of 5 | +24% (-3%, +50%), cheaper on 2 of 5 | 11,110 / 5,514 / 4,267 | 6.7 / 10.6 / 12.3 | 13 / 31 | 0 / 6 |
| Harm: precise edits and debugging on big files | 100% / 100% / 100% | $0.128 / $0.131 / $0.126 | +0% (-11%, +15%), cheaper on 3 of 5 | +8% (-5%, +20%), cheaper on 2 of 5 | 6,919 / 3,789 / 2,658 | 6.3 / 7.7 / 8.5 | 7 / 27 | 0 / 0 |
| Controls: small files, hook never fires | 100% / 100% / 89% | $0.136 / $0.146 / $0.152 | +4% (-3%, +11%), cheaper on 1 of 3 | +6% (-4%, +17%), cheaper on 1 of 3 | 2,153 / 2,302 / 2,246 | 7.8 / 8.2 / 8.6 | 0 / 7 | 0 / 0 |

Enforced, tasks where the worker was called (3 tasks, 9 runs): +57% (+42%, +86%), cheaper on 0 of 3. Enforced, tasks where the hook fired and the worker was never called (13 tasks): +26% (+7%, +48%), cheaper on 4 of 13.

**Reading it.** Per task, the enforced setup's outcome is consistent across repetitions on 12 of 21 tasks. It is cheaper on every run of the cross-read and source-plus-test tasks, where a couple of targeted greps replace an 11,000 to 14,000-token whole-file read at the same or fewer requests. It is dearer on every run of the exhaustive-enumeration tasks, the code-generation-from-a-reference tasks, the precise edits, and two needle reads where the model wanted the surrounding code: the answer is most of the file, and the block only changes how many turns it takes to get it. The shipped setup is a wash where the hook does not fire and a tax where it does, because the model pages around the block (9 of 26 blocks) and the file comes in anyway in slices. Delegation with numbered lines ends the search faster than in grid 05 (9 to 11 requests instead of 12 to 18 on the broker-lifecycle task) and still costs about half again more than stock, because the refused read, the refused paged read, the skill load and the worker call are each a turn.

**Grader notes.** Three failures in 189: SB1 enforced rep 1 (a config key missed after grepping), SC3 shipped rep 3 (one untested method missed), CT2 enforced rep 2 (checklist). ND4 is reworded from grid 05 and graded strictly; all 9 runs pass. CT2 accepts the reference's `LATENCY_SUFFIX` convention. Code-gen is checklist-graded (no offline Gradle). The enforced setup fired on the CT2 control 7 times: the model tried to read a neighbouring 700-line metrics file, which is the hook working as designed on a small-file task.

**Variance notes.** Two runs (one per hook setup, both on the three-file cross-read) spawned a background subagent and waited for it; they are the two most expensive runs in the grid ($0.46 and $0.31) and are included as measured. 47 sandbox refusals across 189 runs, all `find /`-style sweeps or reads outside the workspace; none reached anything.

Files: `tables.md` (`bin/table.py`, three arms), `summary-shipped.json` and `summary-enforced.json` (`bin/summarize.py`, stock paired with each hook setup), one folder per run. Raw transcripts and telemetry stay in the gitignored `runs-06/` tree.
