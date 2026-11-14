"""The Rival Baker: an automated Player 2 driven by a deck of rival cards (solo versus mode).

The 'usual list' is what the rival does unless its card says otherwise. Every rule here has to be
something a person can carry out from the card text, without judgement calls.
"""
import sys, statistics
from sim import *

RIVAL_CARDS = ["By the book", "Newest first", "Early bird", "Door slammer", "Sweet tooth", "Regular customer"]

DOOR_T = 2; EARLY = 5; REGULAR = 1; B2B_SECOND = 'Back-to-back 2'

class Rival:
    name = "rival"
    def __init__(self, cards=None):
        self.cards = list(cards or RIVAL_CARDS); self.deck = []; self.again = False; self.card = None
        self.pick_rule = "peak"
    # ---- setup
    def pick_start(self, g, p, face): return face[0]
    def choose_counter(self, g, pi): return g.counter[-1]
    def choose_use(self, g, pi, ci): return "bake" if len(g.pl[pi].racks) < g.nracks else "bin"
    def pick_slam(self, g, pi, pool):
        ok = [c for c in pool if CAKES[c["c"]][3] != "sturdy"] or pool   # Water bath cakes can't be slammed
        return max(ok, key=lambda c: val(c["c"], c["st"] + 1) - val(c["c"], c["st"] + 2))
    # ---- helpers the printed card text mirrors
    def order(self, g, rev): return list(reversed(g.counter)) if rev else list(g.counter)
    def pull_target(self, p):
        """A cake that can't get any better: next number is not higher, or it is Dark. Highest number first."""
        c = [c for c in p.racks if c["st"] >= 1 and (c["st"] == 3 or val(c["c"], c["st"]) >= val(c["c"], c["st"] + 1))]
        return max(c, key=lambda c: val(c["c"], c["st"])) if c else None
    def slam_target(self, g, pi, thresh):
        o = g.opp(pi)
        if not g.slam_on: return None
        pool = [c for c in g.slammable(o, False) if CAKES[c["c"]][3] != "sturdy"]
        best, bd = None, thresh - 1
        for c in pool:
            d = val(c["c"], c["st"] + 1) - val(c["c"], c["st"] + 2)
            if d > bd: best, bd = c, d
        return best
    def bake_card(self, g, p, rev, key):
        if len(p.racks) >= g.nracks or not g.counter: return None
        cards = self.order(g, rev)
        best = cards[0]
        for c in cards[1:]:
            if key(c) > key(best): best = c
        return best
    def junk_card(self, g, rev):
        cards = self.order(g, rev)
        return min(cards, key=lambda c: max(CAKES[c][1]))   # first of the smallest-peak cards
    peak = staticmethod(lambda c: max(CAKES[c][1]))
    dark = staticmethod(lambda c: (CAKES[c][1][2], max(CAKES[c][1])))
    # ---- one action by the list
    def act(self, g, pi, card):
        p = g.pl[pi]; rev = card == "Newest first"
        key = self.dark if card == "Sweet tooth" else self.peak
        steps = ["pull", "slam", "bake", "bin"]
        if card == "Door slammer": steps = ["slam", "pull", "bake", "bin"]
        if card == "Back-to-back 2": steps = ["pull", "bake"]
        thresh = DOOR_T if card == "Door slammer" else 3
        if card == "Early bird":
            e = [c for c in p.racks if c["st"] >= 1 and val(c["c"], c["st"]) >= EARLY]
            if e: return ("pull", max(e, key=lambda c: val(c["c"], c["st"])))
        for s in steps:
            if s == "pull":
                t = self.pull_target(p)
                if t: return ("pull", t)
            elif s == "slam" and g.counter:
                t = self.slam_target(g, pi, thresh)
                if t is not None: return ("take", self.junk_card(g, rev), "slam")
            elif s == "bake":
                c = self.bake_card(g, p, rev, key)
                if c is not None: return ("take", c, "bake")
            elif s == "bin" and g.counter:
                return ("take", self.order(g, rev)[0], "bin")
        ready = [c for c in p.racks if c["st"] >= 1]
        if ready: return ("pull", max(ready, key=lambda c: val(c["c"], c["st"])))
        return ("pass",)
    def choose(self, g, pi):
        if self.again:                       # second action of Back-to-back
            return self.act(g, pi, B2B_SECOND)
        if not self.deck:
            self.deck = list(self.cards); g.r.shuffle(self.deck)
        self.card = self.deck.pop()
        if self.card == "Regular customer": g.pl[pi].score += REGULAR
        return self.act(g, pi, self.card if self.card != "Regular customer" else "By the book")

def versus(human, n=3000, seed=11, cards=None, **kw):
    w = [0, 0, 0]; sc = [[], []]; t = []
    for i in range(n):
        g = Game(seed * 100000 + i, AIS[human](), Rival(cards), rival=True, **kw)
        g.pl[1].fx = False
        s = g.run(); sc[0].append(s[0]); sc[1].append(s[1]); t.append(g.turns)
        # ties go to the rival
        w[0 if s[0] > s[1] else 1] += 1
    return {"human": w[0] / n, "rival": w[1] / n, "mh": statistics.mean(sc[0]), "mr": statistics.mean(sc[1]), "turns": statistics.mean(t) / 2}

if __name__ == "__main__":
    learn_potentials(rounds=2, n=800)
    for h in ("casual", "strong"):
        r = versus(h)
        print(f"{h:7s} wins {r['human']:.0%}  scores {r['mh']:.1f} v {r['mr']:.1f}  turns each {r['turns']:.1f}")
