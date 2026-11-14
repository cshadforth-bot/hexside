"""Solo expert: tests every legal option with determinized playouts (hidden deck re-shuffled)."""
import copy, random, sys, statistics
from sim import *

class MC(Strong):
    name = "expert"
    K = 10
    def pick_start(self, g, p, face): return max(face, key=lambda c: max(CAKES[c][1]))
    def choose_use(self, g, pi, ci): return "bake" if len(g.pl[pi].racks) < g.nracks else "bin"
    def pick_slam(self, g, pi, pool): return None
    def options(self, g, pi):
        p = g.pl[pi]; o = []
        for c in p.racks:
            if c["st"] >= 1: o.append(("pull", p.racks.index(c)))
        seen = set()
        for ci in g.counter:
            if ci in seen: continue
            seen.add(ci)
            if len(p.racks) < g.nracks: o.append(("take", ci, "bake"))
            o.append(("take", ci, "bin"))
        return o or [("pass",)]
    def concrete(self, g, pi, a):
        return ("pull", g.pl[pi].racks[a[1]]) if a[0] == "pull" else a
    def choose(self, g, pi):
        opts = self.options(g, pi); best = None; bs = -1
        for a in opts:
            tot = 0
            for k in range(self.K):
                g2 = copy.deepcopy(g); g2.r = random.Random(g.r.random())
                g2.r.shuffle(g2.deck); g2.pl[pi].ai = Casual()
                g2.stats = None
                g2.apply(pi, self.concrete(g2, pi, a)); g2.end_turn(); g2.turns += 1; g2.post_turn(pi)
                while not g2.done: g2.step()
                tot += g2.final()[0]
            if tot > bs: bs, best = tot, a
        return self.concrete(g, pi, best)

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    AIS["expert"] = MC
    sc = []
    for i in range(n):
        g = Game(424242 + i, MC(), solo=True); sc.append(g.run()[0])
    print("expert solo", n, "games: mean", round(statistics.mean(sc), 1), "p5/25/50/75/95",
          [pct(sc, q) for q in (.05, .25, .5, .75, .95)], "max", max(sc))
