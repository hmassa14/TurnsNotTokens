# Natural-prompt grid 1: all twelve tasks, three arms, one run each

Date 2026-09-12. Claude Code 2.1.269, main model `claude-sonnet-5`, worker and Explore on `claude-haiku-4-5`, Kafka `0ffb4f5`. Natural prompts (no file path given). 36 runs in 30.7 minutes of wall clock. Per-run trace reports, parsed transcripts, parsed telemetry, grades and worker outputs are in the per-task folders here; the machine-built tables are in `tables.md`.

## Summary, mean per run

| | A stock | B shunt | C hook + Explore |
|---|---|---|---|
| Pass rate | 11/12 | 11/12 | 11/12 |
| Found target file | 12/12 | 12/12 | 12/12 |
| Total cost, all 12 tasks | $1.94 | $2.12 | $2.13 |
| Mean cost per task | $0.161 | $0.177 | $0.177 |
| Of which worker or subagent | 0 | 0 | $0.017 |
| Mean wall clock | 60.6 s | 56.8 s | 56.2 s |
| Mean API requests | 6.8 | 9.1 | 10.8 |
| Lines read into main context, total | 7,111 | 4,363 | 3,897 |
| Lines read by subagent or worker, total | 0 | 0 | 2,291 |
| Hook blocked a read (runs) | 0 | 6 | 4 |
| Block bypassed with offset/limit (runs) | 0 | 3 | 3 |
| Worker calls (arm B) | 0 | **0** | 0 |
| Explore spawns (arm C) | 0 | 0 | 2 |

## Five findings

**1. Spotify's worker was never called. Zero of twelve.** Arm B is their plugin verbatim with only the Portal call swapped for Haiku. The hook blocked a whole-file read in six of the twelve runs. Every time, Claude went around it: three times by re-reading with offset and limit, which the hook allows, and three times by switching to grep. The bulk-reader skill sat in the workspace and was never invoked. On Sonnet 5 in Claude Code 2.1.269, the shipped design does not produce delegation. It produces paging.

**2. The hook rarely fires because Sonnet 5 already pages.** Six blocks across twelve runs, and none on R3, R4, W1, W2, E1, E2, E3 or D2 even though every target is over 350 lines. In those runs Claude opened the file with an offset or limit from the first call, or grepped and read around the hits, and the hook let it through. The stock arm's mean targeted-read count was 0.7 per run before any hook existed. Spotify's 350-line threshold was chosen for a model that reads whole files by default. This one does not.

**3. Same accuracy, stock cheapest.** Eleven of twelve passed in every arm, and it was the same task that failed in all three (W2, on a checklist regex, see below). Stock cost $1.94 for the twelve tasks, shunt $2.12, hook plus Explore $2.13. The hooked arms sent 30 to 40 percent fewer lines into the main context and still paid more, because they took more API requests to get there: 9.1 and 10.8 per run against 6.8. Each extra request resends the whole conversation at the cache-read rate. Cache-read tokens per run: 239k stock, 317k shunt, 266k hook plus Explore.

**4. Delegation, when it happened, worked and was not cheaper.** Arm C spawned Haiku Explore twice, on R1 and R4. Both passed. Both times zero lines of the target entered the main context, the subagent read 879 and 1,412 lines, and the run cost more than stock ($0.169 vs $0.113, $0.209 vs $0.135) and took two to four times as long (100 s vs 39 s, 101 s vs 25 s). The Spotify-style "tokens avoided" figure for those two runs was 8,052 and 16,000 or so, and the bill went up anyway. That is the JetBrains result reproduced: the metric that counts tokens the main model did not read does not predict the bill.

**5. Where the hook helped, it helped by forcing grep.** The shunt arm was the cheapest on four tasks: R3, R4, D1 and E2. On D1 it found the planted race from 50 lines of a 1,019-line file. On R4 it answered a two-file question with zero lines read into context, entirely from grep output. That pattern is real and worth recommending. It is not Spotify's mechanism. It is what a capable model does when a whole-file read is refused and a targeted read is not.

## Per-task cost and pass

| Task | A stock | B shunt | C hook + Explore | Cheapest |
|---|---|---|---|---|
| R1 events | $0.113 pass | $0.204 pass | $0.169 pass, Explore | A |
| R2 config keys | $0.151 pass | $0.309 pass | $0.192 pass | A |
| R3 record replay | $0.382 pass 0.87 | $0.311 pass 1.00 | $0.359 pass 0.85 | B |
| R4 test coverage | $0.135 pass | $0.122 pass | $0.209 pass, Explore | B |
| W1 transform | $0.134 pass | $0.172 pass | $0.117 pass | C |
| W2 sink metrics | $0.252 fail 0.93 | $0.252 fail 0.93 | $0.314 fail 0.93 | A, B |
| W3 config class | $0.159 pass | $0.202 pass | $0.166 pass | A |
| E1 log level | $0.076 pass | $0.078 pass | $0.078 pass | A |
| E2 rename | $0.084 pass | $0.066 pass | $0.080 pass | B |
| E3 roll log | $0.068 pass | $0.066 pass | $0.066 pass | tie |
| D1 lock race | $0.184 pass | $0.133 pass | $0.192 pass | B |
| D2 append race | $0.200 pass | $0.205 pass | $0.184 pass | C |

The edit tasks (E1 to E3) are near-identical across arms: all three grepped for the string and read a few lines around it, hook or no hook. Spotify's post said edits cannot be delegated; here nothing needed delegating.

## Grader notes from this pass

- **R3 deny list was wrong and is fixed.** All three arms named `newStreamsGroupMetadataRecord` and `newStreamsGroupTopologyRecord`, which I had listed as invented. They exist, in `streams/StreamsCoordinatorRecordHelpers.java`. The natural prompt does not scope to one helpers file, so naming them is correct. Removed from the deny list and re-graded: all three now pass, with helper coverage 22/30, 30/30 and 21/30.
- **W2 fails in all three arms on one regex each**, a different one per arm: the stock output did not contain the literal `PROCESSOR_NODE_LEVEL_GROUP`, the shunt output built `"send-latency"` from two constants. Compile was not run because Gradle is not warmed offline in the clone. Treat W2 as unscored until the compile step is in place; the checklist is too literal to decide it.
- **The bug-report grader passed all six D runs.** Reading the answers, all six named the planted method and the right lines. No false positive was credited.

## What is not established

One run per cell. The cost differences are within what a single search choice moves (R1 stock cost $0.11 here and $0.20 under the named prompt, on the same task and model, because of one `find /`). The findings that do not depend on variance are the counts: worker calls, blocks, bypasses, spawns. Those are what this pass establishes.

## Next

1. Arm D, the hook with the offset/limit exception closed, so the only way past a block is the worker. That tests what Spotify intended rather than what they shipped.
2. Three repetitions of this grid for pass^3 and confidence intervals on cost.
3. Gradle warmed offline so W1 to W3 grade on compile.
