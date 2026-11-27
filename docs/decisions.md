# Decisions log — TFM

Short record of choices that later work must respect. Newest at the bottom.
Format: **ID · date · decision** — why · consequences. Claude: read this before changing numerics; propose new entries rather than silently deviating.

## Settled (as of 2026-11-27, from `prototypes/conservation_test.py`)

**D-001 · 2026-11-27 · Stack: Python 3 + NumPy/SciPy, matplotlib for plots.**
`numba` is imported but not used yet (no `@njit`); adopting it is open (O-4).

**D-002 · 2026-11-27 · SI units; temperatures stored in joules internally, reported in eV.**
Avoids hidden normalisations. Plots and text must convert (`T/e`).

**D-003 · 2026-11-27 · 1D electrostatic, fully periodic domain, electrons and ions both kinetic.**
`nx` nodes, `nx-1` cells; node `nx-1` duplicates node 0. Density deposited on node `nx-1` is folded onto node 0.

**D-004 · 2026-11-27 · Particle positions stored in cell units ξ = x/Δx; periodic wrap `pos % (nx-1)`.**

**D-005 · 2026-11-27 · Charge deposition: CIC (linear weighting) to nodes.**

**D-006 · 2026-11-27 · Poisson: 2nd-order central finite differences, direct sparse solve (`scipy.sparse.linalg.spsolve`).**
Gauge fixed by setting φ = 0 at node `nx-1`. Verified against analytic periodic sin/cos sources (2nd-order error). Requires discrete **zero net charge**, which holds while both species have equal macroparticle number and weight — revisit if that changes (injection, ionisation, different weights).

**D-007 · 2026-11-27 · Time integration: explicit leapfrog (v then x).**

**D-008 · 2026-11-27 · Two field-interpolation variants are being compared:**
- `move_particlesMC`: E at nodes (central difference), CIC interpolation (momentum-conserving).
- `move_particlesEC`: E at cell centres, NGP-at-cell interpolation (energy-conserving).
- `move_particlesMC2`: cell-centred E with linear interpolation (experimental).
Current default in the loop: `move_particlesMC` with `E_nodes`.

**D-009 · 2026-11-27 · Reference test case:** xenon, $n_0=10^{17}$ m⁻³, $T_e=10$ eV, $T_i=1$ eV, $L=10$ mm, 200 cells, $\Delta t=10^{-12}$ s, 100 ppc.
Gives Δx/λ_D ≈ 0.67, ω_pe Δt ≈ 0.018.

**D-010 · 2026-11-27 · Repository lives in `C:\Users\crs24\GitHub\TFM\TFM`, not in OneDrive.**
OneDrive syncing a `.git` folder causes corruption/conflicts. Papers and large outputs are not committed (`.gitignore`).

## Open questions (decide, then move up as D-entries)

**O-1 · Leapfrog initialisation.** Velocities are not pushed back Δt/2 at t=0, and kinetic energy is evaluated with $v^{n-1/2}$ against field energy at $t^n$. Decide: add the initial half-step and/or time-centre K as $\tfrac12(K^{n-1/2}+K^{n+1/2})$ before judging energy conservation.

**O-2 · Reproducibility.** No RNG seed is set. Decide: `np.random.default_rng(seed)` with seed stored in run metadata.

**O-3 · Coordinate names.** Hall thruster convention (z axial, θ or y azimuthal, r radial) vs current generic x. Decide before the first E×B / azimuthal run.

**O-4 · Performance.** Particle loops are pure Python. Decide: numba `@njit` kernels vs NumPy vectorisation; keep a slow reference implementation for tests either way.

**O-5 · Next physics step.** Toward the thesis topic (e.g. adding $B_0$ and an E×B drift for azimuthal instabilities). To confirm with supervisor.
