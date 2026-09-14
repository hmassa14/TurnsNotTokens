# Figures

Hand-drawn SVG plus figures generated from the transcripts. Numbers come from `results/05-natural-second-grid`: the SC1 stock and hook runs (rep 1) for the one-question figures, and `summary.json` (from `bin/summarize.py`) for the counts and means. Figure C is from the pilot in `results/03-natural-three-arms`, where the published hook's offset exception was still open.

`post/` holds the set the post uses, rendered at 2x by `post/render.js`:

| File | In the post | What it shows |
|---|---|---|
| `A-hook-in-the-loop.png` | What Spotify built | The tool loop with the PreToolUse hook in the path of a Read, and what the model did after each of the 85 blocks: the worker script 9 times, grep or a shell search 47 times, a paged read 26 times (refused). |
| `B-setup.png` | Our experiment | One run: fresh Kafka copy, one `.claude` folder, headless session, three records, grade. The two folders side by side. |
| `C-callout-published-hook.png` | Sidebar on the removed rule | The pilot under the published hook: a blocked read followed by a paged read the hook allows. |
| `D-one-question-request-by-request.png` | Results | Storyboard of the broker-lifecycle question: stock reads the file on request 3 of 5; the hook refuses the read and a paged read, the model calls the worker, then greps anyway and answers on request 15. |
| `E-requests-as-bars.png` | Results | The same two runs as bars, one per API request, height is context re-sent; blocked requests and the worker call marked. |
| `F-where-the-money-went.png` | Results | The same two runs in cents, stacked by price bucket, worker call included. Re-sends and output grew with the request count. |
| `G-headline.png` | Results | Three small multiples over 21 tasks and 114 runs: target-file tokens in context, API requests per run, cost per run. |
| `H-by-category.png` | Results | Hook cost relative to stock by task type, paired per task with 95% bootstrap intervals, plus the split by what the model did after the block. |

`post/story_callout.html` and `post/story_main.html` are the storyboard fragments figures C and D are built from:

```
bin/storyboard.py --no-tokens --no-css "results/03-natural-three-arms/R1-shunt:4-6:Spotify's hook, as published" > figures/post/story_callout.html
bin/storyboard.py --no-tokens --no-css "results/05-natural-second-grid/SC1-stock-r1:3:A · stock" \
    "results/05-natural-second-grid/SC1-shunt-strict-r1:3,5-9,15:B · Spotify's hook, enforced" > figures/post/story_main.html
```

`post/build_post.py` assembles the eight figures from these fragments, `summary.json`, the SC1 transcripts, and hand-drawn SVG for A and B (the SVG head and Figure A base live in `post/post-figures-v1-five-arms.html`); it writes `post/post-figures.html`. Then `node post/render.js` (run from `post/`) screenshots each figure to `post_<name>.png`; copy those over `<name>.png` to update the post.

Palette: stock `#0A9385`, hook `#B84E28`, validated with the dataviz skill's checker for light and dark surfaces.
