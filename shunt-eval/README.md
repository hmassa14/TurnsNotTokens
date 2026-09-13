# shunt-eval

A paired evaluation of Spotify's "shunt" plugin for Claude Code against stock Claude Code, on a real Java monorepo, measuring the bill rather than tokens avoided.

Spotify's engineering post claimed a PreToolUse hook that blocks reads of files over 350 lines and redirects them to a cheap worker model cut Claude Code token usage by 90%. The number they measured was "tokens Claude would have read" minus "tokens in the summary it got back", estimated as characters divided by four, with the worker's own tokens uncounted and no dollar figure. This repo runs the same design, plus what the post described but did not ship, plus a version built only from Claude Code's own parts, on twelve tasks, and records cost, latency, behavior and correctness for every session from three independent sources.

Sixty-two headless sessions later, the short version:

- The hook, as shipped, was bypassed on every block it made. It allows any read that sets an offset or limit, and the model used that every time.
- With the exception removed, the hook held and cut target-file lines entering the main context by 87%. Spotify's number is real on its own metric.
- The worker behind the hook was called zero times in 24 runs. Blocked from reading, the model grepped.
- Stock Claude Code was the cheapest arm. The enforced hook cost 35% more for the same pass rate, because it turned one read into many turns, and with prompt caching a turn costs more than a file.

Everything below is reproducible from this directory with a Claude Code login and a Kafka checkout.

## Contents

1. [Why Kafka](#why-kafka)
2. [How the evaluation works](#how-the-evaluation-works)
3. [Setup and running it](#setup-and-running-it)
4. [The arms](#the-arms)
5. [The tasks](#the-tasks)
6. [What is measured](#what-is-measured)
7. [Results](#results)
8. [Caveats](#caveats)
9. [Layout](#layout)

## Why Kafka

The hook only matters on files over 350 lines, and stock Claude Code has its own gates (a 25,000-token page limit and a 256 KB refusal) that kick in on very large files. So the target repo needed many files in the band between those two limits, in a language Spotify's benchmark used. Apache Kafka trunk at commit `0ffb4f5`:

| | Kafka (Java + Scala) | Backstage (TypeScript), rejected |
|---|---|---|
| Source files | 6,448 | 7,348 |
| Files over 350 lines | 1,096 (17%) | 549 (7.5%) |
| Share of code in those files | 64% | 38% |

Every task's target file is between 616 and 1,879 lines and under 100 KB, so the hook fires and stock does not page. The clone is shallow (125 MB) and never modified; each run gets a fresh copy.

## How the evaluation works

One run is one fresh headless Claude Code session. The harness (`bin/run.py`):

1. Copies the pinned Kafka clone to a scratch workspace. Planted-bug tasks apply a one-line patch and commit it, so the diff later shows only what Claude changed.
2. Drops the arm's `.claude/` directory into the workspace root. That folder is the entire difference between arms: empty for stock, Spotify's hooks and skills for shunt, and so on.
3. Runs `claude -p "<prompt>"` with a fresh session id, a tool allowlist, a 40-turn cap, a 15-minute timeout, and OpenTelemetry pointed at a local receiver.
4. Collects three records: the JSON Claude Code prints (cost, tokens per model, turns, durations, the answer), the transcript it writes to `~/.claude/projects/` (every tool call, every API request's usage), and the OTLP export (metrics and per-call events).
5. Grades the answer, the diff, or the written file against the task's key, and checks the transcript for whether the target file was ever read, grepped, or delegated.

`bin/grid.py` runs tasks x arms x repetitions for one prompt variant, interleaved across arms so time of day never lines up with one arm, and resumes if interrupted. `bin/table.py` turns run directories into the comparison tables.

The three token sources were checked against each other on every run and agree exactly. Cost is recomputed from tokens at list price with cache writes split by TTL (Claude Code writes the system prompt at the 1-hour rate and file contents at the 5-minute rate) and matches Claude Code's own figure to four decimals.

## Setup and running it

Requirements: Claude Code 2.1.269 or later logged in (a subscription works; usage counts against its limits and the dollar figures are list-price estimates), Python 3.11, `jq`, a Kafka clone.

```
git clone --depth 1 https://github.com/apache/kafka.git /path/to/kafka
cd /path/to/kafka && git checkout 0ffb4f5

# telemetry receiver, once per session
python3 bin/otlp_receiver.py runs/_otel 4318 &

# one run
python3 bin/run.py --task tasks/R1.json --arm stock --variant natural --rep 1 \
  --model claude-sonnet-5 --repo /path/to/kafka --runs-dir runs

# its trace report
python3 bin/report.py runs/<run-id> tasks/R1.json runs/_otel > runs/<run-id>/report.md

# the whole grid, resumable
python3 bin/grid.py --variant natural --reps 1 --model claude-sonnet-5 --repo /path/to/kafka

# tables
python3 bin/table.py runs --variant natural
```

Notes. `bypassPermissions` is refused when running as root, so the runner uses `acceptEdits` plus an allowlist. Headless mode waits on stdin; the runner closes it. Raw OTLP dumps carry account identifiers and are gitignored; `parse_otel.py` strips them before anything is committed. The code-write tasks grade on compile only if Gradle has been warmed offline in the clone (`./gradlew :storage:compileJava` once with network); otherwise they grade on the checklist alone.

Before any grid: run the two smoke tasks in `tasks/smoke/` once. The first proves the pipeline end to end; the second proves the Explore override is running on Haiku.

## The arms

| Arm | What is in `.claude/` | What it tests |
|---|---|---|
| A `stock` | an empty settings file | Claude Code as installed. The "it already delegates" claim. |
| B `shunt` | Spotify's two hooks, two scripts and two skills, verbatim from `spotify/portal-ai-plugins`. One file swapped: the Portal call becomes a one-turn Haiku call with the same mode instructions, and every call's cost is saved. | Their design as shipped. |
| C `hook-explore` | the same hooks with the block message pointing at Claude Code's built-in Explore subagent, an `Explore.md` pinning it to Haiku, and a rule letting the subagent read whole files. | The same idea using only Claude Code's own parts. |
| B' `shunt-strict` | B with the hook's offset/limit exception removed. A big file cannot be Read from the main agent at all. | What the post described. |
| C' `hook-explore-strict` | C with the same exception removed. | Same, with the built-in subagent. |

Each arm was hand-verified before spending: the hook blocks a 770-line read on this Claude Code version, the Haiku worker answers a real question correctly, and Explore runs on Haiku.

## The tasks

Twelve tasks in four categories, each with a mechanically derived answer key. Every task has two prompts: **named**, which gives the file path, and **natural**, which is the question a developer would type with no path, so the session has to find the file first. All reported results use the natural prompts.

| Id | Category | Target | Grader |
|---|---|---|---|
| R1 | bulk-read | BrokerLifecycleManager, 770 lines: every event and the state it sets | recall over 12 names and 5 states |
| R2 | bulk-read | RemoteLogManagerConfig, 616 lines: every config key, type, default | recall over 29 keys |
| R3 | bulk-read, two files | GroupCoordinatorShard + RecordHelpers, 1,496 + 841 lines | recall over 22 cases and 30 helpers |
| R4 | bulk-read, source + test | BatchAccumulator + its test, 646 + 764 lines: untested public methods | recall over 14 methods, 4 untested |
| W1 to W3 | code-write | a new Connect transform, Streams metrics class, config class from a reference | compile plus checklist |
| E1 to E3 | precise edit | one log-level change or rename where the same text appears several times | exact diff, decoys untouched |
| D1, D2 | planted bug | a `synchronized` removed; an append hoisted out of its lock | names the method, a line in range, the race |

Full prompts, keys, and derivation commands are in `docs/TASKS.md`.

## What is measured

Per run, grouped the way the results tables are grouped.

**Performance.** Score and pass from the grader. Whether the target file was found (a run that never read, grepped, or delegated it is a miss). Lines of the target read into the main context, and separately by a subagent or worker. Tool calls by type. Reads blocked by the hook and blocks bypassed with a paged read. Subagent and worker calls. Re-reads after a delegation.

**Latency.** Wall clock. API requests. Longest single API call and time to first token from OpenTelemetry. Time in tools. Time in the worker.

**Cost.** Total at list price, main model and worker separately. Tokens in each priced bucket: uncached input, cache write at the 1-hour and 5-minute rates, cache read, output. Cost split at the first touch of the target file into a finding phase and an answering phase. Spotify's own metric, characters divided by four avoided, computed on the same runs for comparison.

Where each number comes from, field by field, is in `docs/METRICS.md`.

## Results

Twelve tasks, five arms, natural prompts, one run per cell, Sonnet 5 as the main model and Haiku as the worker and as Explore, 2026-09-12.

| | A stock | B shunt | C Explore | B' strict | C' strict |
|---|---|---|---|---|---|
| Pass | 11/12 | 11/12 | 11/12 | 12/12 | 12/12 |
| Found target file | 12/12 | 12/12 | 12/12 | 12/12 | 12/12 |
| Cost, twelve tasks | $1.94 | $2.12 | $2.13 | $2.61 | $2.31 |
| Runs where the hook blocked | 0 | 5 | 4 | 9 | 10 |
| Blocks bypassed by paging | 0 | 3 | 3 | 0 | 0 |
| Spotify's worker called | 0 | 0 | 0 | 0 | 0 |
| Explore spawned | 0 | 0 | 2 | 0 | 2 |
| Target lines into main context | 7,111 | 4,363 | 3,897 | 893 | 1,496 |
| API requests per run | 6.8 | 9.1 | 10.8 | 11.0 | 9.6 |
| Grep calls per run | 2.4 | 3.5 | 4.6 | 7.4 | 3.6 |

The one failure shared by A, B and C is W2, on a checklist regex with compile not run; the strict arms passed the same checklist.

**Finding 1. The shipped hook is not enforcement.** Spotify's `check-file-size` allows any Read with an offset or limit. Every one of the 9 blocks it made in arms B and C was followed by a paged read or a grep. In R2 the model re-read a 616-line file with `limit=616`, the whole file, and the hook let it through.

**Finding 2. The enforced hook works and the worker still goes unused.** With the exception removed, blocks held with zero bypasses and 87% fewer target lines entered the main context. The bulk-reader script was invoked in none of the 24 shunt runs. Blocked from reading, Sonnet 5 grepped, 7.4 times per run, including greps with the pattern `.` and an offset. A hook can stop a tool. It cannot make the model prefer an unfamiliar script over one it uses constantly.

**Finding 3. Stock was cheapest, and the reason is turns, not tokens.** A 770-line file costs about four cents to read once on Sonnet 5 and a tenth of a cent to re-read from cache on every later turn. A blocked read became eight extra API requests, each resending the whole conversation at the cache-read rate and thinking again. On R1, stock re-sent 83,000 cached tokens across 3 requests; shunt re-sent 373,000 across 11. The hook saved the four cents and spent nine avoiding it. Spotify's metric counts only the first side of that trade.

**Finding 4. Delegation, when it happened, worked and was not cheaper.** The built-in Explore was spawned 2 of 12 times in each C arm. Every such run passed with zero target lines in the main context, cost more than stock, and took two to four times longer.

**Finding 5. Forced grep is sometimes a win.** Strict arms were cheapest on four tasks, including finding the D1 race from 50 lines of a 1,019-line file. When the block does not add turns, it saves money. It usually adds turns.

Per-pass write-ups, machine-built tables, and every run's trace report are under `results/`. The stock baseline on named prompts, showing that with the path in the prompt stock reads the file whole in one call and delegates nothing, is in `results/01-named-stock-baseline`.

## Caveats

- One run per cell. The counts (worker calls, blocks, bypasses, spawns) are established. The cost ranking among the hooked arms is observed, not proven; a single search choice moves one run by 50%.
- The worker is Haiku through headless Claude Code, not Gemini Flash through Portal. That call carries Claude Code's tool definitions, about 25,000 cache-write tokens per call, which a raw API call would not. Irrelevant to the result, since the worker was never called, but it would matter if it had been.
- Two graders are keyword-based (bug reports, key lists) and one is too literal (code-write checklist). Weaknesses and fixes are listed in `docs/HARNESS.md`.
- Sonnet 5 on Claude Code 2.1.269. A model that reads whole files by default, which is what the 350-line threshold was designed for, would trigger the hook more and might delegate. That is the experiment to run next, on an older model.

## Layout

```
README.md            this file
docs/                design (PLAN), build spec (HARNESS), metric sources (METRICS), tasks and keys (TASKS)
tasks/               one JSON per task with both prompts and the grader; setup patches for planted bugs; smoke/
arms/                one .claude/ directory per arm
bin/                 run.py, grid.py, otlp_receiver.py, parse_transcript.py, parse_otel.py, grade.py, report.py, table.py, storyboard.py
results/             one folder per pass: README, tables, per-run report/result/transcript/otel/grade; runs.jsonl
figures/             SVG source and PNG exports; figures/post/ is the eight-figure set for the write-up, in post order
runs/                gitignored: raw run directories and OTLP dumps
```
