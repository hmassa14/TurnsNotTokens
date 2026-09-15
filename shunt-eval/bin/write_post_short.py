#!/usr/bin/env python3
"""Emit post-short.html: the blog-length version of the piece, from the same archived grid.

Keeps the research-paper section structure (Our Experiment: Why Kafka, Why These Tasks, Why
These Metrics, How It Ran, Results) but each section is written tighter than the long version —
fewer worked sub-points, one code block instead of three, no full equations block or deviations
table. It is not a different argument, just a shorter pass at the same one.

Usage: python3 bin/write_post_short.py   (writes shunt-eval/post-short.html; CSS head copied from post.html)
Does NOT touch post.html, the long paper-style version.
"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = os.path.join(ROOT, 'results', '06-natural-clean-grid')
S1 = json.load(open(os.path.join(A, 'summary-shipped.json')))
S2 = json.load(open(os.path.join(A, 'summary-enforced.json')))
o1, o2 = S1['overall'], S2['overall']
c1, c2 = S1['by_category'], S2['by_category']
long_post = open(os.path.join(ROOT, 'post.html')).read()
HEAD = long_post[:long_post.index('<main>')]

def pct(v): return f"{v:+.0f}%"
def d(a, b): return f"{(b / a - 1) * 100:+.0f}%"
def ci(g): lo, hi = g['cost_pct_paired_ci']; return f"{pct(lo)} to {pct(hi)}"
PRE = '<pre class="code">'
TH = 'style="text-align:left; padding:6px 12px 10px 0; border-bottom:2px solid var(--line); color:var(--ink-3); font-family:\'IBM Plex Mono\',monospace; font-size:0.72rem; letter-spacing:0.05em; text-transform:uppercase;"'
THR = TH.replace('text-align:left; padding:6px 12px 10px 0', 'text-align:right; padding:6px 0 10px 12px')
TD = 'style="padding:10px 12px 10px 0; border-bottom:1px solid var(--line); vertical-align:top;"'
TDR = 'style="padding:10px 0 10px 12px; border-bottom:1px solid var(--line); vertical-align:top; text-align:right; font-family:\'IBM Plex Mono\',monospace; font-size:0.9em; white-space:nowrap;"'
TABLE = '<div style="overflow-x:auto; margin:24px 0;"><table style="width:100%; border-collapse:collapse; font-size:0.92em; line-height:1.5;">'

read_pct = abs((o2['target_read_lines_mean'][1] / o2['target_read_lines_mean'][0] - 1) * 100)
any_pct2 = abs((o2['tgt_tokens_mean'][1] / o2['tgt_tokens_mean'][0] - 1) * 100)
fin1 = (o1['frontier_input_tokens_mean'][1] / o1['frontier_input_tokens_mean'][0] - 1) * 100
fin2 = (o2['frontier_input_tokens_mean'][1] / o2['frontier_input_tokens_mean'][0] - 1) * 100
cost1, cost2 = o1['cost_pct_of_means'], o2['cost_pct_of_means']
ab1, ab2 = o1['after_block'], o2['after_block']
deleg = S2['delegated_tasks']

body = f'''<main>

<p class="kicker">Field dispatch</p>
<h1>Tokens Are Cheap, Turns Are Not</h1>
<p class="dek">Spotify published a Claude Code plugin that blocks the model from reading big files and hands them to a cheap worker instead, claiming a 90% cut in tokens. I rebuilt it on a real repo and measured the bill. The number they reported is real. The bill went up anyway.</p>
<p class="byline">Twenty-one tasks, three Claude Code setups, 189 offline sessions on one Java monorepo.</p>

<p>I feel like everyone's caught wind of the term <em>tokenomics</em> recently. From customer calls to consultants' LinkedIn posts, people are getting more and more cognizant of AI spend and looking for a better way to quantify it. It can't just be priced per question, flat — we have to think about question complexity and model power together, and lately, teams have started measuring that complexity in tokens needed. Makes sense.</p>

<p>That's led a lot of cost-wary teams to start building their own token optimizers. Seeing the trend take off, I wanted to dig into one of these examples myself. Last week, Spotify published a blog post that bounced around Hacker News and Reddit, about a Claude Code plugin claiming a 90% cut in tokens. So in this piece, I'm taking you with me as we rebuild it and look under the hood.</p>

<blockquote class="tldr">TLDR; the token reduction Spotify reported is real on the metric they used: with their hook enforced, Claude read {read_pct:.0f}% fewer lines of the big files. The tokens the frontier model was actually billed for went up {fin2:.0f}%, and the dollar cost went up {cost1:.0f}% with the plugin as they shipped it and {cost2:.0f}% with the hook doing what their post describes, at the same pass rate. Whether a given task came out cheaper was decided by the task, not by the plugin: when the answer is a slice of a big file, blocking the read saves money; when the answer is most of the file, it costs money. A line count can't tell those apart.</blockquote>

<h2>What Spotify built, and why</h2>

<p><b>The why:</b> the Spotify team noticed a trend in their own Claude Code usage — a huge share of the tokens they were burning went toward tasks that didn't actually need the frontier-level reasoning power they were paying for. Spotify works out of one large monorepo, and most of that non-reasoning work fell into two buckets: <b>bulk file reads</b>, loading a 700-plus-line file into context just to check a pattern or answer a question about a fraction of it, and <b>templated code generation</b>, writing boilerplate where the structure is already known. Because Claude Code resends the whole conversation on every request, any large file that's entered context once stays there and keeps getting rebilled on every turn after it. Spotify didn't want to keep paying frontier prices to carry around the parts of a file nobody asked about.</p>

<p><b>The what:</b> to fix it, they built a <em>PreToolUse hook</em> — a checkpoint that runs before Claude Code lets a <code>Read</code> call through. Over 350 lines, it blocks the call and points the model at a <em>skill</em>, a set of instructions for handing the file to a cheap worker model instead and getting back only a summary. They picked a Gemini model for the worker (other coverage names Gemini 2.5 Flash), published the plugin as <em>shunt</em>, and called it a 90% cut in tokens.</p>

<figure>
  <img src="figures/post/A-hook-in-the-loop.png" alt="Diagram: the model calls Read, a PreToolUse hook checks the line count, and either allows the read or blocks it and returns a message. After a block, the model can call the worker script, page through the file with an offset, or grep it. As shipped it paged through on {ab1.get('Read(paged)',0)} of {o1['blocks']} blocks and never called the worker; with the paging closed it called the worker on {ab2.get('Skill',0)} of {o2['blocks']} blocks and grepped on {ab2.get('Grep',0)+ab2.get('Bash',0)}.">
  <figcaption>Figure A · where the hook sits, and the three ways out</figcaption>
</figure>

<p>Here's the assumption everything rests on: when the model is refused a read, it does what the hook's message tells it to. Nothing about a <code>PreToolUse</code> hook enforces that — it can stop one tool call, but it has no say over what the model tries next. Spotify's own evals never actually test this. They carry two suites, and neither one runs Claude Code: one is a unit test of the hook's line-count arithmetic, and the other times a deterministic script call (file size in characters, divided by four, minus the summary's size) and calls the difference tokens saved, worker cost never included. Both are true and neither is in dispute. What's missing is the one step that isn't deterministic — what the model does with itself once it's told no. I wanted to find out, on a real repo, doing real work.</p>

<blockquote class="tldr">TLDR; Spotify checked the hook's math and timed a script. Neither test ever put a model on the other side of the block to see what it would actually do.</blockquote>

<h2>Our Experiment</h2>

<p>Every task ran under three setups, each one change from the last: <em>stock</em> Claude Code, nothing added; <em>as shipped</em>, stock plus Spotify's plugin exactly as published, including a rule that lets a <code>Read</code> with an offset through even on a big file; and <em>as described</em>, the same plugin with that one rule removed, so the hook actually does what their post says it does. The worker behind both hook setups is the same substitute — a one-turn call to Haiku instead of Spotify's hosted Gemini model, since I don't have access to their internal Portal system — so it's never what explains a difference between the two hook setups.</p>

<h3>Why Kafka</h3>

<p>Spotify's code is private, so this needs a public repo that looks like theirs in the one way the hook cares about: lots of files over 350 lines, in a language their benchmark used. There's a second, less obvious constraint. Stock Claude Code already refuses to read very large files and pages anything over about 25,000 tokens on its own, so the target files have to sit in the band between Spotify's 350-line threshold and Claude Code's own gates, or the hook never gets the chance to fire first.</p>

<p>Backstage, Spotify's own open-source project, was the obvious first pick and lost: only 7.5% of its files clear 350 lines, holding 38% of its code. Apache Kafka has 17% of its files over that line, holding 64% of the code — the hook has real work to do on most of what a developer would touch. Kafka trunk, pinned at one commit, Java and Scala, is the corpus.</p>

{TABLE}
<thead><tr><th {TH}></th><th {THR}>Kafka, used</th><th {THR}>Backstage, rejected</th></tr></thead>
<tbody>
<tr><td {TD}>Files over 350 lines</td><td {TDR}>1,096 of 6,448 (17%)</td><td {TDR}>549 of 7,348 (7.5%)</td></tr>
<tr><td {TD.replace('border-bottom:1px solid var(--line);','')}>Share of code in those files</td><td {TDR.replace('border-bottom:1px solid var(--line);','')}>64%</td><td {TDR.replace('border-bottom:1px solid var(--line);','')}>38%</td></tr>
</tbody></table></div>

<p>One honest limit: Kafka is a repo the model has seen in training, and Spotify's code is not. So every session in the final grid runs offline and sandboxed — no web tools, no network commands, no reading anything outside the checkout, a private empty <code>/tmp</code> per session, and a system-prompt line telling the model to answer from the repository, not memory. That constraint applies to all three setups equally, stock included, so the baseline is "Claude Code as installed, cut off from the internet," which is the honest baseline for a private codebase. Every one of the 189 runs actually touched its target file before answering; nobody got the right answer from memory.</p>

<h3>Why These Tasks</h3>

<p>Twenty-one questions, five named categories, each asked the way a developer would with no file path given, so the session has to find the file before it can read it:</p>

<ul>
<li><b>Spotify's own benchmark (4 tasks).</b> Their four rows, rebuilt on Kafka at the same shapes and file sizes — so the comparison is theirs first.</li>
<li><b>Needle reads (4 tasks).</b> One fact buried in a file of 1,000 to 1,900 lines. This is the case Spotify's own motivation describes — read 700 lines to check one thing — and the case their benchmark never tests.</li>
<li><b>Their shapes at real file sizes (5 tasks).</b> The same question shapes as their four rows, but on files big enough to actually trip the 350-line threshold, which two of theirs never do.</li>
<li><b>Harm (5 tasks).</b> Precise edits and debugging — the two task types Spotify's own post says the approach isn't for. The hook only sees a line count, so it fires on these anyway.</li>
<li><b>Controls (3 tasks).</b> The same shapes on small files, where the hook can't fire at all, to measure what the plugin costs just by being installed.</li>
</ul>

<p>Three repetitions of every task, interleaved by setup so time of day never lines up with one setup by coincidence: 189 sessions, about $30 at list price.</p>

<h3>Why These Metrics</h3>

<p>Spotify's benchmark needed two numbers: corpus size, summary size. A Claude Code session is a sequence of turns the model chooses to make, so this test measures four things per run instead, each summed per turn and kept separate for the main model and the worker:</p>

<ul>
<li><b>Performance</b> — pass at the grader's threshold, and separately, whether the target file was actually read, grepped, or delegated at all. A right answer that never touched the file is flagged as lucky, not counted as evidence the setup worked.</li>
<li><b>Cost</b> — every run's cost recomputed turn by turn from the transcript at list price and checked against what Claude Code itself billed. The headline number is paired per task: each task's own before-and-after difference, then the mean of those differences with an interval, not one pooled average across twenty-one very different questions.</li>
<li><b>Latency</b> — wall clock, turns per run, per-turn duration from OpenTelemetry.</li>
<li><b>Behavior</b> — blocks, what the model's very next call was after each one, and whether that call was the worker, a paged read, or a grep. This is the number Spotify's own evals never produced.</li>
</ul>

<p>Every earlier pass at this grid taught me a control I was missing. The most important one: the strict block message can't hint at the fallback ("use grep for exact lines") or it isn't measuring the model's own choice anymore — it's measuring an instruction I wrote. The final message is Spotify's, word for word, minus only the sentence about the loophole in the setup that closes it.</p>

<h3>How It Ran</h3>

<p>Nothing here is interactive. The harness unpacks a fresh, historyless Kafka checkout, drops in one setup's <code>.claude</code> folder — Spotify's plugin lives there as a project config, not a plugin install — and calls Claude Code once in headless mode with the task's question as the argument. This is the actual command, the same for all three setups:</p>

{PRE}CLAUDE_CODE_ENABLE_TELEMETRY=1 \\
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318 \\
CLAUDE_CODE_PROMPT_CACHE_TTL=5m CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL=5m \\
unshare -m bash -c 'mount -t tmpfs none /tmp && exec "$@"' _ \\
claude -p "$PROMPT" \\
  --model claude-sonnet-5 \\
  --permission-mode acceptEdits \\
  --settings "$HARNESS/settings.json" \\
  --append-system-prompt "Answer from the repository checked out in the \\
working directory. Do not rely on memory of the upstream project or on \\
the internet." \\
  --max-turns 40 \\
  --output-format json</pre>

<p>The cache-TTL pin makes sure every setup pays the same rate for writing a file to the prompt cache, so the comparison can't be skewed by Claude Code silently switching billing tiers mid-run. <code>--settings</code> loads the offline sandbox. <code>unshare</code> gives the session its own empty <code>/tmp</code> so nothing it writes can be found by a later run. When it exits, the harness collects the billed cost and token usage, the full transcript, and the OpenTelemetry trace, diffs the workspace against the starting commit, grades the answer, and deletes the workspace. The next run starts clean.</p>

<h2>Results</h2>

<p>Take one real question: <em>how does the broker lifecycle manager move between states?</em> The file is 770 lines. Stock greps for the class, reads it whole, answers — three turns, ten cents. As shipped, the read gets refused, and the model just pages around the block with an offset, which the hook allows; the whole file ends up in context anyway, one turn later. As described, with that loophole closed, the model does what Spotify actually designed: opens the skill, calls the worker, gets a real summary back, checks one thing with a grep, and answers. Nine turns either way, and the enforced version costs more than stock even though it's the version working exactly as intended, because six extra turns of resending the whole conversation cost more than the two cents it would have cost to just read the file once.</p>

<p>That's the whole mechanism, and it holds across the grid. Both hook setups really do cut what Spotify's number describes — with the loophole closed, lines of the big file that Claude actually reads fall {read_pct:.0f}%, and content reaching the model through any tool falls {any_pct2:.0f}%. But the tokens the frontier model is actually billed for go <em>up</em>, {fin1:.0f}% as shipped and {fin2:.0f}% as described, because refusing a read doesn't remove the need to know what's in the file — it just adds turns, and every turn resends everything before it.</p>

<figure>
  <img src="figures/post/G-headline.png" alt="Three small-multiple bar charts, stock against the hook as shipped and as described, means per run: target-file tokens in context {o1['tgt_tokens_mean'][0]:,.0f}, {o1['tgt_tokens_mean'][1]:,.0f}, {o2['tgt_tokens_mean'][1]:,.0f}; API requests {o1['requests_mean'][0]:.1f}, {o1['requests_mean'][1]:.1f}, {o2['requests_mean'][1]:.1f}; cost ${o1['cost_mean'][0]:.3f}, ${o1['cost_mean'][1]:.3f}, ${o2['cost_mean'][1]:.3f}.">
  <figcaption>Figure G · twenty-one tasks, three runs each</figcaption>
</figure>

<p>Cost went up {cost1:.0f}% as shipped and {cost2:.0f}% as described, worker included, at pass rates within three points of stock. And the model barely used the thing Spotify built for it: given a neutral refusal and a skill it's never opened before, it delegated to the worker on about one block in twenty, and grepped its own way around the rest. Where it did delegate, cost still rose {pct(deleg['cost_pct_paired_mean'])} over stock, because the worker is cheap but the four turns it takes to get to it — refused read, refused paged read, skill load, worker call — are not.</p>

<figure>
  <img src="figures/post/H-by-category.png" alt="Horizontal bars of hook cost relative to stock by task type with 95% intervals, two bars per row for as shipped and as described: Spotify's four tasks {pct(c1['SB']['cost_pct_paired_mean'])} and {pct(c2['SB']['cost_pct_paired_mean'])}; needle reads, harm tasks and controls near zero; Spotify's shapes on big files positive; as described where the worker was called {pct(deleg['cost_pct_paired_mean'])}.">
  <figcaption>Figure H · cost change by task type</figcaption>
</figure>

<p>The average hides the actually useful finding, which is that the outcome isn't random — it's decided by the shape of the question. On 12 of the 21 tasks, all three repetitions land on the same side of stock. Where the answer is a small slice of a big file — how three classes relate, which methods lack tests — the block is cheaper every time, because a targeted grep does the job the whole-file read would have. Where the answer is most of the file — list every config key, generate a class from a 616-line reference, make a precise edit — the block costs more every time, because the content has to come in one way or another and the block just adds the turns it takes to get there. A line-count threshold has no way to tell those two cases apart.</p>

<h2>What I'd take from this</h2>

<p>Spotify's number is real, and it's the wrong number. "File size avoided, divided by four" measures exactly how many tokens a whole-file read would have cost — and once the hook actually enforces the block, it delivers most of that. What it never measures is the response to the block, and a refusal is not a delegation. It's an instruction, and in this test, the instruction got followed about one time in twenty. The other nineteen, the model found its own way back to the same information, at the price of asking again.</p>

<p>If I were building this hook, I'd want it to watch the shape of the question rather than the length of the file — let an enumerate-everything question through, and block a which-of-these question toward a summary — because that's the actual line this test found between where delegation pays and where it doesn't. And the honest caveat: every run here is a single headless task, done in under a minute. Spotify's case is strongest in a long interactive session, where a big file sitting in context gets resent turn after turn for an hour, sometimes at a full cache rewrite. I didn't test that regime, and it's the one place their number and mine could both be right.</p>

<p>A token avoided isn't automatically a dollar saved. A turn is the unit the invoice actually counts, and no hook that only watches the tool call in front of it can tell the difference.</p>

<p class="byline" style="margin-top:8px">The full write-up, with the deviations table, the metrics as equations, the validation checklist, and all 189 runs, is at <a href="https://github.com/hmassa14/TurnsNotTokens">github.com/hmassa14/TurnsNotTokens</a>.</p>

</main>
'''
out = HEAD + body
for stale in ('twelve tasks', 'two arms', '114 sessions'):
    assert stale not in out, stale
assert not re.findall(r'\{[a-z_0-9]+\}', out.replace('${{lines}}', '').replace('${HARNESS}', '').replace('${PROMPT}', '')), 'placeholder left'
open(os.path.join(ROOT, 'post-short.html'), 'w').write(out)
print('post-short.html written', len(out), 'chars')
