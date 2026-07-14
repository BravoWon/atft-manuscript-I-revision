# Preregistration — §7.1 Long-Range Arithmetic Observable

**Date:** 2026-07-13. Committed BEFORE any zeta-vs-control long-range comparison
is computed. Companion to the local null (§5.3): zeta's near-kernel (58) sits
below the GUE band (76), certified — the local channel is empty, as
Montgomery–Odlyzko predicts. This experiment tests whether the arithmetic
survives at **long range**, where zeta and GUE are known to diverge.

---

## 1. Question and hypotheses

**Physics.** Zeta zeros match GUE **local** spacing statistics (Montgomery
pair-correlation; Odlyzko numerics) — proven-strength, and why §5.3 nulled.
But at **long range** they diverge: Berry (1988) showed the zeta zeros'
**number variance Σ²(L) saturates** at large L (the primes make the zeros
*more rigid* than GUE, whose Σ²(L) grows logarithmically). The arithmetic lives
in long-range spectral rigidity.

**H_LR (validation / positive control).** The long-range statistics of the raw
unfolded zeros separate zeta from GUE — zeta's Σ²(L) saturates, GUE's grows.
*This is an established result; reproducing it validates the pipeline and
proves the arithmetic is detectable at long range by construction.*

**H_sheaf (the novel, open test).** A **prime-weighted long-range sheaf
observable** detects the arithmetic rigidity, AND the signal is destroyed by
prime-label scrambling (i.e. it is attributable to the *specific* primes, not
generic level repulsion). The sheaf's prime-phase transport `exp(iΔγ log p)`
may *amplify* the arithmetic signal beyond the raw statistic — or may merely
re-encode it (no added power), or null. **No strong prior; this is the genuine
experiment.**

**Governing distinction (from `CRITIQUE_INTEGRATION.md`): structural ≠
statistical ≠ semantic influence.** Σ²(L)/K(τ) are *statistical* observables of
the point process; the sheaf spectrum is *structural*. H_sheaf tests whether
structural enrichment recovers the statistical arithmetic signal.

---

## 2. Data (frozen)

- **Source:** Odlyzko high-precision zeta zeros, unfolded (mean spacing → 1) by
  the Riemann–von Mangoldt density `N(T) ≈ (T/2π)log(T/2πe)`. Same
  `SpectralUnfolding(method="zeta")` pipeline as §5.3, JTopo commit aa6a300.
- **N — the binding constraint, and it is satisfied.** Long-range
  number-variance saturation lives at window length L up to the arithmetic
  scale; resolving it needs **N ≥ 10⁴–10⁵ unfolded zeros** (the §5.3 N=1000 is
  *insufficient* and is not reused). The shipped `data/odlyzko_zeros.txt` holds
  **exactly 100,000 zeros** (γ = 14.134… to 74,920.827…) — enough for the full
  long-range regime with no new data. Frozen: use all 10⁵ (unfolded); the max
  frozen L is set to ≤ N/20 = 5000 so each Σ²(L) window average has ≥20
  independent samples. Zeta N and highest ordinate recorded in the run env.
- **Controls, ≥100 GUE + the structured set (each matched to zeta's N and
  unfolding):**
  - **GUE** (≥100 draws, seeds recorded) — the primary null (Σ² log-growth).
  - **Poisson/uniform** (≥20) — no level repulsion (Σ²(L)=L), negative control.
  - **Even** (1) — maximal rigidity (Σ²→const), the rigid extreme.
  - **Prime-label permutation** (≥20) — zeta ordinates, but the prime→phase
    assignment in the sheaf is permuted → isolates *which primes* matter.
  - **Phase randomization** (≥20) — transport phase `exp(iθ)` with θ uniform
    random instead of `Δγ log p` → tests the phase structure.
  - **Frequency randomization** (≥20) — `exp(iΔγ ω)` with ω range-matched random
    instead of `log p` → tests primes-specifically vs generic frequencies.

---

## 3. Two-rung protocol (frozen)

### Rung 1 — direct point-process statistics (validation, cheap, CPU)
Compute on the unfolded ordinates directly (no sheaf, no eigensolve):
- **Number variance Σ²(L)** = Var[ #zeros in a window of unfolded length L ],
  averaged over window positions, for L on a frozen grid {1, 2, 5, 10, 20, 50,
  100, 200, 500}.
- **Spectral form factor K(τ)** = |Σ_j e^{2πi τ x_j}|² (windowed, averaged),
  τ on a frozen grid; inspect for structure near the prime frequencies
  τ_p = log p / 2π for the first primes.
- **Dyson–Mehta Δ₃(L)** rigidity as a cross-check on Σ².

### Rung 2 — long-range band-sheaf observable (novel)
- **Band sheaf:** connect zeros i,j iff Δγ = γ_j − γ_i ∈ [b_lo, b_hi], a
  controlled separation band (NOT short-range Rips). Bands frozen on a grid
  {short, mid, long} in unfolded units, **selected before any zeta/control
  separation is observed**. Transport `U_e = exp(iΔγ log p)` prime-weighted,
  σ=1/2 (the critical-line-conditioned point, §3), K-dim arithmetic fibers as
  in §5.3.
- **Per band, compute the sheaf-spectrum global observables** (below), for zeta
  and every control, edge-count matched within each band.

---

## 4. Observables and estimators (each reported separately)

| observable | what it measures | instrument | certification |
|---|---|---|---|
| Σ²(L), K(τ), Δ₃ of the point process (Rung 1) | raw arithmetic rigidity | direct counting, CPU | exact |
| sheaf heat trace Tr(e^{−βL}) vs **bulk** β (Rung 2) | smooth mean-density functional | **GPU stochastic trace** | **VALIDATED, RUNG2_GATE_RESULT.md** (<5% at β≤5; fails large β) |
| sheaf spectral number variance Σ²_sheaf(L), form factor K(τ) (Rung 2) | eigenvalue **fluctuation / rigidity** | **exact eigenvalues (CPU)** — see AMENDMENT below | gate showed NOT stochastic-trace-computable |

**AMENDMENT (2026-07-14, RUNG2_GATE_RESULT.md):** the instrument-validation gate
found spectral **number variance / form factor are FLUCTUATION statistics** —
they need individual eigenvalue positions and cannot be obtained from a
mean-density stochastic-trace estimator (category limit, not tuning). They move
to the **exact-CPU** row. The GPU keeps only the bulk-β heat trace (validated).
Open question sharpened: does the sheaf arithmetic imprint on the DENSITY
(heat-trace curve, GPU-fast) or only on the FLUCTUATIONS (exact-CPU-only)?
| transport non-normality: Henrici d_F(B)=(‖B‖_F²−Σ|λ|²)^½; ε-pseudospectral area (Rung 2) | σ-dependent structure Cor 3.2 removes from eigenvalues (RT-7 edit) | CPU on B blocks | exact |

**GPU instrument validation gate (mandatory — we learned it fails on edge
counts).** Before any Rung-2 GPU number is trusted, the GPU stochastic-trace
estimator (`gpu_slq.py` / `gpu_eigencount.py`) is validated against a dense
`numpy.linalg.eigvalsh` reference on a small sheaf (N≤2000) for **each**
observable used: heat trace at the working β range, and bulk number variance.
Agreement criterion: within 2× the estimator's reported standard error across
the grid. **Established failure mode is on-record: sharp near-kernel edge counts
are NOT computed by the GPU tool — those remain exact CPU spectral-flip.** The
GPU is used only for the smooth global observables (heat trace, bulk Σ²), where
`GPU_EIGENCOUNT_VERDICT.md` shows it is the correct tool.

---

## 5. Decision rules and falsification (frozen)

- **Rung 1 (H_LR):** PASS iff zeta's Σ²(L) lies **below** the GUE ensemble band
  at large L with a saturation signature (dΣ²/dL → 0 for zeta, > 0 for GUE),
  exceedance p = (r+1)/(n+1) at the largest frozen L. *Expected to pass —
  Berry.* A Rung-1 **null** would indicate a pipeline bug (contradicts an
  established result), not a discovery.
- **Rung 2 (H_sheaf) — three pre-declared outcomes:**
  1. **Added power:** the sheaf observable separates zeta from the GUE band at
     ≥1 frozen band, AND prime-label permutation + frequency randomization
     **destroy** the separation (attribution to specific primes), AND phase
     randomization destroys it (attribution to the phase structure). → the
     sheaf enrichment carries arithmetic signal. Reported with effect size.
  2. **No added power:** the sheaf observable separates zeta from GUE *only as
     much as* Rung 1 does (the scrambles that preserve the raw statistic also
     preserve the sheaf separation). → the sheaf re-encodes, adds nothing.
  3. **F1 — FALSIFIED (§9.2):** the sheaf observable places zeta **within** the
     GUE band at **every** frozen band. → "a sheaf observable detects arithmetic
     beyond level repulsion" is falsified — *reported straight, not buried*, and
     any continuation must propose a different observable family.
- **Attribution rule (the honesty rail):** a zeta-vs-GUE separation is called
  *arithmetic* ONLY if prime-scrambling controls kill it. Separation that
  survives scrambling is generic structure, not primes — reported as such.

---

## 6. Prediction (committed now, un-tuned)

- **Rung 1:** zeta Σ²(L) **saturates**, GUE grows ~log L — **high confidence**
  (established; this is the positive control proving arithmetic is long-range
  and the instrument sees it).
- **Rung 2:** **genuinely open.** Weak prior toward outcome (2) "no added power"
  — the sheaf spectrum likely inherits the point-process rigidity without
  amplifying it — but outcome (1) is the hopeful case and F1 is a live,
  publishable result. I commit to reporting whichever lands.
- **Cross-check with §5.3:** the local null (zeta below GUE near-kernel) and a
  Rung-1 long-range separation (zeta below GUE Σ² band) are *consistent* — both
  say zeta is *more rigid / less noisy* than GUE, locally indistinguishable but
  long-range distinguishable. That coherence is itself a validation.

---

## 7. Scope wall

Detection of a finite-sample long-range arithmetic correction **does not imply
RH** (§1.2). No finite computation establishes the infinite-dimensional
spectral correspondence (§6.2). This experiment characterizes where the
arithmetic is *statistically visible* in this machinery; it makes no claim about
a self-adjoint operator whose spectrum is the zeta zeros.

---

## 8. Reproducibility (per §8 + AMENDMENT discipline)

All frozen parameters (N, unfolding, band grid, L grid, τ grid, β range, K, σ,
seeds, GPU estimator config + its validation residuals, JTopo commit) recorded
in `output/longrange/_environment.json` before the run. Every GPU observable
carries its standard error; every exact observable its residual. Bands, grids,
and decision thresholds are frozen here and not adjusted after seeing
separation. Retraction rule 8.7 applies: no value quotable without its
error/residual.
