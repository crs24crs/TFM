# Decisions log — TFM

A short record of choices that later work must respect. Newest entries at the bottom of each section.
Format: **ID · date · decision.** Why · consequences.
Claude: read this before changing numerics. Propose new entries rather than deviating silently.

## Scope

**S-001 · 2026-11-27 · 1D azimuthal only.** The simulated coordinate is $y$, periodic (closed loop around the channel). 1D3V. No 2D extension planned.

**S-002 · 2026-11-27 · Collisionless, idealised scenario.** All electron transport is instability-driven (ECDI). No neutrals, ionisation or walls.

**S-003 · 2026-11-27 · Fields and coordinates follow Bello et al. (2024):** $\mathbf B_0 \parallel \mathbf 1_x$, $\mathbf E_0 \parallel \mathbf 1_z$, drift along $\mathbf 1_y$. Electrons feel $\mathbf E_0 + E_1\mathbf 1_y$; ions feel only $E_1\mathbf 1_y$.

**S-004 · 2026-11-27 · Develop incrementally** along the roadmap in `scope.md` (P1 Boris → P2 baseline + validation → P3 conservation study → P4 alternative algorithms → P5 subsonic/supersonic). Each phase gets tests before the next one starts.

**S-005 · 2026-11-27 · Terminology:** "oscillations" or "instability-driven/anomalous transport", not "turbulence".

## Numerics: settled (from the P0 prototype)

**D-001 · 2026-11-27 · Stack: Python 3 + NumPy/SciPy, matplotlib.**

**D-002 · 2026-11-27 · SI units. Temperatures are stored in J internally and reported in eV.**

**D-003 · 2026-11-27 · Periodic grid.** The P0 prototype uses `nx` nodes, with node `nx-1` duplicating node 0; density on the last node is folded onto node 0.

**D-004 · 2026-11-27 · P0 stores positions in cell units ξ = y/Δy, with periodic wrap.**

**D-005 · 2026-11-27 · Charge deposition: CIC (linear) to nodes.**

**D-006 · 2026-11-27 · P0 Poisson: 2nd-order FD, direct sparse solve, gauge φ = 0 at node `nx-1`.** Verified against analytic periodic sources (2nd-order error). Requires discrete **zero net charge**, which holds while both species have the same macroparticle count and weight.

**D-007 · 2026-11-27 · P0 time integration: explicit leapfrog.** Boris replaces it in P1.

**D-008 · 2026-11-27 · P0 interpolation variants under comparison:** `move_particlesMC` (E at nodes, CIC: momentum-conserving), `move_particlesEC` (E at cell centres, NGP: energy-conserving), `move_particlesMC2` (experimental). These are seeds for the algorithm comparison in P4.

**D-009 · 2026-11-27 · Repository at `C:\Users\crs24\GitHub\TFM\TFM`, not in OneDrive.** Papers and outputs are not committed.

## Assumed (not confirmed by Carlos yet; confirm or change)

**A-1 · Validation target = Bello §III fully periodic case, linear phase.** Compare unstable modes, growth rates and frequencies with the dispersion relation (their Eq. 4) and with the paper's values. The §IV injection cases are out of scope unless decided otherwise.

**A-2 · Performance: numba `@njit` kernels from P1 onwards, each with a slow readable reference version used in tests.** The 1D Bello case is ~40k particles × 6×10⁵ steps, and the P3 parameter sweeps multiply that, so pure Python loops are too slow.

**A-3 · Code, comments and docs in English.** The language of the report and defense is still open (O-6).

## Open questions

**O-1 · Leapfrog/Boris initialisation:** velocities must start at $t^{-1/2}$, and kinetic energy should be time-centred before judging energy conservation. Decide this in P1.

**O-2 · Reproducibility:** use `np.random.default_rng(seed)` and store the seed in run metadata.

**O-3 · Poisson solver for the baseline:** keep the FD sparse solve, or switch to FFT with zero-mean potential as PICASO does. Either can be the baseline; the other becomes a P4 variant.

**O-4 · Validation tolerance:** what agreement in γ and ω_r counts as "validated"?

**O-5 · Supersonic case (P5):** which parameter is varied to reach $M_e>1$ ($E_0$, $B_0$ or $T_{e0}$)? Keep the other dimensionless numbers fixed?

**O-6 · Report/defense language** (English or Spanish).
