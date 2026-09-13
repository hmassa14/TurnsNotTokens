"""Assemble post-figures.html (two-arm version) from the v1 head, hand SVG, generated bars and storyboard fragments."""
import json, re
v1 = open('post-figures-v1-five-arms.html').read()
head = v1[:v1.index('<main>')]
figA = v1[v1.index('<figure>'):v1.index('</figure>')+9]  # Figure A block

# ---------- A: reorder the three exits ----------
old_strip = figA[figA.index('<!-- three columns'):figA.index('</svg>')]
new_strip = '''<!-- three columns: x = 30, 320, 610 ; width 250 -->
      <rect x="30" y="358" width="250" height="52" rx="6" class="box dim" stroke-dasharray="5 4"/>
      <text x="155" y="379" text-anchor="middle" font-weight="600" class="dim">Spotify's worker script</text>
      <text x="155" y="396" text-anchor="middle" class="small">bulk-read → Haiku reads the file → summary</text>
      <text x="155" y="428" text-anchor="middle" class="small mono">0 of 12 runs</text>
      <text x="155" y="443" text-anchor="middle" class="small">what the design assumes</text>

      <rect x="320" y="358" width="250" height="52" rx="6" class="box hook-s" stroke-width="1.6"/>
      <text x="445" y="379" text-anchor="middle" font-weight="600">Grep(pattern, file)</text>
      <text x="445" y="396" text-anchor="middle" class="small">never blocked; matching lines enter context</text>
      <text x="445" y="428" text-anchor="middle" class="small mono">every run</text>
      <text x="445" y="443" text-anchor="middle" class="small">what happened</text>

      <rect x="610" y="358" width="250" height="52" rx="6" class="box dim" stroke-dasharray="5 4"/>
      <text x="735" y="379" text-anchor="middle" font-weight="600" class="dim">Read(file, offset, limit)</text>
      <text x="735" y="396" text-anchor="middle" class="small">the published hook lets this through</text>
      <text x="735" y="428" text-anchor="middle" class="small mono">9 of 9 blocks, before the fix</text>
      <text x="735" y="443" text-anchor="middle" class="small">closed for this test (see call-out)</text>
    '''
figA = figA.replace(old_strip, new_strip)
figA = figA.replace('the three routes the model took after a block: Spotify\'s worker, never; a paged read, every block under the shipped hook; grep, every run under the strict hook.',
                    'what the model did after a block: never Spotify\'s worker; grep in every run with the hook enforced; and, before the exception was closed, a paged read on every block.')
figA = re.sub(r'<figcaption>.*?</figcaption>', '<figcaption><b>Where the hook sits, and the way out.</b> A PreToolUse hook runs between the model\'s tool call and the tool. On allow, the file comes back whole. On block, only the hook\'s message comes back, and the model chooses its next call. Spotify\'s design assumes that choice is the worker script. In twelve tasks it never was: the model grepped the file instead, a few hundred lines at a time. The right-hand exit, a read with an offset, is the one the published hook leaves open; we closed it so the hook would do what the post describes.</figcaption>', figA, flags=re.S)

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
      <text x="20" y="356" class="small">Twelve tasks on Kafka, each asked as a developer would (no file path given), one run per arm per task, Sonnet 5 as the main model, Haiku as the worker.</text>
    </svg>
    <figcaption><b>The setup.</b> Every run starts from an untouched Kafka checkout and a fresh headless session; nothing carries over. Two folders. Stock is Claude Code as installed. The hook arm is Spotify's published plugin with its Portal call pointed at Haiku and one rule removed, so that a file over 350 lines cannot be read by the expensive model at all.</figcaption>
  </figure>'''

# ---------- C: the call-out storyboard ----------
sc = open('story_callout.html').read().replace('<div class="sb">','').rsplit('</div>',1)[0]
figC = f'''<figure id="fig-callout">
    <span class="fig-n">Figure C · call-out: the rule we removed, and why</span>
    <p class="small" style="margin:0 0 10px;color:var(--ink-2)">R1 under Spotify's hook exactly as published, requests 4 to 6 of 11. The blocked read is followed by a read with an offset, which the published hook allows.</p>
<div class="sb">{sc}</div>
    <figcaption><b>Why the test uses a stricter hook than the one Spotify shipped.</b> The published hook has an exception: a Read with an offset or limit is allowed, so the model can page through a big file after being refused it. In our pilot it did exactly that on every block, nine of nine, and 655 of the 770 lines ended up in context anyway. That is not the design the post describes, so we deleted the exception. Everything after this figure is measured with the exception closed.</figcaption>
  </figure>'''

# ---------- D: main storyboard ----------
sm = open('story_main.html').read().replace('<div class="sb">','').rsplit('</div>',1)[0]
sm = sm.replace('and refused the read. The model got this instead of the file:', 'and refused the read; in this arm a paged read is refused too. The model got this instead of the file:')
figD = f'''<figure id="fig-story">
    <span class="fig-n">Figure D · one question, request by request</span>
    <p class="small" style="margin:0 0 10px;color:var(--ink-2)">R1, "how does the broker lifecycle manager move between states?" Stock, request 2 of 3; then with the hook, requests 4, 5, 10, 11 and 15 of 16. Each numbered row is one API request: what the model was given, what it decided, what came back.</p>
<div class="sb">{sm}</div>
    <figcaption><b>What the model does when it cannot read the file.</b> Stock found the file with one grep and read it whole on its second request; the answer came on the third. With the hook, the same read was refused and the model received one sentence naming the bulk-reader. It did not call the bulk-reader. It grepped the file ten times, twice with the pattern <code>.</code> and an offset, which is a paged read through a different tool, then read the small <code>BrokerState.java</code> and answered. Correct answer both times: 3 requests against 16.</figcaption>
  </figure>'''

# ---------- E: bars, generated from the transcripts ----------
def reqs(d):
    tp = json.load(open(d + '/transcript_parsed.json'))
    rs = sorted(tp['requests'], key=lambda r: r['first_ts'] or '')
    tools = {t['request_id']: t for t in tp['tool_calls'] if t.get('agent', 'main') == 'main'}
    return [(r['usage'], tools.get(r['request_id'])) for r in rs]
R = '/home/user/WackyWords/shunt-eval/results/'
stock = reqs(R + '03-natural-three-arms/R1-stock')
strict = reqs(R + '04-natural-strict-arms/R1-shunt-strict')
def sent(u): return u.get('cache_read_input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('input_tokens', 0)
maxt = max(sent(u) for u, _ in stock + strict)
scale = 130 / maxt
def lab(t, u):
    if t is None: return ('answer', f"{u.get('output_tokens',0)/1000:.1f}k out")
    n, i = t['name'], t['input']
    if n == 'Read':
        if 'hook_blocked' in t.get('flags', []): return ('Read', '0 lines')
        if 'offset' in i: return ('Read', f"{i['offset']}+{i.get('limit','')}")
        return ('Read', f"{t.get('result_lines',0)} ln")
    if n == 'Grep':
        p = str(i.get('pattern', ''))
        c = t.get('result_chars', 0)
        return ('Grep', '"."' if p == '.' else (f'{c/1000:.0f}k' if c >= 1000 else str(c)))
    if n == 'Bash': return ('Bash', i.get('command','')[:4].strip())
    if n == 'Glob': return ('Glob', '')
    return (n, '')
def lane(rows, y0, x0, step, w, cls, mark_blocked=True, topn=()):
    out = []
    for k, (u, t) in enumerate(rows):
        h = sent(u) * scale; x = x0 + k * step; cx = x + w / 2
        out.append(f'<rect x="{x:.1f}" y="{y0-h:.1f}" width="{w}" height="{h:.1f}" rx="3" class="{cls}" opacity="0.85"/>')
        if t and 'hook_blocked' in t.get('flags', []):
            out.append(f'<rect x="{x:.1f}" y="{y0-h:.1f}" width="{w}" height="{h:.1f}" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/>')
            out.append(f'<text x="{cx:.1f}" y="{y0-h-22:.0f}" text-anchor="middle" class="small" font-weight="600">blocked</text>')
        if k in topn:
            out.append(f'<text x="{cx:.1f}" y="{y0-h-7:.0f}" text-anchor="middle" class="small mono">{sent(u)/1000:.0f}k</text>')
        a, b = lab(t, u)
        out.append(f'<text x="{cx:.1f}" y="{y0+16}" text-anchor="middle" class="small">{a}</text>')
        if b: out.append(f'<text x="{cx:.1f}" y="{y0+30}" text-anchor="middle" class="small mono">{b}</text>')
    return '\n'.join(out)
st_cr = sum(u.get('cache_read_input_tokens',0) for u,_ in stock); st_out = sum(u.get('output_tokens',0) for u,_ in stock)
sh_cr = sum(u.get('cache_read_input_tokens',0) for u,_ in strict); sh_out = sum(u.get('output_tokens',0) for u,_ in strict)
grep_chars = sum(t.get('result_chars',0) for u,t in strict[4:13] if t and t['name']=='Grep')
figE = f'''<figure id="fig-bars">
    <span class="fig-n">Figure E · the same question as bars</span>
    <svg viewBox="0 0 900 600" role="img" aria-label="Two request-by-request traces of the R1 task. Stock: three API requests, each re-sending about thirty thousand cached tokens, {st_cr:,} cache-read tokens in total, 11 cents. With the hook enforced: sixteen requests, the fourth blocked, followed by ten greps, a glob and a read of a small file; context grows from 30 to 49 thousand tokens per request, {sh_cr:,} cache-read tokens in total, 28 cents.">
      <text x="20" y="22" font-weight="600">R1: "how does the broker lifecycle manager move between states?"  ·  770-line file  ·  Sonnet 5</text>
      <text x="20" y="40" class="small">Each bar is one API request; its height is everything sent to the model, almost all of it read from cache. Under each bar: the tool call made next, and what it returned.</text>
      <text x="20" y="80" font-weight="600" fill="var(--stock)">A · stock</text>
      <text x="20" y="96" class="small">3 requests · {st_cr:,} cached tokens re-sent · {st_out:,} output tokens · $0.113</text>
      <line x1="60" y1="240" x2="880" y2="240" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
{lane(stock, 240, 70, 100, 46, 'stock', topn=(0,1,2))}
      <rect x="270" y="{240-sent(stock[2][0])*scale:.1f}" width="46" height="{13383*scale:.1f}" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 2"/>
      <text x="330" y="140" class="small">← the file, 13.4k tokens, written to cache once (3.3¢)</text>
      <text x="330" y="200" class="small">everything else is re-read from cache at a tenth of the input price</text>
      <text x="20" y="330" font-weight="600" fill="var(--hook)">B · Spotify's hook, enforced</text>
      <text x="20" y="346" class="small">16 requests · {sh_cr:,} cached tokens re-sent · {sh_out:,} output tokens · $0.285</text>
      <line x1="60" y1="490" x2="880" y2="490" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>
{lane(strict, 490, 66, 51, 36, 'hook', topn=(0,15))}
      <path d="M{66+4*51} 540 L{66+4*51} 546 L{66+12*51+36} 546 L{66+12*51+36} 540" fill="none" stroke="currentColor" stroke-width="0.8"/>
      <text x="{66+8*51+18}" y="560" text-anchor="middle" class="small">nine greps returned {grep_chars/1000:.0f}k characters of a 36k-character file, in pieces, each re-sent on every request after it</text>
    </svg>
    <figcaption><b>The same question, request by request.</b> Stock read the file once and answered on the third request. With the hook, the fourth request's read was refused; the model then pulled the file out with grep, a few hundred lines at a time, over nine more requests, each re-sending everything before it. Cached tokens re-sent went from {st_cr//1000}k to {sh_cr//1000}k and output tokens from {st_out/1000:.1f}k to {sh_out/1000:.1f}k. Both answers were correct. Data from the transcripts in <code>results/03-natural-three-arms</code> and <code>results/04-natural-strict-arms</code>.</figcaption>
  </figure>'''

# ---------- F: where the money went ----------
def buckets(rows):
    first = rows[0][0]
    sys_w = first.get('cache_creation_input_tokens',0); rest_w = sum(u.get('cache_creation_input_tokens',0) for u,_ in rows[1:])
    cr = sum(u.get('cache_read_input_tokens',0) for u,_ in rows); out = sum(u.get('output_tokens',0) for u,_ in rows)
    return sys_w, rest_w, cr, out
s_sys, s_rest, s_cr, s_out = buckets(stock); h_sys, h_rest, h_cr, h_out = buckets(strict)
# cents: stock tool results were billed at the 5-minute rate (2.5), the strict run's at the 1-hour rate (4.0); both reconcile to result.json
S = [s_sys*4/1e4, s_rest*2.5/1e4, s_cr*0.2/1e4, s_out*10/1e4]
H = [h_sys*4/1e4, h_rest*4/1e4, h_cr*0.2/1e4, h_out*10/1e4]
px = 8.0; base = 330
def stack(vals, x, cls):
    out = []; y = base; ops = [0.35, 0.6, 0.85, 1.0]; ys = []
    for v, op in zip(vals, ops):
        h = v * px; y -= h
        out.append(f'<rect x="{x}" y="{y:.1f}" width="80" height="{h-2:.1f}" class="{cls}" opacity="{op}"/>')
        out.append(f'<text x="{x+40}" y="{y+h/2+4:.1f}" text-anchor="middle" class="small mono">{v:.1f}</text>')
        ys.append(y + h/2)
    return '\n'.join(out), ys
stS, _ = stack(S, 90, 'stock'); stH, ysH = stack(H, 290, 'hook')
leg = [("system prompt and tools, written to cache once", None),
       ("grep results and the small file, written to cache once", "about as many characters as the whole file would have been"),
       ("the whole conversation re-sent on every request, at the cache-read rate", "3 requests of ~30k tokens vs 16 requests of 30k to 49k"),
       ("output: thinking and the answer, at the output rate", "sixteen rounds of thinking instead of three")]
legsvg = []
for (a, b), y in zip(leg, ysH):
    legsvg.append(f'<line x1="372" y1="{y:.0f}" x2="392" y2="{y:.0f}" stroke="currentColor" stroke-width="0.6" opacity="0.5"/>')
    if b:
        legsvg.append(f'<text x="398" y="{y-4:.0f}" class="small" font-weight="600">{a}</text><text x="398" y="{y+12:.0f}" class="small">{b}</text>')
    else:
        legsvg.append(f'<text x="398" y="{y+4:.0f}" class="small">{a}</text>')
d = [h-s for h, s in zip(H, S)]
figF = f'''<figure id="fig-money">
    <span class="fig-n">Figure F · where the money went</span>
    <svg viewBox="0 0 900 430" role="img" aria-label="Cost breakdown of the two R1 runs in cents, stacked by price bucket. Stock: {S[0]:.1f} cents system prompt, {S[1]:.1f} cents file written to cache, {S[2]:.1f} cents cache re-reads, {S[3]:.1f} cents output, {sum(S):.1f} total. Hook: {H[0]:.1f}, {H[1]:.1f}, {H[2]:.1f}, {H[3]:.1f}, total {sum(H):.1f}. The bucket that grew most is the conversation re-sent on every request.">
      <text x="20" y="22" font-weight="600">Where the money went, R1, in cents at Sonnet 5 list price</text>
      <text x="20" y="40" class="small">Same two runs as Figures D and E. Each bar is the run's total cost, stacked by what the tokens were billed as.</text>
      <text x="130" y="82" text-anchor="middle" font-weight="600" fill="var(--stock)">A · stock</text>
      <text x="130" y="98" text-anchor="middle" class="small mono">{sum(S):.1f}¢ · 3 requests</text>
{stS}
      <text x="330" y="82" text-anchor="middle" font-weight="600" fill="var(--hook)">B · Spotify's hook, enforced</text>
      <text x="330" y="98" text-anchor="middle" class="small mono">{sum(H):.1f}¢ · 16 requests</text>
{stH}
      <line x1="70" y1="{base}" x2="400" y2="{base}" stroke="currentColor" stroke-width="0.8"/>
{chr(10).join(legsvg)}
      <line x1="70" y1="356" x2="880" y2="356" stroke="currentColor" stroke-width="0.6" opacity="0.4"/>
      <text x="70" y="378"><tspan font-weight="600">The read the hook refused would have cost 3.3¢.</tspan><tspan class="small"> Working around it added {d[1]:.1f}¢ of cache writes, {d[2]:.1f}¢ of re-sends and {d[3]:.1f}¢ of output.</tspan></text>
      <text x="70" y="400" class="small mono">Sonnet 5 per million tokens · input $2.00 · cache write $2.50 (5 min) / $4.00 (1 h) · cache read $0.20 · output $10.00</text>
      <text x="70" y="416" class="small">Claude Code wrote the stock run's tool results at the 5-minute rate and the hook run's at the 1-hour rate; both bars reconcile to the cost the CLI reported.</text>
    </svg>
    <figcaption><b>What caching makes cheap, and what it does not.</b> The bucket the hook targets, file content written to cache, went up, not down: the grep results add up to about as much text as the file. But the bucket that grew most is the one the hook never looks at. Every request re-sends the entire conversation. Re-reads are cheap per token, a fifth of a cent per thousand, but sixteen of them at 30k to 49k tokens each cost seven times what three did, and every request ends in fresh thinking at fifty times that price. With caching, a file that enters context once is nearly free afterward. A turn is not.</figcaption>
  </figure>'''

# ---------- G: headline, three small multiples, two arms ----------
def panel(x, title, vals, fmt, w=110, gap=20, top=98, base=260):
    out = [f'<text x="{x}" y="76" font-weight="600">{title}</text>', f'<line x1="{x}" y1="{base}" x2="{x+2*w+gap}" y2="{base}" stroke="currentColor" stroke-width="0.8" opacity="0.5"/>']
    m = max(vals)
    for k, (v, cls, name) in enumerate(zip(vals, ('stock','hook'), ('A stock','B hook'))):
        h = (base - top) * v / m; bx = x + k*(w+gap)
        out.append(f'<rect x="{bx}" y="{base-h:.1f}" width="{w}" height="{h:.1f}" rx="4" class="{cls}"/><rect x="{bx}" y="{base-4}" width="{w}" height="4" class="{cls}"/>')
        out.append(f'<text x="{bx+w/2}" y="{base-h-6:.1f}" text-anchor="middle" class="small mono">{fmt.format(v)}</text>')
        out.append(f'<text x="{bx+w/2}" y="{base+16}" text-anchor="middle" class="small">{name}</text>')
    return '\n'.join(out)
figG = f'''<figure id="fig-headline">
    <span class="fig-n">Figure G · the result</span>
    <svg viewBox="0 0 900 330" role="img" aria-label="Three bar charts, stock against the enforced hook, over twelve tasks. Target-file lines in the main model's context: 7,111 against 893. API requests: 82 against 132. Cost at list price: $1.94 against $2.61. Pass rate 11 of 12 against 12 of 12.">
      <text x="20" y="22" font-weight="600">Twelve tasks: the metric Spotify reported fell 87%, the bill rose 35%</text>
      <text x="20" y="40" class="small">Same tasks, same model, same Kafka, one run per cell. Stock passed 11 of 12, the hook 12 of 12.</text>
{panel(40, 'Target-file lines in main context', [7111, 893], '{:,}')}
{panel(340, 'API requests', [82, 132], '{:,}')}
{panel(640, 'Cost, list price', [1.94, 2.61], '${:.2f}')}
      <rect x="40" y="300" width="14" height="10" rx="2" class="stock"/><text x="60" y="309" class="small">stock Claude Code</text>
      <rect x="200" y="300" width="14" height="10" rx="2" class="hook"/><text x="220" y="309" class="small">with Spotify's hook, enforced</text>
    </svg>
    <figcaption><b>The result.</b> The hook did what the post promised on the post's own metric: 87% fewer target-file lines in the expensive model's context. It did so by turning reads into greps, which added fifty API requests across the twelve tasks, and the bill went up 35% for the same pass rate. The three charts share arms and nothing else; they are deliberately not one dual-axis chart. Detail per task is in the results tables.</figcaption>
  </figure>'''

lede = '<p class="lede">In post order. A: the mechanism. B: the setup. C: the call-out on the rule we removed. D, E, F: one task traced, then as bars, then in cents. G: the headline across twelve tasks. Two arms throughout: stock, and Spotify\'s hook with its exception closed.</p>'
page = head + '<main>\n  <h1>Figures for "Tokens Are Cheap, Turns Are Not"</h1>\n  ' + lede + '\n\n  ' + '\n  '.join([figA, figB, figC, figD, figE, figF, figG]) + '\n</main>\n'
open('post-figures.html', 'w').write(page)
print('stock buckets', [round(v,1) for v in S], round(sum(S),1)); print('hook buckets', [round(v,1) for v in H], round(sum(H),1)); print('grep chars', grep_chars, 'maxt', maxt)
