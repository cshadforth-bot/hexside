// Builds the print-and-play PDFs with the Chromium that ships with Playwright.  Usage: node build-pdfs.js
// Output: pdf/textilesme-cards.pdf (4 pages), pdf/textilesme-rules.pdf (2 pages), pdf/textilesme-print-and-play.pdf (6 pages).
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs'); const { execFileSync } = require('child_process');
(async () => {
  const dir = __dirname, out = path.join(dir, 'pdf'); fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch();
  // 1. Render each card to a 320 dpi PNG (63 mm at 320 dpi is 794 px; the card art is 252 px wide).
  //    Live SVG fabric patterns balloon the PDF to hundreds of MB, so the cards go in as images.
  fs.mkdirSync(path.join(dir, 'img'), { recursive: true });
  const cp = await b.newPage({ viewport: { width: 1130, height: 900 }, deviceScaleFactor: 794 / 252 });
  await cp.goto('file://' + path.join(dir, 'cards.html'), { waitUntil: 'networkidle' }); await cp.evaluate(() => document.fonts.ready);
  const els = await cp.$$('.c');
  for (let i = 0; i < els.length; i++) await els[i].screenshot({ path: path.join(dir, 'img', i === 18 ? 'back.png' : String(i + 1).padStart(2, '0') + '.png'), omitBackground: true });
  await cp.close();
  // 2. Lay them out on A4 and print. The rules sheet is plain HTML and stays small.
  for (const [src, dst] of [['print-cards.html', 'textilesme-cards.pdf'], ['print-rules.html', 'textilesme-rules.pdf']]) {
    const p = await b.newPage(); p.on('pageerror', e => console.log('ERR', src, e.message));
    await p.goto('file://' + path.join(dir, src), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
    await p.pdf({ path: path.join(out, dst), preferCSSPageSize: true, printBackground: true }); await p.close();
  }
  await b.close();
  execFileSync('python3', ['-c', `from pypdf import PdfWriter\nw=PdfWriter()\nfor f in ['textilesme-rules.pdf','textilesme-cards.pdf']: w.append('${out}/'+f)\nw.write('${out}/textilesme-print-and-play.pdf')`]);
  console.log('built', fs.readdirSync(out));
})();
