# Playtest brief: independent Base Game review

You're being asked to do what earlier reports in this folder did: read the rulebook
critically, actually play/simulate the game, and write up what you find — rules
ambiguities, places the engine or drivers disagree with the rulebook, balance issues,
crashes, anything a first-time table would trip over. Nobody has briefed you on what to
find. Form your own view from the rulebook and the code as they actually are, not from
what any earlier report says they were.

## Scope

**Base Game specifically** — the tier defined in `source/hexside-rulebook.html` §1 and
§14: everything except the Tactic Deck (§11). That means `engine/sim.py`'s `ROSTER_BASE`
and `playtest-ai/driver_base.py`, not `driver.py` (which plays the Advanced Game, Tactic
Deck included). If something you find is really about the Advanced Game or about rules
both tiers share, that's fine to note too — just be clear which tier you're talking about,
the way `2026-09-08-base-game-review.md` (see below) is throughout.

## Ground rules

- **The rulebook is the sole authority.** Where code and rulebook disagree, the rulebook
  is right and the code has a bug — say so plainly.
- **Read-only.** Don't edit `engine/`, `playtest-ai/`, or `source/` to fix anything you
  find, even something small and obviously right. Report it; let the maintainer decide
  and make the change. If you want to test a *hypothesis* (a stat change, a rule
  variant), do it in a scratch copy outside this project folder — never in the canonical
  files — the same discipline `2026-09-08-base-game-review.md` describes in its own
  "Method" line.
- **Don't trust old playtest reports for current facts.** This project moves fast —
  since `2026-09-08-base-game-review.md` was written, the board went from 9 zones to 6,
  all 5 Signature abilities went from unimplemented to implemented, several roster stats
  were retuned, the entire kickoff formation system changed from a fixed default position
  to an alternating placement draft, and the Save/rebound mechanic was redesigned (the
  goal box and Goalkeeper Zone are now one unified 3-hex area, a rebound only happens
  without a Flair on the Save roll, and it now lands outside that zone instead of inside
  it — Command the Box no longer exists, replaced by a Goalkeeper signature called
  Shot-Stopper). Any specific line number, card count, hex name, or "currently
  unimplemented" claim in a dated report may no longer hold. Verify everything you cite
  against the current `source/hexside-rulebook.html` and the current code — `grep`
  fresh, don't reuse an old citation.
- **Quantify, and be honest about sample noise.** This project has repeatedly found
  N=200 batches of an *identical* setup disagree by double-digit percentage points on
  goal share by position. Don't draw a conclusion from one small batch. Where you can,
  run at least two independent batches at N=200 and pool them, or say plainly that a
  number is a single small-sample read and could move.

## Suggested method

1. Read `README.md` (repo root) for orientation, then `source/hexside-rulebook.html`
   in full — it's the actual deliverable, read it the way a player building the
   prototype from scratch would.
2. Read `engine/README.md`, `playtest-ai/README.md`, and the module docstrings at the
   top of `engine/sim.py`, `engine/board.py`, and `playtest-ai/driver_base.py` — they
   describe what's implemented, what's deliberately simplified, and why.
3. Run `driver_base.py` — a small batch first (`python3 driver_base.py 10`) just to
   confirm it runs clean from wherever you're invoking it from, then real batches
   (`python3 driver_base.py 200`, at least twice independently) for actual numbers:
   goals/match, shot conversion, dribble/tackle win rates, goal share by unit, card
   usage, discipline rate. Run from a scratch directory outside this project (see
   `playtest-ai/README.md` for why).
4. Read at least one full match log closely (a driver batch writes `batch_stats.json`
   with aggregates; add your own `print`/log capture, or drop the batch size to 1 and
   read the turn-by-turn log it prints) — aggregate stats hide things a real playthrough
   surfaces, like a stalled sequence or a rule that never actually fires.
5. Cross-reference what you read in step 1 against what you saw in steps 3-4. Places to
   look specifically: does every rulebook passage the Base Game reader hits actually
   apply to them, or does it describe an Advanced Game concept unmarked? Does the
   printed/described default setup match what the engine does? Do the dice/roster
   numbers on paper match `ROSTER_BASE` in code? Does anything crash, stall, or produce
   an obviously unbalanced outcome?

## Writing it up

Save your report as `playtests/YYYY-MM-DD-<short-description>.md` (today's date, a few
words on what it covers), matching the naming already in this folder.

For structure and rigor, use `playtests/2026-09-08-base-game-review.md` as your model —
not for its content (stale, per above), but for its shape: a header stating scope and
method, a "Verified-good" section stating what you checked and confirmed correct (so the
rest of the report reads as exceptions), numbered findings with concrete evidence (line
numbers, batch data, quoted rulebook text) rather than impressions, and a final ranked
punch-list (P0 = blocks the game from working as described, down through P2/P3 = design
leads worth considering). `2026-09-08-full-game-review.md` in the same folder is a
second, longer example if you want more than one reference point.

Write what you actually find, including if the answer is "this is in good shape" — a
report that confirms things are working is as useful as one that finds problems, and
more useful than one that manufactures problems to have something to say.
