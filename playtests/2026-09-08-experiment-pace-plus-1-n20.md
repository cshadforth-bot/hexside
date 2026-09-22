# Hexside Experiment — Pace +1 Across the Roster (Goalkeeper excluded), N=20

**Date:** 2026-09-08
**Status:** Test only, engine-side — nothing in the canonical `sim.py`/`board.py`/rulebook was touched, as asked. `ROSTER` was patched in a throwaway scratch copy, then discarded.
**Change tested:** Pace +1 for every outfield position — Sweeper 2→3, Wingback 3→4, Playmaker 3→4, Poacher 4→5. Goalkeeper left at 2 (confined to a 3-hex zone regardless, so extra Pace there wouldn't do anything).
**Baseline for comparison:** the 40-match batch from 2026-09-08, same driver, same everything else.

**Result: shots per match didn't move at all — the hypothesis behind this test didn't pan out, and the small goals bump this batch shows is more likely noise than a real effect.**

---

## Headline comparison

| | Baseline (N=40, current Pace) | Pace +1 (N=20) |
|---|---|---|
| **Shots / match** | **2.30** | **2.30** |
| Goals / match | 1.03 | 1.15 |
| Shot conversion | 44.6% | 50.0% |
| Dribble win rate | 32.7% | 34.6% |
| Tackle win rate | 36.0% | 26.3% |
| Cards / match | 1.48 | 2.00 |
| Discipline / match | 6.40 | 7.55 |
| Scoreless matches | 30% | 35% (7/20) |

## The core hypothesis didn't hold up

The whole reason to test Pace was the theory that more ground covered per activation should mean more turns actually reach Shot Range instead of stalling in transit — directly attacking the frequency bottleneck that Control+1 and Through on Goal both left untouched. **Shots/match came back identical: 2.30 either way.** More Pace didn't get more possessions to a shooting position at all in this sample.

The likely reason, worth recording since it's a useful structural insight: extra Pace only pays off *after* a unit has already won its one Dribble Challenge for the activation — from there it carries through free for the rest of its Pace (§8's existing rule). It doesn't reduce how many separate defensive "gates" (opposing Zones of Control) a possession has to survive *across turns*, since defenders reposition between activations and a fresh gate is usually waiting on the next one regardless of how far the previous turn's burst carried. Pace lets you cover more ground once you're through a gate; it doesn't get you through more gates.

## The goals bump is very likely noise, not a real effect — here's the tell

Goals/match did tick up (1.03→1.15), but two things argue against reading that as real:

1. **Shots didn't increase, so the extra goals would have to come purely from conversion** — and conversion did rise (44.6%→50%), but only from 46/92 attempts to a smaller N=20 sample of 23/46. That's a thin base to hang a real finding on.
2. **Tackle win rate moved by 10 points (36%→26%) despite Pace having no mechanical connection to a Tackle Challenge at all** — Tackle is Tackle(Attack) vs. Control(Defense), neither of which this change touched. A stat with zero causal link moving by a similar magnitude to the ones being tested is the clearest possible sign that N=20 still carries enough natural variance to produce swings like this from chance alone, in both directions.

## Side effect, same shape as Control+1, smaller so far

Cards/match rose (1.48→2.00) and Reds specifically look elevated (11 in 20 matches vs. 18 in 40 — roughly double the rate). Worth watching if Pace is revisited: a faster roster generally means more units end up adjacent to each other more often, which likely means more Tackle/Press opportunities and more Discipline exposure, independent of whether it helps scoring. Not as clean a mechanical explanation as Control+1's shared-stat problem, but the direction is the same and worth keeping an eye on rather than dismissing.

## Bottom line

This doesn't clear the bar either. Shots/match — the actual metric this test was designed to move — didn't budge, and the one number that did move (goals) doesn't have a clean causal story once a mechanically-unrelated stat (Tackle win rate) is shown moving by a comparable amount in the same small sample. Two broad-stat levers (Control, now Pace) have both failed to touch shot frequency. That's a meaningful pattern on its own: whatever's gating how many possessions reach Shot Range, it isn't being fixed by making the roster generically better at any one existing stat. The escape-hex loosening in the attacking third — which directly targets *where* possessions currently die, rather than making every unit marginally better everywhere — is still the untested candidate most likely to actually move shots/match, and I'd recommend it as the next thing to try rather than pushing Pace further.
