// Textilesme card data (draft 0.7, patchwork, Upcycle and effects). Every card is a patch with a fabric on each of its four edges.
// edges: 'TBLR' = top, bottom, left, right fabric. Rotating a card 180 degrees swaps top/bottom and left/right.
// 18 cards x 4 edges = 72 swatches, exactly 12 of each fabric. Every card shows 2 or 3 different fabrics.
const FABRICS = { D: ['Denim', '#2f6fd0'], W: ['Wool', '#e8643c'], S: ['Silk', '#c2408f'], L: ['Lace', '#ffe9c7'], K: ['Knit', '#3fae6a'], C: ['Canvas', '#f2b632'] };
const NAMES = ['Pocket Tee', 'Scarf', 'Scrunchie', 'Tote Bag', 'Beanie', 'Hankie', 'Denim Jacket', 'Cardigan', 'Slip Dress', 'Boiler Suit', 'Peacoat', 'Kimono', 'Pinafore', 'Shawl', 'Patchwork Coat', 'Wedding Dress', 'Quilt', 'Evening Gown'];
const EDGES = ['WSWS', 'SCCL', 'SKCC', 'SSKW', 'SKKS', 'CDDL', 'SCCD', 'LSKL', 'LWWL', 'WLWC', 'WWSW', 'DKDK', 'DKDL', 'KDLD', 'CCLW', 'DKKC', 'SDDW', 'CLKL'];
// Six collections of three garments. Upcycle: sew a card over a card from the same collection.
const COLLECTIONS = { Tops: ['Pocket Tee', 'Cardigan', 'Kimono'], Dresses: ['Slip Dress', 'Wedding Dress', 'Evening Gown'], Workwear: ['Boiler Suit', 'Pinafore', 'Tote Bag'],
  Outerwear: ['Denim Jacket', 'Peacoat', 'Patchwork Coat'], Accessories: ['Beanie', 'Scarf', 'Scrunchie'], Linens: ['Hankie', 'Shawl', 'Quilt'] };
// One effect per collection. It fires after you sew or upcycle a card from that collection.
const EFFECTS = {
  Tops: ['Second pair of hands', 'Take another Rail card and use it.'],
  Dresses: ['Statement piece', 'Take 2 buttons for each matching seam this card made.'],
  Workwear: ['Seam ripper', 'Turn any one card on the quilt 180\u00B0 (not the Foundation). Take 2 buttons.'],
  Outerwear: ['Rummage', 'Draw the top card of the deck and use it.'],
  Accessories: ['Finishing touch', 'Take 3 buttons.'],
  Linens: ['Remnant sale', 'Swap one Rail card for the top card of the deck. Take 1 button.'],
};
const collectionOf = name => Object.keys(COLLECTIONS).find(k => COLLECTIONS[k].includes(name));
const CARDS = NAMES.map((name, i) => ({ name, collection: collectionOf(name), effect: EFFECTS[collectionOf(name)], edges: EDGES[i], top: EDGES[i][0], bottom: EDGES[i][1], left: EDGES[i][2], right: EDGES[i][3] }));
if (typeof module !== 'undefined') module.exports = { FABRICS, COLLECTIONS, EFFECTS, CARDS };
