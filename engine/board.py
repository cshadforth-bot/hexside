"""Hexside hex-grid geometry, built from the printed rulebook (§4), verified against the
book's own worked examples: F3's 6 neighbors (E3,E4,F2,F4,G3,G4), E4->G3 diagonal distance
2, B3->J3 straight-line distance 8. Flat-top hexes, columns A-K, tall/short alternating
(A,C,E,G,I,K run rows 1-6, 6 full hexes tall; B,D,F,H,J nest between them, rows 1-5 full-size,
offset by half a hex, PLUS a half-height cap hex at row 0 and row 6 that squares each short
column off flush with its tall neighbors instead of leaving the top/bottom edge recessed by
half a hex - see min_row()/max_row() below. Those two cap rows behave as ordinary hexes for
every rule in this module; only their on-screen rendering (in the HTML/JS pitch diagrams,
outside this file) draws them at half height.
"""
COLS = "ABCDEFGHIJK"

def is_short(col):
    return COLS.index(col) % 2 == 1  # B,D,F,H,J

def min_row(col):
    return 0 if is_short(col) else 1

def max_row(col):
    return 6

def rows_in_col(col):
    return max_row(col) - min_row(col) + 1  # tall: 6 (unchanged). short: 7 (5 full + 2 caps).

def parse(h):
    return h[0], int(h[1:])

def valid(col, row):
    return col in COLS and min_row(col) <= row <= max_row(col)

def third(col):
    """§4: Third 1 = A-D, Third 2 = E-G, Third 3 = H-K."""
    i = COLS.index(col)
    if i <= 3: return 1
    if i <= 6: return 2
    return 3

def lane(col, row):
    """§4: Top/Bottom, split exactly on the board's physical centerline. Tall columns
    split cleanly 3/3 (rows 1-3 / 4-6) - the centerline falls between rows 3 and 4, so
    every hex is unambiguously one or the other. Short columns split 3/1/3 the same way
    (rows 0-2 Top / row 3 seam / rows 4-6 Bottom) - row 3 sits EXACTLY on the centerline
    (dY(row=3, short) = 7, the exact midpoint of the board's full dY range 2-12), so it
    belongs to both lanes at once - a "seam row", the Lane axis's exact twin of the seam
    columns (D, H; see SEAM_EXTRA in sim.py) - rather than an arbitrary tie-break to one
    side. Returns a tuple, almost always length 1; length 2 only for the seam row's 5
    hexes: B3, D3, F3 (the kickoff spot), H3, J3."""
    if is_short(col):
        if row <= 2: return ('Top',)
        if row == 3: return ('Top', 'Bottom')
        return ('Bottom',)
    else:
        if row <= 3: return ('Top',)
        return ('Bottom',)

def zone(h):
    """One Third x one lane-tuple, e.g. zone('G4') -> (2, ('Bottom',)) or zone('F3') ->
    (2, ('Top', 'Bottom')) for a seam-row hex."""
    col, row = parse(h)
    return third(col), lane(col, row)

def dY(col, row):
    return 2*row + (1 if is_short(col) else 0)

def from_xy(x, Y):
    col = COLS[x]
    short = is_short(col)
    if short and Y % 2 == 0: return None
    if not short and Y % 2 == 1: return None
    row = (Y - (1 if short else 0)) // 2
    if not valid(col, row): return None
    return f"{col}{row}"

def neighbors(h):
    """The 6 hexes surrounding h (fewer at the pitch's top/bottom edges)."""
    col, row = parse(h)
    x = COLS.index(col)
    Y = dY(col, row)
    out = []
    for dx, dy in [(0,-2),(0,2),(-1,-1),(-1,1),(1,-1),(1,1)]:
        nx, nY = x+dx, Y+dy
        if 0 <= nx < len(COLS):
            r = from_xy(nx, nY)
            if r: out.append(r)
    return out

def adjacent(h1, h2):
    return h2 in neighbors(h1)

# GOAL_MOUTH: the 2 hexes directly in front of net (A3/A4, K3/K4) - an internal geometry
# helper, kept only for box_dist()'s old distance approximation below. NOT the same as
# "the goal box" in the rulebook (§4/§5/§8/§14) - that term now names the full 3-hex
# GK_ZONE below, not just these 2 (see GK_ZONE's own comment for why the two used to be
# different areas and no longer are).
GOAL_MOUTH = {'A': ('A3','A4'), 'K': ('K3','K4')}

# The Goalkeeper Zone (§4/§5/§8/§14), a.k.a. "the goal box" - the two terms name the
# same 3-hex area: the 2 goal-mouth hexes (GOAL_MOUTH above) plus one bordering
# seam-column hex, B3 for the A end (adjacent to both A3 and A4), J3 for the K end.
# Distinct from the 3-hex Net (NET_POINTS, below - the Shot's actual target, off the
# playable pitch entirely). Used for: Goalkeeper confinement (the Goalkeeper, or its
# Emergency deputy, may never move outside its own zone); opponent exclusion (every
# other unit may never enter the OPPONENT's zone, though it may freely stand inside its
# own side's); and as the uncontestable area a Save-rebound must land OUTSIDE of to mean
# anything (§8) - see REBOUND_HEX below.
GK_ZONE = {'A': ('A3', 'A4', 'B3'), 'K': ('K3', 'K4', 'J3')}

# Where a parried Save (no Flair on the Save roll, §8) actually lands - one hex outside
# GK_ZONE, in the seam column bordering it, on whichever side matches the shot's own
# Lane (§4). B2/J2 are non-zone neighbors of BOTH the Top zone hex (A3/K3) and the seam
# hex (B3/J3); B4/J4 are the same for the Bottom zone hex (A4/K4) - so each hex is
# reachable regardless of which of the 3 zone hexes the guard is actually standing on.
# A shot from a seam-row hex (both lanes at once - F3 chief among them) has no single
# answer here; see attempt_shot()'s own rebound_target() in the driver for that tiebreak.
REBOUND_HEX = {'A': {'Top': 'B2', 'Bottom': 'B4'}, 'K': {'Top': 'J2', 'Bottom': 'J4'}}

def straight_line(h1, h2):
    """Returns (distance, [intervening hexes excluding endpoints]) or (None, None) if h1
    and h2 don't sit on one of the board's straight lines (§4: up/down a column, the two
    diagonal axes, or same-row same-column-parity)."""
    c1, r1 = parse(h1); c2, r2 = parse(h2)
    if h1 == h2: return 0, []
    x1, x2 = COLS.index(c1), COLS.index(c2)
    if c1 == c2:
        d = abs(r1 - r2)
        step = 1 if r2 > r1 else -1
        mids = [f"{c1}{r1+step*i}" for i in range(1, d)]
        return d, mids
    Y1, Y2 = dY(c1, r1), dY(c2, r2)
    dx, dyv = x2 - x1, Y2 - Y1
    # same-row same-parity horizontal band
    if dyv == 0 and (x1 % 2) == (x2 % 2):
        d = abs(dx)
        step = 2 if dx > 0 else -2
        mids = []
        xx = x1 + step
        while xx != x2:
            mids.append(f"{COLS[xx]}{r1}")
            xx += step
        return d, mids
    # diagonal axes
    if abs(dx) == abs(dyv) and dx != 0:
        d = abs(dx)
        sx = 1 if dx > 0 else -1
        sy = 1 if dyv > 0 else -1
        mids = []
        for i in range(1, d):
            mh = from_xy(x1 + sx*i, Y1 + sy*i)
            mids.append(mh)
        return d, mids
    return None, None

def _short_idx(i):
    """Generalizes is_short() to a raw column index rather than a letter, so it also
    works for the off-board Net columns (index -1, one before A; index len(COLS), one
    after K) — the alternating tall/short pattern simply continues past either edge, and
    Python's modulo already gives the right answer for the negative index for free."""
    return i % 2 == 1

def _dY_idx(i, row):
    return 2*row + (1 if _short_idx(i) else 0)

# §4's Net: three hexes immediately beyond each goal box, in a virtual column that
# continues the tall/short alternation one step past the pitch edge (so it's short,
# since A and K are both tall) — touching the box's row-3 hex only, both, and its row-4
# hex only. Column index -1 for the A end, len(COLS) for the K end; row 2/3/4 in that
# virtual short column's own numbering (verified against GOAL_MOUTH's actual adjacency,
# not just visual placement).
NET_POINTS = {
    'A': [(-1, 2), (-1, 3), (-1, 4)],   # touching A3-only, both A3+A4, A4-only
    'K': [(len(COLS), 2), (len(COLS), 3), (len(COLS), 4)],  # touching K3-only, both, K4-only
}

def net_hexes(end):
    """end = 'A' or 'K'. The 3 off-board (column-index, row) points beyond that goal box
    (§4) — not part of the playable pitch, only the Shot's actual target. Never occupiable
    by any unit; these aren't real hex-string addresses, just coordinates for shot_dist()."""
    return NET_POINTS[end]

def _straight_dist_idx(i1, r1, i2, r2):
    """Like straight_line(), but operates on raw (column-index, row) pairs instead of
    hex-string addresses, so it also works for the off-board Net points, which sit
    outside the normal addressable A-K grid and have no valid hex string of their own.
    Returns distance, or None if the two points don't sit on one of the board's three
    straight-line axes (§4)."""
    if i1 == i2 and r1 == r2: return 0
    if i1 == i2:
        return abs(r1 - r2)
    Y1, Y2 = _dY_idx(i1, r1), _dY_idx(i2, r2)
    dx, dyv = i2 - i1, Y2 - Y1
    if dyv == 0 and (i1 % 2) == (i2 % 2):
        return abs(dx)
    if abs(dx) == abs(dyv) and dx != 0:
        return abs(dx)
    return None

def shot_dist(h, end):
    """Distance from h to the nearest of the 3 real Net hexes beyond `end`'s goal box
    (§4, §8) — the Shot's actual target, not the goal box itself. Genuinely measures to
    the Net now (not the box as an approximation): wherever a straight line already
    reaches the box, the Net is exactly one hex further out on that same line: But the
    Net's forced short-column parity also means some hexes in the OTHER short columns
    (B, D, F, H, J) get a straight line to the Net that never reached the box at all —
    a real, if narrow, extra shooting angle the box-based approximation used to miss
    entirely. Returns None if no straight line reaches any of the 3 net points."""
    col, row = parse(h)
    i1 = COLS.index(col)
    best = None
    for (i2, r2) in NET_POINTS[end]:
        d = _straight_dist_idx(i1, row, i2, r2)
        if d is not None and (best is None or d < best):
            best = d
    return best

# BOUNCE PASS (new mechanic, 2026-09-16 design session): a Pass may be played off a wall
# instead of straight at a teammate. Verified this session, by hand, against real
# straight_line()/shot_dist() output before being generalized here - see the 4 named cases
# below, still the canonical worked examples for this whole mechanic:
#   C6-B5-A5, continuing past A5 -> the net (a plain diagonal, already GOAL under Shot
#     Range today - shot_dist('C6','A')==3)
#   C4-B3-A3, continuing past A3 -> the net (the OTHER diagonal through C4, also already
#     GOAL today - shot_dist('C4','A')==3, unrelated to the line below)
#   C5-A5 (horizontal) -> WALL, reflects back along row 5 (never reaches the net - see
#     _AXIS below for why)
#   C4-A4 (horizontal) -> GOAL - A4 is a GOAL_MOUTH hex, so nothing bounces there at all,
#     on ANY axis; C4's horizontal arrival just isn't the same line as C4's own diagonal
#     above, it's a second, independent way C4 threatens goal
#
# The 4 straight-line axes straight_line() already recognizes (§4), as opposite (d_idx,
# d_dY) step pairs. V and the two diagonals are also the 6 real adjacency directions
# (neighbors()); H is the "same row, same column parity" axis straight_line() recognizes
# for range purposes even though it skips the intervening short column's hex entirely
# (passes through the gap between e.g. B4 and B5 - see straight_line()'s own horizontal
# branch). Grouped this way so the reflection table below can be defined once per axis
# rather than per direction.
_AXIS_STEPS = {
    'V':  ((0,-2), (0,2)),
    'D1': ((-1,-1), (1,1)),
    'D2': ((-1,1), (1,-1)),
    'H':  ((-2,0), (2,0)),
}

# What each axis becomes after reflecting off a SIDE wall (ran off the top/bottom row
# range) vs a BACK wall (ran off column A/K's own outer edge, index -1 or len(COLS)).
# Verified by direct reflection-angle math this session, not guessed: reflecting angle
# theta across a horizontal mirror gives -theta, across a vertical mirror gives
# 180-theta; both sent the board's one 30-degree diagonal straight to the other
# (150-degree) diagonal and back, since a flat-top hex grid only has two diagonal
# directions to begin with, so there's nowhere else for either to go. V can only ever hit
# a side wall (moving along a fixed column never changes which column you're in) and H
# can only ever hit a back wall, for the mirror-image reason - so there's no "V off a back
# wall" or "H off a side wall" case to define; either is a contradiction in terms (the ball
# was already running parallel to that wall, never approaching it).
_BOUNCE_REFLECT = {
    ('V','side'): 'V', ('H','back'): 'H',
    ('D1','side'): 'D2', ('D2','side'): 'D1',
    ('D1','back'): 'D2', ('D2','back'): 'D1',
}

# Budget cost per step of each axis, in the same "hexes crossed" units straight_line()
# itself uses for distance/range. V/D1/D2 steps are real neighbor steps, 1 hex each. An H
# step is (+-2, 0) in idx - it already crosses 2 real columns in one step (e.g. C to A),
# which straight_line()'s own horizontal branch charges as distance 2, not 1 - so an H
# step has to cost 2 units of Pass Range budget here too, or a bounce pass would get every
# horizontal hex for half its real Pass Range price.
_AXIS_STEP_COST = {'V': 1, 'D1': 1, 'D2': 1, 'H': 2}

def _walk_axis(i, Y, d_idx, d_dY, cost, budget):
    """Every (idx,dY) point reachable walking (d_idx,d_dY) hex-steps from (i,Y), each step
    spending `cost` units of `budget`. Stops the instant a step would leave the
    addressable A-K grid, or the next step can't be afforded - the caller
    (bounce_pass_reach) decides what leaving the grid means (a net point, or a wall to
    reflect off). Returns (points, remaining_budget, exited_via) - exited_via is None if
    the walk stopped only because the budget ran out (there was still real pitch ahead),
    else 'side' or 'back' for why it hit the pitch's own edge - 'back' if the failing
    step's column index left [0, len(COLS)), 'side' if the column was still valid but the
    row wasn't (only V/D1/D2 can do this - H's d_dY is always 0, and same-parity columns
    always share the same min_row/max_row, so a pure H step can only ever fail the column
    check, never this one)."""
    pts = []
    remaining = budget
    while remaining >= cost:
        ni, nY = i + d_idx, Y + d_dY
        if not (0 <= ni < len(COLS)):
            return pts, remaining, 'back'
        if from_xy(ni, nY) is None:
            return pts, remaining, 'side'
        i, Y = ni, nY
        pts.append((i, Y))
        remaining -= cost
    return pts, remaining, None

def bounce_pass_reach(start, axis, direction, budget):
    """All legal landing points for a bounce Pass from hex `start`, travelling along
    `axis` ('V','D1','D2', or 'H') in `direction` (0 or 1, indexing _AXIS_STEPS[axis]),
    within total Pass Range `budget` (§14 ruling: counts hexes crossed on BOTH segments
    combined, same as a straight Pass counts hexes crossed on one). Returns a dict with:
      'path': ordered list of real hex strings actually crossed/reachable, nearest first -
        every one of these is a legal target, same as every hex within a straight Pass's
        range is a legal target, not just the furthest one.
      'reaches_net': the net end ('A' or 'K') this line reaches, or None. Two distinct
        ways this can happen, both checked: (1) the LAST real hex reached is itself
        A3/A4/K3/K4 - nothing bounces there on ANY axis, this session's ruling, checked
        first and regardless of why the walk stopped; (2) the line continues past a
        non-goal-mouth hex (A2/A5/K2/K5's own diagonal, or a short column's horizontal)
        and lands exactly on one of the 3 real NET_POINTS anyway. Either way this is
        Save-contested like any other Shot (§8), not treated as a normal Pass - that
        ruling belongs to whatever calls this, not to this geometry function.
      'bounced': True if a real wall reflection actually happened (as opposed to the whole
        budget being used up on the first segment with no wall reached at all).
    A single bounce only (§ this session's v1 scope) - a reflected segment that runs into
    a SECOND wall before the budget is exhausted just stops there, it does not bounce
    again."""
    col, row = parse(start)
    i0, Y0 = COLS.index(col), dY(col, row)
    d_idx, d_dY = _AXIS_STEPS[axis][direction]
    cost = _AXIS_STEP_COST[axis]
    pts1, remaining, exited = _walk_axis(i0, Y0, d_idx, d_dY, cost, budget)
    path = [from_xy(i,Y) for (i,Y) in pts1]
    if path:
        c_last, r_last = parse(path[-1])
        if c_last in ('A','K') and r_last in (3,4):
            return {'path': path, 'reaches_net': c_last, 'bounced': False}
    if exited is None:
        return {'path': path, 'reaches_net': None, 'bounced': False}
    last_i, last_Y = pts1[-1] if pts1 else (i0, Y0)
    # Did the failing step land exactly on a real net point anyway? Net points are stored
    # as (col_index, ROW), not (col_index, dY) - compare via _dY_idx, not a raw tuple
    # match. (This is the short-column-horizontal-reaches-net case, or a diagonal
    # continuing past A2/A5/K2/K5 rather than A3/A4/K3/K4 - the check above.)
    ni, nY = last_i + d_idx, last_Y + d_dY
    end = 'A' if ni < 0 else ('K' if ni >= len(COLS) else None)
    if end and any(ci == ni and _dY_idx(ci, r) == nY for (ci, r) in NET_POINTS[end]):
        return {'path': path, 'reaches_net': end, 'bounced': False}
    if not path:
        # Started already sitting flush on this wall/axis - nothing to bounce, no path.
        return {'path': [], 'reaches_net': None, 'bounced': False}
    new_axis = _BOUNCE_REFLECT.get((axis, exited))
    if new_axis is None:
        # H off a side wall or V off a back wall - a contradiction (see _BOUNCE_REFLECT's
        # own comment), can't actually happen for a real wall hit. Defensive, not a real
        # code path.
        return {'path': path, 'reaches_net': None, 'bounced': False}
    # Pick whichever of the reflected axis's 2 directions actually continues back onto the
    # grid, not out over the edge just hit - a wall corner where neither does is possible
    # in principle, so fall back to "stops here, didn't bounce" rather than crash.
    rd_idx = rd_dY = None
    for cand_dx, cand_dY in _AXIS_STEPS[new_axis]:
        test_i, test_Y = last_i + cand_dx, last_Y + cand_dY
        if 0 <= test_i < len(COLS) and from_xy(test_i, test_Y) is not None:
            rd_idx, rd_dY = cand_dx, cand_dY
            break
    if rd_idx is None:
        return {'path': path, 'reaches_net': None, 'bounced': False}
    pts2, _, _ = _walk_axis(last_i, last_Y, rd_idx, rd_dY, _AXIS_STEP_COST[new_axis], remaining)
    path += [from_xy(i,Y) for (i,Y) in pts2]
    return {'path': path, 'reaches_net': None, 'bounced': True}

def box_dist(h, end):
    """The OLD approximation: distance to the goal-box hex itself, not the Net beyond it
    — always exactly 1 less than shot_dist() wherever both are defined. Kept only for
    reference/comparison; Shot Range is checked against shot_dist(), not this."""
    box = GOAL_MOUTH[end]
    best = None
    for b in box:
        d, _ = straight_line(h, b)
        if d is not None:
            if best is None or d < best: best = d
    return best
