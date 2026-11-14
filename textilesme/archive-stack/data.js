// Textilesme card data (draft 0.4). Every card is a garment order AND a fabric source.
// recipe: fabrics bottom-to-top; recipe[0] is the card's TOP swatch (its own first layer).
// bottom: the card's BOTTOM swatch (a salvage patch, printed upside down). pts: buttons earned when finished.
const FABRICS = { D: ['Denim', '#2f6fd0'], W: ['Wool', '#e8643c'], S: ['Silk', '#c2408f'], L: ['Lace', '#ffe9c7'], K: ['Knit', '#3fae6a'], C: ['Canvas', '#f2b632'] };
const EFFECTS = {
  none:  ['No effect', ''],
  again: ['Second pair of hands', 'Take another Rail card and use it.'],
  moth:  ['Moth', "Unpick the top layer off one of your rival's garments (not its first swatch)."],
  stash: ['Keep the offcuts', 'Put one card from this garment in your button tin (+1 button).'],
  draw:  ['Rummage', 'Draw the top card of the deck and use it.'],
  fresh: ['Jumble sale', 'Put the whole Rail in the rag bag and deal a new one.'],
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
