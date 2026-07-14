# AMENDMENT 3 to PREREGISTRATION_POWERED_NULL — solver final decision

**Date:** 2026-07-13. Logged BEFORE the production fleet was launched.

**Decision: primary solver = spectral-flip** (flip = 1.05·λ_max·I − L, then
`eigsh(flip, k=100, which='LA', tol=1e-6, ncv=384)`), for all sources. This is
the manuscript's own corrected-audit method and the only solver that produced a
resolved, residual-certified spectrum on the GUE test matrix (near-kernel = 73,
6 exact, smooth rise).

**Shift-invert is disqualified** for this matrix class after three distinct
failure modes on the identical `gue_2000` operator (dim 100000, nnz 59.7M):
1. σ = −1e-6 and σ = +1e-9 — *silent degeneracy*: returned 80 spurious
   exact-zero modes (residual 3e-15 but S20 = 0, all sweep points censored).
2. σ = −1e-2 — *loud failure*: ARPACK error 3 (Krylov starvation on the dense
   near-kernel cluster).
3. σ = −1e-1 — *non-termination*: 214,519 CPU-seconds (~5 h wall on all cores)
   with zero output; killed.
The dense ~73-mode near-kernel is hostile to shift-invert regardless of shift
placement; the well-conditioned spectral transformation (flip) handles it.

**Speed adjustments (do not change the method or any frozen statistical
parameter):** `ncv` 256 → 384 (larger Krylov subspace → faster ARPACK
convergence on the cluster; strictly non-degrading for correctness — a bigger
subspace only improves the Ritz approximation, and the residual < 1e-5 gate
catches any shortfall). Laplacian built once per solve (was built twice — pure
efficiency, identical matrix). Workers 4 → 6 (memory: ~2.5 GB/worker × 6 ≈
15 GB on the 32 GB host).

**Cross-check family:** shift-invert retained ONLY as the diagnostic cross-check
on the 3-source subset (zeta, gue_2000, poisson_42); it is *expected to
collapse* on high-near-kernel sources, and that collapse is the reported
diagnostic — a second live instance of the manuscript's near-kernel pathology.

**GPU note (for the record):** the RTX 5070 (Blackwell, sm_120) + GTX 1660 Ti
were considered. This workload is sparse-eigensolver-bound; cupy sparse
eigensolvers offer no robust shift-invert and sm_120 wheel support is
unproven. The validated CPU spectral-flip path is guaranteed and resumable, so
the fleet runs on CPU. GPU acceleration remains an available optimization if a
future run needs it, not a blocker now.

**All frozen statistical parameters UNCHANGED:** N=1000, K=100, σ=1/2,
superposition transport, edges 2492, GUE seeds 2000–2099 (100), Poisson
{42,4000–4018} (20), even control, sweep {1e-8…2e-3}, certification residual
< 1e-5, per-pair residual vectors persisted.
