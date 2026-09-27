# QPDE exact-oracle and five-PDE reconstruction — audited development package

**Status: partly verified, not an accepted replacement for the archived Figure 2/3 experiments.** Original experimental source is missing; these are independently reconstructed implementations. Do not use candidate sweep/fixed CSVs as published data until source-level equality and numeric acceptance checks succeed. The immutable original source remains authoritative.

## Verified now

- The CPU **reduced-grid exact algorithm** minimizes the full 24-bit, two-scalar least-squares objective using the exact conditional quadratic optimum, and compares energy/bitstrings to 34 independent QCI reference problems. It matched all 34 archived ground-state bitstrings and the ground and second-best squared-residual energies within 7e-19.
- An independent *full binary-space torch implementation* enumerates every state in float64 chunks. A CPU full-space smoke test agrees with the reduced oracle at K=2..5. The **CUDA path is implemented but has not been executed in this environment** (no CUDA device).
- All five independently inferred manufactured fields and explicit Dirichlet traces agree with source field/operator fingerprints. The classic (dense) Heat, Burgers and Klein–Gordon integrators reproduce archived endpoint values. The Poisson and Helmholtz manufactured traces and continuous/discrete residuals agree with archived fingerprints.
- Table 3 model matrices have the original stated sizes and conditions, and four exact-oracle calls per column reproduce the 80 / 160 workload counts.

## Not yet verified

- Figure 2: fresh K-sweep *complete* metrics. The saved config does not identify the original sweep forcing/initial/boundary histories; importing fixed-case manufactured functions does not reproduce the archived sweep.
- Figure 3: historical `auto_bound` and three-pass correction scaling. Candidate correction schedules do not reproduce the archived per-PDE errors or cached inverse residuals.
- New CUDA device run. Do not report device timing comparisons until measured on a named GPU.

## Dependencies

Python 3.11+ with NumPy. PyTorch is needed only for full-bitspace torch enumeration (`--backend=cuda` requires a CUDA-capable build and GPU). No QCI token or live hardware connection is used.

## Commands

```bash
python tests/check_oracle.py
python tests/check_archived_qci.py # reads original archived source adjacent to project, or repo data/raw/dirac3
python tests/check_boundaries.py
python run_driver.py oracle --all --out outputs/qci_certified_reference.csv
python run_driver.py oracle --id QCI-001 --backend cuda --chunk-power 16
python tests/compare_results.py  # intentionally reports Fig 2/3 as INCOMPLETE, does not overwrite source
```

To run inside the current GitHub package, put these files in `experimental_reconstruction/`; `tests/check_archived_qci.py` will locate `../data/raw/dirac3/reconstructed_60_instances.csv`. Run the CUDA command on your RTX 5070 Ti Laptop or A40 node after installing a compatible GPU build of PyTorch. For 24-bit instances, each job covers exactly 16,777,216 binary states, not an estimated/sample-based search.

Read `docs/BOUNDARY_AUDIT.md` for exact boundary functions, time-level treatment, and known reproduction gaps.
