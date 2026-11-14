// Textilesme simulator. Usage: node sim.js [games]   Rules are in RULES.md; this file is a test of them, not the authority.
const { CARDS } = require('./data.js');
const rnd = n => Math.floor(Math.random() * n);
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = rnd(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; };

function newGame(opt) {
  const deck = shuffle(CARDS.map((c, i) => ({ ...c, id: i, recycled: false })));
  const g = { opt, deck, counter: [], scrap: [], day: 1, turns: 0, log: { eff: {}, fin: [0, 0], bonus: 0, finBySize: { 2: 0, 3: 0, 4: 0 } },
    pl: [0, 1].map(() => ({ open: [], done: [], stash: [], pts: 0, pen: 0 })), cur: 0, ended: false };
  g.pl.forEach(p => p.open.push({ t: deck.pop(), layers: [], cards: [] })); // starting ticket
  g.pl.forEach(p => { p.open[0].layers.push(p.open[0].t.recipe[0]); });
  if (opt.solo) g.pl.length = 1;
  fill(g); return g;
}
const cSize = g => g.opt.solo ? 3 : 4;
function fill(g) { while (g.counter.length < cSize(g) && g.deck.length) g.counter.push(g.deck.pop()); }
const need = gm => gm.t.recipe[gm.layers.length];
const canStitch = (gm, c) => need(gm) && (c.recipe[0] === need(gm) || c.bottom === need(gm));

// ---- options for one card
function options(g, p, card) {
  const o = [];
  p.open.forEach((gm, i) => { if (canStitch(gm, card)) o.push({ k: 'stitch', gi: i, card }); });
  if (p.open.length < 2) o.push({ k: 'design', card });
  o.push({ k: 'scrap', card });
  return o;
}
function value(g, p, o, skill) {
  const rival = g.pl[1 - g.cur];
  if (o.k === 'stitch') { const gm = p.open[o.gi]; const done = gm.layers.length + 1 === gm.t.recipe.length; return done ? 100 + gm.t.pts : 20 + gm.layers.length * 3 + gm.t.pts; }
  if (o.k === 'design') { // worth more if the Counter already holds what it needs next
    const f = o.card.recipe[1]; const supply = g.counter.filter(c => c !== o.card && (c.recipe[0] === f || c.bottom === f)).length;
    return 6 + o.card.pts * 0.6 + supply * 2 + (o.card.recycled && g.opt.bonus ? 1 : 0);
  }
  // scrap: denial. Is the rival one card from finishing with this?
  let d = 0; if (rival) rival.open.forEach(gm => { if (canStitch(gm, o.card)) d = Math.max(d, gm.layers.length + 1 === gm.t.recipe.length ? 60 : 5); });
  return 1 + d;
}
function chooseTurn(g, p, skill) {
  const all = g.counter.flatMap(c => options(g, p, c)); if (!all.length) return null;
  if (Math.random() < skill.eps) return all[rnd(all.length)];
  let best = null, bv = -1e9; for (const o of all) { const v = value(g, p, o) + Math.random() * 0.01; if (v > bv) { bv = v; best = o; } } return best;
}

// ---- executing
function use(g, p, o, depth = 0) {
  g.turns += depth ? 0 : 1;
  g.counter.splice(g.counter.indexOf(o.card), 1);
  if (o.k === 'scrap') { g.scrap.push(o.card); return; }
  if (o.k === 'design') { const gm = { t: o.card, layers: [o.card.recipe[0]], cards: [] }; p.open.push(gm); return; }
  const gm = p.open[o.gi]; gm.layers.push(need(gm)); gm.cards.push(o.card);
  if (gm.layers.length === gm.t.recipe.length) finish(g, p, gm, depth);
}
function finish(g, p, gm, depth) {
  p.open.splice(p.open.indexOf(gm), 1);
  const bonus = g.opt.bonus ? [gm.t, ...gm.cards].filter(c => c.recycled).length : 0;
  p.pts += gm.t.pts + bonus; g.log.bonus += bonus; p.done.push(gm.t); g.log.fin[g.pl.indexOf(p)]++; g.log.finBySize[gm.t.recipe.length]++;
  const ef = gm.t.effect; g.log.eff[ef] = (g.log.eff[ef] || 0) + 1;
  let recycled = gm.cards.slice();
  if (ef === 'stash' && recycled.length) { p.stash.push(recycled.pop()); }
  recycled.forEach(c => { c.recycled = true; g.scrap.push(c); }); // washing-up pile: layer cards go to the scrap bin, marked recycled
  fill(g);
  if (ef === 'again' && g.counter.length) { const o = chooseTurn(g, p, g.skills[g.pl.indexOf(p)]); if (o) use(g, p, o, depth + 1); }
  if (ef === 'draw' && g.deck.length) { const c = g.deck.pop(); g.counter.push(c); const o = chooseTurn(g, p, g.skills[g.pl.indexOf(p)]); if (o && o.card === c) use(g, p, o, depth + 1); else g.counter.splice(g.counter.indexOf(c), 1), g.scrap.push(c); }
  if (ef === 'fresh') { g.scrap.push(...g.counter); g.counter = []; fill(g); }
  if (ef === 'moth' && !g.opt.solo) { const r = g.pl[1 - g.pl.indexOf(p)]; const t = r.open.filter(x => x.cards.length).sort((a, b) => b.cards.length - a.cards.length)[0]; if (t) { const c = t.cards.pop(); t.layers.pop(); g.scrap.push(c); } }
}
function washUp(g) {
  g.pl.forEach(p => { p.pen += p.open.length; p.open.forEach(gm => { g.scrap.push(...gm.cards); g.scrap.push(gm.t); }); p.open = []; });
  if (g.opt.resale) g.pl.forEach(p => { g.scrap.push(...p.done); p.done = []; }); // finished garments are resold: they re-enter the deck, points already banked
  g.scrap.forEach(c => c.recycled = true);
}
function playGame(opt, skills) {
  const g = newGame(opt); g.skills = skills;
  for (g.day = 1; g.day <= 2; g.day++) {
    if (g.day === 2) { washUp(g); g.deck = shuffle(g.scrap); g.scrap = []; g.counter = []; fill(g); g.pl.forEach(p => { if (!p.open.length && g.deck.length) { const t = g.deck.pop(); p.open.push({ t, layers: [t.recipe[0]], cards: [] }); } }); }
    g.cur = g.day === 2 && !opt.solo ? 1 : 0;
    let guard = 0;
    while (g.counter.length && guard++ < 400) {
      const p = g.pl[g.cur]; const o = chooseTurn(g, p, skills[g.cur]);
      if (!o) break; // no legal action cannot happen (scrap is always legal)
      use(g, p, o);
      if (opt.solo && g.counter.length) g.counter.shift(); // solo: the oldest Counter card goes cold and leaves the game
      fill(g);
      if (!opt.solo) g.cur = 1 - g.cur;
    }
  }
  washUp(g);
  g.pl.forEach(p => p.score = p.pts + p.stash.length - p.pen);
  return g;
}

// ---- reports
const N = +process.argv[2] || 4000;
const SK = { strong: { eps: 0 }, casual: { eps: 0.35 } };
const pct = (a, q) => a[Math.floor(q * (a.length - 1))];
function versus(label, opt, s1, s2) {
  let w = [0, 0], t = 0, sc = [[], []], fin = [0, 0], turns = 0, bonus = 0, sz = { 2: 0, 3: 0, 4: 0 }, eff = {};
  for (let i = 0; i < N; i++) {
    const g = playGame(opt, [SK[s1], SK[s2]]); const [a, b] = g.pl.map(p => p.score);
    if (a > b) w[0]++; else if (b > a) w[1]++; else t++; sc[0].push(a); sc[1].push(b); fin[0] += g.log.fin[0]; fin[1] += g.log.fin[1]; turns += g.turns; bonus += g.log.bonus;
    for (const k in g.log.finBySize) sz[k] += g.log.finBySize[k]; for (const k in g.log.eff) eff[k] = (eff[k] || 0) + g.log.eff[k];
  }
  const m = x => (x.reduce((a, b) => a + b) / x.length).toFixed(1);
  console.log(`${label}: P1 ${(100 * w[0] / N).toFixed(1)}%  P2 ${(100 * w[1] / N).toFixed(1)}%  tie ${(100 * t / N).toFixed(1)}% | mean ${m(sc[0])}/${m(sc[1])} | garments ${(fin[0] / N).toFixed(2)}/${(fin[1] / N).toFixed(2)} | turns ${(turns / N).toFixed(1)} | recycle bonus/game ${(bonus / N).toFixed(2)} | by size 2/3/4: ${(sz[2] / N).toFixed(2)} ${(sz[3] / N).toFixed(2)} ${(sz[4] / N).toFixed(2)}`);
}
function solo(label, opt, s) {
  const sc = [], fin = []; for (let i = 0; i < N; i++) { const g = playGame({ ...opt, solo: true }, [SK[s]]); sc.push(g.pl[0].score); fin.push(g.log.fin[0]); }
  sc.sort((a, b) => a - b); console.log(`${label} solo ${s}: mean ${(sc.reduce((a, b) => a + b) / N).toFixed(1)} p10 ${pct(sc, .1)} p25 ${pct(sc, .25)} p50 ${pct(sc, .5)} p75 ${pct(sc, .75)} p90 ${pct(sc, .9)} max ${sc[N - 1]} | garments ${(fin.reduce((a, b) => a + b) / N).toFixed(2)}`);
}
// supply check
const sup = {}, dem = {}; CARDS.forEach(c => { sup[c.recipe[0]] = (sup[c.recipe[0]] || 0) + 1; sup[c.bottom] = (sup[c.bottom] || 0) + 1; c.recipe.slice(1).forEach(f => dem[f] = (dem[f] || 0) + 1); });
console.log('strips supplied by fabric', sup, '\nlayers demanded (excl. first)', dem, '\n');
for (const [label, o] of [['no hook', {}], ['bonus only', { bonus: true }], ['resale only', { resale: true }], ['resale + bonus', { resale: true, bonus: true }]]) { console.log('--- ' + label + ' ---');
  versus('strong v strong', o, 'strong', 'strong'); versus('strong(P1) v casual(P2)', o, 'strong', 'casual'); versus('casual(P1) v strong(P2)', o, 'casual', 'strong'); solo('', o, 'strong'); solo('', o, 'casual'); }
