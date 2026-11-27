# CLAUDE.md — TFM: Kinetic modeling of plasma instabilities in a Hall thruster discharge

MSc thesis (TFM) of Carlos Rodríguez Sánchez. Particle-in-cell (PIC) code in Python, built up from a
1D electrostatic periodic test toward kinetic simulation of Hall-thruster plasma instabilities.

## Read first
- `docs/notation.md` — symbols and code names. Use them exactly; propose additions, never rename silently.
- `docs/decisions.md` — settled numerics (D-xxx) and open questions (O-x). Respect D-entries; if a change
  conflicts with one, stop and say so.

## Layout
- `prototypes/` — exploratory scripts (e.g. `conservation_test.py`: 1D periodic PIC, e⁻ + Xe⁺, CIC, sparse Poisson).
- `src/` — reusable code once a prototype is promoted (not created yet).
- `tests/` — pytest tests (not created yet; first job is converting the conservation check).
- `docs/` — notation, decisions, notes. `references/` and `outputs/` are git-ignored.

## Physics invariants — never violate
- Do not modify the particle pusher, charge deposition, field solve or interpolation without first stating the
  change mathematically (equations + which conservation property it affects) and getting my "go".
- Keep the deposition/interpolation pairing explicit (momentum-conserving vs energy-conserving, see D-008).
- Poisson gauge assumes zero net charge (D-006). Flag any change that breaks it (injection, ionisation, unequal weights).
- Positions are in cell units ξ = x/Δx (D-004); densities in code are macroparticle counts per node.
- Check and report resolution whenever parameters change: Δx/λ_D, ω_pe·Δt, max |v|Δt/Δx (< 1).
- Never "fix" a conservation plot by changing the diagnostic alone; explain the cause first.

## Workflow
- Plan before code for anything beyond a trivial edit; wait for my approval.
- After changing numerics, run the conservation check (and `pytest` once tests exist) and report relative
  momentum and energy drift.
- Fixed RNG seeds in tests. Keep a slow, readable reference version of any kernel you optimise (numba/vectorised).
- Small commits with clear messages; never commit `outputs/`, large data, or PDFs.
- Platform: Windows, PowerShell. Use `python`, not `python3`.

## Commands
- Run prototype: `python prototypes/conservation_test.py`
- Tests (once added): `pytest -q`
