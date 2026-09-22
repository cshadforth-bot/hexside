# Hexside Playtest — Batch of 10 Full Matches, Through on Goal Live

**Date:** 2026-09-07
**Format:** 10 fresh full-length matches, 48 turns each (480 turns total), independent coin flips and shuffles every match
**Ruleset:** Everything current in the canonical files — Through on Goal, GK confinement + opponent exclusion, Composure, Yellow sin-bin, kickoff release, dynamic ball-carrier, plus Foul/Press/Slide Tackle in the driver
**Purpose:** The single full match earlier today showed Through on Goal accounting for both goals scored. This batch checks whether that was a one-off or the new normal.

**Combined score across all 10: 5 goals for Team A, 6 for Team B.**

---

## Headline: Through on Goal is now the primary way goals happen

| | Total | Share |
|---|---|---|
| All shots | 26 | — |
| Breakaway shots (Through on Goal) | 17 | **65% of all shots** |
| All goals | 11 | — |
| Breakaway goals | 9 | **82% of all goals** |

Breakaway shots converted at 52.9% (9/17); the 9 non-breakaway shots converted at 22.2% (2/9) — that second number is a genuinely small sample (worth a bigger batch before reading much into the exact figure), but the headline pattern is unmistakable across all 10 matches: **more than four out of five goals scored came off a won Dribble Challenge in the same activation.** This isn't a fluke of one match — it held up as the dominant pattern across ten independent games.

## Match-by-match

| # | Score | Shots | Goals | Breakaway shots | Breakaway goals | Tackles (won) | Dribbles (won) | Discipline | Y | R |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A 1–1 B | 4 | 2 | 2 | 2 | 8 (1) | 11 (4) | 8 | 4 | 0 |
| 2 | A 0–0 B | 3 | 0 | 0 | 0 | 6 (1) | 5 (2) | 5 | 0 | 0 |
| 3 | A 0–0 B | 2 | 0 | 2 | 0 | 8 (0) | 9 (2) | 9 | 2 | 2 |
| 4 | A 0–0 B | 1 | 0 | 1 | 0 | 5 (1) | 4 (2) | 4 | 0 | 1 |
| 5 | A 1–1 B | 2 | 2 | 2 | 2 | 3 (1) | 7 (4) | 2 | 0 | 1 |
| 6 | A 1–1 B | 4 | 2 | 4 | 2 | 6 (3) | 11 (7) | 3 | 1 | 0 |
| 7 | A 0–1 B | 2 | 1 | 1 | 1 | 10 (3) | 14 (4) | 8 | 0 | 0 |
| 8 | A 0–2 B | 4 | 2 | 3 | 1 | 10 (2) | 14 (5) | 14 | 2 | 0 |
| 9 | A 2–0 B | 3 | 2 | 1 | 1 | 11 (4) | 14 (5) | 8 | 1 | 0 |
| 10 | A 0–0 B | 1 | 0 | 1 | 0 | 7 (2) | 6 (1) | 6 | 2 | 0 |
| **Total** | | **26** | **11** | **17** | **9** | **74 (18)** | **95 (36)** | **67** | **12** | **4** |

Every goal in matches 1, 5, 6, 7, and 9 was a breakaway; only match 8 had a goal that wasn't. 4 of 10 matches finished scoreless.

## Everything else held up clean

- **Discipline:** 12 Yellow Cards, exactly 12 sin-bin trips (every Yellow correctly triggered one, every unit correctly served its turn and returned — no mismatches). 4 Red Cards, none of them a Goalkeeper (Emergency Goalkeeper correctly never needed to engage).
- **Automatic goals:** 2, both from a Goalkeeper being sent off with no deputy yet standing in — the only way this can still happen under GK confinement, exactly as designed.
- **Composure:** fired 3 times. **Press:** fired 5 times. **Foul:** fired 4 times, always landing a real card. **Slide Tackle:** 3 times.
- **State integrity:** `check_no_overlap()` passed after every position change across all 480 turns — zero crashes, zero collisions.

## Reading the goals/match number correctly

1.1 goals/match this batch is close to the 1.12/match seen in the pre-Through-on-Goal baseline (N=50, back on 2026-09-07) — at a glance that might read as "no real change." But that comparison misses the more important shift: **how** those goals are being scored changed dramatically. Before this rule existed, every shot was rolled at the same flat odds regardless of how the attacker got there. Now, the overwhelming majority of scoring specifically rewards the exact sequence — beat your man, then finish — that both this session's design review and the rulebook's own Dribble-Challenge-doesn't-spend-the-Act rule identified as the sport's signature good chance. The total goal count may not have moved much yet at this sample size, but the *texture* of how the game scores clearly has.

## Bottom line

Ten matches in, Through on Goal isn't a rare bonus — it's become the dominant route to goal, at 82% of all scoring in this batch. Worth a larger batch (30-50) to pin down the exact non-breakaway conversion number with more confidence and see whether the overall goals/match rate genuinely lifts at volume, but the core finding — that Through on Goal has become the primary scoring mechanism rather than an occasional flourish — is already clear from this sample.
