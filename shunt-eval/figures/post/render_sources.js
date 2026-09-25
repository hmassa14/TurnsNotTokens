// Screenshot the standalone figure pages in sources/ (triangle and the three tables).
// SCALE=4 OUT=hires node render_sources.js renders large copies.
const fs = require('fs'), path = require('path');
const { chromium } = require(path.join(require('child_process').execSync('npm root -g').toString().trim(), 'playwright'));
const SCALE = +(process.env.SCALE || 2), OUT = process.env.OUT || '.';
const names = ['B-evaluation-triangle', 'table-kafka-vs-backstage', 'table-token-comparison', 'table-by-category'];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const pg = await b.newPage({ viewport: { width: 900, height: 600 }, deviceScaleFactor: SCALE });
  for (const name of names) {
    await pg.goto('file://' + path.resolve(__dirname, 'sources', `${name}.html`), { waitUntil: 'networkidle' });
    await (await pg.$('figure')).screenshot({ path: path.join(OUT, `${name}.png`) });
    console.log(name);
  }
  await b.close();
})();
