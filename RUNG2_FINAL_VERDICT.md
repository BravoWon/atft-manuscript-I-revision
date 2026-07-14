# §7.1 Rung 2 — Final verdict, both channels (2026-07-14)

**Question:** does the prime-weighted sheaf add a zeta-specific *arithmetic*
discriminator beyond the raw point-process statistics? **Answer: NO (H_sheaf
outcome 2). The local sheaf carries no attributable arithmetic signal.**

## Density channel (‖L‖_F, heat trace) — separation is GEOMETRIC
- zeta vs GUE: z = −34 (‖L‖_F), −22 (heat). Huge separation.
- Prime-scramble (freq-random, log p → 0): zeta stays far below GUE band.
- **Survives scrambling ⇒ geometric, not arithmetic.** (RUNG2_DENSITY_VERDICT.md)

## Fluctuation channel (spectral number variance, exact dense eig, dim 6400) — NO separation
| L | zeta | GUE band | zeta z | freq-scr | primes→0 |
|---|---|---|---|---|---|
| 2 | 2.87 | 3.10±0.17 | −1.3 | 3.02 | 77 |
| 5 | 10.16 | 9.94±0.99 | 0.2 | 13.7 | 296 |
| 10 | 28.97 | 27.6±1.8 | 0.7 | 43.3 | 679 |
| 20 | 74.21 | 73.7±9.3 | 0.1 | 130 | 1426 |
| 50 | 225.1 | 221±41 | 0.1 | 412 | 3600 |
| 100 | 347.5 | 344±107 | 0.0 | 741 | 5391 |

- **zeta ≈ GUE at every L (z ≈ 0).** The fluctuation statistic does not
  distinguish zeta's sheaf spectrum from GUE.
- Scramble sensitivity is real (74→130→1426) but **generic**: structured phases
  → rigid spectrum, random/flat → disordered, for any geometry. Not zeta-specific.
- Caveat: freq-scramble used *uniform* random frequencies; a *log-distributed*
  random control is needed before any "real primes give GUE-matched rigidity"
  claim. Flagged as hypothesis, not finding.

## Synthesis with Rung 1
- **Rung 1 (raw zeros):** number variance SATURATES below GUE (Berry) — the
  arithmetic is real and lives in the zeros themselves. VALIDATED.
- **Rung 2 (sheaf):** the sheaf adds NO detectable arithmetic beyond geometry.
  Density separation is geometric; fluctuation shows no separation.

**Conclusion:** the arithmetic *effect* is genuine (Rung 1) but the sheaf
*construction* does not access it. The apparent sheaf signal (density z=−34) was
a geometric artifact. This is the preregistered weak-prior outcome ("no added
power"), confirmed on both channels.

## Scope of this verdict (honest limits)
- **Small sheaf (N=64) / local range (L≤100).** Cannot probe the long-range
  Berry regime that Rung 1 needed 40k zeros to see. A large long-range
  band-sheaf remains untested (needs a cluster; the exact-eig requirement makes
  it the §5.3 slow wall).
- The residual hypothesis (prime phases → GUE-matched rigidity) is a genuine,
  separable question for a future run with matched-distribution frequency
  controls.

## Program status
§7.1: **Rung 1 PASS (Berry, validation)**, **Rung 2 negative for sheaf
arithmetic (both channels, local scale)**. Gate B (a long-range sheaf observable
separating zeta from GUE under scrambling) is NOT met at the tested scale;
whether it holds at long range on a cluster is open. The defensible paper
(Gate C, numerical-methods/audit framing) is unaffected and arguably
strengthened: another apparent cross-domain signal (density z=−34) correctly
attributed to artifact by the preregistered controls.
