# Repository map

```text
.
├── README.md                    # entry point and quick start
├── requirements.txt            # minimal Python dependencies
├── Makefile                    # convenience commands
├── CITATION.cff                 # GitHub citation metadata
├── VERSION
├── src/qpde_schur/              # reusable numerical and fixed-point/QUBO utilities
├── experiments/                 # fully rerunnable numerical experiments
├── analysis/                    # deterministic rebuild, plotting, and audit scripts
├── data/
│   ├── raw/                     # archived primary scientific outputs
│   └── processed/               # deterministic compact derived tables
├── figures/                     # regenerated publication-quality result plots
├── docs/                        # experiment/data/reproducibility documentation
└── .github/workflows/           # automated numerical verification
```

No manuscript PDF, LaTeX source, bibliography, submission files, old revisions,
development notebooks, temporary render checks, or unused historical archives are stored
here.  The repository is intentionally limited to the computational record.
