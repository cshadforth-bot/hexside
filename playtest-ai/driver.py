"""Hexside reference/test AI - plays a full match against itself using the real,
current canonical ruleset. This is NOT part of the rules engine (see ../engine/README.md
for that distinction) and it is NOT an opponent worth learning from - it's a simplified,
fairly mechanical heuristic player that exists to batch-test the engine and roster at
volume. A human (or an LLM) playing for real will find sharper lines than this driver
does, especially around the positional Tactic Cards (One-Two, Backheel, Long Ball) it
only reaches for in fairly narrow circumstances - see the "Implementation notes and
simplifications" section of /playtests/2026-09-08-batch-50-final-roster-all-tactic-cards.md
for the honest list of simplifications and known rarities.

Imports sim/board from ../engine by path (see the sys.path line below) rather than a
local copy, so this always plays against whatever is actually canonical - it can never
silently drift out of sync with a rule change the way a copied-and-forgotten scratch
driver would. Run it FROM THIS DIRECTORY (`python3 driver.py 50`), not from inside
engine/ - it writes batch_stats.json, game_random.json, and state.json next to wherever
it's invoked from, and those are per-run artifacts, not source (see ../engine/README.md
for the same reasoning about sim.py's own runtime files).

All 13 Tactic Cards are modeled:

  Through Ball  - pre-roll, skips a contested pass's roll if exactly one ZoC hex
                  contests the line (a simplification: "ignores ONE ZoC" is treated as
                  clearing the whole contest, exact when there's only one contesting
                  hex, which is the common case in this driver's play).
  Nutmeg        - post-roll Dribble Challenge reaction: >=1 Flair face in the
                  attacker's own roll wins outright. Needs the actual dice faces, so
                  Dribble Challenges go through dribble_contest() (calls sim.roll()
                  directly) instead of sim.contest(), matching the existing Composure
                  precedent of a direct post-roll sim.roll() call.
  Step-Over     - post-roll Dribble Challenge reaction: roll up to 2 more dice, add any
                  hits. Approximates "reroll 2 dice" as "roll 2 fresh dice and keep the
                  improvement" - the same simplification the existing Composure code
                  already uses for its own single-die reroll.
  Curl Shot     - pre-roll Shot bonus: +1 Attack die when shooting from the Top or
                  Bottom lane (board.lane()).
  Last Ditch Block - post-roll, OPPONENT'S reaction to a Shot or Pass their side is
                  about to lose: cancels one Success (ah -= 1, recheck win). Applied
                  after the shooting/passing side's own post-roll card (Composure) per
                  the rulebook's step 4 (active player) -> step 5 (opponent) order.
  One-Two       - free instant reposition to any open hex adjacent to an adjacent
                  teammate, uncontested, no Dribble Challenge - only played if it beats
                  the normal route already found.
  Backheel      - free pass to an adjacent teammate (still contested by ZoC like any
                  Pass, per the rulebook - only the Act cost is waived) - used as a
                  bail-out when the normal route is fully stuck, instead of holding.
  Long Ball     - pass to a teammate anywhere in the same lane, ignoring Pass Range and
                  intervening ZoC (destination's own ZoC still contests) - a "switch the
                  play" option, tried before falling back to a normal dribble-forward
                  move.
  Foul, Press, Composure, Strong Tackle, Jockey - implemented since earlier in the
                  project; unchanged here.

One-Two/Backheel/Long Ball needed genuinely new logic beyond the original driver -
previously it only ever passed at two trigger points (kickoff release, post-tackle
follow-up); it never modeled choosing to pass instead of dribble during a normal carry.
All three are gated on "beats the already-computed normal route" (One-Two, Long Ball) or
"normal route is fully stuck" (Backheel) - risk-aware, not reflexive. All 8 new cards are
deterministic-if-eligible-and-affordable (no random gating), matching the existing
Composure/Jockey precedent for mechanically optional cards; Foul and Press keep their
own probabilistic judgment-call gating, since those are genuine strategic choices rather
than always-correct-if-affordable plays.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'engine'))
import sim, board as B, random, json, sys

# Bounce pass mechanic (2026-09-16 design session, now printed rulebook §8): ported here
# from driver_base.py, where it was designed, verified against every hand-derived case,
# and tuned against real batches first - see [[project_hexside_bounce_pass_mechanic]] for
# that whole history, including why a flat rank_dist discount works for the teammate tier
# but the empty-hex tier needed a coin flip instead (measured a hard 100%/0% switch at any
# fixed value, not a gradient). Same two knobs, same calibrated values - nothing here is
# being re-tuned for Advanced Game specifically; this port assumes the same discount sizes
# translate, and a fresh n=1000 batch is how that assumption actually gets checked.
BOUNCE_RANK_BONUS = 2
BOUNCE_LOOSE_RANK_BONUS = 2

def run_match(match_no):
    sim.gen_random()
    s = sim.new_state()
    stats = dict(match=match_no, tackles=0, tackles_won=0, dribbles=0, dribbles_won=0,
                 shots=0, goals=0, goals_a=0, goals_b=0, discipline=0, yellows=0, reds=0,
                 fouls_played=0, press_played=0, composure_played=0, strongtackle_played=0,
                 jockey_played=0, throughball_played=0, nutmeg_played=0, stepover_played=0,
                 curlshot_played=0, onetwo_played=0, backheel_played=0, longball_played=0,
                 lastditch_played=0, plain_pass_played=0, clearance_played=0,
                 fullpress_played=0, fullpress_second_act=0, counter_played=0, overlap_played=0,
                 vision_played=0, clinical_played=0, shotstopper_played=0, lastman_played=0,
                 sinbin_trips=0, auto_goals=0, press_won=0, breakaway_shots=0, breakaway_goals=0,
                 bounce_attempts=0, bounce_pass_completed=0, bounce_loose=0, bounce_shots=0,
                 bounce_goals=0,
                 # Character-skin Signatures (hexside-character-cards.html), ported from
                 # driver_base.py 2026-09-17. Unlike that Base-only driver, showman_played
                 # is live here - Nutmeg/Step-Over are real Tactic-deck cards in Advanced.
                 immovable_played=0, playingout_played=0, playingout_yellow=0, nowaythrough_played=0,
                 readsthegame_played=0, marshalled_played=0, gasser_active=0,
                 onemorerun_played=0, seesred_played=0, showman_played=0,
                 outofnowhere_played=0, immovableobject_played=0,
                 # Main Character (Me!) redesigned 2026-09-21 - see driver_base.py's own
                 # note: the original "must Shoot when Through on Goal" restriction had
                 # nothing to restrict (no driver here offers a Pass-instead-of-Shot
                 # choice either). Replaced with "reroll ALL Blank dice on a Shot,
                 # once/match" - same mechanism as Clinical/Shot-Stopper, just sized up.
                 mainchar_played=0,
                 # 'GK' included since a Goalkeeper can reach a real Shot attempt via
                 # Playing Out - see driver_base.py's own note on the crash this fixed.
                 unit_shots={'SW':0,'WB':0,'PM':0,'PO':0,'GK':0}, unit_goals={'SW':0,'WB':0,'PM':0,'PO':0,'GK':0})
    breakaway = {'flag': False}
    full_press = {'active': False, 'start_unit': None}

    def att_end(side):
        own = 'A' if (side=='A')==s['a_defends_low'] else 'K'
        return 'K' if own=='A' else 'A'
    def def_end(side):
        return 'A' if (side=='A')==s['a_defends_low'] else 'K'
    def rank_dist(h, end):
        """Ranking distance-to-goal for hex comparisons (best move, best pass/kickoff
        target, etc.) - real B.shot_dist() where it's defined, else B.box_dist()+0.5
        (always worse than any hex WITH a real shot lane to the same end, since box_dist
        is exactly shot_dist-1 wherever both are defined), else a flat 999 for hexes with
        no line to goal at all. Every one of these callers used to either skip
        shot_dist()-undefined hexes outright or tie them all at one flat sentinel,
        silently falling back to dict/list iteration order among otherwise very different
        hexes - notably E3/E4/G3/G4, the board's most central and contested squares,
        which never have a defined shot_dist to either end (§4: the Net is only 3 hexes
        wide, so most hexes simply aren't on a straight line to it, even ones sitting
        close and square to the wider goal box). Only for ranking/movement choices -
        actual Shot legality still checks the real shot_dist()/srange, never this."""
        d = B.shot_dist(h, end)
        if d is not None:
            return d
        d2 = B.box_dist(h, end)
        if d2 is not None:
            return d2 + 0.5
        return 999
    def other(side):
        return 'B' if side=='A' else 'A'

    def can_afford(side, card):
        return card in s['hand_tac'][side] and s['flair'][side] >= sim.TACTIC_COST[card]

    def pay_and_discard(side, card):
        s['flair'][side] -= sim.TACTIC_COST[card]
        s['hand_tac'][side].remove(card)

    def find_card_for(side, unit):
        for c in s['hand_cmd'][side]:
            if c == 'Counter': continue
            units, fb = sim.card_options(s, side, c)
            if unit in units: return c
        return None

    def play_card(side, card, note):
        s['hand_cmd'][side].remove(card)
        s['log'].append(f"[{side} plays {card}] {note}")
        if card == 'FullPress':
            full_press['active'] = True
            stats['fullpress_played'] += 1
            s['debt'][side] += 2
            s['log'].append(f"  [{side} owes 2 discarded draws for Full Press (§6) - a second Act is now available this turn]")

    def zone_guard(def_side):
        for u in s['pos'][def_side]:
            if sim.is_goalkeeper_role(s, def_side, u):
                return u
        return None

    def dribble_contest(mover, atk_dice, opp, def_dice, label, showman_unit=None):
        """Dribble Challenge via direct sim.roll() (not sim.contest()) so Nutmeg can see
        the attacker's actual dice faces. Applies Nutmeg then Step-Over, both the ACTIVE
        player's own step-4 reactions - no opponent reaction card exists for a Dribble
        Challenge in this deck.

        `showman_unit`, added 2026-09-17 for the Magic character Signature: once/match,
        if the dribbling unit's own sig is 'showman', a Nutmeg or Step-Over IT plays
        this Challenge costs 1 less Flair (minimum 0) - the one Signature that couldn't
        be ported to driver_base.py at all, since Nutmeg/Step-Over are Tactic-deck
        cards Base Game never deals. Applied inline here rather than through
        can_afford/pay_and_discard (both keyed by side and a fixed sim.TACTIC_COST,
        with no per-unit or per-play discount concept) - a purely local, one-shot
        override rather than a shared-helper change that every other card type would
        also have to account for."""
        av, af, ah = sim.roll(s, mover, atk_dice, True)
        dv, df, dh = sim.roll(s, opp, def_dice, False)
        win = ah > dh
        line = (f"[{label}] {mover} rolls {av}->{af} ({ah} succ) | {opp} rolls {dv}->{df} "
                f"({dh} stop) => {'ATTACKER WINS' if win else 'DEFENDER HOLDS'}")
        s['log'].append(line); print(line)
        showman = (showman_unit is not None and sim.ROSTER[showman_unit].get('sig') == 'showman'
                   and not s.setdefault('showman_used', {'A':False,'B':False})[mover])
        nutmeg_cost = max(0, sim.TACTIC_COST['Nutmeg'] - (1 if showman else 0))
        stepover_cost = max(0, sim.TACTIC_COST['StepOver'] - (1 if showman else 0))
        if (not win and 'Nutmeg' in s['hand_tac'][mover] and s['flair'][mover] >= nutmeg_cost
                and 'flair' in af):
            s['flair'][mover] -= nutmeg_cost
            s['hand_tac'][mover].remove('Nutmeg')
            stats['nutmeg_played'] += 1
            win = True
            if showman:
                s['showman_used'][mover] = True
                stats['showman_played'] += 1
                line2 = f"  [{mover} {showman_unit} Showman - Nutmeg costs 1 less Flair, once per match]"
                s['log'].append(line2); print(line2)
            line2 = f"  [{mover} plays Nutmeg ({nutmeg_cost} Flair) - a Flair symbol wins the Dribble Challenge outright]"
            s['log'].append(line2); print(line2)
        elif not win and 'StepOver' in s['hand_tac'][mover] and s['flair'][mover] >= stepover_cost:
            s['flair'][mover] -= stepover_cost
            s['hand_tac'][mover].remove('StepOver')
            stats['stepover_played'] += 1
            k = min(2, atk_dice)
            rv, rf, rh = sim.roll(s, mover, k, True)
            ah += rh
            win = ah > dh
            if showman:
                s['showman_used'][mover] = True
                stats['showman_played'] += 1
                line2 = f"  [{mover} {showman_unit} Showman - Step-Over costs 1 less Flair, once per match]"
                s['log'].append(line2); print(line2)
            line2 = f"  [{mover} plays Step-Over ({stepover_cost} Flair) - rerolls {k} dice: {rv}->{rf} ({rh} succ)]"
            s['log'].append(line2); print(line2)
        return win, ah, dh

    def resolve_pass(mover, passer_unit, start, target, recv, path, contested, label_prefix):
        """Shared contested/uncontested Pass resolution, with Through Ball (pre-roll,
        active player) and Last Ditch Block (post-roll, opponent) layered on top of the
        normal Control-vs-Control contest. Returns True if the receiver ends up with the
        ball at `target`."""
        opp = other(mover)
        if contested and passer_unit == 'PM' and not s.setdefault('vision_used', {'A':False,'B':False})[mover]:
            s['vision_used'][mover] = True
            stats['vision_played'] += 1
            s['log'].append(f"  [{mover} PM Vision (§14) - ignores a defending Zone of Control, once per match, free]")
            contested = False
        elif contested and can_afford(mover, 'ThroughBall'):
            pay_and_discard(mover, 'ThroughBall')
            stats['throughball_played'] += 1
            s['log'].append(f"  [{mover} plays Through Ball (1 Flair) - ignores a defending Zone of Control]")
            contested = False
        if not contested:
            s['ball'] = {'side':mover,'unit':recv,'hex':target}
            return True
        defenders = [u for u,h in s['pos'][opp].items() if any(B.adjacent(h, ph) for ph in path[1:])] if path else \
                    [u for u,h in s['pos'][opp].items() if B.adjacent(h, target)]
        def_unit = max(defenders, key=lambda u: sim.ROSTER[u]['control']) if defenders else None
        def_control = sim.ROSTER[def_unit]['control'] if def_unit else 2
        def_control = maybe_counter_die(opp, def_control)
        win, ah, dh = sim.contest(s, mover, sim.ROSTER[passer_unit]['control'], opp, def_control,
                                   label=f"{label_prefix}: {mover} {passer_unit} {start}->{target} to {recv}")
        if win and def_unit and can_afford(opp, 'LastDitchBlock'):
            pay_and_discard(opp, 'LastDitchBlock')
            stats['lastditch_played'] += 1
            ah -= 1
            win = ah > dh
            s['log'].append(f"  [{opp} plays Last Ditch Block (2 Flair) - cancels one Success from the Pass]")
        if win:
            s['ball'] = {'side':mover,'unit':recv,'hex':target}
            return True
        else:
            if def_unit is None: def_unit = next(iter(s['pos'][opp]))
            def_hex = s['pos'][opp][def_unit]
            s['ball'] = {'side':opp,'unit':def_unit,'hex':def_hex}
            return False

    def resolve_clearance(mover, passer_unit, start, target, path, contested):
        """Like resolve_pass, but for a Clearance to an empty hex (§7: a Pass may target
        a teammate OR any empty hex within Pass Range) - on success the ball goes loose
        at `target`, not to a teammate."""
        opp = other(mover)
        if contested and passer_unit == 'PM' and not s.setdefault('vision_used', {'A':False,'B':False})[mover]:
            s['vision_used'][mover] = True
            stats['vision_played'] += 1
            s['log'].append(f"  [{mover} PM Vision (§14) - ignores a defending Zone of Control, once per match, free]")
            contested = False
        elif contested and can_afford(mover, 'ThroughBall'):
            pay_and_discard(mover, 'ThroughBall')
            stats['throughball_played'] += 1
            s['log'].append(f"  [{mover} plays Through Ball (1 Flair) - ignores a defending Zone of Control]")
            contested = False
        if not contested:
            s['ball'] = {'side':None,'unit':None,'hex':target}
            return True
        defenders = [u for u,h in s['pos'][opp].items() if any(B.adjacent(h, ph) for ph in path[1:])] if path else \
                    [u for u,h in s['pos'][opp].items() if B.adjacent(h, target)]
        def_unit = max(defenders, key=lambda u: sim.ROSTER[u]['control']) if defenders else None
        def_control = sim.ROSTER[def_unit]['control'] if def_unit else 2
        def_control = maybe_counter_die(opp, def_control)
        win, ah, dh = sim.contest(s, mover, sim.ROSTER[passer_unit]['control'], opp, def_control,
                                   label=f"Clearance: {mover} {passer_unit} {start}->{target}")
        if win and def_unit and can_afford(opp, 'LastDitchBlock'):
            pay_and_discard(opp, 'LastDitchBlock')
            stats['lastditch_played'] += 1
            ah -= 1
            win = ah > dh
            s['log'].append(f"  [{opp} plays Last Ditch Block (2 Flair) - cancels one Success from the Clearance]")
        if win:
            s['ball'] = {'side':None,'unit':None,'hex':target}
            return True
        else:
            if def_unit is None: def_unit = next(iter(s['pos'][opp]))
            def_hex = s['pos'][opp][def_unit]
            s['ball'] = {'side':opp,'unit':def_unit,'hex':def_hex}
            return False

    def do_tackle(atk_side, atk_unit, def_side, label, use_strong_chance=0.4):
        stats['tackles'] += 1
        carrier = s['ball']['unit']
        def_control = maybe_counter_die(def_side, sim.ROSTER[carrier]['control'])

        if (sim.ROSTER[carrier].get('sig') == 'immovable_object'
                and not s.setdefault('immovableobject_used', {'A':False,'B':False})[def_side]):
            # Immovable Object (The Wardrobe): once/match, when this unit is the ball-
            # carrying target of a Tackle Challenge, +1 Defense die - approximates
            # "cancel one attacker Success" as "add one Stop" (contest() doesn't expose
            # raw dice back to callers), same shape as Counter's own die-bonus option.
            s['immovableobject_used'][def_side] = True
            stats['immovableobject_played'] += 1
            s['log'].append(f"  [{def_side} {carrier} Immovable Object - +1 Defense die on this Tackle Challenge, once per match]")
            def_control += 1

        atk_sig = sim.ROSTER[atk_unit].get('sig')
        if (atk_sig == 'no_way_through'
                and not s.setdefault('nowaythrough_used', {'A':False,'B':False})[atk_side]):
            # No Way Through (Big Dave): once/match, automatic win, no roll - still
            # draws Discipline TWICE regardless, applying both (identical to a LOST
            # Strong Tackle's penalty, per the card's own text).
            s['nowaythrough_used'][atk_side] = True
            stats['nowaythrough_played'] += 1
            s['log'].append(f"  [{atk_side} {atk_unit} No Way Through - automatic Tackle win, once per match]")
            before = s['p_disc']
            for _ in range(2):
                card = sim.draw_disc(s)
                sim.apply_discipline(s, atk_side, atk_unit, card)
            stats['discipline'] += (s['p_disc'] - before)
            for l in s['log'][-8:]:
                if 'YELLOW CARD' in l: stats['yellows'] += 1
                if 'RED CARD' in l or '2nd Yellow -> RED' in l: stats['reds'] += 1
                if 'sent to the sin-bin' in l: stats['sinbin_trips'] += 1
            stats['tackles_won'] += 1
            return True

        use_strong = 'StrongTackle' in s['hand_tac'][atk_side] and random.random() < use_strong_chance
        sees_red = (atk_sig == 'sees_red' and not use_strong
                    and not s.setdefault('seesred_used', {'A':False,'B':False})[atk_side])
        if sees_red:
            # Sees Red (Roy): once/match, mechanically IDENTICAL to Strong Tackle (+1
            # Attack die, double Discipline draw on a loss) - but reimplemented here
            # directly via sim.contest() rather than calling sim.strong_tackle() itself
            # (unlike driver_base.py's own port of this Signature): that function's
            # ONLY hand-touching line is `hand_tac[atk_side].remove('StrongTackle')`,
            # and unlike driver_base.py (hand_tac always empty there), this driver can
            # genuinely already hold a real StrongTackle card - temporarily injecting a
            # fake one to satisfy that .remove() risks leaving a duplicate behind if the
            # side already had a real one this exact Tackle (use_strong came out False
            # on the dice-roll gate even though the card was available), handing them a
            # free extra use of their own real card later. Only the roll+double-draw
            # logic is reused; the card economy is left alone entirely.
            s['seesred_used'][atk_side] = True
            stats['seesred_played'] += 1
            s['log'].append(f"  [{atk_side} {atk_unit} Sees Red - +1 Attack die on this Tackle Challenge, once per match]")
            before = s['p_disc']
            win, ah, dh = sim.contest(s, atk_side, sim.ROSTER[atk_unit]['tackle'] + 1, def_side, def_control,
                                       label + ' (Sees Red, +1 die)', is_tackle=True)
            if not win:
                for _ in range(2):
                    card = sim.draw_disc(s)
                    sim.apply_discipline(s, atk_side, atk_unit, card)
            stats['discipline'] += (s['p_disc'] - before)
        elif use_strong:
            stats['strongtackle_played'] += 1
            before = s['p_disc']
            win, ah, dh = sim.strong_tackle(s, atk_side, atk_unit, def_side, sim.ROSTER[atk_unit]['tackle'],
                                            def_control, label=label)
            stats['discipline'] += (s['p_disc'] - before)
        else:
            before = s['p_disc']
            win, ah, dh = sim.tackle(s, atk_side, atk_unit, def_side, sim.ROSTER[atk_unit]['tackle'],
                                      def_control, label=label)
            stats['discipline'] += (s['p_disc'] - before)
        if win: stats['tackles_won'] += 1
        for l in s['log'][-5:]:
            if 'YELLOW CARD' in l: stats['yellows'] += 1
            if 'RED CARD' in l or '2nd Yellow -> RED' in l: stats['reds'] += 1
            if 'sent to the sin-bin' in l: stats['sinbin_trips'] += 1
        return win

    def maybe_counter_die(defending_side, base_dice):
        """Counter's "add 1 Defense die" option (§10): a held Counter, discarded before
        the roll, adds 1 die to whatever the defending side is about to roll - the
        simpler of Counter's two options, and the one this driver models. The other
        option (discard to force an immediate Tackle Challenge, which can cancel the
        original action outright if it wins) isn't modeled - it needs its own nested
        Resolution Sequence plus a judgment call about when interrupting the opponent is
        worth spending a scarce card on, neither of which this driver attempts. Spent
        immediately whenever held and eligible, matching every other mechanically-
        optional card here (Composure, Jockey, Nutmeg, Step-Over) rather than judged
        case by case - Foul and Press are the only cards in this driver treated as
        genuine strategic yes/no calls. This is every contested roll's entry point for
        Counter: Pass, Clearance, Dribble Challenge, Tackle, and Shot vs. Save all funnel
        through here, since Counter can answer any of them (§10's "whatever roll is
        about to happen")."""
        if 'Counter' not in s['hand_cmd'][defending_side]:
            return base_dice
        s['hand_cmd'][defending_side].remove('Counter')
        stats['counter_played'] += 1
        s['log'].append(f"  [{defending_side} discards a Counter (§10) - adds 1 Defense die to the incoming roll]")
        return base_dice + 1

    def maybe_play_foul(defending_side, carrier_hex):
        if 'Foul' not in s['hand_tac'][defending_side]:
            return False
        adjacent = [u for u,h in s['pos'][defending_side].items() if B.adjacent(h, carrier_hex)]
        if not adjacent:
            return False
        if random.random() > 0.45:
            return False
        fouling_unit = adjacent[0]
        s['hand_tac'][defending_side].remove('Foul')
        s['log'].append(f"  [{defending_side} plays Foul (free) - {fouling_unit} instantly stops the action in progress]")
        stats['fouls_played'] += 1
        before = s['p_disc']
        card = sim.draw_disc_foul(s)
        sim.apply_discipline(s, defending_side, fouling_unit, card)
        stats['discipline'] += (s['p_disc'] - before)
        for l in s['log'][-4:]:
            if 'YELLOW CARD' in l: stats['yellows'] += 1
            if 'RED CARD' in l or '2nd Yellow -> RED' in l: stats['reds'] += 1
            if 'sent to the sin-bin' in l: stats['sinbin_trips'] += 1
        return True

    def maybe_play_press(attacking_side):
        d = other(attacking_side)
        if 'Press' not in s['hand_tac'][d] or s['flair'][d] < 1:
            return False
        if s['ball']['side'] != attacking_side:
            return False
        carrier = s['ball']['unit']
        carrier_hex = s['pos'][attacking_side][carrier]
        defenders = [u for u,h in s['pos'][d].items() if B.adjacent(h, carrier_hex)]
        if not defenders:
            return False
        if random.random() > 0.5:
            return False
        def_unit = max(defenders, key=lambda u: sim.ROSTER[u]['tackle'])
        s['hand_tac'][d].remove('Press')
        s['flair'][d] -= 1
        s['log'].append(f"  [{d} plays Press (1 Flair) - forces a Tackle Challenge using {def_unit}]")
        stats['press_played'] += 1
        win = do_tackle(d, def_unit, attacking_side,
                         label=f"Press-forced Tackle: {d} {def_unit} vs {attacking_side} {carrier}",
                         use_strong_chance=0.0)
        if win:
            stats['press_won'] += 1
            tackler_hex = s['pos'][d].get(def_unit)
            if tackler_hex:
                s['ball'] = {'side':d,'unit':def_unit,'hex':tackler_hex}
                s['log'].append(f"  [{d} {def_unit} wins the Press tackle - ball moves to {tackler_hex}]")
                sim.check_no_overlap(s)
                free_followup_pass_after_tackle(d, def_unit)
            return True
        return False

    def try_jockey(mover, carrier_unit, carrier_hex):
        d = other(mover)
        if 'Jockey' not in s['hand_tac'][d] or s['flair'][d] < 1:
            return False
        if not any(B.adjacent(h, carrier_hex) for h in s['pos'][d].values()):
            return False
        full_reach = sim.legal_reach(s, mover, carrier_unit)
        srange = sim.ROSTER[carrier_unit]['srange']
        end = att_end(mover)
        threatens = srange is not None and any(
            B.shot_dist(h, end) is not None and B.shot_dist(h, end) <= srange for h in full_reach)
        if not threatens:
            return False
        sim.play_jockey(s, d, None)
        stats['jockey_played'] += 1
        return True

    def try_one_two(mover, carrier, start):
        if not can_afford(mover, 'OneTwo'):
            return None
        end = att_end(mover)
        teammates = [(u,h) for u,h in s['pos'][mover].items() if u != carrier and B.adjacent(h, start)]
        best = None
        for u, h in teammates:
            for n in B.neighbors(h):
                if n == start or n in sim.occupied(s):
                    continue
                d = rank_dist(n, end)
                if best is None or d < best[1]:
                    best = (n, d)
        return best  # (new_hex, new_d) or None

    def try_long_ball(mover, carrier, start):
        if not can_afford(mover, 'LongBall'):
            return None
        end = att_end(mover)
        col0, row0 = B.parse(start)
        my_lanes = set(B.lane(col0, row0))
        best = None
        for u, h in s['pos'][mover].items():
            if u == carrier: continue
            col, row = B.parse(h)
            if not my_lanes & set(B.lane(col, row)):
                continue
            d = rank_dist(h, end)
            if best is None or d < best[2]:
                best = (u, h, d)
        return best  # (unit, hex, d) or None

    def try_backheel(mover, carrier, start):
        if not can_afford(mover, 'Backheel'):
            return None
        end = att_end(mover)
        teammates = [(u,h) for u,h in s['pos'][mover].items() if u != carrier and B.adjacent(h, start)]
        if not teammates:
            return None
        teammates.sort(key=lambda t: rank_dist(t[1], end))
        return teammates[0]  # (unit, hex)

    def _all_hexes():
        return [f"{c}{r}" for c in B.COLS for r in range(B.min_row(c), B.max_row(c)+1)]

    def try_plain_pass_or_clearance(mover, carrier, start):
        """§7's plain Pass - to a teammate, or to an empty hex (a Clearance) - within
        Pass Range. Unlike One-Two/Backheel/Long Ball this is NOT a Tactic Card, so it's
        always available (no hand, no Flair) once the carrier is activated at all - the
        correct last resort when nothing else improves position. This specifically
        fixes a real batch finding: a confined goalkeeper's own best_hex always equals
        its start hex (it can never leave its zone to "advance"), so without this
        fallback it just holds the ball indefinitely turn after turn, since the three
        Tactic Card options above are never available in the Base Game and only
        conditionally available even in the Advanced Game - the same gap applies to any
        other unit that happens to have no better move and no Tactic Card in hand.

        2026-09-16 (ported from driver_base.py): a bounce-pass-to-teammate (or
        -to-empty-hex) now competes directly in this same candidate pool. A
        teammate-reaching option (straight or bounced) always beats every empty-hex
        option (straight or bounced), unchanged from before. Within a tier, a bounce
        candidate's rank_dist() is discounted by BOUNCE_RANK_BONUS before sorting - a
        straight Pass can aim at any teammate on 4 axes while a bounce is locked to one of
        8 fixed lines, so a fair (undiscounted) comparison loses to a straight pass almost
        every time; the discount stands in for the trick-play value rank_dist alone can't
        see. The empty-hex tier uses a coin flip instead of a flat discount for the same
        reason it did in driver_base.py - measured there that a fixed value is a hard
        switch (100%/0% either way), not a dial, because plain Clearance and bounce-loose
        are almost always tied or ~1 apart in real positions.

        Returns (kind, target, recv, path, bounce) - kind is 'pass' or 'clear'; `bounce`
        is None for a normal straight-line option (caller resolves it exactly as before,
        via resolve_pass/resolve_clearance) or the sim.bounce_pass_options() entry it came
        from otherwise (caller resolves it very differently - no ZoC contest, since a
        bounce's path is fixed the instant it's declared, not freely aimed the way a
        straight Pass's is). Returns None if truly nothing is reachable at all, by either
        route."""
        end = att_end(mover)
        prange = sim.ROSTER[carrier]['prange']
        teammates = [(u,h) for u,h in s['pos'][mover].items() if u != carrier]
        bounce_opts = sim.bounce_pass_options(s, mover, carrier)
        candidates = []
        for u,h in teammates:
            d, path = B.straight_line(start, h)
            if d is not None and d <= prange:
                candidates.append((h, u, path, None))
        for opt in bounce_opts:
            if opt['kind'] == 'teammate':
                recv = next(u for u,h in s['pos'][mover].items() if h == opt['end_hex'])
                candidates.append((opt['end_hex'], recv, None, opt))
        if candidates:
            candidates.sort(key=lambda c: rank_dist(c[0], end) - (BOUNCE_RANK_BONUS if c[3] is not None else 0))
            target, recv, path, bounce = candidates[0]
            return ('pass', target, recv, path, bounce)
        occ = sim.occupied(s)
        clear_candidates = []
        for h in _all_hexes():
            if h == start or h in occ:
                continue
            d, path = B.straight_line(start, h)
            if d is not None and d <= prange:
                clear_candidates.append((h, path, None))
        for opt in bounce_opts:
            if opt['kind'] == 'loose':
                clear_candidates.append((opt['end_hex'], None, opt))
        if not clear_candidates:
            return None
        # Measured directly in driver_base.py: a fixed discount here is a hard switch, not
        # a dial - plain Clearance and bounce-loose are almost always tied or a hair apart
        # in real positions, so a coin flip on whether the discount applies at all is what
        # actually keeps both in play, rather than hunting for a deterministic threshold
        # that doesn't exist for this comparison. See [[project_hexside_bounce_pass_mechanic]].
        loose_bonus = BOUNCE_LOOSE_RANK_BONUS if random.random() < 0.5 else 0
        clear_candidates.sort(key=lambda c: rank_dist(c[0], end) - (loose_bonus if c[2] is not None else 0))
        target, path, bounce = clear_candidates[0]
        return ('clear', target, None, path, bounce)

    def dynamic_followup_move(mover, unit, reason):
        start = s['pos'][mover][unit]
        end = att_end(mover)
        reach = sim.legal_reach(s, mover, unit)
        best_hex, best_d = start, rank_dist(start, end)
        for h,(cost,path) in reach.items():
            d = rank_dist(h, end)
            if d < best_d: best_d, best_hex = d, h
        if best_hex == start:
            return
        path = reach[best_hex][1]
        zoc = sim.enemy_zoc(s, mover)
        contested_hex = next((h for h in path[1:] if h in zoc), None)
        if contested_hex is None:
            s['pos'][mover][unit] = best_hex
            s['ball'] = {'side':mover,'unit':unit,'hex':best_hex}
            return
        idx = path.index(contested_hex)
        prev_hex = path[idx-1]
        if maybe_play_foul(other(mover), prev_hex):
            s['pos'][mover][unit] = prev_hex
            s['ball'] = {'side':None,'unit':None,'hex':prev_hex}
            return
        stats['dribbles'] += 1
        defenders = [u for u,h in s['pos'][other(mover)].items() if B.adjacent(h, contested_hex)]
        def_unit = max(defenders, key=lambda u: sim.ROSTER[u]['tackle']) if defenders else None
        def_tackle = sim.ROSTER[def_unit]['tackle'] if def_unit else 2
        def_tackle = maybe_counter_die(other(mover), def_tackle)
        win, ah, dh = dribble_contest(mover, sim.ROSTER[unit]['control'], other(mover), def_tackle,
                                       label=f"Dribble Challenge (dynamic move): {mover} {unit} through {other(mover)} ZoC at {contested_hex}",
                                       showman_unit=unit)
        if win:
            stats['dribbles_won'] += 1
            s['pos'][mover][unit] = best_hex
            s['ball'] = {'side':mover,'unit':unit,'hex':best_hex}
        else:
            s['pos'][mover][unit] = contested_hex
            s['ball'] = {'side':None,'unit':None,'hex':prev_hex}
        sim.check_no_overlap(s)

    def followup_move_then_maybe_shoot(mover, unit, reason):
        """Wraps dynamic_followup_move with Full Press's second Act (§6): "a unit that
        only starts carrying the ball because the first one's Act just passed it there
        still qualifies for the second (a deliberate Pass-then-Shot... combo)". Checked
        after the move resolves, not before, since a contested Dribble Challenge along
        the way can still lose the ball - only a genuinely NEW carrier who still has the
        ball afterward gets the extra Shot; the unit that started the turn with the ball
        never does, since that would just be one unit acting twice, not two different
        ones (§6's own wording)."""
        dynamic_followup_move(mover, unit, reason)
        if (full_press['active'] and unit != full_press['start_unit']
                and s['ball']['side'] == mover and s['ball']['unit'] == unit):
            stats['fullpress_second_act'] += 1
            s['log'].append(f"  [{mover} {unit} takes Full Press's second Act (§6) - attempts a Shot]")
            attempt_shot(mover)

    def handle_kickoff_release(mover, carrier):
        start = s['pos'][mover][carrier]
        prange = sim.ROSTER[carrier]['prange']
        end = att_end(mover)
        teammates = [(u,h) for u,h in s['pos'][mover].items() if u != carrier]
        candidates = []
        for u,h in teammates:
            d, path = B.straight_line(start, h)
            if d is not None and d <= prange:
                candidates.append((d, h, u, path))
        if not candidates:
            # Shouldn't be reachable under the canonical draft: sim.formation() now
            # guarantees the kicking side's first free placement lands within the
            # taker's own Pass Range (§5), specifically so this is never empty. Still no
            # fallback if it ever is, though - the obligation never clears, so this side's
            # turns go blank for the rest of the half. A scratch experiment that swapped
            # in a placement policy bypassing formation()'s must_reach guarantee (testing
            # pure-random setup) hit exactly this and deadlocked entire matches. Any future
            # caller that supplies its own hex-choice function needs to respect must_reach
            # too, or add a real bailout here - don't assume this branch stays dead.
            return False
        candidates.sort(key=lambda c: rank_dist(c[1], end))
        d, target, recv, path = candidates[0]
        card = find_card_for(mover, carrier)
        if card is None:
            return False
        play_card(mover, card, f"activates {carrier}")
        if maybe_play_foul(other(mover), start):
            sim.release_kickoff(s, mover, carrier)
            s['ball'] = {'side':None,'unit':None,'hex':start}
            return True
        zoc = sim.enemy_zoc(s, mover)
        contested = (any(h in zoc for h in path[1:]) if path else (target in zoc))
        receiver_gets_ball = resolve_pass(mover, carrier, start, target, recv, path, contested,
                                           "Kickoff release - Pass")
        sim.release_kickoff(s, mover, carrier)
        sim.check_no_overlap(s)
        if receiver_gets_ball:
            followup_move_then_maybe_shoot(mover, recv, "kickoff release pass landed")
        return True

    def try_reads_game(mover, carrier_unit, carrier_hex):
        d = other(mover)
        sw_hex = s['pos'][d].get('SW')
        if (sw_hex is None or sim.ROSTER['SW'].get('sig') != 'reads_the_game'
                or not B.adjacent(sw_hex, carrier_hex)
                or s.setdefault('readsthegame_used', {'A':False,'B':False})[d]):
            return False
        # Reads the Game (Uncle Barry): once/match, the instant an adjacent opposing
        # unit is activated to move, -1 Pace for that move only - a free Jockey (no
        # Flair, no card), own separate once-per-match budget from Jockey's.
        s['readsthegame_used'][d] = True
        stats['readsthegame_played'] += 1
        s['log'].append(f"  [{d} SW Reads the Game - {mover} {carrier_unit}'s Pace reduced by 1 for this move, once per match]")
        return True

    def move_ball_carrier(mover):
        carrier = s['ball']['unit']
        start = s['pos'][mover][carrier]
        opp = other(mover)
        wb_hex = s['pos'][opp].get('WB')
        if (wb_hex is not None and B.adjacent(wb_hex, start)
                and sim.ROSTER['WB'].get('sig') == 'last_man'
                and not s.setdefault('lastman_used', {'A':False,'B':False})[opp]):
            # Last Man (§14): once per match, WB forces a free Tackle Challenge against
            # an adjacent ball-carrier, without spending a Counter card - "timed exactly
            # like a Counter's forced-Tackle option" (§10, Resolution Sequence step 2),
            # i.e. checked before the carrier's own move/Dribble Challenge even begins.
            # Scoped to this one trigger point (the ball-carrier's own movement decision)
            # rather than every Resolution Sequence window a real table would also cover
            # (a declared Pass or Shot) - the same simplification this driver already
            # makes for Counter's own forced-Tackle option, left unmodeled there.
            s['lastman_used'][opp] = True
            stats['lastman_played'] += 1
            s['log'].append(f"  [{opp} WB Last Man (§14) - forces a free Tackle Challenge against {mover} {carrier} at {start}, once per match]")
            win = do_tackle(opp, 'WB', mover, label=f"Last Man: {opp} WB vs {mover} {carrier} at {start}")
            if win:
                s['ball'] = {'side':opp,'unit':'WB','hex':wb_hex}
                sim.check_no_overlap(s)
                free_followup_pass_after_tackle(opp, 'WB')
                return
            sim.check_no_overlap(s)
        end = att_end(mover)
        jockeyed = try_jockey(mover, carrier, start)
        reads_game = try_reads_game(mover, carrier, start)
        gasser = (s['half'] == 2 and sim.ROSTER[carrier].get('sig') == 'gasser')
        if gasser:
            # Gasser (The Engine): passive, always-on from the start of the second half.
            stats['gasser_active'] += 1
        knee_debuffed = (sim.ROSTER[carrier].get('sig') == 'one_more_run'
                          and s.setdefault('onemorerun_half_debuff', {'A':None,'B':None})[mover] == s['half'])
        pace_mod = ((-1 if jockeyed else 0) + (-1 if reads_game else 0) + (-1 if gasser else 0)
                    + (-1 if knee_debuffed else 0))
        playing_out_move = (sim.ROSTER[carrier].get('sig') == 'playing_out'
                             and not s.setdefault('playingout_used', {'A':False,'B':False})[mover])
        if playing_out_move:
            # Playing Out (Sunday Ederson): ported from driver_base.py 2026-09-17,
            # including its own corrected return timescale - see play_turn's own
            # comment for the return side (a Pace-limited attempt next turn, or a
            # guaranteed Yellow Card).
            s['playingout_used'][mover] = True
            s['playingout_this_turn'][mover] = True
            s.setdefault('playingout_pending_return', {'A':False,'B':False})[mover] = True
            stats['playingout_played'] += 1
            s['log'].append(f"  [{mover} GK Playing Out - acts as a normal outfield unit for this activation, once per match - must return to its zone at the start of {mover}'s next turn]")
        reach = sim.legal_reach(s, mover, carrier, extra_pace=pace_mod, ignore_zone_lock=playing_out_move)
        best_hex, best_d = start, rank_dist(start, end)
        for h,(cost,path) in reach.items():
            d = rank_dist(h, end)
            if d < best_d: best_d, best_hex = d, h

        card = find_card_for(mover, carrier)
        if card is None:
            if best_hex == start:
                s['log'].append(f"  [{mover} {carrier} holds at {start} (rank_dist {best_d}), no better advance found]")
            return

        if (carrier == 'SW' and sim.ROSTER['SW'].get('sig') == 'marshalled'
                and not s.setdefault('marshalled_used', {'A':False,'B':False})[mover]):
            # Marshalled (Gaffer): once/match, reuses Full Press's own existing bonus-
            # Act mechanism - see driver_base.py's own comment for why.
            s['marshalled_used'][mover] = True
            stats['marshalled_played'] += 1
            s['log'].append(f"  [{mover} SW Marshalled - one teammate may act as though also activated this turn, once per match]")
            full_press['active'] = True
            full_press['start_unit'] = carrier

        if carrier == 'SW' and sim.ROSTER['SW'].get('sig') == 'overlap' and (card.startswith('Lane-') or card.startswith('Third-')):
            # Overlap (§14): +1 Pace, but only if the extra hex lands in Third 2 (the
            # user's deliberate rework of the rulebook's original "attacking third" text
            # - a supporting run into midfield, not a run all the way into the scoring
            # zone). Checked fresh every eligible turn (once per turn, not once per
            # match, per explicit instruction), so it can fire repeatedly across a
            # match. Only overrides best_hex if it's a genuine improvement AND lands in
            # Third 2 specifically - overshooting into Third 3 means Sweeper "checks
            # itself" and the normal route is used instead, unmodified.
            overlap_reach = sim.legal_reach(s, mover, carrier, extra_pace=pace_mod + 1)
            overlap_best_hex, overlap_best_d = best_hex, best_d
            for h,(cost,path) in overlap_reach.items():
                if B.third(B.parse(h)[0]) != 2:
                    continue
                d = rank_dist(h, end)
                if d < overlap_best_d:
                    overlap_best_d, overlap_best_hex = d, h
            if overlap_best_hex != best_hex:
                stats['overlap_played'] += 1
                s['log'].append(f"  [{mover} {carrier} Overlap (§14) - the extra hex reaches {overlap_best_hex}, Third 2]")
                best_hex, best_d, reach = overlap_best_hex, overlap_best_d, overlap_reach

        one_two = try_one_two(mover, carrier, start)
        if one_two is not None and one_two[1] < best_d:
            new_hex, new_d = one_two
            play_card(mover, card, f"activates {carrier}")
            pay_and_discard(mover, 'OneTwo')
            stats['onetwo_played'] += 1
            s['log'].append(f"  [{mover} {carrier} plays One-Two (1 Flair) - instant give-and-go, ends up at {new_hex}]")
            s['pos'][mover][carrier] = new_hex
            s['ball'] = {'side':mover,'unit':carrier,'hex':new_hex}
            sim.check_no_overlap(s)
            return

        long_ball = try_long_ball(mover, carrier, start)
        if long_ball is not None and long_ball[2] < best_d:
            recv, target, new_d = long_ball
            play_card(mover, card, f"activates {carrier}")
            pay_and_discard(mover, 'LongBall')
            stats['longball_played'] += 1
            s['log'].append(f"  [{mover} {carrier} plays Long Ball (2 Flair) - switches play to {recv} at {target}]")
            zoc = sim.enemy_zoc(s, mover)
            landed = resolve_pass(mover, carrier, start, target, recv, None, target in zoc, "Long Ball")
            sim.check_no_overlap(s)
            if landed:
                followup_move_then_maybe_shoot(mover, recv, "Long Ball landed")
            return

        if best_hex == start:
            bh = try_backheel(mover, carrier, start)
            if bh is not None:
                recv, target = bh
                play_card(mover, card, f"activates {carrier}")
                pay_and_discard(mover, 'Backheel')
                stats['backheel_played'] += 1
                s['log'].append(f"  [{mover} {carrier} plays Backheel (1 Flair) - free pass to {recv} at {target}]")
                zoc = sim.enemy_zoc(s, mover)
                landed = resolve_pass(mover, carrier, start, target, recv, None, target in zoc, "Backheel")
                sim.check_no_overlap(s)
                if landed:
                    followup_move_then_maybe_shoot(mover, recv, "Backheel landed")
                return
            srange = sim.ROSTER[carrier]['srange']
            has_shot = srange is not None and best_d <= srange
            # Bounce-to-goal is checked first, unconditionally - a bonus scoring chance
            # the direct-Shot check just missed, same priority tier as has_shot itself.
            # Bounce-to-teammate/loose is NOT checked separately here - it's folded into
            # try_plain_pass_or_clearance itself, competing directly against the
            # straight-line options there. See driver_base.py / [[project_hexside_bounce_pass_mechanic]].
            if not has_shot and try_bounce_shot(mover, carrier, start):
                play_card(mover, card, f"activates {carrier}")
                return
            bail = None if has_shot else try_plain_pass_or_clearance(mover, carrier, start)
            if bail is not None:
                kind, target, recv, path, bounce = bail
                play_card(mover, card, f"activates {carrier}")
                if bounce is not None:
                    resolve_bounce_completion(mover, carrier, start, kind, target, recv)
                    return
                zoc = sim.enemy_zoc(s, mover)
                contested = target in zoc
                if kind == 'pass':
                    stats['plain_pass_played'] += 1
                    s['log'].append(f"  [{mover} {carrier} plays a plain Pass to {recv} at {target} (no better advance)]")
                    landed = resolve_pass(mover, carrier, start, target, recv, path, contested, "Pass")
                    sim.check_no_overlap(s)
                    if landed:
                        followup_move_then_maybe_shoot(mover, recv, "Pass landed")
                else:
                    stats['clearance_played'] += 1
                    s['log'].append(f"  [{mover} {carrier} clears the ball to {target} (no better advance)]")
                    resolve_clearance(mover, carrier, start, target, path, contested)
                    sim.check_no_overlap(s)
                return
            s['log'].append(f"  [{mover} {carrier} holds at {start} (rank_dist {best_d}), no better advance found]")
            return

        path = reach[best_hex][1]
        zoc = sim.enemy_zoc(s, mover)
        contested_hex = next((h for h in path[1:] if h in zoc), None)
        carrier_sig = sim.ROSTER[carrier].get('sig')
        if (contested_hex is not None and carrier_sig in ('one_more_run', 'out_of_nowhere')
                and not s.setdefault('bigmove_used', {'A':False,'B':False})[mover]):
            # One More Run (Dodgy Knee) / Out of Nowhere (Flash): once/match, ignores
            # the opposing Zone of Control entirely - only spends the charge when there
            # was actually a ZoC to bypass. Ported from driver_base.py.
            s['bigmove_used'][mover] = True
            contested_hex = None
            if carrier_sig == 'one_more_run':
                stats['onemorerun_played'] += 1
                s['log'].append(f"  [{mover} {carrier} One More Run - ignores the Zone of Control, once per match]")
                s.setdefault('onemorerun_half_debuff', {'A':None,'B':None})[mover] = s['half']
            else:
                stats['outofnowhere_played'] += 1
                s['log'].append(f"  [{mover} {carrier} Out of Nowhere - ignores the Zone of Control, once per match, no Shot this activation]")
                s.setdefault('outofnowhere_no_shot', {'A':False,'B':False})[mover] = True
        play_card(mover, card, f"activates {carrier}")
        if contested_hex is None:
            s['pos'][mover][carrier] = best_hex
            s['ball'] = {'side':mover,'unit':carrier,'hex':best_hex}
            return
        idx = path.index(contested_hex)
        prev_hex = path[idx-1]
        if maybe_play_foul(other(mover), prev_hex):
            s['pos'][mover][carrier] = prev_hex
            s['ball'] = {'side':None,'unit':None,'hex':prev_hex}
            sim.check_no_overlap(s)
            return
        stats['dribbles'] += 1
        defenders = [u for u,h in s['pos'][other(mover)].items() if B.adjacent(h, contested_hex)]
        def_unit = max(defenders, key=lambda u: sim.ROSTER[u]['tackle']) if defenders else None
        def_tackle = sim.ROSTER[def_unit]['tackle'] if def_unit else 2
        def_tackle = maybe_counter_die(other(mover), def_tackle)
        win, ah, dh = dribble_contest(mover, sim.ROSTER[carrier]['control'], other(mover), def_tackle,
                                       label=f"Dribble Challenge: {mover} {carrier} through {other(mover)} ZoC at {contested_hex}",
                                       showman_unit=carrier)
        if win:
            stats['dribbles_won'] += 1
            s['pos'][mover][carrier] = best_hex
            s['ball'] = {'side':mover,'unit':carrier,'hex':best_hex}
            breakaway['flag'] = True
        else:
            s['pos'][mover][carrier] = contested_hex
            s['ball'] = {'side':None,'unit':None,'hex':prev_hex}
        sim.check_no_overlap(s)

    def attempt_shot(mover):
        if s['ball']['side'] != mover:
            breakaway['flag'] = False
            return
        carrier = s['ball']['unit']
        if s.setdefault('outofnowhere_no_shot', {'A':False,'B':False})[mover]:
            # Out of Nowhere (Flash): consumed here, the instant this Act's own Shot
            # attempt would otherwise happen, then cleared for later turns.
            s['outofnowhere_no_shot'][mover] = False
            breakaway['flag'] = False
            return
        hex_ = s['pos'][mover][carrier]
        end = att_end(mover)
        d = B.shot_dist(hex_, end)
        srange = sim.ROSTER[carrier]['srange']
        if srange is None and s.setdefault('playingout_this_turn', {'A':False,'B':False})[mover]:
            # Playing Out (Sunday Ederson): grant it WB's own Shot Range (2) for this
            # attempt only - see driver_base.py's own comment for the full reasoning.
            srange = 2
        had_breakaway = breakaway['flag']
        breakaway['flag'] = False
        if srange is None or d is None or d > srange:
            return
        opp = other(mover)
        stats['shots'] += 1
        stats['unit_shots'][carrier] += 1
        if had_breakaway:
            stats['breakaway_shots'] += 1

        if not sim.gk_zone_occupied(s, opp):
            stats['goals'] += 1; stats['auto_goals'] += 1; stats[f'goals_{mover.lower()}'] += 1
            stats['unit_goals'][carrier] += 1
            if had_breakaway: stats['breakaway_goals'] += 1
            s['score'][mover] += 1
            sim.goal_restart(s, opp); sim.check_no_overlap(s)
            return
        guard = zone_guard(opp)
        if guard is None:
            stats['goals'] += 1; stats['auto_goals'] += 1; stats[f'goals_{mover.lower()}'] += 1
            stats['unit_goals'][carrier] += 1
            if had_breakaway: stats['breakaway_goals'] += 1
            s['score'][mover] += 1
            sim.goal_restart(s, opp); sim.check_no_overlap(s)
            return
        save = sim.save_stat(s, opp, guard)
        save = maybe_counter_die(opp, save)
        shot_dice = sim.shot_dice(carrier, breakaway=had_breakaway)
        curled = False
        if can_afford(mover, 'CurlShot'):  # unconditional +1 die now that every hex is Top or Bottom (§4/§11)
            pay_and_discard(mover, 'CurlShot')
            stats['curlshot_played'] += 1
            shot_dice += 1
            curled = True
        label = f"Shot: {mover} {carrier} vs {opp} {guard}" + (" (THROUGH ON GOAL)" if had_breakaway else "") + \
                (" (CURL SHOT, +1 die)" if curled else "")
        # Rolled directly rather than via sim.contest() so the Save side's individual dice
        # faces stay visible afterward - §8's Save-retention rule needs to know if a Flair
        # showed up on the Save roll, which contest()'s plain (win, ah, dh) return can't
        # expose without changing its signature for every other caller (Pass, Dribble
        # Challenge, Tackle) that has no use for that detail. Same reasoning as
        # dribble_contest() above, which does the same thing for Nutmeg.
        av, af, ah = sim.roll(s, mover, shot_dice, True)
        dv, df, dh = sim.roll(s, opp, save, False)
        win = ah > dh
        line = (f"[{label}] {mover} rolls {av}->{af} ({ah} succ) | {opp} rolls {dv}->{df} "
                f"({dh} stop) => {'ATTACKER WINS' if win else 'DEFENDER HOLDS'}")
        s['log'].append(line); print(line)
        if not win and 'Composure' in s['hand_tac'][mover] and s['flair'][mover] >= 1 and ah <= dh:
            sim.play_composure(s, mover)
            stats['composure_played'] += 1
            rv, rf, rh = sim.roll(s, mover, 1, True)
            if rf[0] == 'success':
                ah += 1
                win = ah > dh
        if (not win and sim.ROSTER[carrier].get('sig') == 'clinical'
                and not s.setdefault('clinical_used', {'A':False,'B':False})[mover]):
            # Clinical (§14): reroll one Blank die on a Shot, once per match, free - "in
            # addition to, not instead of" any post-roll Tactic Card (Composure above),
            # so it's checked independently and can still fire even after Composure
            # already tried and failed to turn the Shot around.
            s['clinical_used'][mover] = True
            stats['clinical_played'] += 1
            s['log'].append(f"  [{mover} PO Clinical (§14) - reroll one Blank die on the Shot, once per match, free]")
            rv, rf, rh = sim.roll(s, mover, 1, True)
            if rf[0] == 'success':
                ah += 1
                win = ah > dh
        if (not win and sim.ROSTER[carrier].get('sig') == 'main_character'
                and not s.setdefault('mainchar_used', {'A':False,'B':False})[mover]):
            # Main Character (Me!): once/match, reroll ALL Blank dice on a Shot (not
            # just Clinical's one) - see driver_base.py's own comment for the full
            # rationale. Marked used on any lost-Shot attempt while eligible, even
            # on the rare roll with zero blanks to reroll.
            s['mainchar_used'][mover] = True
            stats['mainchar_played'] += 1
            n_blank = af.count('blank')
            if n_blank:
                s['log'].append(f"  [{mover} PO Main Character - reroll all {n_blank} Blank dice on the Shot, once per match, free]")
                rv, rf, rh = sim.roll(s, mover, n_blank, True)
                ah += rh
                win = ah > dh
        guard_sig = sim.ROSTER[guard].get('sig') if guard == 'GK' else None
        if guard_sig in ('shot_stopper', 'immovable') and not s.setdefault('shotstopper_used', {'A':False,'B':False})[opp]:
            # Shot-Stopper (§14) / Immovable (The Wall): reroll Blank dice on the Save,
            # once per match, free - see driver_base.py's own comment for the full
            # reasoning, including why this never fires for "Playing Out".
            s['shotstopper_used'][opp] = True
            reroll_dice = 2 if guard_sig == 'immovable' else 1
            if guard_sig == 'immovable':
                stats['immovable_played'] += 1
                s['log'].append(f"  [{opp} GK Immovable - reroll up to 2 Blank dice on the Save, once per match, free]"); print(s['log'][-1])
            else:
                stats['shotstopper_played'] += 1
                s['log'].append(f"  [{opp} GK Shot-Stopper (§14) - reroll one Blank die on the Save, once per match, free]"); print(s['log'][-1])
            for _ in range(reroll_dice):
                rv, rf, rh = sim.roll(s, opp, 1, False)
                df = df + rf
                if rf[0] == 'stop':
                    dh += 1
                    win = ah > dh
        if win and can_afford(opp, 'LastDitchBlock'):
            pay_and_discard(opp, 'LastDitchBlock')
            stats['lastditch_played'] += 1
            ah -= 1
            win = ah > dh
            s['log'].append(f"  [{opp} plays Last Ditch Block (2 Flair) - cancels one Success from the Shot]")
        if win:
            stats['goals'] += 1; stats[f'goals_{mover.lower()}'] += 1
            stats['unit_goals'][carrier] += 1
            if had_breakaway: stats['breakaway_goals'] += 1
            s['score'][mover] += 1
            sim.goal_restart(s, opp); sim.check_no_overlap(s)
        elif 'flair' in df:
            # Save-retention (§8): a Flair among the Save roll's own dice (the Shot-
            # Stopper reroll above included) means the goalkeeper holds on to it
            # outright - no rebound, no loose ball, nothing for the attacking side to
            # chase. A real Goalkeeper rolling Save 3 hits this ~70% of the time
            # (1 - (2/3)^3); an Emergency deputy on a flat Save 1 only ~33% - the
            # differentiation falls straight out of the existing Save-dice-count stat,
            # no new one needed.
            s['ball'] = {'side':opp,'unit':guard,'hex':s['pos'][opp][guard]}
            s['log'].append(f"  [{opp} {guard} holds on to the Save - Flair on the roll, no rebound]"); print(s['log'][-1])
        else:
            def rebound_target():
                """§8: a parried Save with no Flair spills to one hex outside the
                Goalkeeper Zone (B.REBOUND_HEX), on whichever side matches the shot's own
                Lane - genuinely contestable, unlike the old in-zone rebound this
                replaces. A seam-row-origin shot (both lanes at once, F3 chief among
                them) has 2 legal candidates instead of 1: ranked empty > a defender's
                hex > an attacker's hex (landing on an attacker is otherwise a free,
                uncontested chance handed straight to the shooting side off their own
                save); a tie between same-ranked candidates is the defending side's own
                call to make, which this driver has no real judgment for, so it defaults
                to Bottom."""
                lanes = B.lane(hex_[0], int(hex_[1:]))
                if len(lanes) == 1:
                    return B.REBOUND_HEX[end][lanes[0]]
                top_h, bot_h = B.REBOUND_HEX[end]['Top'], B.REBOUND_HEX[end]['Bottom']
                def tier(h):
                    for side_ in ('A', 'B'):
                        if h in s['pos'][side_].values():
                            return 1 if side_ == opp else 2
                    return 0
                t_top, t_bot = tier(top_h), tier(bot_h)
                if t_top != t_bot:
                    return top_h if t_top < t_bot else bot_h
                return bot_h  # tied - defending side's choice; driver defaults to Bottom
            rebound = rebound_target()
            occupant = next(((side_, u) for side_ in ('A', 'B') for u, h in s['pos'][side_].items() if h == rebound), None)
            if occupant:
                occ_side, occ_unit = occupant
                s['ball'] = {'side':occ_side,'unit':occ_unit,'hex':rebound}
                s['log'].append(f"  [rebound spills to {rebound} - {occ_side}'s {occ_unit} was already there, claims it]"); print(s['log'][-1])
            else:
                s['ball'] = {'side':None,'unit':None,'hex':rebound}
                s['log'].append(f"  [rebound spills loose to {rebound} - open ground, first to activate there claims it]"); print(s['log'][-1])

    def resolve_bounce_net(mover, carrier, start):
        """A bounce pass that reached the net (sim.bounce_pass_options' 'net' kind) -
        Save-contested exactly like attempt_shot(), just reached via a bent path instead
        of a straight shot_dist() line, so it can't just call attempt_shot() directly
        (that recomputes distance from the carrier's own hex, which is exactly what's out
        of range here - that's why a bounce was needed at all). 2026-09-16, ported from
        driver_base.py: UNLIKE that version, this file's Composure and Curl Shot are live
        (hand_tac isn't always empty here), so both are replayed below, matching
        attempt_shot()'s own order - driver_base.py's version skipped them as genuinely
        dead code there, which no longer applies once ported into the Advanced Game
        driver. Last Ditch Block (defender's side) is replayed too, for the same reason.
        Still deliberately excludes Through on Goal/breakaway - a bounce pass was never
        the product of winning a Dribble Challenge into a shooting position, so that bonus
        has no analogue here."""
        end = att_end(mover)
        opp = other(mover)
        stats['bounce_shots'] += 1
        stats['shots'] += 1
        stats['unit_shots'][carrier] += 1
        if not sim.gk_zone_occupied(s, opp):
            stats['goals'] += 1; stats['auto_goals'] += 1; stats[f'goals_{mover.lower()}'] += 1
            stats['unit_goals'][carrier] += 1; stats['bounce_goals'] += 1
            s['score'][mover] += 1
            s['log'].append(f"  [{mover} {carrier}'s bounce pass finds an empty net - GOAL]"); print(s['log'][-1])
            sim.goal_restart(s, opp); sim.check_no_overlap(s)
            return
        guard = zone_guard(opp)
        if guard is None:
            stats['goals'] += 1; stats['auto_goals'] += 1; stats[f'goals_{mover.lower()}'] += 1
            stats['unit_goals'][carrier] += 1; stats['bounce_goals'] += 1
            s['score'][mover] += 1
            s['log'].append(f"  [{mover} {carrier}'s bounce pass finds an empty net - GOAL]"); print(s['log'][-1])
            sim.goal_restart(s, opp); sim.check_no_overlap(s)
            return
        save = sim.save_stat(s, opp, guard)
        save = maybe_counter_die(opp, save)
        shot_dice = sim.shot_dice(carrier)
        curled = False
        if can_afford(mover, 'CurlShot'):
            pay_and_discard(mover, 'CurlShot')
            stats['curlshot_played'] += 1
            shot_dice += 1
            curled = True
        label = f"Bounce Pass -> Shot: {mover} {carrier} vs {opp} {guard}" + (" (CURL SHOT, +1 die)" if curled else "")
        av, af, ah = sim.roll(s, mover, shot_dice, True)
        dv, df, dh = sim.roll(s, opp, save, False)
        win = ah > dh
        line = (f"[{label}] {mover} rolls {av}->{af} ({ah} succ) | {opp} rolls {dv}->{df} "
                f"({dh} stop) => {'ATTACKER WINS' if win else 'DEFENDER HOLDS'}")
        s['log'].append(line); print(line)
        if not win and 'Composure' in s['hand_tac'][mover] and s['flair'][mover] >= 1 and ah <= dh:
            sim.play_composure(s, mover)
            stats['composure_played'] += 1
            rv, rf, rh = sim.roll(s, mover, 1, True)
            if rf[0] == 'success':
                ah += 1
                win = ah > dh
        if (not win and sim.ROSTER[carrier].get('sig') == 'clinical'
                and not s.setdefault('clinical_used', {'A':False,'B':False})[mover]):
            s['clinical_used'][mover] = True
            stats['clinical_played'] += 1
            s['log'].append(f"  [{mover} PO Clinical (§14) - reroll one Blank die on the Shot, once per match, free]")
            rv, rf, rh = sim.roll(s, mover, 1, True)
            if rf[0] == 'success':
                ah += 1
                win = ah > dh
        if (not win and sim.ROSTER[carrier].get('sig') == 'main_character'
                and not s.setdefault('mainchar_used', {'A':False,'B':False})[mover]):
            # Main Character (Me!): once/match, reroll ALL Blank dice on a Shot (not
            # just Clinical's one) - see driver_base.py's own comment for the full
            # rationale. Marked used on any lost-Shot attempt while eligible, even
            # on the rare roll with zero blanks to reroll.
            s['mainchar_used'][mover] = True
            stats['mainchar_played'] += 1
            n_blank = af.count('blank')
            if n_blank:
                s['log'].append(f"  [{mover} PO Main Character - reroll all {n_blank} Blank dice on the Shot, once per match, free]")
                rv, rf, rh = sim.roll(s, mover, n_blank, True)
                ah += rh
                win = ah > dh
        guard_sig = sim.ROSTER[guard].get('sig') if guard == 'GK' else None
        if guard_sig in ('shot_stopper', 'immovable') and not s.setdefault('shotstopper_used', {'A':False,'B':False})[opp]:
            s['shotstopper_used'][opp] = True
            reroll_dice = 2 if guard_sig == 'immovable' else 1
            if guard_sig == 'immovable':
                stats['immovable_played'] += 1
                s['log'].append(f"  [{opp} GK Immovable - reroll up to 2 Blank dice on the Save, once per match, free]"); print(s['log'][-1])
            else:
                stats['shotstopper_played'] += 1
                s['log'].append(f"  [{opp} GK Shot-Stopper (§14) - reroll one Blank die on the Save, once per match, free]"); print(s['log'][-1])
            for _ in range(reroll_dice):
                rv, rf, rh = sim.roll(s, opp, 1, False)
                df = df + rf
                if rf[0] == 'stop':
                    dh += 1
                    win = ah > dh
        if win and can_afford(opp, 'LastDitchBlock'):
            pay_and_discard(opp, 'LastDitchBlock')
            stats['lastditch_played'] += 1
            ah -= 1
            win = ah > dh
            s['log'].append(f"  [{opp} plays Last Ditch Block (2 Flair) - cancels one Success from the Shot]")
        if win:
            stats['goals'] += 1; stats[f'goals_{mover.lower()}'] += 1
            stats['unit_goals'][carrier] += 1; stats['bounce_goals'] += 1
            s['score'][mover] += 1
            sim.goal_restart(s, opp); sim.check_no_overlap(s)
        elif 'flair' in df:
            s['ball'] = {'side':opp,'unit':guard,'hex':s['pos'][opp][guard]}
            s['log'].append(f"  [{opp} {guard} holds on to the Save - Flair on the roll, no rebound]"); print(s['log'][-1])
        else:
            lanes = B.lane(start[0], int(start[1:]))
            rebound = B.REBOUND_HEX[end][lanes[0] if len(lanes) == 1 else 'Bottom']
            occupant = next(((side_, u) for side_ in ('A', 'B') for u, h in s['pos'][side_].items() if h == rebound), None)
            if occupant:
                occ_side, occ_unit = occupant
                s['ball'] = {'side':occ_side,'unit':occ_unit,'hex':rebound}
                s['log'].append(f"  [rebound spills to {rebound} - {occ_side}'s {occ_unit} was already there, claims it]"); print(s['log'][-1])
            else:
                s['ball'] = {'side':None,'unit':None,'hex':rebound}
                s['log'].append(f"  [rebound spills loose to {rebound} - open ground, first to activate there claims it]"); print(s['log'][-1])
        sim.check_no_overlap(s)

    def try_bounce_shot(mover, carrier, start):
        """New mechanic (2026-09-16 design session, now printed rulebook §8), ported from
        driver_base.py - see sim.bounce_pass_options's own docstring for the full ruling.
        Checked unconditionally, before even try_plain_pass_or_clearance runs - a genuine
        bonus scoring chance the direct-Shot check just missed, not a fallback. Returns
        True if a bounce shot was actually attempted, False otherwise."""
        options = sim.bounce_pass_options(s, mover, carrier)
        # A Goalkeeper's srange is None and Shot is 0 by design (§14 - not a scoring
        # threat, ever); a bounce pass respects that the same way a direct Shot already
        # does (attempt_shot() never fires for a GK carrier because has_shot needs a real
        # srange).
        can_shoot = sim.ROSTER[carrier]['srange'] is not None
        end = att_end(mover)
        net_opt = next((o for o in options if o['kind'] == 'net' and o['end'] == end), None) if can_shoot else None
        if net_opt is None:
            return False
        stats['bounce_attempts'] += 1
        s['log'].append(f"  [{mover} {carrier} bounces a pass off the {'back' if net_opt['axis'] in ('H','D1','D2') else 'side'} wall - lines up on goal]")
        resolve_bounce_net(mover, carrier, start)
        return True

    def resolve_bounce_completion(mover, carrier, start, kind, target, recv):
        """Completes a bounce-to-teammate ('pass') or bounce-to-empty-hex ('clear')
        candidate chosen by try_plain_pass_or_clearance - deliberately NOT routed through
        resolve_pass/resolve_clearance, since those assume a straight, freely-aimed line
        that can be contested by Zone of Control along the way (§9); a bounce pass's path
        is fixed the instant it's declared, so there's nothing analogous to contest."""
        stats['bounce_attempts'] += 1
        if kind == 'pass':
            stats['bounce_pass_completed'] += 1
            s['log'].append(f"  [{mover} {carrier} bounces a pass off the wall to {recv} at {target}]")
        else:
            stats['bounce_loose'] += 1
            s['log'].append(f"  [{mover} {carrier} bounces a pass off the wall to {target} - nobody there, ball's loose]")
        s['pos'][mover][carrier] = start  # passer doesn't move - only the ball travels
        s['ball'] = {'side':mover,'unit':recv,'hex':target} if kind == 'pass' else {'side':None,'unit':None,'hex':target}
        sim.check_no_overlap(s)
        if kind == 'pass':
            followup_move_then_maybe_shoot(mover, recv, "Bounce pass landed")

    def free_followup_pass_after_tackle(mover, tackler_unit):
        start = s['pos'][mover][tackler_unit]
        prange = sim.ROSTER[tackler_unit]['prange']
        end = att_end(mover)
        teammates = [(u,h) for u,h in s['pos'][mover].items() if u != tackler_unit]
        candidates = []
        for u,h in teammates:
            d, path = B.straight_line(start, h)
            if d is not None and d <= prange:
                candidates.append((d, h, u, path))
        if not candidates:
            return
        candidates.sort(key=lambda c: rank_dist(c[1], end))
        d, target, recv, path = candidates[0]
        if maybe_play_foul(other(mover), start):
            s['ball'] = {'side':None,'unit':None,'hex':start}
            return
        zoc = sim.enemy_zoc(s, mover)
        contested = (any(h in zoc for h in path[1:]) if path else (target in zoc))
        landed = resolve_pass(mover, tackler_unit, start, target, recv, path, contested,
                               "Free follow-up Pass")
        sim.check_no_overlap(s)
        if landed:
            followup_move_then_maybe_shoot(mover, recv, "won Tackle's free follow-up Pass landed")

    def defend_turn(mover):
        opp = other(mover)
        carrier = s['ball']['unit']
        carrier_hex = s['pos'][opp][carrier]
        adjacent_defs = [u for u,h in s['pos'][mover].items() if B.adjacent(h, carrier_hex)]
        if adjacent_defs:
            def_unit = max(adjacent_defs, key=lambda u: sim.ROSTER[u]['tackle'])
            card = find_card_for(mover, def_unit)
            if card is not None:
                play_card(mover, card, f"activates {def_unit}")
                win = do_tackle(mover, def_unit, opp,
                                 label=f"Tackle: {mover} {def_unit} vs {opp} {carrier} at {carrier_hex}",
                                 use_strong_chance=0.4)
                if win:
                    tackler_hex = s['pos'][mover].get(def_unit)
                    if tackler_hex is not None:
                        s['ball'] = {'side':mover,'unit':def_unit,'hex':tackler_hex}
                        sim.check_no_overlap(s)
                        free_followup_pass_after_tackle(mover, def_unit)
                else:
                    sim.check_no_overlap(s)
                return
        reposition(mover, towards=carrier_hex)

    def reposition(mover, towards):
        candidates = list(s['pos'][mover].items())
        if not candidates: return
        candidates.sort(key=lambda item: (B.straight_line(item[1], towards)[0] if B.straight_line(item[1], towards)[0] is not None else 99))
        unit, start = candidates[0]
        r = sim.legal_reach(s, mover, unit)
        best_hex, best_d = start, 999
        for h,(cost,path) in r.items():
            dl,_ = B.straight_line(h, towards)
            d = dl if dl is not None else rank_dist(h, def_end(mover))
            if d < best_d: best_d, best_hex = d, h
        card = find_card_for(mover, unit)
        if card is None or best_hex == start:
            return
        play_card(mover, card, f"activates {unit}")
        s['pos'][mover][unit] = best_hex
        sim.check_no_overlap(s)

    def claim_loose_ball(mover):
        ball_hex = s['ball']['hex']
        best_unit, best_cost = None, 999
        for u in s['pos'][mover]:
            r = sim.legal_reach(s, mover, u)
            if ball_hex in r and r[ball_hex][0] < best_cost:
                best_cost, best_unit = r[ball_hex][0], u
        if best_unit is None:
            reposition(mover, towards=ball_hex)
            return
        card = find_card_for(mover, best_unit)
        if card is None: return
        play_card(mover, card, f"activates {best_unit}")
        s['pos'][mover][best_unit] = ball_hex
        s['ball'] = {'side':mover,'unit':best_unit,'hex':ball_hex}
        sim.check_no_overlap(s)

    def play_turn(turn_no, mover):
        breakaway['flag'] = False
        full_press['active'] = False
        full_press['start_unit'] = s['ball']['unit'] if s['ball']['side'] == mover else None
        s.setdefault('playingout_this_turn', {'A':False,'B':False})[mover] = False
        if s.setdefault('playingout_pending_return', {'A':False,'B':False})[mover] and 'GK' in s['pos'][mover]:
            # Playing Out (Sunday Ederson): ported from driver_base.py, including its
            # corrected design (2026-09-17, after 2 rounds of user correction) - a
            # Pace-limited attempt to path back into the zone, blockable like any
            # normal move; if legal_reach comes back empty (blocked or Pace falls
            # short - the common case once it's wandered far), a guaranteed Yellow
            # Card via apply_discipline() does everything else needed for free (Pace
            # -1, sin-bin, and sinbin_check's own existing zone-return on the way
            # back). See driver_base.py's own comment for the full reasoning and the
            # real stale-ball-reference crash this exact mechanism exposed and fixed
            # at the engine level (apply_discipline/send_to_sinbin, shared by both
            # drivers - already covered here too, nothing extra needed in this file).
            s['playingout_pending_return'][mover] = False
            r = sim.legal_reach(s, mover, 'GK')
            if r:
                best_hex = min(r, key=lambda h: r[h][0])
                s['pos'][mover]['GK'] = best_hex
                s['log'].append(f"  [{mover} GK makes it back into its own zone at {best_hex} - Playing Out's exception ends]")
            else:
                s['log'].append(f"  [{mover} GK can't get back into its own zone - blocked or out of Pace]")
                stats['playingout_yellow'] += 1
                sim.apply_discipline(s, mover, 'GK', 'YellowCard')
        sim.sinbin_check(s, mover)
        s['log'].append(f"=== Half {s['half']} Turn {turn_no} ({mover}) ===")
        if s.get('emergency_gk',{}).get(mover) is None and f"{mover}:GK" in s.get('sent_off', []):
            # 'GK' not in s['pos'][mover] alone isn't enough - that's also true while the
            # GK is merely sin-binned, which must NOT get an emergency deputy (§12: the
            # zone stays genuinely empty that turn, by design).
            sim.assign_emergency_gk(s, mover)
        if s['ball']['side'] == mover:
            pressed = maybe_play_press(mover)
            if pressed and s['ball']['side'] != mover:
                pass
            else:
                carrier = s['ball']['unit']
                if sim.kickoff_release_required(s, mover, carrier):
                    handle_kickoff_release(mover, carrier)
                else:
                    move_ball_carrier(mover)
                    attempt_shot(mover)
        elif s['ball']['side'] is None:
            claim_loose_ball(mover)
        else:
            defend_turn(mover)
        sim.replenish(s, mover)

    for t in range(1, 49):
        mover = 'A' if t % 2 == 0 else 'B'
        play_turn(t, mover)
        if t == 24:
            sim.halftime_reset(s)
            sim.check_no_overlap(s)

    stats['score'] = f"A {s['score']['A']}-{s['score']['B']} B"
    stats['sent_off'] = len(s.get('sent_off', []))
    return stats, s['log']

N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
all_stats = []
for i in range(1, N+1):
    stats, log = run_match(i)
    all_stats.append(stats)

with open('batch_stats.json', 'w') as f:
    json.dump(all_stats, f, indent=1)

totals = {}
for k in all_stats[0]:
    if k in ('score','match','unit_shots','unit_goals'): continue
    totals[k] = sum(m[k] for m in all_stats)
unit_shots = {u: sum(m['unit_shots'][u] for m in all_stats) for u in ('SW','WB','PM','PO')}
unit_goals = {u: sum(m['unit_goals'][u] for m in all_stats) for u in ('SW','WB','PM','PO')}

from collections import Counter
dist = Counter(m['goals'] for m in all_stats)
print("N =", N)
print(totals)
print("goals per match:", round(totals['goals']/N, 3))
print("goals-per-match distribution:", dict(sorted(dist.items())))
print("scoreless matches:", dist.get(0,0), "/", N)
print("shots per match:", round(totals['shots']/N, 3))
print("shot conversion:", round(totals['goals']/totals['shots'], 3) if totals['shots'] else None)
print("breakaway share of shots:", round(totals['breakaway_shots']/totals['shots'], 3) if totals['shots'] else None)
print("breakaway share of goals:", round(totals['breakaway_goals']/totals['goals'], 3) if totals['goals'] else None)
print("shots/goals/conversion by position:")
for u in ('SW','WB','PM','PO'):
    sh, gl = unit_shots[u], unit_goals[u]
    conv = round(gl/sh, 3) if sh else None
    print(f"  {u}: {sh} shots, {gl} goals, conversion {conv}")

print()
print("=== Yellow/Red Cards ===")
print("yellow cards:", totals['yellows'])
print("red cards:", totals['reds'], "(sent off:", totals['sent_off'], ")")
print("cards per match:", round((totals['yellows']+totals['reds'])/N, 3))
print("sin-bin trips:", totals['sinbin_trips'])

print()
print("=== Tactic Card usage (all 13 now modeled) ===")
usage = [
    ('Foul', totals['fouls_played']),
    ('Press', totals['press_played']),
    ('Composure', totals['composure_played']),
    ('StrongTackle', totals['strongtackle_played']),
    ('Jockey', totals['jockey_played']),
    ('ThroughBall', totals['throughball_played']),
    ('Nutmeg', totals['nutmeg_played']),
    ('StepOver', totals['stepover_played']),
    ('CurlShot', totals['curlshot_played']),
    ('OneTwo', totals['onetwo_played']),
    ('Backheel', totals['backheel_played']),
    ('LongBall', totals['longball_played']),
    ('LastDitchBlock', totals['lastditch_played']),
]
for name, count in sorted(usage, key=lambda x: -x[1]):
    print(f"  {name}: {count} ({round(count/N,2)}/match)")
