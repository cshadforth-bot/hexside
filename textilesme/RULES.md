# Textilesme — draft 0.2 (simulated only, never played at a table)
18 cards, 1–2 tailors, ~20 minutes. Make stylish garments out of other people's old clothes.

## Every card is two things
A **garment order** (name, recipe of 2–4 fabrics, tips) and a **fabric source** (two strips: the **top strip** is the card's own first
fabric, the **bottom strip** is a salvage patch, printed upside down). Fabrics: Denim, Wool, Silk, Lace, Knit, Canvas.

## Setup
Shuffle all 18. Each player takes one card as their first **open garment** (its top strip is layer 1). Deal 4 face up: **the Counter**
(3 in solo). The rest is the deck.

## Your turn: take one Counter card and do one thing with it
- **Design** — start a new garment with it (its top strip is layer 1). You have two workbenches: at most 2 open garments.
- **Stitch** — slide it under one of your open garments so one strip peeks out as the next layer. That strip must be the fabric the
  recipe needs next. You may show either of its strips.
- **Unpick** — scrap it (face-up scrap bin). Usually to deny your rival.
Then refill the Counter from the deck. When a garment's layers match its recipe it is **finished**: bank its tips, resolve its effect.
Its stitched cards go to the scrap bin; the garment card itself stays in front of you as your score.

## Effects (when finished)
Second pair of hands: take another Counter card and use it · Moth: unpick the top stitched layer off a rival's open garment ·
Keep the offcuts: put one stitched card in your Stash (+1 each) instead of the scrap bin · Rummage: draw the top deck card and use it ·
Jumble sale: scrap the Counter and deal a new one.

## Two days, and nothing is wasted
When the deck is empty keep playing without refills until the Counter is empty. That ends a day.
**Washing up:** every open garment is unpicked (−1 tip each) and goes to the scrap bin. **Finished garments are resold:** they go
into the scrap bin too (your tips stay banked). Shuffle the scrap bin into a new deck, deal a new Counter; day 2 is played with the
clothes you made on day 1. **Player 2 starts day 2.** Stashed cards leave the game. After day 2, open garments cost −1 each.
**Score:** tips on finished garments + Stash − open garments. Tie: shared win.

## Solo
Counter of 3; after each turn the oldest Counter card goes cold and leaves the game; ignore Moth. Provisional ranks:
0–7 Patcher · 8–10 Seamstress · 11–14 Designer · 15+ Couturier.

## What the simulator says (3,000 games per row, `node sim.js 3000`)
Strong bots, P1/P2/tie 46.5/47.7/5.8%; about 2.9 garments and 8.6 tips each; strong beats casual about 65%.
Solo: strong bot mean 11.2 (p10 6, p90 16), casual bot mean 7.6.
Tested and dropped: a +1 tip for stitching recycled cards (flat inflation, tilts towards the day-2 starter: 45/50).
Not tested: whether resale feels like a real decision to humans; the bots never consider feeding the rival.
