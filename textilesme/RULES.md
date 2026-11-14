# Textilesme — draft 0.6, patchwork and Upcycle (simulated only, never played at a table)
18 cards, 1–2 tailors, ~20 minutes. Piece a quilt together from other people's old clothes, and remake what you can't use.

## Every card is a patch, and a garment
Each card is a garment cut into four patches: a **swatch** on its top, bottom, left and right edges, in one of six fabrics
(Denim, Wool, Silk, Lace, Knit, Canvas). 72 swatches in all, 12 of each fabric. The garment in the middle is drawn from the same four
fabrics, so you can read the edges off the picture. Every garment belongs to a **collection**, named under its title:

| Collection | Garments |
|---|---|
| Tops | Pocket Tee, Cardigan, Kimono |
| Dresses | Slip Dress, Wedding Dress, Evening Gown |
| Workwear | Boiler Suit, Pinafore, Tote Bag |
| Outerwear | Denim Jacket, Peacoat, Patchwork Coat |
| Accessories | Beanie, Scarf, Scrunchie |
| Linens | Hankie, Shawl, Quilt |

## Setup
Shuffle all 18. Turn the top card face up in the middle of the table: the **Foundation**. The fabric on its **top edge** is today's
**Trend**. Deal 4 cards face up: **the Rail** (3 in solo). The rest is the deck. Player 1 goes first.

## Your turn: take one Rail card and do one thing with it
- **Sew** it onto the quilt: lay it next to the cards already there, edge to edge, in a square grid (cards stay upright; you may turn it
  180 degrees). It must touch at least one card.
- **Upcycle** it: sew it **over** a card already on the quilt that belongs to the **same collection**. The covered card is unpicked and
  out of play for the day. A card that covers another can be covered in turn. Score the new card's seams against the cells around it as
  for a sew, then **pay 1 button** (unpicking takes time). The Foundation can be covered; the Trend does not change.
Then refill the Rail.
- **Seam:** each card it touches whose touching edge shows the **same fabric** scores **2 buttons**. A seam in the **Trend** fabric scores **+1**.
- **Perfect fit:** if the card touches 2 or more cards and **every** touching edge matches, **+2 buttons**.
- Edges that don't match score nothing and cost nothing. The Foundation scores nothing.
Every card is sewn or upcycled: there is no pass and no discard. Taking a card is also how you keep it from your rival.

## Two days, and nothing is wasted
A day ends when the deck and the Rail are empty. **Washing up:** unpick the whole quilt, covered cards included, and shuffle all 18 cards
together. Your buttons stay banked. Day 2 is played with the same clothes, remade: a new Foundation, a new Trend, a new Rail.
**Player 2 starts day 2.** **Score:** buttons from both days. Most buttons wins. A tie is a shared win.

## Solo
Rail of 3. After each of your turns the oldest Rail card goes cold and leaves the day, so you play 9 cards a day. Provisional ranks:
0–41 Patcher · 42–47 Seamstress · 48–53 Designer · 54+ Couturier.

## What the simulator says (`node sim-patchwork.js 400 2 1 2 -1`)
Strong bots, P1 / P2 / tie 45 / 51 / 4%; each player makes about 45 buttons and the two seats average the same. A strong bot beats a casual
one (15% random moves) about 81% of the time and a greedy one that never blocks about 74%. Each two-player game has about 2.6 Upcycles in
about 34 plays. Solo: strong bot mean 53 (p10 46, p90 60), casual bot mean 47, about 0.8 Upcycles a game.
Upcycle was tuned in the simulator. Free, or at +2, players Upcycled 5 to 14 times a game, because re-scoring the neighbours of a cell is
worth it on its own. At a cost of 1 button it is a special move; at 2 or more it nearly disappears.
Tested earlier: with no Trend and no Perfect fit, ties jump to 24%, so both stay. A penalty for non-matching edges changed nothing for
strong play. A discard action was dead and was removed.
Not tested: whether it is fun to place cards when you must always sew or remake; how long a game takes with real people; whether the edge
set is fair to the player who sews first on a particular Foundation.
(Earlier drafts built garments in recipe order and were close to Pour Decisions. Draft 0.4 is kept in `archive-stack/`.)
