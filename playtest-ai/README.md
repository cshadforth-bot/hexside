# Hexside playtest AI

Two self-play drivers, both playing a full, unscripted Hexside match against themselves
using the real, current canonical ruleset. `driver.py` plays the **Advanced Game** — all
13 Tactic Cards, the full roster, every rule merged into `../engine` so far. `driver_base.py`
plays the **Base Game** — no Tactic Deck (swaps in `sim.ROSTER_BASE` and disables Tactic
Card refills), otherwise the same engine and the same driver logic, kept as a minimal diff
from `driver.py` rather than a second implementation. Both exist purely to batch-test the
engine and roster at volume (run N matches, get aggregate stats); neither is a strong or
even representative opponent, and several Tactic Cards (One-Two, Backheel, Long Ball in
particular — Advanced Game only, so irrelevant to `driver_base.py`) `driver.py` only
reaches for in fairly narrow circumstances. Read the module docstring at the top of
whichever driver you're using for the full list of what's modeled and the simplifications
each card needed.

Both import `sim`/`board` from `../engine` by path rather than a local copy, so they
always play against whatever is actually canonical there — no risk of quietly drifting
out of sync the way a copied-and-forgotten scratch version would after a future rule
change.

```bash
python3 driver.py 50        # Advanced Game: 50 fresh matches, aggregate stats, batch_stats.json
python3 driver_base.py 50   # Base Game: same, no Tactic Deck
```

Run either from this directory, not from inside `engine/` — like `sim.py` itself, they
write runtime files (`batch_stats.json`, `game_random.json`, `state.json`) next to
wherever they're invoked from, and those are per-run artifacts, not something to keep as
source. Running both from the same directory back-to-back is fine, but they'll overwrite
each other's `batch_stats.json` — copy it elsewhere between runs if you want to keep both.
