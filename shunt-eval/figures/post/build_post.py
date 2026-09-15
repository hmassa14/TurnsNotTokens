"""Assemble post-figures.html (three setups, the clean grid) from the v1 head, hand SVG, generated bars and storyboard fragments.

Run from this directory after regenerating the storyboards (see ../README.md). Data comes from
results/06-natural-clean-grid: the SC1 runs (stock rep 1, shipped rep 1, enforced rep 3) for D, E and F, and
summary-shipped.json / summary-enforced.json for A, B, G and H.
"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, '..', '..', 'results', '06-natural-clean-grid'))
S1 = json.load(open(os.path.join(R, 'summary-shipped.json')))   # stock vs as shipped
S2 = json.load(open(os.path.join(R, 'summary-enforced.json')))  # stock vs as described
O1, O2 = S1['overall'], S2['overall']
v1 = open(os.path.join(HERE, 'post-figures-v1-five-arms.html')).read()
head = v1[:v1.index('<main>')]
figA = v1[v1.index('<figure>'):v1.index('</figure>')+9]  # Figure A block, hand SVG

# ---------- A: why the hook, and what it's designed to do (mechanism only; behavior is Results/Discussion) ----------
ab1, ab2 = O1['after_block'], O2['after_block']
b1, b2 = O1['blocks'], O2['blocks']
grep1 = ab1.get('Grep', 0) + ab1.get('Bash', 0); grep2 = ab2.get('Grep', 0) + ab2.get('Bash', 0)
paged1 = ab1.get('Read(paged)', 0); paged2 = ab2.get('Read(paged)', 0)
skill1 = ab1.get('Skill', 0); skill2 = ab2.get('Skill', 0)
rem1 = b1 - (skill1 + grep1 + paged1); rem2 = b2 - (skill2 + grep2 + paged2)
figA = figA.replace('<figure>', '<figure id="fig-hook">', 1)

# ---------- B: setup, three setups ----------
figB = '''<figure id="fig-setup">
    <span class="fig-n">Figure B · the setup</span>
    <svg viewBox="0 0 900 390" role="img" aria-label="How one run works: a fresh Kafka copy with no git history gets a .claude folder, a headless Claude Code session runs the prompt inside an offline sandbox, three records are collected, and the answer is graded. Three setups differ only in the .claude folder: empty for stock; Spotify's plugin as published for 'as shipped'; the same with the offset/limit exception removed for 'as described'. The worker is a one-turn Haiku call with numbered lines in both hook setups.">
      <defs><marker id="ars" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="currentColor"/></marker></defs>
      <text x="20" y="22" font-weight="600">One run = one fresh, offline Claude Code session. The only thing that differs between setups is the .claude/ folder.</text>
      <rect x="20" y="44" width="150" height="54" rx="6" class="box"/><text x="95" y="66" text-anchor="middle" font-weight="600">Fresh Kafka copy</text><text x="95" y="83" text-anchor="middle" class="small">pinned commit, no history</text>
      <line x1="170" y1="71" x2="200" y2="71" stroke="currentColor" stroke-width="1.2" marker-end="url(#ars)"/>
      <rect x="202" y="44" width="150" height="54" rx="6" class="box"/><text x="277" y="66" text-anchor="middle" font-weight="600">+ one .claude/ folder</text><text x="277" y="83" text-anchor="middle" class="small">the setup</text>
      <line x1="352" y1="71" x2="382" y2="71" stroke="currentColor" stroke-width="1.2" marker-end="url(#ars)"/>
      <rect x="384" y="44" width="170" height="54" rx="6" class="box"/><text x="469" y="66" text-anchor="middle" font-weight="600" class="mono">claude -p "question"</text><text x="469" y="83" text-anchor="middle" class="small">sandboxed to the repo, 40 turns</text>
      <line x1="554" y1="71" x2="584" y2="71" stroke="currentColor" stroke-width="1.2" marker-end="url(#ars)"/>
      <rect x="586" y="44" width="150" height="54" rx="6" class="box"/><text x="661" y="60" text-anchor="middle" font-weight="600">Three records</text><text x="661" y="76" text-anchor="middle" class="small">result JSON · transcript</text><text x="661" y="90" text-anchor="middle" class="small">OpenTelemetry</text>
      <line x1="736" y1="71" x2="766" y2="71" stroke="currentColor" stroke-width="1.2" marker-end="url(#ars)"/>
      <rect x="768" y="44" width="112" height="54" rx="6" class="box"/><text x="824" y="66" text-anchor="middle" font-weight="600">Grade</text><text x="824" y="83" text-anchor="middle" class="small">against a key</text>

      <text x="20" y="140" font-weight="600">The three .claude/ folders</text>
      <rect x="20" y="152" width="250" height="186" rx="6" class="box stock-s" stroke-width="1.6"/>
      <text x="145" y="176" text-anchor="middle" font-weight="600" fill="var(--stock)">A · stock</text>
      <text x="145" y="202" text-anchor="middle" class="small mono">settings.json: {}</text>
      <text x="145" y="236" text-anchor="middle" class="small">nothing else</text>
      <text x="145" y="300" text-anchor="middle" class="small">Claude Code as installed, offline:</text>
      <text x="145" y="314" text-anchor="middle" class="small">its own Read limits, prompt caching,</text>
      <text x="145" y="328" text-anchor="middle" class="small">a subagent if it wants one</text>

      <rect x="290" y="152" width="590" height="186" rx="6" class="box hook-s" stroke-width="1.6"/>
      <text x="585" y="176" text-anchor="middle" font-weight="600" fill="var(--hook)">B · as shipped        C · as described</text>
      <text x="310" y="202" class="small mono">hooks/check-file-size    blocks Read on files over 350 lines  (B: unless offset/limit is set)</text>
      <text x="310" y="217" class="small mono">hooks/check-bash-read    blocks cat, head, tail on the same files</text>
      <text x="310" y="232" class="small mono">scripts/bulk-read        the worker: Haiku reads (numbered lines), returns a summary</text>
      <text x="310" y="247" class="small mono">scripts/code-write       the worker for generated code</text>
      <text x="310" y="262" class="small mono">skills/bulk-reader, code-writer   tell the model when to call them</text>
      <text x="310" y="292" class="small">Spotify's published plugin, byte-identical except the Portal call, which becomes a one-turn Haiku call</text>
      <text x="310" y="306" class="small">with the file sent line-numbered. B keeps the rule that lets a paged read through; C removes it.</text>
      <text x="310" y="320" class="small">That one rule is the only difference between B and C.</text>
      <text x="20" y="372" class="small">21 tasks on Kafka, asked as a developer would (no file path given) · 3 runs per setup per task · Sonnet 5 main, Haiku worker · 189 sessions</text>
    </svg>
    <figcaption><b>The setup.</b> Every run starts from an untouched Kafka checkout with no git history and a fresh headless session that cannot leave the repository; nothing carries over. Three folders, each one change apart. Stock is Claude Code as installed. As shipped is Spotify's published plugin with its Portal call pointed at Haiku. As described is the same with one rule removed, so that a file over 350 lines cannot be read by the expensive model at all.</figcaption>
  </figure>'''

# ---------- C: the call-out storyboard, from this grid's shipped setup ----------
sc = open(os.path.join(HERE, 'story_callout.html')).read().replace('<div class="sb">','').rsplit('</div>',1)[0]
figC = f'''<figure id="fig-callout">
    <span class="fig-n">Figure C · call-out: the rule that makes the shipped hook a suggestion</span>
    <p class="small" style="margin:0 0 10px;color:var(--ink-2)">The config-keys question under Spotify's hook exactly as published, requests 2 to 4 of 5. The blocked read is followed by two reads with an offset, which the published hook allows; between them they cover the whole 616-line file.</p>
<div class="sb">{sc}</div>
    <figcaption><b>Why one setup runs a stricter hook than the one Spotify shipped.</b> The published hook has an exception: a Read with an offset or limit is allowed, so the model can page through a big file after being refused it. In this grid it did that on {paged1} of {b1} blocks, and here the whole file came in anyway, in two slices, one request after the refusal. That is not the design the post describes, so the "as described" setup deletes the exception and everything else stays the same.</figcaption>
  </figure>'''

# ---------- D: main storyboard, three setups on one question ----------
sm = open(os.path.join(HERE, 'story_main.html')).read().replace('<div class="sb">','').rsplit('</div>',1)[0]
figD = f'''<figure id="fig-story">
    <span class="fig-n">Figure D · one question, request by request, three setups</span>
    <p class="small" style="margin:0 0 10px;color:var(--ink-2)">"How does the broker lifecycle manager move between states?" Stock, request 2 of 3. As shipped, requests 3, 5 and 6 of 9. As described, requests 2 and 5 to 9 of 9. Each numbered row is one API request: what the model was given, what it decided, what came back.</p>
<div class="sb">{sm}</div>
    <figcaption><b>What the model does when it cannot read the file.</b> Stock found the file with one grep, read it whole on its second request, and answered on the third. As shipped, the same read was refused, and the model read the file anyway in two slices of 280 and 370 lines, which the hook allows, then answered on the ninth request. As described, the read was refused, a paged read was refused, and the model did what Spotify designed: it opened the bulk-reader skill, sent the file to the worker, checked one thing with a grep, and answered on the ninth. Correct answer all three times.</figcaption>
  </figure>'''

# ---------- E: bars, generated from the transcripts ----------
def reqs(d):
    tp = json.load(open(d + '/transcript_parsed.json'))
    rs = sorted(tp['requests'], key=lambda r: r['first_ts'] or '')
    tools = {t['request_id']: t for t in tp['tool_calls'] if t.get('agent', 'main') == 'main'}
    return [(r['usage'], tools.get(r['request_id'])) for r in rs]
def cost_of(run): return json.load(open(os.path.join(R, run, 'result.json')))['total_cost_usd']
def worker_of(run):
    wd = os.path.join(R, run, 'worker')
    return [json.load(open(os.path.join(wd, f))) for f in sorted(os.listdir(wd))] if os.path.isdir(wd) else []
RUNS = [('stock', 'SC1-stock-r1', 'A · stock'), ('hook', 'SC1-shunt-r1', 'B · as shipped'), ('hook', 'SC1-shunt-strict-r3', 'C · as described')]
lanes = [(cls, run, label, reqs(os.path.join(R, run)), cost_of(run), worker_of(run)) for cls, run, label in RUNS]
def sent(u): return u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('input_tokens', 0)
maxt = max(sent(u) for _, _, _, rows, _, _ in lanes for u, _ in rows)
scale = 120 / maxt
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
        if 'worker_call' in t.get('flags', []): return ('worker', f"{t.get('result_chars',0)/1000:.1f}k")
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
        if t and 'worker_call' in t.get('flags', []):
            out.append(f'<rect x="{x:.1f}" y="{y0-h:.1f}" width="{w}" height="{h:.1f}" rx="3" fill="none" stroke="var(--hook)" stroke-width="1.8" stroke-dasharray="4 3"/>')
            out.append(f'<text x="{cx:.1f}" y="{y0-h-22:.0f}" text-anchor="middle" class="small" font-weight="600">worker</text>')
        if k in topn:
            out.append(f'<text x="{cx:.1f}" y="{y0-h-7:.0f}" text-anchor="middle" class="small mono">{sent(u)/1000:.0f}k</text>')
        a, b = lab(t, u)
        out.append(f'<text x="{cx:.1f}" y="{y0+16}" text-anchor="middle" class="small">{a}</text>')
        if b: out.append(f'<text x="{cx:.1f}" y="{y0+30}" text-anchor="middle" class="small mono">{b}</text>')
    return '\n'.join(out)
svgE = []; y = 70
stats = []
for cls, run, label, rows, cost, workers in lanes:
    cr = sum(u.get('cache_read_input_tokens',0) for u,_ in rows); out = sum(u.get('output_tokens',0) for u,_ in rows)
    wcost = sum(w.get('total_cost_usd', 0) for w in workers)
    stats.append((label, len(rows), cr, out, cost, wcost))
    color = 'var(--stock)' if cls == 'stock' else 'var(--hook)'
    svgE.append(f'<text x="20" y="{y}" font-weight="600" fill="{color}">{label}</text>')
    svgE.append(f'<text x="20" y="{y+16}" class="small">{len(rows)} requests · {cr:,} cached tokens re-sent · {out:,} output tokens · ${cost:.3f}' + (f' + ${wcost:.3f} worker' if wcost else '') + '</text>')
    base = y + 170
    svgE.append(f'<line x1="60" y1="{base}" x2="880" y2="{base}" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>')
    n = len(rows); w = 46 if n <= 5 else 36; step = 100 if n <= 5 else (880 - 66 - w) // (n - 1)
    svgE.append(lane(rows, base, 70 if n <= 5 else 66, step, w, cls, topn=(0, n-1)))
    y += 250
file_read = next(t for _, _, _, rows, _, _ in lanes for u, t in rows if t and t['name']=='Read' and 'BrokerLifecycle' in t['input'].get('file_path','') and 'hook_blocked' not in t.get('flags', []) and 'offset' not in t['input'])
file_tokens = file_read.get('result_chars',0)//4
figE = f'''<figure id="fig-bars">
    <span class="fig-n">Figure E · the same question as bars</span>
    <svg viewBox="0 0 900 {y+10}" role="img" aria-label="Three request-by-request traces of the broker-lifecycle question. Stock: {stats[0][1]} requests, {stats[0][4]*100:.0f} cents. As shipped: {stats[1][1]} requests, one refused read then two paged reads that go through, {stats[1][4]*100:.0f} cents. As described: {stats[2][1]} requests, two refused reads, a worker call, {stats[2][4]*100:.0f} cents plus {stats[2][5]*100:.0f} cents for the worker.">
      <text x="20" y="22" font-weight="600">"How does the broker lifecycle manager move between states?"  ·  770-line file  ·  Sonnet 5</text>
      <text x="20" y="40" class="small">Each bar is one API request; its height is everything sent to the model, almost all of it read from cache. Under each bar: the tool call made next, and what it returned.</text>
{chr(10).join(svgE)}
    </svg>
    <figcaption><b>The same question, request by request.</b> Stock read the file once ({file_tokens/1000:.1f}k tokens, written to cache for {file_tokens*2.5/1e4:.1f}¢) and answered on the third request. As shipped, the third request's read was refused and the model read the file anyway in two slices, plus a few greps, and answered on the ninth. As described, the read and a paged read were refused, the model called the worker, verified one thing with a grep, and answered on the ninth. Every request re-sends everything before it: {stats[0][2]//1000}k cached tokens re-sent for stock, {stats[1][2]//1000}k as shipped, {stats[2][2]//1000}k as described. All three answers were correct. Data from <code>results/06-natural-clean-grid</code>.</figcaption>
  </figure>'''

# ---------- F: where the money went, three bars ----------
def buckets(rows):
    first = rows[0][0]
    sys_w = first.get('cache_creation_input_tokens',0); rest_w = sum(u.get('cache_creation_input_tokens',0) for u,_ in rows[1:])
    cr = sum(u.get('cache_read_input_tokens',0) for u,_ in rows); out = sum(u.get('output_tokens',0) for u,_ in rows)
    return sys_w, rest_w, cr, out
# cents at Sonnet 5 list price; every cache write pinned at the 5-minute rate (2.5); bars reconcile to result.json
B = []
for cls, run, label, rows, cost, workers in lanes:
    s_, r_, c_, o_ = buckets(rows)
    B.append([s_*2.5/1e4, r_*2.5/1e4, c_*0.2/1e4, o_*10/1e4, sum(w.get('total_cost_usd',0) for w in workers)*100])
px = 9.0; base = 330
def stack(vals, x, cls):
    out = []; y = base; ops = [0.3, 0.5, 0.7, 0.9, 1.0]; ys = []
    for v, op in zip(vals, ops):
        h = v * px; y -= h
        if v > 0.05:
            out.append(f'<rect x="{x}" y="{y:.1f}" width="80" height="{max(h-2,0):.1f}" class="{cls}" opacity="{op}"/>')
            out.append(f'<text x="{x+40}" y="{y+h/2+4:.1f}" text-anchor="middle" class="small mono">{v:.1f}</text>')
        ys.append(y + h/2)
    return '\n'.join(out), ys
stacks = []; ysC = None
for k, ((cls, run, label, rows, cost, workers), vals) in enumerate(zip(lanes, B)):
    x = 60 + k * 150
    svg, ys = stack(vals, x, cls); stacks.append(svg)
    color = 'var(--stock)' if cls == 'stock' else 'var(--hook)'
    stacks.append(f'<text x="{x+40}" y="82" text-anchor="middle" font-weight="600" fill="{color}">{label}</text><text x="{x+40}" y="98" text-anchor="middle" class="small mono">{sum(vals):.1f}¢ · {len(rows)} req</text>')
    if k == 2: ysC = ys
leg = [("system prompt and tools, written to cache once", None),
       ("tool results written to cache once", "the whole file vs two slices vs greps plus the summary"),
       ("the conversation re-sent on every request, cache-read rate", f"{stats[0][1]} requests vs {stats[1][1]} vs {stats[2][1]}"),
       ("output: thinking and the answer, at the output rate", "one round of thinking per request"),
       ("the worker's own call (Haiku, one turn, thinking off)", "the numbered file in, a summary out")]
leg = list(reversed(leg))  # legend reads top-down in stack order
ysC = list(reversed(ysC))
legsvg = []
# legend rows at fixed spacing (top to bottom = top to bottom of the stack); a leader from each row to its segment
for k, ((a, b), yv) in enumerate(zip(leg, ysC)):
    yl = 120 + k * 46
    legsvg.append(f'<path d="M502 {yv:.0f} L514 {yv:.0f} L520 {yl:.0f} L526 {yl:.0f}" fill="none" stroke="currentColor" stroke-width="0.6" opacity="0.5"/>')
    if b:
        legsvg.append(f'<text x="532" y="{yl-4:.0f}" class="small" font-weight="600">{a}</text><text x="532" y="{yl+12:.0f}" class="small">{b}</text>')
    else:
        legsvg.append(f'<text x="532" y="{yl+4:.0f}" class="small" font-weight="600">{a}</text>')
figF = f'''<figure id="fig-money">
    <span class="fig-n">Figure F · where the money went</span>
    <svg viewBox="0 0 900 430" role="img" aria-label="Cost breakdown of the three broker-lifecycle runs in cents, stacked by price bucket. Stock {sum(B[0]):.1f} cents; as shipped {sum(B[1]):.1f}; as described {sum(B[2]):.1f} including {B[2][4]:.1f} for the worker. In both hook setups the bucket that grew most is the conversation re-sent on every request.">
      <text x="20" y="22" font-weight="600">Where the money went, in cents at list price</text>
      <text x="20" y="40" class="small">Same three runs as Figures D and E. Each bar is the run's total cost, stacked by what the tokens were billed as.</text>
{chr(10).join(stacks)}
      <line x1="50" y1="{base}" x2="500" y2="{base}" stroke="currentColor" stroke-width="0.8"/>
{chr(10).join(legsvg)}
      <line x1="50" y1="356" x2="880" y2="356" stroke="currentColor" stroke-width="0.6" opacity="0.4"/>
      <text x="50" y="378"><tspan font-weight="600">The read the hook refused would have cost {file_tokens*2.5/1e4:.1f}¢.</tspan><tspan class="small"> Paging around it: +{sum(B[1])-sum(B[0]):.1f}¢. Delegating it: +{sum(B[2])-sum(B[0]):.1f}¢, of which {B[2][4]:.1f}¢ is the worker.</tspan></text>
      <text x="50" y="400" class="small mono">Sonnet 5 per M tokens · input $2.00 · cache write $2.50 (5-min, pinned) · cache read $0.20 · output $10.00 · Haiku at list</text>
      <text x="50" y="416" class="small">All three bars reconcile to the cost Claude Code reported for the run; the worker's cost comes from its own usage record.</text>
    </svg>
    <figcaption><b>What caching makes cheap, and what it does not.</b> The bucket the hook targets, file content written to cache, is small in every bar: a file that enters context once costs a couple of cents. The bucket that grows is the one the hook never looks at, the whole conversation re-sent on every request at the cache-read rate, plus a round of thinking per request at fifty times that price. Six extra requests cost more than the file did. With caching, a file that enters context once is nearly free afterward. A turn is not.</figcaption>
  </figure>'''

# ---------- G: headline, three small multiples, three setups ----------
tgt = (O1['tgt_tokens_mean'][0], O1['tgt_tokens_mean'][1], O2['tgt_tokens_mean'][1])
rq = (O1['requests_mean'][0], O1['requests_mean'][1], O2['requests_mean'][1])
cst = (O1['cost_mean'][0], O1['cost_mean'][1], O2['cost_mean'][1])
pr = (O1['pass_rate'][0], O1['pass_rate'][1], O2['pass_rate'][1])
def panel(x, title, vals, fmt, w=72, gap=12, top=98, base=260):
    out = [f'<text x="{x}" y="76" font-weight="600">{title}</text>', f'<line x1="{x}" y1="{base}" x2="{x+3*w+2*gap}" y2="{base}" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>']
    m = max(vals)
    for k, (v, cls, name, op) in enumerate(zip(vals, ('stock','hook','hook'), ('stock','shipped','described'), (1, 0.55, 1))):
        h = (base - top) * v / m; bx = x + k*(w+gap)
        out.append(f'<rect x="{bx}" y="{base-h:.1f}" width="{w}" height="{h:.1f}" rx="4" class="{cls}" opacity="{op}"/><rect x="{bx}" y="{base-4}" width="{w}" height="4" class="{cls}" opacity="{op}"/>')
        out.append(f'<text x="{bx+w/2}" y="{base-h-6:.1f}" text-anchor="middle" class="small mono">{fmt.format(v)}</text>')
        out.append(f'<text x="{bx+w/2}" y="{base+16}" text-anchor="middle" class="small">{name}</text>')
    return '\n'.join(out)
tp1 = (1 - tgt[1]/tgt[0]) * 100; tp2 = (1 - tgt[2]/tgt[0]) * 100
cp1 = O1['cost_pct_of_means']; cp2 = O2['cost_pct_of_means']
figG = f'''<figure id="fig-headline">
    <span class="fig-n">Figure G · the result</span>
    <svg viewBox="0 0 900 330" role="img" aria-label="Three bar charts, stock against Spotify's hook as shipped and as described, means per run over 21 tasks and 189 runs. Target-file content in the main model's context: {tgt[0]:,.0f}, {tgt[1]:,.0f}, {tgt[2]:,.0f} tokens. API requests: {rq[0]:.1f}, {rq[1]:.1f}, {rq[2]:.1f}. Cost at list price: ${cst[0]:.3f}, ${cst[1]:.3f}, ${cst[2]:.3f}. Pass rates {pr[0]*100:.0f}%, {pr[1]*100:.0f}%, {pr[2]*100:.0f}%.">
      <text x="20" y="22" font-weight="600">Twenty-one tasks, three runs each: content in context fell {tp1:.0f}% and {tp2:.0f}%; the bill rose {cp1:.0f}% and {cp2:.0f}%</text>
      <text x="20" y="40" class="small">Means per run, same tasks, same model, same Kafka, 63 runs per setup, offline. Pass rate {pr[0]*100:.0f}% stock, {pr[1]*100:.0f}% as shipped, {pr[2]*100:.0f}% as described.</text>
{panel(40, 'Target-file tokens in main context', list(tgt), '{:,.0f}')}
{panel(340, 'API requests per run', list(rq), '{:.1f}')}
{panel(640, 'Cost per run, list price', list(cst), '${:.3f}')}
      <rect x="40" y="300" width="14" height="10" rx="2" class="stock"/><text x="60" y="309" class="small">stock, offline</text>
      <rect x="200" y="300" width="14" height="10" rx="2" class="hook" opacity="0.55"/><text x="220" y="309" class="small">Spotify's hook as shipped</text>
      <rect x="420" y="300" width="14" height="10" rx="2" class="hook"/><text x="440" y="309" class="small">as described, exception removed (worker cost included)</text>
    </svg>
    <figcaption><b>The result.</b> Both hook setups deliver Spotify's metric: less of the big file in the expensive model's context, {tp1:.0f}% less as shipped and {tp2:.0f}% less with the loophole closed, counted through every tool and not just Read. Both cost more than stock, {cp1:.0f}% and {cp2:.0f}%, because both add requests, and every request re-sends the conversation. Pass rates are within three points. The three charts share setups and nothing else; they are deliberately not one dual-axis chart. Detail per task is in the results tables.</figcaption>
  </figure>'''

# ---------- H: cost change by task type, both hook setups, paired, with intervals ----------
c1, c2 = S1['by_category'], S2['by_category']
rowsH = [("Spotify's four benchmark tasks", c1['SB'], c2['SB']), ('Needle: one fact in a big file', c1['ND'], c2['ND']),
         ("Spotify's shapes on files over 350 lines", c1['SC'], c2['SC']), ('Harm: precise edits, debugging, big files', c1['HM'], c2['HM']),
         ('Controls: small files', c1['CT'], c2['CT']), None,
         ('As described, the worker was called', None, S2['delegated_tasks']), ('As described, the model grepped instead', None, S2['grep_only_tasks'])]
x0, x1 = 330, 860; lo, hi = -50, 110
def X(v): return x0 + (min(max(v, lo), hi) - lo) / (hi - lo) * (x1 - x0)
svgH = [f'<line x1="{X(0):.0f}" y1="70" x2="{X(0):.0f}" y2="{70+len(rowsH)*56}" stroke="currentColor" stroke-width="0.8"/>']
for tick in (-50, -25, 0, 25, 50, 75, 100):
    svgH.append(f'<text x="{X(tick):.0f}" y="62" text-anchor="middle" class="small mono">{tick:+d}%</text>')
    if tick: svgH.append(f'<line x1="{X(tick):.0f}" y1="70" x2="{X(tick):.0f}" y2="{70+len(rowsH)*56}" stroke="currentColor" stroke-width="0.4" opacity="0.3"/>')
y = 92
def bar(g, yb, op):
    m = g['cost_pct_paired_mean']; ci = g['cost_pct_paired_ci']
    s = []
    if ci[0] is not None:
        s.append(f'<line x1="{X(ci[0]):.0f}" y1="{yb}" x2="{X(ci[1]):.0f}" y2="{yb}" stroke="currentColor" stroke-width="1.2" opacity="0.7"/>')
    s.append(f'<rect x="{min(X(0), X(m)):.0f}" y="{yb-7}" width="{max(abs(X(m)-X(0)),1):.0f}" height="14" rx="3" class="{"hook" if m > 0 else "stock"}" opacity="{op}"/>')
    edge = (max(ci[1], m) if ci[0] is not None else m) if m >= 0 else (min(ci[0], m) if ci[0] is not None else m)
    s.append(f'<text x="{X(edge) + (8 if m >= 0 else -8):.0f}" y="{yb+4}" text-anchor="{"start" if m >= 0 else "end"}" class="small mono" font-weight="600">{m:+.0f}%</text>')
    return '\n'.join(s)
for row in rowsH:
    if row is None:
        svgH.append(f'<line x1="20" y1="{y-14}" x2="880" y2="{y-14}" stroke="currentColor" stroke-width="0.6" opacity="0.4"/>'); y += 6; continue
    label, g1, g2 = row
    svgH.append(f'<text x="20" y="{y}" class="small" font-weight="600">{label}</text>')
    if g1:
        svgH.append(f'<text x="20" y="{y+14}" class="small">{g2["n_tasks"]} tasks · pass {g1["pass_rate"][0]*100:.0f} / {g1["pass_rate"][1]*100:.0f} / {g2["pass_rate"][1]*100:.0f}% · cheaper on {g1["hook_cheaper_tasks"]} and {g2["hook_cheaper_tasks"]} of {g2["n_tasks"]}</text>')
        svgH.append(bar(g1, y - 4, 0.55)); svgH.append(bar(g2, y + 14, 1.0))
    else:
        svgH.append(f'<text x="20" y="{y+14}" class="small">{g2["n_tasks"]} tasks, {g2["runs"][1]} runs · pass {g2["pass_rate"][0]*100:.0f} / {g2["pass_rate"][1]*100:.0f}% · cheaper on {g2["hook_cheaper_tasks"]} of {g2["n_tasks"]}</text>')
        svgH.append(bar(g2, y + 5, 1.0))
    y += 56
figH = f'''<figure id="fig-by-category">
    <span class="fig-n">Figure H · cost change by task type</span>
    <svg viewBox="0 0 900 {y+34}" role="img" aria-label="Horizontal bars of each hook setup's cost relative to stock by task type, paired per task with 95% bootstrap intervals. Spotify's four tasks: as shipped {c1['SB']['cost_pct_paired_mean']:+.0f}%, as described {c2['SB']['cost_pct_paired_mean']:+.0f}%. Needle reads {c1['ND']['cost_pct_paired_mean']:+.0f}% and {c2['ND']['cost_pct_paired_mean']:+.0f}%. Spotify's shapes on big files {c1['SC']['cost_pct_paired_mean']:+.0f}% and {c2['SC']['cost_pct_paired_mean']:+.0f}%. Harm {c1['HM']['cost_pct_paired_mean']:+.0f}% and {c2['HM']['cost_pct_paired_mean']:+.0f}%. Controls {c1['CT']['cost_pct_paired_mean']:+.0f}% and {c2['CT']['cost_pct_paired_mean']:+.0f}%. As described where the worker was called {S2['delegated_tasks']['cost_pct_paired_mean']:+.0f}%; where the model grepped instead {S2['grep_only_tasks']['cost_pct_paired_mean']:+.0f}%.">
      <text x="20" y="22" font-weight="600">Hook cost relative to stock, by task type · paired per task, mean of three runs each</text>
      <text x="20" y="40" class="small">Lighter bar: as shipped. Darker bar: as described. Line: 95% bootstrap interval over tasks. Worker cost included.</text>
{chr(10).join(svgH)}
      <rect x="20" y="{y+14}" width="14" height="10" rx="2" class="hook" opacity="0.55"/><text x="40" y="{y+23}" class="small">as shipped</text>
      <rect x="140" y="{y+14}" width="14" height="10" rx="2" class="hook"/><text x="160" y="{y+23}" class="small">as described</text>
    </svg>
    <figcaption><b>Where the bill moved.</b> Neither hook setup is uniformly more expensive. On the needle reads, the harm tasks and the controls the intervals span zero: where the hook rarely fires, the plugin is a wash. It costs more where it fires on Spotify's own task shapes at real file sizes. The split at the bottom is the mechanism: where the model called the worker, cost rose by half; where it grepped its way around the block, it rose by a quarter on average but was cheaper than stock on four of thirteen tasks, the ones where the answer is a small part of the file.</figcaption>
  </figure>'''

lede = '<p class="lede">In post order. A: the mechanism. B: the setup. C: the call-out on the rule that makes the shipped hook a suggestion. D, E, F: one task traced under all three setups, then as bars, then in cents. G: the headline across twenty-one tasks. H: the same bill split by task type. Three setups throughout: stock, Spotify\'s hook as shipped, and as described.</p>'
page = head + '<main>\n  <h1>Figures for "Tokens Are Cheap, Turns Are Not"</h1>\n  ' + lede + '\n\n  ' + '\n  '.join([figA, figB, figC, figD, figE, figF, figG, figH]) + '\n</main>\n'
open(os.path.join(HERE, 'post-figures.html'), 'w').write(page)
print('E stats', stats); print('F buckets', [[round(v,1) for v in b] for b in B]); print('G', tgt, rq, cst, pr)
