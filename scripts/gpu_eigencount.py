#!/usr/bin/env python
"""GPU stochastic-trace eigencounter (Kernel Polynomial Method).

Counts eigenvalues of a symmetric PSD sparse matrix below threshold(s) t as
    N(<t) = tr( 1[L < t] )
estimated by Hutchinson stochastic trace over independent Rademacher probes,
with the indicator expanded in Chebyshev polynomials (Jackson-damped).

Why this is GPU-harmonious: the only kernel is repeated sparse matrix x
tall-skinny (SpMM) on a batch of probes — dense data-parallel work, no serial
reorthogonalization. Each probe is independent, giving a mean +/- standard
error for free (the statistical price of dropping exact extraction).

Closed form used (x = cos theta, rescaled spectrum in [-1,1]):
    N(<t) ~= (1/pi)[ g_0 mu_0 (pi - theta_t) - 2 sum_{k>=1} (g_k mu_k / k) sin(k theta_t) ]
with theta_t = arccos(t~), t~ = (t - b)/a, mu_k = tr(T_k(L~)) (stochastic),
g_k = Jackson kernel. Derivation: integrate the KPM density of states from the
bottom edge (theta=pi) up to theta_t.
"""
from __future__ import annotations

import numpy as np


def jackson(M):
    """Jackson kernel damping factors g_0..g_M (Gibbs suppression)."""
    k = np.arange(M + 1)
    Mp = M + 2
    return ((Mp - k) * np.cos(np.pi * k / Mp)
            + np.sin(np.pi * k / Mp) / np.tan(np.pi / Mp)) / Mp


def kpm_eigencount(L_cpu, thresholds, M=3000, n_probes=40, seed=0, device=0,
                   lam_max=None, verbose=True):
    """Return dict: per-threshold (mean, se) count estimate + timing.
    L_cpu: scipy CSR symmetric PSD. thresholds: iterable of t (in L's own units).
    """
    import time
    import cupy as cp
    import cupyx.scipy.sparse as csp
    import cupyx.scipy.sparse.linalg as csla

    t0 = time.time()
    with cp.cuda.Device(device):
        n = L_cpu.shape[0]
        Lg = csp.csr_matrix(L_cpu.astype(np.float64))
        if lam_max is None:
            lam_max = float(csla.eigsh(Lg, k=1, which='LA', tol=1e-2,
                                       return_eigenvectors=False)[0])
        lam_min = -1e-9                       # keep 0 strictly inside (-1,1)
        a = (lam_max - lam_min) / 2.0 * 1.01  # scale (pad to keep spectrum in [-1,1])
        b = (lam_max + lam_min) / 2.0

        def apply_Lt(X):                      # rescaled operator L~ = (L - b)/a
            return (Lg @ X - b * X) / a

        rs = cp.random.RandomState(seed)
        Z = (rs.randint(0, 2, size=(n, n_probes), dtype=cp.int32) * 2 - 1).astype(cp.float64)

        # Chebyshev moment sequence, per probe (columns): mu_k[v] = z_v . T_k(L~) z_v
        Tkm1 = Z                              # T_0 Z = Z
        Tk = apply_Lt(Z)                      # T_1 Z
        mom = cp.empty((M + 1, n_probes), dtype=cp.float64)
        mom[0] = cp.sum(Z * Tkm1, axis=0)     # = n exactly (Rademacher)
        mom[1] = cp.sum(Z * Tk, axis=0)
        for k in range(2, M + 1):
            Tkp1 = 2.0 * apply_Lt(Tk) - Tkm1
            mom[k] = cp.sum(Z * Tkp1, axis=0)
            Tkm1, Tk = Tk, Tkp1
        cp.cuda.Stream.null.synchronize()
        t_moments = time.time() - t0

        g = cp.asarray(jackson(M))            # (M+1,)
        kidx = cp.arange(1, M + 1).reshape(-1, 1)  # (M,1)
        out = {}
        for t in thresholds:
            tt = (t - b) / a
            tt = min(max(tt, -1 + 1e-15), 1 - 1e-15)
            theta = float(np.arccos(tt))
            # per-probe N(<t): (1/pi)[ g0 mu0 (pi-theta) - 2 sum_{k>=1} g_k mu_k sin(k theta)/k ]
            term0 = g[0] * mom[0] * (np.pi - theta)
            sk = cp.sin(kidx * theta)                       # (M,1)
            series = cp.sum((g[1:].reshape(-1, 1) * mom[1:] * sk) / kidx, axis=0)  # (n_probes,)
            Nt = (term0 - 2.0 * series) / np.pi             # (n_probes,)
            Nt = cp.asnumpy(Nt)
            out[t] = (float(Nt.mean()), float(Nt.std(ddof=1) / np.sqrt(n_probes)))
        total = time.time() - t0
        del Lg, Z, Tk, Tkm1, mom
        cp.get_default_memory_pool().free_all_blocks()

    if verbose:
        print(f"KPM: M={M} probes={n_probes} lam_max={lam_max:.4f} "
              f"moments={t_moments:.1f}s total={total:.1f}s", flush=True)
    return {"counts": out, "M": M, "n_probes": n_probes, "lam_max": lam_max,
            "t_moments_s": t_moments, "t_total_s": total}


if __name__ == "__main__":
    import sys, warnings
    warnings.filterwarnings("ignore")
    import scipy.sparse as sp
    L = sp.load_npz(sys.argv[1] if len(sys.argv) > 1 else "gue_2000_L.npz")
    TRUTH = {1e-8: 7, 1e-6: None, 1e-4: None, 1e-3: 76, 2e-3: None}  # certified: 76 @ 1e-3
    M = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    npb = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    res = kpm_eigencount(L, list(TRUTH), M=M, n_probes=npb)
    print(f"\n{'threshold':>10} {'KPM est':>14} {'certified':>10}")
    for t, (m, se) in res["counts"].items():
        tr = TRUTH.get(t)
        flag = "" if tr is None else ("  <-- MATCH" if abs(m - tr) < 2*se + 3 else "  <-- off")
        print(f"{t:>10.0e} {m:>7.1f} +/- {se:>4.1f} {str(tr):>10}{flag}")
