# Hexside Playtest — Full Match: Fresh-Session Driver, Baseline Run

**Date:** 2026-09-07
**Format:** Standard full length — 48 turns (24 per side), halftime at turn 24
**Ruleset:** Everything current in `sim.py`/`board.py` as of today — GK confinement, Composure, the Yellow sin-bin, kickoff release, the dynamic ball-carrier rule, Through on Goal.
**Methodology note:** this is a brand-new driver written from scratch this session (not a continuation of the "beefed up driver" from earlier in the week) — real dice throughout via `sim.contest()`/`sim.tackle()`/`sim.slide_tackle()`, no positions arranged or forced. Its heuristics are deliberately simple: move the ball carrier toward goal, shoot on sight once in range, tackle when adjacent to the opposing carrier, and — the one non-rulebook addition — a goalkeeper holding the ball always looks to distribute (a plain pass, or a range/line-agnostic "clearance" logged explicitly as a driver simplification) rather than sit on it, since the zone-confinement rule left the ball genuinely stuck on the keeper in an earlier trial run otherwise. Two real gaps versus prior sessions' drivers: this one never plays Foul, Press, Composure, or Jockey, and it actively routes the ball carrier's move around the opponent's Zone of Control whenever a clear path exists — so it under-represents both Tactic-card play and Dribble Challenges relative to a human table, where players take contested risks far more often. Worth reading this run as a state-integrity and rules-plumbing check first, a tactical result a distant second.

**Final score: Team A 1 – Team B 2.**

---

## Headline: all three goals landed in the first half, on straight shots, no breakaways

```
[Shot: B PO vs A GK] B rolls [6,4,4,5] (2 succ) | A rolls [4,5,1] (1 stop) => ATTACKER WINS
  [GOAL! B PO beats A GK. Score A 0-1 B]
[Shot: A PO vs B GK] A rolls [5,4,1,5] (2 succ) | B rolls [2,2,4] (0 stop) => ATTACKER WINS
  [GOAL! A PO beats B GK. Score A 1-1 B]
[Shot: B PO vs A GK] B rolls [1,5,2,1] (1 succ) | A rolls [3,3,1] (0 stop) => ATTACKER WINS
  [GOAL! B PO beats A GK. Score A 1-2 B]
```

All three were the Poacher (Shot 4, the roster's best) shooting from its own generous Shot Range without ever needing to win a Dribble Challenge first — the driver's ZOC-avoidance heuristic kept both Poachers finding a clear lane to a shooting hex early, before either defense had organized. **Zero Dribble Challenges were attempted all match**, so Through on Goal never had a chance to trigger here — a direct consequence of this driver's own conservative pathing, not a finding about the rule itself (see the mechanic-test and full-match logs from earlier this week for that).

## The rest of the match

- **Shots:** 12 attempted, 3 goals (25% conversion), 9 saved. All 3 goals came in the first 22 turns; the second half went scoreless across 6 more shot attempts, all saved.
- **Tackles:** 2 attempted, 1 won (A's Wingback dispossessed B's Goalkeeper outright at I4, turn 19) — too small a sample to read anything into, consistent with this driver rarely putting a defender adjacent to the carrier before a shot or pass had already resolved.
- **Discipline:** 1 draw (a failed Tackle), landing a Yellow Card — B's Wingback correctly missed exactly one of B's own turns in the sin-bin (sent off turn 20, returned turn 23) and came back with its permanent Pace −1 applied, no double-counting.
- **Kickoff release:** enforced correctly 5 times (the opening kickoff, 3 goal restarts, the halftime restart) — every kickoff-taker's activation was a single Pass and nothing else, verified in the log each time.
- **Goalkeeper distribution (driver simplification, not a rules mechanic):** used 5 times, split between a genuine in-range Pass and a longer range/line-agnostic Clearance when nothing was reachable — logged explicitly both ways so it's never mistaken for tested rules behavior.
- **State integrity:** `check_no_overlap()` passed after every position change across all 48 turns; no collisions, no crashes, no unhandled exceptions.

## Bottom line

Clean, crash-free full match on a fresh driver — sin-bin timing, kickoff release, halftime end-swap, and Emergency-Goalkeeper wiring (never triggered this match, no Red Cards drawn) all read correctly against the log. The tactical picture is thin by design: this driver's own risk-averse pathing suppressed Dribble Challenges to zero, so nothing here should be read as evidence about Through on Goal, Jockey, Composure, or card-level balance — those need a driver willing to walk into contests, the way earlier sessions' more aggressive/randomized drivers did. Good candidate next step if this margin or scoring shape matters: add Foul/Press/Slide-Tackle-style randomized aggression to this same driver (mirroring the "beefed up driver" fix from 2026-09-05) before drawing any balance conclusions from it.
