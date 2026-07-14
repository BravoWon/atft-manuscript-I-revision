# §7.1 Rung 2 — Density channel verdict (2026-07-14)

**Observables:** local sheaf (N=1000, K=100, superposition transport, σ=1/2,
edge-matched 2492), exact Frobenius rigidity ‖L‖_F and GPU bulk heat trace
Tr(e^{−βL}). **Verdict: H_sheaf OUTCOME 2 — separation is GEOMETRIC, not arithmetic.**

## The separation (large, robust)

| | zeta | GUE ensemble (n=13) | z-score |
|---|---|---|---|
| ‖L‖_F | 1746.0 | 1794.0 ± 1.4 [1791.3, 1795.9] | **−34.3** |
| heat Tr(e^{−L}) | 10426 | 12471 ± 93 [12301, 12605] | **−21.9** |

zeta's local sheaf spectrum is far more rigid than *every* GUE draw. `Tr(L)`
matched to 0.002%, so it is a genuine spectral-shape difference, not a scale
shift.

## The attribution test (the decisive part)

Keep zeta's exact geometry + prime-representation bases; scramble ONLY the
prime-frequency structure in the transport A[e]=Σ_p e^{iΔγ log p} B_p:

| zeta variant | ‖L‖_F | heat(β=1) |
|---|---|---|
| baseline (real primes) | 1746.5 | 10432 |
| frequency-randomized (log p → uniform random) | 1744.6 | 10434 |
| **primes destroyed (log p → 0, flat connection)** | 1734.5 | 10429 |
| — GUE band — | 1794.0 | 12471 |

**Scrambling the primes — even zeroing them — leaves zeta far below the GUE
band.** The heat trace is essentially invariant (10429–10434). The monkeypatch
is verified live (the log p→0 case moved ‖L‖_F by 12, so the patch reaches the
transport; the *frequencies* just don't drive the signal).

## Verdict (preregistered rule)

Per PREREGISTRATION_LONGRANGE §5: *"a zeta-vs-GUE separation is called arithmetic
ONLY if prime-scrambling controls kill it; separation that survives scrambling is
generic structure, not primes."* The separation **survives** → it is **geometric**.

**H_sheaf = outcome 2** (density channel adds no arithmetic power). The z=−34
rigidity signal is driven by zeta's point *geometry*, not the primes. This was
the preregistered weak-prior prediction ("no added power"), confirmed.

## Why the control was essential

A z = −34 separation *looks* like a strong arithmetic discovery. The mandatory
scrambling control correctly attributed it to geometry — preventing a false
"the sheaf detects prime rigidity in zeta" claim. This is the honesty rail
working exactly as designed.

## Honest open caveats (what this does NOT settle)

1. **The geometric difference itself is unexplained and may be partly a
   construction artifact.** Montgomery says zeta's local *spacings* match GUE,
   yet zeta's sheaf is systematically more rigid (z=−34). This likely reflects a
   difference in how the point sets are built (zeta: Riemann–von Mangoldt /
   JTopo unfolding to mean spacing 1; GUE: tridiagonal spacings rescaled to
   zeta's range) rather than a deep feature. A geometry-only control
   (match the exact spacing distributions) is needed to resolve — but it is
   *orthogonal to the arithmetic question*, which is settled: not primes.
2. **Only the DENSITY channel is tested.** The arithmetic signal, if present in
   the sheaf, would live in the FLUCTUATION statistics (spectral number
   variance / form factor), which the gate (RUNG2_GATE_RESULT.md) showed are
   NOT stochastic-trace-computable — they need exact eigenvalues (CPU). That
   channel remains untested.
3. **Only the LOCAL sheaf.** The long-range band-sheaf is not built.

## Net

Rung 2 density channel: **negative for arithmetic** (geometric separation,
prime-invariant). The GPU-fast observable does not detect prime structure. The
arithmetic hypothesis for the sheaf now rests on the exact-CPU fluctuation
statistics and/or the long-range band-sheaf — both harder, neither GPU-fast.
