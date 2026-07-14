#!/usr/bin/env python
"""Powered edge-matched null for ATFT Manuscript I Section 5.3 (rev v0.2).

Frozen protocol: PREREGISTRATION_POWERED_NULL.md (same directory).
Instrument: RogueGringo/JTopo @ aa6a300, used read-only via sys.path.
122 solves: zeta + 100 GUE (seeds 2000-2099) + 20 Poisson ({42, 4000-4018}) + even.
Checkpointed one JSON per solve in output/powered_null/ (resumable).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
JTOPO = Path("C:/Users/JT-DEV1/Desktop/development/JTopo")
OUT = HERE / "output" / "powered_null"
OUT.mkdir(parents=True, exist_ok=True)

N, SIGMA, K, KEIG = 1000, 0.5, 100, 40
TARGET_EDGES = 2492
TOL, NCV = 1e-6, 192
SWEEP = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 3e-4, 1e-3, 2e-3]
CERT_RESIDUAL = 1e-5
WORKERS = 8


def _worker_init():
    os.environ["OMP_NUM_THREADS"] = "2"
    os.environ["OPENBLAS_NUM_THREADS"] = "2"
    os.environ["MKL_NUM_THREADS"] = "2"


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
    # GUE: tridiagonal beta=2 ensemble, unfolded to [z_min, z_max] (as original)
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


def solve_one(task):
    """One (kind, seed) -> result dict. Runs in a worker process."""
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
        return name  # resumable

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
        eps = 0.5 * (lo + hi)
    edges = n_edges(pts, eps)

    builder = TransportMapBuilder(K=K, sigma=SIGMA)
    lap = SparseSheafLaplacian(builder, pts, transport_mode="superposition")
    L = lap.build_matrix(eps)
    L = (L + L.getH()) * 0.5
    t_build = time.time() - t0

    t1 = time.time()
    lam_max = float(eigsh(L, k=1, which="LA", tol=1e-3,
                          return_eigenvectors=False)[0]) * 1.05
    flip = sp.identity(L.shape[0], dtype=L.dtype, format="csr") * lam_max - L
    mu, X = eigsh(flip, k=KEIG, which="LA", tol=TOL, ncv=NCV)
    eigs = np.maximum((lam_max - mu).real, 0.0)
    order = np.argsort(eigs)
    eigs = eigs[order]
    X = X[:, order]
    residuals = np.array([float(np.linalg.norm(L @ X[:, i] - eigs[i] * X[:, i]))
                          for i in range(KEIG)])
    t_solve = time.time() - t1

    counts = {}
    for thr in SWEEP:
        if eigs[-1] < thr:
            counts[f"{thr:.0e}"] = {"count": KEIG, "censored": True}
        else:
            counts[f"{thr:.0e}"] = {"count": int((eigs < thr).sum()), "censored": False}

    rec = {
        "name": name, "kind": kind, "seed": seed,
        "eps": float(eps), "edges": edges,
        "eigs40": eigs.tolist(),
        "residual_max": float(residuals.max()),
        "certified": bool(residuals.max() < CERT_RESIDUAL),
        "counts": counts,
        "near_1e-3": counts["1e-03"]["count"],
        "exact_1e-8": counts["1e-08"]["count"],
        "S20": float(eigs[:20].sum()),
        "t_build_s": round(t_build, 1), "t_solve_s": round(t_solve, 1),
    }
    ckpt.write_text(json.dumps(rec, indent=1))
    return name


def main():
    tasks = ([("zeta", None)]
             + [("gue", s) for s in range(2000, 2100)]
             + [("poisson", s) for s in [42] + list(range(4000, 4019))]
             + [("even", None)])
    todo = [t for t in tasks
            if not (OUT / f"{t[0] if t[1] is None else f'{t[0]}_{t[1]}'}.json").exists()]
    print(f"{len(tasks)} tasks total, {len(todo)} to run, {WORKERS} workers", flush=True)

    import numpy, scipy
    commit = subprocess.run(["git", "-C", str(JTOPO), "rev-parse", "HEAD"],
                            capture_output=True, text=True).stdout.strip()
    dirty = subprocess.run(["git", "-C", str(JTOPO), "status", "--porcelain"],
                           capture_output=True, text=True).stdout.strip()
    (OUT / "_environment.json").write_text(json.dumps({
        "jtopo_commit": commit, "jtopo_dirty": dirty.splitlines(),
        "numpy": numpy.__version__, "scipy": scipy.__version__,
        "python": sys.version.split()[0],
        "params": {"N": N, "K": K, "sigma": SIGMA, "keig": KEIG,
                   "target_edges": TARGET_EDGES, "tol": TOL, "ncv": NCV,
                   "sweep": SWEEP, "cert_residual": CERT_RESIDUAL,
                   "transport_mode": "superposition",
                   "zeta_eps": 3.0, "gue_seeds": "2000-2099",
                   "poisson_seeds": "[42, 4000-4018]"},
    }, indent=1))

    from multiprocessing import Pool
    t0 = time.time()
    with Pool(WORKERS, initializer=_worker_init, maxtasksperchild=1) as pool:
        for i, name in enumerate(pool.imap_unordered(solve_one, todo), 1):
            el = time.time() - t0
            print(f"[{i}/{len(todo)}] {name}  ({el/60:.0f} min elapsed, "
                  f"~{el/i*(len(todo)-i)/60:.0f} min left)", flush=True)
    print(f"fleet done in {(time.time()-t0)/60:.0f} min", flush=True)


if __name__ == "__main__":
    main()
