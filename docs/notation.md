# Notation — TFM: Kinetic modeling of plasma instabilities in a Hall thruster discharge

Single source of truth for symbols in the code, the report and the defense slides.
Rule: **one symbol = one meaning**. To add or change a symbol, edit this file first and log it in `decisions.md`.

Units: SI throughout. Temperatures are stored **in joules** in the code (`Te = 10.0*e`) and reported **in eV** in text and plots.

## Physical constants

| Symbol (text) | Code | Meaning | Value / unit |
|---|---|---|---|
| $e$ | `e` | Elementary charge | 1.60217663e-19 C |
| $m_e$ | `me` | Electron mass | 9.1093837e-31 kg |
| $m_i$ | `mi` | Ion mass (xenon, 131.29 u) | 2.1801714e-25 kg |
| $\varepsilon_0$ | `eps0` | Vacuum permittivity | 8.8541878188e-12 F/m |

## Plasma parameters

| Symbol | Code | Meaning | Unit |
|---|---|---|---|
| $n_0$ | `n` (scalar) | Reference (initial, uniform) density | m⁻³ |
| $T_e,\ T_i$ | `Te`, `Ti` | Electron / ion temperature | J in code, eV in text |
| $\omega_{pe} = \sqrt{n_0 e^2/(m_e\varepsilon_0)}$ | `omega_pe` | Electron plasma frequency | rad/s |
| $\lambda_D = \sqrt{\varepsilon_0 T_e/(n_0 e^2)}$ | `l_debye` | Electron Debye length | m |
| $\bar c_e = \sqrt{8T_e/(\pi m_e)}$ | `c_bar_e` | Mean electron thermal speed | m/s |
| $v_{th,s} = \sqrt{T_s/m_s}$ | — | Thermal speed (1D std. dev. of Maxwellian) of species $s$ | m/s |

Note: initial velocities are sampled as `sqrt(2T/m)*erfinv(2U-1)`, i.e. a Maxwellian with standard deviation $v_{th,s}=\sqrt{T_s/m_s}$.

## Grid and time

| Symbol | Code | Meaning |
|---|---|---|
| $L = x_{max}-x_{min}$ | `xmax - xmin` | Domain length (periodic) |
| $N_x$ | `nx` | Number of **nodes** (= $N_c+1$); node `nx-1` is the periodic image of node 0 |
| $N_c$ | `nx-1` | Number of cells |
| $\Delta x$ | `dx` | Cell size |
| $x_j$ | `x[j]` | Node position, $j = 0,\dots,N_x-1$ |
| $\Delta t$ | `dt` | Time step |
| $N_t$ | `Nt` | Number of time steps |
| superscript $n$ | loop index `t` | Time level $t^n = n\Delta t$ |

Index convention: $j$ for grid nodes, $p$ for particles, $n$ for time levels, $s \in \{e, i\}$ for species.

## Particles

| Symbol | Code | Meaning |
|---|---|---|
| $N_{ppc}$ | `Nppc` | Macroparticles per cell (per species) |
| $N_p$ | `Np` | Macroparticles per species |
| $w$ | `w` | Macroparticle weight = $n_0\Delta x/N_{ppc}$ (physical particles per unit transverse area, m⁻²) |
| $\xi_p = (x_p - x_{min})/\Delta x$ | `pos_e`, `pos_i` | Particle position **in cell units** (code stores ξ, not x) |
| $v_p$ | `vel_e`, `vel_i` | Particle velocity (m/s) |
| $q_s/m_s$ | `q_m` | Charge-to-mass ratio |
| $S(\cdot)$ | — | Particle shape function (CIC = linear) |

## Fields and moments

| Symbol | Code | Meaning |
|---|---|---|
| $n_s$ | `ne`, `ni` | Density. In code: **macroparticle count per node**; physical density = `n_s*w/dx` |
| $\rho = e(n_i - n_e)$ | — | Charge density |
| $\phi$ | `phi` | Electrostatic potential (gauge: $\phi_{N_x-1}=0$) |
| $E$ | `E_nodes`, `E_cells` | Electric field at nodes / at cell centres |

Poisson equation as solved: $\nabla^2\phi = -\rho/\varepsilon_0 = e(n_e-n_i)/\varepsilon_0$.

## Diagnostics

| Symbol | Code | Meaning |
|---|---|---|
| $P_s$ | `mom_e`, `mom_i` | Total momentum of species $s$ (per macroparticle sum, unweighted) |
| $K_s$ | `ene_e`, `ene_i` | Kinetic energy of species $s$ (unweighted) |
| $W_E = \sum_j \tfrac12\varepsilon_0 E_j^2\Delta x$ | `ene_f` | Field energy (per unit area); compared with $K_s$ as `ene_f/w` |

## Reserved (planned; confirm before use)

For upcoming E×B / Hall-thruster physics — fix these when the model needs them:
$B_0$ (applied magnetic field), $E_0$ (applied axial field), $\mathbf{v}_{E\times B}$ (drift velocity),
$\omega_{ce}$ (electron cyclotron frequency), $\rho_e$ (electron Larmor radius), $k$ (wavenumber), $\omega,\ \gamma$ (real frequency, growth rate).
Coordinate names for Hall thruster directions (axial / azimuthal / radial): **open**, see `decisions.md` O-3.
