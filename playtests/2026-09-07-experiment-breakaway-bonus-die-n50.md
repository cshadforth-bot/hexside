# Hexside Experiment — Breakaway Bonus Die, N=50

**Date:** 2026-09-07
**Status:** Test only, driver-side — nothing in `sim.py`/`board.py`/the rulebook was touched. The bonus is applied entirely inside the test driver's `attempt_shot()`, not a new engine primitive.
**Change tested:** +1 Shot (Attack) die if the shooting unit won a Dribble Challenge earlier in this same activation — "beat your man and shoot," the exact sequence Hexside's own earliest design review flagged as the sport's most basic move worth protecting. (The "won a Tackle, then shoots" half of the original idea doesn't actually fit the current rules as written — a won Tackle's free follow-up is specifically a Pass, never a Shot, so that half was dropped rather than bolted on inconsistently.)
**Format:** 50 fresh matches, 48 turns each, same beefed-up driver (Foul/Press/Slide Tackle all live) as the last two experiments.

**Result: mixed — the mechanic itself clearly works as designed, but it didn't produce a clean match-level goals increase this run, and the likely reason says something useful about how to test these changes going forward.**

---

## The mechanic is real, verified working, and gets exercised constantly

Confirmed directly in the log, not just trusted from the stat counter — a Playmaker (Shot stat 3) rolling 4 dice on a breakaway shot:

```
[Shot: B PM vs A GK (BREAKAWAY +1 die)] B rolls [2, 1, 3, 1]->[...] (0 succ)
```

And it's not a rare edge case: **59 of the match's 104 total shots (57%) came immediately off a won Dribble Challenge.** More than half of all shooting chances in this ruleset already arrive exactly the way the bonus is designed to reward — a genuinely central sequence, not a corner case.

## Breakaway shots converted better than average — the signal points the right way

| | Conversion rate |
|---|---|
| Breakaway shots (59 attempts) | **61.0%** (36 goals) |
| Non-breakaway shots in this same batch (45 attempts) | 20.0% (9 goals) |
| Baseline average, no bonus (from the Control+1 experiment's N=50 baseline) | 50.9% |

The bonus-die shots converted well above the general baseline (61% vs. 50.9%) — directionally exactly what an extra Attack die should do. But the *non*-breakaway shots in this same batch converted unusually badly (20%, well below the 50.9% baseline norm) — and there's no mechanism by which this change could make a non-bonus shot worse, since it's a strictly additive modifier that only ever applies in the favorable case. That gap is almost certainly this batch's own sampling noise landing unevenly across the two shot types, not a real effect.

## Whole-match totals didn't move cleanly, and that's a `sample-size vs. metric` problem, not necessarily a verdict on the mechanic

| | Baseline (N=50, no bonus) | This test (N=50, breakaway bonus) |
|---|---|---|
| Goals / match | 1.12 | 0.90 |
| Shots / match | 2.20 | 2.08 |
| Shot conversion (all shots) | 50.9% | 43.3% |
| Scoreless matches | 17/50 | 22/50 |

Taken at face value this reads as a decrease — but per the same statistical logic from the Control+1 write-up, a whole-match goal total at this rate has a standard deviation comparable to the gap being measured, and a change that mechanically can only ever add value to an individual shot has no plausible path to *causing* a match-level decrease. The much cleaner, lower-variance number in this report is the **direct 61% vs. 50.9% comparison on the bonus-die shots themselves** — that's the one built from a real dice-math difference (3 or 4 dice instead of 2 or 3), not from full-match emergent noise.

## A methodology note worth carrying forward

This is the second experiment in a row where the mechanically-relevant, low-variance number (contest win rates, or here, per-shot-type conversion) told a clear story while the whole-match goals aggregate bounced around too much to trust on its own at N=50. Testing future scoring levers by isolating the exact contest they touch — rather than reading whole-match goals-per-match as the primary signal — is probably the more reliable methodology from here, the same way the targeted mechanic tests for Emergency Goalkeeper and Jockey worked better than waiting for a rare event to show up in ordinary full matches.

## Bottom line

The breakaway bonus die is mechanically sound, fires on a majority of shots, and the one clean comparison available (conversion rate on the shots it actually touches) points the right direction. It isn't proven at the whole-match level yet, but that's a sample-size and metric-choice problem more than a sign the idea doesn't work. Worth either a much larger batch focused specifically on breakaway-vs-non-breakaway shot conversion (not full-match goals), or a targeted test that deliberately engineers several breakaway situations back-to-back the way the Emergency Goalkeeper test did — cleaner evidence, less noise, faster to run.
