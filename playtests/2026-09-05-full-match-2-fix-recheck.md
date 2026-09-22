# Hexside Playtest — Full Match #2: Rechecking the Emergency Goalkeeper Fix

**Date:** 2026-09-05
**Format:** Standard full length — 48 total turns (24 per side), halftime at turn 24
**Ruleset:** Everything current — seam columns, unified 12-card Discipline Deck, Tackle rebalance, Shot Range fix (real Net geometry), Emergency Goalkeeper (with the second-deputy fix from today's mechanic test), Jockey
**Purpose:** The prior full match ([2026-09-05-full-match-shot-range-emergency-gk-jockey.md](2026-09-05-full-match-shot-range-emergency-gk-jockey.md)) never triggered Emergency Goalkeeper or Jockey at all, and the fix for Emergency Goalkeeper's second-deputy bug was only confirmed in a targeted, engineered test ([2026-09-05-mechanic-test-emergency-gk-jockey.md](2026-09-05-mechanic-test-emergency-gk-jockey.md)). This match re-checks everything under genuine, non-engineered play.

**Final score: Team A 1 – Team B 1.**

---

## How this match was played

Turns 1–7 were driven by hand, turn by turn, exactly like every previous full match. From turn 8 on, both sides' turn-by-turn decisions (which card to play, which unit to move, where to advance, when to tackle) were made by a small heuristic driver script instead of by hand, to get through all 48 turns in one pass — **every dice roll, card draw, and rule resolution still went through the same real, unmodified engine functions** (`contest()`, `tackle()`, `apply_discipline()`, `save_stat()`, `reach()`, `enemy_zoc()`, real pre-generated dice/card streams). Nothing about outcomes was scripted; only the move-selection logic was automated. This is a step beyond the "targeted mechanic test" methodology used earlier today — that one engineered *positions* to force a trigger fast; this one just plays the whole match out and reports what actually happened, for better or worse.

## Headline: still no natural Red Card, so Emergency Goalkeeper is still unconfirmed in live full-match play

Only **one Discipline card with a real effect fell all match** — a Yellow Card on B's Sweeper (half 2). No second Yellow, no Red, on either side. That means **Emergency Goalkeeper never triggered this match either** — two full matches in a row now. This is consistent with the earlier full match's read: a Goalkeeper being sent off at all is a rare event by design (needs a lost Tackle + an unlucky Discipline draw, or a 2nd Yellow), and getting it to happen organically across 48 turns is still not guaranteed. The fix itself is not in doubt — the targeted mechanic test already exercised the exact bug (a deputy itself being sent off) directly against the real engine and confirmed it — but "does it come up in ordinary play" is still an open question the dice haven't answered yet.

**Jockey was also never drawn into either hand** this match, so it went untested live again as well, same as the previous full match.

## The Shot Range mechanism produced both goals again — via the same mechanism, with a new detail

- **B's opening goal (turn 1):** B's Poacher won a Dribble Challenge into the box and beat A's real Goalkeeper on a contested shot (Save 3) — a genuine, contested finish, not an empty-net one.
- **A's equalizer (turn 10):** A's Poacher won a Tackle against B's Goalkeeper *upfield* at J4 two turns earlier (turn 8), then drove into the vacated box at K3 for an automatic empty-net goal — box completely empty, Shot Range 4 covering it with a hex to spare (distance 1).

That second goal is worth flagging honestly: B's Goalkeeper ended up out at J4 because the automated driver's defensive logic doesn't know to keep a Goalkeeper anchored in its own box — it just chases the ball like any other unit. A human defender would very likely have kept the keeper home and challenged with an outfield unit instead. So this goal is a real, correctly-resolved instance of the Shot-Range-punishes-an-exposed-keeper mechanism the fix was built for, but it says more about the automated driver's lack of goalkeeping discipline than about the rule itself — worth knowing before reading too much into the scoreline.

## Other numbers

- **Tackles:** 9 attempted, 3 won (33%).
- **Dribble Challenges:** 13 attempted, 4 won by the attacker (31%).
- **Shots:** 4 total (2 contested, 2 automatic-empty-net).
- **Discipline draws:** 6 (5 Clean Challenge, 1 Yellow Card). Zero Reds.
- **Occupancy/state integrity:** `check_no_overlap()` passed after every single position change, all 48 turns — no collisions.
- Halftime correctly triggered right after turn 24, ends swapped, formations reset cleanly.

## A genuine process note worth fixing before the next automated match

Running the second half exposed a real ambiguity that hand-driven matches never surfaced: `halftime_reset()` correctly hands the ball to `new_kicker` (the side that didn't open the match), but neither the engine nor the rulebook says whether that side's turn is also guaranteed to be the very next turn played, or whether turn alternation just continues in raw sequence regardless of who "kicked off." In this match, raw alternation put the *other* side's turn immediately after halftime, one turn before the actual kicking side got to touch the ball it had just been given. It caused no rule violation here (the receiving side had no unit anywhere near the kickoff spot, so its turn was a harmless reposition), but it's a real gap worth closing explicitly — either in `halftime_reset()`'s docstring or in §14 — rather than leaving it to whoever drives a match to guess.

## Bottom line

The core systems (Tackle rebalance, Shot Range/Net geometry, unified Discipline Deck, halftime, restarts) all continued to hold up cleanly under a second full 48-turn match with zero state-integrity failures. Emergency Goalkeeper and Jockey remain validated only by the targeted mechanic test, not by live full-match play — two matches in a row haven't produced the Red Card or the Jockey draw needed to see them fire organically, which just reflects how rare their triggers are by design, not a problem with the fix.
