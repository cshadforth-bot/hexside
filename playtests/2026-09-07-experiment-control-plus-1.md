# Hexside Experiment — Control +1 Across the Roster (engine-only, not merged to the rulebook)

**Date:** 2026-09-07
**Status:** Test only — `sim.py`'s `ROSTER` was edited in a throwaway scratch copy for this run, then discarded. The canonical `sim.py`/`board.py`/rulebook are untouched.
**Change tested:** Flat +1 Control for every outfield position — SW/WB/PO 2→3, PM 3→4. Goalkeeper Control left at 2 (it barely dribbles under confinement, and wasn't the target of the fix). Everything else identical to the batch run two days ago: same beefed-up driver (Foul, Press, Slide Tackle all live), same 10-match format.
**Purpose:** Direct comparison against the 2026-09-05 batch of 10, to test whether loosening the Dribble-Challenge/Tackle-defense odds in the attacker's favor increases goal count, per option #1 from the earlier scoring discussion.

**Result: no detectable change in scoring.**

---

## The stat moved exactly as predicted — the goals didn't follow

| | Baseline (2026-09-05, unmodified Control) | This test (Control +1) |
|---|---|---|
| Dribble Challenges won by attacker | 23 / 96 (**24%**) | 41 / 95 (**43%**) |
| Tackles won by defender | 31 / 92 (**34%**) | 17 / 82 (**21%**) |
| Shots taken | 19 | 20 |
| Goals | 5 | 5 |
| Goals / match | 0.5 | 0.5 |
| Scoreless matches | 6 / 10 | 6 / 10 |
| Shot conversion | 26% | 25% |

Control is rolled on **both sides** of two different contests — Attack in a Dribble Challenge, Defense in a standard Tackle (the rulebook is explicit: "the ball-carrier rolls Control as Defense"). Bumping it did exactly what the math predicted on both: dribbling past a defender got much easier (24%→43%), and getting tackled off the ball got much harder for the carrier (34%→21%, i.e. tackles succeeding against them dropped). Whichever side currently holds the ball got measurably better at both keeping it and advancing it.

**None of that translated into more shots or more goals in this sample.** Shots ticked up by one; goals were identical, right down to the same 6-of-10 scoreless split.

## Why this probably happened — two live possibilities, not resolved by this run

1. **Small-sample noise.** 10 matches is a thin sample for a genuinely rare event — 5 goals either way is well within the range where the "true" underlying rates could be identical, or could differ by a modest amount this batch size just can't resolve. The dribble/tackle percentages moved by huge, unambiguous margins (double-digit swings on ~90-95 attempts each) precisely because those events are common enough for 10 matches to say something real; goals aren't.
2. **The bottleneck may not be per-contest odds at all.** Surviving individual Dribble Challenges and Tackles more often means a team holds the ball longer and advances more per turn — but that doesn't automatically mean more of those extra turns land inside Shot Range specifically. A team can win its skirmishes all match and still spend most of that possession maneuvering through midfield rather than breaking into the final third's tighter Zone-of-Control geometry. If that's the real shape of the bottleneck, a stat buff that helps *everywhere* won't concentrate its benefit where it's actually needed — reaching the box — the way a positional or final-third-specific change would.

## Bottom line — not implemented, not ruled out

This one data point doesn't clear the bar to recommend merging Control+1 into the canonical rulebook: it did what it was supposed to do to the contests it touches, but didn't move the number we actually care about, at least not detectably at this sample size. Two reasonable next steps, not mutually exclusive:
- **Run it at real volume** (30-50 matches) to find out whether there's a real, small goals effect hiding under this sample's noise.
- **Try a more targeted lever instead** — option #3 (a breakaway bonus die for shooting right after winning a Dribble Challenge/Tackle in the same activation) or option #4 (loosen the escape-hex rule specifically inside the attacking third) both aim directly at converting survival into a shot, rather than making survival itself more likely everywhere.
