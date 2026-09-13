# Figures

Hand-drawn SVG, source in `figures.html`, exported at 2x as PNG. Numbers come from the R1 runs in `results/03-natural-three-arms` (stock and shunt) and the per-arm counts in `results/03` and `04`.

1. `fig1-hook-and-three-exits.png`: where the PreToolUse hook sits in Claude Code's tool loop, and the three calls the model made after a block (worker 0 of 24, paged read 9 of 9 under the shipped hook, grep under the strict hook).
2. `fig2-r1-trace-stock-vs-hook.png`: the R1 task request by request. Bar height is cached context re-sent per request. Stock: 3 requests, 83k tokens. Hook: 11 requests, 373k tokens, the fourth blocked.
3. `fig3-where-the-money-went.png`: the same two runs in cents, stacked by price bucket. The file bucket barely moved; re-reads and output grew with the request count.
