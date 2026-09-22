# Hexside Playtest — Full Match: Tuned Discipline + Shot +1 Combined

**Date:** 2026-09-04
**Format:** Full standard match — 24 turns per side, halftime swap, 48 total
**Ruleset:** Current draft plus both experimental changes running together for the first time: the Standard Challenge Discipline pool (10 cards: 6 base + 4 Clean Challenge, standard Tackle draws once, Slide Tackle draws twice from the harsher 6) and Shot +1 across every outfield position (SW/WB 1→2, PM 2→3, PO 3→4).
**Sides:** Both aggressive, as in every full match this project has run.

**Final score: Team A 2 – 1 Team B.**

---

## The scoreline, and how it happened

Three goals, two saves — five genuine shots in 48 turns, more than either single-variable test managed on its own:

1. **Turn 4** — A's Playmaker (Shot 3, buffed from 2) breaks through two Zones of Control on the opening exchange and finishes from H2. **1-0.**
2. **Turn 11** — B's Poacher (Shot 4, buffed from 3) shoots from point-blank range after winning the ball back. **Saved.**
3. **Turn 40** — B's Sweeper (Shot 2, buffed from 1 — the *smallest* beneficiary of the buff) gets a shot away from distance 2. **Saved.**
4. **Turn 44** — Same Sweeper, same buffed stat, tries again from J3 right on the doorstep. **Goal — 1-1.**
5. **Turn 46** — A's Playmaker again, a clean break down the right after B over-committed, finishes from H4 for **2-1**, the winner.

Worth noting: three of the five shots came from units whose *base* Shot stat was low (PM at 2→3, SW at 1→2 twice) — exactly the units Shot+1 was meant to bring into range as credible finishers, not just the Poacher. That's a good sign for the buff on its own terms.

## The Discipline system, now genuinely load-bearing

15 Tackle attempts, 12 Discipline draws:

- **5 Clean Challenge** — the new card did exactly its job, repeatedly: a failed Tackle that clearly wasn't reckless, no consequence, on top of the usual Flair cost.
- **3 Warning**, **1 Advantage/Play On** — no effect either way.
- **2 Yellow Card** (B's Playmaker, A's Sweeper).
- **1 Red Card** (A's Poacher, turn 29) — still possible even from the softened 10-card pool (1-in-10 now, down from 1-in-6), and it still happened. Team A played from turn 29 onward — nearly 20 turns, well over a third of the match — a player down, and still won.

That's a much healthier spread than the standalone Discipline test: no single incident swallowed the whole match's shape this time, cards showed up on both sides, and the one Red that did land didn't decide the outcome by itself. The softened odds appear to be doing what they were tuned to do — Discipline is now a real, recurring presence without being the whole story of the match the way it was in the 24-turn Discipline-only test.

## Two real bugs, both caught and fixed mid-match

1. **A JSON-safety fix from the previous session held up correctly this time** — no tuple-key crash, confirming that fix was solid.
2. **A new bug, more serious: `goal_restart()` and `halftime_reset()` both rebuilt the full 5-unit default formation unconditionally**, which silently resurrected Team A's already-red-carded Poacher the moment Team A conceded (turn 44's restart). This had never surfaced before because no previous playtest had a Red Card land *before* a later restart in the same match — first time the two systems' interaction actually got exercised. Fixed by tracking sent-off units explicitly (`s['sent_off']`) and excluding them from the rebuilt formation in both restart functions, with a new `_kickoff_taker()` helper so a side missing its Forward doesn't try to send the Goalkeeper to the halfway line instead (a real rules edge case the written draft doesn't cover yet — worth an explicit ruling: right now the sim has the most attack-minded remaining outfield unit take the kickoff spot).

I caught this by noticing A's Poacher had reappeared in the printed state after a restart, despite being sent off 15 turns earlier — a state I should have specifically checked for right after implementing the Discipline tuning, since a Red Card interacting badly with a full-formation reset was a predictable risk once both systems existed together. Corrected on the spot: the erroneous Poacher was removed, the kickoff was reassigned to the Playmaker, and the underlying functions were fixed so this can't recur.

## Bottom line

This is the strongest match this project has produced by the numbers that matter: five real shots, three goals, a genuine one-goal margin, Discipline events on both sides without any one incident dominating, and a Red Card that mattered (a player down for a third of the match) without deciding the game outright. Both tuning passes look like they're pulling in the right direction together, not fighting each other. The kickoff-after-red-card rule is now a real open question worth a deliberate answer rather than a coded default, and it's the kind of edge case this project's approach (build, break it in play, fix it, write it down) keeps finding — which is the point.
