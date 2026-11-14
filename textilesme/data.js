// Textilesme card data (draft 0.2). Every card is a garment order AND a fabric source.
// recipe: fabrics bottom-to-top; recipe[0] is the card's TOP strip (its own first layer).
// bottom: the card's BOTTOM strip (a salvage patch, printed upside down). pts: stitched tips when finished.
const FABRICS = { D: ['Denim', '#3b5a8c'], W: ['Wool', '#b5532f'], S: ['Silk', '#6e3a63'], L: ['Lace', '#eadfc6'], K: ['Knit', '#5c7a3a'], C: ['Canvas', '#d3a21f'] };
const EFFECTS = {
  none:  ['No effect', ''],
  again: ['Second pair of hands', 'Take another Counter card and use it.'],
  moth:  ['Moth', "Unpick the top layer off one of your rival's open garments (not its ticket)."],
  stash: ['Keep the offcuts', 'Put one card from this garment in your Stash (+1) instead of recycling it.'],
  draw:  ['Rummage', 'Draw the top card of the deck and use it.'],
  fresh: ['Jumble sale', 'Scrap the whole Counter and deal a new one.'],
};
const mk = (name, recipe, bottom, effect) => ({ name, recipe: recipe.split(''), bottom, effect, pts: { 2: 2, 3: 4, 4: 6 }[recipe.length] });
const CARDS = [
  mk('Pocket Tee', 'KC', 'D', 'again'), mk('Scarf', 'WK', 'L', 'none'), mk('Scrunchie', 'SL', 'K', 'moth'),
  mk('Tote Bag', 'CD', 'W', 'stash'), mk('Beanie', 'KW', 'S', 'draw'), mk('Hankie', 'LS', 'C', 'none'),
  mk('Denim Jacket', 'DCW', 'S', 'moth'), mk('Cardigan', 'KWL', 'D', 'fresh'), mk('Slip Dress', 'SLK', 'C', 'stash'),
  mk('Boiler Suit', 'CDK', 'L', 'again'), mk('Peacoat', 'WKD', 'S', 'moth'), mk('Kimono', 'SWL', 'D', 'draw'),
  mk('Pinafore', 'DKC', 'W', 'stash'), mk('Shawl', 'LWK', 'C', 'none'),
  mk('Patchwork Coat', 'DWKC', 'L', 'stash'), mk('Wedding Dress', 'LSKS', 'W', 'draw'),
  mk('Quilt', 'KCDW', 'S', 'fresh'), mk('Evening Gown', 'SLWD', 'K', 'moth'),
];
if (typeof module !== 'undefined') module.exports = { FABRICS, EFFECTS, CARDS };
