# Hexside Mechanic Test — Emergency Goalkeeper & Jockey

**Date:** 2026-09-05
**Format:** Targeted engine test, not a full match. Both mechanics are rare-trigger by design (a sent-off Goalkeeper; a specific card landing in hand at the right moment), so rather than hope for them across another 48-turn match, positions were engineered to reach the trigger quickly. Every roll, card draw, and rule resolution still ran through the real, unmodified engine functions (`tackle()`, `contest()`, `reach()`, `apply_discipline()`, real pre-generated dice/card streams) — nothing about the *outcomes* was scripted or faked, only the *setup* was arranged to get there faster.

---

## Emergency Goalkeeper — verified, and a real bug found and fixed along the way

**Basic trigger:** a Poacher was placed adjacent to Team A's Goalkeeper, which then repeatedly attempted real Tackle Challenges against it (using the actual dice stream) until a card landed. Took 23 attempts this run (a 2nd-Yellow escalation, not a direct Red) — plausible variance, not a sign anything's wrong. The instant it happened:

- `assign_emergency_gk()` fired automatically, no manual intervention.
- Team A's Sweeper was correctly picked as deputy (the documented default preference) and placed in the goal box.
- `save_stat()` correctly returned **1** for the deputy and **3** for an untouched real Goalkeeper on the other side.
- A real contested Shot against the deputy rolled exactly **1** Defense die, confirmed live — not just the stat lookup, the actual dice draw matched.
- `goal_restart()` kept the deputy in the box after a full formation reset, rather than reverting it to its normal template position.
- `halftime_reset()` correctly re-placed the deputy into the **new** goal box after the end-swap (Team A's deputy followed the swap from the A-end box to the K-end box).

**The harder case — what happens when the deputy itself gets sent off?** This is where it got interesting. The rulebook text (written when this rule was added) already promised: *"if that first deputy is itself later sent off, the side names a second deputy the same way."* Testing it directly exposed that **the code didn't actually do this** — `apply_discipline()` only checked for the literal string `'GK'` being sent off, not "is the sent-off unit the currently-assigned deputy." When the deputy was carded, the side was left with **zero** goalkeeper coverage at all, silently, with the internal `emergency_gk` record still pointing at a unit no longer on the pitch.

**Fixed:** `apply_discipline()` now checks `unit == 'GK' or emergency_gk[side] == unit` before triggering a fresh assignment — covering both the original keeper and any current deputy. Re-tested after the fix: a second deputy (the Wingback) was correctly assigned when the first deputy was sent off, `save_stat()` correctly returned 1 for the new deputy and stopped applying to the old one, and `sent_off` recorded exactly the two units that actually left (no duplicate garbage entries, which the pre-fix run had produced when my own test loop kept attacking with a unit that no longer existed on the pitch — a bug in the test script that only surfaced *because* the underlying engine bug left state in an inconsistent place).

This is exactly the kind of thing a full match is unlikely to ever surface (it needs two separate cards on the same side's goalkeeping duty in one match) but a targeted test catches immediately.

## Jockey — verified with a concrete "this shot no longer exists" example

Real Tactic Cards were drawn one at a time from Team B's actual pre-generated stream until Jockey appeared (6 draws). A scenario was then set up: Team A's Playmaker (Pace 3) holding the ball at F3, Team B's Sweeper adjacent, about to react to the Playmaker's move.

- **Without Jockey:** the Playmaker's full-pace reach included I2/I3/I4 — all exactly Shot Range 3 from the Team A's own target net, a genuine breakaway shooting chance.
- **Team B plays Jockey** (`play_jockey()`): confirmed it correctly spent 1 Flair, removed the card from hand, and logged the reaction.
- **With the resulting Pace-2 reach** (`reach(..., extra_pace=-1)`): I2/I3/I4 all dropped out of reach entirely. The best remaining hex only reached Shot Range 4 from the net — outside the Playmaker's own Shot Range 3. Jockey didn't just shave a number; it concretely denied a shooting opportunity that would otherwise have existed.
- Edge case checked: calling `play_jockey()` with 0 Flair banked correctly returned `False` and left the card in hand untouched, rather than silently charging a cost the side couldn't pay.

## Bottom line

Both mechanics work as designed. Emergency Goalkeeper needed a real fix — the single-deputy case worked from the start, but the second-loss case was silently broken until this test caught it, and it's fixed now. Jockey needed no code changes at all; it produced exactly the intended effect on the first real scenario tried, including a case where it turned a genuine scoring chance into nothing.
