# Hexside Playtest — Quick Aggressive Match, No Tactic Deck (12 a Side)

**Date:** 2026-09-04
**Format:** Quick length — 12 turns per side, 24 total, halftime at the midpoint
**Ruleset:** Full current canon (Shot +1, unified 12-card Discipline Deck, seam columns D/H, ball-carrier-always-activatable, free kickoff formation) — **Tactic Deck removed entirely** for this run, so no Nutmeg, Step-Over, Slide Tackle, Press, Foul, or any other Tactic Card came into play. Discipline Deck stayed in, since standard Tackles still draw from it regardless of Tactic Cards.
**Sides:** Both told to go all-out for goals — no defensive caution, contest everything, always push for a shot when one's on.

**Final score: Team A 0 – Team B 0.**

---

## Headline: still zero lockouts, even stripped down

**0 cycles in 24 turns (0%).** With the Tactic Deck removed, the only randomness left is the Command Deck, dice, and Discipline draws — and even without Tactic Cards adding activation flexibility (no Press-forced tackles, no free follow-up plays), every single turn found a legal, meaningful move. That's a good sign the lockout fix isn't secretly dependent on Tactic Cards bailing out a bad Command hand — the ball-carrier rule and the free kickoff formation are doing the real work.

## The match: two real chances, two big saves, a goalless draw

Despite "hell for leather" instructions on both sides, this one stayed goalless — not from timidity, but from a genuine defensive stand at both ends:

- **Turn 1 (A's kickoff):** the Poacher dribbled straight through midfield on the opening exchange and had a shot away inside the first turn — saved.
- **Turn 12 (B):** after working a Poacher run the length of the pitch into Team A's own defensive third, B forced the only other shot of the match — also saved, right on the stroke of the (slightly late) halftime whistle.

Both keepers were under real siege the rest of the time without conceding: **9 total Tackle attempts, and not one of them succeeded** — the same "everything failed" variance that showed up in an earlier full match. Team B's Poacher was the one to actually pay for the pressure, picking up a direct **Red Card** in the first half; Team A's Playmaker took a **Yellow**. B finished the match a man down (4 v 5) for the entire second half and still held the clean sheet.

## The seam-column rule got a real workout

Multiple turns this match specifically exercised the new D/H seam columns — a Zone Pair card picked up a unit standing in what used to be a dead zone for that card (confirmed directly against the `card_options()` logic before playing), and a plain Third-2 card reached into column D territory it wouldn't have covered before. Nothing about it felt like a stretch at the table; it read as a natural extra option, which is exactly the "more flowing" feel the change was aiming for.

## Two harness mistakes caught mid-match, both disclosed here

Simulation-driving errors, not rules bugs — flagged for transparency the same way earlier matches have been:

1. **Command Cards weren't being removed from hand after being played**, for the match's first four turns, so both sides' hands went stale instead of cycling. Caught at turn 4; hands were corrected to the right size with fresh draws and the discipline was enforced properly from then on. This also surfaced the actual bug it was masking:
2. **Counter was played as if it were a normal turn card** at turn 4 (drawing "GK" as an activation option) — Counter can never be played on your own turn, only held and discarded on the opponent's turn. Caught immediately, corrected to a legal card, and Team B's docked Flair from the invalid attempt was restored. A third, smaller slip — a "tackle" attempted against a unit that didn't actually have the ball — was also caught and unwound the same turn.
3. **Halftime was missed at the correct midpoint** (turn 12) and only applied late, at turn 16, once it became obvious the running turn count had drifted past it. The match still completed its full 12-a-side length either side of the swap, but the two "halves" ended up 8 turns and 4 turns respectively rather than an even 6 and 6.

None of these affected the legitimacy of the dice rolls or the final position — they were bookkeeping slips in how the sim was driven, not in the rules being tested.

## Bottom line

A tense, believable 0-0 with two genuine chances and heavy — if statistically unlucky — defensive pressure at both ends. The core finding holds even with the Tactic Deck stripped out entirely: this ruleset does not produce dead turns anymore. The seam-column change performed exactly as designed in live play, and the harness bugs are now fixed for any future quick-format matches.
