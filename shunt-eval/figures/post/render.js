// Split post-figures.html into one standalone page per figure and screenshot each at 2x, full height.
const fs = require('fs');
const { chromium } = require(require('path').join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'));
const src = fs.readFileSync('post-figures.html', 'utf8');
const head = src.slice(0, src.indexOf('<main>'));
const figs = src.match(/<figure[^>]*>[\s\S]*?<\/figure>/g);
const names = ['A-hook-in-the-loop','B-setup','C-callout-published-hook','D-one-question-request-by-request','E-requests-as-bars','F-where-the-money-went','G-headline'];
if (figs.length !== names.length) throw new Error(`${figs.length} figures vs ${names.length} names`);
(async () => {
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 1000, height: 600 }, deviceScaleFactor: 2 });
  for (let i = 0; i < figs.length; i++) {
    const html = '<!doctype html><html><head><meta charset="utf-8"><style>body{margin:0;background:#F5F6F3}</style>' + head + '</head><body><main>' + figs[i] + '</main></body></html>';
    fs.writeFileSync(`post_${names[i]}.html`, html);
    await pg.setContent(html, { waitUntil: 'networkidle' });
    await (await pg.$('figure')).screenshot({ path: `post_${names[i]}.png` });
    console.log(names[i]);
  }
  await b.close();
})();
