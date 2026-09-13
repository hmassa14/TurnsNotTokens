# Baseline pass 1: stock Claude Code, one run each of R1 and D1

Date 2026-09-12. Claude Code 2.1.269, main model `claude-sonnet-5`, Kafka `0ffb4f5`, arm `stock` (empty `.claude/settings.json`, no hooks, no CLAUDE.md), headless `claude -p` with `--permission-mode acceptEdits` and an explicit tool allowlist, fresh session id, fresh workspace copy per run, OpenTelemetry exported to a local OTLP receiver. Run in the Claude Code on the web container under the account's OAuth login, so usage drew on the subscription; the dollar figures are Claude Code's list-price computation, verified independently from the token counts.

Each task directory holds the full trace report (`report.md`), the raw result JSON, the parsed transcript with every tool call and API request, the parsed OpenTelemetry records, the grade, and the run metadata.

## The two runs side by side

| | R1 bulk-read (770-line file) | D1 planted bug (1,019-line file) |
|---|---|---|
| Grade | pass, score 1.0 (12/12 events, 5/5 states, initial state) | pass, score 1.0 (named `lock`, lines 504 to 526, get-then-put race, proposed `putIfAbsent`) |
| Cost, list price | $0.2017 | $0.1253 |
| Wall clock | 37.4 s | 52.8 s |
| Time waiting on API | 34.7 s | 50.4 s |
| API requests | 3 | 2 |
| Tool calls | 2 (Bash `find`, Read whole file) | 1 (Read whole file) |
| Subagents | 0 | 0 |
| Lines that entered context | 770 | 1,019 |
| Input, uncached | 6 | 4 |
| Cache write, 1h TTL (system prompt, tools) | 29,487 | 5,577 |
| Cache write, 5m TTL (file contents, results) | 13,771 | 17,954 |
| Cache read | 59,364 | 53,225 |
| Output (of which thinking) | 3,744 (2,558) | 4,741 |
| Longest single API call | 28.4 s (the answer) | 47.1 s (the answer) |

## What the baseline shows

**Stock Claude Code did not delegate.** On both tasks it read the whole file with one `Read` call and answered. No Explore subagent, no Grep-first narrowing, no paging. Both files are over Spotify's 350-line threshold and under stock's own 25k-token page limit, so the hook would have fired on both reads in arm B. This is the delegation rate the Reddit argument assumed was high. On these two tasks it was zero.

**The file read is the cheap part of the bill.** In R1 the whole 770-line file cost 13,771 tokens of 5-minute cache write, $0.034. The system prompt and tool definitions cost 29,487 tokens of 1-hour cache write, $0.118, on the very first request before any file was touched. Output tokens cost $0.037. So the read Spotify's hook would have blocked was 17% of the run's cost; the fixed per-session overhead was 58%. In D1 the same shape: the file was $0.045 of $0.125.

**Latency is the answer, not the read.** The Read tool returned in 115 to 130 ms. The API call that produced the final answer took 28 s in R1 and 47 s in D1, most of the run. A 10 to 30 second worker round trip in arm B would be added on top of that, not instead of it.

**Sonnet 5 found the planted race unaided.** D1 asked for a review of a file where `synchronized` had been removed from `lock`. The answer named the method, the exact check-then-act lines, the asymmetry with the still-synchronized `unlock`, and the `putIfAbsent` fix. It also flagged `removeStartupState` writing to the same map and a secondary note on lifecycle fields, neither of which was the planted bug but both of which are defensible. The grader records the two named false-positive methods without failing the run.

**All three telemetry sources agree exactly.** Result JSON usage, transcript usage deduplicated by request id, and OpenTelemetry `claude_code.token.usage` gave identical counts on both runs: for R1, 6 / 43,258 / 59,364 / 3,744 across input, cache write, cache read, output. The OTel `api_request` events supplied the per-call latencies; the transcript timestamps approximated them within about a second.

**Cost recomputes only with the TTL split.** Claude Code's `total_cost_usd` matched a recomputation from tokens to four decimals once cache writes were priced at 2x input for 1-hour entries and 1.25x for 5-minute entries. Pricing all writes at 2x overstated R1 by 10%. This is now the formula in `METRICS.md`.

## Fixes made during this pass

- `--permission-mode bypassPermissions` is refused when Claude Code runs as root. The runner uses `acceptEdits` plus an explicit `--allowedTools` list, which works as root and on a laptop.
- Claude Code waits 3 s on stdin in headless mode; the runner closes stdin.
- The transcript lives under `~/.claude/projects/<cwd with / and _ replaced by ->/`. The runner encodes the absolute path and falls back to searching by session id.
- The `key_list` grader matched identifiers by substring, so `BeginControlledShutdownEvent` tripped the deny item `ControlledShutdownEvent`. Matching is now on identifier boundaries. R1 went from a false fail to a pass with no change to the answer.

## What this pass does not show

One run each, no repetitions, one model, no other arms. It establishes that the instrumentation works end to end and what the stock baseline looks like on the two workflows. The comparison is the next pass: the same two tasks under arm B (Spotify's hooks with a Haiku worker) and arm C (hooks plus Haiku Explore), then repetitions.
