# Critique Integration — the "influence manifold, not identity manifold" boundary

**Date:** 2026-07-13. Source: an external adversarial research verdict on a
proposed *reduced-round-SHA-256-as-semantic/identity-LSH* system. This file
records how that verdict is absorbed into the crypto companion paper. The
verdict targets an **overclaiming** construction; the diffusion-margin auditor
is the disciplined object the verdict's own "salvageable core" endorses.

## 1. The three leaps — our corpus makes none

The verdict names three unsupported inferences. The auditor commits none:
1. **reduced diffusion ⇒ locality preservation** — we measure *structural
   completion* (all-pairs reachability round), never locality preservation.
2. **locality ⇒ semantic clustering** — never claimed; "semantic" is out of scope.
3. **state differences ⇒ recoverable plaintext-difference locations
   (inversion)** — the Rung-2 LAT/DDT is *per-component and forward*, explicitly
   NOT an inverse map, NOT a multi-round trail optimum (README honesty rail).

## 2. The Round-12 blindness — reproduced from our own data-free graph

The verdict's decisive spec fact: SHA-256 injects one message word W_t per round
for t=0..15, so after 12 completed rounds W_12..W_15 have never entered the
state — exact blindness to the block's tail. **Our auditor exhibits this exactly**
(N_SRC=440, a 55-byte single-block message; source bits live in words W0..W13):

| after N rounds | blind source bits | words | last blind byte |
|---|---|---|---|
| 12 | 56 | W12, W13 | 54 (message end) |
| 13 | 24 | W13 | 54 |
| 14 | 0 | — | full injection complete |

**This mechanistically explains our λ₂ connectivity onset = round 14:** round 14
is where the last source word finishes injecting, so the transport graph first
becomes fully connected. The verdict's schedule analysis and our measured onset
are the same fact from two encodings. (New paper result — see ledger D10.)

Reproduce: `diffusion-margin-auditor` → `sha256.reach_curve(12)`, check
`mats[-1].any(axis=0)` for zero-influence source columns.

## 3. Round-19 — reframed precisely (verdict's fair hit)

"Round-19 topological saturation" is OUR measured quantity, not an established
theorem. Precise claim for the paper:
> Our data-free reachability graph completes at round 19 (every output bit
> depends on every input bit) and λ₂ saturates there; this **coincides with the
> empirically measured SAC max-|S−0.5| cliff** (Vaughn–Borowczak). It is a
> *structural* boundary matching an *independent statistical* measurement — not
> a universal diffusion boundary, not a security threshold, not a proof that
> connectivity implies statistical saturation.

We already measure structural completion (19) and statistical avalanche
(128/256 by ~32) as **separate** observables — honoring the verdict's core
distinction: **structural influence ≠ statistical influence ≠ semantic similarity.**
A graph can connect (Boolean) while influence stays uneven (statistical); the
paper states this explicitly and never elides the three.

## 4. Paper framing — adopt the verdict's phrase

The companion paper's object is an **influence manifold**, not a distinguishing
or identity manifold. The auditor computes *which* source bit can reach *which*
register by *which* round (reachability, onset, saturation, dependency cones) —
structural capacity, never statistical distinguishability or invertibility.

## 5. Explicit NON-GOALS / scope boundaries (new §, from the verdict)

The paper states plainly that the tapped/structural view is **not**:
- a locality-sensitive hash (LSH is defined by a probabilistic
  near-collision guarantee w.r.t. an input metric — nothing here establishes
  d_edit or d_semantic is monotone in d_Hamming(F_r(x),F_r(y)));
- a similarity fingerprint (the correct tools are **MinHash** for set
  resemblance, **SimHash / random-hyperplane** for cosine, **TLSH / ssdeep**
  for near-identical byte streams);
- an identity fingerprint (256-bit state vs 512-bit block ⇒ many-to-one;
  pre-injection words are invisible; cones overlap; carries cancel);
- a security primitive (a reduced-round tap is a deterministic **leakage
  channel**; keyed **HMAC** is the conventional separator). This reinforces our
  "necessary ≠ sufficient, not a security ranking" rail.

## 6. The verdict's discrimination experiment overlaps our experiment 2

The verdict proposes a labeled-pair test: D_r(x,y)=d_H(F_r(x),F_r(y))/256 vs
input distance, ROC-AUC near-vs-unrelated, per-byte sensitivity, MI(mutation,
state-diff), against MinHash/SimHash/TLSH baselines; prediction: blind spots +
positional artifacts in rounds 1–15, near-random later, **no universal round**.
This is the *statistical-influence* companion to our *structural* screen, and
`sha256-round-diffusion/` (experiment 2) already ran its core: the learned
marginal distinguisher **dies by round 6**, the mining selector shows **no lift
at any round** — consistent with the verdict's "no exploitable structure past
the reduced-round window." The paper cites this as the statistical arm that
corroborates the structural one, with the confound controls (canonicalization,
padding, position) the verdict correctly demands.

## 7. New/updated claim-ledger rows for the paper

| ID | Claim | Status | Basis |
|---|---|---|---|
| D10 | Injection-schedule blindness: after r<16 rounds, source words W_r..W_15 have zero structural influence; for the 55-byte model, 56 bits (W12–13) are blind at r=12, 0 at r=14 — which is exactly the λ₂ onset round. | **Verified** | `sha256.reach_curve`; reproduces the spec fact data-free. |
| D11 | The auditor measures structural influence only; structural completion (19) and statistical avalanche (~32) are reported as distinct observables; neither implies semantic similarity or invertibility. | **Scoped (honesty rail)** | round-diffusion exp. + this file §3. |
| N1..N4 | Explicit non-goals: not LSH, not a similarity/identity fingerprint, not a security primitive (§5). | **Non-claims** | LSH theory; MinHash/SimHash/TLSH; HMAC. |

## 8. Net effect

The verdict does not weaken the paper — it **hardens its scope wall and gives it
a new verified result (D10) plus its exact framing (influence manifold).** The
paper should cite the verdict's distinctions as the reason its honesty rails are
drawn where they are.
