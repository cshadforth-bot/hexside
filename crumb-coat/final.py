import json, statistics
from sim import *
learn_potentials(rounds=3, n=1500)
N = 10000; st = new_stats(); w=[0,0,0]; sc=[]; tt=[]; ns=0; margin=[]
for i in range(N):
    g = Game(9100000+i, Strong(), Strong(), stats=st); s=g.run(); ns+=g.nslam; tt.append(g.turns/2); sc+=s
    w[0 if s[0]>s[1] else 1 if s[1]>s[0] else 2]+=1; margin.append(abs(s[0]-s[1]))
a = two_player("strong","casual",n=3000)["p1"]; b = two_player("casual","strong",n=3000)["p2"]
exp = new_stats()
class Explore(Strong): eps = 0.2
for i in range(4000): Game(321000+i, Explore(), Explore(), stats=exp).run()
out = {"games": N, "p1": w[0]/N, "p2": w[1]/N, "tie": w[2]/N, "mean": statistics.mean(sc), "sd": statistics.pstdev(sc),
       "turns": statistics.mean(tt), "slams": ns/N, "skill": (a+b)/2, "median_margin": statistics.median(margin),
       "cards": [{"name":n,"dial":list(d),"eff":e,"quirk":q,"baked":st["baked"][i],
                  "ppb": exp["pts"][i]/max(exp["baked"][i],1), "burn": exp["burnt"][i]/max(exp["baked"][i],1)} for i,(n,d,e,q) in enumerate(CAKES)]}
json.dump(out, open("results.json","w"), indent=1)
print({k:(round(v,3) if isinstance(v,float) else v) for k,v in out.items() if k!="cards"})
for c in out["cards"]: print(f"{c['name']:16s} {str(tuple(c['dial'])):10s} {c['eff']:10s}{c['quirk']:10s} pts/bake {c['ppb']:.2f} burn {c['burn']:.0%}")
