const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + process.cwd() + '/cards.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const fonts = await p.evaluate(() => [...document.fonts].filter(f => f.status === 'loaded').map(f => f.family));
  console.log('fonts loaded:', [...new Set(fonts)].join(', '));
  await p.pdf({ path: 'crumb-coat-cards.pdf', format: 'A4', printBackground: true, preferCSSPageSize: true });
  await b.close();
})();
