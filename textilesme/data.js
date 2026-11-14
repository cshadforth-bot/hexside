// Textilesme card data (draft 0.5, patchwork). Every card is a patch with a fabric on each of its four edges.
// edges: 'TBLR' = top, bottom, left, right fabric. Rotating a card 180 degrees swaps top/bottom and left/right.
// 18 cards x 4 edges = 72 swatches, exactly 12 of each fabric. Every card shows 2 or 3 different fabrics.
const FABRICS = { D: ['Denim', '#2f6fd0'], W: ['Wool', '#e8643c'], S: ['Silk', '#c2408f'], L: ['Lace', '#ffe9c7'], K: ['Knit', '#3fae6a'], C: ['Canvas', '#f2b632'] };
const NAMES = ['Pocket Tee', 'Scarf', 'Scrunchie', 'Tote Bag', 'Beanie', 'Hankie', 'Denim Jacket', 'Cardigan', 'Slip Dress', 'Boiler Suit', 'Peacoat', 'Kimono', 'Pinafore', 'Shawl', 'Patchwork Coat', 'Wedding Dress', 'Quilt', 'Evening Gown'];
const EDGES = ['WSWS', 'SCCL', 'SKCC', 'SSKW', 'SKKS', 'CDDL', 'SCCD', 'LSKL', 'LWWL', 'WLWC', 'WWSW', 'DKDK', 'DKDL', 'KDLD', 'CCLW', 'DKKC', 'SDDW', 'CLKL'];
const CARDS = NAMES.map((name, i) => ({ name, edges: EDGES[i], top: EDGES[i][0], bottom: EDGES[i][1], left: EDGES[i][2], right: EDGES[i][3] }));
if (typeof module !== 'undefined') module.exports = { FABRICS, CARDS };
