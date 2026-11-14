// Monte-Carlo check: does the 18-card economy give a real spread between random play and good play?
const { SALVAGE, COMMISSIONS, DOMINOES, scoreCommission } = require('./data.js');
const rnd = n => Math.floor(Math.random() * n);
const shuffle = a => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = rnd(i + 1); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const meets = (s, pp) => !s.req || pp.every(p => p[0] === s.req || p[1] === s.req);

function options(row, slot) { // every legal cut for this slot
  const out = [];
  row.forEach(card => {
    if (slot.size === 1) card.patches.forEach((p, i) => { if (p && !card.used[i]) out.push({ card, idx: [i], ps: [p] }); });
    else DOMINOES.forEach(([a, b]) => { const pa = card.patches[a], pb = card.patches[b]; if (pa && pb && !card.used[a] && !card.used[b]) out.push({ card, idx: [a, b], ps: [pa, pb] }); });
  });
  return out;
}
function play(policy) {
  const deck = shuffle(SALVAGE).map(c => ({ ...c, used: [false, false, false, false] }));
  let row = deck.splice(0, 4), total = 0;
  for (const c of shuffle(COMMISSIONS)) {
    const placed = c.slots.map(() => null);
    const order = policy === 'smart' ? c.slots.map((s, i) => i).sort((a, b) => c.slots[b].size - c.slots[a].size) : shuffle(c.slots.map((s, i) => i));
    for (const i of order.slice(0, 4)) {
      const opts = options(row, c.slots[i]); if (!opts.length) continue;
      let pick;
      if (policy === 'smart') { // prefer requirement match, then the leftover-minimising cut (keep fat cards intact)
        const good = opts.filter(o => meets(c.slots[i], o.ps)); const pool = good.length ? good : opts;
        pick = pool[rnd(pool.length)];
      } else pick = opts[rnd(opts.length)];
      pick.idx.forEach(k => pick.card.used[k] = true); placed[i] = pick.ps;
    }
    total += scoreCommission(c, placed);
    row = row.filter(cd => cd.patches.some((p, k) => p && !cd.used[k]));
    row.push(...deck.splice(0, 2));
  }
  return total;
}
const stats = pol => { const r = Array.from({ length: 20000 }, () => play(pol)).sort((a, b) => a - b); return { pol, mean: (r.reduce((a, b) => a + b) / r.length).toFixed(1), p10: r[2000], p50: r[10000], p90: r[18000], max: r[r.length - 1] }; };
console.log('Max possible per game: 72');
console.log(stats('random')); console.log(stats('smart'));
const cnt = {}; SALVAGE.forEach(c => c.patches.forEach(p => { if (p) { cnt[p[0]] = (cnt[p[0]]||0)+1; cnt[p[1]] = (cnt[p[1]]||0)+1; } }));
console.log('Usable patches:', SALVAGE.flatMap(c => c.patches).filter(Boolean).length, cnt);
