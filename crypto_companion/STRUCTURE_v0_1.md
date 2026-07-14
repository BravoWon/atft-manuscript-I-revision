# Crypto Companion Paper — Structure & Claim Ledger v0.1

**Date:** 2026-07-13
**Working principle (shared with ATFT):** explicit statement → numerical test → honest scope wall.
**Relationship:** the rigorous **True Positive** to ATFT Manuscript I's rigorous **True Negative**.
**Guardrail (load-bearing, stated first):** same *observable family* and same *audit discipline* as ATFT — **not the same engine.** See §11.

---

## 0. The one-sentence thesis

> A dependency-graph Laplacian built **purely from a primitive's round function and gate truth tables** — never from measured differentials — recovers the exact round at which cryptographic diffusion structurally completes, reproducibly, KAT-anchored, and corroborated in silicon, across both ARX and SPN designs; it is the positive-detection counterpart to the same spectral-observable discipline that returns a *certified null* on zeta-vs-GUE local geometry.

The asymmetry that makes this a genuine positive control: **the answers are exactly checkable.** Round 19 is not a conjecture — it is bit-exactly verifiable against the primitive itself. Where zeta offers only ensembles and residual bounds, crypto offers ground truth.

---

## 1. Publication target

### Working title
**Structural Diffusion Margins from Wiring Alone: A Data-Free, Preregistered Spectral Audit of ARX and SPN Round Functions**

(Companion-explicit alt: *Convergence-Audited Topological Spectral Instruments II: Certified Positive Detection in Cryptographic Round Functions.*)

### Defensible central claim
The structural-diffusion boundary of an iterated cryptographic permutation/compression function — the round at which every output bit first depends on every input bit and the dependency graph's algebraic connectivity λ₂ saturates — is computable **data-free** from the wiring, is **architecture-dependent** in a way a single absolute-round margin hides, and **matches the independently measured avalanche boundary** where one exists. Five primitives instantiate the engine; two were **preregistered** before computation.

**Framing (the object, stated precisely — see `CRITIQUE_INTEGRATION.md`):** the auditor computes an **influence manifold**, not a distinguishing or identity manifold. It answers *which source bit can reach which register by which round* — structural *capacity*. It says nothing about statistical distinguishability, semantic similarity, or invertibility. The governing distinction, held throughout: **structural influence ≠ statistical influence ≠ semantic similarity.**

### Explicit non-claims (honesty rail — inherited from the crypto suite verbatim in spirit)
- **Not a security proof or ranking.** Structural diffusion is **necessary, not sufficient**; a larger margin/multiplier is **not** "more secure," a smaller one is not a break.
- **Not an attack, inversion, or mining edge.** Nothing here weakens any full-round primitive.
- **Not new differential/linear cryptanalysis.** The Rung-2 LAT/DDT screen is **per-component and exact**, not a multi-round trail optimum (ARX modular-add correlation and Matsui search are named, out-of-scope boundaries).
- **The completion round for SHA-256 reproduces known avalanche/SAC results** (Vaughn–Borowczak and predecessors). Novelty is the **data-free method**, the **cross-primitive generalization**, the **architecture-dependence of the multiplier**, and the **preregistered structural findings** — not the fact that SHA-256 diffuses.
- **The positive result validates the observable FAMILY and the discipline, NOT the specific sheaf-Laplacian-on-Rips pipeline** used for zeta. (Guardrail; §11.)
- **Not a locality-sensitive hash, similarity fingerprint, identity fingerprint, or security primitive.** Nothing here establishes that edit- or semantic-distance is monotone in Hamming distance of a tapped state; the correct tools for those tasks are MinHash (set resemblance), SimHash / random-hyperplane (cosine), TLSH / ssdeep (near-identical bytes), and keyed HMAC (identity separation). A reduced-round tap is a *deterministic leakage channel*, not a secure shadow. (Non-goals; `CRITIQUE_INTEGRATION.md` §5.)
- **"Round 19" is our measured structural-completion round** (data-free reachability complete + λ₂ saturated), coinciding with the empirical SAC cliff — **not** an established theorem, a universal boundary, or a claim that connectivity implies statistical saturation. Structural completion (19) and statistical avalanche (~32) are reported as *separate* observables.

---

## 2. Claim ledger

| ID | Claim | Status | Basis / provenance |
|---|---|---|---|
| **D1** | A data-free dependency graph (support propagation through the round ops) yields the structural completion round; for SHA-256 it equals 19, matching the empirical SAC cliff. | **Verified** | Regression test + empirical SAC cross-check (sheaf exp.); drift 1.0 on 2026-07-12. |
| **D2** | λ₂ (Fiedler value) gives a distinct **onset** (graph connects) and **saturation** (λ₂ = complete-bipartite max) per round; onset precedes completion (SHA-256: onset 14, completion 19). | **Verified** | `margin.py`; onset/saturation detectors. |
| **D3** | SHA-256 completes **19/64**, multiplier 3.37×. | **Verified** | KAT vs hashlib + regression pin. |
| **D4** | SHA-512 completes **19/80** — the *same absolute round* as SHA-256 — multiplier 4.21×; **the multiplier is not a SHA-family constant** (extra rounds are pure margin). | **Verified, preregistered** | `PREREGISTRATION_SHA512.md`; point-estimate 20 **falsified** (actual 19), reported straight. |
| **D5** | BLAKE2s **2/10** (5.0×); ASCON-p[12] **4/12** (3.0×). | **Verified** | KAT vs hashlib.blake2s / ascon pkg. |
| **D6** | Keccak-f[1600] completes **3/24** (8.0×), onset 1 (no dead zone); **round-19 is an ARX-message-schedule artifact** — remove the delayed schedule and the boundary collapses to single digits. | **Verified, preregistered (two hypotheses)** | `PREREGISTRATION_KECCAK.md`; both hypotheses passed; in-degree≤33 counting floor. |
| **D7** | The structural stragglers are real in silicon: the last pairs to connect show P(flip)=0 at completion−1 and >0 at completion, over thousands of real primitive evaluations. | **Verified (artifact-backed)** | `outputs/straggler_sha512.json` (12/12, r18/r19) + `outputs/straggler_keccak.json` (12/12, r2/r3), 4000 runs/pair, persisted 2026-07-13 via `persist_stragglers.py`. |
| **D8** | λ₂ saturation coincides with reachability completion in all measured primitives. | **Observed regularity (5/5)** | Open whether universal; candidate for a preregistered law. |
| **D9** | A cross-primitive diffusion-multiplier law (floor, or scaling with state/schedule). | **Open** | N=5; needs ~8+ primitives, preregistered. |
| **R2** | Per-component LAT (linear) and DDT (differential) are exactly brute-forceable from the same gate tables (ASCON S-box LAT 0.5 / DDT 0.25 recovered = published constants). | **Verified, scoped** | Second screen touching sufficiency; explicitly **not** a multi-round optimum. |
| **C1** | The engine and the bespoke sheaf experiment agree (SHA-256 → 19 both ways). | **Verified** | Cross-implementation regression anchor. |
| **D10** | Injection-schedule blindness: after r<16 rounds, un-injected message words have **zero** structural influence — 56 source bits (W12–13) blind at r=12, 0 at r=14; r=14 = the λ₂ onset. Reproduces the SHA-256 spec fact data-free and explains the onset round mechanistically. | **Verified (2026-07-13)** | `sha256.reach_curve`; `CRITIQUE_INTEGRATION.md` §2. |
| **D11** | Structural influence only: completion (19) and statistical avalanche (~32) are distinct measured observables; neither implies semantic similarity or invertibility. | **Scoped (honesty rail)** | round-diffusion exp. + `CRITIQUE_INTEGRATION.md` §3. |

---

## 3. Section architecture

1. **Introduction and scope wall** — the necessary-condition frame; what "structural diffusion" is and is not.
2. **The op-algebra and the data-free dependency graph** — rot/shr/xor/add(carry) + gate(truth-table → D,P); columnar gates; source re-injection; ARX vs SPN unified as gates-at-different-sizes.
3. **Spectral observables** — reachability completion; λ₂ onset/saturation; Gini; why λ₂ adds information beyond all-pairs reachability (the onset≠completion gap).
4. **Primitives in the algebra** — ARX: SHA-256, SHA-512, BLAKE2s; SPN: ASCON-p[12], Keccak-f[1600]. One file each: round function + round-tapped reference + KAT.
5. **Certification** — the acceptance gate: KAT bit-exactness vs reference implementations, symbolic ⊇ empirical superset checks, silicon straggler corroboration. *No measurement counts until the KAT passes.*
6. **Results — the margin table** — completion, onset, saturation, margin, multiplier for all five; the SHA-256↔SHA-512 round-19 invariance; the Keccak collapse to 3.
7. **Preregistration outcomes** — SHA-512 and Keccak scored straight, including the falsified SHA-512 point estimate and the disclosed interval-authoring flaw (P2/P3 endpoint inconsistency, verifier-caught).
8. **Second screen: per-component LAT/DDT (Rung 2)** — one gate engine, both analyses; named boundaries (ARX-add/Wallén, Matsui).
9. **Reproducibility and acceptance criteria** — mirror ATFT §8: KAT anchors, two-implementation agreement (op-algebra vs round-tapped reference vs library), seeds, bit-stable JSON, additive provenance + content hashes.
10. **Limitations and falsification criteria** — mirror ATFT §9: F-triggers (below).
11. **Companion relationship: True Positive / True Negative** — the guardrail section (below).
12. **Discussion and conclusion** — the instrument detects verifiable structure where it exists; the diffusion boundary is set by architecture (schedule delay + pipeline depth for ARX; θ/π mixing for SPN), not by round budget.

**Appendices:** A. the five primitives' exact parameters and derived constants. B. per-manuscript claim ledger. C. reproducibility record (KAT logs, integrity hashes, straggler tables).

---

## 4. Limitations & falsification criteria (§10 preview)

**Limitations.** (i) Necessary-condition only — says nothing about differential/linear/algebraic resistance (sufficiency). (ii) The dependency graph is a *support* abstraction: it tracks whether bit i can influence bit o, not the strength or cancellation of that influence (the capacity rung softens but does not remove this). (iii) N=5 primitives — the multiplier "law" (D9) is a hypothesis, not a result. (iv) SHA-256 completion reproduces known avalanche results; the data-free method is the contribution, not the number.

**Falsification triggers (preregisterable).**
- **CF1 (method validity).** If, for any primitive, the data-free structural completion round **disagrees** with a residual-/KAT-certified empirical avalanche boundary (where one is measurable), the support abstraction is unsound as a diffusion detector and every derived margin is void.
- **CF2 (architecture-dependence).** If a broadened corpus (≥8 primitives) shows the diffusion multiplier is in fact ~constant across architectures, D4/D6's "architecture-dependent, not a family constant" headline is falsified.
- **CF3 (companion claim).** If a critic demonstrates that all-pairs reachability completion in an iterated bijection is a foregone conclusion any method recovers trivially (so the "positive detection" carries no discriminative content), the True-Positive framing loses force — **defense:** the nontrivial, checkable content is the *round* of completion and its architecture-dependence, empirically corroborated in silicon (D7), not the mere fact of completion.

---

## 5. Companion relationship — the guardrail (§11 preview)

**What is genuinely shared (the valid pairing):**
- **Observable family:** algebraic connectivity λ₂, kernel/near-kernel dimension, saturation onset, Gini — spectral graph statistics on a Laplacian.
- **Audit discipline:** preregistration before computation; certification before any number is quotable (KAT bit-exactness here / residual certificates there); matched controls; named falsification triggers; additive, hash-anchored provenance; falsified predictions reported straight.

**What is different (why "same engine" is FALSE and must never be claimed):**

| | Crypto (this paper) | ATFT zeta (companion) |
|---|---|---|
| Graph | data-free **dependency graph** from wiring | **sheaf Laplacian**, K-dim arithmetic fibers, on empirical Rips geometry |
| Input | round function + truth tables (no data) | measured/unfolded zeta ordinates (a point cloud) |
| Certification | KAT bit-exactness + silicon straggler check | eigenpair residual < 1e-5, two solver families |
| Target | **deterministic algebraic structure** | **conjectured arithmetic structure** in a point cloud |
| Ground truth | **exactly checkable** | ensembles + bounds only |

**The claim this pairing licenses (and only this):** the spectral-observable methodology, held to one standard, **recovers exact verifiable invariants where algebraic structure exists** (round 19/64, 3/24, S-box voids) and **returns certified nulls where the sought structure is absent from the projection** (zeta local geometry). This answers the null-machine objection (ATFT RT-2) at the level of the **methodology class** — it is a positive control for *the discipline*, **explicitly not** for the specific zeta pipeline's implementation. A referee diffing `margin.py` against `base_sheaf_laplacian.py` will find two different programs; the paper says so first, in §11, before the referee can.

---

## 6. Publication decision gate

- **Gate P (standalone, recommended first):** the crypto paper stands alone as a data-free structural-diffusion auditor with a preregistered cross-primitive finding. Publishable at an applied-topology / methods venue, or a crypto venue (IACR ToSC-adjacent) **with** the honesty framing foregrounded — crypto reviewers will note the SHA-256 number is known, so the data-free method + generalization + preregistration must carry the novelty.
- **Gate J (joint):** a single methods paper with zeta-null and crypto-positive as two case studies under one discipline. Strongest answer to RT-2, but couples two review timelines and two very different reviewer pools.
- **Gate X (two cross-referenced companions):** ATFT Manuscript I (True Negative) + this (True Positive), each standalone, each citing the other's preprint. Cleanest reviewer fit; the companion claim lives in a Discussion paragraph on each side.

**Recommendation:** Gate X. Ship each to its native venue; let the cross-reference do the framing work without hostage-taking two review processes to one another.

**DECISION (2026-07-13): Gate X selected.** ATFT (True Negative) → applied-topology / numerical-methods venue; crypto (True Positive) → IACR ToSC-adjacent or applied-topology; each cites the other's preprint; the companion claim lives in one Discussion paragraph per side (drafted in §6.1). Timelines independent.

### 6.1 The two reciprocal cross-reference paragraphs (drop-in prose)

**In the crypto paper's Discussion (→ ATFT):**
> The observable family and audit discipline used here — spectral graph
> statistics (algebraic connectivity, kernel dimension, saturation) certified
> before quotation, predictions preregistered, controls matched — are shared
> with a companion study of a very different target [ATFT-I]. There, the same
> discipline applied to a sheaf Laplacian on unfolded Riemann-zeta ordinates
> returns a residual-certified *null*: local spectral geometry does not
> separate zeta from GUE. The two results are complementary controls on the
> methodology — it recovers exact, silicon-checkable invariants where
> deterministic algebraic structure exists (this paper), and reports certified
> absence where the sought structure is not present in the projection (the
> companion). We stress the pairing is at the level of discipline and
> observable family, not implementation: the two graphs are built by different
> programs from different inputs (wiring truth-tables here; an empirical point
> cloud there), and neither result validates the other's specific pipeline.

**In ATFT's Discussion (→ crypto, answering RT-2 directly):**
> A natural objection to a paper whose empirical core is a certified null is
> that the instrument may be constitutionally incapable of a positive result.
> A companion study [CRYPTO] applies the same spectral-observable discipline —
> algebraic connectivity and kernel structure of a Laplacian, preregistered
> and certified — to cryptographic round functions, where it recovers the exact
> structural-diffusion boundary of five primitives data-free from their wiring,
> bit-exactly corroborated against the primitives themselves. The methodology
> therefore detects genuine structure when present; the zeta null of §5.3 is a
> property of the target's local geometry, not an artifact of an instrument
> that can only output nulls. As here, the pairing is of discipline and
> observable family, not of implementation.

---

## 8. Related-work map (skeleton) — with an honest positioning guardrail

Four buckets; each needs a paragraph and the **honest boundary** noted so a
domain referee cannot say "they don't know the sharper tool."

1. **Diffusion metrics & the wide-trail strategy.** Complete/full-diffusion
   rounds, branch number (Daemen–Rijmen wide-trail), avalanche and the Strict
   Avalanche Criterion (Webster–Tavares), SHA-256 SAC (Vaughn–Borowczak).
   *Boundary:* SHA-256's completion round is a **known** avalanche result; our
   contribution is recovering it — and four other primitives' — **data-free**.
2. **Algebraic / propagation views of ciphers — THE GUARDRAIL BUCKET.** Our
   support propagation is adjacent to, but deliberately **weaker than**, the
   **division property / monomial-trail** machinery (Todo; Boura–Canteaut)
   used for integral distinguishers. *Boundary, stated plainly:* division
   property tracks algebraic-degree/monomial presence and yields *attacks*;
   our reachability tracks **bit-support only** and yields a **structural
   necessary-condition screen**. We are the coarser, primitive-agnostic,
   design-time instrument — **not** a competitor to integral cryptanalysis.
   Failing to say this invites a one-line desk-reject from a symmetric-crypto
   referee.
3. **Topological / sheaf-spectral methods.** Hansen–Ghrist (spectral theory of
   cellular sheaves), Wei–Wei (persistent sheaf Laplacians) — the shared
   observable-family anchor tying this paper to the ATFT companion.
4. **Reproducibility & preregistration in computational science.** The audit
   discipline itself (preregistration, certification, additive provenance) as
   a methods contribution, not just a crypto one.

---

## 9. Figure & table inventory

| # | Artifact | Status |
|---|---|---|
| Fig 1 | Normalized diffusion trajectories (λ₂/λ_max vs round/total budget), 5 primitives | **renders** (`run_audit.py`) |
| Fig 2 | Margin bars (completion within total rounds) | **renders** (`run_audit.py`) |
| Fig 3 | The round-19 story: SHA-256 vs SHA-512 same absolute completion despite 64 vs 80 budget; Keccak collapse to 3 (schedule-artifact visual) | **new — to build** |
| Fig 4 | Silicon straggler corroboration: P(flip) at completion−1 (=0) vs completion (>0), SHA-512 & Keccak | **new — data persisted** (`outputs/straggler_*.json`) |
| Table 1 | Five-primitive margin table (completion/onset/saturation/margin/multiplier) | data exists |
| Table 2 | Per-component LAT/DDT (Rung 2) | data exists |
| Table 3 | Preregistration scorecards (SHA-512, Keccak), falsifications included | data exists |

---

## 7. Status — what exists vs what a submission needs

**Exists (verified this session and prior):** the engine (`transport.py`, `margin.py`), all 5 primitives KAT-anchored, 2 preregistrations, silicon straggler corroboration persisted to `outputs/straggler_*.json`, cross-implementation regression, additive provenance with content hashes, 16 passing tests. Fresh-context `driftwave-verifier` scores (session records, not yet serialized to the corpus): base-camp reproduction **1.0**; SHA-512 extension **0.97**; Keccak extension **0.87 → 0.93** across two fix rounds. *Action item:* write a `VERIFICATION_LOG.md` to the corpus so these scores are on-disk, not session-only.

**A submission still needs:** (i) prose (all 12 sections — currently code + record files only); (ii) the D8/D9 multiplier-law question either preregistered-and-run at N≥8 or explicitly deferred; (iii) a related-work map (data-free diffusion: full-diffusion/complete-diffusion rounds, branch number; graph-spectral crypto; avalanche/SAC literature; sheaf Laplacians Hansen–Ghrist / Wei–Wei for the shared-family framing); (iv) figures (the normalized diffusion-trajectory plot and the margin bars already render from `run_audit.py`); (v) a `git init` on the corpus so preregistration timestamps are provable (flagged twice by verifiers).
