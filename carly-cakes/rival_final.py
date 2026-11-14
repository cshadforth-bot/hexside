import json, statistics
import rival
from rival_mc import *
learn_potentials(rounds=3, n=1200)
out = {}
for h in ("casual", "strong"):
    w = 0; d = []; mr = []; mh = []; n = 8000
    for i in range(n):
        g = Game(3300000 + i, AIS[h](), rival.Rival(), rival=True); g.pl[1].fx = RIVAL_FX
        s = g.run(); w += s[0] > s[1]; mh.append(s[0]); mr.append(s[1])
    out[h] = {"win": w / n, "human": statistics.mean(mh), "rival": statistics.mean(mr), "n": n}
class M(MCV): pass
M.K = 10
w, dm = play(M, 300, seed=91)
out["expert"] = {"win": w, "margin": dm, "n": 300}
# rival's own first-player lean: rival vs rival (two identical rivals)
w1 = 0; n = 4000
for i in range(n):
    g = Game(4400000 + i, rival.Rival(), rival.Rival(), rival=True); g.pl[0].fx = RIVAL_FX; g.pl[1].fx = RIVAL_FX
    s = g.run(); w1 += s[0] > s[1]
out["mirror_p1"] = w1 / n
json.dump(out, open("rival_results.json", "w"), indent=1); print(json.dumps(out, indent=1))
