# CLAUDE.md — TFM: Kinetic modeling of plasma instabilities in a Hall thruster discharge

MSc thesis (TFM) of Carlos Rodríguez Sánchez. A 1D-azimuthal, collisionless, electrostatic **1D3V PIC** code in
Python to study the electron cyclotron drift instability (ECDI) and the anomalous electron transport it drives in Hall thrusters.
The code is built incrementally, validated against Bello-Benítez et al. (2024), and then used to compare numerical
parameters and PIC algorithms, and subsonic vs supersonic electron drift.

## Read first
- `docs/scope.md`: motivation, validation case (Bello Table I), and the **roadmap P0–P5**. Check which phase we are in.
- `docs/notation.md`: symbols and code names. Use them exactly. Propose additions; never rename silently.
- `docs/decisions.md`: scope (S), settled numerics (D), assumptions (A) and open questions (O).
  If a change conflicts with an S/D entry, stop and say so.

## Layout
- `prototypes/`: exploratory scripts. `conservation_test.py` = P0: 1D electrostatic periodic PIC, e⁻ + Xe⁺, CIC, sparse Poisson.
- `src/`: reusable, tested code (to be created in P1).
- `tests/`: pytest (to be created in P1).
- `docs/`: scope, notation, decisions. `references/` and `outputs/` are git-ignored.

## Physics invariants: never violate
- **Start simple, build slowly.** Implement only the current roadmap phase. Don't add features from later phases unasked.
- Never modify the pusher, deposition, interpolation or field solve without first stating the change mathematically
  (equations + which conservation property it affects) and getting my "go".
- Electrons feel $E_0\mathbf 1_z + E_1\mathbf 1_y$ and $B_0\mathbf 1_x$; ions feel only $E_1\mathbf 1_y$ (S-003).
- Every algorithm variant (pusher, shape function, solver) must be **selectable**, not overwritten: P4 compares them
  against the validated baseline.
- Keep the deposition/interpolation pairing explicit (momentum- vs energy-conserving, D-008).
- The FD Poisson gauge assumes zero net charge (D-006). Flag anything that breaks it.
- Report resolution whenever parameters change: Δy/λ_D0, ω_pe0·Δt, ω_ce·Δt, max|v_y|Δt/Δy (< 1).
- Never "fix" a conservation or validation plot by changing the diagnostic alone. Explain the cause first.
- Terminology: "oscillations", "instability-driven transport". Not "turbulence".

## Workflow
- Plan before coding anything non-trivial, and wait for my approval.
- Each phase ends with tests that pass (e.g. P1: gyration frequency/radius, |v| conserved in pure B, E×B drift = E0/B0).
- After any numerics change, run `pytest -q` and the conservation check, and report relative momentum and energy drift.
- Fixed RNG seeds in tests. numba kernels must have a slow reference version that the tests compare against (A-2).
- Record new decisions in `docs/decisions.md` (and symbols in `docs/notation.md`) in the same commit as the code.
- Small commits with clear messages. Never commit `outputs/`, large data or PDFs.
- Platform: Windows, PowerShell. Use `python`, not `python3`.

## Commands
- Run P0 prototype: `python prototypes/conservation_test.py`
- Tests (from P1): `pytest -q`
