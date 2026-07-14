# GPU Stochastic-Trace Eigencounter — build + verdict (2026-07-13)

**Task:** reformulate near-kernel eigenvalue counting as GPU-harmonious
stochastic trace estimation, to replace the slow exact CPU solve.
**Deliverables:** `gpu_eigencount.py` (KPM/Chebyshev), `gpu_slq.py` (Stochastic
Lanczos Quadrature). Both work, both run in seconds on the RTX 5070, both are
correct implementations of the standard methods.

## Verdict: intrinsic obstruction for THIS observable

Counting `N(<t) = tr(1[L<t])` for **tiny t at the extreme edge** of a
100k-dim spectrum whose bulk spans [0, 11.34], with a **clustered near-kernel
sitting just below a steeply-rising bulk**, does NOT admit a reliable
stochastic-trace projection.

Validation against the CPU-certified truth (gue_2000 near-kernel(<1e-3) = 76,
zeta = 58; both residual < 5e-6):

| method | config | gue_2000 (truth 76) | zeta (truth 58) |
|---|---|---|---|
| KPM (Chebyshev+Jackson) | M=3000, 40 probes, 200s | 793 | — |
| SLQ (Lanczos quad) | m=200 reorth, 46s | 816 | 29 |
| SLQ | m=800 noreorth, 55s | 893 | 34 |
| SLQ | m=1500 noreorth, 105s | 883 | — |

**Two independent methods agree with each other (~800-900 for gue) and both
disagree with the exact count (76).** SLQ **plateaus** with increasing Lanczos
depth (400→800→1500: 861→893→883) — the error is **fundamental, not a
resolution gap.**

**Salvage attempt (consistent-bias-cancels-in-comparison) FAILED:** the bias is
matrix-dependent and opposite in sign — gue over by ~11x, zeta under by ~0.5x.
Stochastic zeta/gue = 0.035 vs certified 0.76 (off 20x). Not a valid relative
discriminator either.

## Root cause

A stochastic step-counter approximates the sharp indicator 1[lambda<t] by a
smooth polynomial / quadrature rule of finite resolution. At the **extreme
edge** with a **huge adjacent bulk**, (a) KPM's uniform resolution lets bulk
Gibbs oscillations leak into the tiny edge count; (b) SLQ's Gauss nodes cannot
place a sharp cut at 1e-3 without lumping the dense eigenvalues just above it.
The effective smoothing width (~1e-2) exceeds the threshold (1e-3) by 10x. This
is the SAME clustered-near-edge geometry that made the exact ARPACK solve
convergence-bound and slow — the difficulty is intrinsic to the spectral
geometry, and it defeats both the exact-but-slow and the fast-but-approximate
approaches, in dual ways.

## Where the tool IS valid (not wasted)

Stochastic trace estimation is the right, GPU-harmonious method for **global /
bulk spectral observables** — spectral density over wide bins, traces of smooth
matrix functions, and crucially the **long-range zeta observables of the §7.1
experiment: number variance Sigma^2(L) and spectral form factor K(tau)**, which
are global statistics, not extreme-edge sharp counts. The built counters are
correct infrastructure for that experiment; they simply cannot substitute for
the exact solve on the near-kernel count.

## Standing decision

- **Near-kernel counts (the §5.3 powered null): exact CPU spectral-flip only.**
  Certified, gold standard. The reduced 30-GUE fleet remains the path.
- **Long-range §7.1 observables: GPU stochastic trace (this tool).** The right
  place for the 5070's 120x.

## Driftwave note

The projection of an abstract computation onto a hardware substrate is lossless
only when the *observable* admits it. "Count eigenvalues below t" is universal
math; but *this* instance (sharp cut, clustered edge, huge bulk) has an
intrinsic obstruction to GPU-harmonious stochastic realization. Same math,
non-projectable observable. The exact serial method is not slow by accident —
its serial reorthogonalization is exactly what buys the edge resolution that
the parallel stochastic method structurally cannot.
