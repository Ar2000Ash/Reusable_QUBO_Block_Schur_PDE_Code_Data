# Data layout

The repository separates **primary archived scientific outputs** from compact deterministic
derivatives used by the audit and plotting scripts.

## `raw/`

These are the source records retained from the experiments represented in the final
computational study.  They should be treated as immutable inputs.

- `k_sweep/` — exact small-QUBO convergence tables and fitted slopes for Poisson 2D and Klein--Gordon 1D.
- `fixed_validation/` — primary outputs for the five `B=2`, `M=1`, `K=10` validation problems plus the authoritative cross-PDE summary.
- `large_block/` — archived `N=960`, `B=2...32` representability/resource sweep.
- `b8_optimizer/` — archived 96-bit `B=8` optimizer results and the full 960-column greedy-polish study.
- `dirac3/` — sample-level and job-level QCI Dirac-3 records, mapped exact-reference audit, end-to-end PDE reconstructions, and credential-free representative job metadata.

## `processed/`

These CSV files are deterministic derivatives of `raw/`.  They are consumed by the
verification and figure-generation scripts.

Regenerate them with:

```bash
python analysis/build_processed_data.py
```

Then verify the quantitative record with:

```bash
python analysis/verify_results.py
```

No processed file needs to be edited manually.
