// Textilesme card data. Patch = [colour, texture] or null (a moth hole).
// Cards are 2x2 grids: index 0 1 / 2 3. A "domino" is an edge-adjacent pair: 01, 23, 02, 13.
const COLOURS = { Indigo: '#2f3e7a', Rust: '#b5532f', Moss: '#5c7a3a', Cream: '#eadfc6', Plum: '#6e3a63', Mustard: '#d3a21f' };
const TEXTURES = ['Denim', 'Wool', 'Silk', 'Lace', 'Canvas', 'Knit'];
const DOMINOES = [[0, 1], [2, 3], [0, 2], [1, 3]];
const P = (c, t) => [c, t];

const SALVAGE = [
  { name: 'Old Jeans',       patches: [P('Indigo','Denim'), P('Indigo','Denim'), P('Indigo','Denim'), null] },
  { name: 'Worn Jacket',     patches: [P('Indigo','Denim'), P('Indigo','Denim'), P('Rust','Canvas'), P('Rust','Canvas')] },
  { name: 'Tote Bag',        patches: [P('Cream','Canvas'), P('Cream','Canvas'), P('Moss','Canvas'), P('Moss','Canvas')] },
  { name: 'Moth Jumper',     patches: [P('Mustard','Knit'), P('Mustard','Knit'), P('Mustard','Knit'), null] },
  { name: 'Cardigan',        patches: [P('Moss','Knit'), P('Moss','Knit'), P('Cream','Knit'), P('Plum','Knit')] },
  { name: 'Scarf',           patches: [P('Plum','Wool'), P('Plum','Wool'), P('Rust','Wool'), null] },
  { name: 'Blazer',          patches: [P('Rust','Wool'), P('Rust','Wool'), P('Indigo','Wool'), P('Indigo','Wool')] },
  { name: 'Slip Dress',      patches: [P('Plum','Silk'), P('Plum','Silk'), P('Cream','Silk'), P('Cream','Silk')] },
  { name: 'Silk Shirt',      patches: [P('Mustard','Silk'), P('Mustard','Silk'), P('Moss','Silk'), null] },
  { name: 'Net Curtains',    patches: [P('Cream','Lace'), P('Cream','Lace'), P('Cream','Lace'), null] },
  { name: 'Doily Cloth',     patches: [P('Cream','Lace'), P('Cream','Lace'), P('Mustard','Lace'), P('Plum','Lace')] },
  { name: 'Tent Canvas',     patches: [P('Moss','Canvas'), P('Rust','Canvas'), P('Mustard','Canvas'), null] },
];

// size 2 = needs a domino (both patches must meet req), size 1 = single patch. req: colour, texture or null.
const all = (ps, f) => ps.length > 0 && ps.every(f);
const COMMISSIONS = [
  { name: 'Denim Jacket', slots: [
      { name: 'Body', size: 2, req: 'Denim' }, { name: 'Sleeves', size: 2, req: 'Indigo' },
      { name: 'Collar', size: 1, req: null }, { name: 'Pocket', size: 1, req: 'Canvas' }],
    style: 'Tonal', rule: 'All four slots share one colour.',
    test: ps => all(ps, p => p[0] === ps[0][0]) },
  { name: 'Wrap Dress', slots: [
      { name: 'Bodice', size: 2, req: 'Silk' }, { name: 'Skirt', size: 2, req: null },
      { name: 'Sash', size: 1, req: 'Plum' }, { name: 'Trim', size: 1, req: 'Lace' }],
    style: 'Mixed Media', rule: '3 or more different textures.',
    test: ps => new Set(ps.map(p => p[1])).size >= 3 },
  { name: 'Patchwork Coat', slots: [
      { name: 'Body', size: 2, req: 'Wool' }, { name: 'Lining', size: 2, req: 'Silk' },
      { name: 'Cuff', size: 1, req: null }, { name: 'Toggle', size: 1, req: 'Rust' }],
    style: 'Clash', rule: 'No colour appears in two different slots.',
    test: (ps, slots) => { const cs = slots.map(s => new Set(s.map(p => p[0]))); const seen = new Set(); for (const s of cs) { for (const c of s) { if (seen.has(c)) return false; } for (const c of s) seen.add(c); } return true; } },
  { name: 'Market Tote', slots: [
      { name: 'Panel', size: 2, req: 'Canvas' }, { name: 'Strap', size: 2, req: null },
      { name: 'Pocket', size: 1, req: 'Moss' }, { name: 'Tag', size: 1, req: null }],
    style: 'Earthy', rule: 'No Indigo or Plum anywhere.',
    test: ps => ps.every(p => p[0] !== 'Indigo' && p[0] !== 'Plum') },
  { name: 'Winter Jumper', slots: [
      { name: 'Body', size: 2, req: 'Knit' }, { name: 'Sleeves', size: 2, req: 'Mustard' },
      { name: 'Neck', size: 1, req: 'Cream' }, { name: 'Elbow', size: 1, req: null }],
    style: 'Soft Touch', rule: 'No Denim or Canvas anywhere.',
    test: ps => ps.every(p => p[1] !== 'Denim' && p[1] !== 'Canvas') },
  { name: 'Evening Gown', slots: [
      { name: 'Bodice', size: 2, req: 'Silk' }, { name: 'Skirt', size: 2, req: 'Cream' },
      { name: 'Veil', size: 1, req: 'Lace' }, { name: 'Brooch', size: 1, req: null }],
    style: 'Bold Accent', rule: 'Exactly one slot is a different colour to the rest.',
    test: (ps, slots) => { const m = slots.map(s => s[0][0]); const counts = {}; m.forEach(c => counts[c] = (counts[c]||0)+1); return Object.values(counts).sort().join() === '1,3'; } },
];

// Scoring: filled slot 1pt, +1 if requirement met (slot with no requirement always gets the +1). Style bonus +4. Max 12 per commission.
function scoreCommission(c, placed) { // placed: array of arrays of patches (null = empty slot)
  let pts = 0;
  c.slots.forEach((s, i) => {
    const pp = placed[i]; if (!pp) return;
    pts += 1;
    if (!s.req || pp.every(p => p[0] === s.req || p[1] === s.req)) pts += 1;
  });
  if (placed.every(Boolean) && c.test(placed.flat(), placed)) pts += 4;
  return pts;
}
if (typeof module !== 'undefined') module.exports = { COLOURS, TEXTURES, DOMINOES, SALVAGE, COMMISSIONS, scoreCommission };
