import sys, statistics
from sim import *
def run(label, N=3000, **kw):
    learn_potentials(rounds=3, n=1000, **kw)
    class Explore(Strong): eps = 0.2
    st = new_stats()
    for i in range(2500): Game(31000+i, Explore(), Explore(), stats=st, **kw).run()
    pb = [st["pts"][c]/max(st["baked"][c],1) for c in range(18)]
    stt = new_stats(); w=[0,0,0]; ns=0; sc=[]
    for i in range(N):
        g = Game(8000000+i, Strong(), Strong(), stats=stt, **kw); s=g.run(); ns+=g.nslam
        w[0 if s[0]>s[1] else 1 if s[1]>s[0] else 2]+=1; sc+=s
    a = two_player("strong","casual",n=1500,**kw)["p1"]; b = two_player("casual","strong",n=1500,**kw)["p2"]
    print(f"{label:34s} seats {w[0]/N:.0%}/{w[1]/N:.0%}  mean {statistics.mean(sc):4.1f}  slams {ns/N:.1f}  skill {(a+b)/2:.0%}  card sd {statistics.pstdev(pb):.2f}  min {min(pb):.1f} max {max(pb):.1f}")
    return pb
if __name__ == "__main__":
    for mode in ("basic","early","mid","effects"):
        run(f"slam_mode={mode}", slam_mode=mode)
