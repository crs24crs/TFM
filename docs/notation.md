# Notation — TFM: Kinetic modeling of plasma instabilities in a Hall thruster discharge

The single source of truth for symbols in the code, the report and the defense.
Rule: **one symbol = one meaning**. Follows Bello-Benítez et al. (2024) where possible, to ease validation.
To add or change a symbol, edit this file first and log the change in `decisions.md`.

Units: SI throughout. Temperatures are stored **in joules** in the code and reported **in eV** in text and plots.
Subscript `0` = initial equilibrium value. Subscript $s \in \{e, i\}$ = species.

## Geometry and coordinates (Hall thruster analogy)
| Direction | Symbol | Unit vector | Role |
|---|---|---|---|
| Radial | $x$ | $\mathbf 1_x$ | Direction of $\mathbf B_0$ (not resolved) |
| Azimuthal | $y$ | $\mathbf 1_y$ | **The simulated 1D periodic coordinate**; direction of $\mathbf E_0\times\mathbf B_0$ |
| Axial | $z$ | $\mathbf 1_z$ | Direction of $\mathbf E_0$ (not resolved) |

Phase space is 1D3V: position $y$, velocity $(v_x, v_y, v_z)$.
⚠️ The P0 prototype still names the coordinate `x`. Rename it to `y` when it is promoted to `src/`.

## Physical constants
| Symbol | Code | Meaning | Value |
|---|---|---|---|
| $e$ | `e` | Elementary charge | 1.60217663e-19 C |
| $m_e$ | `me` | Electron mass | 9.1093837e-31 kg |
| $m_i$ | `mi` | Ion mass | Bello case: 1 u; prototype: Xe (2.1801714e-25 kg) |
| $\varepsilon_0$ | `eps0` | Vacuum permittivity | 8.8541878188e-12 F/m |

## Applied fields and equilibrium
| Symbol | Code (planned) | Meaning |
|---|---|---|
| $B_0$ | `B0` | Applied magnetic field, along $\mathbf 1_x$ |
| $E_0$ | `E0` | Applied electric field, along $\mathbf 1_z$, felt by **electrons only** |
| $n_0$ | `n0` | Equilibrium density (prototype: `n`) |
| $T_{e0},\ T_{i0}$ | `Te0`, `Ti0` | Equilibrium temperatures (prototype: `Te`, `Ti`). Bello: cold ions |
| $u_{ye0} = E_0/B_0$ | `uye0` | Electron E×B drift velocity |
| $u_{zi0}$ | `uzi0` | Ion axial velocity (no dispersion) |

## Characteristic scales
| Symbol | Code | Definition |
|---|---|---|
| $c_{e0}$ | `ce0` | $\sqrt{T_{e0}/m_e}$, electron thermal velocity (Bello definition) |
| $\bar c_e$ | `c_bar_e` | $\sqrt{8T_{e0}/(\pi m_e)}$, mean electron speed (used only in the P0 CFL print) |
| $c_{s0}$ | `cs0` | $\sqrt{T_{e0}/m_i}$, ion sound speed |
| $\lambda_{D0}$ | `l_debye` | $\sqrt{\varepsilon_0T_{e0}/(n_0e^2)}$, Debye length |
| $\omega_{pe0},\ \omega_{pi0}$ | `omega_pe`, `omega_pi` | Electron/ion plasma frequencies |
| $\omega_{ce}$ | `omega_ce` | $eB_0/m_e$, electron cyclotron frequency |
| $\omega_{lh}$ | `omega_lh` | Lower-hybrid frequency |
| $\rho_{e0}$ | `rho_e` | $c_{e0}/\omega_{ce}$, electron Larmor radius |
| $\ell_{e0}$ | `ell_e` | $u_{ye0}/\omega_{ce}$, azimuthal-drift gyroradius |
| $M_e$ | `Me` | $u_{ye0}/c_{e0}$, electron drift Mach number: **subsonic** $M_e<1$, **supersonic** $M_e>1$ |

## Grid and time
| Symbol | Code | Meaning |
|---|---|---|
| $L_y$ | `Ly` | Azimuthal domain length (periodic) |
| $N_y$ | `Ny` | Number of **cells** (prototype uses `nx` = number of **nodes** = $N_y + 1$) |
| $\Delta y$ | `dy` | Cell size (prototype: `dx`) |
| $y_j$ | `y[j]` | Node position |
| $\Delta t,\ N_t$ | `dt`, `Nt` | Time step, number of steps |
| superscript $n$ | — | Time level $t^n = n\Delta t$; half levels $n\pm\tfrac12$ for leapfrog/Boris velocities |

Indices: $j$ for nodes, $p$ for particles, $n$ for time levels.

## Particles
| Symbol | Code | Meaning |
|---|---|---|
| $N_{ppc}$ | `Nppc` | Macroparticles per cell per species |
| $N_p$ | `Np` | Macroparticles per species |
| $w$ | `w` | Weight $= n_0\Delta y/N_{ppc}$ (physical particles per unit transverse area). Equal and constant for all |
| $\xi_p = y_p/\Delta y$ | `pos_e`, `pos_i` | Position **in cell units** (P0 prototype convention, see D-004) |
| $\mathbf v_p$ | `vel_e`, `vel_i` | Velocity (m/s); 3 components from P1 onwards |
| $q_s/m_s$ | `q_m` | Charge-to-mass ratio |

## Fields and moments
| Symbol | Code | Meaning |
|---|---|---|
| $\phi$ | `phi` | Potential of the self-consistent perturbation |
| $E_1 = -\partial_y\phi$ | `E_nodes`, `E_cells` | Self-consistent azimuthal field (written $E_y$ when unambiguous) |
| $n_s$ | `ne`, `ni` | Density. **P0 code: macroparticle count per node**; physical $= n_s w/\Delta y$ |
| $\rho$ | — | $e(n_i - n_e)$ |
| $j_{ze}$ | `jze` | Axial electron current density: the **anomalous transport** diagnostic |

Poisson: $\partial_y^2\phi = -\rho/\varepsilon_0$.

## Linear theory
| Symbol | Meaning |
|---|---|
| $k_y$, $n$ | Wavenumber; mode number $k_y = 2\pi n/L_y$ |
| $\omega = \omega_r + i\gamma$ | Complex frequency; $\gamma$ = growth rate |
| $\omega_e = \omega - k_yu_{ye0}$ | Doppler-shifted frequency |
| $b_e = k^2\rho_{e0}^2$ | Bessel-function argument in $g(\omega_e,b_e)$ |
| $m$ | Cyclotron resonance index |

## Diagnostics
| Symbol | Code | Meaning |
|---|---|---|
| $P_s$ | `mom_e`, `mom_i` | Total momentum of species $s$ (unweighted sum in P0) |
| $K_s$ | `ene_e`, `ene_i` | Kinetic energy of species $s$ (unweighted in P0) |
| $W_E$ | `ene_f` | Field energy $\sum_j\tfrac12\varepsilon_0E_j^2\Delta y$; compared with $K_s$ as `ene_f/w` |
