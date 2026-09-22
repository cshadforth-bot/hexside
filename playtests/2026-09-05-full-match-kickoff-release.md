# Hexside Playtest — Full Match: Kickoff Release Rule

**Date:** 2026-09-05
**Format:** Standard full length — 48 total turns (24 per side), halftime at turn 24
**Ruleset:** Everything current, plus the new kickoff release rule (§4, §7): the kickoff-taker's entire activation is a single Pass to a teammate within Pass Range, straight from F3 — no Move first, no Clearance, never a Shot or a Tackle.
**Purpose:** Turn 1 of the previous full match ([2026-09-05-full-match-2-fix-recheck.md](2026-09-05-full-match-2-fix-recheck.md)) showed the kickoff-taker personally dribbling through midfield and scoring off its own kickoff — not illegal under the old rules, but a clear mismatch with real football's restriction against a kickoff-taker touching the ball twice in a row. This match tests the fix, tightened once more mid-session: an earlier draft still allowed the taker to move first or clear to open ground; the final version requires an immediate Pass to an actual teammate, nothing else.

**Final score: Team A 2 – Team B 1.**

---

## Headline: every restart resolved correctly, all 5 of them

This match hit **5 separate kickoffs** — match start, two goal restarts for each side plus one more, and halftime — and every single one resolved exactly as designed:

1. **Turn 1 (A kicks off):** A's Poacher passes F3→E4 to the Playmaker, uncontested. Obligation discharged immediately.
2. **After A's 1st goal (B restarts):** B's Poacher passes F3→G4 to the Playmaker, uncontested.
3. **Halftime (B kicks off half 2):** B's Poacher passes F3→E4 to the Playmaker, uncontested.
4. **After B's goal (A restarts):** A's Poacher passes F3→G4 to the Playmaker, uncontested.
5. **After A's 2nd goal (B restarts):** B's Poacher passes F3→E4 to the Playmaker, uncontested.

In every case, the taker's activation was **only** that Pass — no movement beforehand, no Clearance, no Shot, no Tackle — and the receiving Playmaker then became a completely normal ball-carrier on its own later activation, free to dribble and act with no restriction at all. Zero cases of "no teammate in range" (the obligation standing) came up, because the default kickoff formation always leaves a teammate exactly one hex from F3 — same as the rulebook's own worked example.

This is a direct, clean fix for exactly the behavior flagged after the last match: nobody scored, or even advanced the ball themselves, straight off a kickoff this time.

## The rest of the match played out normally

- **Goals (3 total):** A's opener was an automatic empty-net goal (Playmaker at K2, box empty, Shot Range 3 covering distance 1); B's equalizer and A's eventual winner were both genuine contested shots that beat the keeper.
- **Tackles:** 12 attempted, 5 won (42%).
- **Dribble Challenges:** 10 attempted, 5 won by the attacker (50%).
- **Discipline:** 6 draws — 3 Advantage/Play On, 2 Clean Challenge, and 1 Red Card (A's Sweeper, sent off outright — the first time this session a Red has landed in full-match play, though it hit an outfield unit, not either Goalkeeper, so Emergency Goalkeeper still didn't get to fire). A finished the match down to 4 units.
- **State integrity:** `check_no_overlap()` passed after every position change across all 48 turns, no collisions.

## Bottom line

The kickoff release rule holds up cleanly under a full match: every restart — match start, every goal, and halftime — correctly forced the taker into an immediate, teammate-only Pass with no ability to advance or shoot itself, and normal play resumed the instant that pass landed (or was intercepted). No formation in this match ever left a taker without a legal teammate to pass to, so the "obligation stands" edge case remains theoretical rather than something we've seen bite — worth keeping an eye on if a future match tests a deliberately thin or spread-out kickoff formation.
