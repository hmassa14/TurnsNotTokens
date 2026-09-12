# Harness design

Companion to `PLAN.md`. This describes what gets built: directory layout, how a run executes, what gets recorded, how each metric is computed, and how outputs are graded. Task definitions with answer keys live in `TASKS.md` and `tasks/*.json`.

## 1. Layout

```
shunt-eval/
  PLAN.md            experiment design
  HARNESS.md         this file
  TASKS.md           task set with answer keys, human readable
  tasks/
    <task-id>.json   one file per task: prompt, category, files, grader spec
  arms/
    stock/           empty .claude/ (control)
    shunt/           Spotify's plugin verbatim + swapped aika.sh (Haiku worker)
    hook-explore/    same two hooks, deny reason points at Explore; .claude/agents/Explore.md pinned to haiku
  bin/
    run.py           runs one (task, arm, rep), writes runs/<run-id>/
    grid.py          schedules the full grid, interleaved across arms
    otlp_receiver.py local OTLP HTTP receiver, one JSON file per POST
    parse_transcript.py  transcript JSONL -> per-tool-call table
    parse_otel.py    OTLP dumps -> metrics and events table
    grade.py         applies the task's grader to the run's output
    replay_step0.py  Step 0: share of Read tokens from files > 350 lines in existing transcripts
    analyze.py       paired stats and tables
  runs/
    <run-id>/        one directory per run (gitignored)
  results/
    runs.jsonl       one row per run after grading
```

Run id is `<task-id>__<arm>__r<rep>__<yyyymmdd-hhmmss>`.

## 2. One run, step by step

1. **Workspace.** Copy the pinned Kafka checkout to a fresh temp directory (a `git worktree` or `cp -r` of the shallow clone; either is a few seconds). Apply the task's setup patch if it has one (planted-bug tasks modify one file). Copy the arm's `.claude/` directory into the workspace root. Record the Kafka commit, Claude Code version, and arm hash into `meta.json`.
2. **Telemetry on.** Start the OTLP receiver once per grid, not per run. Each run gets the env below plus a unique `OTEL_RESOURCE_ATTRIBUTES=run.id=<run-id>` so its records can be separated.
3. **Execute.**

   ```
   env -u CLAUDECODE -u CLAUDE_CODE_ENTRYPOINT \
     CLAUDE_CODE_ENABLE_TELEMETRY=1 \
     OTEL_METRICS_EXPORTER=otlp OTEL_LOGS_EXPORTER=otlp OTEL_TRACES_EXPORTER=otlp \
     OTEL_EXPORTER_OTLP_PROTOCOL=http/json \
     OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318 \
     OTEL_METRIC_EXPORT_INTERVAL=1000 OTEL_LOGS_EXPORT_INTERVAL=1000 \
     OTEL_LOG_TOOL_DETAILS=1 \
     SHUNT_RUN_DIR=runs/<run-id> \
     claude -p "<task prompt>" \
       --model <main-model> \
       --session-id <uuid> \
       --permission-mode bypassPermissions \
       --max-turns 40 \
       --output-format json \
       > runs/<run-id>/result.json 2> runs/<run-id>/stderr.txt
   ```

   Wall clock is measured around this call by the harness, independently of `duration_ms`. A 15-minute timeout kills the run and marks it `timeout`.

   Arm B's worker scripts read `SHUNT_RUN_DIR` and append every worker call's JSON output to `runs/<run-id>/worker/<n>.json`. That is the only way the worker's cost survives.
4. **Collect.** Copy `~/.claude/projects/<encoded-workspace>/<session-id>.jsonl` and the `<session-id>/subagents/` directory into `runs/<run-id>/transcript/`. Capture `git diff` and `git status --porcelain` of the workspace into `runs/<run-id>/diff.patch`. For code-write tasks also copy the new file.
5. **Grade.** `grade.py` applies the task's grader spec to the result text, the diff, or the workspace, and writes `grade.json`.
6. **Row.** Parse everything into one JSON row appended to `results/runs.jsonl`.

The grid interleaves arms per task (`task1/A, task1/B, task1/C, task2/A, ...`) so time-of-day and cache warmth do not line up with one arm. Repetitions are separate passes over the whole grid.

## 3. What gets recorded per run

Field names in `results/runs.jsonl`. Source in brackets.

**Identity**
- `run_id`, `task_id`, `category`, `arm`, `rep`, `main_model`, `claude_code_version`, `kafka_commit`, `started_at` [meta]

**Cost and tokens**
- `cost_usd_main` [result.json `total_cost_usd`]
- `cost_usd_worker` [sum of worker/*.json `total_cost_usd`; 0 in A and C]
- `cost_usd_total` = main + worker. **Headline metric.**
- `cost_usd_by_model` [result.json `modelUsage[*].costUSD`, plus worker files]. In arm C the Haiku Explore shows up inside `modelUsage` already.
- `tokens_main_input_uncached`, `tokens_main_cache_creation`, `tokens_main_cache_read`, `tokens_main_output` [result.json `usage`]
- `tokens_worker_input`, `tokens_worker_output` [worker files]
- `tokens_by_model` [OTel `claude_code.token.usage` summed by `model` and `type` attributes; cross-check against result.json, they should agree]
- `spotify_style_tokens_avoided` [transcript: for every Read blocked by the hook or delegated, characters of the target file / 4, minus characters / 4 of the summary that entered context]. Computed the way `evals/benchmarks.json` in the shunt repo does it, reported next to the ledger numbers so the two methods can be compared on the same run.

**Latency**
- `wall_ms` [harness stopwatch]
- `duration_ms`, `duration_api_ms` [result.json]
- `api_calls`, `api_latency_ms_p50`, `api_latency_ms_max` [OTel `api_request` events, `duration_ms`]
- `hook_ms_total` [OTel `claude_code.hook` spans; 0 in A]
- `worker_ms_total` [worker files `duration_ms`]
- `time_to_first_delegation_ms` [transcript timestamps]

**Turns and behavior** [transcript unless noted]
- `num_turns` [result.json]
- `reads_total`, `reads_targeted` (offset or limit set), `reads_whole_file`
- `reads_blocked_by_hook` [OTel `tool_decision` with `source` naming the hook, cross-checked with transcript tool results starting with the block reason]
- `reads_gated_by_stock` (result contains "exceeds maximum allowed" or "PARTIAL view")
- `hook_bypass_via_paging` (a blocked or gated read on file F followed within 3 tool calls by an offset/limit read of F)
- `bash_reads_blocked`
- `agent_spawns`, `agent_spawn_models` [result.json `subagent_stats.by_type` and subagents/*.jsonl `model`]
- `worker_calls`, `worker_files_sent`, `worker_lines_sent`
- `reread_after_delegation` (file F sent to worker or Explore, then Read directly by the main agent later)
- `reads_dedup_reminders` (tool result starts with "This file is already in your context")
- `files_read_over_350`, `lines_read_over_350`, `lines_read_total`
- `timeout`, `max_turns_hit`, `is_error` [harness, result.json]

**Quality**
- `score` in [0, 1], `pass` boolean, `grader_notes` [grade.json]

## 4. Grader specs

Each task JSON carries one `grader` object. Four grader types.

**`key_list`** (bulk-read questions). `required`: list of identifiers. `match`: case-insensitive substring of the identifier in the result text. `score` = recall over required minus `penalty` (default 0.05) per invented item, where invented items are matched against a `deny` list of plausible wrong answers the task author supplies (things in the same file that look right but are not). `pass` = recall at or above 0.9 with no more than one invented item. The result text is the `result` field of result.json.

**`compile_and_checklist`** (code-write). Steps: the output file exists at the required path; `./gradlew :<module>:compileJava --offline -q` exits 0 (the harness pre-warms Gradle once on the pinned commit so `--offline` works); each `required_symbols` entry appears in the file (regex); `required_behavior` regex appears. `score` = fraction of checks passed, `pass` = all pass. Compile failure sets score to 0.

**`exact_diff`** (precise edit). `git diff` of the workspace, whitespace-normalized, must contain exactly the expected hunk and no other changed lines. `pass` is binary. `score` = 1 if pass, 0.5 if the right line changed but a decoy also changed, 0 otherwise. The task JSON lists `decoy_lines` that must remain untouched.

**`bug_report`** (planted bug). Parse the result text for the target method name and any line number within `line_tolerance` (default 15) of the planted change, and for at least one of the `race_keywords`. All three required for `pass`. The task JSON lists `false_positive_methods` that must not count.

Every grader is run once on a known-correct answer and once on a known-wrong answer before the grid, and those two checks are stored in `tasks/<task-id>.selftest.json`.

## 5. Arm configuration details

**A. stock.** Workspace `.claude/` contains only an empty `settings.json`. No CLAUDE.md.

**B. shunt.** `plugins/shunt` from `spotify/portal-ai-plugins` copied verbatim into the workspace's `.claude/` as a local plugin (hooks.json, both hook scripts, both skills, `scripts/bulk-read`, `scripts/code-write`). One file replaced: `scripts/lib/aika.sh`. Its `aika_invoke` function becomes

```
claude -p "$payload" --model haiku --output-format json \
  --system-prompt "$MODE_INSTRUCTIONS" --max-turns 1 --disallowedTools "*" \
  > "$SHUNT_RUN_DIR/worker/$(date +%s%N).json"
jq -r .result "$SHUNT_RUN_DIR/worker/..."
```

with `MODE_INSTRUCTIONS` set to the bulk-reader or code-writer prompt from the shunt README, verbatim. `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` are unset inside the script. The 180-second `SHUNT_TIMEOUT_SECONDS` default is kept. Verified once by hand before the grid: a Read on a 400-line file returns the block reason to Claude, and Claude then invokes the skill.

**C. hook-explore.** Same two hook scripts with one string change in the block reason: "Use the Explore subagent (Agent tool, subagent_type Explore) to answer your question about this file instead of reading it directly." Plus `.claude/agents/Explore.md`:

```
---
name: Explore
description: Fast read-only search agent for large files. Reads files and reports findings; never edits.
model: haiku
tools: Read, Grep, Glob, Bash
---
You are a file search specialist. Answer the caller's question about the named files in terse bullets. Quote exact identifiers. Do not modify anything.
```

No bulk-read script. Skills are not needed; the Agent tool is already in the main prompt.

The hooks in B and C both allow offset/limit reads through. That is Spotify's rule and it stays, because the point is to test their design as shipped.

## 6. Telemetry receiver

`otlp_receiver.py` is a 40-line `http.server` that accepts POST on `/v1/metrics`, `/v1/logs`, `/v1/traces`, and writes each body to `runs/_otel/<epoch-ns>-<signal>.json`. `parse_otel.py` groups records by the `run.id` resource attribute. The `tool_decision` event carries `decision`, `source`, `tool_name`, and `tool_parameters`; the `api_request` event carries `model`, `duration_ms`, and token counts; `claude_code.token.usage` carries `type` (input, output, cacheRead, cacheCreation) and `model`.

If the OTLP path fails on a run, the row is still complete from result.json and the transcript. OTel is the cross-check and the per-call latency source, not the only source.

## 7. Step 0 replay

`replay_step0.py` walks `~/.claude/projects/**/*.jsonl`, finds every Read tool call and its result, counts result characters / 4 as tokens, looks up the file's line count at the time if the file still exists (else uses the result's own line count), and reports: share of Read calls on files over 350 lines, share of Read tokens from those calls, and how many were already targeted with offset/limit. That share is the upper bound on what a 350-line hook can save on your own workload. Runs in seconds, costs nothing.

## 8. Analysis

`analyze.py` reads `results/runs.jsonl` and produces:

- Per category and overall: mean and median `cost_usd_total` per arm, paired difference vs A with a bootstrap 95% interval, Wilcoxon signed-rank p-value.
- Same for `wall_ms` and `tokens_main_input_uncached + cache_creation` (the closest ledger analogue to Spotify's number).
- `spotify_style_tokens_avoided` next to the ledger delta, per run, so the gap between the two methods is visible.
- Quality: pass rate per arm and category, sign test vs A, and pass^3 per task.
- Behavior table: delegation rate in A, blocked reads and bypass rate in B and C, re-read-after-delegation rate.

Output is a Markdown report and the CSV behind it.

## 9. Pre-grid checklist

1. Step 0 replay run and reported.
2. Hook block confirmed by hand on v2.1.269 with the older `decision`/`reason` JSON form (if it no longer blocks, switch the script to `hookSpecificOutput.permissionDecision: deny` and note it).
3. Each grader self-tested against a right and a wrong answer.
4. One stock run end to end, all three telemetry sources present in the row.
5. Pilot: 4 tasks (one per category) x 3 arms x 1 rep. Eyeball the rows. Then the grid.
