"""Rival-aware planning bot: tries every legal option (including slams) with playouts against the Rival."""
import copy, random, sys
from rival import *
import solo_mc

RIVAL_FX = {"tip", "glaze", "free_slam", "draw", "scrap"}

class MCV(solo_mc.MC):
    name = "expert-v"
    def pick_start(self, g, p, face): return max(face, key=lambda c: max(CAKES[c][1]))
    def choose_use(self, g, pi, ci):
        return "bake" if len(g.pl[pi].racks) < g.nracks else "bin"
    def pick_slam(self, g, pi, pool):
        return max(pool, key=lambda c: val(c["c"], c["st"] + 1) - val(c["c"], c["st"] + 2))
    def options(self, g, pi):
        o = super().options(g, pi)
        opp = g.opp(pi)
        if g.slammable(opp, False):
            seen = set()
            for ci in g.counter:
                if ci not in seen: seen.add(ci); o.append(("take", ci, "slam"))
        return o
    def choose(self, g, pi):
        opts = self.options(g, pi); best = None; bs = -1e9
        for a in opts:
            tot = 0
            for k in range(self.K):
                g2 = copy.deepcopy(g); g2.r = random.Random(g.r.random()); g2.r.shuffle(g2.deck)
                g2.pl[pi].ai = Casual(); g2.stats = None
                g2.apply(pi, self.concrete(g2, pi, a)); g2.end_turn(); g2.turns += 1; g2.post_turn(pi)
                while not g2.done: g2.step()
                s = g2.final(); tot += (1 if s[0] > s[1] else 0) + 0.02 * (s[0] - s[1])
            if tot > bs: bs, best = tot, a
        return self.concrete(g, pi, best)

def play(ai, n, seed=77, fx=RIVAL_FX):
    w = 0; d = []
    for i in range(n):
        g = Game(seed * 10000 + i, ai(), Rival(), rival=True); g.pl[1].fx = fx
        s = g.run(); w += s[0] > s[1]; d.append(s[0] - s[1])
    return w / n, statistics.mean(d)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    for K in (3, 10):
        class M(MCV): pass
        M.K = K
        r = play(M, n); print(f"planning bot K={K}: wins {r[0]:.0%} over {n}, mean margin {r[1]:+.1f}")
