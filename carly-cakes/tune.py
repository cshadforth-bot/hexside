"""Shape-preserving tuner: each cake keeps its dial profile (when it peaks, how it collapses);
only the peak value moves, so every card earns about the same points per bake."""
import sim, sys, json
from sim import *
KW = dict(slam_mode="early")
T = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 10
shape = {}
for ci, (n, d, e, q) in enumerate(sim.CAKES):
    pk = max(d); shape[ci] = [x / pk for x in d]; peak = {ci: float(pk) for ci in range(18)} if ci == 0 else peak
for rd in range(rounds):
    learn_potentials(rounds=2, n=1000, **KW)
    class Explore(Strong): eps = 0.2
    st = new_stats()
    for i in range(3000): Game(777000 + rd * 5000 + i, Explore(), Explore(), stats=st, **KW).run()
    ms = []
    for ci, (n, d, e, q) in enumerate(sim.CAKES):
        m = st["pts"][ci] / max(st["baked"][ci], 1); ms.append(m)
        peak[ci] = min(9.4, max(3.0, peak[ci] * (1 + 0.5 * (T - m) / T)))
        nd = tuple(int(round(r * peak[ci])) for r in shape[ci])
        sim.CAKES[ci] = (n, nd, e, q)
    print(rd, "sd", round(statistics.pstdev(ms), 2), "min", round(min(ms), 1), "max", round(max(ms), 1))
for c in sim.CAKES: print(c)
json.dump(sim.CAKES, open("cakes_tuned.json", "w"))
