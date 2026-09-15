# Figures

Hand-drawn SVG plus figures generated from the transcripts. Numbers come from `results/06-natural-clean-grid`: the SC1 runs (stock rep 1, as shipped rep 1, as described rep 3) for the one-question figures, SB1 as shipped rep 1 for the call-out, and `summary-shipped.json` / `summary-enforced.json` (from `bin/summarize.py`) for the counts and means.

`post/` holds the set the post uses, rendered at 2x by `post/render.js`:

| File | In the post | What it shows |
|---|---|---|
| `A-hook-in-the-loop.png` | What Spotify built | The tool loop with the PreToolUse hook in the path of a Read, and what the model did after a block in each hook setup: as shipped, a paged read allowed through 9 of 26 times; as described, the worker 4 of 96 times, grep 53, a paged read tried and refused 33. |
| `B-setup.png` | Our experiment | One run: fresh Kafka copy with no history, one `.claude` folder, sandboxed headless session, three records, grade. The three folders, one change apart. |
| `C-callout-published-hook.png` | Sidebar on the removed rule | The config-keys task under the hook as shipped: a blocked read followed by two paged reads the hook allows, covering the whole file. |
| `D-one-question-request-by-request.png` | Results | Storyboard of the broker-lifecycle question in all three setups: stock reads the file on request 2 of 3; as shipped pages around the block; as described delegates, verifies with one grep, answers on request 9. |
| `E-requests-as-bars.png` | Results | The same three runs as bars, one per API request, height is context re-sent; blocked requests and the worker call marked. |
| `F-where-the-money-went.png` | Results | The same three runs in cents, stacked by price bucket, worker call included. Re-sends and output grew with the request count. |
| `G-headline.png` | Results | Three small multiples over 21 tasks and 189 runs, three setups: target-file tokens in context, API requests per run, cost per run. |
| `H-by-category.png` | Results | Each hook setup's cost relative to stock by task type, paired per task with 95% bootstrap intervals, plus the split by what the model did after the block. |

`post/story_callout.html` and `post/story_main.html` are the storyboard fragments figures C and D are built from:

```
bin/storyboard.py --no-tokens --no-css "results/06-natural-clean-grid/SB1-shunt-r1:2-4:B · Spotify's hook, as shipped" > figures/post/story_callout.html
bin/storyboard.py --no-tokens --no-css "results/06-natural-clean-grid/SC1-stock-r1:2:A · stock" \
    "results/06-natural-clean-grid/SC1-shunt-r1:3,5-6:B · as shipped" \
    "results/06-natural-clean-grid/SC1-shunt-strict-r3:2,5-9:C · as described" > figures/post/story_main.html
```

`post/build_post.py` assembles the eight figures from these fragments, the two summary files, the SC1 transcripts, and hand-drawn SVG for A and B (the SVG head and Figure A base live in `post/post-figures-v1-five-arms.html`); it writes `post/post-figures.html`. Then `node post/render.js` (run from `post/`) screenshots each figure to `post_<name>.png`; copy those over `<name>.png` to update the post.

Palette: stock `#0A9385`, hook `#B84E28`, validated with the dataviz skill's checker for light and dark surfaces.
