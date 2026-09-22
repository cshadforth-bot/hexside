# Hexside Playtest — Full Match: Ruthless Aggression vs. Ruthless Aggression

**Date:** 2026-09-04
**Format:** Full standard match — 24 turns per side, halftime swap at the midpoint, 24 more (48 turns total)
**Ruleset:** Current draft, including everything in the previous full-match report plus the two newest fixes: the Slide Tackle cost change (2 Flair → **0 Flair**, free to play, with the failure-case Discipline-draw risk unchanged)
**Sides:** Both Team A and Team B played **Ruthless Aggression** — constant pressing, committing attackers forward, throwing in Tackles and Dribble Challenges rather than sitting back. This was a deliberate change from the previous full match (Aggression vs. Counter) specifically to see what two matching aggressive identities produce, and whether a now-free Slide Tackle would actually get used.

**Final score: Team A 0 – 0 Team B.**

---

## How it played out

Same scoreline as a stalemate on paper, but a completely different match in character from the goalless spells Opus flagged in an earlier report. This was **open and end-to-end for almost the entire 48 turns**: possession changed hands constantly, both sides strung together multiple genuine breakaways deep into the opponent's third, and there were **two real shots on goal** (both from Team B's Playmaker, both saved by Team A's Goalkeeper) plus at least four further breakthroughs that were stopped by a Tackle or a lost Dribble Challenge before a shot was even possible. The 0-0 result reads as **bad finishing luck, not a lack of chances** — B in particular created a strong scoring position three separate times (turns 17, 23, and the second-half push toward the K goal) and converted none of them.

Both sides built up large Flair banks over the match (A finished on 5, B on 4) almost entirely from the 1-Flair-per-failed-Tackle rule — there were a huge number of Tackle attempts and Dribble Challenges this match (both sides pressing constantly means constant contact), and the failed ones kept paying out Flair symbols on top of the tax, so neither side ever felt actually short of Flair despite spending it recklessly on low-odds tackles all match.

## The fixes, under two-sided pressing pressure

- **Slide Tackle (0 Flair fix)** — **never appeared in either side's Tactic hand at a moment it could be played**, across all 48 turns. Neither side drew it into a live hand during a Tackle situation, so this match doesn't actually settle whether the fix works in practice — it's inconclusive by bad luck of the draw, not a finding either way. Worth another playtest specifically seeded to guarantee it comes up.
- **Failed-Tackle Flair cost** — worked as designed, but this match highlights that with two sides both throwing in constant low-odds Tackles, the tax doesn't slow them down much: Flair income from the failed rolls' own Flair symbols roughly kept pace with the cost. Not necessarily a problem — Flair still isn't a moving average of *pure* accumulation, since the two are separate die faces — but this is the first match where the drain and the income visibly offset each other turn to turn.
- **Zone/Zone Pair fallback** — fired at least three separate times for both sides, always exactly at the "otherwise-dead card" moment it targets.
- **Command Card cycling** — used **seven times total** across the match (roughly one turn in seven), almost always because the acting side's hand held only Zone/Third/Lane cards that didn't reach whichever unit was actually near the ball. This is a more frequent "dead turn" rate than either previous playtest surfaced, and it's worth flagging: it's specifically **Lane and Third cards** (deliberately built with no fallback, per the design rationale that going empty on a whole lane/third is "genuinely rare") that produced almost all of these dead turns in practice, not the Zone Pairs. Whether that's an acceptable cost of the wider coverage or worth a second look is a real open question this data raises.
- **Full Press** — played five times total (three by A, two by B) for the extra Act, and the discard-debt bookkeeping (now handled by a proper `replenish()` helper after a mid-match bug — see below) tracked correctly every time.
- **Halftime swap** — executed cleanly at the 24-turn mark, ends flipped, formations reset, Team A (who didn't open the match) correctly kicked off half 2.

## Two things worth flagging transparently

1. **A real simulation-harness bug, caught and fixed on the spot:** the very first won Tackle of the match (turn 41) was initially scripted as removing the tackled unit from the pitch entirely (`pos[side][unit] = None`), as if it were a sent-off player rather than just a change of possession. This is wrong per §7 — a lost Tackle only changes who has the ball, the tackled unit stays on the pitch. It was caught immediately (this was the *first* won Tackle in the whole 48-turn match, so nothing else was affected) and corrected before the turn was saved. This is a bug in my own turn-by-turn scripting, not a rulebook or `sim.py` library bug — the tackled unit's position was restored and the rest of the match played out correctly from there.
2. **Zero Discipline events again** — no Foul Tactic Card played, no Slide Tackle attempted (see above), so no Discipline Deck draws this match either. Combined with the earlier factual audit (zero Discipline events across quick1, quick2, and the first full match too), this is now four playtests in a row with no fouls, yellows, or reds at all. That's either a sign the Foul/Slide-Tackle-risk mechanics are simply rare in practice (plausible — they both require a deliberate choice under pressure that a scripted "always play the odds" playtester may be under-selecting for), or a sign real human play would trigger them more than this simulation does. Worth keeping in mind when judging how tested the Discipline system actually is.

## Bottom line

A much livelier match than the aggression-vs-counter game: constant contested midfield battles, several genuine one-on-one breakaways in both directions, real shots and real saves, and a 0-0 that reflects finishing variance rather than a stale or clogged game state. It's a good sign for the anti-stalemate fixes as a group — but the Slide Tackle question is still open, and the cycling frequency on Lane/Third cards is a new data point worth watching in future playtests.
