# Hexside Playtest — Batch of 50, Final Roster, All 13 Tactic Cards Live

**Date:** 2026-09-08
**Format:** 50 fresh full-length matches, 48 turns each (2,400 turns total), independent coin flips, shuffles, and dice every match
**Ruleset:** The full current canonical ruleset as merged today — Shot +1 across the outfield (again, stacking on the earlier +1), Control/Pass Range raised for the Playmaker and (via the swap) the Wingback, the Sweeper/Wingback full stat-line swap with Signatures swapped to match, plus everything already canonical (Through on Goal, GK confinement + opponent exclusion, Composure, Yellow sin-bin, kickoff release, dynamic ball-carrier)
**Purpose:** Validate the merged roster at real volume, and — for the first time — give the test driver logic for all 13 Tactic Cards rather than just 5. Two prior batches this session (N=50 with 5 cards modeled, goals/match 1.94) only ever exercised Foul, Press, Composure, Slide Tackle, and Jockey; Through Ball, Nutmeg, Step-Over, Curl Shot, One-Two, Backheel, Long Ball, and Last Ditch Block were drawn into hand but never played. This batch adds AI logic for all 8 of those and re-runs.

**Validation:** smoke-tested at N=3 and N=15 before committing to the full N=50 — no crashes, `check_no_overlap()` passed after every position change across all 2,400 turns, and by N=50 every one of the 13 cards had fired at least once (confirming the three rarest — Through Ball, One-Two, Backheel — are genuinely uncommon in this driver's play, not silently broken).

---

## Headline: goals/match rose again, but this run isn't a clean isolated read

**Mean: 2.02 goals/match** (101 goals across 50 matches — 67 for Team A, 34 for Team B). Shots/match 3.74, shot conversion 54.0%, 20% of matches scoreless (10/50).

| Goals in a match | # of matches |
|---|---|
| 0 | 10 |
| 1 | 12 |
| 2 | 8 |
| 3 | 11 |
| 4 | 6 |
| 5 | 2 |
| 6 | 1 |

For context against the same roster with only 5 cards modeled (also N=50, run earlier today):

| | 5 cards modeled | **All 13 cards modeled** |
|---|---|---|
| Goals/match | 1.94 | **2.02** |
| Shots/match | 3.32 | **3.74** |
| Shot conversion | 58.4% | 54.0% |
| Scoreless matches | 22% | **20%** |
| Cards/match | 1.88 | 1.70 |

Worth being explicit about a limit here: this run adds 8 new mechanics **simultaneously**, and 7 of the 8 are Attack-tagged (only Last Ditch Block defends) — so the shots/goals increase reflects the combined effect of the whole ruleset finally being used, not an isolated, single-variable finding the way Control+1/Pace+1/Shot+1 were each tested earlier this session. Treat the rise as "the full game plays livelier than the partial-AI read suggested," not as a precise measurement of any one card's contribution.

## By position

| | Shots | Goals | Conversion |
|---|---|---|---|
| Sweeper | 21 | 11 | 52.4% |
| Wingback | 3 | 2 | 66.7% |
| Playmaker | 139 | 72 | 51.8% |
| Poacher | 24 | 16 | 66.7% |

Small but real news for the Wingback: **0 shots in every prior batch this session, 3 shots / 2 goals here.** Long Ball and One-Two between them evidently give it occasional routes forward that plain dribbling never did. The Playmaker still dominates volume by a wide margin (139 of 187 shots, 74%) — Control remains the deciding factor in who gets forward, as established earlier.

## Cards

| | Total | Per match |
|---|---|---|
| Yellow | 52 | 1.04 |
| Red (sent off) | 33 | 0.66 |
| **Combined** | **85** | **1.70** |
| Sin-bin trips | 52 | 1.04 |

## Tactic Card usage — all 13 modeled for the first time

| Tactic Card | Times played | Per match |
|---|---|---|
| Step-Over | 47 | 0.94 |
| Nutmeg | 34 | 0.68 |
| Curl Shot | 31 | 0.62 |
| Press | 28 | 0.56 |
| Slide Tackle | 28 | 0.56 |
| Last Ditch Block | 25 | 0.50 |
| Foul | 22 | 0.44 |
| Jockey | 19 | 0.38 |
| Composure | 11 | 0.22 |
| Through Ball | 10 | 0.20 |
| Long Ball | 8 | 0.16 |
| One-Two | 6 | 0.12 |
| Backheel | 3 | 0.06 |

### A real finding, not a driver bug: Nutmeg is crowding out the cheaper cards

Nutmeg, Step-Over, Curl Shot, and Last Ditch Block are each played by this driver's AI on an "always play if it helps and you can afford it" basis (deterministic, matching how Composure already behaved before today) — there's no strategic held-back judgment call modeled, unlike Foul/Press which use a probabilistic gate. Because Nutmeg only needs a single Flair face anywhere in the roll to win a Dribble Challenge outright, it's almost always worth taking when available — but at 2 Flair a time, against a shared bank that also has to fund Step-Over, Curl Shot, Last Ditch Block, One-Two, Backheel, and Long Ball, it likely soaks up Flair before the cheaper 1-cost cards (Through Ball, One-Two, Backheel) get a turn. That's consistent with the usage table: the two most expensive "always-play" cards (Nutmeg, Curl Shot, both cost 2) rank near the top, while the cheap positional cards (One-Two, Backheel, both cost 1 but need a narrower positional trigger) sit at the bottom. Worth remembering if Flair income is ever retuned — it would reshuffle this whole pecking order, not just make everything fire more often.

### Three cards are genuinely rare in this driver's play, confirmed not broken

Through Ball (10 plays), One-Two (6), and Backheel (3) all showed 0 across the first N=3 and N=15 smoke tests, which was enough to warrant a closer look before trusting the N=50 number — but all three fired by the full batch, and their trigger conditions were re-checked line by line. One-Two and Backheel both require a teammate to be immediately adjacent to the ball-carrier's own hex before it moves, which is a narrow condition in this driver's spread-out play patterns; Through Ball only has something to do when a pass is contested by exactly one Zone of Control in the first place, which many of this driver's already-well-positioned pass targets simply aren't.

## Implementation notes and simplifications

A few of these 8 cards needed simplified approximations to implement at the driver level, all documented in the driver's own comments:

- **Step-Over** ("reroll up to 2 dice") is approximated as "roll 2 fresh dice and add any hits" rather than literally rerolling 2 specific dice from the original pool — the same simplification the existing Composure code already used for its own single-die reroll.
- **Nutmeg** needed Dribble Challenges to go through a new `dribble_contest()` helper that calls `sim.roll()` directly (to see actual dice faces) instead of the usual `sim.contest()`, which only returns hit counts.
- **Through Ball** ("ignores one defending unit's Zone of Control") is treated as clearing the pass's contest entirely — exact when only one Zone of Control contests the line, which is the common case here, but a slight overstatement on the rare occasion two do.
- **One-Two, Backheel, and Long Ball** required genuinely new logic — previously the driver only ever modeled a Pass at two specific trigger points (kickoff release, the free follow-up after a won Tackle); it never modeled the ball-carrier choosing to pass instead of dribble during a normal carry. All three are gated on beating the already-computed normal route (One-Two, Long Ball) or the normal route being fully stuck (Backheel), matching this session's established risk-aware, not-reflexive design principle for optional plays.
- **Last Ditch Block** is sequenced after the shooting/passing side's own post-roll reaction (Composure), matching the rulebook's explicit step 4 (active player) → step 5 (opponent) ordering.

## Bottom line

The final roster holds up at real volume with the full Tactic Card suite finally in play: 2.02 goals/match, a livelier goals-per-match spread than any earlier batch this session (2-goal and 3-goal matches are now both more common than a 0-0 draw), and — for the first time — all five positions have registered at least one shot. The Flair-competition dynamic among the newly-modeled cards is worth keeping in mind for any future tuning pass, and the three rarest cards (Through Ball, One-Two, Backheel) are confirmed genuinely uncommon in this AI's play rather than broken, though a human table is very likely to find more use for them than this driver's fairly mechanical heuristics do.
