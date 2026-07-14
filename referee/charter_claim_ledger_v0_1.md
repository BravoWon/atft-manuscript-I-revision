# ATFT Publishable-Paper Reconstruction
## Research Charter and Claim Ledger v0.1

**Date:** 12 July 2026  
**Working principle:** explicit statement → numerical test → honest scope wall.

## 1. Publication target

### Working title
**Convergence-Audited Topological Spectral Instruments: Sheaf Laplacians, Near-Kernel Pathologies, and Critical-Phenomena Benchmarks**

### Defensible central claim
A sheaf-enriched spectral pipeline can be defined rigorously and tested reproducibly, but its observables must be residual-certified, confound-controlled, and distinguished from ordinary persistent-homology statistics. The current Ti/JTopo corpus already contains a valuable negative result: a fixed-dimension Lanczos procedure produced a false arithmetic premium by failing to resolve a dense near-kernel.

### Explicit non-claims
- No proof of the Riemann Hypothesis.
- No universal phase-transition detector has yet been validated.
- No unique zeta-versus-GUE arithmetic separation has yet survived matched-edge, matched-tolerance controls.
- The current SU(2) benchmark is not yet a sheaf-Laplacian validation.
- The random 3-SAT v6 experiment remains a proposed protocol.
- The Prime Scalar Field interpretation remains exploratory until null-model testing is completed.

## 2. Claim ledger

| ID | Claim | Status | Reason / required action |
|---|---|---|---|
| M1 | For any finite coboundary matrix \(\delta(\sigma)\), \(L(\sigma)=\delta(\sigma)^*\delta(\sigma)\) is self-adjoint and positive semidefinite. | **Proved** | Direct adjoint and quadratic-form calculation. Holds for every \(\sigma\), not only \(1/2\). |
| M2 | \(\ker L=\ker\delta\), hence the degree-zero kernel represents globally compatible sections. | **Proved** | \(\langle x,Lx\rangle=\|\delta x\|^2\). |
| M3 | The prime generator \(B_p(\sigma)=\log p[p^{-\sigma}\rho(p)+p^{-(1-\sigma)}\rho(p)^T]\) is Hermitian exactly at \(\sigma=1/2\), subject to real \(\sigma\) and \(\rho(p)\neq\rho(p)^T\). | **Proved with conditions** | The skew-Hermitian part factors by \(p^{-\sigma}-p^{-(1-\sigma)}\). |
| M4 | The sheaf Laplacian itself is self-adjoint only at \(\sigma=1/2\). | **False as written** | \(L=\delta^*\delta\) is self-adjoint for all parameters. The critical-line structural statement concerns the generator/transport, not \(L\)'s self-adjointness. |
| Z1 | The published \(21.5\%\), \(16\sigma\), and \(670\times\) zeta premiums are genuine. | **Retracted** | The repository convergence audit identifies fixed-70-vector Lanczos failure on a dense near-kernel. |
| Z2 | A converged local-Rips near-kernel separates zeta zeros from GUE. | **Not supported** | At matched edge count and solver tolerance, zeta lies inside the observed GUE range. |
| Z3 | The current local observable detects something real. | **Supported narrowly** | It separates level-repulsive spectra from Poisson-like spectra; that is not uniquely arithmetic. |
| Z4 | Long-range rigidity may contain a prime-specific signal. | **Open hypothesis** | Test number variance, spectral form factor, long-range edge sheaves, and prime-frequency scrambling under matched geometry. |
| S1 | The SU(2) experiment implements a sheaf Laplacian. | **False for current script** | The published script computes ordinary \(H_0\) persistence/MST merge distances on a Euclidean point cloud; no sheaf restriction maps or sheaf spectrum are used. |
| S2 | The feature \(q_{\mu\nu}=\frac12\operatorname{Im}\operatorname{Tr}P_{\mu\nu}\) captures SU(2) topological charge. | **False** | Every SU(2) matrix has real trace, so this quantity is identically zero up to floating-point error. |
| S3 | The reported discontinuity at \(\beta=2.30\) validates deconfinement detection. | **Unvalidated** | The abrupt plaquette discontinuity and reduced thermalization/configuration counts require an independent lattice-code audit and conventional-observable cross-checks. |
| S4 | Persistent topology can detect SU(2) deconfinement in principle. | **Established precedent** | Prior peer-reviewed/arXiv work uses gauge-invariant filtrations and finite-size scaling. Novelty must be sheaf enrichment or a new validated observable. |
| C1 | The 3-SAT problem-graph approaches detect the satisfiability transition. | **Failed** | They measure monotone instance structure rather than the changing solution space. |
| C2 | The proposed solution-overlap point cloud may detect clustering/shattering. | **Open experiment** | Requires independent instances, solver-bias controls, finite-size scaling, and separation of SAT/UNSAT censoring from topology. |
| P1 | Prime-gap wave embeddings produce visual nodal structure. | **Descriptive result** | True by construction for the selected mapping; not yet evidence of a prime-specific field. |
| P2 | The period near \(2.34\) is intrinsic and prime-specific. | **Unvalidated** | Requires a precisely defined statistic, uncertainty, multiple-testing correction, and matched null sequences. |
| P3 | Spherical nodal plots establish natural three-dimensional information. | **Interpretive only** | Any scalar function mapped to a sphere admits a spherical-harmonic decomposition. Prime specificity must be demonstrated coefficient-wise against nulls. |

## 3. Core derivations

### Proposition 1 — positivity and self-adjointness

Let \(\delta_\theta:C^0\to C^1\) be any finite-dimensional coboundary operator depending on a parameter \(\theta\), and define
\[
L_\theta=\delta_\theta^*\delta_\theta.
\]
Then
\[
L_\theta^*=(\delta_\theta^*\delta_\theta)^*
=\delta_\theta^*\delta_\theta=L_\theta,
\]
and for every \(x\),
\[
\langle x,L_\theta x\rangle
=\langle \delta_\theta x,\delta_\theta x\rangle
=\|\delta_\theta x\|^2\ge 0.
\]
Thus \(L_\theta\) is self-adjoint and positive semidefinite for every \(\theta\).

### Proposition 2 — kernel/global compatibility

\[
L_\theta x=0
\quad\Longleftrightarrow\quad
\langle x,L_\theta x\rangle=0
\quad\Longleftrightarrow\quad
\|\delta_\theta x\|^2=0
\quad\Longleftrightarrow\quad
\delta_\theta x=0.
\]
Therefore \(\ker L_\theta=\ker\delta_\theta\). In degree zero this is the space of globally compatible sections.

### Proposition 3 — critical-line Hermiticity of the generator

For real \(\sigma\), write
\[
B_p(\sigma)
=\log p\left[p^{-\sigma}\rho_p+p^{-(1-\sigma)}\rho_p^T\right].
\]
Assuming \(\rho_p\) is real,
\[
B_p(\sigma)^*
=\log p\left[p^{-\sigma}\rho_p^T+p^{-(1-\sigma)}\rho_p\right],
\]
so
\[
B_p(\sigma)-B_p(\sigma)^*
=\log p\left(p^{-\sigma}-p^{-(1-\sigma)}\right)
(\rho_p-\rho_p^T).
\]
For a non-symmetric truncated multiplication representation, Hermiticity is equivalent to
\[
p^{-\sigma}=p^{-(1-\sigma)},
\]
hence \(\sigma=1/2\). This establishes a symmetry lock in the finite generator. It does not establish a spectral realization of all nontrivial zeta zeros.

### Proposition 4 — failure of the proposed SU(2) odd feature

Every \(U\in SU(2)\) can be written
\[
U=a_0 I+i\sum_{j=1}^{3}a_j\sigma_j,
\qquad a_0,a_j\in\mathbb R,\qquad \sum_{j=0}^{3}a_j^2=1.
\]
Since each Pauli matrix is traceless,
\[
\operatorname{Tr}U=2a_0\in\mathbb R.
\]
A plaquette product \(P_{\mu\nu}\) is again in \(SU(2)\), so
\[
\operatorname{Im}\operatorname{Tr}P_{\mu\nu}=0.
\]
Therefore the implemented quantity called \(q_{\mu\nu}\) cannot encode topological-charge sign. A valid lattice topological density requires an oriented \(\epsilon_{\mu\nu\rho\sigma}\)-weighted construction from field-strength/clover terms (with appropriate smoothing/renormalization), or another independently validated gauge-invariant definition.

## 4. Required experimental rebuild

### A. Numerical linear algebra
1. Require residual certificates \(\|Lx-\lambda x\|/\|x\|\) for every reported bottom eigenpair.
2. Compare at least two independent solver families.
3. Report kernel counts across explicit tolerances and stability plateaus.
4. Pre-register edge count, solver tolerance, Krylov dimension, null ensembles, and stopping rules.
5. Separate exact kernel, soft near-kernel, spectral gap, and normalized spectral density.

### B. Zeta/GUE experiment
1. Reproduce the corrected matched-edge local result.
2. Replace local-only Rips geometry with a long-range observable.
3. Test number variance \(\Sigma^2(L)\) and spectral form factor \(K(\tau)\).
4. Construct a long-range sheaf analogue using controlled \(\Delta\gamma\) bands.
5. Run prime-frequency scrambling, prime-label permutation, phase randomization, GUE, Poisson, and evenly spaced controls with identical geometry.
6. Estimate the ensemble distribution from many independent GUE draws; avoid a one-zeta-versus-few-controls pseudo-replication design.
7. State the scope wall: detection of a finite-sample arithmetic correction would not imply RH.

### C. SU(2) benchmark
1. Replace the current generator with a validated lattice implementation or public configurations.
2. Verify thermalization, autocorrelation times, plaquette curves, Polyakov susceptibility, and finite-size dependence.
3. Use a genuinely gauge-invariant feature/filtration.
4. Compare ordinary persistence against the proposed sheaf-enriched observable.
5. Use multiple spatial volumes and extract a pseudocritical coupling with uncertainty.
6. Benchmark directly against prior persistent-homology SU(2) work.

### D. 3-SAT benchmark
1. Sample solution/near-solution overlap clouds, not clause graphs.
2. Control WalkSAT sampling bias using multiple solvers and seeded restarts.
3. Analyze several \(n\), not only \(n=200\).
4. Separate clustering, condensation, and satisfiability thresholds.
5. Pre-register observables and avoid choosing the successful statistic after seeing the transition.

### E. Prime Scalar Field companion study
1. Freeze the exact map, amplitude, phase, detrending, and period-search procedure.
2. Compare to Cramér-type, renewal, shuffled-gap, residue-class-preserving, and phase-randomized nulls.
3. Quantify spherical-harmonic power \(C_\ell=\sum_m|a_{\ell m}|^2\).
4. Test recurrence with out-of-sample scale prediction.
5. Replace “three-dimensional information” with a precise information-theoretic or reconstruction statement.

## 5. Manuscript architecture

1. **Introduction and scope wall**
2. **Cellular sheaves and the finite operator**
3. **Exact propositions and corrected critical-line statement**
4. **Near-kernel numerical pathology**
5. **Convergence audit and residual certification**
6. **Local zeta/GUE null result**
7. **Long-range arithmetic-observable program**
8. **Independent critical-phenomena benchmark**
9. **Limitations and falsification criteria**
10. **Reproducibility appendix**

## 6. Publication decision gate

The flagship empirical paper proceeds only after at least one of these gates is met:

- **Gate A:** A rebuilt, independently checked SU(2) sheaf observable detects the transition with finite-size scaling and outperforms or adds information beyond ordinary persistence.
- **Gate B:** A long-range zeta sheaf observable separates zeta from GUE under matched geometry, many-draw controls, and prime-specific scrambling.
- **Gate C:** The paper is framed as a numerical-methods/audit contribution centered on dense near-kernel eigensolver failure, with zeta and sheaf Laplacians as the case study.

Gate C is already the closest to a defensible submission. Gates A and B would support a broader ATFT claim.

## 7. Primary literature map

- Hansen & Ghrist, *Toward a Spectral Theory of Cellular Sheaves*, arXiv:1808.01513.
- Wei & Wei, *Persistent Sheaf Laplacians*, arXiv:2112.10906.
- Hayes et al., *Persistent Sheaf Laplacian Analysis of Protein Flexibility*, arXiv:2502.08772.
- Sale, Lucini & Giansiracusa, *Probing Center Vortices and Deconfinement in SU(2) Lattice Gauge Theory with Persistent Homology*, arXiv:2207.13392.
- Spitz, Urban & Pawlowski, *Confinement in Non-Abelian Lattice Gauge Theory via Persistent Homology*, arXiv:2208.03955.
- Das & Biswas, *Critical Scaling through Gini Index*, arXiv:2211.01281.
- Das & Biswas, *Universal Critical Phase Diagram Using Gini Index*, arXiv:2409.01453.
- Lugar, Milinovich & Quesada-Herrera, *On the Number Variance of Zeta Zeros and a Conjecture of Berry*, arXiv:2211.14918.
