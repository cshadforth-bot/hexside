# Hexside Playtest — Full Match: Shot Range Fix, Tackle Rebalance, Emergency GK, Jockey

**Date:** 2026-09-05
**Format:** Standard full length — 24 turns per side, halftime at turn 24 (correctly timed this match), 48 total
**Ruleset:** Everything current — seam columns, unified 12-card Discipline Deck, Tackle rebalance (GK/PM/PO up to 2), Shot Range fix (real Net geometry, +1 across the outfield roster), Emergency Goalkeeper, Jockey replacing Offside Trap
**Sides:** Both playing for real chances, full Tactic Deck live throughout.

**Final score: Team A 1 – Team B 1.**

---

## Headline: zero lockouts, and Tackle finally works

**0 cycles in 48 turns (0%)** — the lockout fix continues to hold at full standard length under the complete current ruleset.

**The Tackle rebalance is the story of this match.** 18 total Tackle attempts, **10 successful (55.6%)** — a night-and-day change from the two most recent matches, where a combined 25 attempts produced *zero* successes. Both goalkeepers won tackles this match (B's GK won one outright at turn 28, using its bumped Tackle 2), and the run of even, back-and-forth possession battles in midfield felt like genuine contests rather than a coin flip stacked against whoever was pressing. This is exactly the outcome the stat change was aiming for.

## The Shot Range fix produced both goals — via the mechanism it was built for

Both goals this match were **automatic empty-net goals**, not contested shots — and both happened because a team won the ball back deep in the opponent's half (via a tackle) and had a unit with enough Shot Range to reach goal from distance, exploiting a keeper who'd been pulled out of position defending:

- **Turn 37 (A, 1-0):** A's Poacher won a tackle at C4 — 3 hexes from goal A — with B's Goalkeeper caught upfield at B4 after being tackled out of the box two turns earlier. Automatic goal, Shot Range 4 covering it comfortably.
- **Turn 46 (B, 1-1):** The mirror image — B's Poacher won the ball at I4 (3 hexes from goal K) with A's Goalkeeper pulled to J4. Automatic goal, same mechanism, opposite end.

Three further contested shots were all saved (0-succ, 1-succ-vs-1-stop, 1-succ-vs-1-stop) — none of them landed on the new short-column angles specifically, so that particular wrinkle didn't get exercised this match, but the core fix (Shot Range reaching far enough to punish a keeper caught out) delivered exactly the drama it was meant to.

## Other mechanics tested live

- **Slide Tackle** — used once (B's Poacher, turn 3), won outright with the +1 die. Confirmed the possession-transfer logic (ball moves to the tackler's own hex, not the carrier's) works correctly — this had to be caught and fixed in the moment; my first pass left the ball on the wrong hex.
- **Command the Box** — B's Goalkeeper used it once (turn 32) to instantly claim a loose ball sitting on the same hex as the opposing Poacher, without needing to physically move onto an occupied hex. Worked as designed, and directly set up the sequence that led to A's first goal three turns later, once the keeper got drawn back out again.
- **Emergency Goalkeeper** — **never triggered.** No Red Card fell on either Goalkeeper this match (only one Yellow all game, on B's Poacher), so this rule went completely untested in live play. Worth deliberately engineering a scenario for it specifically in a future session, since it's the one significant change from this batch that got zero real exercise.
- **Jockey** — **never drawn into either hand** across the full match, so also untested live. Same caveat as above.

## Discipline: unusually light

Only 1 Yellow Card and no Red Cards all match — the lightest Discipline count of any full match this project has run. Combined with the much-improved Tackle success rate, this reads as a genuine consequence of Tackle 2 rather than a fluke: more tackles succeeding outright means fewer of the repeated failed-tackle sequences that used to rack up Discipline draws turn after turn.

## Bottom line

This match did what it needed to: confirmed the Tackle rebalance transforms tackling from a near-guaranteed failure into a real 50/50 contest, and showed the Shot Range fix paying off exactly as intended — a team that wins the ball high up the pitch with a keeper out of position now has a genuine, rules-correct way to punish it from distance. Emergency Goalkeeper and Jockey still need a match where they actually come up before either can be called validated.
