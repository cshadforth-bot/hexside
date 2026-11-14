// Textilesme patchwork simulator (draft 0.7: patchwork, Upcycle and collection effects). A shared quilt of portrait cards; every card has a fabric
// on each of its four edges and belongs to a collection; each collection has an effect that fires when one of its cards is sewn or upcycled.
// Usage: node sim-patchwork.js [games] [seam] [trend] [perfect] [upcycle|off] [effects: all|none|<effect>] [slopes]
const { CARDS } = require('./data.js');
const rnd = n => Math.floor(Math.random() * n);
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = rnd(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const arg = (i, d) => process.argv[i] === undefined ? d : process.argv[i];
const OPT = { seam: +arg(3, 2), trend: +arg(4, 1), perfect: +arg(5, 2), upcycle: arg(6, '-1') === 'off' ? null : +arg(6, -1), effects: arg(7, 'all') };
const EFFECT = { Tops: 'hands', Dresses: 'statement', Workwear: 'ripper', Outerwear: 'rummage', Accessories: 'finish', Linens: 'jumble' };
const activeEffect = col => (OPT.effects === 'all' || OPT.effects === EFFECT[col]) ? EFFECT[col] : null;
const TIP = +arg(12, 2); // Finishing touch
const STMT = +arg(9, 1), RIP = +arg(10, 0), LINEN = arg(11, 'jumble'); // Statement piece per seam, Seam ripper flat bonus, Linens effect (jumble | swap)

const key = (x, y) => x + ',' + y;
const orient = (e, flip) => flip ? [e[1], e[0], e[3], e[2]] : [e[0], e[1], e[2], e[3]]; // [top,bottom,left,right]
const NB = [[0, -1, 0, 1], [0, 1, 1, 0], [-1, 0, 2, 3], [1, 0, 3, 2]]; // dx, dy, my edge, their edge

function scoreAt(g, x, y, o, trend) { // seams a card would make at (x,y); the cell may already be occupied (an Upcycle covers it)
  let pts = 0, touching = 0, matched = 0;
  for (const [dx, dy, mine, theirs] of NB) {
    const t = g.quilt.get(key(x + dx, y + dy)); if (!t) continue; touching++;
    if (t.o[theirs] === o[mine]) { matched++; pts += OPT.seam + (o[mine] === trend ? OPT.trend : 0); }
  }
  if (touching >= 2 && matched === touching) pts += OPT.perfect;
  return { pts, matched };
}
function spots(g) {
  const s = new Set(); for (const k of g.quilt.keys()) { const [x, y] = k.split(',').map(Number); NB.forEach(([dx, dy]) => { if (!g.quilt.has(key(x + dx, y + dy))) s.add(key(x + dx, y + dy)); }); }
  return [...s].map(k => k.split(',').map(Number));
}
function movesFor(g, c) {
  const out = [], ef = activeEffect(c.col);
  const add = (k, x, y, f, cost) => { const { pts, matched } = scoreAt(g, x, y, orient(c.e, f), g.trend);
    out.push({ k, c, x, y, f, gain: pts + cost, seams: matched, bonus: ef === 'statement' ? matched * STMT : ef === 'finish' ? TIP : ef === 'ripper' ? RIP : ef === 'jumble' && LINEN === 'swap1' ? 1 : 0 }); };
  for (const [x, y] of spots(g)) for (const f of [0, 1]) add('sew', x, y, f, 0);
  if (OPT.upcycle !== null) for (const [k, t] of g.quilt) if (t.col === c.col) { const [x, y] = k.split(',').map(Number); for (const f of [0, 1]) add('upcycle', x, y, f, OPT.upcycle); }
  return out;
}
const bestGain = (g, c) => movesFor(g, c).reduce((b, m) => Math.max(b, m.gain + m.bonus), 0);
function setCell(g, m) { const k = key(m.x, m.y), old = g.quilt.get(k); g.quilt.set(k, { o: orient(m.c.e, m.f), col: m.c.col, id: m.c.id }); return old; }
function undo(g, m, old) { const k = key(m.x, m.y); if (old) g.quilt.set(k, old); else g.quilt.delete(k); }

function newDay(g, cards) {
  g.quilt = new Map(); g.deck = shuffle(cards);
  const first = g.deck.pop(), fo = orient(first.e, rnd(2) === 1); g.quilt.set(key(0, 0), { o: fo, col: first.col, id: first.id, foundation: true });
  g.trend = fo[0]; g.rail = []; refill(g);
}
const railSize = g => g.solo ? 3 : 4;
function refill(g) { while (g.rail.length < railSize(g) && g.deck.length) g.rail.push(g.deck.pop()); }

// effect values the bot assumes when comparing moves (a heuristic, not the truth)
const EFFECT_VALUE = { hands: 3, rummage: 2, ripper: 0, jumble: 0 };
function chooseMove(g, skill, only) {
  const moves = (only ? [only] : g.rail).flatMap(c => movesFor(g, c));
  if (!moves.length) return null;
  if (Math.random() < skill.eps) return moves[rnd(moves.length)];
  let best = null, bv = -1e9;
  for (const m of moves) {
    let v = m.gain + m.bonus + (EFFECT_VALUE[activeEffect(m.c.col)] || 0);
    if (!g.solo && skill.deny) {
      const old = setCell(g, m); let danger = 0;
      for (const c of g.rail) if (c !== m.c) danger = Math.max(danger, bestGain(g, c));
      undo(g, m, old); v -= skill.deny * danger;
    }
    v += Math.random() * 0.01;
    if (v > bv) { bv = v; best = m; }
  }
  return best;
}
function execute(g, cur, m, skill, depth) {
  const idx = g.rail.indexOf(m.c); if (idx >= 0) g.rail.splice(idx, 1);
  setCell(g, m); g.pts[cur] += m.gain + m.bonus; if (m.k === 'upcycle') g.log.upcycled++; else g.log.placed++;
  const ef = activeEffect(m.c.col); if (!ef) return;
  g.trig[cur][ef] = (g.trig[cur][ef] || 0) + 1;
  if (ef === 'hands' && depth === 0) { const m2 = chooseMove(g, skill); if (m2) execute(g, cur, m2, skill, depth + 1); }
  else if (ef === 'rummage' && depth === 0 && g.deck.length) { const c = g.deck.pop(); g.rail.push(c); const m2 = chooseMove(g, skill, c); execute(g, cur, m2, skill, depth + 1); }
  else if (ef === 'jumble' && LINEN.startsWith('swap')) { // swap the juiciest Rail card (the rival moves next) for the top card of the deck, if that helps
    if (g.deck.length && g.rail.length) { const top = g.deck[g.deck.length - 1]; let w = null, wv = -1; for (const c of g.rail) { const v = bestGain(g, c); if (v > wv) { wv = v; w = c; } }
      if (bestGain(g, top) < wv) { g.rail[g.rail.indexOf(w)] = g.deck.pop(); } } }
  else if (ef === 'jumble') { g.rail = []; refill(g); }
  else if (ef === 'ripper') { // turn one card 180 degrees; the bot picks the turn that leaves the rival the least to take
    let bestK = null, bv = Math.max(0, ...g.rail.map(c => bestGain(g, c))) ; // baseline: no turn
    for (const [k, t] of g.quilt) { if (t.foundation) continue; const saved = t.o; t.o = orient(t.o, true);
      const danger = Math.max(0, ...g.rail.map(c => bestGain(g, c))); t.o = saved; if (danger < bv - 0.001) { bv = danger; bestK = k; } }
    if (bestK) { const t = g.quilt.get(bestK); t.o = orient(t.o, true); }
  }
}
function play(opts, skills) {
  const g = { solo: !!opts.solo, pts: opts.solo ? [0] : [0, 0], log: { placed: 0, upcycled: 0 }, trig: opts.solo ? [{}] : [{}, {}] };
  const cards = CARDS.map((c, i) => ({ id: i, col: c.collection, e: c.edges.split('') }));
  for (let day = 0; day < 2; day++) {
    newDay(g, cards);
    let cur = (day === 1 && !g.solo) ? 1 : 0, guard = 0;
    while (g.rail.length && guard++ < 200) {
      const m = chooseMove(g, skills[cur]); execute(g, cur, m, skills[cur], 0);
      if (g.solo && g.rail.length) g.rail.shift();
      refill(g); if (!g.solo) cur = 1 - cur;
    }
  }
  return g;
}
const SK = { strong: { eps: 0, deny: 0.5 }, casual: { eps: 0.15, deny: 0.5 }, greedy: { eps: 0, deny: 0 } };
const N = +process.argv[2] || 400, m = a => (a.reduce((x, y) => x + y, 0) / a.length).toFixed(1), pct = (a, q) => a[Math.floor(q * (a.length - 1))];
function versus(label, s1, s2) {
  let w = [0, 0], t = 0, sc = [[], []], placed = 0, up = 0, turns = 0; const trig = {};
  for (let i = 0; i < N; i++) { const g = play({}, [SK[s1], SK[s2]]); const [a, b] = g.pts; if (a > b) w[0]++; else if (b > a) w[1]++; else t++; sc[0].push(a); sc[1].push(b); placed += g.log.placed; up += g.log.upcycled;
    g.trig.forEach(o => { for (const k in o) trig[k] = (trig[k] || 0) + o[k]; }); }
  console.log(`${label}: P1 ${(100 * w[0] / N).toFixed(1)}% P2 ${(100 * w[1] / N).toFixed(1)}% tie ${(100 * t / N).toFixed(1)}% | mean ${m(sc[0])}/${m(sc[1])} | sewn ${(placed / N).toFixed(1)} upcycled ${(up / N).toFixed(1)}`);
  if (label.startsWith('strong v strong')) console.log('   effects per game:', Object.entries(trig).map(([k, v]) => k + ' ' + (v / N).toFixed(2)).join(', '));
}
function solo(label, s) { const sc = []; let up = 0; for (let i = 0; i < N; i++) { const g = play({ solo: true }, [SK[s]]); sc.push(g.pts[0]); up += g.log.upcycled; } sc.sort((a, b) => a - b); console.log(`${label} solo ${s}: mean ${m(sc)} p10 ${pct(sc, .1)} p50 ${pct(sc, .5)} p90 ${pct(sc, .9)} max ${sc[N - 1]} | upcycled ${(up / N).toFixed(1)}`); }
// value of one trigger of each effect: regress the score gap between the seats on the gap in triggers (strong v strong)
function slopes() {
  const sxy = {}, sxx = {}, base = { ...EFFECT }, cols = Object.keys(base), effs = Object.values(base);
  for (let i = 0; i < N; i++) { const p = shuffle(effs); cols.forEach((c, j) => { EFFECT[c] = p[j]; }); // random effect-to-collection mapping each game removes card-quality confounding
   const g = play({}, [SK.strong, SK.strong]); const d = g.pts[0] - g.pts[1];
    for (const ef of new Set([...Object.keys(g.trig[0]), ...Object.keys(g.trig[1])])) { const dx = (g.trig[0][ef] || 0) - (g.trig[1][ef] || 0); sxy[ef] = (sxy[ef] || 0) + dx * d; sxx[ef] = (sxx[ef] || 0) + dx * dx; } }
  console.log('buttons per trigger (score gap on trigger gap):', Object.keys(sxx).map(k => k + ' ' + (sxy[k] / sxx[k]).toFixed(2)).join(', '));
}
console.log('seam', OPT.seam, 'trend', OPT.trend, 'perfect', OPT.perfect, 'upcycle', OPT.upcycle === null ? 'off' : OPT.upcycle, 'effects', OPT.effects);
if (process.argv[8] === 'slopes') slopes(); else {
  versus('strong v strong', 'strong', 'strong'); versus('greedy v greedy', 'greedy', 'greedy');
  versus('strong(P1) v casual', 'strong', 'casual'); versus('casual(P1) v strong', 'casual', 'strong'); versus('strong v greedy', 'strong', 'greedy');
  solo('', 'strong'); solo('', 'casual');
}
