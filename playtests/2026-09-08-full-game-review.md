# Hexside — Full Game Review (rulebook, engine, cards, playtest batches)

**Date:** 2026-09-08
**Scope:** Complete read of `source/hexside-rulebook.html` (all 18 sections + worked examples), cross-check against `engine/sim.py`, `engine/board.py`, `source/hexside-cards.html`, `source/hexside-components.html`, and `hexside-rulebook.pdf`; plus fresh self-play batches at N=1, N=20, N=50, N=60 (instrumented) and N=200.
**Method:** Read-only. No canonical file was modified. All scenario tests were written to scratch space outside the project and are reproduced inline below so each finding is checkable.

---

## Verified-good (things I checked that are correct)

Stating these first so the rest of the report reads as exceptions, not a wall of doom.

- **Section numbering is clean.** TOC and body both run 1–18 with no duplicates, in both the HTML and the exported PDF. The renumbering fix landed.
- **The PDF matches the HTML.** Extracted 90,323 characters of PDF text against 88,146 of HTML text; every load-bearing string I probed (including the *errors* listed below) is present identically in both. No export drift.
- **The roster is consistent across all three sources.** `source/hexside-rulebook.html` §14 table, `sim.ROSTER` (`engine/sim.py:175-179`), and `source/hexside-cards.html:120-126` agree on every one of the 30 numbers, and §14's rationale prose (the Shot +1 twice, Control/Pass Range moves, Tackle moves, Shot Range +1, the Sweeper/Wingback swap) reconciles exactly with the table. Signatures moved with the swap correctly: Overlap → Sweeper, Last Man → Wingback, in the rulebook *and* on the printed cards.
- **The §8.5 worked examples all use current roster numbers** (Sweeper Control 2 / Pass Range 2, Wingback Control 3 / Tackle 3, Playmaker Control 4 / Shot 4 / Shot Range 3, Poacher Shot 5 / Shot Range 4 / Pass Range 1, Save 3). The stat fix propagated into the examples.
- **Hex geometry is correct.** `board.neighbors('F3')` → E3, E4, F2, F4, G3, G4 (matches §8's center circle). B3 is genuinely adjacent to both A3 and A4; J3 to both K3 and K4 (so the Goalkeeper Zone shape in §4 is real). `straight_line('B5','E5')` correctly returns "no line" (mismatched column parity, §4). `shot_dist('I2','K') == 3` and `shot_dist('I3','K') == 3`, matching the Shot and Through-on-Goal worked examples exactly.
- **Seam-column activation is implemented correctly**, which is fiddly enough to be worth saying. Tested with units at D2/D3/D4/H5/A3: `Third-2` → SW,WB,PM,PO; `Zone-T2Center` → the D3 unit; `ZP-Top-T2T3` → the D-Top unit; `ZP-Bottom-T1T2` → the D-Bottom unit natively plus the H-Bottom unit via the seam. The four Zone Pairs plus the single Zone card do cover all nine zones, and the two seam extras close exactly the two gaps the rulebook says they close.
- **Deck arithmetic checks out.** Command 8+1+6+6+6+3+2+3 = 35. Tactic 13 types × 2 = 26. Discipline 2+1+2+1+6 = 12. §8's "1 in 252 hands draws none of the 22 cards that reach F3" is right: C(13,5)/C(35,5) = 1287/324632 = 1/252.3, and the 22 does enumerate correctly.
- **`check_no_overlap()` never fired** across 330 simulated matches (~15,800 turns). No occupancy collisions, no crashes.
- **Print setup is A4** (`hexside-cards.html:40`, `@page{size:A4}`), consistent with the paper-size preference.

---

## 1. Inconsistencies

### 1.1 §8 says dice pools are 1–3; the roster goes to 5
`hexside-rulebook.html:277` — "The number of dice you roll equals the relevant stat on your Player Card **(1–3)**." The roster (`:510-514`) has Poacher Shot 5, Playmaker Shot 4 and Control 4. §8.5's own Shot example rolls five Attack dice. This is a stale parenthetical from before the two Shot passes; it is the single most likely thing to confuse a first-time reader, because it appears in the paragraph that teaches dice-reading. Should read (0–5).

### 1.2 §11.5's first worked example has the wrong title
`:419-422` — heading is "**Through Ball vs. a Zone of Control**"; the body plays **Backheel**, and Through Ball is never mentioned. Through Ball — the one card whose interaction with Zone of Control genuinely needs a worked example — has none.

### 1.3 Malformed cross-reference in the Resolution Sequence
`:241` — "**Roll**: dice per §8–8." Should be §8. This is step 3 of the sequence every contested roll in the game runs through.

### 1.4 §13 refers to "the two ways in §12" of causing a Foul; there is only one
`:499` — Free Kick is placed at "the ball-carrier's hex at the moment the Foul was called (whichever of **the two ways in §12** caused it)". But §8 (`:287`) and §12 (`:452`) and the glossary (`:583`) all say the same thing three times over: a Foul "only ever comes from the Foul Tactic Card", and a lost Tackle Challenge is explicitly *not* a Foul. Stale text from when lost Tackles also stopped play.

### 1.5 §16 refers to a "stalling problem noted elsewhere in this draft" that is noted nowhere
`:544` — "A card that directly targets the stalling problem noted elsewhere in this draft". I grepped the whole rulebook: the words "stall"/"stalling" appear exactly once, here. The design clearly knows stalling is a live risk (see §4 of this report) but never states it. Either the section that described it was cut, or it never got written.

### 1.6 §7 over-claims what Through Ball (and Vision) do
`:239` — "Some cards (**Through Ball**) remove the need to roll at all — skip straight to step 6." But the card (`:400`) only "ignores **one** defending unit's Zone of Control", and §8 (`:279`) is explicit that a Pass can be contested by more than one Zone of Control on the line. With two contesting defenders, Through Ball removes one and the roll still happens. The Playmaker's **Vision** signature (`:513`) repeats the same over-claim — "skipping the contested roll entirely, the same way Through Ball does". Both should be conditional.

Related, smaller: Vision's timing is cited as "(§7 step 4)". §7 step 4 is the *turn's* Act; the Pass-declaration window is *Resolution Sequence* step 1. Every other Signature disambiguates this explicitly (Clinical says "Resolution Sequence step 4", Last Man says "Resolution Sequence step 2"). Vision doesn't.

### 1.7 §12.5's worked examples predate the sin-bin and contradict §12
§12 makes the sin-bin the *headline* effect of a first Yellow (`:441`, `:458`): "the offending unit is pulled off the pitch immediately and misses its own side's next turn entirely". Both §12.5 examples then describe a Yellow as nothing but a Pace penalty:
- `:469` — "**Yellow Card** — 2 in 6 — the Sweeper's Pace drops by 1 for the rest of the match."
- `:482` — "First draw: Yellow Card — Wingback's Pace drops by 1."

A player who reads the worked examples (which is what worked examples are *for*) will never sin-bin anybody.

### 1.8 Glossary puts the Emergency Goalkeeper in the wrong place
`:580` — "placed in **the goal box** immediately". §12 (`:460`) says "placed in any free hex of **its own Goalkeeper Zone**". Those are a 2-hex area and a 3-hex area, and §4 goes out of its way to distinguish them.

### 1.9 Clean Challenge is quoted two different ways
`:443` (§12 table) — "the **challenge** failed, but it wasn't **misconduct**."
`:570` (glossary) — "the **tackle** failed, but it wasn't **a foul**."
The printed card (`hexside-cards.html:177`) and the engine's log line (`sim.py:386`) both use the glossary wording, so the §12 table is the outlier. Trivial in isolation, but it's the flavour text on a physical card, so it should be one string.

### 1.10 §6.5's Full Press hand-size table contradicts its own prose *and* the engine
`:211-221`. The table says the hand is **3** after turn N+1. The prose immediately below says "draw back up to 5 pulls in **as many cards as it takes to close the gap**, not just one" — under which the N+1 draw-up pulls two cards, discards one to the debt, and keeps one, leaving **4**. The engine implements the prose:

```
after N   hand: 4  (rulebook table: 4)  debt: 1
after N+1 hand: 4  (rulebook table: 3)  debt: 0   <-- mismatch
after N+2 hand: 5  (rulebook table: 5)  debt: 0
```

This matters beyond bookkeeping: §6 (`:189`) justifies the Cycling rule partly on "a hand thinned by Full Press can shrink to 3 — on rare occasions all 3 of those could be Counters, and cycling is then your only legal move." Under the engine's (and the prose's) reading the hand never starts a turn below 4, so that deadlock case doesn't arise from a single Full Press at all.

### 1.11 Keeper's Call describes a Shot the Goalkeeper can never take
`:204` — "Pass is the only Act that makes sense for them in practice, **but nothing stops a Shot if one's somehow legal**." The roster gives the Goalkeeper Shot **0** and Shot Range **—** (`:510`). A Shot needs a hex "within your Shot Range stat" (§8), and there is no such stat, so a Goalkeeper Shot is never legal — and even if it were, 0 Attack dice against any Save can only tie at 0, which §8 says resolves as a Save. The sentence promises an option that is provably unreachable.

### 1.12 §4's "full stop" Goalkeeper confinement vs. §5's waiver
`:158` — the Goalkeeper "**may never move outside its own zone**, full stop, whether it's simply repositioning or happens to end up as the ball-carrier itself". `:179` — "Your Goalkeeper may not be the kickoff-taker unless it's the only unit you have left; if so, it takes the spot and **its own-box requirement is waived** for that restart alone." §4's absolutism should be softened to point at §5's exception, especially since that exception is also where the game's hardest deadlock lives (§3.2/§3.3 below).

### 1.13 §7's Tactic-card budget is worded for the wrong player
`:246` — "Each side may play at most one Tactic Card in step 1 and one in step 4 per Resolution Sequence." But steps 1 and 4 are the *active* player's windows; the opponent's are steps 2 and 5. §11 (`:394`) states it correctly as "one pre-roll and one post-roll per Resolution Sequence, per side". §7 should match.

### 1.14 "Sudden-death extra 4 turns each" is two different things
`:532`. Sudden death ends the instant someone scores; "extra 4 turns each" is fixed extra time. The rulebook doesn't say which. At the table this is a real question — if A scores in extra turn 1, does B get its three remaining turns to equalise?

### 1.15 "Straight-line, in hexes" is measured in *columns* on the horizontal band
§4 (`:163`) says Pass/Shot ranges "measure distance **straight-line, in hexes**". On the fourth line type — the same-row, same-parity horizontal band — the engine measures column offset, not hex centres:

```
straight_line('B3','J3') -> (8, ['D3','F3','H3'])
```

Distance 8, but only *three* hex centres lie between the endpoints. A player counting hexes along that line at the table gets 4; the rules mean 8. §11.5's Long Ball example says "8 columns away", which is the right number by accident of phrasing rather than by the stated rule. §4 should say the band is counted in columns, or the metric should change. (Practically this only affects Long Ball, which ignores Pass Range anyway, and shot lines — see 1.16.)

### 1.16 §14's claim that the Shot Range +1 changed nothing is false for four hexes
`:523` — "The +1 **restores the exact same practical shooting distances** that were already in play before the fix (nothing about the roster's shape changes)", and `board.py:180-183` states the same thing as an invariant: `box_dist()` is "always exactly 1 less than `shot_dist()` wherever both are defined". Both are wrong at **A2, A5, K2, K5**, where `shot_dist == box_dist == 1` — those hexes touch a net hex diagonally *and* touch the box. From those four hexes every outfield unit gained a full hex of effective Shot Range in the fix rather than breaking even. Small, but the docstring asserts an invariant the code violates.

I did verify the *other* half of that paragraph: the "new shooting angles" in the short columns are real, and Shot Range coverage lands somewhere sensible — Range 4 covers exactly the attacking third (H–K, 20 hexes), Range 3 covers 15, Range 2 covers 9. That part is fine.

### 1.17 Minor
- §4 (`:160`) — kickoff-taker is "the Forward by default"; §5 (`:179`) — "normally one of the four outfield units, **not necessarily the Forward**". Pick one.
- §8.5 Dribble example (`:317`) — "moves toward C3, **adjacent to** Team B's Sweeper's Zone of Control". Should be "into a hex within". A Zone of Control isn't a thing you stand next to.

---

## 2. Errors / bugs (rulebook ↔ engine ↔ cards)

### 2.1 Every section reference in the engine is still on the old 0-indexed numbering
**67 stale references** — 58 in `engine/sim.py`, 9 in `engine/board.py`. Every single one is exactly one lower than the current rulebook, i.e. they all still map to the pre-fix numbering (Pitch=§3, Setup=§4, Command Deck=§5, Turn Sequence=§6, Actions & Dice=§7, ZoC=§8, Reactions=§9, Tactic=§10, Discipline=§11, Set Pieces=§12, Roster=§13, Winning=§14).

Examples: `sim.py:57` "DISCIPLINE (§11)" → §12; `sim.py:64` "SHOT RANGE (§7, §13)" → §8, §14; `sim.py:90` "GOALKEEPER ZONE (§3/§4/§13)" → §4/§5/§14; `sim.py:153` "§13 Player Roster" → §14; `sim.py:182` "35-card Command Deck (§5)" → §6; `sim.py:818` "§8's escape-hex rule" → §9; `board.py:1,21,28,84,128,141,150` all "§3" for pitch geometry → §4; `board.py:164` "(§3, §7)" → (§4, §8).

Because the offset is uniform, a mechanical `§N → §N+1` pass over those two files fixes all 67. This is the highest-value/lowest-risk cleanup on the list — right now every pointer from code back to the rules lands one section early, which for a project that's explicitly designed to be picked up by a future reader (or LLM) is actively misleading.

### 2.2 The printed Counter card points at the wrong section
`hexside-cards.html:103` — "Hold it, then discard to force a reaction — see Rulebook **&sect;9**." Reactions is now **§10**. This is on a physical card a player reads mid-game. Notably `hexside-cards.html:172` (a code comment) *was* updated to §12, and `hexside-components.html:39,115` use the new numbering correctly — so cards.html got a partial pass and this one printed string was missed.

### 2.3 The printed Yellow Card omits the sin-bin entirely
`hexside-cards.html:179` — "The offending unit's Pace is reduced by 1 for the rest of the match. A second Yellow becomes a Red." No mention of the unit coming off the pitch for a turn, which §12 treats as the *primary* effect ("A real, felt sin-bin"). Combined with §12.5's worked examples doing the same thing (1.7 above), the sin-bin currently exists only in §12's prose. Two of the three places a player would actually look don't have it.

### 2.4 Three more printed Tactic/Discipline cards drop material clauses
- **One-Two** (`:149`) omits "both legs **uncontested regardless of Zone of Control**" and "doesn't trigger a Dribble Challenge along the way" — which is the entire reason to play the card.
- **Long Ball** (`:151`) omits "**The destination's own Zone of Control, if the receiver is marked there, still contests it as normal**." As printed the card reads as a fully uncontested pass. This is the clause the §11.5 worked example specifically exists to teach.
- **Advantage / Play On** (`:178`) omits "in addition to **the free kick being available next stoppage**".

These aren't abbreviation, they're changes of meaning. The cards have room (Slide Tackle's card text is three times longer).

### 2.5 The card sheet doesn't produce three components the rulebook tells you to print
`hexside-cards.html` generates exactly four decks: Command (4 sheets), Player (1), Tactic (3), Discipline (2) = **10 sheets**. §3 (`:127`) also lists "**1 Dice Reference card, 1 Zone Map reference card**", and §17 (`:552`) says "**11 pages** total: 4 Command, 1 Player, 3 Tactic, 2 **Discipline & Reference**, 1 **Backs**". Neither the two Reference cards nor the Backs sheet exists in the source. The Discipline pages have 6 blank slots that would hold the reference cards. §3 also lists a Token Sheet (10 player tokens, 2 ball tokens, 4 Yellow markers) that isn't in `hexside-cards.html` either — it may be intended to live in `hexside-components.html`, but that file is a components *inventory*, not a printable token sheet.

### 2.6 The box-defender's +1 Defense die is not implemented anywhere
§8 (`:284`) specifies it in detail, including the non-obvious "only if they were named by their own side's Command Card on that side's **most recently completed turn**" reactivation requirement and a paragraph of design rationale about it being a recurring cost. `grep` across `engine/` and `playtest-ai/` finds nothing. It is absent from every batch number in this report and every prior one. Given shot conversion is running at ~50%, a missing +1 Defense die on defended shots is not a rounding error.

### 2.7 Full Press has never cost anything in any playtest
`sim.replenish()` (`:571-584`) correctly honours `s['debt'][side]`, but **nothing ever sets it**. There is no `play_full_press()` helper in `sim.py`, the docstring never tells a caller to set `debt = 2`, and `driver.py` never mentions `FullPress` or `debt` at all. `card_options()` returns all five units for it. So in every batch run to date, Full Press has been a strictly-better Tactical Free with **zero downside** — and it's 3 of 35 cards, so it comes up roughly every 12 turns. Any conclusion about Command-card balance drawn from those batches is compromised by this.

The second Act — the actual reason Full Press exists — also isn't modelled; `sim.py` has no concept of an Act being spent at all.

### 2.8 Keeper's Call's guaranteed extra Tactic Card isn't implemented
`sim.card_options()` handles the activation (`:802-806`) but nothing draws the bonus card. §6 calls it "the guaranteed payoff that makes this never a wasted draw" — as simulated, it *is* a wasted draw (activate one Pace-2 unit confined to three hexes).

### 2.9 The engine and README claim a Free Kick restart that doesn't exist
`engine/README.md` and `sim.py:139-142` both say the engine doesn't do "Set Pieces **beyond a plain Free Kick restart**", which reads as "the Free Kick restart *is* implemented". `grep -n "free_kick\|FreeKick\|set_piece"` across `sim.py` and `driver.py`: nothing. The phrasing should be inverted.

### 2.10 `legal_reach()` filters the Goalkeeper Zone by destination only, not by path
`sim.py:711-725` filters `reach()`'s result dict by final hex. The BFS in `reach()` (`:682-703`) walks freely through the opponent's zone. §4 (`:158`) says "**no opposing unit may ever enter it**" — entering includes passing through. Demonstrated:

```
GK_ZONE['A'] = ('A3','A4','B3')
B's Playmaker (Pace 3) at A2 -> destination B4 ALLOWED, path = ['A2','B2','B3','B4']
                                            illegal hex on that path: B3
```

Destinations inside the zone *are* correctly excluded, so this is a pathing hole rather than a total miss. Same issue in the other direction for the goalkeeper-role unit ("may never *move* outside its own zone" is enforced only at the endpoint), though in practice the three zone hexes are mutually adjacent so it can't bite.

### 2.11 `halftime_reset()` doesn't put the kickoff ball on F3
`goal_restart()` (`:647`) explicitly forces `pos[side][kicker_unit] = 'F3'` and its docstring warns "**don't leave a substitute kicker on its own template hex**". `halftime_reset()` (`:619-625`) does exactly that — it reads `kicker_pos = pos[new_kicker][kicker_unit]` straight from the formation template. That's F3 only because `_template()` happens to place the Poacher there; if the Poacher has been sent off, the kickoff happens from wherever the substitute's template hex is. Demonstrated:

```
A's Poacher sent off, A kicks off the 2nd half:
  halftime_reset -> ball {'side':'A','unit':'PM','hex':'G4'}   <-- not F3
  goal_restart   -> ball {'side':'A','unit':'PM','hex':'F3'}   <-- correct
```

Given send-offs occur in 59% of matches (§5), this fires reasonably often. Consequences: no center-circle clearance applies, the kickoff-release Pass isn't taken "straight from F3" as §8 requires, and the ball is spotted in the kicking side's own half.

### 2.12 `halftime_reset()` silently wipes Full Press debt; `goal_restart()` doesn't
`sim.py:628` — `s['debt'] = {'A':0,'B':0}`. Nothing in §6, §6.5 or §15 says a Full Press debt clears at halftime. Either it's a deliberate rule that isn't written down, or an oversight; either way the two restart paths disagree with each other.

### 2.13 Command-card Cycling and the Counter card have no engine support
§6's Cycling (`:189`) — described as "the escape from the one true deadlock" — has no function. `cycle_tactic()` exists for Tactic Cards only (`:586`). The Counter card's two options (force a Tackle Challenge / add 1 Defense die, §10) have no implementation; `sim.py:190-193` explicitly says "don't 'play' Counter as a normal turn card" but offers no alternative path. Neither is listed in the docstring's "WHAT THIS ENGINE DOES NOT DO" section (`:139-144`), which currently names only Tactic-card legality, Signatures, Set Pieces and move validation. That list should also name: Cycling, Counter, Full Press's second Act and its debt, Keeper's Call's bonus draw, the box-defender die, and the escape-hex rule (implemented but advisory — see 3.11).

---

## 3. Broken-rule / edge-case instances

Ordered roughly by how likely they are to actually bite.

### 3.1 A red-carded unit comes back on the pitch (confirmed, reachable, and it's the rulebook's own worked example)

`apply_discipline()` (`:366-377`) sin-bins a first Yellow via `send_to_sinbin()`, which writes `s['sinbin']['A:WB'] = 2`. A **second** Yellow takes the Red branch (`:367-372`) which pops the unit and appends to `sent_off` — but **never clears the sin-bin entry**. Two of that side's turns later, `sinbin_check()` (`:492-497`) unconditionally does `s['pos'][side][unit] = target` and puts the sent-off unit back on the board.

```
[DISCIPLINE: A-WB YELLOW CARD, Pace -1 for the rest of the match]
[A's WB is sent to the sin-bin from C5 - misses A's next turn]
  sinbin: {'A:WB': 2}
[DISCIPLINE: A-WB 2nd Yellow -> RED, removed from the match]
  sent_off: ['A:WB']   sinbin STILL: {'A:WB': 2}   <-- not cleared
[A's WB returns from the sin-bin at A1]
  WB back on the pitch after a RED? True at A1
```

This is exactly the sequence §12.5's "A mistimed Slide Tackle, two draws deep" worked example describes (Yellow, then Yellow → Red). It also fires on any Foul or lost Tackle drawn against an already-yellowed unit. It self-corrects at halftime (`halftime_reset()` pops `sent_off` units from the fresh formation), so it manifests as a unit playing for up to half a match after being sent off. Given 229 Yellows across 200 matches, this is not rare.

**Fix:** `del s['sinbin'][key]` in the 2nd-Yellow-to-Red branch, and/or guard `sinbin_check()` against `key in s['sent_off']`.

### 3.2 A Goalkeeper-role unit outside its own zone has *zero* legal moves — it can't even stand still

`legal_reach()` filters `reach()` down to hexes in the zone. `reach()` includes the start hex at cost 0, but if the start hex isn't in the zone it gets filtered out too, so the function returns `{}`:

```
GK at F3 (Pace 2), zone ('A3','A4','B3') -> legal_reach = {}
RESULT: 0 legal destinations, including "remain where you are"
```

Not a theoretical state: §5 (`:179`) explicitly creates it — "Your Goalkeeper may not be the kickoff-taker unless it's the only unit you have left; if so, it takes the spot". A Goalkeeper standing on F3 can then never legally move again for the rest of the match. Either the waiver needs a matching "and may return to its zone by any route" clause, or `legal_reach()` needs a fall-back that lets an out-of-zone keeper move *toward* its zone.

### 3.3 The sole-unit Goalkeeper kickoff is an absolute deadlock in the rules

Compounding 3.2. §8 (`:265`) — "the kickoff-taker's **entire activation** ... is a single **Pass to a teammate within Pass Range** — straight from F3, no Move first, and **never a Clearance** to open ground". If the Goalkeeper is the only unit you have left, there is no teammate. There is no legal action, no Clearance escape hatch, and no way to discharge the obligation. §5's reassurance that "Placing at least one teammate within Pass Range of F3 is entirely within your own control at setup" is exactly the assumption that fails here.

A softer, much more reachable version of the same problem: the **Poacher has Pass Range 1**, and the setup rule restricts you to your own half (A–E or G–K), so a Poacher kickoff-taker's only legal targets are **E3 and E4** (or G3/G4). With three outfield units sent off, if your one remaining teammate is the Goalkeeper — confined to A3/A4/B3, and F3→B3 is distance 4 — you again have no legal kickoff. Given the send-off rate measured in §5, a side down to two units is not exotic.

**Suggested fix:** allow a Clearance at kickoff when no teammate is in range (it's still "someone else has to touch it" in spirit — the ball leaves the taker either way), or waive the release obligation outright when it's unsatisfiable.

### 3.4 A sin-binned Goalkeeper plus an own outfield unit in the zone is an undefined Shot

§8 (`:284`): auto-goal iff "the opposing side's Goalkeeper Zone is **empty of any of their own units**"; otherwise "roll your Shot stat (Attack) vs **the goalkeeper's Save stat**". §12 (`:458`) explicitly bars Emergency Goalkeeper from covering a sin-bin: "that rule only ever answers a full send-off, never a temporary sin-bin". And §4 lets a side's own outfield units "stand inside their own zone freely".

So: Goalkeeper sin-binned, a Sweeper standing on B3 → the zone is **not** empty (no auto-goal) but there is **no goalkeeper** (no Save stat). The rulebook has no answer. The engine has no answer either — `save_stat()` raises:

```
sim.save_stat(s,'B','SW') -> KeyError: 'save'
```

`driver.py:505-512` papers over it with `if guard is None: auto-goal`, which resolves the case *against* the rulebook's own text (the zone is occupied, so §8 says roll). Whatever the intended answer is — flat Save 1 like a deputy, Save 0, auto-goal anyway — it needs saying, because parking a defender in the box while your keeper serves a sin-bin is an obvious and attractive play.

### 3.5 Warning and Advantage / Play On are undefined on a lost Tackle
Both Discipline cards are written assuming a stoppage:
- **Warning** (`:439`) — "Nothing happens. **Play on from a free kick at the spot of the foul.**"
- **Advantage / Play On** (`:440`) — "The fouled side may **ignore the stoppage** and continue with the ball, in addition to **the free kick** being available next stoppage."

But §8 (`:287`) is emphatic that a lost Tackle Challenge is *not* a Foul: "play doesn't stop and there's no Free Kick". Six of the twelve Discipline cards are Clean Challenge, and three of the remaining six (Warning ×2, Advantage ×1) reference a free kick that by construction doesn't exist on the trigger that produces 90%+ of all draws. In practice both become "nothing happens", which makes the effective lost-Tackle deck 9/12 no-effect, 2/12 Yellow, 1/12 Red — worth stating plainly rather than leaving to be worked out.

### 3.6 The Free Kick itself is under-specified
§13 (`:499-500`) says where the ball goes and who falls back, and nothing else. Unanswered: whose turn is it (the Foul is played as a reaction on the opponent's turn)? Does taking it consume an activation or the turn's Act? Is the taker exempt from Command Card restrictions the way a kickoff-taker is? Can the direct Shot be taken immediately, or on the next turn? The one Set Piece in the game is three sentences long.

Also `:500` — "The Goalkeeper is exempt: it may stay in its own **goal box**". Should be Goalkeeper Zone; a Goalkeeper on B3 that's adjacent to the foul spot currently has to fall back, and has nowhere legal to fall back *to*.

### 3.7 `goal_restart()` desyncs ball and unit when the deputy is the only kicker
When a side's Goalkeeper has been sent off and the Emergency deputy is the only remaining outfield unit, `goal_restart()` picks it as kicker (the `alt` guard at `:645` finds nothing), places it on F3, then `_reapply_emergency_gk()` at `:649` moves it straight back into the goal zone — while `:650` records the ball on F3:

```
ball says: {'side':'A','unit':'SW','hex':'F3'}   SW actually stands at: A3   DESYNC
```

### 3.8 The Tactic Deck has no exhaustion rule
§6 (`:187`) says "reshuffle the discard pile when the draw pile runs out" for Command Cards. §11 says nothing equivalent for the 26-card Tactic Deck, and §7 step 6 tops the Tactic hand up every turn. Over 24 turns a side, plus Keeper's Call bonus draws and Tactic cycling, 26 cards is genuinely reachable. The engine silently reshuffles (`_draw_with_reshuffle` is shared by `draw_cmd` and `draw_tac`, `:300-320`), so it's undocumented engine behaviour rather than a crash — but the printed rules leave a table with no instruction.

### 3.9 The escape-hex rule is one-directional, so a side can box in its own carrier
§9 (`:377`) forbids only *the defending side* from closing the last gap around *the opposing* ball-carrier. Nothing stops your own units from surrounding your own carrier, and §9 explicitly blesses the self-inflicted variant ("a ball-carrier that dribbles itself into a fully boxed hex has no one to blame but its own move"). The resulting position — carrier can't Move, and can only Pass if a teammate happens to sit on a straight line within Pass Range — has no resolution rule. Self-harm, so low priority, but the rulebook currently declares a dead position legal rather than resolving it.

Board edges are handled correctly, for what it's worth: the tightest hexes (A1, A6, K1, K6) have only two neighbours, and the rule still guarantees one stays open.

### 3.10 Latent, not currently reachable: pre-generated pool exhaustion
`roll()` (`:336-337`) slices `pool[p:p+n]` with no bounds check, so past 400 dice it **silently returns fewer dice than asked for** — a weaker roll, no error:

```
asked for 5 dice at pointer 398 -> got 2 dice: [6, 2]  (silently short)
draw_disc past 600 -> IndexError
```

Measured peak over 60 matches: **131/400 dice and 13/600 Discipline draws**. So it's comfortably provisioned today and I'd not prioritise it — but the silent-shortening failure mode is nastier than a crash, and a `gen_random()` extension guard (like the one `_draw_with_reshuffle` already has for cards) would close it.

### 3.11 `would_seal_last_gap()` exists but is never called
`sim.py:817-827` implements the escape-hex check correctly. `driver.py` never calls it (nor `escape_hexes_free`). So the escape-hex rule — described in §9 as targeting "a specific failure mode found in playtesting" — has never been exercised in any batch.

### 3.12 Driver: turn order ignores the coin flip
`driver.py:658-659` — `mover = 'A' if t % 2 == 0 else 'B'`. Team B always moves first, regardless of `s['kicker']`. §5 rule 1: "The side with kickoff moves first." Measured: **104 of 200 matches** had A winning the kickoff while B moved first, meaning A began holding the ball on F3 and B got a free turn before the kickoff pass. Same at halftime. No net scoring bias resulted (A 187 goals, B 192 across N=200), but it's a rule the harness doesn't obey.

### 3.13 Driver: a Foul turns the ball loose instead of awarding a Free Kick
`driver.py:334-337`, `:457-460`, `:565-567` all set `s['ball'] = {'side':None,...}` after a successful Foul. §13 gives the ball to the **fouled** side at the foul spot. As modelled, being fouled is a 50/50 scramble rather than a restart in your favour — which materially understates the cost of the Foul card and overstates its value.

---

## 4. Stalemate analysis

**Short answer: there is no hard structural stalemate in normal play, but there is a well-defined stalling incentive that the rules currently do nothing about, and the rulebook already knows it (§16) without ever saying so.**

### 4.1 Structural: stalling is cheap and breaking a stall is expensive

Three rules combine:

1. **Cycling is unconditionally legal, every turn, forever.** §6 (`:189`) — "This is always legal, not just when your hand is unplayable." The stated cost is "you get none of your team's usual activation that turn, so cycling repeatedly just hands your opponent a free run of the pitch." That's only a cost if the opponent can convert a free run into a goal.
2. **A ball-carrier can stand still indefinitely without consequence.** §9 (`:375`) — "The trigger is movement, not proximity. A ball-carrier that's already standing in an opposing Zone of Control ... doesn't retrigger anything by simply staying put." And §7 step 4 makes the Act optional. So a leading side can hold the ball in its own third and simply never move it.
3. **There is no clock pressure of any kind** — no shot clock, no possession limit, no offside, no out-of-bounds, no penalty for a turn in which nothing happens, and no away-goals/tiebreak asymmetry. §15 makes a draw a perfectly good outcome for the side that's level.

And breaking a stall is *actively punished*. Measured over N=200:

- **Tackle win rate: 25.0%** (418 won / 1,672 attempted).
- Every lost Tackle costs the tackler **1 Flair** and **one Discipline draw** (2/12 Yellow, 1/12 Red).
- Expected cost of winning the ball back by tackling: ~4 attempts, ~3 losses → **~0.5 Yellows and ~0.25 Reds per ball won**.

So a side that needs a goal must, on average, accept a **1-in-4 chance of a red card for each time it wins the ball back by tackling** — while the side that's happy with the current scoreline can decline to engage at zero cost. That's the wrong way round: the pressure mechanic taxes the presser, not the staller. §16 lists "A card that directly targets the stalling problem ... something that rewards patience for the **trailing** side specifically" as a future idea, which suggests the design intuition is already there.

A secondary vector: **the kickoff obligation plus Cycling is undefined.** §8 makes the kickoff-taker's whole activation a mandatory Pass, but §6's Cycling activates nobody. Nothing says the obligation carries forward, so a kicking side can in principle cycle indefinitely while sitting on the ball at F3 — and the opponent has just been forced to clear the seven-hex exclusion zone, so it takes them a turn or two to even reach the carrier.

### 4.2 Structural: the genuine hard deadlocks

These are true "no legal action" states rather than stalling:

- **3.2 / 3.3** — a side reduced to its Goalkeeper alone at a kickoff. No legal Pass (no teammate), no Clearance (barred at kickoff), and once on F3 the keeper can never legally move again. Absolute.
- **3.3 variant** — a Poacher kickoff-taker (Pass Range 1) with no teammate placeable on E3/E4.
- **3.9** — a self-boxed ball-carrier with no teammate on a straight line within Pass Range.

All three require a heavily depleted squad, which — given a 0.825 send-off rate per match (§5) — is not as remote as it sounds.

### 4.3 Empirical

The self-play driver is a maximally forward-pushing player: it always advances the carrier toward goal and never elects to stall. So it **cannot demonstrate deliberate stalling** — what it can do is put a floor under natural scoring. Over N=200:

| | value |
|---|---|
| **0–0 finishes** | **40 / 200 = 20.0%** |
| All drawn matches | 68 / 200 = 34.0% |
| Matches where at least one side never scored | **130 / 200 = 65.0%** |
| Shots per match (both sides) | 3.82 → **1.91 per side per 24 turns** |
| ≈ one shot every | **12.5 turns per side** |
| Matches with zero shots | 0 |
| Turns where the driver found no advancing move at all | **0 / 2,880** (N=60 instrumented) |

So the engine never *jams* — the driver always found something legal to do across ~15,800 simulated turns, and `check_no_overlap()` never fired. But a fifth of matches finish goalless and two-thirds contain a side that never scored once in 24 turns, with a *maximally* aggressive player on both sides. Against a player who is actively trying to kill the game, the 0–0 rate would be materially higher.

One more empirical note on repetition: over 60 matches the same hex, **F4, was the site of 216 Dribble Challenges (3.6 per match)** — because both sides use the same default formation, and the shortest path forward from the kickoff-release receiver runs through it every single time. The next-most-contested hexes are I3 (91) and C3 (75). Play funnels through a startlingly small number of squares. That's partly the driver's fixed formation and greedy move heuristic rather than a rules property — but it's worth knowing that the board's *effective* width in practice is far narrower than 11 columns.

### 4.4 What would fix it

Cheapest first: make an unproductive turn cost something. Options that fit the existing economy — a Flair penalty for a turn in which no unit moves toward the opponent's net; forcing the trailing side's Cycling to be free but the leading side's to cost a card; or the "Killer Pass"-style card §16 already imagines. Also worth considering: reduce the Discipline exposure on a *standard* lost Tackle (see §6.2), since that's what currently makes pressing unaffordable.

---

## 5. Playthrough results

All runs from inside `playtest-ai/` with the current canonical engine.

### 5.1 Batch data

| | N=20 | N=50 | **N=200** |
|---|---|---|---|
| Goals / match | 2.40 | 1.66 | **1.895** |
| Goals distribution | 0:3 1:2 2:7 3:3 4:2 5:3 | 0:13 1:16 2:8 3:7 4:2 5:2 6:2 | 0:40 1:55 2:44 3:29 4:17 5:11 6:3 8:1 |
| Scoreless matches | 3/20 = 15% | 13/50 = 26% | **40/200 = 20.0%** |
| Shots / match | 4.20 | 3.48 | **3.82** |
| Shot conversion | 57.1% | 47.7% | **49.6%** |
| Tackles / match (win rate) | 9.50 (29.5%) | 8.08 (25.2%) | **8.36 (25.0%)** |
| Dribble Challenges / match (win rate) | 12.2 (57.8%) | 10.6 (53.9%) | **10.74 (55.4%)** |
| Breakaway share of shots | 64.3% | 66.1% | **67.8%** |
| Breakaway share of goals | 70.8% | 69.9% | **71.5%** |
| Discipline draws / match | 7.55 | 7.26 | **7.40** |
| Yellow cards / match | 1.15 | 1.16 | **1.145** |
| Red cards / match | 0.55 | 0.70 | **0.835** |
| Send-offs / match (authoritative) | 0.55 | 0.70 | **0.825** |
| Sin-bin trips / match | 1.20 | 1.16 | **1.16** |
| Automatic goals (whole batch) | 1 | 1 | 14 |

**Send-off distribution (N=200):** 0 send-offs in 82 matches, 1 in 81, 2 in 28, 3 in 8, **4 in 1**. So **59% of matches see at least one player sent off**, and 18.5% see two or more.

**Shots and goals by position (N=200):**

| | Shots | Goals | Conversion | Share of shots |
|---|---|---|---|---|
| Playmaker | 572 | 286 | 50.0% | **74.9%** |
| Poacher | 96 | 58 | 60.4% | 12.6% |
| Sweeper | 90 | 32 | 35.6% | 11.8% |
| Wingback | 6 | 3 | 50.0% | **0.8%** |

**Tactic Card usage (N=200, plays per match, both sides):** Nutmeg 0.71, Step-Over 0.64, Press 0.59, Jockey 0.55, Curl Shot 0.52, Slide Tackle 0.50, Composure 0.44, Foul 0.40, Last-Ditch Block 0.39, Long Ball 0.18, Through Ball 0.09, Backheel 0.04, One-Two 0.02. Total ≈ **4.95 Tactic Card plays per match across both sides** — about 2.5 per side across 24 turns.

The three rare cards (One-Two, Backheel, Through Ball) are exactly the ones the driver docstring flags as narrowly-triggered, so I'd read their low counts as a driver limitation rather than a card-design finding, as instructed. I found no independent reason to think otherwise: One-Two only fires when it strictly beats the already-computed best route, Backheel only when the route is fully stuck, and Through Ball only when a pass is contested at all — and the driver passes very rarely (see 5.3).

### 5.2 A methodological finding about the batch sizes themselves

Goals per match has **SD 1.57** (N=200). That gives:

| Batch size | Standard error | 95% CI on goals/match |
|---|---|---|
| N=20 | ±0.351 | **±0.688** |
| N=40 | ±0.248 | ±0.486 |
| N=50 | ±0.222 | **±0.435** |

My own N=20 and N=50 runs of the **identical ruleset** returned 2.40 and 1.66 goals/match — a swing of 0.74, entirely noise.

This has a direct consequence for the playtest log. `2026-09-08-batch-50-final-roster-all-tactic-cards.md` headlines "goals/match **rose again**" on a move from 1.94 to 2.02 — a difference of 0.08, which is **0.36 standard errors**. That is not a measurement. Neither is "scoreless matches 22% → 20%" (1 match in 50), nor "cards/match 1.88 → 1.70". The same report's own caveat about confounded variables is right and should be extended: at N=50 this simulator cannot resolve anything smaller than about **±0.44 goals/match**. Tuning decisions taken on sub-0.4 differences at N=50 have been reading noise. Recommend N≥200 for any goals/match comparison, or a paired/common-random-numbers design.

For what it's worth, the prior N=50 report's headline numbers *do* reproduce within noise against my N=200 (2.02 vs 1.895 goals, 3.74 vs 3.82 shots, 20% vs 20% scoreless), so it isn't wrong — it's just over-precise.

### 5.3 One match, read qualitatively (N=1, full log)

48 turns produced **33 dice-rolling events and 2 shots**, final score B 1–0 A. What that reads like:

**What works.** The kickoff sequence is genuinely football-shaped: the Poacher releases to the Playmaker, the Playmaker carries, gets challenged at F4, beats his man, and drives on. The "beat your man, then shoot" chain (Dribble Challenge won → Through on Goal → Shot) plays exactly like a breakaway, and the one goal in the match came off it — line 29-30: Playmaker wins the challenge at I3, takes the shot at +1 die, 2 successes to 1 stop. That is the game's best moment and it works.

Two other nice touches actually landed: a Goalkeeper playing **Long Ball from B3 out to the Playmaker at H3** reads like a keeper launching a counter; and a Yellow-carded Poacher going off, missing a turn, and returning at G1 gave the sin-bin real texture.

**What doesn't.** Three things stood out as mechanically off:

1. **Repetition.** Team B's Sweeper attempted a Dribble Challenge *through the same Zone of Control at C1* on **three consecutive activations** and lost all three, ending the half stuck in the same spot. Because a lost Dribble Challenge spills the ball one hex back and the carrier can just walk onto it again next turn, the game has a natural attractor: attempt, fail, re-collect, attempt. It reads like a stuck record, not like football.

2. **Nobody passes.** In an entire 48-turn match the ball was passed **twice** — the mandatory kickoff release, and one Long Ball. Every other transfer of possession was a tackle or a spilled dribble. Football is a passing game; Hexside as currently played is a dribbling game with occasional tackles. Some of that is the driver (it only passes at kickoff, after a won tackle, or when Long Ball/One-Two/Backheel strictly beat a dribble) — but the underlying incentive is real: Control is the same stat for dribbling *and* for surviving a contested pass, dribbling doesn't spend your Act, and a won dribble earns +1 shot die. Passing gets you nothing comparable.

3. **The discipline-to-football ratio is inverted.** That match had **6 Discipline draws and 2 shots**. More cards were drawn than shots taken. Across the full N=200: 7.4 Discipline draws vs 3.8 shots per match — the referee is twice as busy as the strikers.

---

## 6. Playability assessment

### 6.1 Does it read as a finished ruleset or a patchwork?

Honestly: **a very well-written patchwork.** The prose quality is unusually high — §4's explanation of the interlocking-hex straight lines and §9's justification of "first challenge per activation" are genuinely good rules writing, and the worked examples are the right idea. But the seams show, and they show in a specific, diagnosable way: **the rulebook is written as a running commentary on its own tuning history rather than as a rulebook.**

Count the sentences in §14 alone that exist only to explain what a number *used to be*: "Shot has now been raised twice", "The first pass put it +1 across every outfield position", "A second pass went +1 again", "Control moved for three of the four outfield positions in the same round", "an earlier draft had flattened everyone to Pace 3", "The Sweeper and Wingback had their entire stat lines swapped". §11 has two cards whose text includes an explanation of the card they *replaced* (Composure/Advantage Play, Jockey/Offside Trap). §6 has a paragraph about the retired Target Player card. §16's list of future ideas leaks backward into §11's card text.

None of that is wrong, and for a prototype in active tuning it's arguably valuable — but it means a first-time reader has to sort load-bearing rules from changelog, and the changelog is where nearly every inconsistency in section 1 of this report lives (1.1, 1.7, 1.10, 1.16 are all stale-rationale artefacts). **The single highest-leverage structural change would be to move all of that into a separate "Design Notes / Changelog" appendix**, leaving §14 as a stat table and one paragraph of positional identity. It would cut the rulebook's length by a meaningful fraction and remove an entire class of future inconsistency.

### 6.2 Complexity for a first-time player

Too high for what the game currently delivers, and unevenly distributed.

The **core loop is excellent**: play a card, see which of your five units it lights up, move them, take one action. That's teachable in three minutes and it's the good idea at the centre of the design. §17's advice ("Playtest the core loop first — Command Card → activate → move → one action — before worrying about Tactic Cards, Fouls, or Set Pieces") is exactly right.

But around that loop sits a lot of bookkeeping a new player has to hold:
- **Four distinct areas at each goal end** — goal box (2 hexes), Goalkeeper Zone (3), Net (3, off-board), plus the goal box's role as the Save-rebound target. §4 spends four paragraphs distinguishing them and the glossary needs three entries. A player will get these wrong.
- **Two range stats sharing one column** on the player card, written "2 / 2", with different meanings and different measuring targets (Pass Range measures to a hex, Shot Range measures to a *virtual off-board* hex one further out).
- **Four different sources of Discipline** (standard Tackle ×1, Slide Tackle ×2, Foul ×1-redrawing) with different Clean Challenge handling.
- **Six-step Resolution Sequence** with four separate card windows, and 4 of 13 Tactic Cards timed outside their obvious slot (Jockey earlier than step 1; Last-Ditch Block at step 5; Press and Foul at step 2).
- **The seam-column rule.** §4's paragraph on D and H is the single hardest thing in the book to hold in your head, and it exists to close a gap that only affects a Center-lane unit parked on one of two columns. I'd genuinely question whether it earns its complexity cost — the Zone Pair fallback already prevents dead cards.

Against that: **the "ball-carrier is always activatable" rule (§6) is the best single piece of design in the book.** It removes a whole category of frustrating dead turns, it's thematically obvious, and it makes the kickoff exception unnecessary. Similarly the Zone Pair fallback. Both are examples of complexity *removed*, and there should be more of them.

### 6.3 Is the dice/card economy balanced?

**Flair is not a real currency.** I instrumented 60 matches:

```
dice rolled            8,285  (138/match)
Flair symbols rolled   2,709  (45.1/match, both sides)
Flair LOST to the cap  1,451  = 53.6% of all Flair earned
rolls ending with the roller's bank at 5   60.1%
```

**Over half of all Flair earned is thrown away against the cap-5 bank, and 60% of rolls end with the roller already full.** Meanwhile total Tactic Card play is ~2.5 per side per match at an average cost of ~1.2 Flair. So the printed Flair costs (0/1/2) are essentially decorative: what limits Tactic Cards is hand size (3) and trigger conditions, not affordability. A player who understands this will simply play every affordable card the moment it's eligible — which is exactly what the driver does, and which is why the driver's "deterministic-if-affordable" simplification turns out not to be much of a simplification.

If Flair is meant to be a resource you husband, either the cap needs to drop sharply (2-3), or Flair needs to come off fewer die faces (currently 2 of 6 on *both* die types, on *both* sides of *every* roll), or costs need to be much higher. As it stands the cap is doing all the work and the economy is inert.

**Discipline is badly over-tuned.** This is the clearest balance outlier in the game:

- **1.98 cards per match; 0.825 send-offs per match; 59% of matches see a red.**
- For a **5-a-side** game where each side has four outfield players, losing one is a 25% squad reduction. Losing two happens in 18.5% of matches.
- Real 5-a-side sees a red card in maybe one match in twenty. This is roughly **17× that rate.**

The mechanism is clear and it's not the Discipline deck's ratios — it's the *trigger frequency*. Discipline is drawn on **every** lost Tackle Challenge, and 75% of tackles are lost (8.36 attempted, 25% won → ~6.3 lost per match), plus Slide Tackle doubles the draw and Foul redraws past Clean Challenge (making a Foul 1-in-6 Red rather than 1-in-12). 7.4 draws per match at 1/12 Red is 0.62 expected reds before the second-Yellow-to-Red path is counted.

§8 rationalises this well ("a mistimed challenge carries real physical risk"), and 6-in-12 Clean Challenge is a sensible dampener — it just isn't nearly enough at this volume. Options, roughly in order of how surgical they are:
1. Draw Discipline only on a lost **Slide Tackle** (a committed challenge), not on every standing tackle. Cleanest fix, and it's already the thematic distinction §11 draws.
2. Or raise Clean Challenge to 8-of-14 and drop Red to 1-in-14.
3. Or make Red only reachable via a second Yellow, never a direct draw.

Note also that fixing the tackle win rate would compound: at 25%, tackles are both ineffective *and* dangerous, which is why the driver's sides mostly just don't defend.

**Shot conversion is very high, shot volume is very low.** 49.6% conversion on 3.82 shots per match. Real 5-a-side has far more shots at far lower conversion. The current shape means each match turns on roughly four coin-flips, which is high variance dressed as low scoring — the 0-to-8 goal spread at N=200 with a mean of 1.9 shows it. And 67.8% of all shots carry the Through on Goal +1 die, meaning the "special reward for beating your man" is in fact the **default** way a shot happens. That's not necessarily wrong, but it's not what §8's rationale describes; the bonus is currently a baseline, and a shot *without* it is the exception. If the intent is that a breakaway feels special, either more shots need to arrive by other routes (passing — see 6.4) or the bonus should be rarer.

### 6.4 Pacing, and the one thing I'd change about the game itself

The pacing problem and the passing problem are the same problem.

Right now the dominant strategy is: *get the ball to your Playmaker, dribble him up the pitch, shoot.* The N=200 data is unambiguous — the Playmaker takes **74.9% of all shots** and scores **75.5% of all goals**, while the Wingback takes 6 shots in 200 matches. §14's own rationale identifies why ("Control, not Shot, turns out to be what actually decides who gets to shoot in the first place") and then *leans into it* by raising the Playmaker's Control to a roster-best 4. The result is a five-player game in which one player does three-quarters of the attacking.

The Poacher is the sharpest symptom. It has the best Shot (5), the best Shot Range (4), the best Pace (4), and a finishing Signature — and it takes **12.6% of shots**. Its Pass Range 1 means it can barely be *reached*, its Control 3 means it loses the ball on the way up, and there is no mechanic that rewards playing a ball into it. A striker that can't be passed to is a striker that doesn't play.

So the change I'd argue for, if you only make one: **make passing competitive with dribbling.** Concretely — a completed Pass that moves the ball toward the opponent's net could grant the *receiver* something analogous to Through on Goal (+1 to its next Shot this activation), or simply not be contested by Zones of Control the line merely passes over (currently a pass is *more* dangerous than a dribble, because it's contested by every ZoC along the whole line while a dribble is contested only once per activation). That second point is worth restating plainly: **§9 gives a dribbler free passage through every subsequent Zone of Control once he wins one, while §8 makes a passer contest every Zone of Control on the line.** The asymmetry is large, deliberate-looking, and pointed the wrong way for a football game.

That change would also help the stalling problem (§4), because it gives a trailing side a way to progress that doesn't require winning 55%-odds dribble contests one at a time, and it would spread shots across the roster.

---

## 7. Prioritised punch-list

**P0 — correctness bugs that change outcomes**

1. **Clear the sin-bin entry when a 2nd Yellow becomes a Red** (`sim.py:366-372`). A sent-off unit currently returns to the pitch two turns later. This is the rulebook's own §12.5 worked example. (3.1)
2. **Global `§N → §N+1` pass over `engine/sim.py` and `engine/board.py`** — 67 references, all uniformly one section low. Mechanical, zero risk, and it's the difference between the codebase pointing at the rules and pointing at the wrong rules. (2.1)
3. **Fix `hexside-cards.html:103`** — the printed Counter card says "see Rulebook §9"; Reactions is §10. It's on a physical card. (2.2)
4. **Put the sin-bin on the printed Yellow Card** (`hexside-cards.html:179`) **and into §12.5's two worked examples** (`:469`, `:482`). The rule currently exists only in §12's prose; two of the three places a player looks contradict it. (2.3, 1.7)
5. **`halftime_reset()` must force the kickoff-taker onto F3** (`sim.py:619-625`), the way `goal_restart()` does. Fires whenever the kicking side's Poacher has been sent off — i.e. often. (2.11)
6. **Define the sin-binned-keeper Shot.** Goalkeeper in the bin + an own outfield unit in the zone = not an auto-goal, but no Save stat exists. Rules undefined, `save_stat()` raises KeyError, and the driver silently resolves it as a goal. (3.4, 2.6-adjacent)

**P1 — rulebook errors a reader will actually hit**

7. §8's "**(1–3)**" dice range → (0–5). (1.1)
8. §11.5's "Through Ball vs. a Zone of Control" example is a **Backheel** example. Retitle it, and write the Through Ball example that's missing. (1.2)
9. "**dice per §8–8**" (`:241`) → §8. (1.3)
10. "**the two ways in §12**" (`:499`) → there is one way. (1.4)
11. §16's "**stalling problem noted elsewhere in this draft**" (`:544`) — either write that section or drop the reference. (1.5)
12. Fix the **§6.5 Full Press table** (row N+1 says 3, prose and engine both give 4) — and re-check §6's Cycling rationale, which depends on the hand reaching 3. (1.10)
13. Soften §7's "**Through Ball removes the need to roll at all**" and the Playmaker's Vision text to "if it is the only contesting Zone of Control". (1.6)
14. Restore the clauses dropped from the printed **One-Two**, **Long Ball** and **Advantage/Play On** cards. (2.4)
15. Say what **Warning** and **Advantage/Play On** do when drawn from a lost Tackle, where there is no stoppage and no free kick. (3.5)

**P2 — balance, in the order I'd tune them**

16. **Cut the Discipline rate.** 0.825 send-offs and 1.98 cards per match in a 5-a-side game is the single most out-of-band number in the project. Preferred fix: draw Discipline only on a lost **Slide Tackle**, not on every standing tackle. (6.3)
17. **Make passing competitive with dribbling.** Currently a dribbler gets free passage past every ZoC after the first, while a passer is contested by every ZoC on the line — plus the dribbler gets +1 shot die. Result: the Playmaker takes 75% of shots and the Poacher, the best finisher on the roster, takes 12.6%. (6.4)
18. **Fix the Flair economy.** 53.6% of all Flair earned is lost to the cap; 60% of rolls end with a full bank. Either drop the cap to 2-3, or cut Flair from 2 die faces to 1. As it stands the printed costs don't constrain anything. (6.3)
19. **Give the trailing side a reason to press and the leading side a reason not to stall.** No clock pressure of any kind exists, and the tackle economics punish exactly the side that needs the ball. (4.1, 4.4)

**P3 — engine completeness (needed before the next tuning batch means anything)**

20. **Implement Full Press's debt** — nothing has ever set `s['debt']`, so 3 of 35 Command Cards have been free supercards in every batch to date. Any Command-deck balance conclusion from prior batches is compromised. (2.7)
21. **Implement the box-defender's +1 Defense die** (§8) — a fully specified defensive mechanic that has never been simulated, in a game running ~50% shot conversion. (2.6)
22. **Make `legal_reach()` filter paths, not just destinations**, for the Goalkeeper Zone. (2.10)
23. **Handle the out-of-zone goalkeeper** — `legal_reach()` currently returns `{}`, so the unit can't even stand still. And resolve §5's sole-unit-Goalkeeper kickoff, which is an unconditional deadlock in the rules as written. (3.2, 3.3)
24. **Driver: obey the coin flip for turn order** (`driver.py:659`) and **award a Free Kick to the fouled side** rather than turning the ball loose (`:334`, `:457`, `:565`). (3.12, 3.13)
25. **Update `sim.py`'s "WHAT THIS ENGINE DOES NOT DO"** to include Cycling, Counter, Full Press's second Act and debt, Keeper's Call's bonus draw, the box-defender die, and the escape-hex rule being advisory. And fix `engine/README.md`'s claim that a Free Kick restart is implemented — there's no free-kick code at all. (2.13, 2.9)

**P4 — process**

26. **Stop drawing conclusions from N=50 batches.** SD is 1.57 goals/match, so N=50 gives a 95% CI of **±0.435**. The 1.94 → 2.02 "rise" in the most recent batch report is 0.36 SE. Use N≥200, or common random numbers for paired comparisons. (5.2)
27. Add the missing **Dice Reference card, Zone Map card, Backs sheet and Token Sheet** to `hexside-cards.html` — §3 and §17 both promise them, and §17's "11 pages" doesn't match the 10 the file produces. (2.5)
28. Consider moving §14's and §11's tuning-history prose into a **separate Design Notes appendix**. Nearly every rulebook inconsistency found here lives in that changelog layer. (6.1)
