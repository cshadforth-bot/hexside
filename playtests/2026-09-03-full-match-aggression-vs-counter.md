# Hexside Playtest — Full Match: Ruthless Aggression vs. Sit Back & Counter

**Date:** 2026-09-03
**Format:** Full standard match — 24 turns per side, halftime swap at the midpoint, 24 more (48 turns total)
**Ruleset:** Current draft, including the escape-hex rule (§8), Clearance (§7), the Zone/Zone Pair fallback with Target Player retired (§5), the 1-Flair cost on a failed Tackle (§7), Tactic Card cycling (§10), and all of Opus's wording clarifications (Thirds, Long Ball, One-Two, Foul/Press in the Resolution Sequence, Last Man)
**Sides:** Team A played **Ruthless Aggression** — constant pressing, Full Press often, both attackers committed forward throughout. Team B played **Sit Back & Counter** — a compact deep block, minimal forward commitment, waiting for a genuine break before committing numbers forward.

**Final score: Team A 1 – 0 Team B.**

---

## How the two philosophies played out

**Ruthless Aggression (Team A)** delivered on its identity: it scored inside the first 3 turns via a coast-to-coast Poacher dribble-then-shot straight from kickoff, pressed constantly (Full Press played 5 times across the match), and kept both attackers committed forward almost the entire second half. The cost was real — three separate failed-tackle Flair deductions under the new rule, and it spent long stretches with 0 Flair banked from throwing itself at low-odds tackles rather than sitting back. It never found a second goal despite generating at least 4 more clear sight-of-goal moments (shots or near-breaks), largely to bad luck on otherwise-favorable dice.

**Sit Back & Counter (Team B)** played exactly as billed: absorbed pressure in a compact deep block, rarely committed more than one unit forward at a time, and explicitly waited for gaps rather than forcing anything. It found **three genuine counter-attack lanes** — each one a real dribble through a correctly-identified weak defender (Tackle 1) with clearly favorable dice odds — and lost all three, twice to a flat tie (defender wins ties by rule) and once to a straight whiff. That's the story of the match: B's game-reading was sound, but the coin never landed. It's a good demonstration that "sit back and counter" is a real, viable strategy under these rules, just one that concentrates its variance into a handful of high-leverage rolls rather than spreading risk across many attempts the way Aggression does.

## The fixes, under a full match's pressure

- **Flair-cost on failed Tackles** — worked exactly as intended: it didn't stop either side from tackling, but Team A's aggressive spam visibly drained its own Flair bank over the match (down to 0 at multiple points), which is precisely the intended brake.
- **Zone/Zone Pair fallback** — fired repeatedly for both sides throughout, most usefully in exactly the "otherwise-dead card" moments the fix targets.
- **Clearance and escape-hex** — available and checked several times, but this particular match's flow never produced a genuine full-encirclement or hopeless-pass situation to force either one into deliberate use — a longer or more attritional match might.
- **Halftime swap** — executed cleanly at the midpoint: ends flipped, formations fully reset, Team B (who didn't open the match) kicked off half 2, exactly per §14.
- **Tactic Card cycling** — never actually triggered; both sides mostly held serviceable Tactic hands or didn't have spare Flair to burn on a cycle mid-press.

## Two things worth flagging transparently

1. **A real rules gap I hit and fixed on the spot:** partway through, the pre-shuffled 35-card Command Deck stream ran out for Team A — a full match draws far more cards than one shuffle provides. This is exactly the "reshuffle the discard pile when the draw pile runs out" case in §5, which the simulation's harness hadn't provisioned for. It was extended with genuinely fresh reshuffled batches (unseeded new entropy) rather than fudged, consistent with this project's randomness discipline. Worth noting for the record: this is a simulation-harness gap, not a rulebook gap — the rulebook already says to reshuffle.
2. **Four occupancy bugs on the simulation side**, all caught and corrected transparently mid-match (two units briefly recorded on the same hex due to bookkeeping slips during manual play, not a rules problem) — a proper duplicate-detector was built after the second one and used for the rest of the match.

## Bottom line

A clean, low-scoring, believable match where both contrasting styles felt distinct and legitimate, and none of the fixes caused new problems — B's three near-misses read as bad luck on sound decisions, not a broken counter-attack game plan.
