# Figures

Hand-drawn SVG plus storyboards generated from the transcripts. Numbers come from the R1 stock run in `results/03-natural-three-arms` and the R1 run under the enforced hook in `results/04-natural-strict-arms` (arm `shunt-strict`), plus the twelve-task means in both.

## For the post: `post/`

Seven figures in the order the post uses them. Source is `post/post-figures.html` (one page, all seven, built by `post/build_post.py` from the transcripts); `post/render.js` splits it into one page per figure and exports each at 2x with Playwright. Palette validated with the dataviz checks: stock teal `#0A9385`, hook rust `#B84E28` (dark mode `#1E9A8C` / `#C97440`).

The post compares two arms only: stock, and Spotify's hook with the offset/limit exception removed (arm `shunt-strict` in the results, called simply "the hook" in the post). The published hook without that fix is not a third arm here — it is the subject of the call-out in figure C, which is the evidence for why the fix was necessary before the comparison could mean anything.

| File | Section | What it shows |
|---|---|---|
| `A-hook-in-the-loop.png` | What the hook claims to do | Where a PreToolUse hook sits in the tool loop, and what the model did after a block: never Spotify's worker, grep on every enforced run, a paged read on every block before the exception was closed. |
| `B-setup.png` | The setup | One run is one fresh session on a pinned Kafka copy; the only difference between the two arms is the `.claude/` folder. |
| `C-callout-published-hook.png` | Call-out, inside the setup section | R1 under the hook exactly as Spotify published it: the block, then a read with an offset, which the published rule allows. This is why the comparison uses the hook with that rule removed. |
| `D-one-question-request-by-request.png` | One question, traced | R1 under stock (one request) and under the enforced hook (five of sixteen requests): what the model was given, what it decided, what came back. Real excerpts from the transcripts. |
| `E-requests-as-bars.png` | Same question, as bars | All of R1's requests as bars, height is context re-sent. Stock: 3 requests, 83k tokens. Hook: 16 requests, 601k. |
| `F-where-the-money-went.png` | Where the money goes | The same two runs in cents, stacked by price bucket. The file bucket barely moved; re-sends and output grew with the request count. |
| `G-headline.png` | The result | Three small multiples, stock against the hook, over twelve tasks: target-file lines in context, API requests, and cost. |

`post/story_callout.html` and `post/story_main.html` are the storyboard fragments figures C and D are built from:

```
bin/storyboard.py --no-tokens --no-css "results/03-natural-three-arms/R1-shunt:4-6:Spotify's hook, as published"
bin/storyboard.py --no-tokens --no-css results/03-natural-three-arms/R1-stock:2:"A · stock" \
    "results/04-natural-strict-arms/R1-shunt-strict:4-5,10-11,15:B · Spotify's hook, enforced"
```

`post/build_post.py` assembles the seven figures from these fragments plus hand-drawn SVG for A, B and G; run it after regenerating the storyboards to rebuild `post-figures.html`.

## Earlier set

Source in `figures.html`, exported at 2x. Superseded by `post/` for the write-up; kept for reference.

1. `fig1-hook-and-three-exits.png`: an earlier, five-arm version of figure A.
2. `fig2-one-task-step-by-step.png`: the R1 question under stock and the shipped (unenforced) hook, uncropped, with token counts.
3. `fig3-r1-trace-stock-vs-hook.png`: an earlier version of figure E, against the shipped hook rather than the enforced one.
4. `fig4-where-the-money-went.png`: an earlier version of figure F, same pairing as fig3.
