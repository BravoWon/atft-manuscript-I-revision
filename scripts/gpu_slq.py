#!/usr/bin/env python
"""GPU stochastic-trace eigencounter, SLQ variant (Stochastic Lanczos Quadrature).

N(<t) = tr(1[L<t]) ~= (n / n_probes) * sum_v sum_{theta_j^v < t} tau_j^v
where, for each independent probe z_v, an m-step Lanczos on L produces a
tridiagonal T_m whose eigenpairs give Gauss quadrature nodes theta_j (Ritz
values) and weights tau_j = (first component of the j-th eigenvector)^2.

Edge-adaptive: Lanczos converges to the extreme (smallest) eigenvalues first,
so the near-kernel is resolved with modest m -- unlike KPM's uniform grid.
Batched across probes (each Lanczos step = one SpMM) -> GPU-harmonious.
"""
from __future__ import annotations

import sys, time, warnings
warnings.filterwarnings("ignore")
import numpy as np
import scipy.sparse as sp
from scipy.linalg import eigh_tridiagonal


def slq_eigencount(L_cpu, thresholds, m=200, n_probes=40, seed=0, device=0,
                   reorth=True, verbose=True):
    import cupy as cp
    import cupyx.scipy.sparse as csp
    t0 = time.time()
    with cp.cuda.Device(device):
        n = L_cpu.shape[0]
        Lg = csp.csr_matrix(L_cpu.astype(np.float64))
        rs = cp.random.RandomState(seed)
        Z = (rs.randint(0, 2, size=(n, n_probes), dtype=cp.int32) * 2 - 1).astype(cp.float64)
        znorm2 = cp.sum(Z * Z, axis=0)                 # = n for Rademacher
        Q = Z / cp.sqrt(znorm2)                        # q_1, unit columns

        alphas = cp.empty((m, n_probes)); betas = cp.empty((m, n_probes))
        Qprev = cp.zeros_like(Q); beta = cp.zeros(n_probes)
        Qbasis = [] if reorth else None
        for j in range(m):
            w = Lg @ Q - beta * Qprev
            alpha = cp.sum(Q * w, axis=0)
            w = w - alpha * Q
            if reorth and Qbasis:                      # full reorth (batched, columnwise)
                for Qi in Qbasis:
                    w = w - cp.sum(Qi * w, axis=0) * Qi
            beta = cp.sqrt(cp.sum(w * w, axis=0)) + 1e-300
            alphas[j] = alpha; betas[j] = beta
            Qprev = Q; Q = w / beta
            if reorth:
                Qbasis.append(Qprev)
        cp.cuda.Stream.null.synchronize()
        t_lanczos = time.time() - t0
        A = cp.asnumpy(alphas); B = cp.asnumpy(betas); nn = int(n)
        del Lg, Z, Q, Qprev
        if reorth: Qbasis.clear()
        cp.get_default_memory_pool().free_all_blocks()

    # per-probe tridiagonal eig -> nodes theta, weights tau (CPU, tiny)
    thetas = []; taus = []
    for v in range(n_probes):
        th, V = eigh_tridiagonal(A[:, v], B[:-1, v])
        thetas.append(th); taus.append(V[0, :] ** 2)

    out = {}
    for t in thresholds:
        per = np.array([nn * taus[v][thetas[v] < t].sum() for v in range(n_probes)])
        out[t] = (float(per.mean()), float(per.std(ddof=1) / np.sqrt(n_probes)))
    total = time.time() - t0
    if verbose:
        print(f"SLQ: m={m} probes={n_probes} reorth={reorth} "
              f"lanczos={t_lanczos:.1f}s total={total:.1f}s", flush=True)
    return {"counts": out, "m": m, "n_probes": n_probes,
            "t_lanczos_s": t_lanczos, "t_total_s": total}


if __name__ == "__main__":
    L = sp.load_npz(sys.argv[1] if len(sys.argv) > 1 else "gue_2000_L.npz")
    TRUTH = {1e-8: 7, 1e-6: None, 1e-4: None, 1e-3: 76, 2e-3: None}
    m = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    npb = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    reorth = (sys.argv[4] != "noreorth") if len(sys.argv) > 4 else True
    res = slq_eigencount(L, list(TRUTH), m=m, n_probes=npb, reorth=reorth)
    print(f"\n{'threshold':>10} {'SLQ est':>16} {'certified':>10}")
    for t, (mm, se) in res["counts"].items():
        tr = TRUTH.get(t)
        flag = "" if tr is None else ("  <-- MATCH" if abs(mm - tr) < 2*se + 5 else "  <-- off")
        print(f"{t:>10.0e} {mm:>8.1f} +/- {se:>4.1f} {str(tr):>10}{flag}")
