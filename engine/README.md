# Hexside simulation engine

`board.py` (hex-grid geometry) and `sim.py` (match state, card options, dice resolution)
implement the current canonical Hexside ruleset — see `../source/hexside-rulebook.html`
(or `../hexside-rulebook.pdf`) for the actual rules text these two files encode.

**This is a calculator, not an opponent or a rules book.** It tracks positions, tells you
which units a Command Card can activate, and resolves contested dice rolls correctly. It
does not decide what to play, does not know the Signature abilities or Set Pieces beyond a
plain Free Kick restart, and does not validate that a move you make is actually legal —
call `reach()` and check before moving a unit.

Read the module docstring at the top of `sim.py` for a full quick-start (state shape,
function list, a worked example of one turn). If you're an LLM picking this project back
up: read that docstring and the rulebook before running anything, and re-derive which end
each side attacks (`a_defends_low`) fresh each time rather than assuming — this has been
gotten backwards before.

Usage sketch:

```python
import sim, board
sim.gen_random()       # unseeded — new match, new random decks/dice
s = sim.new_state()
# ... play turns, editing s['pos'][side][unit] directly and calling sim.contest()/
#     sim.tackle()/sim.card_options() etc. as needed, sim.save(s) at the end of each turn ...
```

Run it from a scratch/working directory, not from inside this folder — `sim.py` writes
`state.json` and `game_random.json` next to wherever it's imported from, and those are
per-match runtime files, not something to keep alongside the source.

For a working example of exactly this — a full self-play match, all 13 Tactic Cards,
run at batch volume — see `../playtest-ai/driver.py`. It imports this engine by path,
so it always tests whatever is currently canonical here.
