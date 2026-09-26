# Independently reconstructed terminal PDE validation

This release exposes **all 34 normalized, upper-triangular 24-bit mathematical input QUBOs directly** in `data/reconstructed_qubos/`. Each of the 34 text CSV files contains exactly 300 terms; `MANIFEST.csv` identifies its unique job, representative instance, filename, and actual SHA-256. The reconstructed numerical coefficients, not byte-identical historical uploads, are the maintained reproducible input objects. `python analysis/check_qci_input_qubos.py` checks all entries against the independently reconstructed formula based on the archived Schur block and signed encoding, and checks objective values at recorded reference/device bitstrings. The immutable dated recovery archive remains available under `data/provenance/qci_reconstruction_2026_09_26/`.

`python analysis/reconstruct_dirac3_pde.py --write` reconstructs the Heat 1D, Poisson 2D, and Klein–Gordon 1D *terminal* numerical fields, rather than merely copying published hardware-solution columns. For every original recorded 24-bit hardware bitstring, it independently decodes two signed 12-bit scalar values, assembles the 2×2 inverse block columns and the ten archived Schur blocks, reconstructs the 20×20 block-tridiagonal operator from the first two Schur blocks, and applies classical forward and backward block-Schur substitution.

**Terminal RHS provenance:** the archived dense final reference vector is preserved but the original time-dependent forcing and boundary-history driver is missing. The reconstruction defines `b = A @ u_ref` separately for each archived terminal vector and checks that exact dense factors reproduce it; this is a reproducible *terminal linear solve*, not a reconstruction of the complete original transient PDE trajectory or a new QCI run. The independently reconstructed QCI terminal solutions match all 60 archived components to machine precision. The archived `data/raw/dirac3/*_solution.csv` sources remain unchanged.

`analysis/build_processed_data.py` now invokes the independent PDE routine and regenerates `data/processed/dirac_heat.csv`, `dirac_poisson.csv`, `dirac_kg.csv`, `dirac_poisson_slices.csv`, `dirac_pde_independent_reconstruction.csv` and explicit terminal RHS tables from the newly decoded hardware bitstrings. Figure 7 uses these regenerated values; Figure 6 is independently generated from the corrected local QCI mapping and archived result audit. `analysis/verify_results.py` validates the published summary scalars. GitHub Actions runs the independent QUBO, terminal PDE, numerical-summary, integrity and figure checks.

| PDE | Relative terminal error | Relative terminal residual |
|---|---:|---:|
| Heat 1D | 0.00032391279008389326 | 0.00033263717850195865 |
| Poisson 2D | 0.001970816149365653 | 0.015508288121356788 |
| Klein–Gordon 1D | 0.00029703911071363637 | 0.00029691333574971714 |

Expected values above are the previously reported archived numbers checked against independent regeneration, **not** newly fitted parameters. No original historical upload polynomial is implied.
