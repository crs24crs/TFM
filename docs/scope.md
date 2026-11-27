# Thesis scope and roadmap — TFM

**Title:** Kinetic modeling of plasma instabilities in a Hall thruster discharge
**Author:** Carlos Rodríguez Sánchez

## Motivation
- Hall effect thrusters (HET) are the dominant electric propulsion technology (especially since large constellations such as Starlink).
- Open problem: **anomalous electron cross-field transport**. Electrons from the cathode should be confined by the radial magnetic field and reach the anode only through rare collisions with neutrals, but the measured anode current is far larger than collisions explain.
- Proposed cause: plasma **oscillations**. MHz-range azimuthal oscillations driven by the **electron cyclotron drift instability (ECDI)** are considered the main contributors.
- Terminology: say "oscillations", "instability-driven transport" or "anomalous transport". **Avoid "turbulence"** (author's preference).

## Approach
- **Kinetic** model (PIC), not fluid: it resolves the velocity distribution function of each species. More accurate in principle, but computationally more expensive.
- **Idealised, collisionless** scenario: the only transport is instability-driven.
- **Geometry: 1D azimuthal only.** Coordinate $y$ is a closed periodic loop around the thruster channel. Velocities are 3D (1D3V). Applied fields follow the Bello et al. convention: $\mathbf B_0 = B_0\mathbf 1_x$ (radial), $\mathbf E_0 = E_0\mathbf 1_z$ (axial), drift $\mathbf E_0\times\mathbf B_0$ along $y$ (azimuthal).

## Reference / validation
Bello-Benítez, Marín-Cebrián & Ahedo, *Effect of injection conditions on the non-linear behavior of the ECDI and related turbulent transport* (2024), UC3M, code PICASO (2D z–y, Boris pusher, FFT Poisson with zero-mean potential, equal constant weights, collisionless).
Reference case (Table I): $m_i = 1$ u, $E_0 = 10^4$ V/m, $B_0 = 200$ G, $n_0 = 10^{17}$ m⁻³, $u_{zi0} = 2.5$ km/s, $T_{e0} = 6$ eV, $u_{ye0} = 500$ km/s, $L_y = 5.359$ mm, $N_y = 100$, $N_{ppc} = 200$, $\Delta t = 5\times10^{-12}$ s, $N_t = 6\times10^5$.
Linear theory targets (their §II, $L_y$ as above): fastest mode $n = 13$ ($\gamma/2\pi = 34.7$ MHz, $k_y\ell_{e0} = 2.167$, $\omega_r = 46.6$ MHz); $n = 7$ close behind ($\gamma/2\pi = 32.6$ MHz).
Electrons feel $\mathbf E_0 + \mathbf E_1$, ions only $\mathbf E_1$ (no ion acceleration by $E_0$).

**Caveat:** the paper is 2D. Our 1D code can be validated on the **linear phase** (unstable modes, growth rates, frequencies against the dispersion relation and the paper's values). Long-term behaviour may differ: the paper notes that 1D-azimuthal runs without particle refreshing tend to show unbounded growth and heating, while their 2D periodic runs saturated.

## Roadmap (start simple, build slowly)
| Phase | Content | Done when |
|---|---|---|
| P0 ✅ | 1D electrostatic periodic PIC prototype (`prototypes/conservation_test.py`), momentum/energy diagnostics | exists |
| P1 | **Boris pusher** (1D3V) with $B_0\mathbf 1_x$, $E_0\mathbf 1_z$ on electrons | unit tests pass: gyration ($\omega_{ce}$, $\rho_e$), $|v|$ conserved in pure B, E×B drift $= E_0/B_0$ |
| P2 | **Baseline**: 1D-azimuthal periodic ECDI with Bello parameters + linear dispersion-relation solver | growth rates/frequencies of dominant modes match theory and the paper within an agreed tolerance |
| P3 | Conservation study: momentum & energy vs $N_{ppc}$, $\Delta y$, $\Delta t$ | parameter-sweep plots + conclusions |
| P4 | Alternative PIC algorithms from the literature (pushers, deposition/interpolation pairs, field solvers): do they predict the same behaviour? | comparison against the baseline |
| P5 | **Subsonic vs supersonic** electron drift, $M_e = u_{ye0}/c_{e0} < 1$ vs $> 1$ (Bello case: $M_e \approx 0.49$) | characterisation of both regimes |
| — | Report and defense | |
