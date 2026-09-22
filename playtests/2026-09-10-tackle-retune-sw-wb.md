# 2026-09-10 — Sweeper/Wingback Tackle +1 each (a fourth, separate lever from Control)

**Scope:** `ROSTER_BASE` in `engine/sim.py`. Follows the same day's Control retune (`2026-09-10-driver-fixes-and-control-retune.md`); this is a genuinely different stat, tested and locked in separately.
**Trigger:** a direct question about a specific matchup — what are a Poacher's actual odds dribbling past a Sweeper at the numbers the Control retune left behind? Computed exactly (dice-face probability, not simulated): **Poacher (Control 5) past Sweeper (Tackle 2) ≈ 65%**; the reverse, Sweeper actively Tackling Poacher, **≈ 11%**. That read as too low for a stat whose whole job is stopping people.

## What was tried, in order

1. **Sweeper/Wingback Control −1, Tackle +1 each** (keeping a rough "budget"): dribble win rate 52.3%→47.2%, tackle win rate 17.3%→20.7%, but **Playmaker's goal share rose** (51.6%→53.3%) and Sweeper itself became easier to dispossess (Control also defends a Tackle Challenge). Rejected.
2. **Every dice-count stat capped at 4** (Sweeper/Wingback/Poacher Control 5→4, Poacher Shot 5→4): goals/match 2.15→2.02, but **Playmaker's goal share jumped to 64.1%** and Poacher's shot conversion collapsed (~65%→48.8%). Rejected — removing the stats that were specifically compensating for Playmaker's positional advantage left Playmaker relatively stronger, not more balanced.
3. **A broader "gut feel" reshuffle** (Control: GK 2, SW 3, WB 3, PM 4, PO 3; Tackle: GK 3, SW 2, WB 3, PM 2, PO 2; Shot: PM 4→3): tackle win rate genuinely rose (17.3%→22.2%) but goals/match fell to 1.69 (below the original pre-retune 1.68 floor) and Playmaker's share rose again (62.7%) — the Control cuts were doing the same damage as attempt 1, just spread across three positions.
4. **Isolated: GK Tackle 2→3 alone** (+ PM Shot 4→3): tackle win rate barely moved (17.3%→16.9%) — confirmed the Goalkeeper is too rarely in a position to Tackle at all (confined to its own 3-hex zone) for its own Tackle stat to matter at the aggregate level.
5. **Isolated: Sweeper/Wingback Tackle +1 each, Control and everything else untouched, PM Shot also cut to 3**: tackle win rate up (19.1%), Playmaker's share down (45.3%), but goals/match fell hard (1.72).
6. **Same, without the PM Shot cut** — the change actually kept: tackle win rate up, Playmaker's share down, goals/match cost much smaller. See below.

## The kept change: Sweeper Tackle 2→3, Wingback Tackle 3→4, nothing else touched

Two independent N=200 batches (pooled N=400) on the scratch variant, then a third, independent N=200 on the canonical drivers after locking it in:

| | Canonical (pre-change) | Test run 1 | Test run 2 | Pooled (1+2, N=400) | **Canonical, post-lock, N=200** |
|---|---|---|---|---|---|
| Tackle win rate | 17.3% | 18.8% | 18.1% | 18.5% | **19.6%** |
| Dribble win rate | 52.3% | 50.2% | 47.9% | 49.0% | 48.8% |
| Goals/match | 2.15 | 2.06 | 1.84 | 1.95 | 1.91 |
| Playmaker goal share | 51.6% | 49.5% | 45.5% | 47.6% | **51.6%** |
| Sweeper goal share | 24.2% | 29.9% | 31.9% | 30.8% | 28.8% |

**Tackle win rate is the one number that held up consistently across all four independent samples** — every run shows it up 1.5–2.3 points from the 17.3% baseline, and the direction never reversed. That's the real, load-bearing effect, and the actual mechanism matters: Sweeper and Wingback winning more Tackle Challenges themselves means *they* end up with the ball (and its free follow-up Pass) more often, which is a genuinely different and more effective lever on Playmaker's dominance than anything tried on Control ever was — attempts 1–3 above all made Playmaker *more* dominant by weakening its competition without touching it; this is the one change that made it *less* dominant, in 3 of 4 runs.

**Playmaker's goal share and goals/match are noisier than they first looked.** The two scratch test runs (49.5% and 45.5%) suggested a clean, sub-50% result; the pooled N=400 estimate was 47.6%. But the third, independent confirmation batch — on the canonical drivers, after locking the change in — came back at 51.6%, statistically indistinguishable from the pre-change baseline. Likewise goals/match ranged from 1.84 to 2.06 across the three N=200 samples (1.91 on the final canonical run) — a real, consistent ~0.15–0.3 cost versus the 2.15 baseline, but not a number precise to two decimal places at this sample size.

**Honest read:** lock in the Tackle change for what's actually robust across four samples — genuinely better defending, at a real but modest scoring cost — and don't oversell the Playmaker-balance number specifically; it moved the right direction in most runs but isn't a settled, reliable win on its own the way the tackle-rate change is. The formation-based fix (moving the receiver hex away from Playmaker, still on the punch list from the 2026-09-08 Base Game review) remains the more directly targeted lever for that specific problem if it needs solving further.

## What was explicitly rejected and why

- Cutting Sweeper/Wingback's Control to "pay for" the Tackle increase (attempts 1 and 3): makes Playmaker relatively stronger, not weaker, and makes Sweeper/Wingback themselves easier to dispossess.
- Capping every dice stat at 4 as a blanket rule (attempt 2): removes load-bearing compensation (Poacher's Shot, everyone's post-Counter Control) without anything replacing it.
- Raising Goalkeeper's Tackle (attempt 4): too low-leverage — it's rarely in a position to use it.
- Cutting Playmaker's Shot alongside the Tackle change (attempts 3 and 5): tested, worked exactly as a Shot cut should (lower conversion, same opportunity share), but cost another ~0.3 goals/match for no meaningful extra balance benefit once Tackle was isolated on its own. Left at its current value.

## Final roster, `ROSTER_BASE` (= `ROSTER`, Advanced, per the ongoing unification)

| Position | Pace | Shot | Control | Range (Pass/Shot) | Tackle |
|---|---|---|---|---|---|
| Goalkeeper | 2 | 0 / Save 3 | 2 | 2 / — | 2 |
| Sweeper | 3 | 3 | 5 | 2 / 2 | **3** (was 2) |
| Wingback | 2 | 3 | 5 | 3 / 2 | **4** (was 3) |
| Playmaker | 3 | 4 | 4 | 4 / 3 | 2 |
| Poacher | 4 | 5 | 5 | 1 / 4 | 2 |
