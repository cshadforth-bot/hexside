import sys, statistics, json
from sim import *
from solo_mc import MC
learn_potentials(rounds=2, n=800)
res = {}
sc,_,t = solo("casual", n=6000); res["casual"] = sc
for name,K,n in (("good",2,500),("expert",10,500)):
    class M(MC): pass
    M.K = K; xs=[]
    for i in range(n): xs.append(Game(555000+i, M(), solo=True).run()[0])
    res[name]=xs
for k,v in res.items():
    print(f"{k:7s} n={len(v):5d} mean {statistics.mean(v):5.1f}  p5/10/25/50/75/90/95/99 {[pct(v,q) for q in (.05,.1,.25,.5,.75,.9,.95,.99)]}")
json.dump(res, open("solo_scores.json","w"))
