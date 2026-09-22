# 2026-09-10 — Lanes collapsed 3→2, full Command Deck remodel (9 zones → 6)

**Scope:** `engine/board.py`, `engine/sim.py`, both drivers, `source/hexside-rulebook.html` (§4, §6, §8, §11, §18, embedded pitch diagram), `source/hexside-cards.html`, `source/hexside-components.html`, `source/hexside-pitch.html`, `source/hexside-pitch-large.html`, all 5 dependent PDFs. Planned via a formal plan-mode research pass before any file was touched — see the approved plan for the full research findings this was built on.

## Why

Two things, both confirmed with real data before touching anything:

1. **Command Cards should hit more reliably.** The old board split into 3 Thirds × 3 Lanes = 9 zones, several as small as 5-6 hexes. Fewer, bigger zones directly reduce "dead" activations.
2. **The Center lane was structurally starved, worse than it looked.** Center was already the narrowest lane (17 hexes vs Top/Bottom's 22 each). Quantified during research: **every hex in both Goalkeeper Zones (A3, A4, B3, K3, K4, J3) was a Center-lane hex** — 6 of Center's 17 hexes (35%) permanently keeper-only or opponent-off-limits, entirely concentrated in Thirds 1 and 3. This is what "the middle zone is currently tiny now we have the goalkeeper box" was actually pointing at.

## The design

- **Lane boundary runs exactly through the board's physical centerline.** Tall columns (6 rows) split cleanly 3/3 (rows 1-3 Top, 4-6 Bottom) — the centerline falls *between* rows 3 and 4, no ambiguity. Short columns (5 rows) are different: row 3 sits **exactly on** the centerline (verified: `dY(row=3, short)=7`, the exact midpoint of the board's full dY range 2-12) — so it belongs to **both** lanes at once. This is a **seam row**, the Lane-axis twin of the existing seam columns (D, H) — same "on the boundary, reachable from either side" idea, just running the other way. Affects exactly 5 hexes: B3, D3, F3 (the kickoff spot), H3, J3 — including both former Goalkeeper Zone seam hexes.
- **`board.py`'s `lane()`** now returns a tuple (`('Top',)`, `('Bottom',)`, or `('Top','Bottom')`) instead of a single string. Every caller that did `lane(...) == 'X'` became `'X' in lane(...)`.
- **6 solo Zone cards** (one per Third × Lane) replace the old 4-Zone-Pair-plus-1-solo-Zone mechanism — with only 2 lanes, pairing the 2 zones in a Third would just duplicate the Third card, so there was nothing left to pair. Each keeps the same "no units there → activate 1 of your choice" fallback.
- **Curl Shot's Top/Bottom condition removed** — it was excluding Center specifically; with Center gone, "Top or Bottom" is vacuously every hex, so the die bonus is now unconditional. Cost (2 Flair) left untouched — that's a balance question for later, not part of this structural change.
- **Seam columns kept as-is**; Third 2's two new Zone cards (T2-Top, T2-Bottom) each get the same D/H reach the old Zone Pair and solo Zone cards had, split by lane. D3/H3 fall out of this automatically now (they're seam-row hexes themselves, so they already answer to both of their own Third's Zone cards without any hardcoding — the old `h in ('D3','H3')` special case is gone, not replaced).
- **Command Deck: 35 cards → 36.** 6 Zone types × 2 + 2 Lane types × 2 + 3 Third types × 2 (unchanged) + the 4 generic cards (unchanged, 14) = 12+4+6+14=36. Verified this still fits the existing physical print layout exactly (9 cards/page × 4 pages = 36, where 35 needed the same 4 pages with one spare slot before).

## Verification

- Hand-traced `card_options()` against a constructed scenario covering every interaction (a unit on a seam-row hex, a unit on a seam column, ball-carrier-always-activatable) before running anything — every one of 8 test cards matched hand-derived expectations exactly.
- Both drivers: syntax-checked, smoke-tested at N=10, then N=200 on each. No crashes. Goals/match landed at 1.80 (Base) / 2.115 (Advanced) — both within the noise band already established for these drivers across independent runs this session (1.84–2.22), so no sign of a behavioral regression from the mechanical change.
- Recomputed the kickoff-hand-probability fact in §8 exactly (hypergeometric, not estimated): with the seam-row hex F3 now reachable by *both* Lane cards (previously only Lane-Center reached it), 27 of 36 cards reach F3 directly — about 1 in 3000 hands miss all of them, versus the old 22-of-35 / 1-in-252.
- Tag-balance checks (open/close tag counts) on every touched HTML file — all clean.
- Visual spot-check of the rendered pitch diagram (rulebook §4 and the standalone `hexside-pitch.html`) in-browser: the 5 seam-row hexes render in a distinct third tint, Third 1/2/3 dividers still run through D and H, Top/Bottom edge labels replace the old three.
- All 5 dependent PDFs (`hexside-rulebook`, `hexside-cards`, `hexside-components`, `hexside-pitch`, `hexside-pitch-large`) rebuilt via `build-pdfs.sh` and confirmed newer than their HTML sources.

## What this didn't touch

No roster stats, no balance retuning — goals/match, dribble win rate, and tackle win rate were checked only for "did anything break," not re-tuned. If a future batch shows the new zone shape has shifted card-play patterns enough to matter (e.g. Full Press or Tactical Free's relative value, now that precise Zone cards hit more often), that's a fresh question for later, not something this pass addressed. Counter's unmodeled "force a Tackle Challenge" option, the receiver-hex formation question, and the tackle-rate/stalling tradeoff are all still open, untouched by this work.
