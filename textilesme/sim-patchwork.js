// Textilesme patchwork prototype (draft 0.5 candidate). A shared quilt of portrait cards; every card has a fabric on each of its four edges.
// Usage: node sim-patchwork.js [games] [seamPts] [trendBonus] [perfectBonus]
const rnd = n => Math.floor(Math.random() * n);
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = rnd(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const FAB = 'DWSLKC'.split('');

// ---- cards: 18 x 4 edges (top, bottom, left, right), 12 of each fabric overall, every card has at least 2 different fabrics.
function seededEdges(seed) {
  let s = seed; const r = () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
  for (;;) {
    const pool = []; FAB.forEach(f => { for (let i = 0; i < 12; i++) pool.push(f); });
    for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }
    const cards = []; for (let i = 0; i < 18; i++) cards.push(pool.slice(i * 4, i * 4 + 4).join(''));
    const ok = cards.every(c => new Set(c.split('')).size >= 2 && new Set(c.split('')).size <= 3);
    if (ok) return cards;
  }
}
const OPT = { seam: +process.argv[3] || 2, trend: process.argv[4] === undefined ? 1 : +process.argv[4], perfect: process.argv[5] === undefined ? 2 : +process.argv[5], clash: process.argv[6] === undefined ? 0 : +process.argv[6] };
const EDGES = seededEdges(7);

const key = (x, y) => x + ',' + y;
const orient = (e, flip) => flip ? [e[1], e[0], e[3], e[2]] : [e[0], e[1], e[2], e[3]]; // [top,bottom,left,right]
function scorePlace(g, x, y, e, flip, trend) {
  const o = orient(e, flip); let pts = 0, touching = 0, matched = 0;
  const nb = [[x, y - 1, 0, 1], [x, y + 1, 1, 0], [x - 1, y, 2, 3], [x + 1, y, 3, 2]]; // my edge index, their edge index
  for (const [nx, ny, mine, theirs] of nb) {
    const t = g.quilt.get(key(nx, ny)); if (!t) continue; touching++;
    if (t[theirs] === o[mine]) { matched++; pts += OPT.seam + (o[mine] === trend ? OPT.trend : 0); }
    else pts -= OPT.clash; // puckered seam
  }
  if (touching >= 2 && matched === touching) pts += OPT.perfect;
  return pts;
}
function spots(g) { // empty cells next to the quilt
  const s = new Set(); for (const k of g.quilt.keys()) { const [x, y] = k.split(',').map(Number); [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]].forEach(([a, b]) => { if (!g.quilt.has(key(a, b))) s.add(key(a, b)); }); }
  return [...s].map(k => k.split(',').map(Number));
}
function bestGain(g, e, trend) { let b = 0; for (const [x, y] of spots(g)) for (const f of [0, 1]) b = Math.max(b, scorePlace(g, x, y, e, f, trend)); return b; }

function newDay(g, cards) {
  g.quilt = new Map(); g.deck = shuffle(cards); g.rag = [];
  const first = g.deck.pop(), fo = orient(first.e, rnd(2) === 1); g.quilt.set(key(0, 0), fo); g.rag.push(first); // the foundation starts the quilt and scores nothing
  g.trend = fo[0]; // the Trend is the fabric on the foundation's top edge
  g.rail = []; refill(g);
}
const railSize = g => g.solo ? 3 : 4;
function refill(g) { while (g.rail.length < railSize(g) && g.deck.length) g.rail.push(g.deck.pop()); }

function chooseMove(g, p, skill) {
  const moves = [];
  for (const c of g.rail) {
    for (const [x, y] of spots(g)) for (const f of [0, 1]) moves.push({ k: 'sew', c, x, y, f, gain: scorePlace(g, x, y, c.e, f, g.trend) });
  }
  if (Math.random() < skill.eps) { const sews = moves.filter(m => m.k === 'sew'); return sews[rnd(sews.length)]; }
  let best = null, bv = -1e9;
  for (const m of moves) {
    let v = m.gain;
    if (!g.solo) {
      // denial: what could the rival take from the rail next? Look at the quilt after this move.
      const rest = g.rail.filter(c => c !== m.c); let danger = 0;
      if (m.k === 'sew') { const saved = g.quilt.get(key(m.x, m.y)); g.quilt.set(key(m.x, m.y), orient(m.c.e, m.f)); for (const c of rest) danger = Math.max(danger, bestGain(g, c.e, g.trend)); g.quilt.delete(key(m.x, m.y)); }
      else for (const c of rest) danger = Math.max(danger, bestGain(g, c.e, g.trend));
      v -= skill.deny * danger;
    }
    v += Math.random() * 0.01; if (m.k === 'unpick') v -= 0.6; // unpicking wastes the card
    if (v > bv) { bv = v; best = m; }
  }
  return best;
}
function play(opts, skills) {
  const g = { solo: !!opts.solo, trends: shuffle(FAB).slice(0, 2), pts: opts.solo ? [0] : [0, 0], log: { seams: 0, placed: 0, unpick: 0 } };
  const cards = EDGES.map((e, i) => ({ id: i, e: e.split('') }));
  for (let day = 0; day < 2; day++) {
    newDay(g, cards);
    let cur = (day === 1 && !g.solo) ? 1 : 0, guard = 0;
    while (g.rail.length && guard++ < 200) {
      const m = chooseMove(g, cur, skills[cur]); g.rail.splice(g.rail.indexOf(m.c), 1);
      if (m.k === 'sew') { g.quilt.set(key(m.x, m.y), orient(m.c.e, m.f)); g.pts[cur] += m.gain; g.log.placed++; if (m.gain) g.log.seams++; } else { g.rag.push(m.c); g.log.unpick++; }
      if (g.solo && g.rail.length) g.rail.shift(); // oldest card goes cold
      refill(g); if (!g.solo) cur = 1 - cur;
    }
  }
  return g;
}
const SK = { strong: { eps: 0, deny: 0.5 }, casual: { eps: 0.15, deny: 0.5 }, greedy: { eps: 0, deny: 0 } };
const N = +process.argv[2] || 2000, m = a => (a.reduce((x, y) => x + y, 0) / a.length).toFixed(1), pct = (a, q) => a[Math.floor(q * (a.length - 1))];
function versus(label, s1, s2) {
  let w = [0, 0], t = 0, sc = [[], []], placed = 0, unpick = 0;
  for (let i = 0; i < N; i++) { const g = play({}, [SK[s1], SK[s2]]); const [a, b] = g.pts; if (a > b) w[0]++; else if (b > a) w[1]++; else t++; sc[0].push(a); sc[1].push(b); placed += g.log.placed; unpick += g.log.unpick; }
  console.log(`${label}: P1 ${(100 * w[0] / N).toFixed(1)}% P2 ${(100 * w[1] / N).toFixed(1)}% tie ${(100 * t / N).toFixed(1)}% | mean ${m(sc[0])}/${m(sc[1])} | sewn/unpicked per game ${(placed / N).toFixed(1)}/${(unpick / N).toFixed(1)}`);
}
function solo(label, s) { const sc = []; let placed = 0; for (let i = 0; i < N; i++) { const g = play({ solo: true }, [SK[s]]); sc.push(g.pts[0]); placed += g.log.placed; } sc.sort((a, b) => a - b); console.log(`${label} solo ${s}: mean ${m(sc)} p10 ${pct(sc, .1)} p50 ${pct(sc, .5)} p90 ${pct(sc, .9)} max ${sc[N - 1]} | sewn ${(placed / N).toFixed(1)}`); }
console.log('cards', EDGES.join(' '), '| seam', OPT.seam, 'trend', OPT.trend, 'perfect', OPT.perfect);
versus('strong v strong', 'strong', 'strong'); versus('greedy v greedy', 'greedy', 'greedy');
versus('strong(P1) v casual', 'strong', 'casual'); versus('casual(P1) v strong', 'casual', 'strong'); versus('strong v greedy', 'strong', 'greedy');
solo('', 'strong'); solo('', 'casual');
