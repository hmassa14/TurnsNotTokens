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

body = r'''<main>

<p class="kicker">Field dispatch</p>
<h1>Tokens Are Cheap, Turns Are Not</h1>
<p class="dek">Spotify published a Claude Code plugin that blocks the model from reading big files and hands them to a cheap worker instead, claiming a 90% cut in tokens. I rebuilt it on a real repo and measured the bill. The number they reported is real. The bill went up anyway.</p>
<p class="byline">Twenty-one tasks, three Claude Code setups, 189 offline sessions on one Java monorepo.</p>

<p>I feel like everyone has caught wind of the term <em>tokenomics</em> recently. From customer calls to consultants' LinkedIn posts, people are becoming more and more aware of AI spend and looking for a better way to quantify it. You can't price it for teams as a simple price per question. Instead, we need to think about question complexity and model power. Teams are measuring that complexity by the tokens needed. Makes sense.</p>

<p>That's led a lot of cost-wary teams to start building their own token optimizers. Seeing the trend take off, I wanted to dig into one of these examples myself. A few weeks ago, Spotify published a blog post that bounced around Hacker News and Reddit about a Claude Code plugin claiming a 90% cut in tokens. So in this piece, I'm taking you with me as we rebuild it and look under the hood.</p>

<blockquote class="tldr">TLDR; Spotify's number is real: with their hook enforced, Claude read 87% fewer lines of the big files. But the bill went up — 8% with the plugin as they shipped it, 19% with the hook working the way their post describes — at the same pass rate. The culprit isn't the plugin itself. It's how Claude Code prices every extra turn it takes to get an answer.</blockquote>

<h2>What Spotify Built, and Why</h2>

<p><b>The why:</b> The Spotify team noticed a trend in their Claude Code usage. A huge share of the tokens Claude Code used went toward tasks that didn't need the frontier-level reasoning power of high-powered LLMs.</p>

<p>For their use case, Spotify works on a large monorepo. In that repo, most of their questions or work end up falling into:</p>

<ul>
<li><b>Bulk file reads:</b> loading 700-plus-line files into context just to check a pattern or answer a question about a fraction of it.</li>
<li><b>Templated code generation:</b> writing boilerplate, configs, or scaffolding, where the structure is already known.</li>
</ul>

<p>Because Claude Code resends the whole conversation on every request, any large file that's entered into context once stays there and keeps getting rebilled on every turn after it. Spotify didn't want to keep paying frontier prices to carry around the parts of a file nobody asked about.</p>

<p><b>The what:</b> To fix this, Spotify implemented a more deterministic workflow for these task types. This deterministic workflow sends these requests to a smaller model to process and return key insights to Claude as context. They chose Gemini 2.5 Flash as this cheaper <em>worker</em>: it takes the large file, reads it, and hands back the key context for Claude Code. They published it as a plugin called <em>shunt</em>, in their <a href="https://github.com/spotify/portal-ai-plugins/tree/b5ed620c6850f1ea7327b7cd9d0696aae0bf2d89/plugins/shunt">portal-ai-plugins</a> repository.</p>

<figure>
  <img src="figures/post/A-hook-in-the-loop.png" alt="Two straight pipelines. Top, reading a large file: the model calls Read on a file over 350 lines, a PreToolUse hook blocks the call, the bulk-reader skill hands the file to AiKA, and only a summary re-enters the model's context. Bottom, generating templated code: no hook is involved — the model recognizes a boilerplate task on its own, the code-writer skill hands a spec and reference file to AiKA, and only a line-count confirmation re-enters context, since the generated code is written straight to the target file.">
  <figcaption>Figure A · shunt's two delegation paths, at a glance</figcaption>
</figure>

<p>This is built with two Claude Code primitives working together:</p>

<ul>
<li><b>Skills</b> load instructions into context only when a task calls for them.</li>
<li><b>Hooks</b> are a checkpoint in front of a tool call, able to block or redirect it before the model ever sees the result.</li>
</ul>

<p>Spotify built two skills, bulk-reader and code-writer, disclosed when a request matches one of the two workflows above (really just instructions for how to hand a task off to the cheaper model and what to do with what comes back). The hook is what's supposed to force the choice: a <code>PreToolUse</code> hook checks a <code>Read</code> call's file against the 350-line threshold, and if it's over, blocks the call outright and points the model to bulk-reader instead of the raw file. A skill only helps if the model opens it. The hook is the enforcer layer that's meant to make sure it has to.</p>

<p>The assumption they're making is that fewer tokens sent to the expensive model reads as a proportionally smaller bill. That equivalence (a token avoided is a dollar saved) is exactly what the rest of this post tests.</p>

<h2>Our Experiment</h2>

<p>Does cutting tokens actually cut cost? That became the thesis of this evaluation. However, as I began experimenting, I knew I wanted a holistic evaluation of the workflow the team had developed. I believe that all AI workflows (whether predictive, generative, or agentic) need to fit into the evaluation triangle: performance, latency, and cost.</p>

<p>Getting a fair read on all three meant reproducing Spotify's setup as closely as an outsider reading a blog post can: their kind of repo, their hook, their two workflows, run against the plain baseline they're implicitly comparing themselves to.</p>

<h2>Experiment Design</h2>

<p>Every task ran under three setups: <em>stock</em>, Claude Code with nothing added; <em>as shipped</em>, stock plus Spotify's plugin exactly as published; and <em>as described</em>, the same plugin with one loophole closed so the hook actually blocks. Both hook setups use a one-turn Haiku call in place of Spotify's hosted Gemini model, since I don't have access to their internal system.</p>

<h3>Why Kafka</h3>

<p>Spotify's code is private, so this needs a public repo that looks like theirs in the one way the hook cares about: lots of files over 350 lines, in a language their benchmark used. (There's a second, less obvious constraint. Stock Claude Code already refuses to read very large files and pages anything over about 25,000 tokens on its own, so the target files have to sit between Spotify's 350-line threshold and Claude Code's own gates, or the hook never gets the chance to fire first.)</p>

<p>Backstage, Spotify's own open-source project, was the obvious first pick and lost: only 7.5% of its files clear 350 lines, holding 38% of its code. Apache Kafka has 17% of its files over that line, holding 64% of the code. The corpus is the Kafka trunk, pinned to one commit, in Java and Scala.</p>

<figure>
  <img src="figures/post/table-kafka-vs-backstage.png" alt="Table: files over 350 lines, Kafka 1,096 of 6,448 (17%) versus Backstage 549 of 7,348 (7.5%); share of code in those files, Kafka 64% versus Backstage 38%.">
  <figcaption>Why Kafka was used as the corpus instead of Spotify's own open-source Backstage.</figcaption>
</figure>

<p>One honest limit: Kafka is a repo the model has seen in training, and Spotify's code is not. So every session runs offline and sandboxed — no web tools, no network commands, no reading anything outside the checkout, a private empty <code>/tmp</code> per session, and a system-prompt line telling the model to answer from the repository, not memory. That constraint — Claude Code cut off from the internet — was applied to every test.</p>

<h3>Why We Ran It Through Claude</h3>

<p>One interesting thing I found in their codebase: Spotify's own benchmark never sends a single request through Claude Code. The eval compares the original file's token count against the summarized Gemini output.</p>

<p>To test the plugin more thoroughly, this eval runs real Claude Code sessions. Every task runs the whole way through: one live, headless <code>claude -p</code> session per task per setup — the real Claude Code model, on the real repo, making its own tool calls, hitting the real hook, and choosing its own next move after a block. That's how we really test whether the model opens the skills, how it deals with the block, what it loads into context, and what that costs.</p>

<h3>How It Ran</h3>

<p>So now we have Kafka, and we know we want to run it through Claude — but I'm not going to sit and prompt my Claude Code UI by hand. Nothing is interactive. It all runs from a script, with Claude Code in headless mode and the same files, constraints, and setup across every task. This is the actual command, the same for all three setups:</p>

<pre class="code">CLAUDE_CODE_ENABLE_TELEMETRY=1 \
OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4318 \
CLAUDE_CODE_PROMPT_CACHE_TTL=5m CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL=5m \
unshare -m bash -c 'mount -t tmpfs none /tmp && exec "$@"' _ \
claude -p "$PROMPT" \
  --model claude-sonnet-5 \
  --permission-mode acceptEdits \
  --settings "$HARNESS/settings.json" \
  --append-system-prompt "Answer from the repository checked out in the \
working directory. Do not rely on memory of the upstream project or on \
the internet." \
  --max-turns 40 \
  --output-format json</pre>

<p>The cache-TTL pin makes sure every setup pays the same rate for writing a file to the prompt cache, so the comparison can't be skewed by Claude Code silently switching billing tiers mid-run — that turns out to matter a lot in the results below.</p>

<ul>
<li><code>--model</code>: every setup runs on the same baseline Sonnet model.</li>
<li><code>--settings</code>: loads the offline sandbox.</li>
<li><code>unshare</code>: gives the session its own empty <code>/tmp</code> so nothing it writes can be found by a later run.</li>
</ul>

<p>When it exits, the harness collects the billed cost and token usage, the full transcript, and the OpenTelemetry trace, diffs the workspace against the starting commit, grades the answer, and deletes the workspace. The next run starts clean.</p>

<h2>Evaluation Design</h2>

<h3>Why These Tasks</h3>

<p>As a non-Kafka expert, I'll admit I cheated and used Claude to think through which synthetic workflows would make the most sense. I focused on five workflow categories that I felt represented what Spotify explicitly named as workflows and future ideas in their blog, with 3–5 tasks each for a small but early representative sample:</p>

<ul>
<li><b>Spotify's own benchmark (4 tasks).</b> Their four rows, rebuilt on Kafka at the same shapes and file sizes — so the comparison is theirs first.</li>
<li><b>Needle reads (4 tasks).</b> One fact buried in a file of 1,000 to 1,900 lines. This is the case Spotify's own motivation describes — read 700 lines to check one thing — and the case their benchmark never tests.</li>
<li><b>Their shapes at real file sizes (5 tasks).</b> The same question shapes as their four rows, but on files big enough to actually trip the 350-line threshold, which two of theirs never do.</li>
<li><b>Harm (5 tasks).</b> Precise edits and debugging — the two task types Spotify's own post says the approach isn't for. The hook only sees a line count, so it fires on these anyway — worth testing whether that gets costly.</li>
<li><b>Controls (3 tasks).</b> The same shapes on small files, where the hook can't fire at all, to measure what the plugin costs just by being installed.</li>
</ul>

<p>I also ran three repetitions of every task, interleaved by setup so time of day never lines up with one setup by coincidence: 189 sessions, about $30 at list price.</p>

<h3>Why These Metrics</h3>

<p>Spotify's own evaluation was driven by one metric: tokens avoided. I kept it to check their findings against my own, but added the rest of the evaluation triangle, plus one more:</p>

<ul>
<li><b>Performance:</b> did the task actually get done? A cheaper solution isn't great if it misses major pieces of information. Measured by whether the answer was correct and whether the right file was found.</li>
<li><b>Cost:</b> what each headless Claude Code session actually cost, broken down per turn and by what the context was billed as.</li>
<li><b>Latency:</b> in agents, this tends to track cost pretty closely, but I was curious what it feels like for the person waiting. Measured by wall clock, turns per run, and per-turn duration.</li>
<li><b>Behavior:</b> what the model did right after a block. Was the next call the worker, a grep, or a paged read?</li>
</ul>

<p>Behavior earned its place after the first run, when I realized their hook as published wasn't actually blocking. So I built the third setup, which enforces it, to test their workflow the way their post describes.</p>

<h2>Some Things Worth Remembering Before the Results</h2>

<p>Tokens, you already know. Two other mechanics matter for what's coming.</p>

<ul>
<li><b>No memory between turns.</b> The model itself remembers nothing on its own — not here, not in ChatGPT, not anywhere; no model works that way. Every time Claude Code asks it anything, it rebuilds the entire conversation so far — every earlier message, every file it's read, every tool result — and sends the whole thing again, fresh. A session feels continuous because Claude Code reconstructs and resends everything every turn, not because the model remembers.</li>
<li><b>Prompt caching.</b> A discount, not a memory upgrade. If the same content was already sent to the model in the last few minutes, sending it again is billed at a tenth of the normal price instead of full price. It changes what resending costs. It doesn't change whether resending happens — that still happens on every turn, cache or no cache.</li>
</ul>

<p>We'll come back to both in the numbers — they're key to understanding what Claude actually costs.</p>

<h2>Our Results</h2>

<p>Across all 189 sessions, Spotify's own metric holds up: with the hook enforced, Claude read 87% fewer lines of the big files. That didn't translate to cost savings — the hook cost more than stock, not less.</p>

<h3>TLDR; Why an Extra Turn Costs Money Even When It Works</h3>

<p>Every turn bills for two different things, priced very differently. Resending the conversation so far is cheap — read straight from cache, at a tenth the price of a normal token. The model's fresh thinking that turn is not cached, and costs about fifty times more. A hook can only block one read at a time — it has no way to know how many extra turns, each with its own expensive round of thinking, it'll take to get the same answer a different way. Refusing a read doesn't remove that cost. It just spreads it across more turns.</p>

<p>One small example: find which states a record accumulator's ready-check moves through, in an 1,100-line file.</p>

<ul>
<li><b>Stock</b> takes three turns and costs 4.5 cents: one grep, one Read, one answer.</li>
<li><b>The hook-enforced setup</b> takes six turns and costs 6.8 cents — 50% more. It tries a blocked <code>Read</code>, then another blocked <code>Read</code> at a different offset, then three separate greps to find the same fact by search.</li>
</ul>

<p>Both setups land on the same correct answer; nothing here was wasted, every tool call was reasonable. The extra turns are simply the price of finding it without ever reading the whole file.</p>

<h3>The Headline Numbers</h3>

<figure>
  <img src="figures/post/G-headline.png" alt="Three small-multiple bar charts, stock against the hook as shipped and as described, means per run: target-file tokens in context 6,016, 3,721, 2,919; API requests 6.1, 7.7, 9.2; cost $0.121, $0.131, $0.144.">
  <figcaption>Figure G · twenty-one tasks, three runs each</figcaption>
</figure>

<p>Overall, measured against the evaluation triangle, on average:</p>

<ul>
<li><b>Performance</b> is unchanged: 100% of stock runs passed, 98% as shipped, 97% as described — three failures in 189, one of them a checklist grader on a code-generation control, not the hook.</li>
<li><b>Cost</b> rose 8% as shipped and 19% as described, worker included; paired per task, the enforced hook's own 95% interval is +7% to +39%, which doesn't cross zero.</li>
<li><b>Latency</b> rose with it: 6.1 turns a run for stock, 7.7 as shipped, 9.2 as described; wall time from 39 seconds to 51.</li>
<li><b>Behavior</b>: given a neutral refusal and a skill it's never opened before, the model delegated to the worker on 7 of 96 blocks — about one in twenty — and grepped or ran a shell search around the rest.</li>
</ul>

<h3>Same Mechanism, a Bigger Question</h3>

<p>Traced through the actual OpenTelemetry data this time: <em>how does the broker lifecycle manager move between states?</em>, from a 770-line file. Every answer below is correct — the enforced setup is working exactly as intended, and it's still the most expensive of the three.</p>

<figure>
  <img src="figures/post/F-where-the-money-went.png" alt="Stacked bar chart in cents for the three runs on the broker-lifecycle question: stock about 10 cents in 3 requests, as shipped about 17 cents in 9, as described about 15 cents in 9 including the worker. The bucket that grows in both hook runs is the re-sent conversation, not the file itself.">
  <figcaption>Figure F · where the money actually went, same question, from the OpenTelemetry trace</figcaption>
</figure>

<p>The file-write bucket — two cents everywhere — barely moves. The resent-conversation bucket grows: three requests for stock, nine for both hook setups.</p>

<h3>What "90% Fewer Tokens" Actually Means</h3>

<p>Depending on how you count it, "90% fewer tokens" is right, half right, or backward. Spotify's own formula can't be computed for most of this grid — it needs the worker called, which happened on 0 shipped runs and only 5 of 63 described.</p>

<figure>
  <img src="figures/post/table-token-comparison.png" alt="Table: three ways to count 90% fewer tokens. Lines of the target read: 450 stock, 232 as shipped (-48%), 59 as described (-87%). Target content reaching the model by any tool: 6,016 stock, 3,721 as shipped (-38%), 2,919 as described (-51%). Input tokens the frontier model was billed for: 229,697 stock, 277,146 as shipped (+21%), 324,523 as described (+41%).">
  <figcaption>Three ways to count what "90% fewer tokens" could mean, per run across the same 189 sessions.</figcaption>
</figure>

<ul>
<li>Lines pulled in through <code>Read</code>: down 87%.</li>
<li>Tokens reaching the model by any tool — Read plus whatever <code>Grep</code> or <code>Bash</code> separately turned up: down 51%.</li>
<li>Tokens the frontier model was actually billed for — the number on the invoice: up 21% as shipped, 41% as described. That's the one that matters.</li>
</ul>

<h3>By Task Type, and Why</h3>

<p>On 12 of the 21 tasks, all three repetitions land on the same side of stock — the shape of the question explains it.</p>

<ul>
<li>A small slice of a big file (how three classes relate, which methods lack tests): cheaper with the hook every time — a targeted grep does the job a full-file read would.</li>
<li>Most of the file (every config key, a generated class, a precise edit): costs more every time — the content has to come in one way or another, and the block just adds turns to get there.</li>
<li>Spotify's own four benchmark tasks land squarely in the second camp — enumerate-the-whole-file questions by construction, so the block fires most and pays off least.</li>
</ul>

<p>A line-count threshold can't tell "which of these" from "all of these" apart, and that distinction — not file size — predicts whether a block pays off.</p>

<figure>
  <img src="figures/post/table-by-category.png" alt="Table: cost change by task type, paired per task. Spotify's own four: +25% as shipped, +53% as described, cheaper on 2 and 1 of 4. Needle reads: +3%, +19%, cheaper on 1 and 1 of 4. Spotify's shapes, real sizes: +11%, +24%, cheaper on 2 and 2 of 5. Harm: +0%, +8%, cheaper on 3 and 2 of 5. Controls: +4%, +6%, cheaper on 1 and 1 of 3.">
  <figcaption>Hook cost relative to stock, by category, paired per task.</figcaption>
</figure>

<h2>In Conclusion</h2>

<h3>Let Claude Be Claude</h3>

<p>I want to be clear: this wasn't a crazy idea, and knocking Spotify isn't the point of this piece. Token spend is one of the most talked-about problems in AI right now, and Spotify did the rare, useful thing — built a fix, measured it, and published it in the open. That's the only reason a hobby blogger like me could rebuild it at all.</p>

<p>What changed isn't the idea. It's the ground under it. The efficiency shunt was built to force is increasingly showing up in the platform on its own, at three layers:</p>

<ul>
<li><b>In the tokens.</b> Prompt caching makes content you've already sent cost a tenth as much to send again.</li>
<li><b>In the context window.</b> Tools like MCP servers let a model pull just what it needs from a file store instead of loading whole files into context.</li>
<li><b>In the harness.</b> In my own stock runs — no hook, no instruction — Claude already grepped instead of reading the whole file on most needle and harm tasks.</li>
</ul>

<p>Boris Cherny, who leads Claude Code at Anthropic, made this point at YC Startup School, in conversation with YC's Diana Hu: "Every six months, delete your claude.md, delete your skills, delete your hooks, see what the model does, and it might surprise you." In the same talk, he said his team deleted over 80% of Claude Code's own system prompt for Opus 5 (<a href="https://www.barath.ai/learnings/boris-cherny-yc-startup-school-2026">write-up</a>, <a href="https://sozai.app/transcript/boris-cherny-cut-80-percent-claude-code-prompt/">transcript</a>). I'd take a vendor's word on its own product with a grain of salt — but it matches what my stock arm did.</p>

<p>That's what I take "let Claude be Claude" to mean. Not "stop building" — Spotify's instinct to test was exactly right. It's that every optimization is a bet on today's model, and the bet needs rechecking every time the model and harness change. A hook that might have saved money on last year's model can cost money on this one.</p>

<blockquote class="tldr">TLDR; build and test ideas like shunt — then keep retesting them, because the platform underneath keeps doing more of the work for free.</blockquote>

<h3>Claude Plugin Evals</h3>

<p>Speaking of letting Claude be Claude: while this sat in my drafts for a month, Anthropic beat me to it. In September it shipped <code>claude plugin eval</code>, which runs your plugin against a suite of test cases, scores each result, and — by default — runs every case again without the plugin, so you can see what the plugin actually contributes. <code>claude plugin eval init</code> will even ask you what a good result looks like and draft the test cases and graders for you. The summary shows each case's score with and without the plugin, the difference, and the cost.</p>

<p>That's the same core move as this piece: plugin versus no plugin, on the same tasks, with the bill attached. Where they differ is depth. Plugin eval tells you <em>whether</em> a plugin helped and what it cost. This eval went a layer down to ask <em>why</em> — turn by turn, cache bucket by cache bucket, and what the model did right after a block. For most teams, plugin eval is the right place to start. If the cost column surprises you, that's when it's worth pulling the traces.</p>

<p>If I were Spotify, that's the test I'd rerun every time a new model ships. Tokens are the number everyone's watching right now. Turns are the number on the bill.</p>

<p class="byline" style="margin-top:8px">The full write-up, with the deviations table, the metrics as equations, the validation checklist, and all 189 runs, is at <a href="https://github.com/hmassa14/TurnsNotTokens">github.com/hmassa14/TurnsNotTokens</a>.</p>

</main>
'''
out = HEAD + body
for stale in ('twelve tasks', 'two arms', '114 sessions'):
    assert stale not in out, stale
assert not re.findall(r'\{[a-z_0-9]+\}', out.replace('${{lines}}', '').replace('${HARNESS}', '').replace('${PROMPT}', '')), 'placeholder left'
open(os.path.join(ROOT, 'post-short.html'), 'w').write(out)
print('post-short.html written', len(out), 'chars')
