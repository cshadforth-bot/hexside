// Textilesme patchwork simulator (draft 0.6: patchwork + Upcycle). A shared quilt of portrait cards; every card has a fabric on each of its
// four edges and belongs to a collection. Usage: node sim-patchwork.js [games] [seamPts] [trendBonus] [perfectBonus] [upcycleBonus|off]
const { CARDS } = require('./data.js');
const rnd = n => Math.floor(Math.random() * n);
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = rnd(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const arg = (i, d) => process.argv[i] === undefined ? d : process.argv[i];
const OPT = { seam: +arg(3, 2), trend: +arg(4, 1), perfect: +arg(5, 2), upcycle: arg(6, '2') === 'off' ? null : +arg(6, 2) };

const key = (x, y) => x + ',' + y;
const orient = (e, flip) => flip ? [e[1], e[0], e[3], e[2]] : [e[0], e[1], e[2], e[3]]; // [top,bottom,left,right]
const NB = [[0, -1, 0, 1], [0, 1, 1, 0], [-1, 0, 2, 3], [1, 0, 3, 2]]; // dx, dy, my edge, their edge

// Seams a card would make at (x,y); the cell itself may already be occupied (an Upcycle covers it).
function scorePlace(g, x, y, o, trend) {
  let pts = 0, touching = 0, matched = 0;
  for (const [dx, dy, mine, theirs] of NB) {
    const t = g.quilt.get(key(x + dx, y + dy)); if (!t) continue; touching++;
    if (t.o[theirs] === o[mine]) { matched++; pts += OPT.seam + (o[mine] === trend ? OPT.trend : 0); }
  }
  if (touching >= 2 && matched === touching) pts += OPT.perfect;
  return pts;
}
function spots(g) { // empty cells next to the quilt
  const s = new Set(); for (const k of g.quilt.keys()) { const [x, y] = k.split(',').map(Number); NB.forEach(([dx, dy]) => { if (!g.quilt.has(key(x + dx, y + dy))) s.add(key(x + dx, y + dy)); }); }
  return [...s].map(k => k.split(',').map(Number));
}
function movesFor(g, c) { // every legal way to use card c
  const out = [];
  for (const [x, y] of spots(g)) for (const f of [0, 1]) out.push({ k: 'sew', c, x, y, f, gain: scorePlace(g, x, y, orient(c.e, f), g.trend) });
  if (OPT.upcycle !== null) for (const [k, t] of g.quilt) if (t.col === c.col) { const [x, y] = k.split(',').map(Number);
    for (const f of [0, 1]) out.push({ k: 'upcycle', c, x, y, f, gain: scorePlace(g, x, y, orient(c.e, f), g.trend) + OPT.upcycle }); }
  return out;
}
const bestGain = (g, c) => movesFor(g, c).reduce((b, m) => Math.max(b, m.gain), 0);
function apply(g, m) { const k = key(m.x, m.y), old = g.quilt.get(k); g.quilt.set(k, { o: orient(m.c.e, m.f), col: m.c.col, id: m.c.id }); return old; }
function undo(g, m, old) { const k = key(m.x, m.y); if (old) g.quilt.set(k, old); else g.quilt.delete(k); }

function newDay(g, cards) {
  g.quilt = new Map(); g.deck = shuffle(cards); g.under = [];
  const first = g.deck.pop(), fo = orient(first.e, rnd(2) === 1); g.quilt.set(key(0, 0), { o: fo, col: first.col, id: first.id });
  g.trend = fo[0]; // the Trend is the fabric on the foundation's top edge
  g.rail = []; refill(g);
}
const railSize = g => g.solo ? 3 : 4;
function refill(g) { while (g.rail.length < railSize(g) && g.deck.length) g.rail.push(g.deck.pop()); }

function chooseMove(g, skill) {
  const moves = g.rail.flatMap(c => movesFor(g, c));
  if (Math.random() < skill.eps) return moves[rnd(moves.length)];
  let best = null, bv = -1e9;
  for (const m of moves) {
    let v = m.gain;
    if (!g.solo && skill.deny) { // denial: what could the rival take from the rail next?
      const old = apply(g, m); let danger = 0;
      for (const c of g.rail) if (c !== m.c) danger = Math.max(danger, bestGain(g, c));
      undo(g, m, old); v -= skill.deny * danger;
    }
    v += Math.random() * 0.01;
    if (v > bv) { bv = v; best = m; }
  }
  return best;
}
function play(opts, skills) {
  const g = { solo: !!opts.solo, pts: opts.solo ? [0] : [0, 0], log: { placed: 0, upcycled: 0 } };
  const cards = CARDS.map((c, i) => ({ id: i, col: c.collection, e: c.edges.split('') }));
  for (let day = 0; day < 2; day++) {
    newDay(g, cards);
    let cur = (day === 1 && !g.solo) ? 1 : 0, guard = 0;
    while (g.rail.length && guard++ < 200) {
      const m = chooseMove(g, skills[cur]); g.rail.splice(g.rail.indexOf(m.c), 1);
      apply(g, m); g.pts[cur] += m.gain; if (m.k === 'upcycle') g.log.upcycled++; else g.log.placed++;
      if (g.solo && g.rail.length) g.rail.shift(); // oldest card goes cold
      refill(g); if (!g.solo) cur = 1 - cur;
    }
  }
  return g;
}
const SK = { strong: { eps: 0, deny: 0.5 }, casual: { eps: 0.15, deny: 0.5 }, greedy: { eps: 0, deny: 0 } };
const N = +process.argv[2] || 400, m = a => (a.reduce((x, y) => x + y, 0) / a.length).toFixed(1), pct = (a, q) => a[Math.floor(q * (a.length - 1))];
function versus(label, s1, s2) {
  let w = [0, 0], t = 0, sc = [[], []], placed = 0, up = 0;
  for (let i = 0; i < N; i++) { const g = play({}, [SK[s1], SK[s2]]); const [a, b] = g.pts; if (a > b) w[0]++; else if (b > a) w[1]++; else t++; sc[0].push(a); sc[1].push(b); placed += g.log.placed; up += g.log.upcycled; }
  console.log(`${label}: P1 ${(100 * w[0] / N).toFixed(1)}% P2 ${(100 * w[1] / N).toFixed(1)}% tie ${(100 * t / N).toFixed(1)}% | mean ${m(sc[0])}/${m(sc[1])} | sewn ${(placed / N).toFixed(1)} upcycled ${(up / N).toFixed(1)} per game`);
}
function solo(label, s) { const sc = []; let up = 0; for (let i = 0; i < N; i++) { const g = play({ solo: true }, [SK[s]]); sc.push(g.pts[0]); up += g.log.upcycled; } sc.sort((a, b) => a - b); console.log(`${label} solo ${s}: mean ${m(sc)} p10 ${pct(sc, .1)} p50 ${pct(sc, .5)} p90 ${pct(sc, .9)} max ${sc[N - 1]} | upcycled ${(up / N).toFixed(1)}`); }
console.log('seam', OPT.seam, 'trend', OPT.trend, 'perfect', OPT.perfect, 'upcycle', OPT.upcycle === null ? 'off' : '+' + OPT.upcycle);
versus('strong v strong', 'strong', 'strong'); versus('greedy v greedy', 'greedy', 'greedy');
versus('strong(P1) v casual', 'strong', 'casual'); versus('casual(P1) v strong', 'casual', 'strong'); versus('strong v greedy', 'strong', 'greedy');
solo('', 'strong'); solo('', 'casual');
