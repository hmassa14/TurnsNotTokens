// Short-post variants of Figures G and F: relettered C and D, with subtitles that stand on their own.
const fs = require('fs');
const { chromium } = require(require('path').join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'));
const src = fs.readFileSync('post-figures.html', 'utf8');
const head = src.slice(0, src.indexOf('<main>'));
const pick = id => { const m = src.match(new RegExp(`<figure id="${id}">[\\s\\S]*?</figure>`)); if (!m) throw new Error(id); return m[0]; };
const swap = (s, a, b) => { if (!s.includes(a)) throw new Error('missing: ' + a); return s.replace(a, b); };
let C = pick('fig-headline');
C = swap(C, 'Figure G · the result', 'Figure C · the result');
C = C.replace(/content in context fell (\d+)% and (\d+)%; the bill rose (\d+)% and (\d+)%/, 'less of the big file reached the model (−$1%, −$2%), but the bill rose (+$3%, +$4%)');
let D = pick('fig-money');
D = swap(D, 'Figure F · where the money went', 'Figure D · where the money went');
D = swap(D, 'Same three runs as Figures D and E.', 'One question, three setups: how does the broker lifecycle manager move between states?');
C = swap(C, ' The three charts share setups and nothing else; they are deliberately not one dual-axis chart. Detail per task is in the results tables.', '');
D = D.replace(/>[ABC] · (stock|as shipped|as described)</g, '>$1<');
D = D.replace(/<figcaption><b>What caching makes cheap[\s\S]*?<\/figcaption>/, '');
if (D.includes('fifty times')) throw new Error('D note not removed');
const out = [['short-C-headline', C], ['short-D-where-the-money-went', D]];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const pg = await b.newPage({ viewport: { width: 1000, height: 600 }, deviceScaleFactor: 2 });
  for (const [name, fig] of out) {
    const html = '<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#F5F6F3}</style>' + head + '</head><body><main>' + fig + '</main></body></html>';
    await pg.setContent(html, { waitUntil: 'networkidle' });
    await (await pg.$('figure')).screenshot({ path: `${name}.png` });
    console.log(name);
  }
  await b.close();
})();
