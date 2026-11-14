// usage: node render.js [in.html out.pdf]   (defaults: the cake cards)
const { chromium } = require('playwright');
(async () => {
  const [inp, out] = process.argv.length > 3 ? [process.argv[2], process.argv[3]] : ['cards.html', 'carly-cakes-cards.pdf'];
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + process.cwd() + '/' + inp, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  console.log('fonts loaded:', [...new Set(await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family)))].join(', '));
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
