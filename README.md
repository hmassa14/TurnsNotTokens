# Tokens Are Cheap, Turns Are Not

An evaluation of Spotify's "shunt" plugin for Claude Code — a PreToolUse hook that blocks reads of files over 350 lines and hands them to a cheap worker model — against stock Claude Code, on Apache Kafka, measuring the bill rather than tokens avoided.

- **The write-up:** [`index.html`](index.html) (served by GitHub Pages), source in [`shunt-eval/post.html`](shunt-eval/post.html).
- **The harness, tasks, arms and results:** [`shunt-eval/`](shunt-eval/) — start with [`shunt-eval/README.md`](shunt-eval/README.md).
- **The evaluation framework** (hypotheses, task categories, metrics, controls): [`shunt-eval/docs/EVAL_FRAMEWORK.md`](shunt-eval/docs/EVAL_FRAMEWORK.md).
- **The final grid:** [`shunt-eval/results/06-natural-clean-grid/`](shunt-eval/results/06-natural-clean-grid/) — 189 sessions, three setups, one folder per run, tables and paired statistics.

Short version: with Spotify's hook enforced, Claude read 87% fewer lines of the big files. The tokens the frontier model was billed for went up 41%, and the dollar cost went up 8% with the plugin as shipped and 19% with the hook doing what the post describes, at the same pass rate. Whether a task came out cheaper was decided by the task: a slice of a big file, the block saves; most of the file, it costs. A line count can't tell those apart.

`madlibs/` is an unrelated small project that used to live at the root.
