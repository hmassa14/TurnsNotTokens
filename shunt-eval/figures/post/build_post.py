"""Assemble post-figures.html (two arms, second grid) from the v1 head, hand SVG, generated bars and storyboard fragments.

Run from this directory after regenerating the storyboards (see ../README.md). Data comes from
results/05-natural-second-grid: the SC1 stock/hook pair (rep 1) for D, E and F, and summary.json for A, G and H.
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, '..', '..', 'results', '05-natural-second-grid'))
S = json.load(open(os.path.join(R, 'summary.json')))
OV = S['overall']
v1 = open(os.path.join(HERE, 'post-figures-v1-five-arms.html')).read()
head = v1[:v1.index('<main>')]
figA = v1[v1.index('<figure>'):v1.index('</figure>')+9]  # Figure A block, hand SVG

# ---------- A: the three exits, with the second grid's counts ----------
ab = OV['after_block']
blocks = OV['blocks']
n_grep = ab.get('Grep', 0) + ab.get('Bash', 0)
n_paged = ab.get('Read(paged)', 0)
n_skill = ab.get('Skill', 0)
runs_hook = OV['runs'][1]
old_strip = figA[figA.index('<!-- three columns'):figA.index('</svg>')]
new_strip = f'''<!-- three columns: x = 30, 320, 610 ; width 250 -->
      <rect x="30" y="358" width="250" height="52" rx="6" class="box hook-s" stroke-width="1.6"/>
      <text x="155" y="379" text-anchor="middle" font-weight="600">Spotify's worker script</text>
      <text x="155" y="396" text-anchor="middle" class="small">bulk-read → Haiku reads the file → summary</text>
      <text x="155" y="428" text-anchor="middle" class="small mono">{n_skill} of {blocks} blocks</text>
      <text x="155" y="443" text-anchor="middle" class="small">what the design assumes; {OV['worker_calls']} worker calls in {runs_hook} runs</text>

      <rect x="320" y="358" width="250" height="52" rx="6" class="box hook-s" stroke-width="1.6"/>
      <text x="445" y="379" text-anchor="middle" font-weight="600">Grep or Bash on the file</text>
      <text x="445" y="396" text-anchor="middle" class="small">never blocked; matching lines enter context</text>
      <text x="445" y="428" text-anchor="middle" class="small mono">{n_grep} of {blocks} blocks</text>
      <text x="445" y="443" text-anchor="middle" class="small">what usually happened</text>

      <rect x="610" y="358" width="250" height="52" rx="6" class="box dim" stroke-dasharray="5 4"/>
      <text x="735" y="379" text-anchor="middle" font-weight="600" class="dim">Read(file, offset, limit)</text>
      <text x="735" y="396" text-anchor="middle" class="small">the published hook lets this through</text>
      <text x="735" y="428" text-anchor="middle" class="small mono">tried {n_paged} times; refused here</text>
      <text x="735" y="443" text-anchor="middle" class="small">closed for this test (see call-out)</text>
    '''
figA = figA.replace(old_strip, new_strip)
figA = re.sub(r'aria-label="[^"]*"', f'aria-label="Claude Code\'s tool loop with Spotify\'s PreToolUse hook in the path of a Read call, and what the model did next after each of the {blocks} blocks in the second grid: the worker script {n_skill} times, grep or a shell search {n_grep} times, a paged read {n_paged} times, which the enforced hook refused."', figA, count=1)
figA = re.sub(r'<figcaption>.*?</figcaption>', f'<figcaption><b>Where the hook sits, and the way out.</b> A PreToolUse hook runs between the model\'s tool call and the tool. On allow, the file comes back whole. On block, only the hook\'s message comes back, and the model chooses its next call. Spotify\'s design assumes that choice is the worker script. Across {blocks} blocks in {runs_hook} hook runs it was, {n_skill} times. The usual choice was grep, {n_grep} times. The right-hand exit, a read with an offset, is the one the published hook leaves open; we closed it so the hook would do what the post describes, and the model still tried it {n_paged} times.</figcaption>', figA, flags=re.S)
figA = figA.replace('<figure>', '<figure id="fig-hook">', 1)

# ---------- B: setup, two arms ----------
figB = '''<figure id="fig-setup">
    <span class="fig-n">Figure B · the setup</span>
    <svg viewBox="0 0 900 372" role="img" aria-label="How one run works: a fresh Kafka copy gets a .claude folder, a headless Claude Code session runs the prompt, three records are collected, and the answer is graded. Two arms differ only in the .claude folder: empty for stock; Spotify's hooks, scripts and skills for the hook arm, with the Portal call replaced by a Haiku call and the offset/limit exception removed.">
      <defs><marker id="ars" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
      <text x="20" y="22" font-weight="600">One run = one fresh Claude Code session. The only thing that differs between the two arms is the .claude/ folder.</text>
      <rect x="20" y="44" width="150" height="54" rx="6" class="box"/><text x="95" y="66" text-anchor="middle" font-weight="600">Fresh Kafka copy</text><text x="95" y="83" text-anchor="middle" class="small">pinned commit, 125 MB</text>
      <line x1="170" y1="71" x2="200" y2="71" stroke="currentColor" stroke-width="1.2" marker-end="url(#ars)"/>
      <rect x="202" y="44" width="150" height="54" rx="6" class="box"/><text x="277" y="66" text-anchor="middle" font-weight="600">+ one .claude/ folder</text><text x="277" y="83" text-anchor="middle" class="small">the arm</text>
      <line x1="352" y1="71" x2="382" y2="71" stroke="currentColor" stroke-width="1.2" marker-end="url(#ars)"/>
      <rect x="384" y="44" width="170" height="54" rx="6" class="box"/><text x="469" y="66" text-anchor="middle" font-weight="600" class="mono">claude -p "question"</text><text x="469" y="83" text-anchor="middle" class="small">new session, 40-turn cap</text>
      <line x1="554" y1="71" x2="584" y2="71" stroke="currentColor" stroke-width="1.2" marker-end="url(#ars)"/>
      <rect x="586" y="44" width="150" height="54" rx="6" class="box"/><text x="661" y="60" text-anchor="middle" font-weight="600">Three records</text><text x="661" y="76" text-anchor="middle" class="small">result JSON · transcript</text><text x="661" y="90" text-anchor="middle" class="small">OpenTelemetry</text>
      <line x1="736" y1="71" x2="766" y2="71" stroke="currentColor" stroke-width="1.2" marker-end="url(#ars)"/>
      <rect x="768" y="44" width="112" height="54" rx="6" class="box"/><text x="824" y="66" text-anchor="middle" font-weight="600">Grade</text><text x="824" y="83" text-anchor="middle" class="small">against a key</text>

      <text x="20" y="140" font-weight="600">The two .claude/ folders</text>
      <rect x="20" y="152" width="300" height="170" rx="6" class="box stock-s" stroke-width="1.6"/>
      <text x="170" y="176" text-anchor="middle" font-weight="600" fill="var(--stock)">A · stock</text>
      <text x="170" y="202" text-anchor="middle" class="small mono">settings.json: {}</text>
      <text x="170" y="236" text-anchor="middle" class="small">nothing else</text>
      <text x="170" y="300" text-anchor="middle" class="small">Claude Code as installed: its own Read limits,</text>
      <text x="170" y="314" text-anchor="middle" class="small">prompt caching, and the Explore subagent if it wants it</text>

      <rect x="340" y="152" width="540" height="170" rx="6" class="box hook-s" stroke-width="1.6"/>
      <text x="610" y="176" text-anchor="middle" font-weight="600" fill="var(--hook)">B · Spotify's hook</text>
      <text x="360" y="202" class="small mono">hooks/check-file-size    blocks Read on files over 350 lines</text>
      <text x="360" y="217" class="small mono">hooks/check-bash-read    blocks cat, head, sed on the same files</text>
      <text x="360" y="232" class="small mono">scripts/bulk-read        the worker: Haiku reads, returns a summary</text>
      <text x="360" y="247" class="small mono">scripts/code-write       the worker for edits</text>
      <text x="360" y="262" class="small mono">skills/bulk-reader, code-writer   tell the model when to call them</text>
      <text x="360" y="290" class="small">Spotify's published plugin with two changes: the call to their internal Portal</text>
      <text x="360" y="304" class="small">becomes a call to Haiku, and the rule that let a paged read through is deleted,</text>
      <text x="360" y="318" class="small">so the hook enforces what the post describes (call-out below).</text>
      <text x="20" y="356" class="small">Twenty-one tasks on Kafka, each asked as a developer would (no file path given), three runs per arm per task, Sonnet 5 as the main model, Haiku as the worker.</text>
    </svg>
    <figcaption><b>The setup.</b> Every run starts from an untouched Kafka checkout and a fresh headless session; nothing carries over. Two folders. Stock is Claude Code as installed. The hook arm is Spotify's published plugin with its Portal call pointed at Haiku and one rule removed, so that a file over 350 lines cannot be read by the expensive model at all.</figcaption>
  </figure>'''

# ---------- C: the call-out storyboard (from the pilot, unchanged) ----------
sc = open(os.path.join(HERE, 'story_callout.html')).read().replace('<div class="sb">','').rsplit('</div>',1)[0]
figC = f'''<figure id="fig-callout">
    <span class="fig-n">Figure C · call-out: the rule we removed, and why</span>
    <p class="small" style="margin:0 0 10px;color:var(--ink-2)">The same broker-lifecycle question under Spotify's hook exactly as published, requests 4 to 6 of 11, from the pilot. The blocked read is followed by a read with an offset, which the published hook allows.</p>
<div class="sb">{sc}</div>
    <figcaption><b>Why the test uses a stricter hook than the one Spotify shipped.</b> The published hook has an exception: a Read with an offset or limit is allowed, so the model can page through a big file after being refused it. In our pilot it did exactly that on every block, nine of nine, and 655 of the 770 lines ended up in context anyway. That is not the design the post describes, so we deleted the exception. Everything after this figure is measured with the exception closed.</figcaption>
  </figure>'''

# ---------- D: main storyboard, SC1 rep 1 ----------
sm = open(os.path.join(HERE, 'story_main.html')).read().replace('<div class="sb">','').rsplit('</div>',1)[0]
figD = f'''<figure id="fig-story">
    <span class="fig-n">Figure D · one question, request by request</span>
    <p class="small" style="margin:0 0 10px;color:var(--ink-2)">"How does the broker lifecycle manager move between states?" Stock, request 3 of 5; then with the hook, requests 3, 5, 6, 7, 8, 9 and 15 of 15. Each numbered row is one API request: what the model was given, what it decided, what came back.</p>
<div class="sb">{sm}</div>
    <figcaption><b>What the model does when it cannot read the file.</b> Stock found the file with one grep and read it whole on its third request; the answer came on the fifth. With the hook, the same read was refused, a paged read was refused, and then the model did what Spotify designed: it opened the bulk-reader skill and sent the file to the Haiku worker. The worker's summary came back on request 7. The model then grepped the file anyway, tried another paged read, grepped twice more, and answered on request 15. Correct answer both times: 5 requests against 15, plus the worker's own call.</figcaption>
  </figure>'''

# ---------- E: bars, generated from the transcripts ----------
def reqs(d):
    tp = json.load(open(d + '/transcript_parsed.json'))
    rs = sorted(tp['requests'], key=lambda r: r['first_ts'] or '')
    tools = {t['request_id']: t for t in tp['tool_calls'] if t.get('agent', 'main') == 'main'}
    return [(r['usage'], tools.get(r['request_id'])) for r in rs]
stock = reqs(os.path.join(R, 'SC1-stock-r1'))
strict = reqs(os.path.join(R, 'SC1-shunt-strict-r1'))
stock_cost = json.load(open(os.path.join(R, 'SC1-stock-r1', 'result.json')))['total_cost_usd']
strict_cost = json.load(open(os.path.join(R, 'SC1-shunt-strict-r1', 'result.json')))['total_cost_usd']
worker = [json.load(open(os.path.join(R, 'SC1-shunt-strict-r1', 'worker', f))) for f in sorted(os.listdir(os.path.join(R, 'SC1-shunt-strict-r1', 'worker')))]
worker_cost = sum(w.get('total_cost_usd', 0) for w in worker)
worker_chars = sum(len(w.get('result', '')) for w in worker)
def sent(u): return u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('input_tokens', 0)
maxt = max(sent(u) for u, _ in stock + strict)
scale = 130 / maxt
def lab(t, u):
    if t is None: return ('answer', f"{u.get('output_tokens',0)/1000:.1f}k out")
    n, i = t['name'], t['input']
    if n == 'Read':
        if 'hook_blocked' in t.get('flags', []): return ('Read', 'refused')
        if 'offset' in i: return ('Read', f"{i['offset']}+{i.get('limit','')}")
        return ('Read', f"{t.get('result_lines',0)} ln")
    if n == 'Grep':
        c = t.get('result_chars', 0)
        return ('Grep', f'{c/1000:.1f}k' if c >= 1000 else str(c))
    if n == 'Bash':
        if 'bulk-read' in i.get('command', ''): return ('worker', f"{t.get('result_chars',0)/1000:.1f}k")
        return ('Bash', i.get('command','')[:4].strip())
    if n == 'Skill': return ('Skill', 'bulk')
    if n == 'Glob': return ('Glob', '')
    return (n, '')
def lane(rows, y0, x0, step, w, cls, topn=()):
    out = []
    for k, (u, t) in enumerate(rows):
        h = sent(u) * scale; x = x0 + k * step; cx = x + w / 2
        out.append(f'<rect x="{x:.1f}" y="{y0-h:.1f}" width="{w}" height="{h:.1f}" rx="3" class="{cls}" opacity="0.85"/>')
        if t and 'hook_blocked' in t.get('flags', []):
            out.append(f'<rect x="{x:.1f}" y="{y0-h:.1f}" width="{w}" height="{h:.1f}" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/>')
            out.append(f'<text x="{cx:.1f}" y="{y0-h-22:.0f}" text-anchor="middle" class="small" font-weight="600">blocked</text>')
        if t and t['name'] == 'Bash' and 'bulk-read' in t['input'].get('command', ''):
            out.append(f'<rect x="{x:.1f}" y="{y0-h:.1f}" width="{w}" height="{h:.1f}" rx="3" fill="none" stroke="var(--hook)" stroke-width="1.8" stroke-dasharray="4 3"/>')
            out.append(f'<text x="{cx:.1f}" y="{y0-h-22:.0f}" text-anchor="middle" class="small" font-weight="600">worker</text>')
        if k in topn:
            out.append(f'<text x="{cx:.1f}" y="{y0-h-7:.0f}" text-anchor="middle" class="small mono">{sent(u)/1000:.0f}k</text>')
        a, b = lab(t, u)
        out.append(f'<text x="{cx:.1f}" y="{y0+16}" text-anchor="middle" class="small">{a}</text>')
        if b: out.append(f'<text x="{cx:.1f}" y="{y0+30}" text-anchor="middle" class="small mono">{b}</text>')
    return '\n'.join(out)
st_cr = sum(u.get('cache_read_input_tokens',0) for u,_ in stock); st_out = sum(u.get('output_tokens',0) for u,_ in stock)
sh_cr = sum(u.get('cache_read_input_tokens',0) for u,_ in strict); sh_out = sum(u.get('output_tokens',0) for u,_ in strict)
grep_chars = sum(t.get('result_chars',0) for u,t in strict if t and t['name']=='Grep')
file_read = next(t for u,t in stock if t and t['name']=='Read' and 'BrokerLifecycle' in t['input'].get('file_path',''))
file_tokens = file_read.get('result_chars',0)//4
n_st, n_sh = len(stock), len(strict)
w_sh = 36; step_sh = (880-66-w_sh)//(n_sh-1) if n_sh > 1 else 50
figE = f'''<figure id="fig-bars">
    <span class="fig-n">Figure E · the same question as bars</span>
    <svg viewBox="0 0 900 600" role="img" aria-label="Two request-by-request traces of the broker-lifecycle question. Stock: {n_st} API requests, {st_cr:,} cache-read tokens in total, {stock_cost*100:.0f} cents. With the hook enforced: {n_sh} requests, three of them refused reads, one the worker call; context grows from 30 to 45 thousand tokens per request, {sh_cr:,} cache-read tokens in total, {strict_cost*100:.0f} cents plus {worker_cost*100:.0f} cents for the worker.">
      <text x="20" y="22" font-weight="600">"How does the broker lifecycle manager move between states?"  ·  770-line file  ·  Sonnet 5</text>
      <text x="20" y="40" class="small">Each bar is one API request; its height is everything sent to the model, almost all of it read from cache. Under each bar: the tool call made next, and what it returned.</text>
      <text x="20" y="80" font-weight="600" fill="var(--stock)">A · stock</text>
      <text x="20" y="96" class="small">{n_st} requests · {st_cr:,} cached tokens re-sent · {st_out:,} output tokens · ${stock_cost:.3f}</text>
      <line x1="60" y1="240" x2="880" y2="240" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
{lane(stock, 240, 70, 100, 46, 'stock', topn=tuple(range(n_st)))}
      <text x="560" y="150" class="small">the file: {file_tokens/1000:.1f}k tokens, written to cache once ({file_tokens*2.5/1e4:.1f}¢)</text>
      <text x="560" y="168" class="small">everything else: re-read from cache at a tenth of input price</text>
      <text x="20" y="330" font-weight="600" fill="var(--hook)">B · Spotify's hook, enforced</text>
      <text x="20" y="346" class="small">{n_sh} requests · {sh_cr:,} cached tokens re-sent · {sh_out:,} output tokens · ${strict_cost:.3f} + ${worker_cost:.3f} worker</text>
      <line x1="60" y1="490" x2="880" y2="490" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
{lane(strict, 490, 66, step_sh, w_sh, 'hook', topn=(0, n_sh-1))}
      <text x="470" y="560" text-anchor="middle" class="small">the worker's summary came back as {worker_chars/1000:.1f}k characters; the model grepped {grep_chars/1000:.0f}k more out of the file after it, each piece re-sent on every request after it</text>
    </svg>
    <figcaption><b>The same question, request by request.</b> Stock read the file once and answered on the fifth request. With the hook, the third request's read was refused and so was a paged read; the model then called the worker, got a summary, and kept going: four more greps, another refused read, and the answer on request {n_sh}. Cached tokens re-sent went from {st_cr//1000}k to {sh_cr//1000}k and output tokens from {st_out/1000:.1f}k to {sh_out/1000:.1f}k. Both answers were correct. Data from <code>results/05-natural-second-grid</code>, SC1 rep 1.</figcaption>
  </figure>'''

# ---------- F: where the money went ----------
def buckets(rows):
    first = rows[0][0]
    sys_w = first.get('cache_creation_input_tokens',0); rest_w = sum(u.get('cache_creation_input_tokens',0) for u,_ in rows[1:])
    cr = sum(u.get('cache_read_input_tokens',0) for u,_ in rows); out = sum(u.get('output_tokens',0) for u,_ in rows)
    return sys_w, rest_w, cr, out
s_sys, s_rest, s_cr, s_out = buckets(stock); h_sys, h_rest, h_cr, h_out = buckets(strict)
# cents at Sonnet 5 list price; every cache write in this grid is at the 5-minute rate (2.5), pinned; both bars reconcile to result.json
Sb = [s_sys*2.5/1e4, s_rest*2.5/1e4, s_cr*0.2/1e4, s_out*10/1e4, 0.0]
Hb = [h_sys*2.5/1e4, h_rest*2.5/1e4, h_cr*0.2/1e4, h_out*10/1e4, worker_cost*100]
px = 8.0; base = 330
def stack(vals, x, cls):
    out = []; y = base; ops = [0.3, 0.5, 0.7, 0.9, 1.0]; ys = []
    for v, op in zip(vals, ops):
        h = v * px; y -= h
        if v > 0:
            out.append(f'<rect x="{x}" y="{y:.1f}" width="80" height="{max(h-2,0):.1f}" class="{cls}" opacity="{op}"/>')
            out.append(f'<text x="{x+40}" y="{y+h/2+4:.1f}" text-anchor="middle" class="small mono">{v:.1f}</text>')
        ys.append(y + h/2)
    return '\n'.join(out), ys
stS, _ = stack(Sb, 90, 'stock'); stH, ysH = stack(Hb, 290, 'hook')
leg = [("system prompt and tools, written to cache once", None),
       ("tool results written to cache once", f"the whole file ({file_tokens/1000:.1f}k tokens) vs {grep_chars/4/1000:.1f}k of greps plus the worker's summary"),
       ("the whole conversation re-sent on every request, at the cache-read rate", f"{n_st} requests of ~30-48k tokens vs {n_sh} requests of 30-45k"),
       ("output: thinking and the answer, at the output rate", f"{n_sh} rounds of thinking instead of {n_st}"),
       ("the worker's own call (Haiku, one turn)", f"{worker[0]['usage'].get('cache_creation_input_tokens',0)/1000:.0f}k in, {worker[0]['usage'].get('output_tokens',0)/1000:.0f}k out, mostly its thinking")]
legsvg = []
for (a, b), y in zip(leg, ysH):
    legsvg.append(f'<line x1="372" y1="{y:.0f}" x2="392" y2="{y:.0f}" stroke="currentColor" stroke-width="0.6" opacity="0.5"/>')
    if b:
        legsvg.append(f'<text x="398" y="{y-4:.0f}" class="small" font-weight="600">{a}</text><text x="398" y="{y+12:.0f}" class="small">{b}</text>')
    else:
        legsvg.append(f'<text x="398" y="{y+4:.0f}" class="small">{a}</text>')
d = [h-s for h, s in zip(Hb, Sb)]
figF = f'''<figure id="fig-money">
    <span class="fig-n">Figure F · where the money went</span>
    <svg viewBox="0 0 900 430" role="img" aria-label="Cost breakdown of the two broker-lifecycle runs in cents, stacked by price bucket. Stock: {Sb[0]:.1f} cents system prompt, {Sb[1]:.1f} cents tool results written to cache, {Sb[2]:.1f} cents cache re-reads, {Sb[3]:.1f} cents output, {sum(Sb):.1f} total. Hook: {Hb[0]:.1f}, {Hb[1]:.1f}, {Hb[2]:.1f}, {Hb[3]:.1f}, plus {Hb[4]:.1f} cents for the worker, total {sum(Hb):.1f}. The bucket that grew most is the conversation re-sent on every request.">
      <text x="20" y="22" font-weight="600">Where the money went, in cents at list price</text>
      <text x="20" y="40" class="small">Same two runs as Figures D and E. Each bar is the run's total cost, stacked by what the tokens were billed as.</text>
      <text x="130" y="82" text-anchor="middle" font-weight="600" fill="var(--stock)">A · stock</text>
      <text x="130" y="98" text-anchor="middle" class="small mono">{sum(Sb):.1f}¢ · {n_st} requests</text>
{stS}
      <text x="330" y="82" text-anchor="middle" font-weight="600" fill="var(--hook)">B · Spotify's hook, enforced</text>
      <text x="330" y="98" text-anchor="middle" class="small mono">{sum(Hb):.1f}¢ · {n_sh} requests + worker</text>
{stH}
      <line x1="70" y1="{base}" x2="400" y2="{base}" stroke="currentColor" stroke-width="0.8"/>
{chr(10).join(legsvg)}
      <line x1="70" y1="356" x2="880" y2="356" stroke="currentColor" stroke-width="0.6" opacity="0.4"/>
      <text x="70" y="378"><tspan font-weight="600">The read the hook refused would have cost {file_tokens*2.5/1e4:.1f}¢.</tspan><tspan class="small"> Delegating, then searching anyway: +{d[2]:.1f}¢ re-sends, +{d[3]:.1f}¢ output, +{d[4]:.1f}¢ worker.</tspan></text>
      <text x="70" y="400" class="small mono">Sonnet 5 per M tokens · input $2.00 · cache write $2.50 (5-min, pinned) · cache read $0.20 · output $10.00 · Haiku at list</text>
      <text x="70" y="416" class="small">Both bars reconcile to the cost Claude Code reported for the run; the worker's cost comes from its own usage record.</text>
    </svg>
    <figcaption><b>What caching makes cheap, and what it does not.</b> The bucket the hook targets, file content written to cache, did shrink: the greps and the worker's summary add up to less than the file. But the bucket that grew most is the one the hook never looks at. Every request re-sends the entire conversation. Re-reads are cheap per token, a fifth of a cent per thousand, but {n_sh} of them at 30k to 45k tokens each cost three times what {n_st} did, and every request ends in fresh thinking at fifty times that price. With caching, a file that enters context once is nearly free afterward. A turn is not.</figcaption>
  </figure>'''

# ---------- G: headline, three small multiples, two arms ----------
tgt = OV['tgt_tokens_mean']; rq = OV['requests_mean']; cst = OV['cost_mean']; pr = OV['pass_rate']
def panel(x, title, vals, fmt, w=110, gap=20, top=98, base=260):
    out = [f'<text x="{x}" y="76" font-weight="600">{title}</text>', f'<line x1="{x}" y1="{base}" x2="{x+2*w+gap}" y2="{base}" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>']
    m = max(vals)
    for k, (v, cls, name) in enumerate(zip(vals, ('stock','hook'), ('A stock','B hook'))):
        h = (base - top) * v / m; bx = x + k*(w+gap)
        out.append(f'<rect x="{bx}" y="{base-h:.1f}" width="{w}" height="{h:.1f}" rx="4" class="{cls}"/><rect x="{bx}" y="{base-4}" width="{w}" height="4" class="{cls}"/>')
        out.append(f'<text x="{bx+w/2}" y="{base-h-6:.1f}" text-anchor="middle" class="small mono">{fmt.format(v)}</text>')
        out.append(f'<text x="{bx+w/2}" y="{base+16}" text-anchor="middle" class="small">{name}</text>')
    return '\n'.join(out)
tgt_pct = (1 - tgt[1]/tgt[0]) * 100; cost_pct = OV['cost_pct_of_means']; req_pct = (rq[1]/rq[0]-1)*100
figG = f'''<figure id="fig-headline">
    <span class="fig-n">Figure G · the result</span>
    <svg viewBox="0 0 900 330" role="img" aria-label="Three bar charts, stock against the enforced hook, means per run over 21 tasks and 114 runs. Target-file content in the main model's context: {tgt[0]:,.0f} against {tgt[1]:,.0f} tokens. API requests: {rq[0]:.1f} against {rq[1]:.1f}. Cost at list price: ${cst[0]:.3f} against ${cst[1]:.3f}. Pass rate {pr[0]*100:.0f}% against {pr[1]*100:.0f}%.">
      <text x="20" y="22" font-weight="600">Twenty-one tasks, three runs each: the content Spotify counts fell {tgt_pct:.0f}%, the bill rose {cost_pct:.0f}%</text>
      <text x="20" y="40" class="small">Means per run, same tasks, same model, same Kafka, {OV['runs'][0]} runs per arm. Pass rate {pr[0]*100:.0f}% stock, {pr[1]*100:.0f}% hook.</text>
{panel(40, 'Target-file tokens in main context', [tgt[0], tgt[1]], '{:,.0f}')}
{panel(340, 'API requests per run', [rq[0], rq[1]], '{:.1f}')}
{panel(640, 'Cost per run, list price', [cst[0], cst[1]], '${:.3f}')}
      <rect x="40" y="300" width="14" height="10" rx="2" class="stock"/><text x="60" y="309" class="small">stock Claude Code</text>
      <rect x="200" y="300" width="14" height="10" rx="2" class="hook"/><text x="220" y="309" class="small">with Spotify's hook, enforced (worker cost included)</text>
    </svg>
    <figcaption><b>The result.</b> The hook did what the post promised on the post's own metric: {tgt_pct:.0f}% less target-file content in the expensive model's context, counted through every tool, not just Read. It did so by turning reads into greps and, sometimes, into a worker call, which added {req_pct:.0f}% more API requests per run, and the bill went up {cost_pct:.0f}% for the same pass rate. The three charts share arms and nothing else; they are deliberately not one dual-axis chart. Detail per task is in the results tables.</figcaption>
  </figure>'''

# ---------- H: cost change by task type, paired, with intervals ----------
cats = S['by_category']
rowsH = [('Spotify\'s four benchmark tasks', cats['SB']), ('Needle: one fact in a big file', cats['ND']),
         ('Spotify\'s shapes on files over 350 lines', cats['SC']), ('Harm: precise edits, debugging, big files', cats['HM']),
         ('Controls: small files, hook never fires', cats['CT']), None,
         ('Hook fired, model called the worker', S['delegated_tasks']), ('Hook fired, model grepped instead', S['grep_only_tasks'])]
x0, x1 = 330, 860; lo, hi = -60, 100
def X(v): return x0 + (min(max(v, lo), hi) - lo) / (hi - lo) * (x1 - x0)
svgH = [f'<line x1="{X(0):.0f}" y1="70" x2="{X(0):.0f}" y2="{70+len(rowsH)*40}" stroke="currentColor" stroke-width="0.8"/>']
for tick in (-50, -25, 0, 25, 50, 75, 100):
    svgH.append(f'<text x="{X(tick):.0f}" y="62" text-anchor="middle" class="small mono">{tick:+d}%</text>')
    if tick: svgH.append(f'<line x1="{X(tick):.0f}" y1="70" x2="{X(tick):.0f}" y2="{70+len(rowsH)*40}" stroke="currentColor" stroke-width="0.4" opacity="0.3"/>')
y = 90
for row in rowsH:
    if row is None:
        svgH.append(f'<line x1="20" y1="{y-8}" x2="880" y2="{y-8}" stroke="currentColor" stroke-width="0.6" opacity="0.4"/>'); y += 12; continue
    label, g = row
    m = g['cost_pct_paired_mean']; ci = g['cost_pct_paired_ci']; n = g['n_tasks']
    cls = 'hook' if m > 0 else 'stock'
    svgH.append(f'<text x="20" y="{y+4}" class="small" font-weight="600">{label}</text>')
    svgH.append(f'<text x="20" y="{y+18}" class="small">{n} tasks · pass {g["pass_rate"][0]*100:.0f}% / {g["pass_rate"][1]*100:.0f}% · hook cheaper on {g["hook_cheaper_tasks"]} of {n}</text>')
    if ci[0] is not None:
        svgH.append(f'<line x1="{X(ci[0]):.0f}" y1="{y}" x2="{X(ci[1]):.0f}" y2="{y}" stroke="currentColor" stroke-width="1.2" opacity="0.7"/>')
    svgH.append(f'<rect x="{min(X(0), X(m)):.0f}" y="{y-9}" width="{abs(X(m)-X(0)):.0f}" height="18" rx="3" class="{cls}" opacity="0.85"/>')
    edge = (max(ci[1], m) if ci[0] is not None else m) if m >= 0 else (min(ci[0], m) if ci[0] is not None else m)
    svgH.append(f'<text x="{X(edge) + (8 if m >= 0 else -8):.0f}" y="{y+4}" text-anchor="{"start" if m >= 0 else "end"}" class="small mono" font-weight="600">{m:+.0f}%</text>')
    y += 40
figH = f'''<figure id="fig-by-category">
    <span class="fig-n">Figure H · cost change by task type</span>
    <svg viewBox="0 0 900 {y+30}" role="img" aria-label="Horizontal bars of the hook arm's cost relative to stock, per task type, with 95% bootstrap intervals over tasks. Spotify's four benchmark tasks {cats['SB']['cost_pct_paired_mean']:+.0f}%. Needle reads {cats['ND']['cost_pct_paired_mean']:+.0f}%. Spotify's shapes on big files {cats['SC']['cost_pct_paired_mean']:+.0f}%. Harm tasks {cats['HM']['cost_pct_paired_mean']:+.0f}%. Controls {cats['CT']['cost_pct_paired_mean']:+.0f}%. Tasks where the worker was called {S['delegated_tasks']['cost_pct_paired_mean']:+.0f}%. Tasks where the model grepped instead {S['grep_only_tasks']['cost_pct_paired_mean']:+.0f}%.">
      <text x="20" y="22" font-weight="600">Hook cost relative to stock, by task type · paired per task, mean of three runs each</text>
      <text x="20" y="40" class="small">Bar: mean of the per-task percentage differences. Line: 95% bootstrap interval over tasks. Worker cost included in the hook arm.</text>
{chr(10).join(svgH)}
    </svg>
    <figcaption><b>Where the bill moved.</b> The hook is not uniformly more expensive. On the needle reads it is a little cheaper, because the block turns a paged read into a grep. Where it fires on Spotify's own task shapes at real file sizes, and on the edit and debugging tasks Spotify says the approach is not for, it costs more. The split at the bottom is the mechanism: on the five tasks where the model actually called the worker, cost rose by half; on the twelve where it grepped its way around the block, cost was flat on average with a wide interval. Delegation, when it happens, is the expensive path.</figcaption>
  </figure>'''

lede = '<p class="lede">In post order. A: the mechanism. B: the setup. C: the call-out on the rule we removed. D, E, F: one task traced, then as bars, then in cents. G: the headline across twenty-one tasks. H: the same bill split by task type. Two arms throughout: stock, and Spotify\'s hook with its exception closed.</p>'
page = head + '<main>\n  <h1>Figures for "Tokens Are Cheap, Turns Are Not"</h1>\n  ' + lede + '\n\n  ' + '\n  '.join([figA, figB, figC, figD, figE, figF, figG, figH]) + '\n</main>\n'
open(os.path.join(HERE, 'post-figures.html'), 'w').write(page)
print('stock buckets', [round(v,1) for v in Sb], round(sum(Sb),1)); print('hook buckets', [round(v,1) for v in Hb], round(sum(Hb),1))
print('G', tgt, rq, cst, pr); print('A exits: skill', n_skill, 'grep/bash', n_grep, 'paged', n_paged, 'of', blocks)
