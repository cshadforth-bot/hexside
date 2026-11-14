# Textilesme — draft 0.5, patchwork (simulated only, never played at a table)
18 cards, 1–2 tailors, ~20 minutes. Piece a quilt together from other people's old clothes.

## Every card is a patch
Each card is a garment cut into four patches: a **swatch** on its top, bottom, left and right edges, in one of six fabrics
(Denim, Wool, Silk, Lace, Knit, Canvas). 72 swatches in all, 12 of each fabric. The garment in the middle is drawn from the same four
fabrics, so you can read the edges off the picture.

## Setup
Shuffle all 18. Turn the top card face up in the middle of the table: the **Foundation**. The fabric on its **top edge** is today's
**Trend**. Deal 4 cards face up: **the Rail** (3 in solo). The rest is the deck. Player 1 goes first.

## Your turn
Take one Rail card and **sew** it onto the quilt: lay it next to the cards already there, edge to edge, in a square grid (cards stay
upright; you may turn it 180 degrees). It must touch at least one card. Then refill the Rail.
- **Seam:** each card it touches whose touching edge shows the **same fabric** scores **2 buttons**. A seam in the **Trend** fabric scores **+1**.
- **Perfect fit:** if the card touches 2 or more cards and **every** touching edge matches, **+2 buttons**.
- Edges that don't match score nothing and cost nothing. The Foundation scores nothing.
Every card is sewn: there is no pass and no discard. Taking a card is also how you keep it from your rival.

## Two days, and nothing is wasted
A day ends when the deck and the Rail are empty. **Washing up:** unpick the whole quilt and shuffle all 18 cards together. Your buttons stay
banked. Day 2 is played with the same clothes, remade: a new Foundation, a new Trend, a new Rail. **Player 2 starts day 2.**
**Score:** buttons from both days. Most buttons wins. A tie is a shared win.

## Solo
Rail of 3. After each of your turns the oldest Rail card goes cold and leaves the day, so you sew 9 cards a day. Provisional ranks:
0–41 Patcher · 42–47 Seamstress · 48–53 Designer · 54+ Couturier.

## What the simulator says (`node sim-patchwork.js 400`)
Strong bots, P1 / P2 / tie 48 / 45 / 7%; each player makes about 44 buttons. A strong bot beats a casual one (15% random moves) about 80% of the
time and a greedy one that never blocks about 76%. Solo: strong bot mean 52 (p10 46, p90 59), casual bot mean 46.
Tested: with no Trend and no Perfect fit, ties jump to 24%, so both stay. A penalty for non-matching edges changed nothing for strong play.
A discard ("unpick") action was dead (used about 0.1 times a game) and was removed.
Not tested: whether it is fun to place cards when you must always sew; how long a game takes with real people; whether the edge set is fair
to the player who sews first on a particular Foundation.
(Earlier drafts built garments in recipe order and were close to Pour Decisions. Draft 0.4 is kept in `archive-stack/`.)
