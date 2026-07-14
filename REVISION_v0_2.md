# ATFT Manuscript I — Revision v0.1 → v0.2

**Date:** 2026-07-13. Every edit below is keyed to the referee finding(s) it
resolves (see `ATFT_Manuscript_I_REFEREE_REPORT.md`, 32 verified findings).
Text in blockquotes is drop-in replacement/insertion prose. Section 5.3's new
table is **PENDING COMPUTE** — the 122-solve powered fleet (preregistered in
`PREREGISTRATION_POWERED_NULL.md`) fills it when it lands.

**Numbering note:** the GO order requested "Corollary 3.6", but Theorem 3.6
(path decomposition) already exists; the new result is numbered **Corollary
3.7** and placed at the end of §3.3.

---

## EDIT 1 — §3.3: new Corollary 3.7 + corrected prose (MATH-1, RT-7)

**Delete** the sentence: "Normalization changes the common spectral scale but
not the diagonal symmetrization or real-spectrum property."

**Replace with:**

> The normalization is *not* a common change of spectral scale. Because the
> per-prime factor depends on both p and σ, normalization re-weights primes
> relative to one another as σ moves — and this non-uniformity has exact
> spectral consequences, recorded in the following corollary.
>
> **Corollary 3.7 (normalization breaks cross-σ isospectrality; reality and
> the functional-equation symmetry survive).** Let
> G_K(σ) = Σ_{p≤K} B_{K,p}(σ) / ||B_{K,p}(σ)||_F
> be the per-prime Frobenius-normalized generator (the implemented
> functional-equation transport mode), and write
> c_p(σ) = ||B_{K,p}(σ)||_F^{-1} = [log p · √⌊K/p⌋ · √(p^{-2σ} + p^{-2(1-σ)})]^{-1}
> from (3.3). Then:
> (i) *Reality.* G_K(σ) = D_K(σ) [Σ_p c_p(σ) B_{K,p}(1/2)] D_K(σ)^{-1}: every
> block conjugates by the *same* D_K(σ) (Theorem 3.1) and positive scalars
> respect similarity, so G_K(σ) is similar to a real symmetric matrix and has
> real spectrum for every real σ.
> (ii) *Broken isospectrality.* The weight ratios c_p(σ)/c_q(σ) vary with σ
> whenever p ≠ q, so G_K(σ) and G_K(σ′) are in general *not* isospectral for
> |σ − 1/2| ≠ |σ′ − 1/2|. Corollary 3.2's σ-independence does not survive
> normalization.
> (iii) *Functional-equation symmetry.* c_p(σ) = c_p(1−σ) exactly, so G_K(σ)
> and G_K(1−σ) *are* isospectral: the normalized spectrum is a function of
> |σ − 1/2| alone.
> *Numerical witness (K = 120, π(120) = 30 primes):* max|Im λ| = 1.9·10⁻¹⁷ (reality);
> ‖spec G(0.3) − spec G(0.5)‖_∞ = 1.17 — an O(1) spectral shift, not
> roundoff (broken isospectrality); ‖spec G(0.3) − spec G(0.7)‖_∞ = 3.9·10⁻¹⁵
> (exact σ ↔ 1−σ symmetry). The relative small-vs-large-prime weight
> c_2/c_97 moves from 0.122 at σ = 1/2 to 0.501 at σ = 0.1.
>
> Corollary 3.7 answers a natural objection to the whole program: if all
> finite generator spectra were σ-independent (Corollary 3.2), eigenvalue
> observables would be vacuous in the parameter of interest. They are not.
> The *implemented* operator's spectrum carries a genuine dependence on the
> distance |σ − 1/2| to the critical line — introduced, transparently, by the
> normalization itself. Two honesty rails attach. First, this σ-sensitivity
> is engineered (like the defect (3.4)); observing it verifies the
> construction and says nothing about unknown zeta zeros. Second, by (iii)
> even normalized spectra cannot distinguish σ from 1 − σ: the critical line
> is visible to them only as the fixed point of the functional-equation
> symmetry, never as a one-sided selection.

## EDIT 2 — §6, first paragraph (MATH-1 knock-on)

**Replace** "Finite generator eigenvalues are not critical-line selectors
because of diagonal similarity." **with:**

> Finite *unnormalized* generator eigenvalues are not critical-line selectors
> because of diagonal similarity (Corollary 3.2). The implemented per-prime-
> normalized generator does retain |σ − 1/2|-dependent spectra (Corollary
> 3.7), but by symmetry these cannot distinguish σ from 1 − σ, so no finite
> spectrum in this family singles out the critical line except as the fixed
> point of the functional-equation symmetry.

## EDIT 3 — new §9 "Limitations and falsification criteria" (DRIFT-2)

Insert after current §8; renumber Discussion → §10, Conclusion → §11.

> **9. Limitations and falsification criteria**
>
> **9.1 Limitations.** (i) One zeta sequence: the arithmetic side of every
> comparison is a single structured sample; all uncertainty derives from
> control ensembles. (ii) Finite truncation: every statement is about the
> K-truncated family; §6.2 lists what a K → ∞ theorem would require, and none
> of it is established here. (iii) Constructed symmetry: the critical-line
> structure of §3 (and the |σ − 1/2| sensitivity of Corollary 3.7) is
> engineered by the functional-equation weighting; its observation validates
> the construction only. (iv) The SU(2) and 3-SAT designs of §7.2–7.3 are
> unexecuted protocols, not results.
>
> **9.2 Falsification criteria.** We commit to the following outcomes as
> falsifying, in print, before the experiments are run:
> **F1 (long-range arithmetic hypothesis — Gate B).** If, under the §7.1
> protocol (≥100 GUE controls, matched band geometry, matched solver
> tolerance, residual-certified kernels), zeta's long-range observables
> (Σ²(L), K(τ), band near-kernels, transport non-normality) lie within the
> control ensembles at every preregistered band, then the hypothesis that
> this machinery detects arithmetic structure beyond level repulsion is
> falsified — not "open," falsified — and any continuation must propose a
> different observable family.
> **F2 (instrument validity).** If the pipeline fails its positive controls —
> the Poisson/GUE near-kernel separation of §5.3, or a known-structure
> benchmark — at any preregistered configuration, the observable family is
> invalid as a detector and no null result from it carries evidential weight.
> **F3 (SU(2) sheaf enrichment — Gate A).** If the rebuilt gauge-invariant
> sheaf observable of §7.2 adds no detection power or information beyond
> ordinary persistence under finite-size scaling, the sheaf-enrichment claim
> for critical phenomena is falsified for this construction.
> **What would NOT falsify:** a local-observable null (§5.3 already
> establishes it); failure to prove any K → ∞ statement (out of scope, §6.2);
> and no outcome of any experiment here bears on RH in either direction
> (§1.2).

## EDIT 4 — §7.1 restored protocol items (DRIFT-3)

**Insert as new first bullet:**

> - Step zero: independently reproduce the corrected matched-edge local null
>   of §5.3 on the published pipeline (same instrument, ≥100 GUE draws,
>   residual-certified) before any long-range measurement is attempted.

**Amend the controls bullet** ("Compare prime phases log p against...") to end:

> ...and geometry-only controls, **retaining the Poisson and evenly spaced
> ensembles of §5.3 at identical geometry** so the long-range experiment
> remains anchored to the local baseline.

**Append as final bullet:**

> - Protocol scope wall, stated inside the preregistration itself: detection
>   of a finite-sample arithmetic correction in any long-range observable
>   would not imply RH (§1.2), and a null across all bands triggers F1 of
>   §9.2.

## EDIT 5 — §7.3 preregistration bullet (DRIFT-7) + §7.2 S3 note (DRIFT-5)

§7.3, **append:**

> Observables and analysis plans must be preregistered before any transition
> statistic is computed; the reported statistic must never be selected after
> seeing the transition (the forking-paths control this program adopted after
> the audit of §5).

§7.2, **append:**

> The previously reported plaquette discontinuity at β = 2.30 (claim S3 of
> the program ledger) remains unvalidated pending this rebuild — obtained at
> 8³×4 with five configurations per coupling [3, atft/experiments/
> p5_lattice_gauge.py] — and is not asserted here.

## EDIT 6 — Rule 8.7 reword (IC-6, RT-6, DRIFT-8)

**Replace** bullet 7 of §8 **with:**

> Retracted values must remain visible in provenance records and must not
> reappear **as asserted results** in abstracts, figures, or derived claims;
> they may be named solely as objects of retraction, explicitly labeled as
> such (as in this paper's abstract).

## EDIT 7 — §5.1 reconciliation of "≥ 30" vs 24 (IC-4, MATH-2)

**Replace** "The audit found at least thirty near-zero modes." **with:**

> The audit's initial converged run found at least thirty near-zero modes —
> a count *censored at the 30-eigenvalue solver window* and obtained before
> solver tolerances were equalized across sources; the audit record [4] shows
> the tolerance mismatch alone moved zeta's count between 24 and 30. The
> matched-tolerance v0.1 configuration gave 24 — but that number was itself
> solver-limited: at tol = 10⁻⁴ the eigenpair residuals (~10⁻³) sit at the
> counting threshold. At certified tolerance the value is **58** (spectral-flip
> — the validated primary solver, residual 2·10⁻⁶); the shift-invert cross-check
> reads 62, but that family was disqualified after it collapsed on the GUE
> matrices (EDIT 11 solver note), so 58 is the quotable certified count. The
> numbers are one story — the count is a function of solver rigor until
> residuals are driven far below the threshold — and Table 2 (§5.3) quotes only
> certified spectral-flip values.

## EDIT 8 — §3 positioning + Theorem 3.5 qualifier (RT-3, RT-4)

**Insert after Corollary 3.4:**

> These finite statements sit inside two classical frameworks, and we claim
> no novelty for their forms. Diagonal symmetrization of a weighted-shift
> family is the standard balancing/symmetrization similarity for
> symmetrizable matrices [10]; Corollaries 3.3–3.4 are the quasi-Hermitian /
> metric-operator setting of Dieudonné [11], Scholtz–Geyer–Hahne [12], and
> the pseudo-Hermitian program of Mostafazadeh [13], with M_K(σ) the metric
> operator. What we take to be new here is not the similarity but (a) the
> exact arithmetic form of the symmetrizer forced by prime multiplication,
> (b) the uniform-conditioning characterization of the critical line
> (Theorem 3.5), and (c) the normalization spectroscopy of Corollary 3.7 —
> together with the convergence-audit case study of §5.
>
> One uniqueness caveat: Theorem 3.5 concerns the *natural diagonal*
> symmetrizer D_K(σ). The full set of admissible metrics for B_K(σ) is
> M = D_K(σ)^{-1} C D_K(σ)^{-1} with C positive definite and commuting with
> B_K(1/2); since B_K(1/2) has degenerate eigenvalues (Theorem 3.6 forces
> heavy multiplicity across single-prime path components), C is not unique,
> and Theorem 3.5 does not assert that *every* admissible metric family is
> ill-conditioned off the critical line. The claim is that the arithmetic
> symmetrizer forced by the construction is — which is the statement the
> abstract and conclusion now carry.

**Abstract**, replace "hence sigma = 1/2 is the unique parameter for which the
canonical metric remains uniformly well-conditioned as the fiber cutoff
grows" **with** "hence sigma = 1/2 is the unique parameter at which this
natural arithmetic symmetrizer remains uniformly well-conditioned as the
fiber cutoff grows". Make the parallel change in §10 (Conclusion).

## EDIT 9 — §4 monograph citation (IC-2) + [3] file-list amendment (IC-8)

§4 first sentence → "The ATFT monograph **[14]** alternates between two onset
definitions..." (same for the §7.3 mention).

Reference [3]: **append to the file list**
"atft/experiments/p5_lattice_gauge.py; atft/lattice/su2.py" (the SU(2)
benchmark script audited in §4 and §7.2).

## EDIT 10 — §7.2 SU(2) claim gets its proof (IC-7)

**Replace** "Its proposed parity-odd feature q_{mu nu} = 1/2 Im Tr P_{mu nu}
is identically zero for SU(2), because every SU(2) matrix has real trace."
**with:**

> **Remark 7.1.** The proposed parity-odd feature q_{μν} = ½ Im Tr P_{μν} is
> identically zero: every U ∈ SU(2) is U = a₀I + i·Σⱼaⱼσⱼ with a real and
> the σⱼ traceless, so Tr U = 2a₀ ∈ ℝ; a plaquette product is again in
> SU(2). (Verified numerically to 4·10⁻¹⁶ over 10⁴ random plaquettes.) A
> valid lattice topological density requires an ε_{μνρσ}-weighted
> field-strength construction with controlled smoothing, or another
> independently validated gauge-invariant definition.

Add to §1.1 contributions list: "A proof that the previously proposed SU(2)
parity-odd feature is identically zero (Remark 7.1), closing claim S2 of the
program ledger."

## EDIT 11 — §5.3 powered table (RT-1, MATH-3, RT-5, RT-2) — PENDING SOLVER RESOLUTION

Replace the 5-row table and its prose with the powered version. Numbers land
when the fleet completes **on the solver that survives the cross-family
diagnostic** (see the EDIT 11 solver note in Status). All counts are
residual-certified (‖Lx − λx‖ < 10⁻⁵) and reported at the k that uncensors the
10⁻³ threshold (k = 80 for the certified zeta solve). The single filled cell
below is the zeta value from the surviving-solver check; every other cell is
withheld until both solver families agree per source.

> Edge-matched near-kernel counts (<10⁻³), residual-certified (‖Lx − λx‖ <
> 10⁻⁵), k = 80, two solver families cross-checked per source:
>
> | source | n | edges | near-kernel (<10⁻³) | zeta quantile |
> |---|---|---|---|---|
> | zeta | 1 | 2492 | **58** (certified spectral-flip, residual 2·10⁻⁶; shift-invert cross-check 62, that family disqualified on GUE collapse) | [PENDING] of GUE ensemble |
> | GUE ensemble | 100 | 2492 | [PENDING — solver resolution] | — |
> | Poisson ensemble | 20 | 2492 | [PENDING — solver resolution] | — |
> | even | 1 | 2492 | [PENDING] | — |
>
> Tolerance sweep: counts at {10⁻⁸ … 2·10⁻³} in the reproducibility record
> [18]; censoring flagged per draw. Poisson-vs-GUE separation (the instrument's
> positive control): Mann–Whitney p = [PENDING], rank-biserial = [PENDING].
> Hyperparameters: N = 1000, K = 100, σ = 1/2, superposition transport,
> zeta ε = 3.0; controls bisected to 2492 edges; seeds 2000–2099 (GUE),
> {42, 4000–4018} (Poisson); numpy/scipy versions and the JTopo commit in
> the record. **Both solver families (shift-invert and spectral-flip) reported
> per source with per-pair residual certificates**; any source where they
> disagree beyond tolerance is flagged, not averaged (§8 criterion 2).

Also update the abstract's final sentence per RT-8:
"arithmetic specificity, if detectable by this machinery, **is not visible in
local Rips geometry at this configuration and should be sought** in
long-range spectral rigidity."

## EDIT 12 — references (LIT-1..4, IC-1) 

Corrections:
- **[2]** Wei & Wei, Foundations of Data Science **7(2)** (2025), **446–463**; arXiv:2112.10906.
- **[5]** Sale, Lucini & Giansiracusa, "**Probing center vortices and
  deconfinement in SU(2) lattice gauge theory with persistent homology**,"
  Phys. Rev. D 107 (2023) 034501; arXiv:2207.13392.
- **[8]** **M. M.** Lugar, M. B. Milinovich, **E.** Quesada-Herrera, "On the
  number variance of zeta zeros and a conjecture of Berry," arXiv:2211.14918
  (to appear, Mathematika).

New entries:
- **[11]** J. Dieudonné, "Quasi-Hermitian operators," Proc. Int. Symp. Linear
  Spaces (Jerusalem 1960), Pergamon, 1961, 115–123.
- **[12]** F. G. Scholtz, H. B. Geyer, F. J. W. Hahne, "Quasi-Hermitian
  operators in quantum mechanics and the variational principle," Ann. Phys.
  213 (1992) 74–101.
- **[13]** A. Mostafazadeh, "Pseudo-Hermitian representation of quantum
  mechanics," Int. J. Geom. Methods Mod. Phys. 7 (2010) 1191–1306.
- **[14]** B. A. Jones, *Adaptive Topological Field Theory* (program
  monograph), files docs/framework_theories/adaptive_topological_field_theory.pdf
  and docs/paper/atft_v2.md in [3], commit aa6a30034864b271d256f91a9bef367c3d6d7cc8.
- **[15]** A. M. Odlyzko, "On the distribution of spacings between zeros of
  the zeta function," Math. Comp. 48 (1987) 273–308.
- **[16]** M. V. Berry, "Semiclassical formula for the number variance of the
  Riemann zeros," Nonlinearity 1 (1988) 399–407.

Wire dangling refs into the body (IC-1):
- §5.1, after "hand-written Lanczos procedure": cite **[9, 10]** (restarting
  and reorthogonalization practice; symmetric eigenproblem theory).
- §7.1, number-variance sentence: "Number variance and the spectral form
  factor concentrate arithmetic corrections that are nearly invisible in
  nearest-neighbor spacings **[7, 8, 15, 16]**."
- §5.3 / §2.1: cite **[15]** for the unfolded-zeta-vs-GUE comparison baseline.

## EDIT 13 — small consistency fixes (IC-3, IC-5)

- Reference Figure 1 from §3.1 text: "...diverges polynomially in K otherwise
  **(Figure 1)**."
- Number the tables (Table 1 = §5.2 corrected values; Table 2 = §5.3 powered
  null; Table 3 = Appendix B ledger) and reference each from its prose.
- §5.3 footnote (supersedes IC-5 once the powered run lands, which bisects
  ALL controls to exactly 2492): "In the v0.1 table the Poisson control sat
  at 2491 edges (bisection undershoot by one edge); the v0.2 run bisects all
  controls to exactly 2492."

## EDIT 14 — Appendix B ledger: one REPLACEMENT + appended rows (DRIFT-6, DRIFT-4)

**14a — REPLACE** the existing Appendix B row 1 (currently "B_K(σ) is
Hermitian only at 1/2 | proved, canonical Euclidean metric | forward and
reverse coefficients match only at 1/2") — do **not** leave it in place beside
a near-duplicate — **with:**

> | B_K(σ) Hermitian in the canonical metric only at Re σ = 1/2 | proved, with M3's conditions: **real σ** and ρ_p ≠ ρ_pᵀ (the latter automatic for truncated multiplication) | forward/reverse coefficients p^{−σ}, p^{−(1−σ)} match only at σ = 1/2; for complex σ, Hermiticity holds on the whole line Re σ = 1/2 (‖B−B*‖_F = 0 at σ = 1/2 + it), so "only at 1/2" is a statement about **real** σ |

(The real-σ qualifier is load-bearing: dropping it makes the row false, since
B is Hermitian everywhere on Re σ = 1/2. Corollary 3.4's proof is amended in
parallel to state both hypotheses explicitly.)

**14b — REPLACE** Appendix B row 4 (RT-4 exposure): the row reading "critical
line uniquely preserves a uniformly conditioned canonical metric | proved |
κ(D_K)=K^{|σ−1/2|}" **with:**

> | the **natural arithmetic symmetrizer** D_K uniquely preserves a uniformly conditioned canonical metric at σ = 1/2 | proved (for D_K; not claimed for every admissible metric M = D⁻¹CD⁻¹) | κ₂(D_K) = K^{|σ−1/2|}, Theorem 3.5 |

**14c — APPEND rows** (DRIFT-6 — every claim the manuscript asserts or defers
now has a row, so "deferred" is distinguishable from "quietly dropped"):

> | local observable separates level-repulsive from Poisson-like spectra (Z3) | supported, quantified | §5.3 powered ensembles: [PENDING p, effect size] |
> | current SU(2) script implements a sheaf Laplacian (S1) | false | ordinary H0/MST persistence on a Euclidean cloud (§4, §7.2) |
> | q = ½ Im Tr P captures SU(2) topological charge (S2) | false | Tr U ∈ ℝ for U ∈ SU(2); Remark 7.1 |
> | β = 2.30 SU(2) discontinuity validates deconfinement (S3) | unvalidated | 5 configs/coupling at 8³×4 [3, output/atft_validation/p5_lattice_gauge.json]; independent rebuild required (§7.2) |
> | 3-SAT clause-graph approaches detect the SAT transition (C1) | failed | monotone instance structure; solution-cloud protocol replaces it (§7.3) |
> | 3-SAT solution-overlap cloud detects clustering/shattering (C2) | **deferred — open experiment** | §7.3 protocol; not attempted in this paper |
> | Prime Scalar Field claims (P1–P3) | **deferred — out of scope of this paper** | listed for ledger completeness; belongs to the companion PSF study, not this manuscript |
> | normalization preserves a "common spectral scale" | false (corrected in v0.2) | per-prime, σ-dependent re-weighting; Corollary 3.7 |

## EDIT 15 — Appendix A max-rank correction (MATH-4)

**Replace** "Adding edges adds rows and potential constraints, so edge count
directly affects the maximum possible rank and therefore the kernel."
**with:**

> The maximum possible rank of the EK × NK coboundary is min(EK, NK). Adding
> edges therefore raises the rank *cap* only while E < N; once the Rips graph
> is connected (E ≥ N − 1, so EK is within K of NK), the cap is NK and further
> edges cannot raise it. Beyond that regime, edges reduce the kernel only by
> making existing constraints independent — a function of restriction maps and
> cycle holonomy, not edge count alone (which is why matched edge count is
> necessary but not sufficient, Appendix A). In the reported experiments
> E = 2492 ≫ N, so the kernel is governed by constraint independence, not by
> the rank cap.

## EDIT 16 — §7.1: define the non-normality / pseudospectral observables (RT-7)

The manuscript names "transport non-normality" and "pseudospectral
sensitivity" (§6, §7.1) without defining them as statistics. **Amend the §7.1
observables bullet** ("Report number variance Σ²(L), spectral form factor
K(τ), exact kernel, soft-mode density, and transport non-normality as separate
observables.") **to:**

> Report as separate observables, each with a preregistered estimator: number
> variance Σ²(L); spectral form factor K(τ); exact-kernel dimension and
> soft-mode density at fixed tolerance; and two non-normality statistics of
> the transport generator B — the departure from normality
> d_F(B) = (‖B‖_F² − Σ_i|λ_i|²)^{1/2} (Henrici), and the ε-pseudospectral area
> ratio A_ε(B)/A_ε(diag λ) computed on a fixed grid at ε = 10⁻³, 10⁻² (methods
> per Trefethen & Embree [17]). These quantify the σ-dependent structure that
> Corollary 3.2 removes from the eigenvalues but Corollary 3.7 and
> non-normality retain — the concrete answer to "what is left to measure once
> the finite spectrum is σ-independent."

Add reference **[17]** L. N. Trefethen & M. Embree, *Spectra and
Pseudospectra*, Princeton, 2005. (Status-table mapping for RT-7 corrected: it
is EDIT 16, not EDIT 1.)

## EDIT 17 — remaining sub-element fixes (RT-5 archival, DRIFT-5 protocol, RT-4/§10, numbering)

- **17a (RT-5 archival).** Add reference **[18]** B. A. Jones, "ATFT
  convergence-audit scripts, matrices, and powered-null records" (Zenodo
  archive, DOI to be minted at submission; snapshot of the
  `atft-manuscript-revision/` tree + JTopo commit aa6a300). §8 and §5.3 point
  to [18] for the residual-certified eigenvalues, not to a bare repo path.
- **17b (DRIFT-5 protocol).** §7.2, extend the SU(2) rebuild list to restore
  charter 4C.2/4C.5: "verify thermalization and autocorrelation times, plaquette
  curves, and **Polyakov-loop susceptibility**; extract a **pseudocritical
  coupling with uncertainty via finite-size scaling** across ≥3 spatial
  volumes." Source the "8³×4, 5 configs/coupling" figures to
  [3, output/atft_validation/p5_lattice_gauge.json].
- **17c (RT-4 / numbering).** EDIT 8's "parallel change in §10 (Conclusion)"
  now reads **§11** (EDIT 3 renumbers Conclusion → §11; Discussion → §10). The
  §3 positioning insert (EDIT 8) forward-references Theorem 3.5 / Corollary 3.7;
  add "(stated below)" at first mention to flag the forward reference.

## EDIT 18 — charter-side ledger rows M5–M8 (DRIFT-1)

Not a manuscript edit — a one-block update to the **research charter's** §2
ledger, so the charter (the program's gate document) tracks the manuscript's
new theorems:

> | M5 | D_K(σ)⁻¹ B_K(σ) D_K(σ) = B_K(1/2) for all real σ, K ≥ 2 (diagonal similarity). | **Proved** | Theorem 3.1. |
> | M6 | All B_K(σ) are isospectral with real, σ-independent spectrum before normalization. | **Proved** | Corollary 3.2. Note: normalization breaks cross-σ isospectrality (Corollary 3.7). |
> | M7 | κ₂(D_K(σ)) = K^{|σ−1/2|}; σ = 1/2 is the unique uniformly-conditioned parameter for the natural symmetrizer D_K. | **Proved** | Theorem 3.5; not claimed for all admissible metrics. |
> | M8 | Single-prime block spectrum = ⋃ 2 log p · p^{−1/2} cos(jπ/(ℓ_m+1)); H0 death-quantile ≠ sheaf spectral-gap onset. | **Proved** | Theorems 3.6, Proposition 4.1. |

---

## Status (post RT-04 recursion — verifier drift 0.781 → recursed)

| edit | resolves | status |
|---|---|---|
| 1 | MATH-1 | drafted; witness header corrected (π(120)=30) |
| 2 | MATH-1 knock-on | drafted |
| 3 | DRIFT-2 | drafted |
| 4 | DRIFT-3 | drafted |
| 5 | DRIFT-5, DRIFT-7 | drafted (protocol half completed in 17b) |
| 6 | IC-6, RT-6, DRIFT-8 | drafted |
| 7 | IC-4, MATH-2 | drafted (sourced [4] line 123) |
| 8 | RT-3, RT-4 | drafted (Appx B exposure fixed in 14b; numbering in 17c) |
| 9, 10 | IC-2, IC-8, IC-7 | drafted |
| 11 | RT-1, MATH-3, RT-5, RT-2, RT-8 | **PENDING SOLVER RESOLUTION** — see note |
| 12 | LIT-1..4, IC-1 | drafted |
| 13 | IC-3, IC-5 | drafted |
| 14 | DRIFT-4, DRIFT-6, RT-4 | drafted (14a real-σ restored; 14b row 4; 14c C2/P1–P3) |
| 15 | MATH-4 | drafted (was dropped; now covered) |
| 16 | RT-7 | drafted (was falsely marked resolved; now a real edit) |
| 17 | RT-5 archival, DRIFT-5 protocol, numbering | drafted |
| 18 | DRIFT-1 | drafted (charter-side) |

**All 32 findings now have a drafted edit.** (Prior status table over-claimed:
MATH-4 had no edit and RT-7's fix was cosmetic; both corrected above.)

**EDIT 11 solver note (cross-solver diagnostic RESOLVED):** the powered-null
fleet surfaced a solver artifact — shift-invert (σ = −10⁻⁶) returned an
all-zero 80-mode spectrum on the GUE matrices (`gue_2000`), disagreeing with
the spectral-flip audit. A three-way diagnostic disqualified shift-invert
(silent degeneracy) and **certified spectral-flip as the §5.3 solver**;
zeta's certified near-kernel is **58** (spectral-flip, residual 2·10⁻⁶), with
the shift-invert cross-check (62) retained only as the collapse diagnostic.
**Remaining pending item:** the GUE *band* — the k=100 window **censors most
GUE draws** (their near-kernel exceeds 100), so the band's values are
floor-estimates. The direction is certified and strong (zeta 58 ≪ GUE, below
all draws); a clean quantitative band needs a **k ≥ 150 rerun**. Table 2's GUE
cells stay `[PENDING]` until then. This is the manuscript's own §8
second-solver + tolerance-sweep criteria doing their job before publication.
