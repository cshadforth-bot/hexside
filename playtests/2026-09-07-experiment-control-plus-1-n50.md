# Hexside Experiment — Control +1, at N=50 (both arms)

**Date:** 2026-09-07
**Status:** Test only, engine-side — same throwaway-copy discipline as before. Nothing here touched the canonical `sim.py`/`board.py`/rulebook.
**Change:** SW/WB/PO Control 2→3, PM Control 3→4 (GK unchanged at 2).
**Why re-run:** The first comparison (10 matches per arm, 2026-09-07) found the stat moved exactly as predicted but goals didn't budge — with an open question of whether that was a real null result or just sample-size noise. This run puts **50 matches on each side** (2,400 turns per arm, 4,800 total) to actually resolve that question, and — importantly — **reruns the baseline at 50 too**, not just the test arm, since comparing a 50-match test against a 10-match baseline would have been comparing apples to a much noisier orange.

**Result: still no reliable increase in goals — and a real, unwanted side effect showed up that the smaller sample never surfaced.**

---

## Headline comparison

| | Baseline (N=50) | Control +1 (N=50) |
|---|---|---|
| Dribble Challenges won by attacker | 153 / 457 (**33.5%**) | 212 / 483 (**43.9%**) |
| Tackles won by defender | 132 / 428 (**30.8%**) | 97 / 422 (**23.0%**) |
| Shots / match | 2.20 | 2.44 |
| Goals / match | **1.12** | **1.00** |
| Scoreless matches | 17 / 50 (34%) | 22 / 50 (44%) |
| Shot conversion | 50.9% | 41.0% |
| Cards (Y+R) / match | 1.92 | 2.04 |
| **Red Cards, total** | **32** | **46** |
| Discipline draws / match | 6.72 | 7.46 |

## The contest-level effect held up exactly as before, at 5x the sample

Dribble win rate and Tackle-vs-carrier win rate both moved by huge, unambiguous margins again — this isn't noise; ~450-480 attempts per arm is more than enough to trust a 10-point swing in either direction. Control +1 does precisely what it says on the tin for the two contests it touches.

## But goals did not follow — and this time the sample is big enough to say so with real confidence

A 12-goal gap (56 vs. 50 across 50 matches) sounds like a real drop, but goals-per-match here behaves like a low-count Poisson process with a standard deviation close to its own mean — for ~50 matches at ~1 goal/match, the expected match-to-match noise in the *total* is on the order of 7 goals. A 6-goal gap is comfortably inside that band. Same story for the scoreless-match split (17 vs. 22 of 50): the sampling noise on a proportion this size is wide enough that this isn't distinguishable from chance either. **The honest conclusion is not "Control+1 makes scoring worse" — it's "even 50 matches can't detect a goals effect from this change, in either direction."** Given the dribble/tackle numbers moved so cleanly and the goal numbers didn't move at all reliably, that's now reasonably strong evidence the effect on goals, if any, is small enough not to be the lever worth pulling.

## A real, unwanted side effect this sample size actually did catch

**Red Cards jumped 44%** (32 → 46) and overall cards/match rose (1.92 → 2.04). This has a clean mechanical explanation, not a coincidence: Control also defends a *standard* Tackle attempt (the carrier rolls Control as Defense), so the same stat bump that helps attackers dribble past defenders **also makes it harder for defenders to win an ordinary Tackle** — their win rate dropped from 30.8% to 23.0%. More failed Tackle attempts means more Discipline draws, and at this volume that reliably shows up as materially more Reds, not just more noise. This is the one place this batch found a real, load-bearing consequence of the change: **Control+1 doesn't just fail to raise scoring — it broadly weakens standard defending too, as an unavoidable side effect of the stat being shared between the Dribble Challenge (Attack) and Tackle (Defense) rolls.**

## Bottom line

Two clean 50-match arms now agree: **Control+1 is not the lever.** It reliably does what it mechanically promises (easier dribbling, harder tackling) without reliably producing more goals, and it comes with a real, unintended cost — a lot more cards and send-offs, since it weakens ordinary defending as a side effect of weakening it against dribbles specifically. I'd park this one rather than merge it, and move to a lever that doesn't touch a stat shared between an attacking and a defending roll — the breakaway bonus die (Shot Range only, tied to *this same activation's* won challenge) or a final-third-specific escape-hex loosening both act only where the actual bottleneck seems to be, without this spillover into ordinary Tackle defense.
