# Hexside Playtest — Full Match: Dynamic Ball-Carrier Activation

**Date:** 2026-09-05
**Format:** Standard full length — 48 total turns (24 per side), halftime at turn 24
**Ruleset:** Everything current, plus the newly-clarified dynamic reading of §5's ball-carrier-is-always-activatable rule: whenever possession changes hands mid-turn (a kickoff release Pass, a won Tackle's free follow-up Pass), the new carrier is itself immediately activatable — for a further Move only, never a second Act (Pass/Shot/Tackle) unless Full Press paid for one.
**Purpose:** This rule was added after a rules-design discussion but had never been exercised. This match specifically checks that a receiving unit picking up the ball mid-turn (a) actually gets to move further under the dynamic rule, and (b) never illegally gets a second Act out of it.

**Final score: Team A 0 – Team B 0.**

---

## Headline: the dynamic rule fired 6 times, every one of them correctly capped at Move-only

Two distinct triggers for the rule came up all match, both handled identically and correctly every time:

**Kickoff release → dynamic move (2 instances):** both the match-opening kickoff and the halftime kickoff resolved as: taker passes to the Playmaker (mandatory release, §4/§7) → Playmaker is now itself activatable → Playmaker attempts to advance further, resolving a real Dribble Challenge along the way. Both times the Dribble Challenge was lost, so the Playmaker's move ended on the contested hex with the ball spilling back — a legitimate outcome, not a scripted one.

**Won Tackle's free follow-up Pass → dynamic move (4 instances):** a tackler wins the ball, immediately plays its free follow-up Pass to a teammate (not spending the turn's one Act, per §7), and that receiving teammate is then itself dynamically activatable. One of these was a genuinely funny edge case worth flagging: Team A's Sweeper won a Tackle and its free follow-up Pass landed on its own **Goalkeeper**, who — correctly, per the rule as written, with no special-case exclusion for the GK — became dynamically activatable and attempted to advance the ball out of its own box. It lost the resulting Dribble Challenge and the ball spilled back toward its own goal. Nothing in the rule text excludes the Goalkeeper from this, and nothing in the engine did either, so this played out exactly as the rule implies — worth a deliberate look at whether that's actually desired.

**Verified programmatically, not just by eye:** every one of the 6 dynamic-activation instances was checked against the full log to confirm no Shot or second Act followed it before the turn ended — all 6 came back clean. The driver never called a Shot attempt after any dynamic move, and the log confirms nothing tried to sneak one in.

## Why the score is 0-0

Zero contested Shots happened all match (compared to 2-4 in every previous full match) — every dangerous advance either got shut down by a Dribble Challenge or a Tackle before reaching Shot Range, including several of the dynamic-activation follow-on moves above. This reads as this run's ball-carrying AI playing a bit more conservatively / less lucky than previous runs' heuristics, not a rules problem — 12 Tackles (8 won, 67%) and 14 Dribble Challenges were contested throughout, so the match wasn't inactive, it just never broke through. Discipline was light: 4 draws, no cards with any real effect (1 Warning, 1 Advantage/Play On, 2 Clean Challenge).

## Other notes

- **State integrity:** `check_no_overlap()` passed after every position change across all 48 turns.
- **A real driver bug found and fixed before this run completed cleanly:** the first attempt crashed with a `KeyError` — a follow-up Pass or kickoff-release Pass that was contested (its straight line crossed an opposing Zone of Control) but where the ZoC-based "is this contested" check and the adjacency-based "which unit is defending" check disagreed on which unit was actually adjacent, leaving no defender to attribute a failed pass's turnover to. Fixed with a safe fallback (attribute the turnover to any opposing unit if none is found adjacent) rather than crashing — this is a test-harness bug, not an engine bug, since the real engine functions (`contest()`, `reach()`, `enemy_zoc()`) were all already correct; the bug was in how the throwaway driver script picked which unit to credit an interception to.
- One repeat of a known driver limitation from earlier matches: the simplified AI's `reposition()` logic doesn't know to keep a Goalkeeper anchored in its own box, so B's Goalkeeper wandered out to F1 by full time. Not a rules issue, just the same caveat as previous automated-driver matches.

## Bottom line

The dynamic ball-carrier rule works exactly as intended: a new carrier picking up the ball mid-turn — whether from a kickoff release or a won Tackle's free follow-up Pass — is correctly given the chance to move further under its own steam, and correctly never gets to act again without Full Press. The one thing worth a deliberate design decision, surfaced by this match rather than reasoned out in advance: should a Goalkeeper be excluded from becoming a dynamically-activated ball-carrier via a stray follow-up pass, or is a keeper being drawn out of its box by an errant pass from a teammate a legitimate (if rare) situation to leave as-is?
