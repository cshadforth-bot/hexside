# Hexside — Base Game Review (rulebook §1/§14, `driver_base.py`, N=400 batches)

**Date:** 2026-09-08
**Scope:** The **Base Game** specifically — the Tactic-Deck-less tier defined in `source/hexside-rulebook.html` §1 and §14, played by `engine/sim.py`'s `ROSTER_BASE` and `playtest-ai/driver_base.py`. Read against `2026-09-08-full-game-review.md` and `2026-09-08-base-game-roster.md` so as not to re-litigate the Advanced Game's own issues; Advanced-Game findings appear below only where the Base Game changes their shape.
**Method:** Read-only. No canonical file was modified. All batches were run by invoking the real, unmodified `playtest-ai/driver_base.py` with the working directory set to scratch space outside the project, so its runtime JSON (`state.json`, `game_random.json`, `batch_stats.json`) landed in scratch rather than in the repo. Four N=400 batches, one N=400 Advanced comparison batch, plus N=200 instrumented runs and one full match log.

---

## Verified-good

Stated first so the rest reads as exceptions.

- **`ROSTER_BASE` matches §14's Base table exactly.** `engine/sim.py:205-211` vs `hexside-rulebook.html:530-539`: GK 2/0/2/2-—/2 Save 3, SW 3/3/**4**/2-2/2, WB 2/3/**5**/3-2/3, PM 3/4/4/4-3/2, PO 4/5/**5**/1-4/2. All 30 numbers agree, and §14's prose ("Control +2 for the Sweeper, Wingback, and Poacher", Playmaker untouched) reconciles with both.
- **The rulebook PDF is current.** `hexside-rulebook.pdf` (41 pages) contains "Base Game", "Advanced Game", "The Base Game Roster", "Flair Points that pay for it" and "Control +2". Its mtime (13:28) is after `source/hexside-rulebook.html` (13:27). No export drift on the Base Game content.
- **`driver_base.py` genuinely disables the Tactic Deck.** Three independent mechanisms, all correct: `:69` swaps `sim.ROSTER`; `:73-86` replaces `sim.replenish` with a version that never tops up `hand_tac`; `:91` clears `new_state()`'s own initial 3-card deal. Confirmed empirically — **0 Tactic Card plays of any of the 13 types across 400 matches**.
- **The docstring's "every Tactic Card check safely no-ops on its own" claim is true.** I traced all 13. Every gate resolves through `can_afford()` (`:110-111`) or a bare `'X' in s['hand_tac'][side]` test (`:199`, `:220`, `:243`, `:275`, `:548`), and `hand_tac` is permanently `[]`. No path can fire. (One consequence of keeping them is not harmless, though — see Engine/Driver Check 3.)
- **Base Game Discipline arithmetic is exactly as the rules imply.** N=400: 3,043 tackles, 608 won, and **2,435 Discipline draws = exactly 3,043 − 608**. Every single draw in the Base Game is one standard lost Tackle, drawn once. `fouls_played` and `slidetackle_played` are 0 across the whole batch, as they must be.
- **The Base Game roster does what it was retuned to do.** Against my own Advanced N=400 control, the Playmaker's share of shots falls **73.6% → 60.7%** and its share of goals **73.5% → 61.8%**, while the Sweeper rises from 9.0% to 18.9% of goals. The `2026-09-08-base-game-roster.md` conclusion reproduces.
- **`check_no_overlap()` never fired** across 1,600 simulated matches (~76,800 turns). No crashes.

---

## 1. Rulebook Check

### 1.1 The split is announced in exactly two places and marked nowhere else

`grep` for "Base Game"/"Advanced Game" across the whole rulebook returns hits on **five lines only**: `:112` (§1) and `:527`, `:528`, `:529`, `:540` (§14). That is the entire footprint of a two-tier structure.

Both statements are individually well written. §14's (`:528`) is the better one and is the one a designer would call canonical. But they **do not say the same thing**, and §1 is the one a first-time reader hits first:

- `:112` — "the **Base Game** (everything here except the Tactic Deck, §11)... They share every rule except the Player Roster's numbers".
- `:528` — "the **Base Game** — everything in this rulebook except the Tactic Deck (§11) **and the Flair Points that pay for it**".

So §1 says the Base Game keeps Flair and differs only in roster numbers; §14 says it drops Flair. Those cannot both be true, and the difference is not cosmetic — Flair is referenced 27 times in the rulebook, including on the dice table every player reads in their first five minutes. §1 should be brought in line with §14.

### 1.2 Everything a Base Game player would actually need marked, isn't

Because the split is confined to §1 and §14, a Base Game reader walks into the following unmarked:

| Where | What it tells a Base Game player to do | Reality |
|---|---|---|
| `:126` (§3 Components) | Print the **Tactic Deck — 26 cards, printed twice (52 physical cards)** | They will never use one of them |
| `:181` (§5 Setup step 4) | "Shuffle the Command Deck, **Tactic Deck**, and Discipline Deck separately. Each side draws... **3 Tactic Cards**" | There is no Tactic hand |
| `:273` (§8 dice table) | Die faces 3–4 = "**Flair (bank 1 Flair Point)**", on *both* die types | 2 of 6 faces on every die in the game are inert |
| `:288` (§8 Tackle) | A lost Tackle "costs the tackling side **1 Flair Point**, if they have one banked" | Nothing to lose; the tax silently vanishes |
| `:239-247` (§7 Resolution Sequence) | A six-step sequence with four card windows | Two windows are permanently empty (see 1.3) |
| `:389` (§10 Reactions) | A paragraph on "**Four Tactic Cards** behave like Counters" | All four are gone |
| `:396` (§11) | Cycling a Tactic Card for 1 Flair | No deck, no Flair |
| `:440-441`, `:451-453` (§12) | Warning/Advantage's free kick; Slide Tackle and Foul draw rows | None can occur (see 1.4) |
| `:463-494` (§12.5) | Three worked examples | Two are Advanced-only; the third cites Flair (`:490`) |
| `:498-502` (§13 Set Pieces) | The Free Kick, falling back, direct/indirect | Unreachable (see 1.4) |
| `:568`, `:573` (§17 Build Guide) | "Print the **4 Command pages and 3 Tactic pages twice each**"; "Playtest the core loop first — before worrying about **Tactic Cards**, Fouls, or Set Pieces" | §17 still describes the pre-split world; it never mentions that the Base Game *is* that suggestion, formalised |
| `:592`, `:598`, `:599`, `:610`, `:620` (§18 Glossary) | Cycling, Flair Point, Foul, Resolution Sequence, Tactic Card | All written Advanced-only |

**Verdict: the split is not clear to a first-time reader.** §1 tells them they're playing a subset, then thirteen sections proceed to teach the superset without a single marker. §17 is the sharpest example — it is the one section explicitly aimed at a first-time table, it gives exactly the advice the Base Game exists to institutionalise, and it does not know the Base Game exists.

The cheapest fix is a marker convention (a tinted "Advanced Game only" tag, applied to §11 wholesale plus the ~12 lines above), not new prose. The second-cheapest is a single "What the Base Game leaves out" box in §1 listing them.

### 1.3 The six-step Resolution Sequence has three live steps in the Base Game

`:239-246` teaches six steps. In the Base Game:

| Step | Base Game status |
|---|---|
| 1. Tactic Card (active player) | **Permanently empty** |
| 2. Opponent's Reaction | Reduced to the **Counter** Command Card, plus the Wingback's **Last Man** once per match. Press/Foul/Jockey all gone |
| 3. Roll | Live |
| 4. Post-Roll Tactic Card | Reduced to the Poacher's **Clinical**, once per match. Step-Over/Nutmeg gone |
| 5. Opponent's Post-Roll Reaction | **Permanently empty** — Last-Ditch Block was the only occupant |
| 6. Apply the result | Live |

A Base Game player is taught a six-step procedure they will execute as three steps for almost the entire match. `:247` ("Each side may play at most one Tactic Card in step 1 and one in step 4 per Resolution Sequence") is dead text for them. This is the single biggest missed simplification in the tier: the Base Game's actual resolution procedure is **"roll, apply, unless the defender spends a Counter"** — three lines — and printing that as the Base Game's own sequence would cut the game's hardest-to-hold procedure by half.

### 1.4 The Foul question: yes, it's a genuine gap, but a small and mostly-benign one

**Answer to the brief's question:** In the Base Game there is **no way whatsoever to deliberately stop play**, and Discipline comes *only* from a standard lost Tackle, drawn once. Confirmed both in the rules and empirically (2,435 draws = 2,435 lost tackles, N=400).

The chain: Foul is a Tactic Card (`:413`), and `:288` is explicit that "A Foul, in the full sense — stoppage, Free Kick, falling back, the lot — **only ever comes from the Foul Tactic Card**". Slide Tackle is also a Tactic Card (`:409`). So both of §12's non-standard draw triggers are gone.

Downstream consequences, none of which the rulebook flags:

1. **§13 Set Pieces is entirely unreachable.** The Free Kick is the only set piece in the game, and only a Foul creates one. In the Base Game §13 is three paragraphs of rules that can never fire. (It is *also* the section the earlier review found under-specified — so the Base Game accidentally sidesteps that problem.)
2. **3 of 12 Discipline cards become pure no-ops.** Warning ×2 (`:440`, "Play on from a free kick at the spot of the foul") and Advantage/Play On ×1 (`:441`, "may ignore the stoppage... the free kick being available next stoppage") both describe a stoppage that cannot exist. Added to Clean Challenge ×6, the effective Base Game Discipline deck is **9/12 nothing, 2/12 Yellow, 1/12 Red**. That is worth stating plainly on the page rather than leaving a table to be worked out.
3. **§12's trigger table (`:451-453`) has one live row of three**, and **§12.5's worked examples have one live example of three** — "One Foul, four possible draws" (`:465`) and "A mistimed Slide Tackle, two draws deep" (`:477`) are both Advanced-only. The surviving one (`:487`) still says "The Sweeper loses 1 Flair, if Team A had one banked" (`:490`).

**Is this a gap or a fine simplification? Mostly a fine simplification, with one thing that needs saying.**

Losing the ability to cynically stop play is a genuine loss of expressive range, but it is the *right* thing to cut for a first game: the Foul card is the one place in Hexside where a player deliberately courts a Red Card, and the earlier review already established that Discipline is the most out-of-band system in the design. Removing it is a net win, and the Base Game's measured discipline rate is duly gentler than the Advanced Game's (1.54 vs 1.76 cards/match; 43.0% vs 48.8% of matches with a send-off). Losing §13 is also fine — a first game does not need a set piece.

What is *not* fine is leaving 3 of 12 Discipline cards printed with text that cannot apply, in the one deck a Base Game table draws from six times a match. Either print a Base Game note ("Warning and Advantage have no effect in the Base Game — there is no stoppage to play on from"), or accept that a quarter of the deck reads as a rules error to a new player. Given that the physical deck is shared between tiers, a one-line footnote on §12's table is the whole fix.

### 1.5 Keeper's Call is broken in the Base Game, and §6 says the opposite

`:205` — Keeper's Call: "Activate your Goalkeeper only... **Whether or not they do anything at all, draw one extra Tactic Card this turn regardless — the guaranteed payoff that makes this never a wasted draw.**"

In the Base Game there is no Tactic Deck, so the guaranteed payoff does not exist, and the card becomes precisely the wasted draw §6 promises it can never be: activate one unit, Pace 2, confined to a three-hex zone, with nothing else. This is a **direct contradiction between §6's own text and §14's definition of the Base Game**, and it is the only place I found where a Base Game rule is not merely unmarked but actively wrong.

It is not rare. Keeper's Call is 2 of 35 Command Cards, and the driver played it **1.76 times per match** (353 times over 200 matches). Roughly 3–4 Keeper's Calls a match across both sides, each one a card whose stated compensation is absent.

Options: give the Base Game's Keeper's Call a different guaranteed payoff (an extra Command Card draw is the obvious like-for-like), or state that in the Base Game it also activates one other unit of your choice, or simply say in §14 that the two Keeper's Call cards are removed from the Base Game's Command Deck. Any of the three is fine; leaving it is not.

### 1.6 The printed Player Roster has no Base Game cards at all — highest-severity finding

`source/hexside-cards.html:120-125` defines exactly five Player Roster cards, and they carry the **Advanced Game** numbers: Sweeper Control **2**, Wingback **3**, Playmaker 4, Poacher **3**. I confirmed this renders through to the physical component — `hexside-cards.pdf` page 5 prints "Sweeper / Control 2", "Wingback / Control 3", "Poacher / Control 3". A `grep` of `hexside-cards.html` for "Base Game", "Advanced Game" or any Base roster value returns nothing.

So a Base Game table that builds the prototype as instructed gets player cards with **Control 2/3/4/3** when their game calls for **4/5/4/5**. And §14's own opening line (`:507`) — "**See the printed Player Roster for full cards**" — points them straight at the wrong numbers, in the section that then prints the right ones two tables lower.

This silently reverts the entire Base Game retune. Everything in `2026-09-08-base-game-roster.md` — the whole reason `ROSTER_BASE` exists — is undone by playing with the printed cards. On my own measurements, that means a Base Game table is playing the "unpatched" variant the retune was created to avoid: dribble win rate ~44% instead of ~53%, and the flatter game the report explicitly says would "ship a worse game to exactly the players (new/casual) it's meant to welcome."

`hexside-cards.html` needs a second five-card Player Roster set (or a dual-value line on each card, e.g. "Control 2 / **4 Base**"), and §17's build guide (`:568`, "The Player, Discipline & Reference, and Backs pages print once") needs updating to match. This is P0.

### 1.7 Smaller Base-Game-specific notes

- `:278` — the stale "**(1–3)**" dice-range parenthetical (already flagged as 1.1 in the earlier review, still unfixed) is **worse** in the Base Game than in the Advanced Game: `ROSTER_BASE` reaches Control **5**, so the sentence that teaches dice-reading is now wrong by two rather than one, in the tier aimed at first-time players.
- `:242` — "dice per **§8–8**" is still there.
- `:499` — "whichever of **the two ways in §12** caused it" is still there, and in the Base Game there are *zero* ways.
- `:540` — §14's closing paragraph is good, honest writing (it states the Tackle-win-rate cost openly and flags the Wingback as unresolved). No complaint; noting it because it is the model the rest of the split should follow.

---

## 2. Engine/Driver Check

### 2.1 What `driver_base.py` gets right

The three-mechanism deck disabling (2.1 above under Verified-good) is correct and complete, and the docstring's stated rationale for a separate file rather than a flag (`:8-14`) is sound — the batch outputs are unambiguous about which ruleset produced them. `sim.ROSTER = sim.ROSTER_BASE` at `:69` is a module-global rebind, so it correctly reaches inside `sim.py`'s own `shot_dice()` (`:470-477`), `save_stat()` (`:462-468`) and `reach()` (`:724-745`) as the comment claims. I verified `save_stat` returns 3 for the Base GK and `reach` uses Base Pace.

### 2.2 Things it does that the rulebook doesn't authorize

**(a) It runs a Flair economy the Base Game doesn't have.** `sim.roll()` (`:364-373`) banks Flair on every roll, and `sim.contest(..., is_tackle=True)` (`:384-386`) docks 1 Flair on every lost Tackle — 2,435 times per 400 matches. §14 (`:528`) says the Base Game has no Flair Points. The divergence is **outcome-inert** (nothing in the Base Game reads the bank: `can_afford` is gated on an empty hand, and `maybe_play_press`/`try_jockey` are gated on cards that never arrive), so no batch number is affected. But it means the Base Game logs are full of `[failed Tackle: B docked 1 Flair, now 4]` lines describing a resource the tier doesn't have. Cosmetic, but it will confuse the next reader of a Base log, and it is the kind of thing that stops being inert the moment someone adds a Flair sink.

**(b) It prints a Tactic Card usage table that is structurally all zeros.** `:732-749` unconditionally prints `=== Tactic Card usage (all 13 now modeled) ===` followed by thirteen `0 (0.0/match)` rows. Harmless, but it's the driver's own summary asserting something the file's docstring spends a paragraph explaining is impossible.

### 2.3 Things the rulebook authorizes that it doesn't do

Most of these are pre-existing and inherited unchanged from `driver.py`, so they do **not** bias Base-vs-Advanced comparisons. I list them because they set the confidence interval on the absolute Base numbers.

1. **No reactions of any kind are modelled in the Base Game.** `find_card_for` (`:117-122`) skips `Counter` explicitly at `:119`, and the four Tactic-Card reactions are gone by construction. In the Advanced Game the driver at least models Press (0.62/match), Jockey (0.56), Last-Ditch Block (0.45) and Foul (0.40). **In the Base Game, Resolution Sequence steps 2 and 5 are empty in every batch ever run** — the defending side has literally no ability to interfere with any roll.

   This matters for how `2026-09-08-base-game-roster.md` should be read. Its headline comparison sets a Base Game with *zero* modelled reactions against an Advanced Game with *four*. The Base Game's measured 53.4% dribble win rate is therefore an over-estimate of what a real Base table would see, because Counter (3 of 35 Command Cards — a side holds one about 43% of the time, and may hold up to 3) can add a Defense die to exactly that roll. The **relative** finding stands (Counter is missing from both tiers equally), but I would not treat "Control +2 restores the Advanced Game's dribble win rate" as settled until Counter exists in the engine, because Counter is a much larger share of the Base Game's total interaction budget than of the Advanced Game's.

2. **Full Press still costs nothing and grants nothing.** `s['debt']` is never set by either driver — I grepped both N=400 logs for the `Full Press debt` line `sim.replenish` emits and got **0 hits in 800 matches**. And `sim.py` has no concept of an Act, so the second Act (§6, `:204`) is unmodelled. The driver played Full Press **2.97 times per match** in the Base Game — 9.5% of all Command Cards played, second only to Tactical Free.

   **This is the brief's Full Press question, and the answer is yes, it is disproportionate — but not for the reason expected.** It isn't that the two-Act mechanic overshadows a quieter turn; it's that neither half of the card is implemented. As simulated, Full Press is "activate all five units, free, forever" three times a match. In the Advanced Game that sits among ~5 Tactic Card plays a match competing for attention; in the Base Game it is, by a distance, the strongest thing that can happen on a turn, and nothing offsets it. Any Base Game Command-deck balance conclusion is compromised until `debt` is wired up. I would put implementing the debt ahead of any further Base Game tuning batch — it is three lines and it touches 9.5% of card plays.

3. **The escape-hex rule is still never called.** `sim.would_seal_last_gap()` and `sim.escape_hexes_free()` (`sim.py:866-876`) have no caller in either driver. Unchanged from the earlier review's 3.11.

4. **`sim.py`'s "WHAT THIS ENGINE DOES NOT DO" (`:143-148`) is now also wrong about the Base Game.** It still claims Set Pieces are implemented "beyond a plain Free Kick restart" (there is no free-kick code at all — earlier review 2.9, unfixed), and it says nothing about the Base Game, `ROSTER_BASE`, or the fact that Cycling, Counter, Full Press's debt and second Act, Keeper's Call's bonus draw and the box-defender die are all absent. For a Base Game reader that list is more misleading than for an Advanced one, because in the Base Game those absences are a much larger fraction of what's left.

5. **Turn order still ignores the coin flip.** `driver_base.py:681` — `mover = 'A' if t % 2 == 0 else 'B'`, so B always moves first regardless of `s['kicker']`, exactly as `driver.py:659` does. §5 rule 1 (`:178`) says the side with kickoff moves first. Inherited, unchanged.

### 2.4 One new driver bug, Base-Game-relevant

**Pass-target selection is effectively arbitrary whenever more than one target is legal.** `handle_kickoff_release` (`:387`) and `free_followup_pass_after_tackle` (`:585`) both sort candidate receivers by `B.shot_dist(hex, attacking_end)`, falling back to `99` when it returns `None`. But `shot_dist` is defined for only **37 of the pitch's 61 hexes (60.7%)** — it returns `None` for any hex with no straight line to the net, including **E3, E4, G3, G4**, the very hexes the kickoff pass targets. So for most candidate sets every entry scores 99, the sort is a no-op, and the receiver is chosen by `dict` insertion order of the formation template.

In the canonical formation this is masked, because the Poacher's Pass Range 1 leaves exactly one legal target. It stops being masked the moment anything changes — which is how I found it (see 4.2). It also silently governs every post-tackle follow-up pass in both tiers.

The same `None → 999` fallback drives the carrier's own navigation in `move_ball_carrier` (`:415-418`) and `dynamic_followup_move` (`:341-345`): the driver doesn't advance toward the goal, it advances toward *having a straight shooting line*. That is a real limitation on how much the batch numbers can say about spatial play, and it is a plausible contributor to the earlier review's finding that play funnels through a handful of hexes. Identical in both drivers, so comparisons are safe.

---

## 3. Playthrough Results

All runs invoke the real, unmodified `playtest-ai/driver_base.py`, with cwd set to scratch space.

### 3.1 Batch data — Base Game, N=400

| | **Base N=400** | Advanced N=400 (my control) |
|---|---|---|
| **Goals / match** | **1.840** (SD 1.423, 95% CI ±0.139) | 1.975 (SD 1.526, ±0.150) |
| Goal distribution | 0:72 1:116 2:94 3:62 4:41 5:10 6:3 7:2 | 0:76 1:93 2:95 3:72 4:40 5:16 6:6 7:1 8:1 |
| **Scoreless matches** | **72 / 400 = 18.0%** | 76 / 400 = 19.0% |
| Drawn matches | 37.0% | 39.2% |
| At least one side blanked | 61.8% | 56.2% |
| **Shots / match** | **3.672** | 3.808 |
| Shot conversion | 50.1% | 51.9% |
| Tackles / match (win rate) | 7.61 (**20.0%**) | 8.21 (26.2%) |
| Dribbles / match (win rate) | 10.94 (**53.4%**) | 11.13 (55.6%) |
| Breakaway share of shots / goals | 70.3% / 75.4% | 67.1% / 71.1% |
| **Discipline draws / match** | **6.088** | 7.258 |
| Yellow cards / match | 1.015 | 1.107 |
| Sin-bin trips / match | 1.015 | 1.117 |
| **Send-offs / match** | **0.522** | 0.642 |
| **Cards / match** | **1.538** | 1.762 |
| Send-off distribution | 0:228 1:137 2:33 3:2 | 0:205 1:144 2:40 3:11 |
| Matches with ≥1 send-off / ≥2 | **43.0% / 8.8%** | 48.8% / 12.8% |
| Automatic goals (whole batch) | 23 | 25 |

The Base Game lands within ~7% of the Advanced Game on every headline. Given SE ±0.071, the 0.135 goals/match gap is ~1.9 SE — marginal, directionally real, not large. **The retune worked.** `2026-09-08-base-game-roster.md`'s figure of 1.945 sits 1.5 SE above my 1.840; both are consistent with a true value near 1.9.

### 3.2 Goal share by position — Base Game, N=400

| | Shots | Share of shots | Goals | **Share of goals** | Conversion |
|---|---|---|---|---|---|
| Sweeper | 358 | 24.4% | 139 | **18.9%** | 38.8% |
| Wingback | 13 | **0.9%** | 4 | **0.5%** | 30.8% |
| Playmaker | 892 | 60.7% | 455 | **61.8%** | 51.0% |
| Poacher | 206 | 14.0% | 138 | **18.8%** | 67.0% |

Advanced control, same batch size: PM **73.5%** of goals, SW 9.0%, PO 16.7%, WB 0.8%.

**My honest read: better than the Advanced Game, and still not healthy.**

The good news is real and should be said clearly — the Base Game's roster produces a **meaningfully better-spread team than the Advanced Game does**, which is a slightly awkward thing for the "simplified" tier to be true of, but it is true. Moving the Playmaker from 73.5% to 61.8% of goals, and lifting the Sweeper from 9.0% to 18.9%, turns a one-man team into a two-and-a-half-man team. The Poacher also finishes best on the roster (67.0%), which reads correctly.

The bad news is that **61.8% is still one unit scoring more than the other three combined**, in a game whose entire pitch is five players, and the **Wingback is not in the game at all**: 13 shots and 4 goals in 400 matches — one shot every 31 matches. That isn't an under-used position, it's a position a new player will conclude is broken. §14 (`:540`) and `2026-09-08-base-game-roster.md` both flag this and both correctly say Control wasn't going to fix it. I agree, and section 4 below is my answer to what would.

For a game "whose whole purpose is being a good, complete first experience", the distribution I'd want is roughly 35/25/25/15. What ships is 62/19/19/0.5. The Base Game moved a third of the way there and then stopped because it was only allowed to touch Control.

### 3.3 Turn-level activity — Base Game, N=200 (9,600 turns)

| Turn type | Count | Share |
|---|---|---|
| Command Card played **and** dice rolled | 3,957 | **41.2%** |
| Command Card played, no dice rolled | 2,526 | 26.3% |
| **No Command Card played at all** | 3,092 | **32.2%** |
| Dice rolled with no card played | 25 | 0.3% |
| Turns containing "no better advance found" | 877 | 9.1% |

Nearly a third of turns pass with no card played. Most of that is a driver limitation — `reposition()` (`:622-638`) and `move_ball_carrier()` (`:420-424`) both return silently when `find_card_for()` can't reach the one unit they wanted, instead of playing a different card, activating someone else, or Cycling. A human would never forfeit a turn there. But it is also a real measure of Command Card friction, and the number is worth having: in ~32% of turns, *no card in a five-card hand activated the unit the player most wanted to move.*

### 3.4 The one match, read qualitatively (match 7, full 48-turn log)

Final score **A 0–0 B**. Two shots. Nine tackles, none won. **Nine Discipline draws.** One red card. Four dribbles.

**What works.** The opening is football-shaped and reads well. Turn 2: A's Poacher releases the kickoff to the Playmaker, who immediately drives at F4, wins the Dribble Challenge, and carries. Turn 3: B's Sweeper comes across to tackle at H3 and is beaten (0 successes vs 3 stops). Turn 4: the Playmaker shoots and the keeper saves 1–2. That four-turn sequence — restart, carry, challenge, shot — is genuinely the game working, and without a single Tactic Card in it. **The Base Game's core loop is intact and it is the good part of Hexside.** Nothing about removing the deck damaged it.

**What doesn't — and this is the finding of the review.** From turn 8 to turn 24, and then again from turn 38 to turn 48, **the match simply stops.** Team B's Goalkeeper ends up holding the ball at J3, inside its own Goalkeeper Zone, and the log reads:

```
=== Half 1 Turn  9 (B) ===   [B GK holds at J3 (shot_dist 10), no better advance found]
=== Half 1 Turn 11 (B) ===   [B GK holds at J3 (shot_dist 10), no better advance found]
=== Half 1 Turn 13 (B) ===   [B GK holds at J3 (shot_dist 10), no better advance found]
... turns 15, 17, 19, 21, 23 — identical ...
=== Half 1 Turn 16 (A) ===   (nothing at all)
=== Half 1 Turn 18 (A) ===   (nothing at all)
... A's turns 20, 22, 24 — also nothing ...
```

Eight consecutive B turns and five consecutive A turns in which literally nothing happens. The second half dies the same death from turn 38. Seventeen of the match's 48 turns are this.

The mechanism is a clean interaction of three published rules:
1. §8 (`:258`) parries a saved shot to the *other hex of the goal box* — inside the Goalkeeper Zone.
2. §8 (`:262-263`) lets the Goalkeeper claim it, free, via Command the Box or a normal activation.
3. §4 (`:159`) confines the Goalkeeper to its three-hex zone, "**full stop**".

So the ball is now held by the one unit on the pitch that is physically incapable of advancing it. `sim.legal_reach()` (`:753-767`) correctly returns only the three zone hexes, all of which are equally far from goal, so there is no move that improves anything.

**How much of this is the rules and how much is the driver?** Mostly the driver — but the Base Game makes it worse, and the rulebook is not blameless.

- The rules *do* have an answer: §8's **Clearance** (`:281`), explicitly described as "the release valve for a unit holding the ball under pressure with no safe pass". I checked the geometry — a keeper on B3 has **11** legal straight-line Clearance targets within Pass Range 2, and on A3/A4/K3/K4 it has **9**. There is never a position where a keeper cannot clear. So a real table does not deadlock here.
- But **neither driver implements a plain Pass or Clearance at all.** `grep` finds no clearance code in `driver_base.py`. The driver only ever passes at kickoff, after a won tackle, or via One-Two / Backheel / Long Ball — **all three of which are Tactic Cards**. So in the Base Game the stuck-carrier branch at `:452-467` tries Backheel, no-ops, logs "holds", and returns. **The Base Game driver has no bail-out whatsoever.**

Measured across N=200 for both tiers:

| | Base | Advanced |
|---|---|---|
| "no better advance" hold turns / match | **4.33** | 3.99 |
| ...of which the holder is the Goalkeeper | **95%** | 95% |
| Matches with a GK frozen on the ball ≥3 of its own turns running | **42.5%** | 38.5% |
| Longest freeze observed | 10 own turns | 10 own turns |

So this is **not** primarily a Base Game problem — it happens in 38.5% of Advanced matches too, because Backheel/Long Ball are only in hand and affordable a fraction of the time. The Base Game is 4 points worse, not 40. But it is the dominant qualitative feature of Base Game play as currently simulated, it is the reason ~32% of turns are empty, and **it depresses every Base Game batch number in this project relative to what the rules actually permit**. Wiring a plain Pass/Clearance into the driver is, in my view, the highest-value change available to the playtest harness — higher than the Full Press debt.

The third thing the match shows is the one the earlier review already named, undiminished: **9 Discipline draws to 2 shots.** In the Base Game, where every draw is a lost standing Tackle and 9 of 12 cards do nothing, the referee is still four and a half times busier than the strikers.

---

## 4. Stalemate Risk

### 4.1 The earlier review's analysis holds, essentially unchanged

`2026-09-08-full-game-review.md` §4 rested on three things: Cycling is free and unconditional (§6, `:190`); a ball-carrier can stand still forever (§9, `:376`); there is no clock pressure of any kind (§15). All three are Command-Card-level or turn-structure rules, none touched by removing the Tactic Deck. **All three hold verbatim in the Base Game.**

Its second leg — that breaking a stall is actively punished because tackling is both ineffective and dangerous — holds too, and is **worse in the Base Game**:

| | Base | Advanced |
|---|---|---|
| Tackle win rate | **20.0%** | 26.2% |
| Lost tackles / match | **6.09** | 6.06 |
| Expected attempts to win the ball back by tackling | **5.0** | 3.8 |
| Expected Yellows per ball won by tackling | **0.67** | 0.47 |
| Expected Reds per ball won by tackling | **0.33** | 0.24 |

A Base Game side that needs a goal must accept **a one-in-three chance of a red card for each time it wins the ball back by tackling** — up from one in four in the Advanced Game. `2026-09-08-base-game-roster.md` flagged this trade openly ("Tackle win rate falls further under this roster... a real, deliberate trade, not a side effect"). I'd sharpen the accounting: the trade wasn't only livelier attacking for weaker defending, it was livelier attacking for a **worse stalling incentive**, because it made the press-vs-stall economics 30% more lopsided in the staller's favour. That consequence isn't in the roster report and I don't think it was priced in.

### 4.2 What the Base Game changes, in both directions

**Worse:**
- Tackle economics, as above.
- **Counter is the only reaction left.** In the Advanced Game a stalling opponent still faces Press (forces a Tackle Challenge), Foul (stops an action outright) and Jockey. Strip those and the Base Game's *entire* toolkit for making a passive opponent uncomfortable is three Counter cards. That is a large reduction in the anti-stall surface, and it is unmodelled, so no batch number reflects it either way.
- **The goalkeeper black hole (3.4) is a stalling mechanism nobody designed.** A leading side whose keeper has the ball, inside a zone no opposing unit may legally enter (§4, `:159`), is in the safest possible position in the game. It cannot be tackled without the opponent standing adjacent from outside the zone; it cannot be dispossessed by a Dribble Challenge (it isn't moving); and §9's "trigger is movement, not proximity" (`:376`) means standing still costs it nothing. A player who wants a 0–0 currently has an *optimal, rules-legal, unbreakable* way to get one, and it is the position 42.5% of matches wander into by accident.

**Better:**
- Removing the Foul card removes the cynical-stoppage lever entirely.
- 18.0% scoreless vs 19.0% is a wash, but "at least one side blanked" is *worse* in the Base Game (61.8% vs 56.2%) — the Base Game is slightly more prone to one-sided nothing.

### 4.3 Verdict

**The original stalemate analysis holds unchanged, and the Base Game is modestly worse on every axis of it.** It is not catastrophically worse — the differences are 4-7 points, not step changes — but every one points the same way, and one of them (the goalkeeper black hole) is a genuinely new hard case that the Advanced Game's Tactic Cards partially paper over and the Base Game does not.

If I were fixing one thing for the Base Game specifically, it would not be the Cycling rule. It would be **saying, in §4 or §8, what a goalkeeper in possession must do** — even something as light as "a Goalkeeper that gains possession must Clear or Pass on its next activation" would remove both the black hole and the stall.

---

## 5. The Forward-Positioning Concentration — my own take

The exploratory finding described to me is **real, it is larger than described, and it is not really about the Playmaker and Poacher at all.** But the specific experiment described (randomising which forward takes each role) is confounded, and I got a different answer from it than the one reported. Both things are true and worth separating.

### 5.1 What I ran

Four N=400 arms, all Base roster, all through the real `driver_base.py`, differing only in the formation template.

| Arm | On the receiver hex (E4/G4) | On F3 (kickoff taker) | Goals/match | Scoreless | **Receiver-hex unit's goal share** | **F3 unit's goal share** |
|---|---|---|---|---|---|---|
| **A — canonical** | Playmaker | Poacher | 1.840 | 18.0% | **PM 61.8%** | PO 18.8% |
| **B — receiver-hex swap only** (SW↔PM slots; taker untouched) | **Sweeper** | Poacher | 1.758 | 17.8% | **SW 49.8%** | PO 13.1% |
| **C — full PM/PO swap** | Poacher | Playmaker | **1.347** | **30.3%** | PO 8.2% | PM 47.0% |
| **D — full swap incl. Pass Range** | Poacher | Playmaker | **2.248** | **14.5%** | **PO 60.5%** | PM 25.5% |

### 5.2 Arm B is the clean test, and it is decisive

Arm B holds the kickoff-taker exactly as canon (Poacher on F3, Pass Range 1, so its only legal targets are E3/E4) and changes **only which unit stands on the receiver hex** — the Sweeper moves to E4/G4, the Playmaker takes the Sweeper's old C2/I2 slot. Nothing else moves; no stat changes.

- The **Sweeper** goes from 18.9% of goals to **49.8%**, a +31 point swing, purely from standing on a different hex.
- The **Playmaker** goes from 61.8% to 35.6%, purely from *not* standing on it.
- Goals/match barely moves (1.840 → 1.758) and scoreless barely moves (18.0% → 17.8%).

The Sweeper has Shot 3, Shot Range 2 and Pace 3 — the second-worst finisher on the roster, and the *shortest* shooting reach. Put it on E4 and it becomes the team's leading scorer. **The receiver hex is worth about thirty points of goal share to whoever occupies it, independent of that unit's stats.** That is a bigger effect than every roster change made in this project put together.

The mechanism is not board geometry, and it isn't really "F3 is isolated". It is a chain of published rules:

1. §8's kickoff release (`:266`) makes the taker's **entire activation a single Pass** — it can never carry from a restart, so its ceiling is set by the rules.
2. The Poacher's **Pass Range 1** means the pass has exactly one legal destination. The receiver is not chosen, it is determined by the formation.
3. §6's **ball-carrier-is-always-activatable** rule (`:189`) then guarantees the receiver stays activatable regardless of hand — so once it has the ball, it keeps it.
4. Every restart repeats this: match start, halftime, and after every goal — roughly 4–5 times a match.

So the game hands the ball to one predetermined unit, several times a match, and then guarantees that unit can always be played. That unit ends up carrying the team. The Poacher's low share isn't a Poacher problem; it's the rules-mandated ceiling on whoever stands on the kickoff spot.

### 5.3 Where I part company with the exploratory finding

**Arm C — the straight PM/PO swap, which is what "randomise which forward takes each role" amounts to — does not reproduce the reported pattern.** With the Playmaker as taker and the Poacher as receiver, the *taker* scored 47.0% and the *receiver* 8.2% — the opposite of the reported 50-57% / 15-20%. Pooling my arms A and C (which is exactly a 50/50 randomisation, run as two equal N=400 halves rather than one mixed batch) gives **receiver-role 39.1% / taker-role 30.7%** — a real gap, but a fraction of the reported one.

The reason is a confound, and I'd want it known before anyone acts on the exploratory numbers: **swapping the two forwards also swaps the kickoff taker's Pass Range from 1 to 4.** That changes the restart structurally — the pass is no longer forced to the adjacent hex. And in arm C it interacts with the driver bug at 2.4 above: with three legal targets all scoring `99` on the `shot_dist` sort, the tie-break falls through to template insertion order and the driver passes to the **Sweeper at C2, three hexes backwards**, at every single restart. Arm C's collapse (goals/match 1.347, scoreless 30.3%, breakaway share of shots down from 70.3% to 27.5%) is substantially that artifact, not a property of the rules.

Arm D confirms it: swap the two forwards' Pass Ranges as well, so the taker is again Pass-Range-1-locked onto the receiver hex, and the effect snaps back — the Poacher on the receiver hex takes **60.5%** of goals, matching arm A's Playmaker almost exactly.

**So: three of my four arms show the receiver-hex occupant taking 50–62% of goals, and the fourth is the one where a driver tie-break bug redirects the kickoff pass.** The formation effect is real and robust. The "which forward" framing is the wrong axis, and the randomised experiment as described will keep producing noisy, partly-artifactual answers until the pass-target sort is fixed.

### 5.4 Is it a problem worth flagging? Yes — and it's the most actionable finding in this review

Three reasons:

**It's live in what ships, and it's worse in the Base Game.** The Base Game uses the original fixed formation, so this is not hypothetical. And the Base Game has fewer ways to route around it: no Long Ball to switch the play, no One-Two, no Backheel, no Through Ball. The Playmaker takes 61.8% of Base Game goals against 73.5% of Advanced ones — the retune helped — but the Base Game's *remaining* concentration is more structural, because the Tactic Cards that let a good Advanced player redistribute possession are exactly what was removed.

**It explains the Wingback, which nothing else has.** §14 (`:540`) and the roster report both note the Wingback is unfixably uninvolved and guess at "its poor Pass Range and where it sits in the default formation". Arm B settles it: it's the formation, and it isn't about the Wingback at all. Any unit parked at C5/I5 gets 0.5% of goals; any unit parked at E4/G4 gets 50-62%. The Wingback isn't a broken position, it's standing in the wrong place. That's worth knowing before anyone spends another retune on it.

**Arm D is a genuine, free design lead.** Putting the best finisher on the receiver hex produced **the best football of anything I tested**: 2.248 goals/match (+22% on canon), 14.5% scoreless (the lowest of any arm), 55.9% conversion, and a goal spread of PO 60.5% / PM 25.5% / SW 13.1% / WB 0.9%. That last number is still bad, but the top three are the healthiest distribution I saw. And §5 (`:180`) already permits this — outfield units may be placed anywhere in your own half, and "any one of your units" may be the kickoff-taker. **The default formation is a suggestion the rules already let players deviate from; it just happens to be a poor one, and it's the one every new player will copy from the figure in §5.**

**What I'd actually recommend**, in increasing order of cost:

1. **Cheapest, and I'd do it regardless:** fix the driver's pass-target sort (2.4). It is currently making formation experiments unreliable, and every conclusion in 5.3 depended on noticing it.
2. **Change the default formation figure** so the Poacher stands on the receiver hex and the Playmaker takes the kickoff. Costs nothing, breaks no rule, tested at N=400, and it improves scoring, scoreless rate, positional spread and the Poacher's relevance simultaneously. The one caveat: with the Playmaker's Pass Range 4 the taker now has a genuine choice of receiver, which a human would use well and the current driver uses badly — so this needs a re-run after (1), not before.
3. **Say something in §5 about it.** One sentence — "the unit you place within Pass Range of the kickoff spot will carry your attack; choose it deliberately" — converts an invisible trap into an actual decision. Right now §5's own advice (`:266`) is only "Placing at least one teammate within Pass Range of F3 is entirely within your own control at setup", framed purely as a legality check. It's the most consequential setup choice in the game and the rulebook treats it as a formality.

I would **not** change roster stats over this. Arm B shows Control did nothing to move it, which matches what the roster report already found when it tested a Control edge for the disadvantaged unit.

---

## 6. Playability Verdict

**Does the Base Game deliver on why it was created? Mostly yes on the game, clearly no on the presentation.**

Splitting the tiers was the right call and the roster retune was done properly — tested at real sample size, weighted rather than flat, with the cost stated openly. On the numbers the Base Game is a complete game: 1.84 goals/match against the Advanced Game's 1.975, 18.0% scoreless against 19.0%, 3.67 shots against 3.81. Those are the same game. It is not a hollowed-out version, and reading a match log confirms it — the restart-carry-challenge-shoot sequence that is Hexside's best moment plays out unchanged with no cards on the table at all. **On its own merits the Base Game is genuinely simpler and still good, and it is measurably better balanced by position than the Advanced Game is.** That is a real achievement and it should not be lost in what follows.

But "does it *feel* like the full game with something missing" is a question about the rulebook, not the dice, and there the answer is currently **yes, it feels like a subtraction**, for three specific reasons:

1. **The Base Game has no printed components.** A table that follows §17 builds the Advanced Game's player cards and unknowingly plays the unpatched roster the retune exists to prevent (1.6). Everything else in this report is secondary to that.
2. **Nothing is marked.** Thirteen sections teach the superset. A Base Game player reads a dice table telling them to bank a currency they don't have, a six-step resolution sequence of which they use three (1.3), a Discipline deck where 9 of 12 cards do nothing and 3 of those describe a free kick that cannot exist (1.4), a whole §13 that cannot fire, a Keeper's Call whose printed compensation is absent (1.5), and §17 advising them to start without Tactic Cards without mentioning that doing so has a name. Every one of these is a place a new player stops and asks "am I reading this wrong?" — which is precisely the experience the Base Game was created to prevent.
3. **The simplifications weren't taken.** The Base Game currently *removes* a deck. It doesn't yet *simplify* anything: the resolution sequence is still printed as six steps, the components list still says print 52 Tactic Cards, the glossary still defines Flair. A tier defined by subtraction reads as a lesser version; a tier with its own three-step resolution box and its own five player cards reads as a game.

None of that is deep. It's a marking convention, a second roster sheet, and about a page of Base-Game-specific text. The design work is done and it's sound — the packaging is what's missing.

Two things I'd fix *in the game*, not the book, and both are Base-Game-specific in severity rather than in kind:

- **The goalkeeper black hole** (3.4, 4.2). 42.5% of Base matches have a keeper freeze on the ball for three or more of its own turns; my sample match lost 17 of 48 turns to it across both halves. The rules have an answer (Clearance) but the driver has never implemented one, and the Base Game has no Tactic Card bail-out either. Fix the driver first so we can see the real numbers; then consider whether §4/§8 should say what a keeper in possession must do.
- **The formation** (section 5). One unit takes 61.8% of goals and another takes 0.5%, and arm B proves it's the hexes, not the stats. This is fixable for free, today, by changing a diagram.

Ordered punch-list, Base-Game-specific only:

**P0**
1. Add the Base Game Player Roster to `hexside-cards.html` (`:120-125` currently emits Advanced numbers only), and update §17's build guide (`:568`). Without this the Base Game does not exist at the table. (1.6)
2. Reconcile §1 (`:112`) with §14 (`:528`) on whether the Base Game has Flair Points. (1.1)
3. Resolve Keeper's Call (`:205`) — §6 promises a payoff the Base Game cannot deliver, on 2 of 35 cards, played ~1.8×/match. (1.5)

**P1**
4. Mark the ~12 Advanced-only passages listed in 1.2, or add a "what the Base Game leaves out" box in §1.
5. Print the Base Game's own three-step Resolution Sequence. (1.3)
6. Footnote §12's table: Warning and Advantage have no effect in the Base Game. (1.4)
7. Fix `(1–3)` at `:278` — with `ROSTER_BASE` it is now wrong by two, in the beginner tier. (1.7)

**P2 — engine/driver, before the next Base Game tuning batch means anything**
8. Give the driver a plain Pass / Clearance for a stuck carrier. Costs ~4.3 turns/match in the Base Game and is the single biggest distortion in every Base number in this project. (3.4)
9. Implement Full Press's debt — 9.5% of Base Game card plays, currently entirely free. (2.3.2)
10. Fix the `shot_dist`-based pass-target sort (`:387`, `:585`) — it silently randomises receiver choice and it corrupted one of my four experiment arms. (2.4)
11. Implement Counter. It is the Base Game's *only* remaining reaction; steps 2 and 5 of the Resolution Sequence have been empty in every Base batch ever run. (2.3.1)
12. Update `sim.py:143-148` to describe the Base Game and the real omissions list. (2.3.4)

**P3 — design leads**
13. Re-test arm D's formation (Poacher on the receiver hex) after fix 10, then consider changing §5's default figure. Best numbers of anything tested: 2.248 goals/match, 14.5% scoreless. (5.4)
14. Revisit the Base Game's 20.0% tackle win rate against its stalling incentive — the retune's honest cost is 30% worse press-vs-stall economics, which I don't think was priced in. (4.1)
