# Natural-prompt pilot 1: R1 and D1 across all three arms

Date 2026-09-12. Claude Code 2.1.269, main model `claude-sonnet-5`, Kafka `0ffb4f5`, one run per cell, natural prompts (no file path given). Six runs, 7.4 minutes wall clock for the whole grid, all six passed, all six found the target file. Full tables in `tables.md`; per-run trace reports and parsed artifacts in the run directories.

## The headline

**Spotify's hook did not make Claude delegate.** In arm B, both runs hit the block, and both times Claude routed around it with `offset`/`limit` reads, which the hook allows by design. The bulk-reader skill and the Haiku worker were never invoked. Worker calls: 0 of 2. Arm B was Spotify's plugin verbatim, so this is the shipped design's behavior on this Claude Code version and model, not a rebuild artifact.

**Arm C delegated once.** On R1 Claude followed the block message and spawned the Haiku Explore agent, which read the whole file (879 lines including a second file) and returned 1,111 characters. Zero lines of the target entered the main context. On D1 it paged with offset/limit instead, same as arm B.

**No arm was cheaper on both tasks.** Stock was cheapest on R1 and most expensive on D1. Shunt was most expensive on R1 and cheapest on D1. The paging that followed the block cut D1's context to 50 lines and still found the bug, but on R1 it took eleven requests to page through what stock read in one.

## R1, reading: list the broker lifecycle events and their states

| | A stock | B shunt | C hook + Explore |
|---|---|---|---|
| Pass | yes | yes | yes |
| Lines read into main context | 771 | 655 | 0 |
| Lines read by subagent | 0 | 0 | 879 |
| Hook blocked / bypassed by paging | 0 / 0 | 1 / 1 | 1 / 0 |
| Worker or subagent calls | 0 | 0 | 1 (Haiku Explore) |
| Tool calls | 2 | 10 | 8 |
| API requests | 3 | 11 | 11 |
| Wall clock | 39 s | 78 s | 100 s |
| Total cost | $0.113 | $0.204 | $0.169 |
| Main / subagent cost | $0.113 / 0 | $0.204 / 0 | $0.120 / $0.049 |
| Cache read tokens | 83,119 | 372,647 | 33,584 |
| Spotify-style tokens avoided | 0 | 0 | 8,052 |

What happened in each: stock grepped for the class name, read the file whole, answered. Shunt searched with `find /` three times, got blocked, grepped for `class \w+Event`, then read the file in four slices of 180, 300, 40 and 135 lines and answered. The 372k cache-read tokens are the price of eleven requests each resending the growing context. Hook + Explore searched, got blocked, spawned Explore, which read the whole file and a second one on Haiku and returned a summary the main model answered from.

## D1, debugging: find the planted race in StateDirectory

| | A stock | B shunt | C hook + Explore |
|---|---|---|---|
| Pass | yes | yes | yes |
| Lines read into main context | 1,020 | 50 | 175 |
| Hook blocked / bypassed by paging | 0 / 0 | 1 / 1 | 1 / 1 |
| Worker or subagent calls | 0 | 0 | 0 |
| Tool calls | 6 | 6 | 10 |
| API requests | 6 | 7 | 11 |
| Wall clock | 70 s | 70 s | 60 s |
| Total cost | $0.184 | $0.133 | $0.192 |
| Cache read tokens | 197,290 | 215,242 | 380,342 |

All three found `lock`. Stock read the whole 1,019-line file. Shunt got blocked, grepped for `lock|unlock|Lock`, read 50 lines around the hits, and named the race from those 50 lines at the lowest cost of the three. Hook + Explore did the same but wandered into a second file and took eleven requests.

## What this changes about the experiment

1. **The "hook bypass via paging" counter is the story, not a footnote.** Spotify's allow-rule for offset/limit reads means the hook's real effect on Sonnet 5 is "force a grep-then-page pattern", not "force delegation". That pattern was cheaper on the debugging task and more expensive on the reading task.
2. **Arm B needs a variant with the bypass closed** to test what Spotify intended rather than what they shipped: block paged reads too, so the only way through is the worker. That is a one-line change to `check-file-size` and a fourth arm worth adding.
3. **The subagent-or-worker row is the delegation rate.** Across the six runs it was 1. The Reddit premise that Claude Code delegates big reads on its own was 0 of 2 in stock, and even with a hook pointing at Explore it was 1 of 2.
4. **Finding cost was similar across arms** ($0.03 to $0.06), because every arm searched the same way: `find` and `grep` from the main model. Nobody used Explore to search, which is the thing Explore exists for.

One run per cell. None of the differences above are established; they are what to look for in the repetitions.
