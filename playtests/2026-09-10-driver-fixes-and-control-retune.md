# 2026-09-10 — Driver fixes (Clearance, hex-ranking, Full Press, Counter) and the resulting Control retune

**Scope:** Closes the P0–P2 punch list from `2026-09-08-base-game-review.md`. Four driver bugs fixed across `playtest-ai/driver.py` and `driver_base.py`; several rulebook consistency fixes; a third Control retune pass on `ROSTER_BASE` prompted by the last of the four fixes.
**Method:** Real, unmodified drivers, genuine per-match randomness (`sim.gen_random()`). N=200 batches at each step, run from scratch copies during development and re-confirmed against the canonical files before locking anything in.

## What was fixed, in order

1. **Goalkeeper "black hole."** Neither driver ever attempted a plain Pass or Clearance for a stuck ball carrier — only Tactic-Card bail-outs (One-Two/Backheel/Long Ball) existed, none available in the Base Game and only conditionally in Advanced. A confined goalkeeper's `best_hex` always equals its own hex (it can never leave its zone), so it held the ball indefinitely. Added `try_plain_pass_or_clearance` (§7's actual, always-available Pass/Clearance rule) as the true last resort, gated so it never fires when a legal Shot is already available from the current hex. Result: matches with a 3+ turn same-unit freeze streak went from the review's reported 42.5% (Base) to **0% in every batch since**.
2. **Broken hex-ranking.** `B.shot_dist()` is genuinely `None` for E3/E4/G3/G4 and ~20 other hexes — correct hex-grid geometry (the Net is only 3 hexes wide), not a bug. But ~9 call sites either skipped `None`-hexes outright or tied them at a flat sentinel when ranking candidates (best move, kickoff-release target, pass targets), silently falling back to dict/list iteration order and systematically undervaluing the board's most central, most-contested hexes. Fixed with a shared `rank_dist()` helper (real `shot_dist`, else `box_dist+0.5`, else 999).
3. **Full Press.** Previously modeled as free — activated all 5 units with neither its 2-turn card-discard debt nor its second Act ever applied. Both now work: `play_card` charges the debt (verified end-to-end against `sim.py`'s pre-existing, already-correct consumption logic in `replenish()`), and a new `followup_move_then_maybe_shoot` wrapper lets a genuinely new ball-carrier (one who received the ball via a landed Pass this turn) take the second Act — the "Pass-then-Shot" combo the card text names — without letting one unit act twice.
4. **Counter.** Was the Base Game's *only* remaining reaction and had never been modeled at all — Resolution Sequence steps 2 and 5 were empty in every Base Game batch ever run. Implemented the simpler of its two rules-text options (discard a held Counter to add 1 Defense die to the incoming roll), wired into all five contested-roll types via one `maybe_counter_die` helper. The other option (discard to force an immediate Tackle Challenge, cancelling the opponent's action outright) is explicitly *not* modeled — it needs its own nested Resolution Sequence, a separate piece of work.

Also fixed in the rulebook: the §1/§14 contradiction over whether the Base Game has Flair Points (it does — §14 was wrong, brought in line with §1 and with §8's Tackle-loss Flair cost, which is a Base Game rule); Keeper's Call's guaranteed bonus draw, previously impossible in the Base Game (now a Command Card draw there, a Tactic Card draw in Advanced); a "what the Base Game actually leaves out" box in §1 plus targeted notes at §5/§7/§12/§13/§17; `sim.py`'s "what this engine does not do" note, which was claiming a Free Kick restart existed when no such code has ever been written.

## The Control retune this forced

The 2026-09-08 roster retune (Control +2 for Sweeper/Wingback/Poacher) was tuned to hit ~53–56% dribble win rate. That number was measured on a driver missing all four fixes above. Once Counter existed, a clean N=200 Base Game batch read **48.4%** — a real, not noise-sized, gap.

Tried the obvious extension: more Control for the same three positions. Wingback and Poacher were already at **Control 5 — the documented ceiling for any stat in this game** (§8: "0–5, see §14"; no roster value has ever exceeded it). Only the Sweeper had headroom. Tested Sweeper 4→5 at N=200:

| | Dribble win rate | Tackle win rate | Goals/match |
|---|---|---|---|
| Post-Counter baseline (all 4 fixes, pre-retune) | 48.4% | 18.2% | 2.14 |
| + Sweeper Control 4→5 (scratch test) | 51.5% | 15.8% | 2.09 |
| **Final, canonical drivers, locked in** | **52.3%** | **17.3%** | **2.15** |

Still short of 53–56%. **Decision (user's call): keep the Sweeper move, stop retuning Control, and accept 48–52% as the correct figure for this ruleset** — not a regression from the old target, since that target predates most of what the engine now does. Raising the stat ceiling above 5, or cutting defenders' Tackle instead of raising Control, were both considered and explicitly declined for now.

## Final numbers, both tiers, N=200 (canonical drivers, 2026-09-10)

| | Base Game | Advanced Game |
|---|---|---|
| Goals/match | 2.15 | 2.48 |
| Dribble win rate | 52.3% | 60.8% |
| Tackle win rate | 17.3% | 15.5% |
| Shot conversion | 49.4% | 50.2% |
| GK freeze streak (3+ turns) | 0% | 0% |

`ROSTER_BASE` now: GK 2/0/2/2-—/2, SW 3/3/**5**/2-2/2, WB 2/3/5/3-2/3, PM 3/4/4/4-3/2, PO 4/5/5/1-4/2 (Pace/Shot/Control/Range-Pass-Shot/Tackle). `ROSTER` (Advanced) is still an identical copy, per the ongoing "one roster, both tiers, for now" decision (§14).

## What this doesn't cover

Counter's "force a Tackle Challenge" option remains unmodeled. The P3 design leads from the 2026-09-08 review — the receiver-hex formation swap (arm D: Poacher on E4/G4 tested at 2.25 goals/match, the healthiest position spread of anything tried) and the tackle-rate/stalling-incentive tradeoff — are both still open and untouched by this pass.
