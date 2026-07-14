# §7.1 Rung 2 — GPU instrument validation gate (2026-07-14)

**Gate (per PREREGISTRATION_LONGRANGE §4):** validate the GPU stochastic-trace
estimator against a dense `eigvalsh` reference on a small sheaf (dim 5000,
N=50 zeta points × K=100, exact ground truth) before any Rung-2 number counts.

## Result — a clean split, and a corrected observable list

**Heat trace Tr(e^{−βL}) — VALIDATED in the bulk, fails at the edge:**

| β | exact | GPU-SLQ | error | regime |
|---|---|---|---|---|
| 1 | 139.6 | 137.0 | 1.9% | bulk ✓ |
| 5 | 76.1 | 72.5 | 4.8% | bulk ✓ |
| 20 | 43.9 | 37.9 | 14% | transition |
| 50 | 25.4 | 18.3 | 28% | edge ✗ |
| 100 | 16.4 | 10.6 | 35% | edge ✗ |

**Spectral number variance Σ²_spec(L) — NOT stochastic-trace-computable
(fundamental):**

| L | exact | GPU | error |
|---|---|---|---|
| 5 | 28.4 | 1.7 | 94% |
| 50 | 328.6 | 2.6 | 99% |
| 100 | 477.9 | 2.5 | 99.5% |

## The fundamental finding

**Number variance is a FLUCTUATION statistic; stochastic trace gives only the
MEAN density.** Σ²(L) measures how the eigenvalue count fluctuates as a window
slides — it requires the individual eigenvalue *positions*. Stochastic trace
(KPM/SLQ) estimates `Tr(f(L))` for smooth f — the smooth mean spectral density.
You cannot recover a fluctuation/rigidity statistic from a mean-density
estimator. (Worse: number variance's window edges are sharp cuts → the same
Gibbs/edge problem, doubly.) This is a *category* limit, not a tuning gap.

## Corrected Rung-2 instrument map

| observable | nature | instrument |
|---|---|---|
| heat trace Tr(e^{−βL}), bulk β (≤~5) | smooth trace functional (mean density) | **GPU stochastic trace** ✓ (validated <5%) |
| heat trace, large β (near-kernel) | edge | exact CPU |
| spectral **number variance** Σ²_spec, **form factor** K(τ) | eigenvalue **fluctuation / rigidity** | **exact eigenvalues (CPU)** — NOT stochastic trace |

## Consequence for Rung 2 (honest)

The arithmetic signal in Rung 1 lived in a **fluctuation statistic** (point-process
number variance). If the sheaf-spectrum arithmetic signal is *also* a fluctuation
statistic (likely, by analogy), then the discriminator needs **exact sheaf
eigenvalues** — the slow CPU wall of §5.3, not the GPU. The GPU's genuine Rung-2
role is narrower than the prereg assumed: the **heat-trace curve Tr(e^{−βL}) vs
bulk β** — a *density-level* discriminator. Open question, now sharpened:

> Does the sheaf-spectrum arithmetic imprint on the **density** (heat-trace curve,
> GPU-fast) or only on the **fluctuations** (number variance / form factor,
> exact-CPU-only)?

## Amendment to PREREGISTRATION_LONGRANGE §4

Strike "sheaf spectral number variance Σ²_sheaf(L)" from the GPU-instrument row;
it moves to the exact-CPU row. The GPU row keeps only the bulk-β heat trace,
validated here. Number variance / form factor of the sheaf spectrum require
exact eigenvalues. This is logged, not silently changed.

## The gate worked

This is precisely why the validation gate is mandatory: it caught that a
headline Rung-2 observable was uncomputable by the intended fast instrument
*before* a single wrong number was reported.
