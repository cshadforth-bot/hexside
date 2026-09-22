"""Hexside match-state engine — current canonical ruleset (see /source/hexside-rulebook.html
for the full rules this implements). This is a state-tracking and dice-resolution library,
not an AI: it computes legal options and resolves contested rolls correctly, but a human
(or an LLM) still has to decide what to actually play each turn.

QUICK START
-----------
    import sim, board
    sim.gen_random()          # pre-generates one match's worth of shuffled decks & dice
    s = sim.new_state()       # coin-flip kickoff, kickoff-placement draft, empty log

    # Each turn:
    sim.sinbin_check(s, 'A')                 # returns any sin-binned unit whose turn-count has elapsed (§12) - call first
    sim.card_options(s, 'A', 'Third-2')      # -> (list of unit codes this card can activate, fallback: bool)
    sim.legal_reach(s, 'A', 'PO')            # -> {hex: (pace_cost, path)} every hex PO can legally end its move on (Goalkeeper Zone rules included)
    sim.enemy_zoc(s, 'A')                    # -> set of hexes inside the OPPONENT's Zone of Control (threatens A's ball-carrier)

    # Move a unit by just editing s['pos'][side][unit] directly, e.g.:
    s['pos']['A']['PO'] = 'H3'
    sim.check_no_overlap(s)                  # raises if that move created a hex collision

    # Contested rolls:
    sim.contest(s, 'A', 2, 'B', 3, label='Dribble Challenge: ...')   # generic attack-dice vs defense-dice roll
    sim.tackle(s, 'A', 'PO', 'B', sim.ROSTER['PO']['tackle'], sim.ROSTER['SW']['control'], label='...')
    sim.strong_tackle(s, ...)                # +1 die, draws Discipline twice on a loss (needs 'StrongTackle' in hand_tac)

    # A Shot's Defense stat is a Save — use sim.save_stat(s, side, unit), not
    # sim.ROSTER[unit]['save'] directly, since an Emergency Goalkeeper (see below) uses a
    # flat Save 1 instead of a real Goalkeeper's Save 3. Its own Attack dice should go
    # through sim.shot_dice(unit, breakaway=...) too, for the Through on Goal bonus below.
    sim.contest(s, 'A', sim.shot_dice('PO', breakaway=True), 'B', sim.save_stat(s, 'B', 'GK'), label='Shot: ...')

    # End of turn:
    sim.replenish(s, 'A')                    # draw back up to 5 Command Cards (respecting Full Press debt), top up Tactic hand to 3
    sim.save(s)                              # persist state.json

    # Restarts:
    sim.goal_restart(s, conceding_side)      # after a goal
    sim.halftime_reset(s)                    # at the midpoint (turn 12 of 24, or half the agreed length)

STATE SHAPE (the `s` dict)
---------------------------
    pos: {'A': {'GK':'A3', 'SW':'C2', ...}, 'B': {...}}   -- unit -> hex; a unit missing from
                                                              here has been sent off (Red/2nd Yellow)
    ball: {'side': 'A'|'B'|None, 'unit': code|None, 'hex': 'F3'}   -- side/unit are None when the ball is loose
    score, flair, yellow, sent_off, pace_mod, debt, hand_cmd, hand_tac: as named
    a_defends_low: True if Team A currently defends the A3/A4 end
    log: list of human-readable strings describing what happened, in order

A NOTE ON DIRECTION (a real mistake made during development — check this every turn):
    Whichever end a side DEFENDS is named by `a_defends_low` (A defends A3/A4 if True, K3/K4
    if False; B always defends the other end). A side ATTACKS the opposite end from the one
    it defends — i.e. it should be moving the ball AWAY from its own goal box, not toward it.
    Before pushing a ball-carrier "forward," check board.shot_dist(hex, <the end you attack>)
    is shrinking, not board.shot_dist(hex, <your own end>).

DISCIPLINE (§12): one single 12-card deck for everything, shuffled and returned to after
every draw (draw_disc never has memory between calls — each is independent at the fixed
12-card odds). Standard Tackle draws once; Strong Tackle draws twice; a Foul (Tactic Card)
uses draw_disc_foul(), which redraws past Clean Challenge until a real card lands.
apply_discipline() automatically calls assign_emergency_gk() the instant a side's actual
Goalkeeper is sent off — see EMERGENCY GOALKEEPER below.

SHOT RANGE (§8, §14): board.shot_dist() measures genuinely to the Net now (§4), not the
goal box — the two used to differ by exactly one hex, which is why every outfield Shot
Range number here is +1 from the roster's original published values. A few short-column
hexes (B, D, F, H, J) that never had a straight line to the box at all now have one to the
Net instead — a real, if narrow, extra shooting angle, not just a wider version of the old
box-based lines. box_dist() is kept in board.py only for reference/comparison.

THROUGH ON GOAL (§8): the mirror image of the box-defender's own +1 Defense die — where
a defender's continued presence in the goal box helps the Save, the defender a shooter
just beat being out of the picture helps the Shot. If the shooting unit itself won the
Dribble Challenge that carried it into this shooting position, earlier in this same
activation, its Shot gets +1 Attack die. Pass breakaway=True to shot_dice(unit) to get
the right dice count; the bonus belongs to that one unit and that one Shot only — pass
to a teammate instead, or win a second/third Dribble Challenge in the same activation
(§9: free passage for the rest of it once the first is won), and no extra die stacks.

EMERGENCY GOALKEEPER (§12): the instant a side's Goalkeeper is sent off, apply_discipline()
calls assign_emergency_gk(s, side) automatically, picking a default deputy (Sweeper
preferred) and placing it in its Goalkeeper Zone (see below). Pass your own `unit` to
assign_emergency_gk() if you want a different pick instead. That deputy keeps its own
stats and Signature for everything else, but any Shot it faces should use
save_stat(s, side, unit) — 1, not the real Goalkeeper's 3 — and it never gains
Shot-Stopper. goal_restart() and halftime_reset() both re-place an already-assigned
deputy into the (possibly just-swapped) zone automatically; you don't need to redo this
yourself after a restart.

GOALKEEPER ZONE (§4/§5/§8/§14), a.k.a. "the goal box" — the two terms name the same
3-hex confinement/exclusion area at each end (B.GK_ZONE — B.GOAL_MOUTH's 2 goal-mouth
hexes plus one bordering seam-column hex, e.g. A3/A4/B3), distinct from the 3-hex Net
(the Shot's actual target, off the pitch entirely). The goalkeeper-role unit
(is_goalkeeper_role() — the real GK, or its Emergency deputy) may never end a move
outside its own zone; every other unit may never enter the OPPONENT's zone, though it
may stand inside its own side's freely. Always move a unit through legal_reach(s, side,
unit) rather than raw reach() so both rules apply automatically. A Shot is only an
automatic goal if gk_zone_occupied(s, opposing_side) is False — note gk_zone_occupied()
itself checks specifically for a goalkeeper-ROLE occupant, not just any of that side's
units:
an outfield teammate parked in its own zone (legal) never counts as covering it, most
importantly while the real Goalkeeper is sin-binned (Emergency Goalkeeper doesn't cover
a sin-bin, by design) — that scenario is still an automatic goal even though the zone
technically isn't empty of the side's own units.

YELLOW CARD SIN-BIN (§12): a first Yellow (not the 2nd-Yellow-to-Red case, which already
removes the unit permanently) now also pulls the carded unit off the pitch immediately
via send_to_sinbin(), on top of the existing permanent Pace −1. It misses its own side's
next turn entirely. Call sinbin_check(s, side) at the very start of each of that side's
turns, before anything else — it ticks the pending sin-bin down and returns the unit
the moment its count reaches 0, at a touchline hex in its own half (or inside its own
Goalkeeper Zone, if it plays that role — a sin-binned keeper is not exempt, and leaves
the zone genuinely empty for that one turn).

COMPOSURE (§11): replaces the retired Advantage Play in the same 26-card Tactic Deck
slot (2 copies, 1 Flair, Attack). play_composure(s, side) discards it and pays the
Flair; the reroll itself (up to 1 die from a Shot just taken — Step-Over's exact shape,
redirected from Dribble Challenges to Shots) is on you to apply, the same way
play_jockey() doesn't compute the reduced reach itself.

JOCKEY (§10, §11): replaces the original Offside Trap card — same deck slot (2 copies),
1 Flair, Defense. Reacts to an opposing unit's Move the instant it's activated (not a
Resolution Sequence window): play_jockey(s, side, unit) discards it and pays the Flair;
then call reach(s, opp_side, opp_unit, extra_pace=-1) to get that unit's actual reduced
reach for this one move. No roll, no Discipline risk, doesn't stop the move outright.

KICKOFF RELEASE (§5, §8): mirrors real football's restriction against a kickoff-taker
touching the ball twice in a row. new_state(), goal_restart(), and halftime_reset() all
set s['kickoff_taker'] = {'side':..., 'unit':...} for whichever unit is placed on F3
with the ball. While that obligation stands, kickoff_release_required(s, side, unit)
returns True for that unit, meaning its ENTIRE activation this turn is a single Pass to
a teammate within Pass Range, straight from F3 — no Move first, no Clearance (unlike an
ordinary Pass), and never a Shot or a Tackle. The engine doesn't block an illegal
Shot/Move/Tackle itself (see WHAT THIS ENGINE DOES NOT DO, below) — check
kickoff_release_required() yourself before resolving anything else for that unit. The
instant that Pass resolves (successfully or not, contested or not), call
release_kickoff(s, side, unit) to discharge the obligation for good — the receiving
unit (or the intercepting defender, if it fails) is then just a normal ball-carrier,
free to Move, Dribble, Pass, or Shoot on its own next activation like any other turn.
A Dribble Challenge or a Shot can never discharge the obligation, and it isn't renewed
even if the ball comes straight back to the original taker afterward.

WHAT THIS ENGINE DOES NOT DO: it doesn't enforce which Tactic Cards are legal to play when,
doesn't implement any of the 5 Signature abilities or Counter itself (no code here forces a
Tackle Challenge, adds a Defense die from a held Counter, or grants any Signature's effect —
a caller has to do all of that), and doesn't validate that a proposed unit move is actually
reachable (call reach() yourself and check before moving). Nor does it implement Set Pieces
at all — despite an earlier version of this note claiming a "plain Free Kick restart"
existed, no Free Kick code has ever been here; a caller that wants §13's behavior places the
ball itself. What it DOES carry, for a caller to actually use: the Base Game's own roster
(ROSTER_BASE, §14, swapped in via sim.ROSTER = sim.ROSTER_BASE), the kickoff-placement
draft (formation(), below — see its own docstring), and Full Press's 2-turn debt field
(s['debt'], consumed automatically by replenish() once a caller sets it — see
playtest-ai/driver.py's play_card() for where that happens). See playtest-ai/driver.py and
driver_base.py for a caller that drives the Advanced and Base Games respectively — both now
implement all 5 Signature abilities (Shot-Stopper, Last Man, Vision, Clinical, Overlap —
Overlap uses §14's "ends in Third 2, not the attacking third" version, not the rulebook's
original text) and Counter's "+1 Defense die" option (maybe_counter_die()) inside their own
turn logic. Counter's other option (discard to force an immediate Tackle Challenge) is
deliberately not modeled by either driver — see maybe_counter_die()'s own docstring for why.
Treat this module as a calculator for "what can activate, and who wins this roll" — the
rulebook itself is still the authority for everything else.
"""
import json, random
import board as B

STATE = 'state.json'
RAND = 'game_random.json'

# §14 BASE GAME ROSTER (2026-09-08): the Base Game is the full ruleset with the 13-card
# Tactic Deck removed entirely (no Tactic hand, no Flair spent on cards; Command Cards,
# dice, Discipline, the sin-bin, GK confinement etc. are all unchanged). Simply dropping
# the deck out of the historical Advanced numbers (see ROSTER_ADVANCED_ARCHIVE below)
# left it measurably flatter - playtesting at N=200 found goals/match falling
# 1.895->1.675, driven almost entirely by dribble win rate falling 55.4%->44.3% once
# Nutmeg/Step-Over are gone to rescue a losing Dribble Challenge. This roster
# compensates with Control +2 for Sweeper/Wingback/Poacher ONLY - Playmaker is left
# unmoved from its historical value since it already carried the roster's highest
# Control, and an earlier flat +1-for-everyone version recovered scoring (goals/match
# 2.005, dribble win rate 56.0%) but made Playmaker's existing shot-share dominance
# worse, not better (70.6%->75.7%). Weighting the bump toward the other three instead
# recovered scoring just as well (goals/match 1.85, dribble win rate 55.1%, both close
# to the pre-retune Advanced numbers) while pulling Playmaker's share down to 62.9% -
# the best result on both fronts across four tested variants. See /playtests/ for the
# full comparison. Real cost, not hidden: Tackle win rate falls further under this
# roster (25.9% with no retune -> 18.8% here) - defenders are more often beaten
# outright. Zone of Control and the escape-hex rule were already doing most of
# defense's real work rather than tackling, so this reads as an acceptable trade, not a
# free one.
#
# UPDATE (2026-09-10): once Counter (§10) was actually implemented in the test drivers -
# previously the Base Game's only remaining reaction, never modeled at all - a fresh
# N=200 batch measured dribble win rate at only 48.4%, well under the ~53-56% this
# roster was tuned to hit. That target was always going to move: it was measured on a
# driver missing Counter, plus three other fixes landed since (a stuck-carrier
# Clearance/Pass bail-out, corrected hex-ranking for kickoff/pass-target choice, and
# Full Press's actual debt + second Act). Tried extending the same fix - more Control
# for Wingback and Poacher too - but both already sit at 5, the hard ceiling for any
# stat in this game (§8: "0-5, see §14"; no roster value has ever gone above it).
# Sweeper still had headroom (4->5) and used it: dribble win rate 51.5%, goals/match
# 2.09, tackle win rate down further to 15.8% (Control also defends a Tackle Challenge,
# so this was always going to cost something on that axis too). Decision: keep the
# Sweeper move and stop there, rather than raise the stat ceiling itself or cut a
# different stat to chase the original number - 48-52% dribble win rate is the correct
# figure for the actual, now-substantially-more-complete ruleset, not a regression from
# a target that predates most of what the engine currently does.
#
# UPDATE (2026-09-10, later same day): separately from Control, raised Sweeper and
# Wingback's Tackle by +1 each (2->3, 3->4) - a genuinely different lever from every
# Control change above. Motivated by a direct question: what are a Poacher's actual odds
# dribbling past a Sweeper? At the numbers above, ~65% (5 Control dice vs 2 Tackle dice)
# - and the reverse, a Sweeper actively Tackling a Poacher, was only ~11%. Tried fixing
# that through Control first (Sweeper/Wingback Control -1, Tackle +1, keeping the "total"
# similar) and separately through a blanket "cap every dice stat at 4" pass - both made
# things measurably worse: the Control cuts pushed MORE of the team's scoring through the
# Playmaker (it never lost anything, so weakening its competition just left it
# relatively stronger), not less. Isolating Tackle alone from Control fixed that:
# Sweeper/Wingback actually winning more Tackle Challenges means THEY end up with the
# ball (and its free follow-up Pass) more often, which is what actually redistributes
# scoring away from the Playmaker - a different mechanism than any Control-based attempt.
# Two independent N=200 batches (pooled N=400) at Tackle-only +1/+1, Control and every
# other stat unchanged: tackle win rate 17.3%->18.5%, Playmaker's goal share 51.6%->47.6%
# (below half for the first time in any variant tested), Sweeper's share 24.2%->30.8%.
# Real cost: goals/match 2.15->1.95 (~0.2 down) - noisier between the two batches
# (2.06 and 1.84) than the win-rate/share numbers were, so treat that ~0.2 as the
# honest estimate, not either single run. A separate PM Shot 4->3 cut was also tried
# alongside this and explicitly NOT kept - it cost another ~0.3 goals/match for almost
# no extra balance benefit once Tackle was isolated on its own.
#
# 2026-09-16: Pace +1 across all five positions (2/3/2/3/4 -> 3/4/3/4/5), adopted as
# canon after a direct n=1000-vs-n=1000 comparison on driver_base.py (same board/roster
# otherwise, run back to back the same day). goals/match 2.667->2.956 (+11%), shots/match
# 5.214->5.888 (+13%), shot conversion flat (51.2%->50.2%), tackle win rate 19.0%->19.4%,
# dribble win rate 52.6%->53.1% - the extra scoring comes from more shots taken, not
# either contest getting easier. Side effect, not the goal: cards/match rose 1.98->2.16
# and sent-off/match 0.75->0.83, since more mobility means more contests means more
# Discipline draws off an already-high red-card rate. Notable rebalancing: Poacher's
# goal share fell 55.6%->49.5% while Wingback (+4.3pp) and Sweeper (+1.9pp) picked up
# share - a flat +1 is a bigger RELATIVE gain for the slower units (2or3->3or4) than for
# Poacher (4->5), so they close ground and contest more even though Poacher is still
# fastest in absolute terms. The relative spread that "Pace is deliberately uneven"
# (rulebook §14) argues for is preserved exactly - only the absolute numbers moved.
ROSTER_BASE = {
    'GK': dict(pace=3, shot=0, control=2, prange=2, srange=None, tackle=2, save=3, sig='shot_stopper'),
    'SW': dict(pace=4, shot=3, control=5, prange=2, srange=2, tackle=3, sig='overlap'),
    'WB': dict(pace=3, shot=3, control=5, prange=3, srange=2, tackle=4, sig='last_man'),
    'PM': dict(pace=4, shot=4, control=4, prange=4, srange=3, tackle=2, sig='vision'),
    'PO': dict(pace=5, shot=5, control=5, prange=1, srange=4, tackle=2, sig='clinical'),
}
# 'sig' names which of §14's 5 Signature abilities (or, since 2026-09-17, one of the
# hexside-character-cards.html alternates) this unit's slot carries - driver code
# dispatches on sim.ROSTER[unit]['sig'] rather than hardcoding the slot code, so a
# swapped-in character roster (same 5 keys, different sig per slot) drives the exact
# same trigger points a standard roster does. 'vision' IS implemented in both
# playtest-ai/driver.py and driver_base.py (see their own vision_used/vision_played
# tracking and the "ignores a defending Zone of Control, once per match" logic) - an
# earlier version of this comment claimed neither driver had it, which was stale by the
# time line 156 above was written. The digital board Artifact's own independent JS
# implementation is the one still missing it, not either Python driver.

# 2026-09-08 decision: the Advanced Game (Base Game + the Tactic Deck) currently plays
# the SAME roster as the Base Game, deliberately - kept unified while the Base Game is
# being validated on its own, rather than tuning two rosters at once. Advanced-specific
# tuning is deferred until the Tactic Deck itself gets tailored for Advanced play (see
# /playtests/ for whenever that happens); at that point ROSTER may diverge from
# ROSTER_BASE again, the way it used to (see ROSTER_ADVANCED_ARCHIVE below). Worth
# knowing going in: stacking this Control boost UNDER the full Tactic Deck (Nutmeg and
# Step-Over both also rescue a losing Dribble Challenge, the same thing Control was
# raised to compensate for the ABSENCE of) is very likely to run hotter than the
# Advanced Game's old numbers did - not yet measured, flagged here so it isn't a
# surprise the first time someone runs a full-deck batch against this roster.
ROSTER = {k: dict(v) for k, v in ROSTER_BASE.items()}

# Historical Advanced-only roster, live from earlier in the project until 2026-09-08's
# decision above to unify the two tiers. Kept for reference, not currently used
# anywhere - reintroduce (or start the next Advanced pass from) these numbers if/when
# the two rosters diverge again. This is the roster every pre-2026-09-08(-evening)
# playtest report and worked example in the rulebook was actually measured against.
ROSTER_ADVANCED_ARCHIVE = {
    'GK': dict(pace=2, shot=0, control=2, prange=2, srange=None, tackle=2, save=3),
    'SW': dict(pace=3, shot=3, control=2, prange=2, srange=2, tackle=2),
    'WB': dict(pace=2, shot=3, control=3, prange=3, srange=2, tackle=3),
    'PM': dict(pace=3, shot=4, control=4, prange=4, srange=3, tackle=2),
    'PO': dict(pace=4, shot=5, control=3, prange=1, srange=4, tackle=2),
}

# 36-card Command Deck (§6, redesigned 2026-09-10 for the 2-lane board - see board.py's
# lane() docstring). 6 solo Zone cards replace the old 4-Zone-Pair-plus-1-solo-Zone
# mechanism entirely: with only 2 lanes, pairing the 2 zones in a Third would just
# duplicate the Third card, so there's nothing left to pair. Each Zone card carries its
# own fallback, same as the old Zone Pairs did.
#
# 2026-09-22 reallocation (revised same day): Zone cards were the most restrictive card
# in the deck (each names exactly one Third x Lane) and were trimmed from 2 copies to 1,
# freeing 6 slots. Lane and Third briefly went to 3 copies each (+1-each, see the
# now-superseded git-blame/memory history for that version) but were reverted back to
# their original 2 copies each on the same day - Third stayed there, and Tactical Free
# was reverted to its original 6 too. That left all 6 freed slots unallocated, and the
# user chose to put them ALL into Lane: 2 types x +3 each = 2->5 copies. Lane is the only
# card type where a flat 6-card addition divides evenly (2 types), so this stays exactly
# symmetric between Lane-Top/Lane-Bottom with no remainder to arbitrate, unlike Lane's
# earlier awkward 3-way split attempt against Third's 3 types. Net effect vs. the
# pre-reallocation original: only Zone (2->1) and Lane (2->5) changed; Third/TacticalFree/
# FullPress/KeepersCall/Counter are all back to their original counts. Total stays 36 -
# see hexside-cards.html, hexside-components.html, and hexside-rulebook.html's §6 table,
# all independent copies of this same composition, for the matching edit.
COMMAND = (
    [('Zone-T1-Top', 1), ('Zone-T1-Bottom', 1), ('Zone-T2-Top', 1), ('Zone-T2-Bottom', 1),
     ('Zone-T3-Top', 1), ('Zone-T3-Bottom', 1), ('Lane-Top', 5), ('Lane-Bottom', 5),
     ('Third-1', 2), ('Third-2', 2), ('Third-3', 2), ('TacticalFree', 6),
     ('FullPress', 3), ('KeepersCall', 2), ('Counter', 3)]
)
FALLBACK_CARDS = {'Zone-T1-Top', 'Zone-T1-Bottom', 'Zone-T2-Top', 'Zone-T2-Bottom', 'Zone-T3-Top', 'Zone-T3-Bottom'}
# Counter (§10) is never played on your own turn — it's held, then discarded on the
# OPPONENT's turn to force a Tackle Challenge or add a Defense die. card_options() will
# still answer for it (mainly so the ball-carrier-always-activatable check has something
# to append to), but don't "play" Counter as a normal turn card.

# 26-card Tactic Deck (§11). Jockey replaces the original Offside Trap (§10) — Offside
# Trap's own trigger (a back line pushed fully out of its own Third, with a Pass landing
# exactly on the seam column) turned out too narrow to arise in normal play. StrongTackle
# is a straight rename of the original SlideTackle (2026-09-16) - real five-a-side
# football doesn't allow sliding tackles, so the card's own flavor was describing an
# illegal challenge; the mechanics (+1 Attack die, free, double Discipline draw on a
# loss) are completely unchanged, only the name and its flavor text.
TACTIC = [('ThroughBall',2),('Nutmeg',2),('StepOver',2),('CurlShot',2),('OneTwo',2),
          ('Backheel',2),('LongBall',2),('Composure',2),('StrongTackle',2),
          ('LastDitchBlock',2),('Jockey',2),('Press',2),('Foul',2)]
TACTIC_COST = {'ThroughBall':1,'Nutmeg':2,'StepOver':1,'CurlShot':2,'OneTwo':1,'Backheel':1,
               'LongBall':2,'Composure':1,'StrongTackle':0,'LastDitchBlock':2,
               'Jockey':1,'Press':1,'Foul':0}

# §12: the single 12-card Discipline Deck — Warning x2, Advantage/Play On x1, Yellow x2,
# Red x1, Clean Challenge x6. Every draw is independent (shuffled and returned to before
# the next one), never a dealt-down deck — see gen_random() below.
DISCIPLINE_DECK = [('Warning',2),('AdvantagePlayOn',1),('YellowCard',2),('RedCard',1),('CleanChallenge',6)]

def _expand(deck):
    out = []
    for name, n in deck: out += [name]*n
    return out

def gen_random(seed=None):
    """Pre-generates one match's worth of shuffled Command/Tactic decks, dice, and
    Discipline draws into game_random.json. Uses an UNSEEDED random.Random() by default
    (pass seed=... only if you deliberately want a reproducible match) — genuine
    randomness is the whole point of a physical deck, so don't seed a real playtest.
    Generously over-provisioned: 400 dice and 600 Discipline draws per side is far more
    than any single match will need, so nothing runs dry mid-game."""
    rng = random.Random(seed)
    r = {}
    r['coinflip'] = rng.choice(['A','B'])
    for side in ('A','B'):
        cmd = _expand(COMMAND); rng.shuffle(cmd); r['command_'+side] = cmd
        tac = _expand(TACTIC); rng.shuffle(tac); r['tactic_'+side] = tac
        r['dice_'+side] = [rng.randint(1,6) for _ in range(400)]
    # Independent draws, not a dealt-down deck: each entry is its own fresh pick at the
    # 12-card pool's fixed odds (rng.choices samples WITH replacement) — matching the
    # "shuffle and return the card before every draw" rule. No deck-memory, ever.
    pool = _expand(DISCIPLINE_DECK)
    r['discipline'] = rng.choices(pool, k=600)
    json.dump(r, open(RAND, 'w'))
    return r

def face(v, attack=True):
    """§7 dice: each d6 face is Blank (1-2), Flair (3-4), or a hit — Success on an Attack
    die, Stop on a Defense die (5-6)."""
    if v <= 2: return 'blank'
    if v <= 4: return 'flair'
    return 'success' if attack else 'stop'

def load():
    return json.load(open(STATE))

def save(s):
    json.dump(s, open(STATE, 'w'), indent=1)

def _kickoff_taker(side_pos):
    """§5: any unit may be named kickoff-taker, not just the Forward. Randomizes between
    the Poacher and Playmaker when both are available - not a rules requirement (§5 lets a
    side name literally any outfield unit), just the simulation's own default policy for
    which of the two attack-minded positions gets the role, so batches see both instead of
    always the same one. Falls back deterministically through the two Defenders as PO/PM
    are sent off (WB, then SW), and the Goalkeeper is only eligible as the sole unit left,
    per the rulebook's last-resort rule (its own-box requirement is waived for that
    restart). Works on any container supporting `in` - formation() below passes a plain
    list of units still available to place."""
    candidates = [u for u in ('PO', 'PM') if u in side_pos]
    if candidates:
        return random.choice(candidates)
    for unit in ('WB', 'SW'):
        if unit in side_pos:
            return unit
    return next(iter(side_pos))  # everyone but the GK is somehow gone; last resort

_KICKOFF_ZONE = set(B.neighbors('F3')) | {'F3'}  # §5/§8: the non-kicking side must clear
# this 7-hex circle before a restart; the kicking side is exempt (its own units, including
# the taker on F3 itself, may stand inside it).

def _random_draft_hex(s, side, low_end, cols, occ, kicking, must_reach=None):
    """One pick of the kickoff-placement draft (formation(), below): a uniformly random
    choice among every legal candidate hex - §5 has always let each side freely choose
    where its outfield units go, so this exercises that freedom directly rather than
    picking one deterministic "best" hex every time; two batches (or two matches) never
    draft the same layout twice. `occ` is the set of hexes already claimed by either side
    this draft; `kicking` gates the exclusion-zone check (§5: the kicking side may place
    inside it, the non-kicking side may not). `cols` is the legal column set for the
    specific unit being placed - formation() passes the full own-half (A-E/G-K) for a
    Playmaker or Poacher, or just the defensive third (A-D/H-K) for a Sweeper or Wingback
    (§5). `must_reach`, if given, is a (hex, max_dist) pair - candidates are additionally
    filtered to straight-line distance <= max_dist of that hex; formation() uses this for
    §5's mandatory kickoff-support placement (the kicking side's first free pick must land
    within the taker's own Pass Range, so the taker's mandatory §8 Pass always has a legal
    target - never left to chance).

    The two constraints can conflict - Poacher (the only Pass Range 1 unit) as taker, with
    no Playmaker available so the support slot falls to a Wingback or Sweeper, and no hex
    in the defensive third is within Pass Range 1 of F3 (closest is distance 2). §5's
    stated resolution: the Pass-Range guarantee wins, since a kickoff that can never be
    passed is worse than a defender briefly standing past its own third. So if restricting
    to `cols` leaves nothing that also satisfies `must_reach`, the column restriction is
    dropped and the full own-half is used instead - this exception is significant only in
    that one specific combination; every other case satisfies both at once."""
    full_cols = ('A', 'B', 'C', 'D', 'E') if low_end else ('G', 'H', 'I', 'J', 'K')

    def _pool(col_set):
        p = [f'{c}{r}' for c in col_set for r in range(B.min_row(c), B.max_row(c) + 1)
             if f'{c}{r}' not in occ and (kicking or f'{c}{r}' not in _KICKOFF_ZONE)]
        if must_reach:
            target, max_dist = must_reach
            def _reaches(h):
                d, _ = B.straight_line(h, target)
                return d is not None and d <= max_dist
            p = [h for h in p if _reaches(h)]
        return p

    candidates = _pool(cols)
    if not candidates and cols != full_cols:
        candidates = _pool(full_cols)  # the one stated exception above
    if not candidates:
        raise RuntimeError(f"no legal own-half hex left for side {side}"
                            + (f" within reach of {must_reach[0]}" if must_reach else ""))
    return random.choice(candidates)

def formation(s, kicker, sent_off=(), avoid_taker=None):
    """§5: builds both sides' starting positions for a restart via the alternating
    kickoff-placement draft. There's no fixed template - §5 has always let each side
    freely choose where its outfield units go, within their own legal range. What this
    function fixes is the ORDER placement happens in:
      1. The kicking side's taker (_kickoff_taker's random pick between PO and PM, where
         both are available) is forced onto F3.
      2. Sides then alternate, one unit at a time in priority order (PO, PM, WB, SW),
         starting with the NON-kicking side - every pick after the first can react to
         everything already on the board, on either side.
    The Goalkeeper is placed first, automatically, into its own zone (_zone_hex) - not
    part of the draft, since §4/§5 already pin it to a 3-hex zone with no real choice to
    make. An Emergency Goalkeeper deputy (§12) gets the exact same treatment when the real
    GK is off: placed into the zone before anyone else drafts, and pulled out of
    `remaining` so the normal draft can't also send it somewhere else. Root-caused
    2026-09-17: leaving the deputy in the ordinary draft pool let another outfield unit
    legally draft onto the same zone hex the deputy needed a moment later, at which point
    _reapply_emergency_gk's own re-placement (called right after formation() returns) had
    nowhere conflict-free left to put it - the K3-double-occupancy crash. Sweeper and
    Wingback (the two Defenders) are confined to their own defensive
    third (A-D or H-K) for every pick but the taker's; Playmaker and Poacher (the
    Midfielder and Forward) may use the full own-half range, including the one column
    that also belongs to Third 2 (E or G) - restored 2026-09-13 from the original
    rulebook, which had dropped it somewhere along the way. Every pick within its own
    legal range is uniformly random (_random_draft_hex) - §5 leaves the actual choice
    entirely to the side making it, so this exercises that freedom directly rather than
    always drafting the same layout. The kicking side's very next placement after the
    taker - its first free pick - is additionally mandatory support: it must land within
    the taker's own Pass Range of F3, so the taker's mandatory §8 kickoff Pass is always
    guaranteed a legal target. Without this, a taker with nobody in range has no legal
    Pass at all and the restart deadlocks - never actually possible under this draft (the
    constraint sees to that), but a real failure mode confirmed the hard way when testing
    a placement policy that ignored it. These two rules can conflict (Poacher as taker,
    prange 1, with no Playmaker available to take the support slot instead of a defender)
    - see _random_draft_hex's own docstring for the resolution (Pass-Range wins).

    `sent_off` ('side:unit' strings) excludes units from the draft entirely, so a stripped
    unit can never end up forced onto F3 as the taker. `avoid_taker`, if given (the
    Emergency Goalkeeper deputy - see goal_restart/halftime_reset), is skipped in favor of
    any other available unit, so a deputy isn't sent forward for the restart unless it's
    the only unit left - if every outfield unit is gone too, the real Goalkeeper itself
    becomes eligible as a last resort (§5), pulled out of its zone onto F3 for this
    restart alone. Mutates s['pos'] directly (call with it already reset to
    {'A': {}, 'B': {}}) and returns the taker unit for `kicker`."""
    a_defends_low = s['a_defends_low']
    low_end = {'A': a_defends_low, 'B': not a_defends_low}
    remaining = {side: [u for u in ('PO', 'PM', 'WB', 'SW') if f'{side}:{u}' not in sent_off]
                 for side in ('A', 'B')}
    deputy = {}
    for side in ('A', 'B'):
        if f'{side}:GK' not in sent_off:
            s['pos'][side]['GK'] = _zone_hex(s, side)
        else:
            dep = s.get('emergency_gk', {}).get(side)
            if dep in remaining[side]:
                deputy[side] = dep
                remaining[side].remove(dep)
                s['pos'][side][dep] = _zone_hex(s, side, dep)
    occ = set(s['pos']['A'].values()) | set(s['pos']['B'].values())

    gk_alive = f'{kicker}:GK' not in sent_off
    kicker_deputy = deputy.get(kicker)
    taker_pool = remaining[kicker] + (['GK'] if gk_alive else []) + ([kicker_deputy] if kicker_deputy else [])
    if not taker_pool:
        raise RuntimeError(f"{kicker} has no unit left to take the kickoff")
    preferred = [u for u in taker_pool if u != avoid_taker]
    taker = _kickoff_taker(preferred if preferred else taker_pool)
    if taker == 'GK':
        occ.discard(s['pos'][kicker]['GK'])  # leaving its zone for this restart only (§5)
    elif taker == kicker_deputy:
        occ.discard(s['pos'][kicker][kicker_deputy])  # leaving its zone for this restart only (§5)
    else:
        remaining[kicker].remove(taker)
    s['pos'][kicker][taker] = 'F3'
    occ.add('F3')

    non_kicker = 'B' if kicker == 'A' else 'A'
    turn = non_kicker
    kicker_needs_support = True
    while remaining['A'] or remaining['B']:
        if not remaining[turn]:
            turn = 'B' if turn == 'A' else 'A'
            continue
        unit = remaining[turn].pop(0)
        full_cols = ('A', 'B', 'C', 'D', 'E') if low_end[turn] else ('G', 'H', 'I', 'J', 'K')
        own_third_cols = ('A', 'B', 'C', 'D') if low_end[turn] else ('H', 'I', 'J', 'K')
        cols = own_third_cols if unit in ('SW', 'WB') else full_cols
        must_reach = ('F3', ROSTER[taker]['prange']) if (turn == kicker and kicker_needs_support) else None
        h = _random_draft_hex(s, turn, low_end[turn], cols, occ, kicking=(turn == kicker), must_reach=must_reach)
        if turn == kicker:
            kicker_needs_support = False
        s['pos'][turn][unit] = h
        occ.add(h)
        turn = 'B' if turn == 'A' else 'A'

    return taker

def new_state():
    """Starts a fresh match: coin-flip kickoff, kickoff-placement draft (formation(),
    §5), 5 Command + 3 Tactic Cards each. Call gen_random() first."""
    r = json.load(open(RAND))
    kicker = r['coinflip']
    s = dict(
        turn=1, half=1, kicker=kicker, a_defends_low=True, pos={'A':{}, 'B':{}},
        ball={}, kickoff_taker={},
        score={'A':0,'B':0}, flair={'A':0,'B':0}, yellow=[],
        p_cmd={'A':0,'B':0}, p_tac={'A':0,'B':0}, p_dice={'A':0,'B':0}, p_disc=0,
        hand_cmd={'A':[],'B':[]}, hand_tac={'A':[],'B':[]}, debt={'A':0,'B':0},
        log=[]
    )
    taker = formation(s, kicker)
    s['ball'] = {'side':kicker,'unit':taker,'hex':'F3'}
    s['kickoff_taker'] = {'side':kicker,'unit':taker}
    for side in ('A','B'):
        s['hand_cmd'][side] = r['command_'+side][:5]; s['p_cmd'][side] = 5
        s['hand_tac'][side] = r['tactic_'+side][:3]; s['p_tac'][side] = 3
    save(s)
    return s

def _draw_with_reshuffle(rand_key, s, pointer_dict, side, deck_source):
    """§6: 'reshuffle the discard pile when the draw pile runs out' — when the
    pre-generated stream for `rand_key` (e.g. 'command_A') is exhausted, reshuffle a fresh
    copy of the full deck (unseeded — a genuine new shuffle, not a repeat of the same
    order) and append it, so play never crashes on a long match. This was a real bug
    (confirmed by an external playtest report: a 48-turn match with heavy Full Press/
    Counter cycling exhausted a 35-card Command pool at turn 42 and crashed on every draw
    after that, for the rest of the match)."""
    r = json.load(open(RAND))
    if pointer_dict[side] >= len(r[rand_key]):
        fresh = _expand(deck_source); random.Random().shuffle(fresh)
        r[rand_key] = r[rand_key] + fresh
        json.dump(r, open(RAND, 'w'))
    c = r[rand_key][pointer_dict[side]]
    pointer_dict[side] += 1
    return c

def draw_cmd(s, side):
    return _draw_with_reshuffle('command_'+side, s, s['p_cmd'], side, COMMAND)
def draw_tac(s, side):
    return _draw_with_reshuffle('tactic_'+side, s, s['p_tac'], side, TACTIC)
def draw_disc(s):
    """One draw from the single 12-card Discipline Deck — independent every time (§12)."""
    r = json.load(open(RAND)); c = r['discipline'][s['p_disc']]; s['p_disc']+=1; return c
def draw_disc_foul(s):
    """A Foul (Tactic Card) draws from the same deck, but redraws past any Clean Challenge
    (§12) — a called Foul is already an adjudicated stoppage, so it always lands a real
    card. Standard Tackle and Strong Tackle should call draw_disc() instead."""
    while True:
        c = draw_disc(s)
        if c != 'CleanChallenge':
            return c

def roll(s, side, n, attack=True):
    """Rolls n dice for `side` from its pre-generated stream, banking any Flair rolled
    (capped at 5 per §8/§11). Returns (raw values, faces, hit count)."""
    r = json.load(open(RAND)); pool = r['dice_'+side]
    vals = pool[s['p_dice'][side]:s['p_dice'][side]+n]; s['p_dice'][side]+=n
    faces = [face(v, attack) for v in vals]
    hits = faces.count('success' if attack else 'stop')
    flair = faces.count('flair')
    s['flair'][side] = min(5, s['flair'][side]+flair)
    return vals, faces, hits

def contest(s, atk_side, atk_dice, def_side, def_dice, label='', is_tackle=False):
    """The shared Resolution Sequence roll (§7): attacker needs STRICTLY MORE hits than
    the defender (a tie, including 0-0, goes to the defender). Use this directly for a
    Pass, Dribble Challenge, or Shot; tackle()/strong_tackle() wrap it with the Discipline
    side-effects a Tackle Challenge also carries."""
    av, af, ah = roll(s, atk_side, atk_dice, True)
    dv, df, dh = roll(s, def_side, def_dice, False)
    win = ah > dh
    line = f"[{label}] {atk_side} rolls {av}->{af} ({ah} succ) | {def_side} rolls {dv}->{df} ({dh} stop) => {'ATTACKER WINS' if win else 'DEFENDER HOLDS'}"
    if is_tackle and not win and s['flair'][atk_side] > 0:
        s['flair'][atk_side] -= 1
        line += f"  [failed Tackle: {atk_side} docked 1 Flair, now {s['flair'][atk_side]}]"
    s['log'].append(line); print(line)
    return win, ah, dh

def _drop_ball_if_holding(s, side, unit, hex_):
    """If `unit` (just removed from `side`'s s['pos']) was the ball carrier, the ball
    can't leave the pitch with it - set it loose at the hex it was just standing on
    instead. Root-caused 2026-09-17: apply_discipline's three removal points (2nd
    Yellow -> Red, a straight Red Card, and send_to_sinbin's own first-Yellow case)
    all popped the unit from s['pos'] without ever touching s['ball'], which was never
    reachable before a Discipline card could land directly on the CURRENT ball carrier
    itself - every existing caller (a lost Tackle, a Foul) always cards the unit that
    INITIATED the challenge, never the passive carrier being tackled/fouled. The
    "Playing Out" character Signature's own forced-return check is the first caller
    that can genuinely land a card on whichever unit currently holds the ball - found
    via a real KeyError crash (move_ball_carrier's `s['pos'][mover][carrier]`, with
    s['ball']['unit'] left pointing at a unit no longer in s['pos']), not guessed."""
    if s['ball']['side'] == side and s['ball']['unit'] == unit:
        s['ball'] = {'side': None, 'unit': None, 'hex': hex_}

def apply_discipline(s, side, unit, card):
    """Applies a drawn Discipline card's effect to the offending unit (§12). Uses string
    keys throughout ('A:WB') — JSON object keys must be strings, and a tuple key silently
    becomes a list on save/reload, breaking membership checks like `in`."""
    key = f"{side}:{unit}"
    sent_off_now = False
    first_yellow_now = False
    if card == 'YellowCard':
        if key in s.get('yellow', []):
            s['yellow'].remove(key)
            hex_ = s['pos'][side].pop(unit, None)  # 2nd Yellow = Red: unit off the pitch
            _drop_ball_if_holding(s, side, unit, hex_)
            s.setdefault('sent_off', []).append(key)
            s.get('sinbin', {}).pop(key, None)  # a Red always supersedes a pending sin-bin trip
            sent_off_now = True
            line = f"  [DISCIPLINE: {side}-{unit} 2nd Yellow -> RED, removed from the match]"
        else:
            s.setdefault('yellow', []).append(key)
            s.setdefault('pace_mod', {})[key] = s.get('pace_mod',{}).get(key,0) - 1
            first_yellow_now = True
            line = f"  [DISCIPLINE: {side}-{unit} YELLOW CARD, Pace -1 for the rest of the match]"
    elif card == 'RedCard':
        hex_ = s['pos'][side].pop(unit, None)
        _drop_ball_if_holding(s, side, unit, hex_)
        s.setdefault('sent_off', []).append(key)
        s.get('sinbin', {}).pop(key, None)  # a Red always supersedes a pending sin-bin trip
        sent_off_now = True
        line = f"  [DISCIPLINE: {side}-{unit} RED CARD, removed from the match]"
    elif card == 'AdvantagePlayOn':
        line = "  [DISCIPLINE: Advantage/Play On drawn - fouled side keeps the ball, plays on]"
    elif card == 'CleanChallenge':
        line = "  [DISCIPLINE: Clean Challenge drawn - the tackle failed, but it wasn't a foul]"
    else:
        line = f"  [DISCIPLINE: {card} drawn - no effect]"
    s['log'].append(line); print(line)
    if sent_off_now and is_goalkeeper_role(s, side, unit):
        # Either the real Goalkeeper just went, or the current Emergency Goalkeeper
        # deputy did (§12: "if that first deputy is itself later sent off, the side
        # names a second deputy the same way") — either way, a fresh assignment is due.
        assign_emergency_gk(s, side)
    elif first_yellow_now:
        # §12 sin-bin: a FIRST Yellow (not the 2nd-Yellow-to-Red case above, already
        # handled) also pulls the unit off the pitch for one of its own side's turns,
        # on top of the permanent Pace -1 already applied.
        send_to_sinbin(s, side, unit)

def _emergency_gk_pick(side_pos):
    """Which outfield unit becomes emergency keeper by default, mirroring
    _kickoff_taker()'s same-spirit convenience default — §12 leaves the actual choice to
    the side itself; pass `unit` to assign_emergency_gk() directly to choose a different
    one. Sweeper preferred as the most defense-minded outfield unit."""
    for unit in ('SW', 'WB', 'PM', 'PO'):
        if unit in side_pos:
            return unit
    return None

def assign_emergency_gk(s, side, unit=None):
    """§12: the instant the Goalkeeper is sent off, its side names one remaining outfield
    unit as emergency keeper, placed in its own goal box with no activation needed. Pass
    `unit` to choose which one; omit it for the default pick (see _emergency_gk_pick).
    That unit keeps its own stats/Signature for everything else — see save_stat() for
    what it uses in goal instead of a real Goalkeeper's Save, and it never gains Command
    the Box. Returns the assigned unit, or None if no outfield units are left at all."""
    if unit is None:
        unit = _emergency_gk_pick(s['pos'][side])
    if unit is None:
        return None
    target = _zone_hex(s, side, unit)
    s['pos'][side][unit] = target
    s.setdefault('emergency_gk', {})[side] = unit
    line = f"  [{side}'s {unit} becomes Emergency Goalkeeper at {target} - Save 1, no Shot-Stopper]"
    s['log'].append(line); print(line)
    return unit

def save_stat(s, side, unit):
    """The Defense stat to use for a Save (§8): the real Goalkeeper's own Save 3, or an
    Emergency Goalkeeper's flat Save 1 if this side's Goalkeeper has been sent off (§12).
    Use this instead of ROSTER[unit]['save'] directly wherever a Save might be made."""
    if s.get('emergency_gk', {}).get(side) == unit:
        return 1
    return ROSTER[unit]['save']

def shot_dice(unit, breakaway=False):
    """Attack dice for a Shot (§8): the unit's own Shot stat, +1 if it's Through on
    Goal - the shooting unit itself won the Dribble Challenge that carried it into
    this shooting position, earlier in this same activation. The engine doesn't
    track per-activation history itself (see WHAT THIS ENGINE DOES NOT DO) - pass
    breakaway=True yourself once you know the answer; this just gets the arithmetic
    right and gives the rule a single, discoverable home."""
    return ROSTER[unit]['shot'] + (1 if breakaway else 0)

def bounce_pass_options(s, side, unit):
    """Every legal bounce-pass outcome for `unit` from its current hex (this session's
    design pass, 2026-09-16): tries all 4 axes, both directions (8 lines total) via
    B.bounce_pass_reach(), budgeted by the unit's own Pass Range (ROSTER[unit]['prange'] -
    the same stat a normal Pass uses, per this session's ruling that Pass Range counts
    hexes crossed on BOTH segments of a bounce combined). Returns a list of outcome
    dicts, each tagged by 'kind':
      'net'         - the line reaches the opposing net, either because it's aimed
                      straight through a goal-mouth hex (A3/A4/K3/K4 - no wall there on
                      any axis, this session's ruling) or because it threads all the way
                      to one of the 3 real net points some other way (see
                      bounce_pass_reach's own docstring). Resolved exactly like a Shot
                      (Save-contested, §8), never as a normal Pass.
      'teammate'    - lands exactly on a hex this side already occupies - a normal
                      completed pass, just via a bent path instead of a straight one.
      'intercepted' - lands exactly on a hex the OPPOSING side occupies - legal to
                      attempt, just a bad idea; tracked for completeness, the simplified
                      driver AI never deliberately picks one.
      'loose'       - lands on a hex nobody occupies - a legal, if riskier, outcome (this
                      session's ruling: unlike a normal Pass, which is always aimed at a
                      chosen teammate, a bounce pass's path is fixed by the wall it
                      reflects off, so it can land on nobody). Whoever activates a unit
                      onto that hex first claims the ball, same as any other loose ball
                      (§9's Dribble-Challenge spillage, §8's Save rebound).
    Every outcome carries 'end_hex' (None for a 'net' outcome) and 'axis'/'direction' so a
    caller can actually replay the chosen line."""
    unit_hex = s['pos'][side][unit]
    budget = ROSTER[unit]['prange']
    # Excludes the unit's OWN hex - a single bounce can genuinely loop back to exactly
    # where it started (verified this session: a full round-trip off a back wall with
    # enough budget lands right back on the passer), and that has to resolve as 'loose'
    # (the ball comes back to an empty hex the passer just vacated in ball-terms, even
    # though they're still standing there), never as 'teammate' - you can't be your own
    # pass target.
    own_pos = set(h for u, h in s['pos'][side].items() if u != unit)
    opp_pos = set(s['pos']['B' if side == 'A' else 'A'].values())
    out = []
    for axis in ('V', 'D1', 'D2', 'H'):
        for direction in (0, 1):
            r = B.bounce_pass_reach(unit_hex, axis, direction, budget)
            if r['reaches_net']:
                out.append({'kind': 'net', 'end': r['reaches_net'], 'end_hex': None, 'axis': axis, 'direction': direction})
            elif r['path']:
                target = r['path'][-1]
                if target in own_pos:
                    kind = 'teammate'
                elif target in opp_pos:
                    kind = 'intercepted'
                else:
                    kind = 'loose'
                out.append({'kind': kind, 'end_hex': target, 'axis': axis, 'direction': direction})
    return out

def send_to_sinbin(s, side, unit):
    """§12: pulls a first-Yellow unit off the pitch immediately - it misses `side`'s
    next turn entirely, then returns automatically at the start of the turn after that
    (sinbin_check(), called by the driver at the start of each of `side`'s turns). The
    Goalkeeper (or its Emergency deputy) is not exempt: a sin-binned keeper leaves its
    own zone genuinely empty for that one turn, real tension by design - Emergency
    Goalkeeper only ever covers a full send-off, not a temporary sin-bin. No-op if
    `unit` is already off the pitch for some other reason (e.g. this Yellow arrived in
    the same Discipline resolution as something that already removed it)."""
    hex_ = s['pos'][side].pop(unit, None)
    if hex_ is None:
        return
    _drop_ball_if_holding(s, side, unit, hex_)
    # 2, not 1: sinbin_check() is called once at the start of each of `side`'s own
    # turns, so the first call must tick down without returning yet (that's the turn
    # being missed) and only the second call actually brings the unit back.
    s.setdefault('sinbin', {})[f"{side}:{unit}"] = 2
    line = f"  [{side}'s {unit} is sent to the sin-bin from {hex_} - misses {side}'s next turn]"
    s['log'].append(line); print(line)

def _touchline_hex(s, side):
    """A legal, unoccupied touchline hex (a column's own first row, or its own last row)
    inside `side`'s own half - where a sin-binned unit re-enters (§12). Not used for the
    Goalkeeper role, which re-enters inside its own zone instead (see sinbin_check). Uses
    B.min_row()/B.max_row() rather than a hardcoded row 1, so a short column's own first
    row (0, not 1) is correctly offered too."""
    own_end = 'A' if (side == 'A') == s['a_defends_low'] else 'K'
    half_cols = ['A','B','C','D','E'] if own_end == 'A' else ['G','H','I','J','K']
    occ = occupied(s)
    for c in half_cols:
        top = f"{c}{B.min_row(c)}"
        bottom = f"{c}{B.max_row(c)}"
        for h in (top, bottom):
            if h not in occ:
                return h
    return f"{half_cols[0]}{B.min_row(half_cols[0])}"

def sinbin_check(s, side):
    """Call at the very start of `side`'s own turn, before anything else. Ticks down
    any pending sin-bin (§12) for this side's units and returns one to the pitch the
    moment its count reaches 0 - at a touchline hex inside its own half, or inside its
    own Goalkeeper Zone if it plays that role (is_goalkeeper_role()). No-op if nothing
    is currently serving a sin-bin turn for this side. Defensive: a unit already in
    `sent_off` never returns, even if some other path left a stale sin-bin entry behind
    for it - apply_discipline() already clears this itself when a Red supersedes a
    pending sin-bin trip (e.g. a Strong Tackle's two-card draw landing Yellow then
    Yellow/Red on the same unit), but this guard is cheap insurance against that
    invariant ever being broken by a future code path."""
    sinbin = s.get('sinbin', {})
    sent_off = set(s.get('sent_off', []))
    for key in list(sinbin.keys()):
        k_side, unit = key.split(':')
        if k_side != side:
            continue
        if key in sent_off:
            del sinbin[key]
            continue
        sinbin[key] -= 1
        if sinbin[key] <= 0:
            del sinbin[key]
            target = _zone_hex(s, side) if is_goalkeeper_role(s, side, unit) else _touchline_hex(s, side)
            s['pos'][side][unit] = target
            line = f"  [{side}'s {unit} returns from the sin-bin at {target}]"
            s['log'].append(line); print(line)

def play_jockey(s, side, unit):
    """§10/§11: discard Jockey (1 Flair) from `side`'s Tactic hand, reacting the instant an
    adjacent opposing unit is activated to move. Doesn't compute the reduced move itself —
    call reach(s, opp_side, opp_unit, extra_pace=-1) for that unit's actual reduced reach
    this move. Returns False (no-op) if the side doesn't have the Flair to pay for it."""
    if s['flair'][side] < 1: return False
    s['flair'][side] -= 1
    s['hand_tac'][side].remove('Jockey')
    line = f"  [{side} plays Jockey (1 Flair) - the reacted-to unit's Pace is reduced by 1 for this move only]"
    s['log'].append(line); print(line)
    return True

def play_composure(s, side):
    """§11: replaces the retired Advantage Play (same deck slot, 2 copies). Composure
    (Attack, 1 Flair) lets the shooting side reroll up to 1 die from a Shot it has just
    taken - Step-Over's exact shape (a post-roll reroll, Resolution Sequence step 4),
    redirected from Dribble Challenges to Shots. Doesn't perform the reroll itself -
    call roll() again for the die/dice being rerolled and use the better result.
    Returns False (no-op) if the side doesn't have the Flair to pay for it."""
    if s['flair'][side] < 1: return False
    s['flair'][side] -= 1
    s['hand_tac'][side].remove('Composure')
    line = f"  [{side} plays Composure (1 Flair) - may reroll up to 1 die from that Shot]"
    s['log'].append(line); print(line)
    return True

def kickoff_release_required(s, side, unit):
    """§5/§8: True if `unit` is still under the standing kickoff-release obligation —
    meaning its entire activation this turn must be a single Pass to a teammate within
    Pass Range, straight from F3: no Move first, no Clearance, never a Shot or a Tackle.
    Mirrors real football's restriction against a kickoff-taker touching the ball twice
    in a row."""
    kt = s.get('kickoff_taker')
    return bool(kt and kt['side'] == side and kt['unit'] == unit)

def release_kickoff(s, side, unit):
    """§5/§8: discharges `unit`'s standing kickoff-release obligation, the moment it
    actually plays the required Pass to a teammate — successfully or not, contested or
    not; a Dribble Challenge, a Clearance, or a Shot can never discharge it. No-op if
    `unit` isn't currently under the obligation."""
    kt = s.get('kickoff_taker')
    if kt and kt['side'] == side and kt['unit'] == unit:
        s['kickoff_taker'] = None
        line = f"  [{side}'s {unit} releases the kickoff ball - Shot/Tackle now legal for it again]"
        s['log'].append(line); print(line)

def tackle(s, atk_side, atk_unit, def_side, tackle_stat, def_dice, label=''):
    """A standard Tackle Challenge (§8). On failure: the usual 1-Flair cost applies (via
    contest's is_tackle flag), PLUS a lost Tackle Challenge draws once from the 12-card
    Discipline Deck for the tackling unit. Not a Foul: no stoppage, no Free Kick — the
    ball simply stays with the carrier either way."""
    win, ah, dh = contest(s, atk_side, tackle_stat, def_side, def_dice, label, is_tackle=True)
    if not win:
        card = draw_disc(s)
        apply_discipline(s, atk_side, atk_unit, card)
    return win, ah, dh

def strong_tackle(s, atk_side, atk_unit, def_side, tackle_stat, def_dice, label=''):
    """Free to play (§11). +1 Attack die to the Tackle. On failure: the usual 1-Flair
    Tackle cost still applies, PLUS this unit mistimed it — draw from the same Discipline
    Deck TWICE (Clean Challenge is a live result on each draw, same as a standard Tackle)
    and apply both cards in sequence. Still not a Foul — no stoppage. Removes 'StrongTackle'
    from the attacking side's Tactic hand. Renamed from SlideTackle (2026-09-16, pure
    rename, mechanics unchanged) - real five-a-side football doesn't allow sliding
    tackles."""
    s['hand_tac'][atk_side].remove('StrongTackle')
    s['log'].append(f"  [{atk_side} plays Strong Tackle, free, +1 Attack die]")
    win, ah, dh = contest(s, atk_side, tackle_stat+1, def_side, def_dice, label+' (Strong Tackle, +1 die)', is_tackle=True)
    if not win:
        for _ in range(2):
            card = draw_disc(s)
            apply_discipline(s, atk_side, atk_unit, card)
    return win, ah, dh

def replenish(s, side):
    """End-of-turn draw-back-up-to-5 (§6), honoring Full Press debt (§6: two turns of
    discard-unseen after playing Full Press). Also tops the Tactic hand back up to 3."""
    needed = 5 - len(s['hand_cmd'][side])
    for _ in range(needed):
        c = draw_cmd(s, side)
        if s['debt'][side] > 0:
            s['debt'][side] -= 1
            left = s['debt'][side]
            s['log'].append(f"  [{side} draw-up: 1 card discarded unseen (Full Press debt, {left} left)]")
        else:
            s['hand_cmd'][side].append(c)
    while len(s['hand_tac'][side]) < 3:
        s['hand_tac'][side].append(draw_tac(s, side))

def cycle_tactic(s, side, card):
    """§11: once per turn, 1 Flair, discard a dead Tactic Card for a fresh draw."""
    if s['flair'][side] < 1: return False
    s['flair'][side] -= 1
    s['hand_tac'][side].remove(card)
    s['hand_tac'][side].append(draw_tac(s, side))
    return True

def _reapply_emergency_gk(s):
    """After a formation reset (goal_restart/halftime_reset rebuild `pos` from the
    default template, which assumes a real Goalkeeper), re-place any already-assigned
    Emergency Goalkeeper (§12) into its side's CURRENT goal box — a_defends_low may have
    just flipped at halftime, so this re-derives the box fresh rather than reusing
    wherever it stood before the reset."""
    for side, unit in s.get('emergency_gk', {}).items():
        if 'GK' in s['pos'][side] or unit not in s['pos'][side]:
            continue  # keeper's back (shouldn't happen once assigned), or deputy also gone
        s['pos'][side][unit] = _zone_hex(s, side, unit)

def halftime_reset(s):
    """§15: at the match's midpoint, swap ends, full formation reset via the kickoff-
    placement draft (§5), the side that DIDN'T open the match kicks off. Sent-off units
    (Red Card, or 2nd Yellow) never return to the pitch on a restart. Call this once, at
    the midpoint turn — for a 12-a-side quick match that's turn 12 of 24 (6 turns each),
    not turn 16."""
    opener = s['kicker']  # who opened turn 1
    new_kicker = 'B' if opener == 'A' else 'A'
    s['a_defends_low'] = not s['a_defends_low']
    s['pos'] = {'A':{}, 'B':{}}
    sent_off = set(s.get('sent_off', []))
    deputy = s.get('emergency_gk', {}).get(new_kicker)
    taker = formation(s, new_kicker, sent_off=sent_off, avoid_taker=deputy)
    _reapply_emergency_gk(s)
    s['ball'] = {'side':new_kicker,'unit':taker,'hex':'F3'}
    s['kickoff_taker'] = {'side':new_kicker,'unit':taker}
    s['half'] = 2
    s['debt'] = {'A':0,'B':0}
    msg = f"=== HALFTIME: ends swapped ({'A' if s['a_defends_low'] else 'B'} now defends the A3/A4 end), {new_kicker} kicks off half 2 ==="
    s['log'].append(msg); print(msg)

def goal_restart(s, conceding_side):
    """§8: after a goal, full reset via the kickoff-placement draft (§5), the side that
    conceded kicks off. Sent-off units never return. The kickoff-taker is placed on F3
    with the ball."""
    s['pos'] = {'A':{}, 'B':{}}
    sent_off = set(s.get('sent_off', []))
    deputy = s.get('emergency_gk', {}).get(conceding_side)
    taker = formation(s, conceding_side, sent_off=sent_off, avoid_taker=deputy)
    _reapply_emergency_gk(s)
    s['ball'] = {'side':conceding_side,'unit':taker,'hex':'F3'}
    s['kickoff_taker'] = {'side':conceding_side,'unit':taker}

def occupied(s, exclude=None):
    out = set()
    for side in ('A','B'):
        for u, h in s['pos'][side].items():
            if exclude == (side,u): continue
            out.add(h)
    return out

def check_no_overlap(s):
    """Call this after every position change. Raises with a clear message if any hex
    ends up holding two units — a real bug, not a legal board state."""
    seen = {}
    for side in ('A','B'):
        for u, h in s['pos'][side].items():
            if h in seen:
                raise ValueError(f"OCCUPANCY CONFLICT: {h} holds both {seen[h]} and {side}-{u}")
            seen[h] = f"{side}-{u}"
    return True

def enemy_zoc(s, side):
    """§9: the union of every hex adjacent to an opposing unit — this is what threatens
    `side`'s ball-carrier (entering or moving through it triggers a Dribble Challenge).
    Doesn't matter at all for a unit that isn't carrying the ball."""
    other = 'B' if side=='A' else 'A'
    z = set()
    for u, h in s['pos'][other].items():
        z |= set(B.neighbors(h))
    return z

def reach(s, side, unit, extra_pace=0):
    """Every hex `unit` can reach this turn (ignoring Dribble Challenges — those are
    resolved separately, not a movement cost baked into this BFS), as {hex: (cost, path)}.
    Respects other units blocking hexes and this unit's own Pace (plus any Yellow-Card
    pace_mod and extra_pace, e.g. Wingback's Overlap signature)."""
    start = s['pos'][side][unit]
    occ = occupied(s, exclude=(side,unit))
    pace = ROSTER[unit]['pace'] + extra_pace + s.get('pace_mod',{}).get(f"{side}:{unit}",0)
    pace = max(pace, 0)
    best = {start: (0, [start])}
    frontier = [start]
    for _ in range(pace):
        nf = []
        for h in frontier:
            d0 = best[h][0]
            for n in B.neighbors(h):
                if n in occ: continue
                if n not in best or best[n][0] > d0+1:
                    best[n] = (d0+1, best[h][1]+[n])
                    nf.append(n)
        frontier = nf
    return best

def is_goalkeeper_role(s, side, unit):
    """§5/§14: True if `unit` currently plays the goalkeeper role for `side` - the real
    Goalkeeper, or its Emergency deputy (§12) if the real one has been sent off. Used by
    legal_reach() to decide which confinement rule applies to a given unit."""
    return unit == 'GK' or s.get('emergency_gk', {}).get(side) == unit

def legal_reach(s, side, unit, extra_pace=0, ignore_zone_lock=False):
    """reach(), filtered by the Goalkeeper Zone rules (§4/§5/§14): the goalkeeper-role
    unit (is_goalkeeper_role() above) may never end its move outside its own zone, full
    stop - whether it's just repositioning or happens to be the ball-carrier. Every
    other unit may never enter the OPPONENT's zone (symmetric with Net hexes already
    being unenterable), though it may stand inside its own side's zone freely. Prefer
    this over calling reach() directly wherever a unit's move destination is chosen.

    `ignore_zone_lock`, added 2026-09-17 for the "Playing Out" character Signature
    (hexside-character-cards.html) - a Goalkeeper's once-per-match "act as a normal
    outfield unit for one activation": skips straight to the outfield branch below
    (still barred from the OPPONENT's zone, same as any outfield unit) instead of the
    own-zone-only filter. No effect on a non-goalkeeper-role unit."""
    r = reach(s, side, unit, extra_pace=extra_pace)
    own_end = 'A' if (side == 'A') == s['a_defends_low'] else 'K'
    if is_goalkeeper_role(s, side, unit) and not ignore_zone_lock:
        zone = set(B.GK_ZONE[own_end])
        return {h: v for h, v in r.items() if h in zone}
    att_end = 'K' if own_end == 'A' else 'A'
    off_limits = set(B.GK_ZONE[att_end])
    return {h: v for h, v in r.items() if h not in off_limits}

def gk_zone_occupied(s, side):
    """§8: True if a goalkeeper-ROLE unit (is_goalkeeper_role() - the real Goalkeeper,
    or its Emergency deputy) currently stands in `side`'s own Goalkeeper Zone. This is
    deliberately NOT "any of side's own units" - an outfield teammate parked in the
    zone (legal - §4/§5/§14 only bars the OPPONENT from entering it) never defends a
    Shot on its own, most importantly while the real Goalkeeper is serving a sin-bin
    trip (Emergency Goalkeeper doesn't cover a sin-bin, by design - see send_to_sinbin,
    §12): that outfield unit's presence must not make the zone count as covered, or the
    sin-bin would cost nothing whenever a side had a spare defender to spot it. Check
    this instead of the literal 2-hex goal box when resolving whether a Shot is an
    automatic goal - the zone, not the box, is what confinement/exclusion actually
    keeps populated (or doesn't) in practice."""
    own_end = 'A' if (side == 'A') == s['a_defends_low'] else 'K'
    zone = set(B.GK_ZONE[own_end])
    return any(h in zone for u, h in s['pos'][side].items() if is_goalkeeper_role(s, side, u))

def _zone_hex(s, side, unit=None):
    """First unoccupied hex of `side`'s own Goalkeeper Zone, for placing a Goalkeeper,
    an Emergency deputy, or a returning sin-bin Goalkeeper (§5/§12/§14). `unit` is
    excluded from the occupancy check if it's already standing somewhere (e.g. being
    re-placed on a restart).

    All 3 zone hexes can legally be held by this side's OTHER units at once (§5 lets a
    side stand freely in its own zone) - formation() reserves the zone for a Goalkeeper/
    deputy before anyone else drafts, specifically to keep this rare, but assign_emergency_gk
    (mid-play) and sinbin_check (a goalkeeper-role return) place into a board that's
    already fully set, where it's still possible. Root-caused 2026-09-17: this used to
    hand back GK_ZONE[0] unconditionally in that case - a hex it had just proven was
    occupied - which is exactly what produced the K3-double-occupancy crash. Widen the
    search instead: the zone's own neighbors, then anywhere at all, so this only ever
    returns a hex nothing else is standing on."""
    own_end = 'A' if (side == 'A') == s['a_defends_low'] else 'K'
    occ = occupied(s, exclude=(side, unit) if unit else None)
    for h in B.GK_ZONE[own_end]:
        if h not in occ:
            return h
    ring = {n for h in B.GK_ZONE[own_end] for n in B.neighbors(h)} - set(B.GK_ZONE[own_end])
    for h in ring:
        if h not in occ:
            return h
    for c in B.COLS:
        for r in range(B.min_row(c), B.max_row(c) + 1):
            h = f"{c}{r}"
            if h not in occ:
                return h
    return B.GK_ZONE[own_end][0]  # entire pitch occupied - can't happen with ≤10 units

def card_zones(card):
    """The single (third, lane) a Zone card names."""
    m = {
        'Zone-T1-Top': (1, 'Top'),
        'Zone-T1-Bottom': (1, 'Bottom'),
        'Zone-T2-Top': (2, 'Top'),
        'Zone-T2-Bottom': (2, 'Bottom'),
        'Zone-T3-Top': (3, 'Top'),
        'Zone-T3-Bottom': (3, 'Bottom'),
    }
    return m.get(card)

# §4: columns D and H are the "seam columns" — the frontmost column of Third 1 and Third 3
# respectively, bordering Third 2. They still belong to their own Third for every other
# purpose, but a Third-2 (or matching Zone) card can also activate a unit standing there.
# Only Third 2's own Zone cards get this - Third 1/3's Zone cards already cover D/H
# natively, the same way Third-1/Third-3 do below. The lane itself doesn't need repeating
# here since it's already known from the card's own card_zones() entry.
SEAM_EXTRA = {
    'Zone-T2-Top': ('D', 'H'),
    'Zone-T2-Bottom': ('D', 'H'),
}

def card_options(s, side, card):
    """Returns (units, fallback) — units is the list of `side`'s units this card can
    activate right now (from which you then pick, per the card's own stated count —
    e.g. Tactical Free lets you pick any 2 of the returned units, not all of them).
    fallback=True means the card's zone was empty and this is one of the 5 fallback
    cards that lets you activate any 1 unit of your choice instead.

    The ball-carrier is always activatable (§6): whenever `side` currently holds the
    ball, the ball-carrying unit is appended to the result regardless of what the card
    would otherwise cover. This never applies on defense (only when `side` has the ball)."""
    pos = s['pos'][side]
    if card in FALLBACK_CARDS:
        t, ln = card_zones(card)
        hit = [u for u,h in pos.items() if B.zone(h)[0]==t and ln in B.zone(h)[1]]
        if card in SEAM_EXTRA:
            cols = SEAM_EXTRA[card]
            hit += [u for u,h in pos.items() if h[0] in cols and ln in B.lane(h[0],int(h[1:])) and u not in hit]
        if hit:
            units, fallback = hit, False
        else:
            units, fallback = list(pos.keys()), True  # fallback: any 1 of your choice
    elif card.startswith('Third-'):
        t = int(card.split('-')[1])
        units = [u for u,h in pos.items() if B.zone(h)[0]==t]
        if t == 2:
            units += [u for u,h in pos.items() if h[0] in ('D','H') and u not in units]
        fallback = False
    elif card.startswith('Lane-'):
        lane = card.split('-')[1]
        units, fallback = [u for u,h in pos.items() if lane in B.zone(h)[1]], False
    elif card == 'KeepersCall':
        # A sent-off Goalkeeper leaves nothing for this card to activate — return empty
        # rather than naming a unit that no longer exists (a real bug: previously always
        # returned ['GK'] regardless, silently wasting the card with no signal).
        units, fallback = (['GK'] if 'GK' in pos else []), False
    elif card in ('TacticalFree', 'FullPress'):
        units, fallback = list(pos.keys()), False
    else:
        units, fallback = [], False
    if s['ball']['side'] == side:
        carrier = s['ball']['unit']
        if carrier in pos and carrier not in units:
            units = units + [carrier]
    return units, fallback

def escape_hexes_free(s, carrier_side, carrier_hex):
    """§9's escape-hex rule: neighbors of the ball-carrier not occupied by anyone."""
    occ = occupied(s)
    return [h for h in B.neighbors(carrier_hex) if h not in occ]

def would_seal_last_gap(s, defending_side, carrier_side, carrier_hex, dest_hex):
    """True if defending_side moving a unit to dest_hex (adjacent to the carrier) would
    leave zero escape hexes — i.e. this specific move is illegal under the escape-hex rule."""
    if not B.adjacent(dest_hex, carrier_hex): return False
    free = escape_hexes_free(s, carrier_side, carrier_hex)
    return free == [dest_hex]  # dest_hex is currently the only open one

def show(s):
    """Quick human-readable dump of the current state, for sanity-checking mid-match."""
    print(f"=== Half {s['half']}  Turn {s['turn']}  Score A {s['score']['A']}-{s['score']['B']} B ===")
    for side in ('A','B'):
        units = ' '.join(f"{u}@{h}" for u,h in s['pos'][side].items())
        print(f" {side}: {units}")
        print(f"    cmd: {s['hand_cmd'][side]}  tac: {s['hand_tac'][side]}  flair={s['flair'][side]} debt={s['debt'][side]}")
    print(f" BALL: {s['ball']}")
