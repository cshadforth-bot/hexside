# Hexside Playtest — Full Match: Through on Goal, Live in Real Play

**Date:** 2026-09-07
**Format:** Standard full length — 48 turns (24 per side), halftime at turn 24
**Ruleset:** Everything current, including today's merge — Through on Goal (+1 Shot die after winning a Dribble Challenge in the same activation), on top of GK confinement, Composure, the Yellow sin-bin, kickoff release, the dynamic ball-carrier rule, and everything from earlier in the session.
**Purpose:** The mechanic test (2026-09-07) proved Through on Goal works mathematically, at a scale where noise washes out. This is the first check of whether it actually shows up and matters in genuine, non-engineered full-match play — no positions arranged, nothing forced, real dice throughout.

**Final score: Team A 1 – Team B 1.**

---

## Headline: both goals this match were Through on Goal

```
[Shot: A PM vs B GK (THROUGH ON GOAL, +1 die)] A rolls [3, 6, 5, 2]->[...] (2 succ) | B rolls [...] (0 succ) => ATTACKER WINS
  [GOAL! (THROUGH ON GOAL) A PM beats B GK. Score A 1-0 B]
...
[Shot: B PM vs A GK (THROUGH ON GOAL, +1 die)] B rolls [4, 6, 3, 5]->[...] (2 succ) | A rolls [...] (0 succ) => ATTACKER WINS
  [GOAL! (THROUGH ON GOAL) B PM beats A GK. Score A 1-1 B]
```

Both Playmakers won a real Dribble Challenge, carried straight into shooting position in that same activation, and scored with the bonus die — the exact sequence the rulebook now names and rewards, happening twice, unprompted, in a match nobody steered. **3 of this match's 4 shots (75%) were breakaway shots**, and every goal scored came from one. The one non-breakaway shot (Composure was played to try to save it) missed.

## The rest of the match, for context

- **Dribble Challenges:** 16 attempted, 8 won by the attacker (50%) — a healthy rate, consistent with why breakaways are common rather than rare.
- **Tackles:** 12 attempted, 3 won (25%).
- **Discipline:** 10 draws — 3 Yellow Cards (each correctly triggering a one-turn sin-bin trip and a clean return, verified in the log) and 1 Red Card (B's Sweeper, sent off outright — not the Goalkeeper, so Emergency Goalkeeper correctly never engaged).
- **Automatic goals:** zero — GK confinement held throughout, both keepers stayed in their zones the entire match, so both goals had to be earned the hard way.
- **State integrity:** `check_no_overlap()` passed after every position change across all 48 turns — no collisions, no crashes.

## Bottom line

This is about as clean a confirmation as a single genuine match can give: Through on Goal wasn't just mathematically sound in isolation, it was the mechanism behind the *entire* scoreline the first time it got a real, unscripted match to play out in. Worth remembering this is one match, not a trend — but combined with the mechanic test's verified +11-point conversion lift and the earlier finding that over half of all shots already arrive via a won dribble, this is a strong sign the rule is doing exactly the job it was designed for: making the sport's most basic good chance actually feel like one.
