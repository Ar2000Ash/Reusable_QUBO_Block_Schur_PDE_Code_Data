# QPDE exact-oracle and five-PDE reconstruction — audited development package

**Status: Figure 2 independently reproduced; Figure 3 fixed-validation refinement still unresolved.** Original experimental source is missing; these are independently reconstructed implementations. Figure 2 is now accepted by source-level numerical verification; do not substitute the candidate Table 3 outputs into published data. The immutable original source remains authoritative.

## Verified now

- The CPU **reduced-grid exact algorithm** minimizes the full 24-bit, two-scalar least-squares objective using the exact conditional quadratic optimum, and compares energy/bitstrings to 34 independent QCI reference problems. It matched all 34 archived ground-state bitstrings and the ground and second-best squared-residual energies within 7e-19.
- An independent *full binary-space torch implementation* enumerates every state in float64 chunks. A CPU full-space smoke test agrees with the reduced oracle at K=2..5. The **CUDA path is implemented but has not been executed in this environment** (no CUDA device).
- All five independently inferred manufactured fields and explicit Dirichlet traces agree with source field/operator fingerprints. The classic (dense) Heat, Burgers and Klein–Gordon integrators reproduce archived endpoint values. The Poisson and Helmholtz manufactured traces and continuous/discrete residuals agree with archived fingerprints.
- Figure 2: all 14 precision-sweep rows now reproduce the archived numerical results and fitted slopes under the reconstructed homogeneous boundary/input protocol.
- Table 3 model matrices have the original stated sizes and conditions, and four exact-oracle calls per column reproduce the 80 / 160 workload counts.

## Not yet verified

- The numerical Figure 2 reconstruction is described in `docs/FIGURE2_RECONSTRUCTION.md`; its separate CUDA implementation still requires an actual device run.
- Figure 3: historical `auto_bound` and three-pass correction scaling. Candidate correction schedules do not reproduce the archived per-PDE errors or cached inverse residuals.
- New CUDA device run. Do not report device timing comparisons until measured on a named GPU.

## Dependencies

Python 3.11+ with NumPy. PyTorch is needed only for full-bitspace torch enumeration (`--backend=cuda` requires a CUDA-capable build and GPU). No QCI token or live hardware connection is used.

## Commands

```bash
python tests/check_oracle.py
python tests/check_archived_qci.py # reads original archived source adjacent to project, or repo data/raw/dirac3
python tests/check_boundaries.py
python tests/check_figure2.py    # source-to-experiment verification of all 14 sweep rows and fitted slopes
python run_driver.py oracle --all --out outputs/qci_certified_reference.csv
python run_driver.py oracle --id QCI-001 --backend cuda --chunk-power 16
python tests/compare_results.py  # Figure 2 passes; Figure 3 remains explicitly INCOMPLETE
```

To run inside the current GitHub package, put these files in `experimental_reconstruction/`; `tests/check_archived_qci.py` will locate `../data/raw/dirac3/reconstructed_60_instances.csv`. Run the CUDA command on your RTX 5070 Ti Laptop or A40 node after installing a compatible GPU build of PyTorch. For 24-bit instances, each job covers exactly 16,777,216 binary states, not an estimated/sample-based search.

Read `docs/BOUNDARY_AUDIT.md` for exact boundary functions, time-level treatment, and known reproduction gaps.
