#!/usr/bin/env python3
"""Emit post-short.html: the blog-length version of the piece, from the same archived grid.

Structure, matching a research paper: What Spotify built > Experiment Design (Why Kafka, Why
We Ran It Through Claude, How It Ran) > Evaluation Design (Why These Tasks, Why These Metrics)
> Results (headline numbers, why cost rises even though less of the file enters context, one
traced example, by task type and why — each finding paired with its explanation in place) >
Discussion (Let Claude Be Claude) > Conclusion (with a takeaways list). Same skeleton as the
long post, each section shorter.

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
TDL = 'style="padding:10px 12px 10px 0; border-bottom:1px solid var(--line); vertical-align:top; font-size:0.9em; color:var(--ink-2);"'
TABLE = '<div style="overflow-x:auto; margin:24px 0;"><table style="width:100%; border-collapse:collapse; font-size:0.92em; line-height:1.5;">'

read_pct = abs((o2['target_read_lines_mean'][1] / o2['target_read_lines_mean'][0] - 1) * 100)
any_pct1 = abs((o1['tgt_tokens_mean'][1] / o1['tgt_tokens_mean'][0] - 1) * 100)
any_pct2 = abs((o2['tgt_tokens_mean'][1] / o2['tgt_tokens_mean'][0] - 1) * 100)
fin1 = (o1['frontier_input_tokens_mean'][1] / o1['frontier_input_tokens_mean'][0] - 1) * 100
fin2 = (o2['frontier_input_tokens_mean'][1] / o2['frontier_input_tokens_mean'][0] - 1) * 100
cost1, cost2 = o1['cost_pct_of_means'], o2['cost_pct_of_means']
ab1, ab2 = o1['after_block'], o2['after_block']
deleg = S2['delegated_tasks']

# ---- three-way token table, minus Spotify's formula (no clean comparable number; stated in prose instead) — rendered as a static figure; see figures/post/table-*.png ----
token_table = '''<figure>
  <img src="figures/post/table-token-comparison.png" alt="Table: three ways to count 90% fewer tokens. Lines of the target read: 450 stock, 232 as shipped (-48%), 59 as described (-87%). Target content reaching the model by any tool: 6,016 stock, 3,721 as shipped (-38%), 2,919 as described (-51%). Input tokens the frontier model was billed for: 229,697 stock, 277,146 as shipped (+21%), 324,523 as described (+41%).">
  <figcaption>Three ways to count what "90% fewer tokens" could mean, means per run across the same 189 sessions.</figcaption>
</figure>'''

# ---- per-category cost table — rendered as a static figure; see figures/post/table-by-category.png ----
cat_table = '''<figure>
  <img src="figures/post/table-by-category.png" alt="Table: cost change by task type, paired per task. Spotify's own four: +25% as shipped, +53% as described, cheaper on 2 and 1 of 4. Needle reads: +3%, +19%, cheaper on 1 and 1 of 4. Spotify's shapes, real sizes: +11%, +24%, cheaper on 2 and 2 of 5. Harm: +0%, +8%, cheaper on 3 and 2 of 5. Controls: +4%, +6%, cheaper on 1 and 1 of 3.">
  <figcaption>Hook cost relative to stock, by category, paired per task.</figcaption>
</figure>'''

body = f'''<main>

<p class="kicker">Field dispatch</p>
<h1>Tokens Are Cheap, Turns Are Not</h1>
<p class="dek">Spotify published a Claude Code plugin that blocks the model from reading big files and hands them to a cheap worker instead, claiming a 90% cut in tokens. I rebuilt it on a real repo and measured the bill. The number they reported is real. The bill went up anyway.</p>
<p class="byline">Twenty-one tasks, three Claude Code setups, 189 offline sessions on one Java monorepo.</p>

<p>I feel like everyone's caught wind of the term <em>tokenomics</em> recently. From customer calls to consultants' LinkedIn posts, people are becoming more and more aware of AI spend and looking for a better way to quantify it. You can't price it for teams as a simple price per question. Instead, we need to think about question complexity and model power. Teams are measuring that complexity by the tokens needed. Makes sense.</p>

<p>That's led a lot of cost-wary teams to start building their own token optimizers. Seeing the trend take off, I wanted to dig into one of these examples myself. Last week, Spotify published a blog post that bounced around Hacker News and Reddit about a Claude Code plugin claiming a 90% cut in tokens. So in this piece, I'm taking you with me as we rebuild it and look under the hood.</p>

<blockquote class="tldr">TLDR; the token reduction Spotify reported is real on the metric they used: with their hook enforced, Claude read {read_pct:.0f}% fewer lines of the big files. The tokens the frontier model was actually billed for went up {fin2:.0f}%, and the dollar cost went up {cost1:.0f}% with the plugin as they shipped it and {cost2:.0f}% with the hook doing what their post describes, at the same pass rate. Whether a given task came out cheaper was decided by the task, not by the plugin, and the reason isn't the greps or the worker — it's how Claude Code's own prompt caching prices a turn. A line count can't see any of that.</blockquote>

<h2>What Spotify built, and why</h2>

<p><b>The why:</b> the Spotify team noticed a trend in their Claude Code usage. A huge share of the tokens Claude Code used went toward tasks that didn't need the frontier-level reasoning power of high-powered LLMs.</p>

<p>For their use case, Spotify works on a large monorepo. In that repo, most of their questions or work end up falling into:</p>

<ul>
<li><b>Bulk file reads</b>: loading 700-plus-line files into context just to check a pattern or answer a question about a fraction of it.</li>
<li><b>Templated code generation</b>: writing boilerplate, configs, or scaffolding, where the structure is already known.</li>
</ul>

<p>Because Claude Code resends the whole conversation on every request, any large file that's entered into context once stays there and keeps getting rebilled on every turn after it. Spotify didn't want to keep paying frontier prices to carry around the parts of a file nobody asked about.</p>

<p><b>The what:</b> to fix this, Spotify implemented a more deterministic workflow for these task types. This deterministic workflow sends these requests to a smaller model to process and return key insights to Claude as context. They chose the Gemini 2.5 Flash model for this implementation, which takes the large file input, reads the files, and returns key context for Claude Code to read. They published it as a plugin called <em>shunt</em>, in their <a href="https://github.com/spotify/portal-ai-plugins/tree/b5ed620c6850f1ea7327b7cd9d0696aae0bf2d89/plugins/shunt">portal-ai-plugins</a> repository.</p>

<figure>
  <img src="figures/post/A-hook-in-the-loop.png" alt="Two straight pipelines. Top, reading a large file: the model calls Read on a file over 350 lines, a PreToolUse hook blocks the call, the bulk-reader skill hands the file to AiKA, and only a summary re-enters the model's context. Bottom, generating templated code: no hook is involved — the model recognizes a boilerplate task on its own, the code-writer skill hands a spec and reference file to AiKA, and only a line-count confirmation re-enters context, since the generated code is written straight to the target file.">
  <figcaption>Figure A · shunt's two delegation paths, at a glance</figcaption>
</figure>

<p>This is built with two Claude Code primitives working together:</p>

<ul>
<li><b>Skills</b> load instructions into context only when a task calls for them.</li>
<li><b>Hooks</b> are a checkpoint in front of a tool call, able to block or redirect it before the model ever sees the result.</li>
</ul>

<p>Spotify built two skills, bulk-reader and code-writer, disclosed when a request matches one of the two workflows above — really just instructions for how to hand a task off to the cheaper model and what to do with what comes back. The hook is what's supposed to force the choice: a <code>PreToolUse</code> hook checks a <code>Read</code> call's file against the 350-line threshold, and if it's over, blocks the call outright and points the model to bulk-reader instead of the raw file. A skill only helps if the model opens it. The hook is the enforcer layer that's meant to make sure it has to.</p>

<p>The assumption everything rests on: when the model is refused a read, it does what the hook's message tells it to. Nothing about a <code>PreToolUse</code> hook enforces that — it can stop one tool call, but it has no say over what the model tries next.</p>

<blockquote class="tldr">TLDR; the skill is the manual. The hook is supposed to force the model to open it. Whether that actually holds is the seam this whole piece pulls on.</blockquote>

<p>The assumption they're making is that fewer tokens sent to the expensive model reads as a proportionally smaller bill. That equivalence, a token avoided is a dollar saved, is exactly what the rest of this post tests.</p>

<h2>Our Experiment: Building a Framework to Copy Theirs</h2>

<p>Does cutting tokens actually cut cost? That became the thesis of this evaluation. But as I began experimenting, I knew I wanted a holistic evaluation of the workflow the team had developed. I believe that all AI workflows, whether predictive, generative, or agentic, need to fit into the same evaluation triangle.</p>

<figure>
  <p style="border:1px dashed #999; padding:10px; color:#666; font-style:italic;">[Figure: the evaluation triangle — performance, latency, and cost. Pending design.]</p>
  <figcaption>The evaluation triangle</figcaption>
</figure>

<p>Getting a fair read on all three meant reproducing Spotify's setup as closely as an outsider reading a blog post can: their kind of repo, their hook, their two workflows, run against the plain baseline they're implicitly comparing themselves to.</p>

<h2>Experiment Design</h2>

<p>Every task ran under three setups, each one step from the last. <em>Stock</em> is Claude Code with nothing added. <em>As shipped</em> is stock plus Spotify's plugin exactly as published, offset/limit exception included. <em>As described</em> is the same plugin with that one exception removed, so the hook actually does what their post says it does. Both hook setups substitute a one-turn Haiku call for Spotify's hosted Gemini model, since I don't have access to their internal Portal system — the same substitute in both, so it's never what explains a difference between them.</p>

<h3>Why Kafka</h3>

<p>Spotify's code is private, so this needs a public repo that looks like theirs in the one way the hook cares about: lots of files over 350 lines, in a language their benchmark used. (There's a second, less obvious constraint: stock Claude Code already refuses to read very large files and pages anything over about 25,000 tokens on its own, so the target files have to sit between Spotify's 350-line threshold and Claude Code's own gates, or the hook never gets the chance to fire first.)</p>

<p>Backstage, Spotify's own open-source project, was the obvious first pick and lost: only 7.5% of its files clear 350 lines, holding 38% of its code. Apache Kafka has 17% of its files over that line, holding 64% of the code. The corpus is the Kafka trunk, pinned to one commit, in Java and Scala.</p>

<figure>
  <img src="figures/post/table-kafka-vs-backstage.png" alt="Table: files over 350 lines, Kafka 1,096 of 6,448 (17%) versus Backstage 549 of 7,348 (7.5%); share of code in those files, Kafka 64% versus Backstage 38%.">
  <figcaption>Why Kafka was used as the corpus instead of Spotify's own open-source Backstage.</figcaption>
</figure>

<p>One honest limit: Kafka is a repo the model has seen in training, and Spotify's code is not. So every session in the final grid runs offline and sandboxed — no web tools, no network commands, no reading anything outside the checkout, a private empty <code>/tmp</code> per session, and a system-prompt line telling the model to answer from the repository, not memory. This constraint, Claude Code cut off from the internet, was applied to all three setups.</p>

<h3>Why We Ran It Through Claude</h3>

<p>One interesting thing I found in their codebase: Spotify's own benchmark never sends a single request through Claude Code. The eval is done explicitly on token count — the original file's token count compared against the summarized Gemini output.</p>

<p>To more thoroughly test the plugin, this evaluation runs through an actual Claude Code session. Every task runs the whole way through: one live, headless <code>claude -p</code> session per task per setup — the real Claude Code model, on the real repo, making its own tool calls, hitting the real hook, and choosing its own next move after a block. That's how this actually tests whether the model opens the skill, deals with the block, loads tokens into context, and drives the resulting cost.</p>

<h3>How It Ran</h3>

<p>So now we have Kafka, and we know we want to run it through Claude — I'm not going to sit there and prompt my Claude Code UI by hand. Nothing here is interactive: the harness unpacks a fresh, historyless Kafka checkout, drops in one setup's <code>.claude</code> folder — Spotify's plugin lives there as a project config, not a plugin install — and calls Claude Code once in headless mode with the task's question as the argument. This is the actual command, the same for all three setups:</p>

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

<p>The cache-TTL pin makes sure every setup pays the same rate for writing a file to the prompt cache, so the comparison can't be skewed by Claude Code silently switching billing tiers mid-run — that turns out to matter a lot in Discussion, below.</p>

<ul>
<li><code>--model</code> pins every setup to the same Sonnet 5 baseline, so no comparison is skewed by which model is running.</li>
<li><code>--settings</code> loads the offline sandbox.</li>
<li><code>unshare</code> gives the session its own empty <code>/tmp</code> so nothing it writes can be found by a later run.</li>
</ul>

<p>When it exits, the harness collects the billed cost and token usage, the full transcript, and the OpenTelemetry trace, diffs the workspace against the starting commit, grades the answer, and deletes the workspace. The next run starts clean.</p>

<h2>Evaluation Design</h2>

<h3>Why These Tasks</h3>

<p>As a non-Kafka expert, I'll admit I cheated a little and used Claude to think through which synthetic workflows or examples would make the most sense. I focused on five key workflow categories that I felt represented what Spotify explicitly named, in their blog, as workflows and future ideas. For each category, I wrote a handful of tasks, a small but early representative sample:</p>

<ul>
<li><b>Spotify's own benchmark (4 tasks).</b> Their four rows, rebuilt on Kafka at the same shapes and file sizes — so the comparison is theirs first.</li>
<li><b>Needle reads (4 tasks).</b> One fact buried in a file of 1,000 to 1,900 lines. This is the case Spotify's own motivation describes — read 700 lines to check one thing — and the case their benchmark never tests.</li>
<li><b>Their shapes at real file sizes (5 tasks).</b> The same question shapes as their four rows, but on files big enough to actually trip the 350-line threshold, which two of theirs never do.</li>
<li><b>Harm (5 tasks).</b> Precise edits and debugging — the two task types Spotify's own post says the approach isn't for. The hook only sees a line count, so it fires on these anyway; worth testing whether that comes at a cost.</li>
<li><b>Controls (3 tasks).</b> The same shapes on small files, where the hook can't fire at all, to measure what the plugin costs just by being installed.</li>
</ul>

<p>I ran three repetitions of every task, interleaved by setup so time of day never lines up with one setup by coincidence: 189 sessions, about $30 at list price.</p>

<h3>Why These Metrics</h3>

<p>Spotify's own evaluation was driven by a single metric: tokens avoided. I kept that metric to check their findings against my own, but it's not robust enough on its own to answer what this piece is actually asking: it never checks whether the answer was even correct, it says nothing about how many turns it took to get there, and it bakes in the exact assumption under test — that a token avoided is a dollar saved — instead of checking it. So I added three more dimensions from the evaluation triangle above, to get the fuller picture:</p>

<ul>
<li><b>Performance</b> — whether the task actually got done, since a cheaper answer isn't worth much if it's missing the point. Measured two ways: was the answer correct, and separately, was the right file even found — a correct answer that never touched the file is flagged as lucky, not counted as evidence the setup worked.</li>
<li><b>Cost</b> — what the headless Claude Code session actually cost, recomputed turn by turn from the transcript at list price and checked against what Claude Code itself billed. The headline number is paired per task: each task's own before-and-after difference, then the mean of those differences with an interval, not one pooled average across twenty-one very different questions.</li>
<li><b>Latency</b> — in agent work this tends to track cost almost 1:1, but it's worth measuring on its own for what it actually feels like to the person waiting on it. Wall clock, turns per run, per-turn duration, from OpenTelemetry.</li>
<li><b>Behavior</b> — the piece Spotify's own evals never produce, because nothing in their harness runs long enough to have a "next call" at all: what the model's very next call was after each block, and whether that call was the worker, a grep, or a paged read.</li>
</ul>

<p>Behavior earned its place the hard way. After the first pass at this grid, I realized Spotify's hook as published wasn't actually blocking — the offset/limit exception let the model page around it and get the whole file anyway. So I built a third setup, with that exception removed, to actually test the workflow enforced the way their post describes.</p>

<p>Every earlier pass at this grid also taught me a smaller control I was missing: the strict block message can't hint at the fallback ("use grep for exact lines") or it isn't measuring the model's own choice anymore — it's measuring an instruction I wrote. The final message is Spotify's, word for word, minus only the sentence about the loophole in the setup that closes it.</p>

<h2>Two things worth knowing before the numbers</h2>

<p>Tokens, you already know. Two other mechanics decide most of what follows.</p>

<ul>
<li><b>No memory between turns.</b> The model remembers nothing on its own — not here, not in ChatGPT, not anywhere; no model works that way. Every time Claude Code asks it anything, it rebuilds the entire conversation so far — every earlier message, every file it's read, every tool result — and sends the whole thing again, fresh. A session feels continuous because Claude Code is doing that reconstruction, every turn, not because the model remembers.</li>
<li><b>Prompt caching.</b> A discount, not a memory upgrade. Content already sent to the model in the last few minutes is billed at a tenth of the normal price on resend instead of full price. It changes what resending costs, not whether resending happens.</li>
</ul>

<h2>Results</h2>

<p>Across all 189 sessions, Spotify's own metric holds up: with the hook enforced, Claude read {read_pct:.0f}% fewer lines of the big files. That didn't translate to cost savings — the hook cost more than stock, not less.</p>

<h3>Why an extra turn costs money even when it works</h3>

<p>Every turn bills for two different things, priced very differently. Resending the conversation so far is cheap — read straight from cache, at a tenth the price of a normal token. The model's fresh thinking that turn is not cached, and costs about fifty times more. A hook can only block one read at a time — it has no way to know how many extra turns, each with its own expensive round of thinking, it'll take to get the same answer a different way. Refusing a read doesn't remove that cost. It just spreads it across more turns.</p>

<p>One small example: find which states a record accumulator's ready-check moves through, in an 1,100-line file. <b>Stock</b> takes three turns and costs 4.5 cents: one grep, one Read, one answer.</p>

<p><b>The hook-enforced setup</b> takes six turns and costs 6.8 cents — 50% more. It tries a blocked <code>Read</code>, then another blocked <code>Read</code> at a different offset, then three separate greps to find the same fact by search. Both setups land on the same correct answer; nothing here was wasted, every tool call was reasonable. The extra turns are simply the price of finding it without ever reading the whole file.</p>

<h3>The headline numbers</h3>

<figure>
  <img src="figures/post/G-headline.png" alt="Three small-multiple bar charts, stock against the hook as shipped and as described, means per run: target-file tokens in context {o1['tgt_tokens_mean'][0]:,.0f}, {o1['tgt_tokens_mean'][1]:,.0f}, {o2['tgt_tokens_mean'][1]:,.0f}; API requests {o1['requests_mean'][0]:.1f}, {o1['requests_mean'][1]:.1f}, {o2['requests_mean'][1]:.1f}; cost ${o1['cost_mean'][0]:.3f}, ${o1['cost_mean'][1]:.3f}, ${o2['cost_mean'][1]:.3f}.">
  <figcaption>Figure G · twenty-one tasks, three runs each</figcaption>
</figure>

<p><b>Performance</b> is unchanged: {o1['pass_rate'][0]*100:.0f}% of stock runs passed, {o1['pass_rate'][1]*100:.0f}% as shipped, {o2['pass_rate'][1]*100:.0f}% as described — three failures in 189, one of them a checklist grader on a code-generation control, not the hook. <b>Cost</b> rose {cost1:.0f}% as shipped and {cost2:.0f}% as described, worker included; paired per task, the enforced hook's own 95% interval is {ci(o2)}, which doesn't cross zero. <b>Latency</b> rose with it: {o1['requests_mean'][0]:.1f} turns a run for stock, {o1['requests_mean'][1]:.1f} as shipped, {o2['requests_mean'][1]:.1f} as described; wall time from {o1['wall_mean'][0]:.0f} seconds to {o2['wall_mean'][1]:.0f}. And on <b>behavior</b>: given a neutral refusal and a skill it's never opened before, the model delegated to the worker on {o2['worker_calls']} of {o2['blocks']} blocks — about one in twenty — and grepped or ran a shell search around the rest, the same pattern as the needle example above.</p>

<h3>Same mechanism, a bigger question</h3>

<p>Traced through the actual OpenTelemetry data this time: <em>how does the broker lifecycle manager move between states?</em>, from a 770-line file. Every answer below is correct — the enforced setup is working exactly as intended, and it's still the most expensive of the three.</p>

<figure>
  <img src="figures/post/F-where-the-money-went.png" alt="Stacked bar chart in cents for the three runs on the broker-lifecycle question: stock about 10 cents in 3 requests, as shipped about 17 cents in 9, as described about 15 cents in 9 including the worker. The bucket that grows in both hook runs is the re-sent conversation, not the file itself.">
  <figcaption>Figure F · where the money actually went, same question, from the OpenTelemetry trace</figcaption>
</figure>

<p>The file-write bucket — two cents everywhere — barely moves. What grows is the resent-conversation bucket: three requests for stock, nine for both hook setups.</p>

<h3>What "90% fewer tokens" actually means</h3>

<p>Depending on how you count it, "90% fewer tokens" is right, half right, or backwards. Spotify's own formula can't be computed for most of this grid — it needs the worker called, which happened on 0 shipped runs and only {o2['runs_with_worker']} of 63 described. Three counts can be computed for every run:</p>

{token_table}

<p>Count lines pulled in through <code>Read</code>, and the claim holds: down {read_pct:.0f}%. Widen that to tokens — Read content plus whatever <code>Grep</code> or <code>Bash</code> separately turned up — and it's a smaller {any_pct2:.0f}% down, because a block that stops one Read doesn't stop the greps that follow it. Count what the frontier model is actually billed for — the number on the invoice — and it goes the other way: up {fin1:.0f}% as shipped, {fin2:.0f}% as described. That last number is the one that matters.</p>

<h3>By task type, and why</h3>

<figure>
  <img src="figures/post/H-by-category.png" alt="Horizontal bars of hook cost relative to stock by task type with 95% intervals, two bars per row for as shipped and as described: Spotify's four tasks {pct(c1['SB']['cost_pct_paired_mean'])} and {pct(c2['SB']['cost_pct_paired_mean'])}; needle reads, harm tasks and controls near zero; Spotify's shapes on big files positive; as described where the worker was called {pct(deleg['cost_pct_paired_mean'])}.">
  <figcaption>Figure H · cost change by task type, paired per task</figcaption>
</figure>

{cat_table}

<p>On 12 of the 21 tasks, all three repetitions land on the same side of stock — the shape of the question explains it. A small slice of a big file (how three classes relate, which methods lack tests) is cheaper with the hook every time: a targeted grep does the job a whole-file read would have. Most of the file (every config key, a generated class, a precise edit) costs more every time, because the content has to come in one way or another and the block just adds turns to get there. That's exactly where Spotify's own four benchmark tasks land — enumerate-the-whole-file questions by construction, so the block fires most and pays off least. A line-count threshold can't tell "which of these" from "all of these" apart, and that distinction, not file size, is what predicts whether a block pays off.</p>

<h2>Discussion</h2>

<h3>Let Claude Be Claude</h3>

<p>There's a broader case here, and it's not really about shunt specifically. Prompt caching — the mechanism doing the damage above — is a relatively recent, platform-level pricing choice, not something any plugin author built around. And in this test's own stock arm, with no hook at all, the model already defaulted to grepping instead of reading the whole file on most needle and harm tasks. That's not something I configured — it's what Sonnet 5 already does inside Claude Code, for free.</p>

<p>Both are the harness getting cheaper on its own schedule, independent of any plugin. A hook keyed to a static proxy — file length — is betting against a moving target: every time the platform gets better at exactly what the hook is trying to force, the stock baseline it's compared to improves for free, and the hook's case gets weaker. Token count was never a perfect stand-in for dollar cost, and it's a worse one with every release. The more durable move, if the goal is spend, is to let Claude be Claude — trust the platform's own defaults, and look for savings in the shape of your questions, not in a rule that assumes today's defaults are the ceiling.</p>

<h2>Conclusion</h2>

<p>Spotify's number is real, and it's the wrong number. "File size avoided, divided by four" measures exactly how many tokens a whole-file read would have cost, and once the hook actually enforces the block, it delivers most of that. What it never measures is the response to the block — a refusal is an instruction, not a delegation, and in this test the instruction was followed about one time in twenty. The other nineteen times, the model found its own way back to the same information — correctly, almost every time — and paid the caching-priced cost of extra turns to do it.</p>

<p>The honest limit on all of this: every run here is a single headless task, done in under a minute. Spotify's case is strongest in a long interactive session, where a big file sitting in context gets resent turn after turn for an hour, sometimes at a full cache rewrite — I didn't test that regime, and it's the one place their number and mine could both be right. But the general point survives it: a token avoided isn't automatically a dollar saved, a turn is the unit the invoice actually counts, and no hook that only watches the tool call in front of it — while the harness underneath it keeps getting better on its own — can tell the difference.</p>

<p>The five things worth remembering:</p>

<ul>
<li><b>The token metric is real, on its own terms.</b> With the hook enforced, Claude read {read_pct:.0f}% fewer lines of the big files — Spotify's own measure holds exactly as they defined it.</li>
<li><b>The bill went up anyway — even on runs that got the exact right answer.</b> {cost1:.0f}% as shipped, {cost2:.0f}% as described. An extra turn costs the same whether it ends in success or a dead end, and Claude Code's own caching prices the resent conversation, not the file — a block just adds turns.</li>
<li><b>Whether a task got cheaper depended on the question, not the plugin.</b> Narrow, targeted questions got cheaper on every run; enumerate-the-whole-file questions got more expensive on every run.</li>
<li><b>The model followed the redirect about one time in twenty.</b> A hook can block a read; it has no say over what the model tries next.</li>
<li><b>If the goal is spend, the fix isn't a bigger hook.</b> It's watching what caching and the model's own defaults already do for free, and aiming any rule at the specific question shapes that don't benefit from them.</li>
</ul>

<p>One last thing, since it shipped while this was in progress: Anthropic now ships <code>claude plugin eval</code>, which runs a plugin against a suite of test cases and scores it against a no-plugin baseline — the same basic comparison this whole piece is built on. What it doesn't do, as far as the docs describe it, is this piece's actual angle: break a session down turn by turn and bucket by bucket to explain why a plugin that passes its own tests can still cost more than doing nothing.</p>

<p class="byline" style="margin-top:8px">The full write-up, with the deviations table, the metrics as equations, the validation checklist, and all 189 runs, is at <a href="https://github.com/hmassa14/TurnsNotTokens">github.com/hmassa14/TurnsNotTokens</a>.</p>

</main>
'''
out = HEAD + body
for stale in ('twelve tasks', 'two arms', '114 sessions'):
    assert stale not in out, stale
assert not re.findall(r'\{[a-z_0-9]+\}', out.replace('${{lines}}', '').replace('${HARNESS}', '').replace('${PROMPT}', '')), 'placeholder left'
open(os.path.join(ROOT, 'post-short.html'), 'w').write(out)
print('post-short.html written', len(out), 'chars')
