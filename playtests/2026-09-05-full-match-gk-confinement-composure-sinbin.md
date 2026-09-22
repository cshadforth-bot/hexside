# Hexside Playtest — Full Match: Merging Report II's Proposals

**Date:** 2026-09-05
**Format:** Standard full length — 48 total turns (24 per side), halftime at turn 24
**Ruleset:** Everything current, plus four proposals merged from an independent agent's "Hexside Match Report II" in this same pass: **Composure** replacing Advantage Play, **Goalkeeper confinement** to a new 3-hex **Goalkeeper Zone**, **opponent exclusion** from that zone, and the **Yellow Card sin-bin**.
**Purpose:** Validate the combination together, for the first time, against the full canonical ruleset built up over today's session (Shot Range/Net fix, Emergency Goalkeeper, Jockey, kickoff release, the dynamic ball-carrier rule, seam columns, unified Discipline Deck) — none of which Report II's own testing had access to, since it ran in a separate throwaway harness against an older engine snapshot.

**Final score: Team A 1 – Team B 0.**

---

## What actually got merged (this is now live in the canonical files, not a driver-only experiment)

- **`board.py`**: new `GK_ZONE = {'A': ('A3','A4','B3'), 'K': ('K3','K4','J3')}` — a 3-hex zone, distinct from the existing 2-hex `GOAL_BOX` (Save-rebound placement, the box-defender die — both unchanged) and the existing 3-hex Net (the Shot's off-board target).
- **`sim.py`**: `is_goalkeeper_role()`, `legal_reach()` (confinement for the goalkeeper-role unit, opponent-exclusion for everyone else), `gk_zone_occupied()`, `_zone_hex()`; `assign_emergency_gk()`/`_reapply_emergency_gk()` now place the deputy anywhere in the 3-hex zone, not just the literal box; `TACTIC`/`TACTIC_COST` swap `AdvantagePlay` for `Composure`, plus `play_composure()`; `send_to_sinbin()`, `sinbin_check()`, `_touchline_hex()`, wired into `apply_discipline()`'s first-Yellow branch.
- **`hexside-rulebook.html`** (§3, §4, §7, §10, §11, glossary), **`hexside-cards.html`**, **`hexside-components.html`**: all updated to match, PDFs regenerated (rulebook 37→38 pages; cards and components unchanged at 10 and 3).

## Verified, not just by eye

**Goalkeeper Zone confinement: checked programmatically against every single logged Goalkeeper movement this match, both halves, correctly accounting for the halftime end-swap — zero violations.** Every move, reposition, dribble-through, and loose-ball claim by a Goalkeeper landed inside its own current zone, whichever end that was after the swap.

**Opponent exclusion held by construction** — every unit's movement in this test run went through the new `legal_reach()` filter, which was itself unit-tested directly beforehand (confirmed a unit standing right next to the opponent's zone edge has those 3 hexes stripped from its reachable set, while a defender standing inside its *own* zone is untouched).

**Automatic goals: zero, all match** — consistent with Report II's own finding: with the zone always populated (barring the one carve-out below) and never enterable by an attacker, every shot this match had to beat a genuine Save roll.

## A real, previously-undiscussed rule interaction, found while building the test

Report II never mentions this, and it's a genuine consequence of stacking "opponent exclusion" on top of a rule that already existed: **a Save rebound lands on "the other hex of the goal box" (§7) — which is inside the *defending* side's own zone.** Since the shooting side can now never enter the opponent's zone for any reason, **it can no longer contest that rebound at all** — only the defending side can ever reclaim it. The rulebook's own §7 text still says a Save rebound is "genuinely contestable by either side," which this quietly contradicts.

I did not add a carve-out for this on my own judgment — Report II didn't propose one, and it's exactly the kind of thing you flagged wanting to decide yourself in a couple of the design questions earlier today. This match's own log shows it happening twice (turn 17: A saves, rebound at A4, B can never reach it; turn 30-ish: B saves, rebound at A3 after the half-swap, A can never reach it) and in both cases the rebound was simply reclaimed by the defending side next turn, consistent with Report II's broader "defense-favored, every goal properly earned" pattern — but it is a one-sided change from what §7 currently promises in writing, worth a deliberate call: leave it (rebounds are now always safe for the defense) or add a claim exception (mirroring the existing loose-ball/Zone-of-Control carve-out in §8) so a rebound stays genuinely contestable.

## Composure fired once, exactly as designed

Team B lost a Shot 0 succ vs 2 stop, played Composure (1 Flair), rerolled a die, rolled a Success — the reroll worked exactly as intended, but 1 succ still wasn't enough to beat the Goalkeeper's 2 stops, so the shot stayed saved. A clean, honest test: the card did precisely what it says, without being scripted to succeed.

## The Yellow Card sin-bin didn't fire naturally this match

Zero Yellow Cards landed in this particular 48-turn run (7 Discipline draws total, all Clean Challenge / Advantage / Warning-type outcomes) — ordinary variance, the same way full matches earlier today sometimes went a whole game without a Red. I validated the sin-bin mechanic directly beforehand with targeted engine calls instead (not part of this match's own log): confirmed the exact turn-timing (carded unit misses precisely one of its own side's turns, returns at the start of the turn after that), and confirmed the Goalkeeper-specific exception (a sin-binned Goalkeeper's zone sits genuinely empty for that one turn, rather than getting an Emergency Goalkeeper deputy, and it returns into its own zone rather than a touchline hex).

## Other numbers

- **Tackles:** 9 attempted, 2 won (22%).
- **Dribble Challenges:** 12 attempted, 4 won by the attacker (33%).
- **Shots:** 3 total, 1 goal (a genuine contested Shot-vs-Save win, not automatic).
- **State integrity:** `check_no_overlap()` passed after every position change, all 48 turns, no collisions, no crashes.

## Bottom line

All four of Report II's proposals are now live in the canonical rulebook and engine, not just a separate agent's test harness, and held up cleanly together under a full match on top of everything else built today. The one open item is the Save-rebound contestability conflict above — worth a decision before the next match, since right now it's a quiet, undocumented change to what §7 already promises in writing.
