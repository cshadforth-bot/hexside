# Hexside Playtest — Batch of 40 Full Matches, Goals-per-Match Summary

**Date:** 2026-09-08
**Format:** 40 fresh full-length matches, 48 turns each (1,920 turns total), independent coin flips and shuffles every match
**Ruleset:** Everything current — Through on Goal, GK confinement + opponent exclusion, Composure, Yellow sin-bin, kickoff release, dynamic ball-carrier, Foul/Press/Slide Tackle
**Purpose:** A goals-per-match summary at real volume, following on from the 10-match batch two days ago.

---

## Goals per match: the distribution

| Goals in a match | # of matches | % of matches |
|---|---|---|
| 0 | 12 | 30% |
| 1 | 20 | 50% |
| 2 | 5 | 12.5% |
| 3 | 2 | 5% |
| 5 | 1 | 2.5% |

**Mean: 1.03 goals/match. Median: 1 goal/match.** 41 total goals across 40 matches, 25 for Team A and 16 for Team B (no side asymmetry built into the ruleset — that split is this batch's own coin-flip and dice variance, not a bias). The most common outcome by far is a single goal deciding — or not deciding — the match; a third of matches stay scoreless, and a genuine multi-goal match (3+) happened 3 times in 40, including one 5-goal outlier.

## Through on Goal, at this larger sample

| | This batch (N=40) | 10-match batch (2026-09-07) |
|---|---|---|
| Breakaway share of shots | 48.9% | 65.4% |
| Breakaway share of goals | 58.5% | 81.8% |
| Breakaway shot conversion | 53.3% | 52.9% |
| Non-breakaway shot conversion | 36.2% | 22.2% |

The two batches' breakaway-conversion numbers agree closely (53.3% vs. 52.9%) — that's now a well-supported figure. The *share* of shots/goals that are breakaways came down somewhat at this larger sample (roughly half rather than two-thirds/four-fifths), which is the expected effect of a bigger, less noisy sample settling toward a more representative rate rather than the smaller batch's lucky streak. **Combined across both batches (50 matches total): 33 of 52 goals (63%) were breakaways** — still comfortably the majority scoring mechanism, just not quite as overwhelming as the first 10-match look suggested.

## Supporting numbers

- **Shots/match:** 2.3 (92 shots, 40 matches). **Shot conversion overall:** 44.6% (41/92).
- **Tackles:** 333 attempted, 120 won (36%). **Dribble Challenges:** 370 attempted, 121 won by the attacker (33%).
- **Discipline:** 6.4 draws/match, 1.475 cards/match (41 Yellow, 18 Red) — every Yellow correctly produced exactly one sin-bin trip (41 Yellows, 41 sin-bin trips).
- **Automatic goals:** 4 across 40 matches — all from a Goalkeeper sent off with no deputy yet standing in, the only route left under GK confinement.
- **State integrity:** `check_no_overlap()` passed after every position change, all 1,920 turns — zero crashes, zero collisions.

## Bottom line

At 40 matches, goals-per-match settles right around 1 — a single goal is the modal, median, and near-mean outcome, with real variance either side (12 scoreless matches, 8 with two or more). Through on Goal's conversion advantage (53% vs. 36%) is now backed by good sample size and holding steady across two independent batches, and it remains the majority route to goal even once the sample got big enough to pull back from the smaller batch's more extreme share.
