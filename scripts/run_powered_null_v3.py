#!/usr/bin/env python
"""Powered edge-matched null, fleet v3 (per PREREGISTRATION AMENDMENT 2).

Primary solver: SPECTRAL-FLIP (validated audit method) — flip = 1.05*lam_max*I - L,
eigsh(flip, k=100, which='LA', tol=1e-6, ncv=256). Shift-invert kept ONLY as a
cross-check on a 3-source subset (expected to collapse on dense near-kernels).
Per-pair residual vectors persisted. 122 solves; checkpointed, resumable.

Env override: N_GUE (default 100), N_POISSON (default 20) let the ensemble be
resized without editing frozen params — any change is logged to AMENDMENT 3.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
JTOPO = Path(os.environ.get("JTOPO_PATH", "C:/Users/JT-DEV1/Desktop/development/JTopo"))
OUT = HERE / "output" / "powered_null_v3"
OUT.mkdir(parents=True, exist_ok=True)

N, SIGMA, K, KEIG, NCV = 1000, 0.5, 100, 100, 384  # bigger Krylov -> faster convergence on the dense near-kernel
TARGET_EDGES = 2492
TOL = 1e-6
SWEEP = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 3e-4, 1e-3, 2e-3]
CERT_RESIDUAL = 1e-5
WORKERS = int(os.environ.get("WORKERS", "6"))
N_GUE = int(os.environ.get("N_GUE", "100"))
N_POISSON = int(os.environ.get("N_POISSON", "20"))
CROSSCHECK = {"zeta", "gue_2000", "poisson_42"}  # also run shift-invert here


def _worker_init():
    # 2 threads/worker x 4 workers = 8 = physical cores (AMENDMENT 4: no oversubscription)
    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[v] = "2"


def _zeta_points():
    sys.path.insert(0, str(JTOPO))
    from atft.feature_maps.spectral_unfolding import SpectralUnfolding
    from atft.sources.zeta_zeros import ZetaZerosSource
    src = ZetaZerosSource(str(JTOPO / "data" / "odlyzko_zeros.txt"))
    return SpectralUnfolding(method="zeta").transform(src.generate(N)).points[:, 0]


def _points_for(task, z_min, z_max):
    import numpy as np
    from scipy.linalg import eigvalsh_tridiagonal
    kind, seed = task
    if kind == "zeta":
        return _zeta_points()
    if kind == "even":
        return np.linspace(z_min, z_max, N)
    rng = np.random.default_rng(seed)
    if kind == "poisson":
        return np.sort(rng.uniform(z_min, z_max, N))
    diag = rng.standard_normal(N)
    dof = 2.0 * np.arange(N - 1, 0, -1, dtype=np.float64)
    sub = np.sqrt(rng.chisquare(dof)) / np.sqrt(2.0)
    e = np.sort(eigvalsh_tridiagonal(diag, sub) / np.sqrt(2.0 * N))
    s = np.diff(e)
    sc = s * ((z_max - z_min) / (N - 1) / s.mean())
    pts = np.zeros(N)
    pts[0] = z_min
    pts[1:] = z_min + np.cumsum(sc)
    return pts


def _counts(eigs):
    out = {}
    for thr in SWEEP:
        cens = bool(eigs[-1] < thr)
        out[f"{thr:.0e}"] = {"count": len(eigs) if cens else int((eigs < thr).sum()),
                             "censored": cens}
    return out


def solve_one(task):
    _worker_init()
    import numpy as np
    import scipy.sparse as sp
    from scipy.sparse.linalg import eigsh
    from scipy.spatial.distance import pdist

    sys.path.insert(0, str(JTOPO))
    from atft.topology.sparse_sheaf_laplacian import SparseSheafLaplacian
    from atft.topology.transport_maps import TransportMapBuilder

    kind, seed = task
    name = kind if seed is None else f"{kind}_{seed}"
    ckpt = OUT / f"{name}.json"
    if ckpt.exists():
        return name

    t0 = time.time()
    zeta = _zeta_points()
    z_min, z_max = float(zeta.min()), float(zeta.max())
    pts = _points_for(task, z_min, z_max)

    def n_edges(p, eps):
        return int(np.sum(pdist(p.reshape(-1, 1)) <= eps))

    if kind == "zeta":
        eps = 3.0
    else:
        lo, hi = 0.01, 20.0
        for _ in range(40):
            mid = 0.5 * (lo + hi)
            if n_edges(pts, mid) < TARGET_EDGES:
                lo = mid
            else:
                hi = mid
        eps = hi
    edges = n_edges(pts, eps)

    builder = TransportMapBuilder(K=K, sigma=SIGMA)
    lap = SparseSheafLaplacian(builder, pts, transport_mode="superposition")
    L0 = lap.build_matrix(eps)                    # build ONCE (fix: was built twice)
    L = ((L0 + L0.getH()) * 0.5).tocsr()
    del lap, builder, L0
    t_build = time.time() - t0

    # --- primary: spectral flip ---
    t1 = time.time()
    lam_max = float(eigsh(L, k=1, which="LA", tol=1e-3, return_eigenvectors=False)[0]) * 1.05
    flip = sp.identity(L.shape[0], dtype=L.dtype, format="csr") * lam_max - L
    mu, vecs = eigsh(flip, k=KEIG, which="LA", tol=TOL, ncv=NCV)
    eigs = np.maximum((lam_max - mu).real, 0.0)
    order = np.argsort(eigs)
    eigs = eigs[order]
    vecs = vecs[:, order]
    resid = np.array([float(np.linalg.norm(L @ vecs[:, i] - eigs[i] * vecs[:, i]))
                      for i in range(KEIG)])
    t_solve = time.time() - t1

    rec = {
        "name": name, "kind": kind, "seed": seed,
        "solver": "spectral-flip eigsh which=LA tol=1e-6 (Amendment 2)",
        "eps": float(eps), "edges": edges,
        "eigs": eigs.tolist(),
        "residuals": [float(r) for r in resid],   # per-pair, persisted (RT fix)
        "residual_max": float(resid.max()),
        "certified": bool(resid.max() < CERT_RESIDUAL),
        "counts": _counts(eigs),
        "near_1e-3": _counts(eigs)["1e-03"]["count"],
        "near_1e-3_censored": _counts(eigs)["1e-03"]["censored"],
        "exact_1e-8": int((eigs < 1e-8).sum()),
        "S20": float(eigs[:20].sum()),
        "t_build_s": round(t_build, 1), "t_solve_s": round(t_solve, 1),
    }

    # --- cross-check family (shift-invert) on the subset ---
    if name in CROSSCHECK:
        t2 = time.time()
        try:
            vals2, vecs2 = eigsh(L.tocsc(), k=KEIG, sigma=-1e-6, which="LM")
            e2 = np.sort(np.maximum(vals2, 0.0))
            r2 = float(max(np.linalg.norm(L @ vecs2[:, i] - vals2[i] * vecs2[:, i])
                           for i in range(KEIG)))
            # one-sided match: each flip eigenvalue within tol of some shift-invert one
            match = float(np.max([np.min(np.abs(e2 - x)) for x in eigs]))
            rec["crosscheck_shiftinvert"] = {
                "near_1e-3": int((e2 < 1e-3).sum()),
                "exact_1e-8": int((e2 < 1e-8).sum()),
                "residual_max": r2,
                "one_sided_match_max": match,
                "collapsed": bool((e2 < 1e-8).sum() >= KEIG - 1),
                "t_s": round(time.time() - t2, 1),
            }
        except Exception as exc:  # cross-check is best-effort, never blocks
            rec["crosscheck_shiftinvert"] = {"error": str(exc)}

    ckpt.write_text(json.dumps(rec, indent=1))
    return name


def main():
    gue = [("gue", s) for s in range(2000, 2000 + N_GUE)]
    poi = [("poisson", s) for s in ([42] + list(range(4000, 4000 + N_POISSON - 1)))]
    tasks = [("zeta", None)] + gue + poi + [("even", None)]
    todo = [t for t in tasks
            if not (OUT / f"{t[0] if t[1] is None else f'{t[0]}_{t[1]}'}.json").exists()]
    print(f"{len(tasks)} tasks ({N_GUE} GUE + {N_POISSON} Poisson), "
          f"{len(todo)} to run, {WORKERS} workers, spectral-flip k={KEIG}", flush=True)

    import numpy, scipy
    commit = subprocess.run(["git", "-C", str(JTOPO), "rev-parse", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", str(JTOPO), "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    (OUT / "_environment.json").write_text(json.dumps({
        "jtopo_commit": commit, "jtopo_dirty": dirty.splitlines(),
        "numpy": numpy.__version__, "scipy": scipy.__version__,
        "python": sys.version.split()[0], "amendment": 2,
        "params": {"N": N, "K": K, "sigma": SIGMA, "keig": KEIG, "ncv": NCV,
                   "target_edges": TARGET_EDGES, "solver": "spectral-flip",
                   "tol": TOL, "sweep": SWEEP, "cert_residual": CERT_RESIDUAL,
                   "transport_mode": "superposition", "zeta_eps": 3.0,
                   "n_gue": N_GUE, "n_poisson": N_POISSON, "workers": WORKERS,
                   "crosscheck_subset": sorted(CROSSCHECK)},
    }, indent=1))

    from multiprocessing import Pool
    t0 = time.time()
    with Pool(WORKERS, initializer=_worker_init, maxtasksperchild=1) as pool:
        for i, name in enumerate(pool.imap_unordered(solve_one, todo), 1):
            el = time.time() - t0
            print(f"[{i}/{len(todo)}] {name}  ({el/60:.1f} min, "
                  f"~{el/i*(len(todo)-i)/60:.0f} min left)", flush=True)
    print(f"fleet v3 done in {(time.time()-t0)/60:.0f} min", flush=True)


if __name__ == "__main__":
    main()
