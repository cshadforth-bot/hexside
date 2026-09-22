# Hexside Playtest — Full Match: Ball-Carrier Exception + Current Canon (48 Turns)

**Date:** 2026-09-04
**Format:** Full standard match — 24 turns per side, halftime swap, 48 total
**Ruleset:** Current canon (Shot +1, tuned Discipline with the Standard Challenge pool) **plus** the experimental "ball-carrier always activatable" rule from the earlier 24-turn test — still not written into the rulebook, being validated at full length before that decision.
**Sides:** Both aggressive, as in every full match this project has run.

**Final score: Team A 1 – 2 Team B.**

---

## Headline: the lockout fix holds at full length

**1 cycle in 47 recorded turns (~2.1%)** — and that one genuine lockout was the specific edge case the rulebook itself calls out as a legitimate rarity: a hand of exactly three Counters, which can never be played on your own turn regardless of any other rule. That's not a card-reach failure the new rule was supposed to fix — it's the one deadlock the designers already knew about and accepted. Excluding it, this match had **zero** "couldn't do anything with the ball" turns across a full 48-turn match, matching the clean result from the 24-turn test and confirming it holds up at full length, not just in a short sample.

For comparison: the baseline aggregate across the last several pre-fix playtests was ~21.7% of turns lost to lockouts, with some individual matches over 30%. This match landed at roughly a twentieth of that rate.

## The match itself: two Red Cards decided it

Team A conceded a Red Card in the first half (Playmaker, sent off turn 12, direct 1-in-6 draw) and a second in the third quarter (Poacher, second Yellow escalating to Red, turn 29) — finishing the match with only **3 units** (Goalkeeper, Sweeper, Wingback) against Team B's full 5. Despite that, Team A:

- Equalized at 1-1 in the second half via a Sweeper counter-attack that reached the goal box unmarked while the opposing Goalkeeper had wandered forward — a genuine escape-hex/thin-defense interaction, not a fluke.
- Forced 15 total Tackle attempts across the match and drew real value from the Standard Challenge pool doing its job: **5 Clean Challenge draws** kept several of A's own failed tackles from compounding into further cards, even while A was already down players.

Team B ultimately won it with a clean late breakaway (Poacher, turn 46, Shot 4 vs Save 3) after A's severely thinned defense couldn't cover the whole pitch. That's a believable, not a broken, outcome — a team playing two men down for most of a match losing to a side at full strength is exactly what should happen, and the fact that A could still equalize along the way says the numbers disadvantage was real but not a death sentence.

**Discipline tally:** 2 Red Cards (both Team A, one direct, one via second-Yellow), 1 Yellow, 5 Clean Challenge, 3 Warning, 1 Advantage/Play On, across 13 total draws from 15 Tackle attempts. Both Reds landed on the same side purely from how the dice fell in this particular match — nothing about the rule itself favors one side.

**Scoring:** 5 shots attempted, 3 goals (60% conversion) — consistent with the Shot+1 buff converting well once a shot is actually taken, matching the pattern from earlier Shot+1-specific tests.

## Two real bugs caught and fixed mid-match

1. **A shot-resolution error I made myself:** at turn 43, I ran a contested Shot roll for a unit standing in an empty goal box (Team B's Goalkeeper had wandered forward to press and never returned home). Per §7, an empty goal box means an automatic goal, no roll needed — I initially rolled it as a contested Shot and called it saved. Caught by checking actual unit positions against the box before trusting the result, corrected on the spot: the erroneous roll was discarded and the goal awarded properly (this is the 1-1 equalizer above).
2. **A `goal_restart()` bug specific to a depleted roster:** when Team A's normal kickoff-taker (Poacher) had already been sent off, the substitute kickoff-taker (chosen correctly by the existing `_kickoff_taker()` fallback logic) was left standing at its own normal formation hex instead of actually being moved to the kickoff spot F3 — meaning the restart briefly had nobody standing on the kickoff spot at all, with the ball just floating at an arbitrary defensive position. Fixed by explicitly relocating the substitute kicker to F3 as part of the restart, rather than trusting the formation template (which always assumes the Poacher is available).

## Bottom line

The ball-carrier exception passes its stress test: a full 48-turn match with two Red Cards, a numbers-disadvantage comeback, and heavy Tackle traffic still produced essentially zero lockouts. Recommend writing it into §5/§7 now as proposed, folding in the existing kickoff-specific carve-out. Separately, the two bugs this match surfaced (both in the simulation harness, not the rules themselves) are now fixed and worth carrying forward into any future playtest scripts.
