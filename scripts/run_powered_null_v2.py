#!/usr/bin/env python
"""Powered edge-matched null, fleet v2 (per PREREGISTRATION AMENDMENT 1).

Primary solver: shift-invert eigsh(L, k=80, sigma=-1e-6, which='LM').
122 solves: zeta + 100 GUE (2000-2099) + 20 Poisson ({42, 4000-4018}) + even.
4 memory-lean workers; checkpointed one JSON per solve (resumable).
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
OUT = HERE / "output" / "powered_null"
OUT.mkdir(parents=True, exist_ok=True)

N, SIGMA, K, KEIG = 1000, 0.5, 100, 80
TARGET_EDGES = 2492
SHIFT = -1e-6
SWEEP = [1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 3e-4, 1e-3, 2e-3]
CERT_RESIDUAL = 1e-5
WORKERS = 4


def _worker_init():
    os.environ["OMP_NUM_THREADS"] = "4"
    os.environ["OPENBLAS_NUM_THREADS"] = "4"
    os.environ["MKL_NUM_THREADS"] = "4"


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


def solve_one(task):
    _worker_init()
    import numpy as np
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
    L = lap.build_matrix(eps)
    L = ((L + L.getH()) * 0.5).tocsc()
    del lap, builder
    t_build = time.time() - t0

    t1 = time.time()
    vals, vecs = eigsh(L, k=KEIG, sigma=SHIFT, which="LM")
    order = np.argsort(vals)
    eigs = np.maximum(vals[order], 0.0)
    vecs = vecs[:, order]
    residuals = np.array([float(np.linalg.norm(L @ vecs[:, i] - eigs[i] * vecs[:, i]))
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
        "solver": "shift-invert eigsh sigma=-1e-6 which=LM (Amendment 1)",
        "eps": float(eps), "edges": edges,
        "eigs80": eigs.tolist(),
        "residual_max": float(residuals.max()),
        "certified": bool(residuals.max() < CERT_RESIDUAL),
        "counts": counts,
        "near_1e-3": counts["1e-03"]["count"],
        "near_1e-3_censored": counts["1e-03"]["censored"],
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
        "amendment": 1,
        "params": {"N": N, "K": K, "sigma": SIGMA, "keig": KEIG,
                   "target_edges": TARGET_EDGES,
                   "solver": "shift-invert", "shift": SHIFT,
                   "sweep": SWEEP, "cert_residual": CERT_RESIDUAL,
                   "transport_mode": "superposition", "zeta_eps": 3.0,
                   "gue_seeds": "2000-2099", "poisson_seeds": "[42, 4000-4018]",
                   "workers": WORKERS},
    }, indent=1))

    from multiprocessing import Pool
    t0 = time.time()
    with Pool(WORKERS, initializer=_worker_init, maxtasksperchild=1) as pool:
        for i, name in enumerate(pool.imap_unordered(solve_one, todo), 1):
            el = time.time() - t0
            print(f"[{i}/{len(todo)}] {name}  ({el/60:.1f} min elapsed, "
                  f"~{el/i*(len(todo)-i)/60:.0f} min left)", flush=True)
    print(f"fleet done in {(time.time()-t0)/60:.0f} min", flush=True)


if __name__ == "__main__":
    main()
