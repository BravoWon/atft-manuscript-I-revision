# ATFT Manuscript I — revision + §7.1 experiment arc (intermediate)

**Status: work-in-progress checkpoint (2026-07-13/14).** Honest, incomplete,
and preregistered throughout. This directory captures the referee-driven
revision of Manuscript I plus the §7.1 long-range experiment, with every
apparent signal run through its attribution controls.

## The arc, in one screen

1. **Referee pass** (`referee/ATFT_Manuscript_I_REFEREE_REPORT.md`): 5-dimension
   multi-agent adversarial review of Manuscript I v0.1 → **32 verified findings**
   (10 major). The five headline theorems verified at machine precision; the
   failures were in the *record* (n=3 GUE null, single-threshold counts, missing
   falsification criteria, novelty positioning).

2. **Revision** (`REVISION_v0_2.md`): 18 keyed edits resolving all 32 findings,
   including the new **Corollary 3.7** (per-prime normalization breaks cross-σ
   isospectrality while preserving reality + the functional-equation symmetry),
   a §9 falsification section (F1/F2/F3), and the quasi-Hermitian positioning.

3. **Powered null** (§5.3; `PREREGISTRATION_POWERED_NULL.md` + AMENDMENTS 1–4):
   replacing the referee-killed n=3 with a certified GUE ensemble. A long solver
   saga is on the record (shift-invert failed 3 ways; spectral-flip is the
   certified method; GPU/inertia exhausted). **Preliminary result:** zeta
   near-kernel = **58** (certified) sits **below the entire GUE band** — the
   opposite of the retracted "zeta is special" premium. **KNOWN ISSUE:** the
   k=100 window **censors most GUE draws** (their near-kernel exceeds 100); the
   band's upper values are floor-estimates and the fleet needs **k ≥ 150** for a
   clean quantitative comparison. Direction is safe (zeta ≪ GUE); the exact band
   is pending.

4. **§7.1 long-range experiment** (`PREREGISTRATION_LONGRANGE.md`):
   - **Rung 1 — PASS** (`RUNG1_RESULTS.md`): the pipeline reproduces **Berry's
     number-variance saturation** on 40k Odlyzko zeros — zeta tracks GUE at small
     L (Montgomery), saturates below all GUE draws at large L (arithmetic
     rigidity). Positive control validated; the arithmetic is real and lives in
     the zeros.
   - **Rung 2 — negative for sheaf arithmetic** (`RUNG2_FINAL_VERDICT.md`).
     Density channel: zeta separates hugely (z = −34) but **geometric**
     (survives prime-scrambling). Fluctuation channel (exact dense eig): zeta ≈
     GUE (z ≈ 0), no separation. **The sheaf adds no attributable arithmetic
     beyond geometry** (H_sheaf outcome 2). The mandatory scrambling controls
     correctly demoted a z=−34 signal to artifact — the honesty rail working.
   - **GPU instrument** (`RUNG2_GATE_RESULT.md`, `GPU_EIGENCOUNT_VERDICT.md`):
     stochastic-trace eigencounting is fast but has a *fundamental* bias on
     extreme-edge counts and cannot compute fluctuation statistics
     (mean-density ≠ eigenvalue positions). It IS the right tool for smooth
     bulk trace functionals. Domain characterized, not oversold.

## Honest known limits (do not merge as final)
- §5.3 GUE band is **censored** at k=100 (fix: k ≥ 150); fleet ~45% complete;
  Poisson positive control not yet run.
- Rung 2 is **local / small-sheaf** only; the long-range band-sheaf is untested
  (exact-eig wall, needs a cluster).
- One open residual hypothesis: real prime phases produce GUE-matched sheaf
  rigidity (needs a log-distributed-frequency control before any claim).

## Layout
- `*.md` — revision, preregistrations, amendments, per-experiment verdicts.
- `referee/` — the 32-finding referee report + the research charter/claim ledger.
- `scripts/` — the runnable experiment code (data blobs .npz / output/ gitignored;
  regenerable from these).
- `crypto_companion/` — the True-Positive companion paper structure (crypto
  diffusion corpus) + the reduced-round-LSH critique integration.

## Defensible position
Gate C (numerical-methods / audit framing) is intact and **strengthened**: two
more apparent cross-domain signals (the §5.3 premium direction and the Rung-2
z=−34) were correctly attributed to solver-artifact and geometry by the
preregistered controls. The exact theorems stand; the empirical claims are
scoped to exactly what the controls support.
