"""Carly Cakes - rules engine, heuristic AIs and balance simulator.

Rules in one breath: 18 cards, each a cake with 3 dial values (stages B, C, D) printed on
three edges and a blank 'batter' edge (stage A).  Racks: 2 per player.  Each of your turns:
  1. Rotate every cake in your oven one stage (A->B->C->D->cinders).  Cinders = the card is
     binned and scores nothing.
  2. Do ONE thing: PULL a cake (score the dial value showing + its effect), or take a
     Counter card and BAKE it (empty rack, starts at stage A), SLAM the door (tuck it under
     an opposing cake: that cake advances a stage immediately) or BIN it (deny).
"""
import random, sys, statistics
from collections import defaultdict

# name, (B, C, D), effect, quirk
CAKES = [
    ('Souffle', (9, 2, 0), 'twofor', ''),
    ('Celebration Cake', (6, 3, 0), 'fresh', ''),
    ('Cookies', (6, 2, 0), 'tip', ''),
    ('Choux Puffs', (6, 4, 1), 'draw', ''),
    ('Birthday Cake', (6, 6, 2), 'twofor', ''),
    ('Cherry Bakewell', (4, 7, 3), 'none', ''),
    ('Lemon Drizzle', (3, 6, 4), 'free_slam', ''),
    ('Red Velvet', (4, 7, 4), 'fresh', ''),
    ('Brownies', (5, 6, 5), 'rest', ''),
    ('Victoria Sponge', (4, 6, 5), 'glaze', ''),
    ('Carrot Cake', (4, 6, 6), 'draw', ''),
    ('Blueberry & Lemon Cake', (4, 5, 6), 'scrap', ''),
    ('Pavlova', (2, 5, 7), 'rest', ''),
    ('Coffee & Salted Pecan', (2, 5, 6), 'tip', 'preheated'),
    ('Black Forest', (1, 5, 7), 'free_slam', ''),
    ('Wedding Cake', (1, 2, 7), 'none', ''),
    ('Cheesecake', (2, 4, 6), 'none', 'sturdy'),
    ('Fruitcake', (2, 4, 6), 'glaze', 'sturdy'),
]
EFFVAL = {"none": 0, "tip": 1, "fresh": 1, "draw": 2, "twofor": 2.5, "free_slam": 1.5,
          "rest": 1, "glaze": 1, "scrap": 1.5}

def val(ci, st):
    return CAKES[ci][1][st - 1] if 1 <= st <= 3 else 0

POT = {}
def potential(ci):
    if ci in POT: return POT[ci]
    n, d, e, q = CAKES[ci]
    return max(d) * 0.75 + EFFVAL[e] + (0.5 if q == "sturdy" else 0)

def learn_potentials(rounds=4, n=1500, **kw):
    """Self-consistent card values: the AI bakes by measured points-per-bake, re-measured each round."""
    POT.clear()
    for _ in range(rounds):
        st = new_stats()
        for i in range(n):
            Game(900000 + i, Strong(), Strong(), stats=st, **kw).run()
        for ci in range(len(CAKES)):
            if st["baked"][ci] > 50:
                m = st["pts"][ci] / st["baked"][ci]
                POT[ci] = 0.5 * POT.get(ci, m) + 0.5 * m
            else:
                POT[ci] = POT.get(ci, 0) * 0.5 + 0.5 * potential(ci) * 0.6

class P:
    def __init__(self, ai):
        self.ai = ai; self.racks = []; self.score = 0; self.rest = False; self.fx = True
        self.pulled = []; self.nbake = 0

class Game:
    def __init__(self, seed, ai0, ai1=None, solo=False, leftover=0.0, counter_n=None, racks=2,
                 stats=None, p2_start_day2=True, slam=True, slam_mode='early', days=2, wash='sold', rival=False):
        self.r = random.Random(seed); self.solo = solo; self.leftover = leftover
        self.N = counter_n or (3 if solo else 4); self.nracks = racks
        self.pl = [P(ai0)] + ([] if solo else [P(ai1)])
        self.deck = list(range(18)); self.r.shuffle(self.deck)
        self.disc = []; self.counter = []; self.day = 1
        self.rival = rival; self.days = days; self.wash = wash; self.sold = []; self.slam_on = slam; self.slam_mode = slam_mode; self.nslam = 0; self.stats = stats; self.turns = 0; self.pi = 0; self.done = False; self.p2d2 = p2_start_day2
        self.setup()

    # ---- helpers
    def refill(self):
        while len(self.counter) < self.N and self.deck:
            self.counter.append(self.deck.pop())

    def setup(self):
        face = [self.deck.pop() for _ in range(3)]
        order = [0] if self.solo else ([0, 1] if self.rival else [1, 0])
        for pi in order:
            p = self.pl[pi]
            pick = p.ai.pick_start(self, p, face)
            face.remove(pick); self.place(p, pick)
        self.counter = face; self.refill()

    def place(self, p, ci):
        st = 1 if CAKES[ci][3] == "preheated" else 0
        p.racks.append({"c": ci, "st": st}); p.nbake += 1
        if self.stats is not None: self.stats["baked"][ci] += 1

    def opp(self, pi): return None if self.solo else self.pl[1 - pi]

    def burn(self, p, cake):
        p.racks.remove(cake); self.disc.append(cake["c"])
        if self.stats is not None: self.stats["burnt"][cake["c"]] += 1

    def advance(self, cake, owner):
        cake["st"] += 1
        if cake["st"] > 3: self.burn(owner, cake)

    def pull(self, pi, cake):
        p = self.pl[pi]; ci = cake["c"]; v = val(ci, cake["st"])
        p.racks.remove(cake); gain = v
        eff = CAKES[ci][2]
        if p.fx is not True and eff not in (p.fx or ()): eff = "none"
        if eff == "tip": gain += 1
        if eff == "glaze": gain += len(p.racks)
        p.score += gain; self.disc_after = ci
        if self.stats is not None:
            self.stats["pulls"][ci] += 1; self.stats["pts"][ci] += gain
            self.stats["stage"][ci][cake["st"]] += 1
        # effects that act
        if eff == "fresh":
            self.disc += self.counter; self.counter = []; self.refill()
        elif eff == "free_slam" and not self.solo:
            self.slam_target(pi, free=True)
        elif eff == "rest": p.rest = True
        elif eff == "draw" and self.deck:
            self.use_card(pi, self.deck.pop())
        elif eff == "scrap" and self.disc:
            self.use_card(pi, self.disc.pop())
        elif eff == "twofor" and self.counter:
            c = p.ai.choose_counter(self, pi); self.counter.remove(c); self.use_card(pi, c)
        self.disc.append(ci); self.sold.append(ci)

    def slam_target(self, pi, free=False, card=None):
        o = self.opp(pi)
        if o is None or not o.racks or not self.slam_on: return False
        pool = self.slammable(o, free)
        if not pool: return False
        self.nslam += 1
        tgt = self.pl[pi].ai.pick_slam(self, pi, pool)
        if tgt is None: return False
        if CAKES[tgt["c"]][3] != "sturdy": self.advance(tgt, o)
        return True

    def slammable(self, o, free):
        """Cakes a basic slam may target (free effect slams can hit anything)."""
        if free or self.slam_mode == "basic": return list(o.racks)
        if self.slam_mode == "effects": return []
        if self.slam_mode == "early": return [c for c in o.racks if c["st"] <= 1]
        if self.slam_mode == "mid": return [c for c in o.racks if 1 <= c["st"] <= 2]
        return list(o.racks)

    def legal_uses(self, pi):
        p = self.pl[pi]; u = ["bin"]
        if len(p.racks) < self.nracks: u.append("bake")
        o = self.opp(pi)
        if o is not None and self.slammable(o, False) and self.slam_on: u.append("slam")
        return u

    def use_card(self, pi, ci):
        p = self.pl[pi]; how = p.ai.choose_use(self, pi, ci)
        if how == "bake" and len(p.racks) < self.nracks: self.place(p, ci)
        elif how == "slam" and self.slam_target(pi, card=ci): self.disc.append(ci)
        else: self.disc.append(ci)

    # ---- turn
    def rotate(self, pi):
        p = self.pl[pi]
        if p.rest: p.rest = False
        else:
            for c in list(p.racks): self.advance(c, p)

    def apply(self, pi, act):
        p = self.pl[pi]
        if act[0] == "pull": self.pull(pi, act[1])
        elif act[0] == "take":
            _, ci, how = act; self.counter.remove(ci)
            if how == "bake": self.place(p, ci)
            elif how == "slam":
                self.slam_target(pi); self.disc.append(ci)
            else: self.disc.append(ci)

    def end_turn(self):
        if self.solo and self.counter:       # oldest card goes cold and leaves the game
            self.counter.pop(0)
        self.refill()

    def turn(self, pi):
        self.rotate(pi)
        ai = self.pl[pi].ai
        self.apply(pi, ai.choose(self, pi))
        if getattr(ai, "again", False):
            ai.again = False
            self.apply(pi, ai.choose(self, pi))
        self.end_turn()

    def day_over(self): return not self.deck and not self.counter

    def post_turn(self, pi):
        if self.day_over():
            if self.day >= self.days: self.done = True; return
            self.day += 1
            self.deck = self.disc if self.wash == 'all' else [c for c in self.disc if c in self.sold]
            self.disc = []; self.r.shuffle(self.deck)
            self.refill()
            if self.day_over(): self.done = True; return
            self.pi = 1 if (self.p2d2 and not self.solo) else pi
            return
        self.pi = pi if self.solo else 1 - pi

    def step(self):
        pi = self.pi; self.turn(pi); self.turns += 1; self.post_turn(pi)

    def final(self):
        for p in self.pl:
            for c in p.racks:
                p.score += int(val(c["c"], c["st"]) * self.leftover)
        return [p.score for p in self.pl]

    def run(self):
        self.pi = 0; self.done = False
        while not self.done: self.step()
        return self.final()

# ------------------------------------------------------------------ AIs
class Strong:
    name = "strong"
    eps = 0.0
    def pick_start(self, g, p, face): return max(face, key=potential)
    def pull_gain(self, g, pi, c):
        s = c["st"]; v = val(c["c"], s); e = EFFVAL[CAKES[c["c"]][2]]
        w = val(c["c"], s + 1)
        if not g.solo and CAKES[c["c"]][3] != "sturdy":
            w = 0.85 * w + 0.15 * val(c["c"], s + 2)
        return v + e - w
    def pick_slam(self, g, pi, pool):
        cand = [c for c in pool if CAKES[c["c"]][3] != "sturdy"]
        if not cand: return pool[0]
        return max(cand, key=lambda c: val(c["c"], c["st"] + 1) - val(c["c"], c["st"] + 2))
    def slam_dmg(self, g, pi):
        o = g.opp(pi); best = 0
        for c in g.slammable(o, False):
            if CAKES[c["c"]][3] == "sturdy": continue
            best = max(best, val(c["c"], c["st"] + 1) - val(c["c"], c["st"] + 2))
        return best
    def choose_counter(self, g, pi): return max(g.counter, key=potential)
    def choose_use(self, g, pi, ci):
        p = g.pl[pi]
        if len(p.racks) < g.nracks: return "bake"
        if not g.solo and g.slam_on and g.slammable(g.opp(pi), False) and self.slam_dmg(g, pi) >= 3: return "slam"
        return "bin"
    def choose(self, g, pi):
        p = g.pl[pi]; opts = []
        if self.eps and g.counter and len(p.racks) < g.nracks and g.r.random() < self.eps:
            if not any(c["st"] >= 1 and val(c["c"], c["st"]) >= 5 for c in p.racks):
                return ("take", g.r.choice(g.counter), "bake")
        for c in p.racks:
            if c["st"] >= 1:
                gn = self.pull_gain(g, pi, c)
                opts.append((gn + 1.5 if gn > 0 else gn * 0.3 - 0.5, ("pull", c)))
        free = len(p.racks) < g.nracks
        if g.counter:
            best = max(g.counter, key=potential)
            if free:
                opts.append((0.6 * potential(best) + 0.8, ("take", best, "bake")))
            if not g.solo and g.slam_on and g.slammable(g.opp(pi), False):
                dmg = self.slam_dmg(g, pi)
                junk = min(g.counter, key=potential)
                opts.append((dmg * 0.95 - 0.25 * potential(junk) + 0.1, ("take", junk, "slam")))
            # deny / stall: bin the juiciest card
            opts.append((0.25 * potential(best) - 0.6, ("take", best, "bin")))
        if not opts:
            return ("pass",)
        if not g.counter:   # forced to pull if we can
            pulls = [o for o in opts if o[1][0] == "pull"]
            if pulls: return max(pulls, key=lambda o: val(o[1][1]["c"], o[1][1]["st"]))[1]
        return max(opts, key=lambda o: o[0])[1]

class Casual(Strong):
    name = "casual"
    def pick_start(self, g, p, face): return max(face, key=lambda c: max(CAKES[c][1]))
    def choose(self, g, pi):
        p = g.pl[pi]
        pulls = [c for c in p.racks if c["st"] >= 1 and (val(c["c"], c["st"]) >= 5 or c["st"] == 3)]
        if pulls: return ("pull", max(pulls, key=lambda c: val(c["c"], c["st"])))
        if g.counter and len(p.racks) < g.nracks:
            return ("take", max(g.counter, key=lambda c: max(CAKES[c][1])), "bake")
        ready = [c for c in p.racks if c["st"] >= 1]
        if not g.counter and ready: return ("pull", max(ready, key=lambda c: val(c["c"], c["st"])))
        if g.counter: return ("take", g.counter[0], "bin")
        return ("pass",)
    def choose_use(self, g, pi, ci):
        return "bake" if len(g.pl[pi].racks) < g.nracks else "bin"
    def pick_slam(self, g, pi, pool): return None

AIS = {"strong": Strong, "casual": Casual}

# ------------------------------------------------------------------ harness
def new_stats():
    return {"baked": defaultdict(int), "pulls": defaultdict(int), "pts": defaultdict(int),
            "burnt": defaultdict(int), "stage": defaultdict(lambda: defaultdict(int))}

def two_player(a, b, n=4000, seed=1, **kw):
    w = [0, 0, 0]; sc = [[], []]; turns = []; st = new_stats()
    for i in range(n):
        g = Game(seed * 100000 + i, AIS[a](), AIS[b](), stats=st, **kw)
        s = g.run(); sc[0].append(s[0]); sc[1].append(s[1]); turns.append(g.turns)
        w[0 if s[0] > s[1] else 1 if s[1] > s[0] else 2] += 1
    return {"p1": w[0] / n, "p2": w[1] / n, "tie": w[2] / n, "m1": statistics.mean(sc[0]),
            "m2": statistics.mean(sc[1]), "turns": statistics.mean(turns) / 2, "stats": st, "n": n}

def solo(ai="strong", n=6000, seed=7, **kw):
    sc = []; st = new_stats(); t = []
    for i in range(n):
        g = Game(seed * 100000 + i, AIS[ai](), solo=True, stats=st, **kw)
        sc.append(g.run()[0]); t.append(g.turns)
    return sc, st, statistics.mean(t)

def pct(xs, q):
    s = sorted(xs); return s[min(len(s) - 1, int(q * len(s)))]

if __name__ == "__main__":
    for lo in (0.0, 0.5, 1.0):
        r = two_player("strong", "strong", n=3000, leftover=lo)
        print(f"2p strong v strong leftover x{lo}: P1 {r['p1']:.1%} P2 {r['p2']:.1%} tie {r['tie']:.1%} "
              f"mean {r['m1']:.1f}/{r['m2']:.1f} turns each {r['turns']:.1f}")
    r = two_player("strong", "casual", n=3000)
    print(f"strong(P1) v casual(P2): {r['p1']:.1%} / {r['p2']:.1%}")
    r = two_player("casual", "strong", n=3000)
    print(f"casual(P1) v strong(P2): {r['p1']:.1%} / {r['p2']:.1%}")
    for ai in ("casual", "strong"):
        sc, st, t = solo(ai, n=4000)
        print(ai, "solo mean", round(statistics.mean(sc), 1), "turns", round(t, 1),
              "p10/25/50/75/90/97", [pct(sc, q) for q in (.1, .25, .5, .75, .9, .97)])
