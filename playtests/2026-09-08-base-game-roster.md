# Hexside — The Base Game Roster (Base/Advanced split, locked in)

**Date:** 2026-09-08
**Status:** Merged to canon. `engine/sim.py` now carries both `ROSTER` (Advanced Game) and `ROSTER_BASE` (Base Game) as separate, permanent dicts — neither overwrites the other. `playtest-ai/driver_base.py` is a new permanent test driver alongside the existing `driver.py`. The rulebook (§1, §14) documents the two-tier structure and both roster tables.
**Purpose:** Following Opus's full-game review (`2026-09-08-full-game-review.md`), which flagged first-time-player complexity as a real problem, the decision was made to split Hexside into a **Base Game** (everything except the 13-card Tactic Deck) and an **Advanced Game** (Base + that deck) — the same structural pattern *Commands & Colors* itself uses. This report covers the specific problem that split created and how it was resolved: the Base Game, played with the *existing* roster and no Tactic Deck, is measurably flatter than the full game, and needed its own numbers rather than just having cards removed.

---

## The problem: removing the Tactic Deck alone leaves the game flatter

| | Advanced Game (N=200) | Base Game, unpatched roster (N=200) |
|---|---|---|
| Goals/match | 1.895 | 1.675 |
| Shots/match | 3.82 | 3.415 |
| **Dribble win rate** | 55.4% | **44.3%** |
| Cards/match | 1.97 | 1.42 |

The gap is almost entirely explained by dribble win rate: Nutmeg (any Flair face wins a Dribble Challenge outright) and Step-Over (reroll up to 2 dice on a loss) are both Tactic Cards that exist specifically to rescue a losing Dribble Challenge. Remove them and dribbling — the only way to advance the ball at all once cards are gone — gets meaningfully harder, which cascades into fewer shots and fewer goals. Simply printing "Base Game = ignore the Tactic Cards" on the existing roster would ship a worse game to exactly the players (new/casual) it's meant to welcome.

## Four variants tested, all N=200, all via a driver with the Tactic Deck disabled at the source (never dealt, never refilled — not patched per-card)

| | Advanced | Unpatched | Flat Control+1 | Weighted Control+1 | **Weighted Control+2 (chosen)** |
|---|---|---|---|---|---|
| Goals/match | 1.895 | 1.675 | 2.005 | 1.72 | **1.85 / 1.945†** |
| Shots/match | 3.82 | 3.415 | 3.905 | 3.51 | **3.68 / 3.77†** |
| Dribble win rate | 55.4% | 44.3% | 56.0% | 49.4% | **55.1% / 52.8%†** |
| Playmaker share of shots | 70.6%‡ | 70.6% | 75.7% | 65.2% | **62.9% / 58.1%†** |
| Tackle win rate | 25.0% | 25.9% | 21.4% | 23.6% | **18.8% / 20.2%†** |
| Scoreless matches | 20.0% | 23.5% | 19.0% | 24.5% | **19.0% / 16.0%†** |

†First figure from the scratch experiment; second from the confirming run through the real, permanent `driver_base.py` against the live engine (see below) — both shown since they're both genuine N=200 data points, not a revision.
‡Advanced Game's own N=200 run didn't separately track by-position share; using the unpatched Base Game figure as the reference point since nothing about removing the deck should shift *which* position dominates on its own.

**Flat Control+1** (all four outfield positions): fully recovered scoring (goals/match 2.005, dribble win rate 56.0%, both slightly *above* the Advanced Game) but made the Playmaker's existing dominance worse (70.6%→75.7% share of shots) — a flat bump compounds most for whoever already has the highest Control.

**Weighted Control+1** (Sweeper/Wingback/Poacher only, Playmaker untouched): fixed the balance problem well (75.7%→65.2%) but only half-recovered scoring (dribble win rate 49.4%, roughly halfway between the unpatched and fully-recovered figures) — the Playmaker is still the highest-volume carrier, so leaving it untouched still bottlenecks the whole team's advancement.

**Weighted Control+2 (chosen):** pushing the same three positions further, still leaving the Playmaker untouched, recovered scoring almost fully (dribble win rate 55.1%/52.8%, both close to the Advanced Game's own 55.4%) *while continuing to improve balance* rather than reopening it (Playmaker's share kept falling, to 62.9%/58.1%). Best result on both axes across all four variants tested.

## The chosen roster

Only Control changes, and only for three of the four outfield positions — everything else (Pace, Shot, Pass Range, Shot Range, Tackle, all Signatures) is identical to the Advanced Game roster.

| Position | Control (Advanced) | **Control (Base)** |
|---|---|---|
| Sweeper | 2 | **4** (+2) |
| Wingback | 3 | **5** (+2) |
| Playmaker | 4 | 4 (unchanged) |
| Poacher | 3 | **5** (+2) |

## By position (confirming N=200 run, real permanent driver)

| | Shots | Goals | Conversion | Share of shots |
|---|---|---|---|---|
| Sweeper | 197 | 87 | 44.2% | 26.1% |
| Wingback | 14 | 5 | 35.7% | 1.9% |
| Playmaker | 438 | 236 | 53.9% | 58.1% |
| Poacher | 105 | 61 | 58.1% | 13.9% |

Sweeper is now a genuine secondary scoring threat (over a quarter of the team's shots, up from being barely involved). Poacher has the best conversion on the roster. Wingback remains the least-involved position — but that was true in *every* variant tested today, tactics or not, so it reads as a separate issue (most likely its poor Pass Range and where it sits in the default formation) rather than something a Control retune was ever going to fix on its own. Worth its own look later.

## The honest cost

Tackle win rate falls further under this roster than in any other tested variant (25.9% unpatched → 18.8–20.2% here) — defenders are more often beaten outright when they do commit to a Tackle. Zone of Control and the escape-hex rule were already doing most of defense's real work rather than tackling in every version tested this session, so this reads as an acceptable trade for a livelier Base Game rather than a free one — but it's a real, deliberate trade, not a side effect that slipped through unnoticed.

## What's now real, not scratch

- `engine/sim.py`: `ROSTER_BASE` added alongside the existing `ROSTER` — the Advanced Game's roster is untouched.
- `playtest-ai/driver_base.py`: new permanent test driver, mirrors `driver.py` exactly except it plays `ROSTER_BASE` and never deals the Tactic Deck. Run it the same way (`python3 driver_base.py 200`, from inside `playtest-ai/`).
- Rulebook §1: a short note establishing the Base/Advanced split exists, pointing to §14.
- Rulebook §14: the Base Game Roster table, with the same rationale as this report in brief.

## Still open

- The Wingback's low involvement, independent of which roster is used — a formation or Pass Range question, not a Control one.
- What else, if anything, differs between Base and Advanced beyond the roster and the Tactic Deck itself (e.g., does Full Press's second-Act mechanic feel too strong without cards to compete with it for a turn's attention? Not tested here — this pass was scoped to the roster specifically).
- The Advanced Game's own numbers were not re-examined in this pass; they remain exactly as they were before the Base/Advanced split was introduced.
