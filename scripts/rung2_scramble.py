#!/usr/bin/env python
"""Rung 2 attribution gate — scrambling controls.

zeta's local sheaf is more rigid than the GUE band (||L||_F=1746 vs ~1794).
Is that from the PRIME phases (arithmetic) or the GEOMETRY (positions)?

Keep zeta's exact point geometry + fiber bases; scramble ONLY the prime-frequency
structure in the superposition transport (A[e] = sum_p e^{i dg log p} B_p):
  - freq-random : log(p) -> uniform random in [min,max] (destroy specific freqs)
  - prime-perm  : log(p) -> a permutation (same set, wrong assignment)
Then rebuild the sheaf and measure ||L||_F.

Decision:
  scrambled ||L||_F rises to the GUE band (~1794)  => rigidity is ARITHMETIC (primes cause it)
  scrambled ||L||_F stays at zeta baseline (~1746) => rigidity is GEOMETRIC (not primes)
"""
import json, os, sys, time, warnings; warnings.filterwarnings("ignore")
import numpy as np
from scipy.spatial.distance import pdist
JTOPO = os.environ.get("JTOPO_PATH", "C:/Users/JT-DEV1/Desktop/development/JTopo"); sys.path.insert(0, JTOPO)
from atft.feature_maps.spectral_unfolding import SpectralUnfolding
from atft.sources.zeta_zeros import ZetaZerosSource
from atft.topology.sparse_sheaf_laplacian import SparseSheafLaplacian
from atft.topology.transport_maps import TransportMapBuilder
OUT="output/rung2_scramble"; os.makedirs(OUT, exist_ok=True)
N,K,TARGET=1000,100,2492

def frob(L):
    return float(np.sqrt((np.abs(L.data)**2).sum())), float(np.real(L.diagonal()).sum())

def zeta_points_eps():
    src=ZetaZerosSource(JTOPO+"/data/odlyzko_zeros.txt")
    z=SpectralUnfolding(method="zeta").transform(src.generate(N)).points[:,0]
    lo,hi=0.01,20.0
    for _ in range(40):
        m=0.5*(lo+hi)
        if int(np.sum(pdist(z.reshape(-1,1))<=m))<TARGET: lo=m
        else: hi=m
    return z, 0.5*(lo+hi)

def build_frob(z, eps, scramble=None, seed=0):
    b=TransportMapBuilder(K=K, sigma=0.5)
    b.build_superposition_bases()               # real prime bases + real _log_primes
    real=b._log_primes.copy()
    if scramble=="freq":  b._log_primes=np.random.default_rng(seed).uniform(real.min(), real.max(), len(real))
    elif scramble=="perm": b._log_primes=np.random.default_rng(seed).permutation(real)
    # else baseline (real)
    lap=SparseSheafLaplacian(b, z, transport_mode="superposition")
    L=lap.build_matrix(eps); L=((L+L.getH())*0.5).tocsr()
    return frob(L)

def main():
    z, eps = zeta_points_eps()
    # verify monkeypatch: baseline must reproduce ~1746
    t=time.time(); bf,btr=build_frob(z,eps,None)
    print(f"zeta BASELINE (real primes): ||L||_F={bf:.1f} Tr={btr:.0f}  ({time.time()-t:.0f}s) [expect ~1746]", flush=True)
    json.dump({"kind":"baseline","frob":bf,"tr":btr}, open(f"{OUT}/baseline.json","w"))
    for kind in ("freq","perm"):
        for seed in range(5):
            ck=f"{OUT}/{kind}_{seed}.json"
            if os.path.exists(ck): continue
            t=time.time(); f,tr=build_frob(z,eps,kind,seed)
            json.dump({"kind":kind,"seed":seed,"frob":f,"tr":tr}, open(ck,"w"))
            print(f"zeta {kind}_{seed}: ||L||_F={f:.1f} Tr={tr:.0f}  ({time.time()-t:.0f}s)", flush=True)
    # verdict
    def band(kind):
        v=[json.load(open(f"{OUT}/{f}"))["frob"] for f in os.listdir(OUT) if f.startswith(kind+"_")]
        return np.array(v)
    print("\n=== VERDICT ===", flush=True)
    print(f"zeta baseline (primes): {bf:.1f}", flush=True)
    print(f"GUE band (from ensemble): ~1791-1796", flush=True)
    for kind in ("freq","perm"):
        v=band(kind)
        if len(v):
            toward = "-> GUE band (ARITHMETIC: primes cause rigidity)" if v.mean()>1775 else ("-> stays at zeta baseline (GEOMETRIC: not primes)" if v.mean()<1760 else "-> intermediate")
            print(f"{kind}-scramble ||L||_F = {v.mean():.1f} +/- {v.std():.1f}  {toward}", flush=True)

if __name__=="__main__": main()
