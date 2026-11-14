# Carly Cakes — rules, draft 0.1

18-card baking game for 1–2 bakers, about 25 minutes. Sister game to Pour Decisions, First Crack and Microlot.
Every number below is what `sim.py` plays; if this file and the code ever disagree, fix whichever is wrong.

## The cards

Each card is a cake. Its four edges are a **dial**, printed so a quarter-turn clockwise brings the next edge to the top:

| Edge (clockwise from top) | Stage | Shows |
|---|---|---|
| Top | **Batter** | nothing (blank) |
| Left | **Risen** | points (0–9) |
| Bottom (upside down) | **Golden** | points |
| Right | **Dark** | points |

One more turn after Dark and the cake is **cinders**: it goes to the Bin and scores nothing.
Below the dial each card has a **When pulled** effect, and some have a quirk.

## Setup

1. Shuffle the 18 cards. Deal 3 face up.
2. Player 2 takes one into their oven, then Player 1 takes one (Batter edge up). The third card starts **the Counter**.
3. Deal the Counter up to 4 cards (solo: 3). The rest is the deck. Each baker has **two racks**: at most two cakes in the oven at once.
4. Player 1 goes first.

## Your turn

1. **Turn your cakes.** Give every cake in your oven a quarter-turn clockwise. (Skip this if Cooling rack told you to.)
2. **Do one thing:**
   - **Pull** a cake that is Risen, Golden or Dark: score the number on its top edge, resolve its effect, put it on the **Sold pile**.
   - **Bake**: take a Counter card, put it in an empty rack, Batter edge up.
   - **Slam the door**: take a Counter card and tuck it sideways under an opposing cake that is **Batter or Risen** (a Golden or Dark cake is set and can't be knocked). Turn that cake a quarter-turn at once. The tucked card goes to the **Bin**.
   - **Bin**: take a Counter card and put it in the Bin (to deny it).
   If the Counter is empty you must pull. If you can do nothing, skip.
3. Refill the Counter to 4 from the deck.

A slam makes the cake skip a stage: its owner's next turn starts one dial-edge further on than they planned. If the next stage was the peak, they lose it. If the stage after is better, the slam helped them.

*Use a card* (for effects) means: bake it, slam with it, or put it in the Bin.

## Days

The game is two **days**. A day ends the moment the deck and the Counter are both empty.
**Washing up:** shuffle the **Sold pile** into a new deck. Everything in the Bin leaves the game. Deal a new Counter. Cakes still in ovens stay there. **Player 2 starts day 2.**
When day 2 ends, cakes still in the oven score nothing.

## Winning

Most points wins. A tie is a shared win.

## Quirks

- **Water bath** (Cheesecake, Fruitcake): can't be slammed.
- **Preheated** (Tiramisu): bake it with the Risen edge up.

## Effects (When pulled)

| Effect | Text |
|---|---|
| Tip jar | +1 point. |
| Glaze | +1 point for each other cake in your oven. |
| Second helping | Take another Counter card and use it. |
| Chef's pick | Use the top card of the deck. |
| Fresh batch | Bin the whole Counter and deal a new one. |
| Draught | Slam any one of your opponent's cakes, at any stage. |
| Cooling rack | Your cakes don't turn at the start of your next turn. |
| Reheat | Use the most recently discarded card (Bin or Sold pile). |

## Solo

Play two days alone with one oven and two racks.
- The Counter is 3 cards. After each turn the **oldest** Counter card goes cold and leaves the game, then refill.
- No slamming. Ignore the opponent part of any effect.
- Score as usual, then grade yourself. **A win is Apprentice or better.**

| Score | Result | |
|---|---|---|
| 36 or less | **Burnt Offering** | lose |
| 37–42 | **Soggy Bottom** | lose |
| 43–49 | **Apprentice** | win |
| 50–56 | **Journeyman** | win |
| 57–62 | **Head Baker** | win |
| 63+ | **Master Baker** | win |

## Status

Draft 0.1, simulated only. Nobody has played it at a table yet. See `hub.html` for results and open issues.

## Rival Baker (solo versus mode)

Play the two-player game against an automated Player 2, driven by six Rival cards (`cards/build_rival.py`).
**Setup:** deal 3 cakes. You pick one, the Rival takes the left-most of the other two, the third starts the Counter. You go first.
**Rival's turn:** turn its cakes, flip the top Rival card (when they run out, shuffle all six), do what it says, refill the Counter.

**The usual list** (do the first that works):
1. **Pull** a cake that can't get better: its next number is the same or lower, or it is Dark. Biggest number first.
2. **Slam** one of your Batter or Risen cakes if skipping a stage would cost it 3 or more (not a Water bath). Use the Counter card with the smallest biggest-number.
3. **Bake**, if it has an empty rack: the Counter card with the biggest number on it.
4. **Bin** the left-most Counter card.
If the Counter is empty it pulls its best cake, or skips. Ties go to the left-most card.

**Effects it plays:** Tip jar and Glaze (points), Draught (on your cake that would lose most), Chef's pick and Reheat (bake the card if it has a free rack, otherwise bin it). It ignores every other effect.

| Rival card | What it does |
|---|---|
| By the book | Usual list, reading the Counter from the left. |
| Newest first | Usual list, reading the Counter from the right. |
| Early bird | First, pull the cake showing the biggest number if that number is 5 or more. Then the usual list. |
| Door slammer | Slam first if one of your Batter or Risen cakes would lose 2 or more. Then pull, bake, bin. |
| Sweet tooth | Usual list, but it bakes the card with the biggest Dark number. |
| Regular customer | The Rival scores +1 point. Then the usual list. |

Most points wins. **A tie goes to the Rival.** Simulated: casual bot wins 38%, heuristic bot 69%, planning bot 71%.
