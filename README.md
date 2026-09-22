# Hexside

Hexside is a hex-grid 5-a-side football tabletop wargame — two 5-unit sides (Goalkeeper,
Sweeper, Wingback, Playmaker, Poacher), an 11-column hex pitch, and two card decks
(Command, which decides who may act each turn, and Tactic, an optional layer of one-off
plays) that resolve contested actions with dice.

**The rulebook is the only authority.** Nothing in this codebase — engine, drivers, or
any file under `playtests/` — overrides it. If code and rulebook ever disagree, the
rulebook is right and the code has a bug.

- `source/hexside-rulebook.html` — the full rules, source of truth. Open it in a browser.
- `hexside-rulebook.pdf` — the same content, print-formatted. Regenerate with
  `./build-pdfs.sh hexside-rulebook` after any change to the HTML source (needs local
  Chrome; see the script's own comments).
- `source/hexside-cards.html`, `hexside-components.html`, `hexside-pitch.html`,
  `hexside-pitch-large.html` (+ their `.pdf` builds) — the physical components: cards,
  reference sheets, pitch diagrams.

## Base Game vs Advanced Game

Two ways to play live in the one rulebook (§1): the **Base Game** is everything except
the Tactic Deck (§11); the **Advanced Game** is the Base Game plus that deck. §1 has a
callout box spelling out exactly what dropping the Tactic Deck ripples out to — read it
before assuming a passage that mentions Flair Points, a Tactic Card, or a six-step
Resolution Sequence applies to the tier you're playing. New to Hexside, or teaching
someone who is: start with the Base Game.

## Repo layout

```
source/            Rulebook + all printable components, as HTML (edit these, not the PDFs)
engine/             board.py + sim.py — the rules engine (state, legality, dice resolution)
playtest-ai/        driver.py (Advanced Game) and driver_base.py (Base Game) — self-play
                    AIs built on the engine, for batch-testing balance at volume
playtests/          Dated write-ups of past test sessions — results, bugs found, rules
                    questions raised. See playtests/PLAYTEST-BRIEF.md if you're here to
                    run a fresh review and playtest.
build-pdfs.sh       Rebuilds any source/*.html into its matching root .pdf via headless Chrome
```

## Running the engine

Requires Python 3, no dependencies beyond the standard library.

```python
import sim, board          # run from engine/, or add it to sys.path
sim.gen_random()           # unseeded — fresh shuffled decks & dice for one match
s = sim.new_state()        # coin-flip kickoff, kickoff-placement draft, empty log
```

`engine/README.md` has the full quick-start (state shape, function list, a worked turn).
For an actual full match rather than hand-driving one turn at a time, use the self-play
drivers:

```bash
cd playtest-ai
python3 driver_base.py 50   # Base Game: 50 matches, aggregate stats, batch_stats.json
python3 driver.py 50        # Advanced Game: same, with the Tactic Deck in play
```

Run drivers from `playtest-ai/`, not from inside `engine/` — they write per-run JSON
files (`state.json`, `game_random.json`, `batch_stats.json`) next to wherever they're
invoked, and those are runtime artifacts, not source. `playtest-ai/README.md` has more
detail, including what each driver simplifies and why.

**Neither driver is a strong or "correct" player.** They exist to put volume through the
engine so balance questions have real numbers behind them, not to demonstrate good
tactics. Read a driver's own module docstring before trusting a specific in-game decision
it made.
