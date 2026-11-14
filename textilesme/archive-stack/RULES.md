# Textilesme — draft 0.4 (simulated only, never played at a table)
18 cards, 1–2 tailors, ~20 minutes. Make stylish garments out of other people's old clothes.

## Every card is two things
A **garment order** (name, recipe of 2–4 fabrics, buttons) and a **fabric source** (two swatches: the **top swatch** is the card's own first
fabric, the **bottom swatch** is a salvage patch, printed upside down). Fabrics: Denim, Wool, Silk, Lace, Knit, Canvas.

## Setup
Shuffle all 18. Each player takes one card as their first **open garment** on a dress form (its top swatch is layer 1). Deal 4 face up:
**the Rail** (3 in solo). The rest is the deck.

## Your turn: take one Rail card and do one thing with it
- **Design** — start a new garment with it (its top swatch is layer 1). You have two dress forms: at most 2 open garments.
- **Stitch** — slide it under one of your open garments so one swatch peeks out as the next layer. That swatch must be the fabric the
  recipe needs next. You may show either of its swatches.
- **Unpick** — put it in the face-up rag bag. Usually to deny your rival.
Then refill the Rail from the deck. When a garment's layers match its recipe it is **finished**: bank its buttons, resolve its effect.
Its stitched cards go to the rag bag; the garment card itself stays in front of you as your score.

## Effects (when finished)
Second pair of hands: take another Rail card and use it · Moth: unpick the top stitched layer off a rival's open garment ·
Keep the offcuts: put one stitched card in your button tin (+1 button each) instead of the rag bag · Rummage: draw the top deck card and use it ·
Jumble sale: put the Rail in the rag bag and deal a new one.

## Two days, and nothing is wasted
When the deck is empty keep playing without refills until the Rail is empty. That ends a day.
**Washing up:** every open garment is unpicked (−1 button each) and goes to the rag bag. **Finished garments are resold:** they go
into the rag bag too (your buttons stay banked). Shuffle the rag bag into a new deck, deal a new Rail; day 2 is played with the
clothes you made on day 1. **Player 2 starts day 2.** Cards in a button tin leave the game. After day 2, open garments cost −1 each.
**Score:** buttons on finished garments + button tin − open garments. Tie: shared win.

## Solo
Rail of 3; after each turn the oldest Rail card goes cold and leaves the game; ignore Moth. Provisional ranks:
0–7 Patcher · 8–10 Seamstress · 11–14 Designer · 15+ Couturier.

## What the simulator says (3,000 games per row, `node sim.js 3000`)
Strong bots, P1/P2/tie 46.5/47.7/5.8%; about 2.9 garments and 8.6 buttons each; strong beats casual about 65%.
Solo: strong bot mean 11.2 (p10 6, p90 16), casual bot mean 7.6.
Tested and dropped: a +1 button for stitching recycled cards (flat inflation, tilts towards the day-2 starter: 45/50).
Not tested: whether resale feels like a real decision to humans; the bots never consider feeding the rival.
(The simulator's code still uses the earlier names: counter, scrap, stash, tips. Same rules, only the words changed in draft 0.4.)
