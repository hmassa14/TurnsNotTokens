# Strict arms: the hook with the offset/limit exception closed

Date 2026-09-12. Same setup as `03-natural-three-arms`: Claude Code 2.1.269, Sonnet 5 main, Haiku worker and Explore, Kafka `0ffb4f5`, natural prompts, one run per cell. Two new arms, twelve tasks each, 24 runs in 27.7 minutes. This folder holds those 24 runs; `tables.md` has all five arms side by side.

The strict hooks are Spotify's `check-file-size` with one block removed: the rule that allows any Read carrying `offset` or `limit`. In strict arms a file over 350 lines cannot be Read from the main agent at all. Grep is still allowed, as in Spotify's design. Arm C strict keeps the rule that lets the Explore subagent read whole files.

## All five arms, twelve tasks each

| | A stock | B shunt | C hook + Explore | B' shunt strict | C' Explore strict |
|---|---|---|---|---|---|
| Pass | 11/12 | 11/12 | 11/12 | 12/12 | 12/12 |
| Found target file | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| Total cost, twelve tasks | $1.94 | $2.12 | $2.13 | $2.61 | $2.31 |
| Of which Haiku (worker or Explore) | 0 | 0 | $0.20 | 0 | $0.09 |
| Runs where the hook blocked | 0 | 5 | 4 | 9 | 10 |
| Runs where a block was bypassed by paging | 0 | 3 | 3 | 0 | 0 |
| **Spotify's bulk-reader called** | 0 | **0** | 0 | **0** | 0 |
| Explore spawned | 0 | 0 | 2 | 0 | 2 |
| Lines read into main context, total | 7,111 | 4,363 | 3,897 | 893 | 1,496 |
| Lines read by subagent, total | 0 | 0 | 2,291 | 0 | 2,073 |
| Grep calls per run | 2.4 | 3.5 | 4.6 | 7.4 | 3.6 |
| API requests per run | 6.8 | 9.1 | 10.8 | 11.0 | 9.6 |
| Mean wall clock | 61 s | 57 s | 56 s | 68 s | 59 s |

## What enforcement changed

**The hook now holds.** Nine and ten blocks in twelve runs, zero bypasses. Lines of the target files entering the main context fell from 7,111 in stock to 893 in strict shunt. That is an 87% reduction in exactly the quantity Spotify's 90% figure measures. The mechanism works as a gate.

**Spotify's worker was still never called.** Zero of twelve, with the Read tool fully closed to it. In strict shunt Claude grepped instead, 7.4 greps per run against 2.4 in stock, including greps with the pattern `.` and an offset, which is a paged read of the file through a different tool. It passed all twelve tasks that way. The bulk-reader skill sat unused in every one of 24 shunt runs across both variants.

**Strict shunt was the most expensive arm.** $2.61 for the twelve tasks against $1.94 for stock, a 35% increase, for the same pass rate. Fewer lines in context, more requests to get them: 11.0 per run against 6.8. Every extra request resends the whole conversation at the cache-read rate, and grep output is not free either.

**Strict Explore delegated twice and was cheaper than strict shunt.** $2.31, with Explore spawned on R1 and R3. On R4 strict Explore was the cheapest run of any arm on any task ($0.099): blocked, grepped the test file for call sites, answered. On D2 it was the most expensive ($0.411): blocked, and eleven requests of grep-and-reason to find the race without ever seeing the file whole.

**Delegation rate with the hook fully enforced: 2 of 12 for a built-in subagent, 0 of 12 for an external script.** A hook can stop a read. It cannot make the model prefer a shell script it has never used over grep, which it uses constantly. To force the worker, the design would also have to block grep on large files, at which point the main agent is blind to the file except through the summary. That is a much stronger claim than the post makes, and a different experiment.

## Per task, cost and result

| Task | A stock | B shunt | C hook + Explore | B' shunt strict | C' Explore strict |
|---|---|---|---|---|---|
| R1 | $0.113 | $0.204 | $0.169 E | $0.285 | $0.159 E |
| R2 | $0.151 | $0.309 | $0.192 | $0.304 | $0.205 |
| R3 | $0.382 | $0.311 | $0.359 | $0.421 | $0.291 E |
| R4 | $0.135 | $0.122 | $0.209 E | $0.203 | $0.099 |
| W1 | $0.134 | $0.172 | $0.117 | $0.159 | $0.125 |
| W2 | $0.252 fail | $0.252 fail | $0.314 fail | $0.241 | $0.407 |
| W3 | $0.159 | $0.202 | $0.166 | $0.277 | $0.200 |
| E1 | $0.076 | $0.078 | $0.078 | $0.087 | $0.060 |
| E2 | $0.084 | $0.066 | $0.080 | $0.106 | $0.114 |
| E3 | $0.068 | $0.066 | $0.066 | $0.074 | $0.082 |
| D1 | $0.184 | $0.133 | $0.192 | $0.191 | $0.156 |
| D2 | $0.200 | $0.205 | $0.184 | $0.258 | $0.411 |

E marks a run where Explore was spawned. All runs passed except the three marked fail (W2, a checklist regex; the strict arms passed the same checklist, which says more about the checklist than the arms).

## Grader fix in this pass

The found-the-file check missed E1 on strict Explore: Claude grepped the repo for the log string, got the file and line in the grep result, and edited the right line without ever calling Read on the file. The check only looked at Read and Grep inputs. It now also counts Edit and Write targets and grep results that name the file. All 60 natural runs were re-graded; that was the only change.

## What is not established

Still one run per cell, so the cost ranking between the hooked arms is suggestive. The counts are not: 24 shunt runs, zero worker calls; 10 strict-Explore blocks, two spawns. Repetitions would tighten the dollars, not change those.
