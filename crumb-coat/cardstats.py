import sys
from sim import *
kw = {}
for a in sys.argv[1:]:
    k,v = a.split('='); kw[k] = eval(v)
learn_potentials(**kw)
st = new_stats(); w=[0,0,0]; ns=0; N=4000; sc=[]; tt=[]
for i in range(N):
    g = Game(5000000+i, Strong(), Strong(), stats=st, **kw); s=g.run(); ns+=g.nslam; tt.append(g.turns/2)
    w[0 if s[0]>s[1] else 1 if s[1]>s[0] else 2]+=1; sc+=s
print(f"{kw}: P1 {w[0]/N:.1%} P2 {w[1]/N:.1%} tie {w[2]/N:.1%} mean {statistics.mean(sc):.1f} turns {statistics.mean(tt):.1f} slams/game {ns/N:.2f}")
r = two_player("strong","casual",n=2000,**kw); print(f"  strong beats casual {r['p1']:.1%}  (casual P1 vs strong: {two_player('casual','strong',n=2000,**kw)['p2']:.1%})")
if '-v' in sys.argv or True:
    print(f"  {'card':16s} {'baked':>5s} pts/bake burn%")
    for i,(n,d,e,q) in enumerate(CAKES):
        b=st['baked'][i]
        print(f"  {n:16s} {b:5d}  {st['pts'][i]/max(b,1):6.2f}  {100*st['burnt'][i]/max(b,1):4.0f}")
