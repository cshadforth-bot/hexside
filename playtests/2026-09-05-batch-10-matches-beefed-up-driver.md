# Hexside Playtest — Batch of 10 Full Matches, Beefed-Up Driver

**Date:** 2026-09-05
**Format:** 10 independent full-length matches, 48 turns each (480 turns total), fresh coin flip and fresh shuffled decks/dice every match
**Ruleset:** Everything current — Shot Range/Net fix, Emergency Goalkeeper, Jockey, kickoff release, dynamic ball-carrier, GK confinement + opponent exclusion + Composure + Yellow sin-bin (today's Report-II merge)
**Purpose:** The previous few matches this session showed noticeably fewer cards than the other agent's "Hexside Match Report" (25 Yellow + 27 Red across 28 matches ≈ 1.86 cards/match). That gap turned out to be a test-harness artifact, not a rules difference — my driver never played **Foul** or **Press**, and rarely played **Slide Tackle**. This batch adds all three (Foul ~45% of the time when a unit is adjacent to a Dribble Challenge or Pass in progress; Press ~50% of the time when a non-activated defender is adjacent to the ball-carrier and 1 Flair is banked; Slide Tackle up from a 30% to 40% chance on any standard Tackle attempt) and reruns at volume to get a genuinely comparable dataset.

---

## Headline numbers, this batch vs. the earlier under-tested matches vs. Report I

| | This batch (10 matches) | This session's earlier matches (informal) | Report I (28 matches) |
|---|---|---|---|
| Cards (Yellow+Red) / match | **1.6** | ~0.5–1 | ~1.86 |
| Discipline draws / match | **6.7** | ~1–4 | ~8.0 |
| Goals / match | **0.5** | ~1–2 | (not directly comparable — different ruleset generation) |

Cards and discipline draws per match both landed much closer to Report I's numbers once Foul and Press were actually in play — not identical (different random draws, different exact heuristics, and Report I predates today's GK confinement/Emergency Goalkeeper/kickoff-release additions entirely), but the order-of-magnitude gap is gone. This confirms the diagnosis from earlier: **the underlying Discipline Deck odds were never the difference — how often the dice got rolled at all was.**

## Full per-match breakdown

| # | Score | Shots | Goals (auto) | Tackles (won) | Dribbles (won) | Discipline | Y | R | Foul | Press (won) | Slide | Sin-bin | Composure |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A 1–0 B | 1 | 1 (0) | 8 (3) | 6 (0) | 7 | 0 | 1 | 1 | 1 (0) | 0 | 0 | 0 |
| 2 | A 0–0 B | 1 | 0 | 10 (4) | 7 (0) | 6 | 0 | 0 | 0 | 1 (0) | 0 | 0 | 0 |
| 3 | A 0–0 B | 1 | 0 | 14 (3) | 13 (4) | 11 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| 4 | A 0–2 B | 3 | 2 (0) | 10 (3) | 16 (6) | 7 | 0 | 2 | 0 | 0 | 0 | 0 | 1 |
| 5 | A 0–0 B | 4 | 0 | 8 (3) | 3 (2) | 5 | 0 | 0 | 0 | 0 | 1 | 0 | 1 |
| 6 | A 0–1 B | 1 | 1 (0) | 8 (2) | 17 (5) | 6 | 1 | 0 | 0 | 0 | 0 | 1 | 0 |
| 7 | A 0–0 B | 1 | 0 | 6 (1) | 8 (0) | 6 | 3 | 1 | 1 | 0 | 0 | 3 | 0 |
| 8 | A 1–0 B | 3 | 1 (1) | 14 (7) | 10 (1) | 9 | 2 | 0 | 1 | 0 | 0 | 2 | 0 |
| 9 | A 0–0 B | 2 | 0 | 5 (3) | 6 (2) | 3 | 1 | 1 | 1 | 0 | 1 | 1 | 0 |
| 10 | A 0–0 B | 2 | 0 | 9 (2) | 10 (3) | 7 | 2 | 1 | 0 | 1 (1) | 0 | 2 | 0 |
| **Total** | | **19** | **5 (1)** | **92 (31)** | **96 (23)** | **67** | **10** | **6** | **4** | **3 (1)** | **2** | **10** | **2** |

Tackle win rate: 34% (31/92). Dribble win rate: 24% (23/96). All 10 matches ran clean — `check_no_overlap()` passed every time, zero exceptions, zero crashes, across 480 turns.

## Directly answering "why still low-scoring" with a bigger sample

**6 of the 10 matches finished 0–0.** Only 19 shots emerged from 480 turns despite 92 tackle attempts and 96 dribble challenges — the overwhelming majority of contested movement ends in a turnover before anyone reaches Shot Range, exactly the pattern flagged earlier today and independently by Report I. And of the 5 goals that did go in, only **1 was automatic** (an empty Goalkeeper Zone) — the other 4 were genuine contested Shot-vs-Save wins. That 20% automatic-goal share is a sharp drop from before GK confinement, when automatic goals were a much larger fraction of total scoring. Both effects compound in the same direction: fewer possessions survive to become a shot, and the shots that do happen almost always have to beat a real Save roll now.

## The three new mechanics, actually exercised this time

- **Foul** fired 4 times, and — as the rule promises — never once came back Clean Challenge (2 Reds, 2 Warnings across the 4 real draws), confirming the redraw-past-Clean-Challenge logic held under real play.
- **Press** fired 3 times, won once — a real forced Tackle Challenge using a non-activated defender, exactly as designed, including one instance where the won Press tackle immediately fed into a free follow-up Pass and a further dynamic-activation move.
- **Slide Tackle** fired twice (no cards drawn from either — the "successful slide carries no risk" clause holding both times).
- **Composure** fired twice, **Sin-bin** triggered 10 times across the batch (about 1/match, consistent with the ~10 real Yellow cards landed).

## Bottom line

The scoring rate is genuinely low under the current full ruleset, and this larger sample makes that harder to dismiss as noise — worth deciding whether that's the intended difficulty curve (a hard-won goal, the way Report I's own note put it) or a balance point to revisit now that automatic goals are almost entirely gone. The card-count gap from earlier today, on the other hand, is resolved: it was this driver's missing Foul/Press/Slide-Tackle usage, not anything about the rules themselves — with all three actually in play, the numbers land in the same neighborhood as the other agent's much larger dataset.
