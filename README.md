# Reusable QUBO-derived Block-Schur PDE Code and Data

This repository is the computational companion to *Reusable QUBO-Derived Block-Schur Inverse Factors for Fixed-Operator Finite-Difference PDE Solvers*. All scripts, archived paper figures and numerical data are inside [`qpde_schur_qubo_reproducibility/`](qpde_schur_qubo_reproducibility/).

```bash
cd qpde_schur_qubo_reproducibility
python -m pip install -r requirements.txt
sha256sum -c SHA256SUMS.txt
python analysis/build_processed_data.py
python analysis/verify_results.py
python analysis/check_dirac3_decode.py
python analysis/check_qci_input_qubos.py
python analysis/reconstruct_dirac3_pde.py --write
python analysis/verify_qci_recovery.py
```

The [2026-09-26 original QCI source](qpde_schur_qubo_reproducibility/data/provenance/qci_reconstruction_2026_09_26/README.md) preserves the original 34-job device response JSONL and six preprocessing source tables alongside mathematical QUBO inputs and signed-decoding outputs.

The independent [GitHub Actions audit](.github/workflows/audit.yml) runs the preprocessing, decoding, numerical checks, result figures, large-block experiment and raw-QCI reconstruction verification.

## Sequential CUDA QUBO array solver

The new [general-purpose sequential CUDA utility](qpde_schur_qubo_reproducibility/experimental_reconstruction/docs/CUDA_BATCH_QUBO.md) accepts arrays or iterables of QUBO matrices and returns minimum bitstrings and objective values in input order. It exhaustively searches one QUBO at a time in bounded GPU-memory batches using float64.
