# Results

Passes in the order they were run. Each folder has a `README.md` with the write-up, `tables.md` built by `bin/table.py`, and one folder per run holding the trace report, raw result JSON, parsed transcript, parsed telemetry, grade, and any diff or written file. `runs.jsonl` is one row per run across all passes.

| Pass | What | Runs | Read this for |
|---|---|---|---|
| `01-named-stock-baseline` | R1 and D1, named prompts, stock only | 2 | The instrumentation validated end to end; what stock does when the path is in the prompt (reads whole, delegates nothing) |
| `02-natural-pilot-r1-d1` | R1 and D1, natural prompts, arms A, B, C | 6 | First sight of the bypass: every block followed by a paged read |
| `03-natural-three-arms` | all twelve tasks, natural prompts, arms A, B, C | 36 | Worker called 0 of 12; hook fired in only half the runs; stock cheapest |
| `04-natural-strict-arms` | all twelve tasks, natural prompts, arms B' and C' | 24 | Hook enforced, 87% fewer lines in context, worker still 0 of 12, strict shunt 35% over stock |

Grader corrections made during these passes are noted in each README. All 60 natural runs were re-graded after the last correction, so the numbers across `03` and `04` are on the same grader.

Runs on the smoke tasks are not included.
