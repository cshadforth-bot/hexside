# Hexside Playtest — Discipline Risk on Any Failed Tackle (24 Turns)

**Date:** 2026-09-04
**Format:** Single half, 12 turns per side (24 total)
**Rule under test:** The new §7 change — any lost Tackle Challenge now draws once from the Discipline Deck (in addition to the existing 1-Flair cost), with a lost Slide Tackle drawing **twice**. Neither stops play; only the Foul Tactic Card causes a real stoppage/Free Kick now. Baseline roster stats (no Shot+1 buff — this test isolates the Discipline change).
**Sides:** Both aggressive, as in prior full-length tests.

**Final score: Team A 0 – 0 Team B** — but the scoreline is the least interesting number from this match.

---

## Headline result: the mechanic has real teeth — maybe too much

**The very first Tackle attempt of the entire match** (turn 2, Team A's Sweeper) failed and drew a straight **Red Card** — a 1-in-6 outcome, hit immediately. Team A played essentially the **entire rest of the match a player down**, from turn 2 of 24 onward.

By full time, across just **10 Tackle attempts** in the whole 24-turn match:

- **1 Red Card** (Team A's Sweeper, sent off turn 2)
- **3 Yellow Cards** (Team A's Wingback, Team B's Poacher, Team B's Playmaker)
- **3 Warnings**, **1 Advantage/Play On** (no effect either way)

That's **8 Discipline draws in one 24-turn half** — compared to **zero** Discipline events total across the four previous full-length or quick playtests this project has run. The mechanic went from completely dormant to the single most consequential thing that happened in the match, in one change.

## Is this too harsh?

Worth flagging honestly: 10 Tackle attempts is a fairly normal count for a match this length (the two 48-turn full matches earlier this project saw many more), and 8 of those 10 failed — an unusually poor run of luck for tacklers, which inflated the Discipline-draw count along with it. But even accounting for that, the core math is stark: **every single failed Tackle now carries a 1-in-6 chance of an immediate Red Card**, not just via second-Yellow escalation — that's baked into the Discipline Deck's composition (1 Red / 6 cards) regardless of which of the two triggers caused the draw. A team that commits to contesting the ball aggressively — which every playtest this project has run does, by design — is now exposed to losing a player early and often. Team A spent 22 of 24 turns at a numerical disadvantage because of one unlucky roll two turns in.

This might be exactly the "make tackling cost something real" outcome the change was aimed at. It might also be overtuned for how frequently Tackle Challenges actually occur in normal play — worth watching across a longer match (or several) before concluding either way, since one Red Card two turns in is a small sample driving a large chunk of this match's shape.

## What else the match showed

- **A cornered Goalkeeper is a real, sustainable pressing target now.** Once Team A's Sweeper was gone, Team B spent several turns hunting Team A's ball-carrying Goalkeeper into the corner (A4 → A2 → A1, running out of open hexes each time), eventually winning the ball right on the byline. This is a good sign for the escape-hex rule's interaction with a depleted defense — the Goalkeeper genuinely had to run, not just stand and absorb pressure.
- **A real infrastructure bug, caught and fixed:** `apply_discipline()` was keying `pace_mod` and the Yellow-card tracker with Python tuples — which JSON silently can't serialize as dict keys, and silently turns into a list (breaking `in` membership checks) inside a list. This crashed the very first Yellow Card the match tried to apply, and would have silently broken second-Yellow-to-Red detection even where it didn't crash outright. Fixed by switching to string keys (`"A:WB"`) throughout; the corrupted save file was hand-repaired from its last-good JSON rather than replayed, since the failure happened at the very last line of the write.
- **The Discipline Deck itself ran out mid-match** — a 6-card deck depleted after 8 draws was always going to need a reshuffle, and did, extended with a freshly-shuffled (unseeded) batch per the project's standing randomness discipline, consistent with how Command Card exhaustion was handled in earlier full matches.

## Bottom line

The core ask — make Discipline a mechanic that actually shows up in play — worked emphatically. Whether it worked *too* well is the open question: one bad roll on turn 2 shaped almost the entire rest of this match. Recommend running at least one longer match before deciding whether to soften it (e.g., a smaller Red-Card share in the deck, or reserving the double-draw penalty for Slide Tackle only and keeping standard Tackles to a lighter consequence like Yellow/Warning only) or leaving it as-is.
