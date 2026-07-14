# AMENDMENT 4 — ensemble size + worker config (2026-07-13)

Logged BEFORE the reduced fleet was relaunched. Justified, not silent.

## Trigger
The full-100 certified fleet (spectral-flip, AMENDMENT 3) ran at ~150 min per
solve — `zeta` 7452 s, `gue_2000` 9118 s — because 6 workers × 4 BLAS threads
oversubscribed the i9-9900K's 8 physical cores and ~40 GB/s memory bus on a
bandwidth-bound SpMV workload. Projected full-100 wall-clock: ~1-2 days. The
shift-invert / GPU / inertia alternatives were all exhausted (see the bake-off
records): none certifies faster. The certified method is inherently ~30-60
min/solve on this hardware.

## Certified results already obtained (kept — checkpointed, res < 1e-5)
- **zeta: near-kernel(<1e-3) = 58** (res 2.2e-6); shift-invert cross-check 62,
  did NOT collapse (families agree → high confidence).
- **gue_2000: near-kernel(<1e-3) = 76** (res 3.2e-6); shift-invert cross-check
  collapsed to 100 (the diagnosed degeneracy — auto-flagged, spectral-flip
  trusted).
- **Direction certified: zeta (58) < GUE (76)** — opposite the retracted
  "zeta is special / larger kernel" claim. n=1 GUE so far.

## Decision (frozen)
- **Ensemble reduced: 30 GUE (seeds 2000-2029) + 10 Poisson (42,4000-4008) +
  zeta + even = ~42 solves.** This is 10× the referee-killed n=3, sufficient
  for a real mean±sd band, zeta's quantile/exceedance-p, and the GUE-vs-Poisson
  positive control (Mann-Whitney). The preregistered n=100 is deferred to a
  compute cluster; the reduction is a *hardware-runtime* concession, not a
  design change — all other frozen parameters (N=1000, K=100, σ=1/2,
  superposition, edges 2492, certification res < 1e-5, sweep, per-pair
  residuals, shift-invert cross-check) UNCHANGED.
- **Worker config:** WORKERS=4, 2 BLAS threads each (= 8 threads = physical
  cores, no oversubscription). ncv=384 retained (proven to certify).
- **Homogeneity note:** zeta and gue_2000 were solved at the same k=100,
  tol=1e-6, ncv=384 and certified to the same res < 1e-5 bar as the rest; the
  count is a property of the certified eigenvalues, not of ncv, so the two
  existing solves are pooled with the reduced-fleet solves.

## Reporting
The paper's §5.3 table reports n=30 GUE (not 100), states the deferral
explicitly, and gives the exceedance p at n=30. If zeta's quantile is
unambiguous at n=30 (e.g. below the GUE minimum), the conclusion is robust to
the reduction; if borderline, the cluster run is required before publication.
