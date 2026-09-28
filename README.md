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

The [2026-09-26 original QCI source recovery](qpde_schur_qubo_reproducibility/data/provenance/qci_reconstruction_2026_09_26/README.md) preserves the original 34-job device response JSONL and six preprocessing source tables alongside independently reconstructed mathematical QUBO inputs and corrected signed-decoding outputs. The 34 original uploaded polynomial files have **not** been recovered byte-for-byte. Their archived original hashes remain separate from new reconstructed-file hashes. No new hardware experiment was performed.

The independent [GitHub Actions audit](.github/workflows/audit.yml) runs the preprocessing, decoding, numerical checks, result figures, large-block experiment and raw-QCI reconstruction verification. The historical exact 24-bit enumeration driver and complete original PDE driver remain unarchived; consult project documentation for the precise reproducibility boundary.

The repository has no explicit software license yet. Copyrighted code is provided for review and reproducibility, but no open-source license is implied.

## Independently rerun fixed-scale Figure 3

A new fixed-paper-scale five-PDE benchmark and manuscript replacement, with all three correction passes explicitly logged, is available under [experimental_reconstruction](qpde_schur_qubo_reproducibility/experimental_reconstruction/docs/FIGURE3_FIXED_SCALE_PROTOCOL.md). Its [Figure 3](qpde_schur_qubo_reproducibility/experimental_reconstruction/figures/figure3_fixed_paper_scales.svg) and [new Table 3](qpde_schur_qubo_reproducibility/experimental_reconstruction/outputs/figure3_fixed_paper_scales.csv) are fresh **CPU-exact reduced-grid** measurements. The original archived `auto_bound` results remain untouched. With unchanged nominal scales all 360 residual-correction solves return zero; no refinement gain or new GPU timings are claimed.

## New multiscale five-PDE Figure 3

The independently rerun [predetermined multiscale Figure 3](qpde_schur_qubo_reproducibility/experimental_reconstruction/docs/FIGURE3_MULTISCALE_PROTOCOL.md) is the recommended **new** five-PDE numerical result for the revised manuscript. It retains the paper's initial scales, 24-bit QUBO, PDE data and the same four solves per column, but explicitly reduces the correction scale by a factor eight at each stage. [New Table 3](qpde_schur_qubo_reproducibility/experimental_reconstruction/outputs/figure3_multiscale.csv), [Figure 3 SVG](qpde_schur_qubo_reproducibility/experimental_reconstruction/figures/figure3_multiscale.svg), [stage diagnostics](qpde_schur_qubo_reproducibility/experimental_reconstruction/figures/figure3_multiscale_stages.svg), and [manuscript LaTeX](qpde_schur_qubo_reproducibility/experimental_reconstruction/manuscript/FIGURE3_MULTISCALE_REVISION.tex) are generated independently of the preserved historical data. The original fixed-grid rerun remains a control. The new results do not claim GPU or QCI hardware timings.
