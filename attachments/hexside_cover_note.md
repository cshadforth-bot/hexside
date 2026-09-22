# Hexside playtest — cover note

We ran 28 simulated matches against your `sim.py` / `board.py` (unmodified — nothing in the
engine or rulebook was edited) using an external test-driver, from 6-turn smoke tests up to a
double-length 96-turn stress match, with the full 13-card Tactic deck and the Discipline deck
live throughout. Full writeup with tables and details:

**Report:** https://claude.ai/code/artifact/dddbbaae-5aad-4254-9a81-0c7cbd7c9226
**Raw logs + driver scripts:** attached (`hexside_playtest_logs.zip`, see `INDEX.md` inside for
which file is which match)

## Headline findings

- **Command Deck exhaustion is real.** `gen_random()` never reshuffles once a side's 35-card
  pool runs dry — confirmed by direct crash at turn 42 of a long match, despite §5 explicitly
  calling for a reshuffle. We worked around it in the test driver only; `sim.py` itself still
  needs the fix.
- **No goalkeeper-replacement rule is the single biggest swing factor we found.** A sent-off
  keeper leaves a permanently open net for the rest of the match — decisive on its own at least
  once. We drafted an "Emergency Goalkeeper" idea for §15 (automatic deputy, flat Save 1, no
  Command the Box) in the report.
- **Offside Trap fired zero times across 13 real matches** where it was in the deck (confirmed
  the mechanic itself works via a hand-built test — the condition is just too narrow to arise
  naturally). We trialled swapping it for "Jockey," already on your own §15 wishlist — better,
  but still one of the rarer cards even after widening its trigger.
- **Shot Range has a genuine text/code mismatch, and we chased it all the way through.** §7 says
  range should reach the Net, not the box; `board.py` measures to the box. We found 5 real goals
  across the session that only counted because of that gap, then confirmed Sweeper/Wingback
  would be reduced to zero shooting margin under a literal net-based reading. Recommendation:
  keep net-based measurement (it's the thematically correct football rule) and add **+1 to
  every non-Goalkeeper's Shot Range** to compensate — mechanically identical to today's numbers,
  and validated in 5 fresh matches where SW/WB genuinely started converting from real
  mid-range distance rather than only from inside an empty box.
- Two bugs were in our own test driver, not your code — found and fixed mid-session (both
  detailed in the report, in case the same edge cases matter for anything else built on top of
  `sim.py`).

Everything else — full Tactic Card usage counts, the complete 28-match Discipline log, and the
reasoning behind each recommendation — is in the report.
