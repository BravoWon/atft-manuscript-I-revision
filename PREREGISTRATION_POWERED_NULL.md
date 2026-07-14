# Preregistration — Powered Edge-Matched Null (Manuscript I, Section 5.3 upgrade)

**Date:** 2026-07-13 (committed BEFORE the fleet below was launched)
**Purpose:** replace the n=3 GUE / single-threshold table in ATFT Manuscript I §5.3
with an honestly powered null, per the manuscript's own Section 8 acceptance
criteria and the referee findings RT-1 / MATH-3 / RT-5 / RT-2.

## Instrument (frozen — identical to the corrected audit pipeline)

- Repository: `RogueGringo/JTopo` at commit `aa6a300` (the manuscript's pinned
  provenance; working tree verified clean at launch, hash recorded in output).
- Pipeline: `SparseSheafLaplacian` + `TransportMapBuilder(K=100, sigma=0.5)`,
  `transport_mode="superposition"`, N=1000 unfolded Odlyzko zeta ordinates,
  zeta at eps=3.0 (2492 edges); every control binary-searched to exactly 2492
  edges (40 bisection steps in [0.01, 20]).
- Solver (primary family — spectral flip, as in the corrected audit):
  `eigsh(flip, k=40, which='LA', tol=1e-6, ncv=192)` with eigenvectors,
  flip = 1.05*lambda_max * I − L. KEIG raised 30→40 (censoring headroom),
  tol tightened 1e-4→1e-6 because the smoke test measured eigenpair residuals
  ~1.2e-3 at tol=1e-4 — the same order as the 1e-3 counting threshold, which
  the manuscript's own Section 8 forbids.
- Residual certificates: ||L x − lambda x||_2 (||x||=1) recorded for all 40
  pairs of every solve. **Certification rule: a solve is certified iff its max
  residual < 1e-5** (two orders below the primary threshold). Non-certified
  solves are reported as such, never silently included.
- Second solver family (Section 8 criterion 2): shift-invert
  `eigsh(L, k=40, sigma=-1e-6, which='LM')` on the subset {zeta, gue_2000,
  gue_2001, gue_2002, poisson_42}; agreement tolerance |Δlambda| < 1e-6 per
  pair. Best-effort: an out-of-memory factorization is reported, not hidden.

## Ensembles (frozen)

- **zeta**: 1 structured sample (treated as n=1 throughout — no pseudo-replication).
- **GUE**: 100 independent draws, seeds 2000–2099. Seeds 2000–2002 are the
  original three (continuity subset); 2003–2099 are new and untouched.
- **Poisson/uniform**: 20 draws, seeds {42, 4000–4018}. Seed 42 is the original.
- **even**: 1 evenly spaced control (restores the control the manuscript table
  dropped; charter 4B.5).

## Endpoints and decision rules (frozen)

1. **Primary endpoint:** near-kernel count at threshold 1e-3.
   **Separation rule:** zeta separates from GUE iff zeta's count strictly
   exceeds the maximum of all 100 certified GUE counts. Otherwise report
   zeta's empirical exceedance p = (r+1)/(n+1), r = #{GUE draws ≥ zeta}.
2. **Positive-control quantification (RT-2):** GUE-vs-Poisson near-kernel
   ensembles: means ± sd, Mann–Whitney U (two-sided), rank-biserial effect.
   Pre-declared detection: zero ensemble overlap OR p < 1e-4.
3. **Tolerance sweep (Section 8 criterion):** counts at
   {1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 3e-4, 1e-3, 2e-3}, each with an explicit
   censoring flag (count reported as ">= 40, censored" if eigs[39] < threshold).
   The primary threshold stays 1e-3 (continuity with the manuscript).
4. **Secondary:** S_20 (sum of 20 smallest eigenvalues) distributions,
   zeta quantile within GUE.
5. **Prediction (operator, committed now):** zeta's count will land INSIDE the
   100-draw GUE distribution (no separation), consistent with §5.3's thesis —
   the local observable is a level-repulsion detector, not an arithmetic one.
   The Poisson contrast WILL separate (positive control). If zeta separates
   instead, that is reported as a discovery claim requiring the §7.1 long-range
   program to arbitrate, not celebrated as one.

## Reporting (frozen)

All hyperparameters (N, K, sigma, transport mode, eps per source, edges, seeds,
solver, tol, ncv, KEIG, thresholds, numpy/scipy versions, JTopo commit), all
40 eigenvalues per solve, all residual maxima, and per-solve wall time go into
`output/powered_null/*.json` + a summary. Retraction rule 8.7 (as amended)
applies: no value from this run is quotable without its residual certificate.

---

## AMENDMENT 1 — 2026-07-13, logged BEFORE any new ensemble data existed

**Unblinding state at amendment time:** only the zeta solve had completed
(both solver families). Zeta was already public in manuscript v0.1. Zero new
GUE/Poisson draws had been computed. Decision rules, ensembles, seeds,
thresholds, endpoints, and the certification requirement are UNCHANGED.

**What changed and why:**

1. **Primary solver: spectral-flip → shift-invert** `eigsh(L, sigma=-1e-6,
   which='LM')`. Measured on zeta: 94 s vs 4309 s per solve (the original
   8-worker spectral-flip fleet memory-thrashed: 73 min for solve 1, ~147 h
   projected) and max residual 1.0e-13 vs 9.5e-6. The certification rule
   (residual < 1e-5) is solver-agnostic and unchanged; shift-invert passes it
   by eight orders.
2. **KEIG: 40 → 80.** The certified zeta solve censored at the 40-eigenvalue
   window (count at 1e-3 = 40 = window). k=80 uncensors the primary
   threshold (zeta: 62 < 80). The 2e-3 sweep point may still censor; flags
   stay mandatory.
3. **Solver-family roles swapped, both retained.** Spectral-flip (tol=1e-6)
   becomes the cross-check family: zeta cross-check already complete;
   gue_2000 and poisson_42 to follow post-fleet. Agreement metric amended to
   one-sided match distance (each spectral-flip eigenvalue within tol of
   SOME shift-invert eigenvalue) because position-wise pairing is invalid
   when one family resolves only a subset of a dense cluster — the zeta
   comparison (position-wise max |dLambda| = 3.19e-4 despite a 9.5e-6
   residual bound) demonstrates exactly the cluster-subset behavior the
   manuscript's Section 5 documents.
4. **Workers: 8 → 4** with memory-lean build (no flip-matrix copy), sized to
   the 32 GB host.

**Finding logged at amendment time (quotable, certified):** zeta's
residual-certified near-kernel at 1e-3 is **62** (shift-invert, k=80,
residual 1.0e-13), not the 24 of manuscript v0.1 Table 5.3 — the v0.1 count
was limited by solver tolerance (residuals ~1e-3 at tol=1e-4, the same order
as the counting threshold). The v0.1 comparison remains internally consistent
(all sources shared the tolerance limit); the powered table supersedes it at
certified tolerance.

---

## AMENDMENT 2 — 2026-07-13, logged BEFORE any ensemble result was accepted

**Trigger:** the fleet's first GUE solve (gue_2000) returned an all-zero
80-mode spectrum under the Amendment-1 primary solver (shift-invert
sigma=-1e-6). A three-way cross-solver diagnostic on that exact matrix
(dim 100000, nnz 59.7M, edges 2492) resolved it:

| solver | near<1e-3 | exact<1e-8 | bottom spectrum |
|---|---|---|---|
| spectral-flip, tol 1e-6, k=80 (validated) | **73** | 6 | 7.6e-13 ... 1.25e-6 ... 1.15e-4 (resolved) |
| shift-invert sigma=-1e-6 | 80 | 80 | all 0.0 (degenerate) |
| shift-invert sigma=+1e-9 | 80 | 80 | all ~1.8e-16 (degenerate) |

**Diagnosis:** shift-invert with sigma inside a dense near-kernel cluster is
catastrophically ill-conditioned; ARPACK returns spurious Ritz vectors pinned
at the shift (reported as ~0), collapsing all sweep resolution (S20=0, every
threshold censored). The per-pair residual guard did NOT catch it because the
spurious vectors genuinely lie in the near-null space (||Lx||~0); what they
destroy is *resolution within* the cluster, not the residual. This is a second,
independent instance of the manuscript's core near-kernel pathology — now on
the record as a methods result, not just an ops note.

**Decision (frozen):** **primary solver reverts to spectral-flip** (the
manuscript's own corrected-audit method: flip = 1.05*lam_max*I - L, then
eigsh which='LA', tol=1e-6), for ALL sources, at **k=100** (headroom: GUE
near-kernel reaches 73; k=80 leaves only 7 modes of margin). Shift-invert is
demoted to the cross-check family and is expected to disagree by *collapsing*
on high-near-kernel sources — that disagreement is the reported diagnostic,
not a defect to average away. All other frozen parameters (N, K, sigma,
transport, edges, seeds, ensembles, certification rule, sweep) UNCHANGED.
Per-pair residual vectors are now persisted (closes the RT-verifier recording
gap).

**Emerging finding (single-comparison, certified via the validated solver):**
gue_2000 near-kernel (<1e-3) = **73**, *larger* than zeta's ~62 — the direction
opposite to the retracted "zeta is special" claim. The full ensemble
establishes the band; the sign of the effect is already the null-strengthening
one. (Zeta is re-counted with spectral-flip at k=100 for the final
apples-to-apples number; shift-invert's 62 may be inflated by the same
mechanism that inflated GUE by +7.)

**Runtime note:** spectral-flip at certified tolerance is ~30 min/GUE solve
(vs shift-invert 94 s) — the correctness cost. Fleet wall-clock and any
ensemble-size adjustment recorded in AMENDMENT 3 if made.
