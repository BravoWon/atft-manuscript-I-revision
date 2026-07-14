#!/usr/bin/env python
"""Rung 2 fluctuation channel (exact CPU).

Number variance is a FLUCTUATION statistic -> needs exact eigenvalue positions
(RUNG2_GATE_RESULT.md: not stochastic-trace-computable). So: small sheaf
(dim ~6400), DENSE eigvalsh for the full spectrum, then Sigma^2_spec(L) of the
unfolded sheaf eigenvalues. Compare zeta vs GUE ensemble; if zeta separates,
scrambling controls attribute it (arithmetic <-> geometric), same rail that
showed the density channel is geometric.
"""
import json, os, sys, time, warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.spatial.distance import pdist
from scipy.linalg import eigvalsh_tridiagonal
JTOPO="C:/Users/JT-DEV1/Desktop/development/JTopo"; sys.path.insert(0, JTOPO)
from atft.feature_maps.spectral_unfolding import SpectralUnfolding
from atft.sources.zeta_zeros import ZetaZerosSource
from atft.topology.sparse_sheaf_laplacian import SparseSheafLaplacian
from atft.topology.transport_maps import TransportMapBuilder
OUT="output/rung2_fluct"; os.makedirs(OUT, exist_ok=True)
Npts, K, TARGET = 64, 100, 200   # dim = 6400; edge target scaled to N
LG=[2,5,10,20,50,100]

def eps_for(pts):
    lo,hi=0.01,20.0
    for _ in range(40):
        m=0.5*(lo+hi)
        if int(np.sum(pdist(pts.reshape(-1,1))<=m))<TARGET: lo=m
        else: hi=m
    return 0.5*(lo+hi)

def numvar(eigs):
    p=np.polyfit(eigs, np.arange(len(eigs),dtype=float), 15); u=np.polyval(p,eigs); u=u-u[0]
    r=np.random.default_rng(1); out={}
    for Lw in LG:
        s=r.uniform(u[0],u[-1]-Lw,6000); c=np.searchsorted(u,s+Lw)-np.searchsorted(u,s); out[Lw]=float(c.var())
    return out

def build_eig(pts, eps, scramble=None, seed=0):
    b=TransportMapBuilder(K=K,sigma=0.5); b.build_superposition_bases(); real=b._log_primes.copy()
    if scramble=="freq": b._log_primes=np.random.default_rng(seed).uniform(real.min(),real.max(),len(real))
    elif scramble=="zeros": b._log_primes=np.zeros_like(real)
    lap=SparseSheafLaplacian(b,pts,transport_mode="superposition")
    L=lap.build_matrix(eps); L=((L+L.getH())*0.5)
    return np.linalg.eigvalsh(L.toarray())

def zeta_pts():
    src=ZetaZerosSource(JTOPO+"/data/odlyzko_zeros.txt")
    z=SpectralUnfolding(method="zeta").transform(src.generate(Npts)).points[:,0]
    return z, float(z.min()), float(z.max())

def gue_pts(seed, zmin, zmax):
    r=np.random.default_rng(seed); diag=r.standard_normal(Npts)
    sub=np.sqrt(r.chisquare(2.0*np.arange(Npts-1,0,-1)))/np.sqrt(2.0)
    e=np.sort(eigvalsh_tridiagonal(diag,sub)/np.sqrt(2.0*Npts)); s=np.diff(e)
    sc=s*((zmax-zmin)/(Npts-1)/s.mean()); p=np.zeros(Npts); p[0]=zmin; p[1:]=zmin+np.cumsum(sc); return p

def main():
    z, zmin, zmax = zeta_pts(); ez=eps_for(z)
    # zeta
    if not os.path.exists(f"{OUT}/zeta.json"):
        t=time.time(); lam=build_eig(z,ez); json.dump({"nv":numvar(lam),"dim":len(lam)},open(f"{OUT}/zeta.json","w"))
        print(f"zeta: dim={len(lam)} nv={numvar(lam)} [{time.time()-t:.0f}s]",flush=True)
    # GUE ensemble
    for seed in range(3000,3008):
        ck=f"{OUT}/gue_{seed}.json"
        if os.path.exists(ck): continue
        pts=gue_pts(seed,zmin,zmax); t=time.time(); lam=build_eig(pts,eps_for(pts))
        json.dump({"nv":numvar(lam),"seed":seed},open(ck,"w")); print(f"gue_{seed}: nv(L=20)={numvar(lam)[20]:.2f} [{time.time()-t:.0f}s]",flush=True)
    # zeta scrambles
    for scr,seeds in (("freq",[0,1,2]),("zeros",[0])):
        for s in seeds:
            ck=f"{OUT}/zeta_{scr}_{s}.json"
            if os.path.exists(ck): continue
            t=time.time(); lam=build_eig(z,ez,scr,s); json.dump({"nv":numvar(lam),"scr":scr,"seed":s},open(ck,"w"))
            print(f"zeta_{scr}_{s}: nv(L=20)={numvar(lam)[20]:.2f} [{time.time()-t:.0f}s]",flush=True)
    # verdict
    zn=json.load(open(f"{OUT}/zeta.json"))["nv"]
    gv=[json.load(open(f"{OUT}/{f}"))["nv"] for f in os.listdir(OUT) if f.startswith("gue_")]
    scr={sc:[json.load(open(f"{OUT}/{f}"))["nv"] for f in os.listdir(OUT) if f.startswith(f"zeta_{sc}_")] for sc in ("freq","zeros")}
    print("\n=== SPECTRAL NUMBER VARIANCE Sigma^2_spec(L) ===",flush=True)
    print(f"{'L':>5} {'zeta':>8} {'GUE band':>20} {'zeta z':>7} | {'zeta-freq-scr':>13} {'zeta-zeros':>10}",flush=True)
    for Lw in LG:
        g=np.array([d[str(Lw)] for d in gv]); zz=zn[str(Lw)]
        zsc=np.mean([d[str(Lw)] for d in scr["freq"]]) if scr["freq"] else np.nan
        zzr=np.mean([d[str(Lw)] for d in scr["zeros"]]) if scr["zeros"] else np.nan
        z=(zz-g.mean())/(g.std()+1e-9)
        print(f"{Lw:>5} {zz:>8.2f} {g.mean():>8.2f}+/-{g.std():>5.2f}[{g.min():.1f},{g.max():.1f}] {z:>6.1f} | {zsc:>13.2f} {zzr:>10.2f}",flush=True)
    print("\nATTRIBUTION: if zeta separates AND scrambles stay at zeta (not GUE) -> geometric;",flush=True)
    print("             if scrambles move to GUE band -> ARITHMETIC (fluctuation carries primes).",flush=True)

if __name__=="__main__": main()
