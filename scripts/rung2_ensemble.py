# NOTE (Copilot review): full reorth retains the Lanczos basis, O(m*n*probes) GPU
# memory; kept ON because near-kernel accuracy requires it (see RUNG2_GATE_RESULT.md).
# reorth memory note
#!/usr/bin/env python
"""Rung 2 density discriminator — GUE ensemble band vs zeta.

For each GUE draw: build the local sheaf (matched to zeta_L: N=1000, K=100,
superposition, edge-target 2492), compute the EXACT Frobenius rigidity ||L||_F
and Tr(L), plus the GPU bulk-beta heat trace. Checkpoint one JSON per draw.
zeta reference is the cached zeta_L.npz. Answers: is zeta outside the GUE band?
"""
import json, os, sys, time, warnings; warnings.filterwarnings("ignore")
import numpy as np, scipy.sparse as sp
from scipy.linalg import eigvalsh_tridiagonal, eigh_tridiagonal
from scipy.spatial.distance import pdist

JTOPO = os.environ.get("JTOPO_PATH", "C:/Users/JT-DEV1/Desktop/development/JTopo"); sys.path.insert(0, JTOPO)
OUT="output/rung2_ensemble"; os.makedirs(OUT, exist_ok=True)
BETAS=[0.5,1,2,3,5]; N,K=1000,100; TARGET=2492

def zeta_pts():
    from atft.feature_maps.spectral_unfolding import SpectralUnfolding
    from atft.sources.zeta_zeros import ZetaZerosSource
    src=ZetaZerosSource(JTOPO+"/data/odlyzko_zeros.txt")
    z=SpectralUnfolding(method="zeta").transform(src.generate(N)).points[:,0]
    return z, float(z.min()), float(z.max())

def gue_pts(seed, zmin, zmax):
    r=np.random.default_rng(seed); diag=r.standard_normal(N)
    sub=np.sqrt(r.chisquare(2.0*np.arange(N-1,0,-1)))/np.sqrt(2.0)
    e=np.sort(eigvalsh_tridiagonal(diag,sub)/np.sqrt(2.0*N)); s=np.diff(e)
    sc=s*((zmax-zmin)/(N-1)/s.mean()); p=np.zeros(N); p[0]=zmin; p[1:]=zmin+np.cumsum(sc); return p

def build_L(pts):
    from atft.topology.sparse_sheaf_laplacian import SparseSheafLaplacian
    from atft.topology.transport_maps import TransportMapBuilder
    def ne(eps): return int(np.sum(pdist(pts.reshape(-1,1))<=eps))
    lo,hi=0.01,20.0
    for _ in range(40):
        m=0.5*(lo+hi)
        if ne(m)<TARGET: lo=m
        else: hi=m
    eps = hi
    b=TransportMapBuilder(K=K,sigma=0.5); lap=SparseSheafLaplacian(b,pts,transport_mode="superposition")
    L=lap.build_matrix(eps); return ((L+L.getH())*0.5).tocsr(), eps, ne(eps)

def heat_gpu(L, m=150, npb=80, dev=0, seed=0):
    import cupy as cp, cupyx.scipy.sparse as csp
    with cp.cuda.Device(dev):
        Lg=csp.csr_matrix(L.astype(np.float64)); n=L.shape[0]
        r=cp.random.RandomState(seed); Z=(r.randint(0,2,(n,npb),dtype=cp.int32)*2-1).astype(cp.float64)
        Q=Z/cp.sqrt(cp.sum(Z*Z,axis=0)); Qp=cp.zeros_like(Q); bet=cp.zeros(npb)
        A=cp.empty((m,npb)); B=cp.empty((m,npb)); basis=[]
        for j in range(m):
            w=Lg@Q-bet*Qp; a=cp.sum(Q*w,axis=0); w=w-a*Q
            for Qi in basis: w=w-cp.sum(Qi*w,axis=0)*Qi
            bet=cp.sqrt(cp.sum(w*w,axis=0))+1e-300; A[j]=a;B[j]=bet;Qp=Q;Q=w/bet;basis.append(Qp)
        A=cp.asnumpy(A);B=cp.asnumpy(B); basis.clear(); cp.get_default_memory_pool().free_all_blocks()
    th=[];ta=[]
    for v in range(npb):
        t_,V=eigh_tridiagonal(A[:,v],B[:-1,v]); th.append(t_); ta.append(V[0,:]**2)
    return {str(be): float(np.mean([n*np.sum(ta[v]*np.exp(-be*th[v])) for v in range(npb)])) for be in BETAS}

def frob(L):
    d=L.data; return float(np.sqrt((np.abs(d)**2).sum())), float(np.real(L.diagonal()).sum())

def main():
    seeds=list(range(2001,2013))  # 12 GUE draws (2000 already cached)
    _, zmin, zmax = zeta_pts()
    for seed in seeds:
        ck=f"{OUT}/gue_{seed}.json"
        if os.path.exists(ck): print(f"skip {seed}", flush=True); continue
        t=time.time(); L,eps,edges=build_L(gue_pts(seed, zmin, zmax))
        fro,trL=frob(L); ht=heat_gpu(L)
        json.dump({"seed":seed,"edges":edges,"eps":eps,"frob":fro,"trL":trL,"heat":ht,"t_s":round(time.time()-t,0)}, open(ck,"w"), indent=1)
        print(f"gue_{seed}: edges={edges} ||L||_F={fro:.1f} Tr={trL:.0f} heat(b=1)={ht['1']:.0f} ({time.time()-t:.0f}s)", flush=True)
    # zeta reference (Frobenius from cache; heat already computed earlier = 10426 at b=1)
    zL=sp.load_npz("zeta_L.npz"); zf,ztr=frob(zL)
    print(f"\nZETA ref: ||L||_F={zf:.1f} Tr={ztr:.0f}", flush=True)
    fs=[json.load(open(f"{OUT}/{f}"))["frob"] for f in os.listdir(OUT) if f.startswith("gue_")]
    if fs:
        fs=np.array(fs); z=(zf-fs.mean())/fs.std()
        print(f"GUE ||L||_F band: {fs.mean():.1f} +/- {fs.std():.1f}  [{fs.min():.1f},{fs.max():.1f}]  (n={len(fs)})", flush=True)
        print(f"zeta ||L||_F={zf:.1f} -> z-score {z:.1f}  {'OUTSIDE (below) band' if zf<fs.min() else 'inside band'}", flush=True)

if __name__=="__main__": main()
