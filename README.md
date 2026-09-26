# Reusable QUBO-derived Block-Schur PDE Code and Data

This repository is the computational companion to *Reusable QUBO-Derived Block-Schur Inverse Factors for Fixed-Operator Finite-Difference PDE Solvers*. All scripts, archived paper figures and numerical data are inside [`qpde_schur_qubo_reproducibility/`](qpde_schur_qubo_reproducibility/).

```bash
cd qpde_schur_qubo_reproducibility
python -m pip install -r requirements.txt
sha256sum -c SHA256SUMS.txt
python analysis/build_processed_data.py
python analysis/verify_results.py
python analysis/check_dirac3_decode.py
python analysis/verify_qci_recovery.py
```

The [2026-09-26 original QCI source recovery](qpde_schur_qubo_reproducibility/data/provenance/qci_reconstruction_2026_09_26/README.md) preserves the original 34-job device response JSONL and six preprocessing source tables alongside independently reconstructed mathematical QUBO inputs and corrected signed-decoding outputs. The 34 original uploaded polynomial files have **not** been recovered byte-for-byte. Their archived original hashes remain separate from new reconstructed-file hashes. No new hardware experiment was performed.

The independent [GitHub Actions audit](.github/workflows/audit.yml) runs the preprocessing, decoding, numerical checks, result figures, large-block experiment and raw-QCI reconstruction verification. The historical exact 24-bit enumeration driver and complete original PDE driver remain unarchived; consult project documentation for the precise reproducibility boundary.

The repository has no explicit software license yet. Copyrighted code is provided for review and reproducibility, but no open-source license is implied.
