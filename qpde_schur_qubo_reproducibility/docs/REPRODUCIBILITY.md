# Reproducibility guide

The repository preserves four kinds of computational evidence at the appropriate level.

## 1. Exact 24-bit oracle studies

The quantization sweep and the five-PDE `B=2` validation used exhaustive finite-bit
enumeration.  Their archived primary tables and configurations are stored under
`data/raw/k_sweep/` and `data/raw/fixed_validation/`.

The original GPU enumeration driver was not preserved in the final canonical source
archive.  The repository therefore does not replace it with a newly written program and
misrepresent that program as the original.  Instead it retains the exact primary outputs
and provides deterministic processing and consistency checks.

## 2. Large-block representability/resource sweep

Fully rerunnable:

```bash
python experiments/run_large_block.py
```

The experiment computes classical Schur inverse blocks, quantizes them onto the signed
fixed-point grid, and propagates them through the cached block solve.  The large dense
QUBOs are not asserted to have been globally optimized.

## 3. B=8 / 96-bit heuristic optimization

Fully rerunnable with fixed random seeds:

```bash
python experiments/run_b8_optimizer.py
```

The script evaluates direct rounding, greedy local search, cold-start simulated annealing,
warm-start simulated annealing, and the full 960-column greedy-polish pass.  Scientific
objective/residual/error values are deterministic; wall-clock timings depend on hardware.

## 4. QCI Dirac-3 hardware campaign

Physical device execution requires external hardware access and cannot be reproduced
offline.  The repository instead preserves the sample-level and job-level records required
to audit the reported campaign, including the mapping to all 60 PDE inverse-column uses and
the reconstructed PDE fields.

Run:

```bash
python analysis/audit_dirac3.py
```

No credentials are stored.

## Rebuild processed data and figures

```bash
python analysis/build_processed_data.py
python analysis/generate_figures.py
python analysis/verify_results.py
```

The public package intentionally contains no manuscript source or paper PDF.
