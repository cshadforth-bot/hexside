# Textilesme — draft 0.7, patchwork, Upcycle and effects (simulated only, never played at a table)
18 cards, 1–2 tailors, ~20 minutes. Piece a quilt together from other people's old clothes, and remake what you can't use.

## Every card is a patch, and a garment
Each card is a garment cut into four patches: a **swatch** on its top, bottom, left and right edges, in one of six fabrics
(Denim, Wool, Silk, Lace, Knit, Canvas). 72 swatches in all, 12 of each fabric. The garment in the middle is drawn from the same four
fabrics, so you can read the edges off the picture. Every garment belongs to a **collection**, named under its title. All three garments in a
collection share one **effect**, printed on the card:

| Collection | Garments | Effect |
|---|---|---|
| Tops | Pocket Tee, Cardigan, Kimono | **Second pair of hands:** take another Rail card and use it. |
| Dresses | Slip Dress, Wedding Dress, Evening Gown | **Statement piece:** take 2 buttons for each matching seam this card made. |
| Workwear | Boiler Suit, Pinafore, Tote Bag | **Seam ripper:** turn any one card on the quilt 180° (not the Foundation). Take 2 buttons. |
| Outerwear | Denim Jacket, Peacoat, Patchwork Coat | **Rummage:** draw the top card of the deck and use it. |
| Accessories | Beanie, Scarf, Scrunchie | **Finishing touch:** take 3 buttons. |
| Linens | Hankie, Shawl, Quilt | **Remnant sale:** swap one Rail card for the top card of the deck (the swapped card is out for the day). Take 1 button. |

## Setup
Shuffle all 18. Turn the top card face up in the middle of the table: the **Foundation**. The fabric on its **top edge** is today's
**Trend**. Deal 4 cards face up: **the Rail** (3 in solo). The rest is the deck. Player 1 goes first.

## Your turn: take one Rail card and do one thing with it
- **Sew** it onto the quilt: lay it next to the cards already there, edge to edge, in a square grid (cards stay upright; you may turn it
  180 degrees). It must touch at least one card.
- **Upcycle** it: sew it **over** a card already on the quilt that belongs to the **same collection**. The covered card is unpicked and
  out of play for the day. A card that covers another can be covered in turn. Score the new card's seams against the cells around it as
  for a sew, then **pay 1 button** (unpicking takes time). The Foundation can be covered; the Trend does not change.
- **Seam:** each card it touches whose touching edge shows the **same fabric** scores **2 buttons**. A seam in the **Trend** fabric scores **+1**.
- **Perfect fit:** if the card touches 2 or more cards and **every** touching edge matches, **+2 buttons**.
- Edges that don't match score nothing and cost nothing. The Foundation scores nothing.
- **Effect:** after you sew or upcycle a card, score it, then resolve its collection's effect. Effects are not optional, except that you may choose
  not to turn a card with Seam ripper or not to swap with Remnant sale. Second pair of hands and Rummage only fire for a card you played
  yourself, not for a card they handed you. A card you are given must be sewn or upcycled, scoring as usual.
Then refill the Rail. Every card is sewn or upcycled: there is no pass and no discard. Taking a card is also how you keep it from your rival.

## Two days, and nothing is wasted
A day ends when the deck and the Rail are empty. **Washing up:** unpick the whole quilt, covered cards included, and shuffle all 18 cards
together. Your buttons stay banked. Day 2 is played with the same clothes, remade: a new Foundation, a new Trend, a new Rail.
**Player 2 starts day 2.** **Score:** buttons from both days. Most buttons wins. A tie is a shared win.

## Solo
Rail of 3. After each of your turns the oldest Rail card goes cold and leaves the day, so you play 9 cards a day. Provisional ranks:
0–73 Patcher · 74–83 Seamstress · 84–92 Designer · 93+ Couturier.

## What the simulator says (`node sim-patchwork.js 400 2 1 2 -1 all run 2 2 swap1 3`)
Strong bots, P1 / P2 / tie 47 / 50 / 3.5%; each player makes about 67 buttons and the seats average the same. Each effect fires about 5.5 times a
game, and there are about 2.4 Upcycles in about 33 plays. A strong bot beats a casual one (15% random moves) about 78% of the time. It beats a
greedy one that never blocks only about 52% to 45%: effects change the Rail so often that blocking is no longer reliable. Solo: strong bot mean 87
(p10 78, p90 95), casual bot mean 79.
Effect values were measured as the score gap per trigger over 1,500 games with a random effect-to-collection mapping each game. Second pair of
hands and Rummage are worth about +1.2 to +1.4 buttons more than the rest, which sit within about a button of each other. The measurement noise is
about 0.4 buttons a trigger, so no finer tuning was possible. Earlier tuning: Jumble sale (scrap the Rail) cost the player who used it 0.7 buttons
and became Remnant sale; Upcycle must cost 1 button or it happens 5 to 14 times a game.
Not tested: whether it is fun; how long a game takes with real people; whether the effect strength matters more than the seams; whether the
edge set is fair to the player who sews first on a particular Foundation.
(Earlier drafts built garments in recipe order and were close to Pour Decisions. Draft 0.4 is kept in `archive-stack/`.)
