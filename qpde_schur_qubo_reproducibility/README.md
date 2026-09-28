# Reusable QUBO Block-Schur PDE Solvers — Code and Data

This repository is the **code-and-data companion** for the study
**“Reusable QUBO-Derived Block-Schur Inverse Factors for Fixed-Operator Finite-Difference PDE Solvers.”**

It contains the computational material needed to inspect, regenerate, and verify the
reported numerical results:

- clean numerical source code for the reusable block-Schur and fixed-point/QUBO utilities;
- the experiments that are fully rerunnable from source;
- the archived primary outputs for the exact 24-bit oracle studies;
- the sample-level and job-level records from the QCI Dirac-3 hardware campaign;
- deterministic scripts that rebuild the processed data tables;
- publication-quality result plots regenerated from those processed tables;
- automated consistency checks for the central numerical claims.

**The manuscript PDF, LaTeX source, bibliography, and journal submission files are not
included in this repository.**  This is intentionally a computational companion package,
not a public copy of the paper.

The repository also excludes superseded experiments, old development folders, temporary
render files, notebooks, unused data archives, credentials, and other research-history
artifacts that are not needed to understand or reproduce the final computational record.

---

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Rebuild the processed data, verify the archived results, regenerate the figures, and audit
the stored hardware records:

```bash
make all
```

Or run the steps separately:

```bash
python analysis/build_processed_data.py
python analysis/verify_results.py
python analysis/generate_figures.py
python analysis/audit_dirac3.py
```

---

## Reproducibility levels

| Study | Included material | Reproduction mode |
|---|---|---|
| Exact quantization sweep, B=2 | exact archived result tables, configurations, fitted slopes | deterministic rebuild and audit of reported outputs |
| Five-PDE B=2 validation | primary outputs for all five PDEs plus authoritative summary | deterministic rebuild and audit of reported outputs |
| N=960 large-block study | clean runnable code plus archived reference CSV | fully rerunnable locally |
| B=8 / 96-bit optimizer study | clean runnable code, fixed seeds, archived outputs | fully rerunnable locally |
| QCI Dirac-3 campaign | 457 stored returned-sample rows, 34 unique jobs, 60 mapped instances, PDE reconstructions | fully auditable offline; device execution itself requires hardware access |

The original GPU exhaustive-enumeration driver used for the exact 24-bit runs was not
preserved in the final canonical project archive.  This repository therefore preserves
the exact primary outputs from those runs and validates them deterministically rather than
inventing replacement code and presenting it as the original implementation.

---

## Repository layout

```text
.
├── README.md
├── CITATION.cff
├── requirements.txt
├── Makefile
├── VERSION
│
├── src/qpde_schur/
│   ├── core.py
│   └── binary.py
│
├── experiments/
│   ├── run_large_block.py
│   └── run_b8_optimizer.py
│
├── analysis/
│   ├── build_processed_data.py
│   ├── generate_figures.py
│   ├── verify_results.py
│   └── audit_dirac3.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── figures/
│   ├── figure_02_quantization_convergence.png
│   ├── figure_03_five_pde_validation.png
│   ├── figure_04_large_block_scaling.png
│   ├── figure_05_b8_optimizer.png
│   ├── figure_06_dirac3_audit.png
│   └── figure_07_dirac3_reconstructions.png
│
├── docs/
│   ├── REPRODUCIBILITY.md
│   ├── EXPERIMENTS.md
│   ├── DATA_DICTIONARY.md
│   ├── FIGURES.md
│   ├── HARDWARE_AUDIT.md
│   └── REPOSITORY_MAP.md
│
└── .github/workflows/verify.yml
```

---

## Fully rerunnable experiments

### Large-block representability/resource sweep

```bash
python experiments/run_large_block.py
```

This reproduces the fixed-`N=960` sweep for `B = 2, 4, 8, 16, 32`.  It computes classical
Schur inverses, rounds them to the same signed fixed-point representation used by the QUBO
construction, and propagates the cached factors through the block solve.  It does **not**
claim global optimization of the 96-, 192-, or 384-bit QUBOs.

### B=8 / 96-bit optimizer study

```bash
python experiments/run_b8_optimizer.py
```

The script reproduces the rounded reference, greedy polishing, cold-start simulated
annealing plus polishing, warm-start simulated annealing plus polishing, and the full
960-column greedy-polish pass.  Seeds and search budgets are explicit in the source.
No 96-bit ground-state certificate is claimed.

---

## Hardware audit

The Dirac-3 archive contains the scientific records needed to audit the hardware campaign
without account access:

- every stored returned sample and its multiplicity;
- all 34 unique submitted jobs and job IDs;
- the mapping back to 60 PDE inverse-column uses;
- exact finite-bit reference comparisons;
- decoded inverse-column residuals;
- end-to-end Heat, Poisson, and Klein--Gordon reconstructions;
- a credential-free representative request description.

Run:

```bash
python analysis/audit_dirac3.py
```

No API keys, access tokens, or account credentials are included.

---

## Regeneration guide: new manuscript and archived evidence

Run these from this package directory after `pip install -r requirements.txt`.

**Recompute the new Figure 3/Table 3 from the PDEs and exact CPU finite-grid oracle** (not a replay of the historical GPU experiment):

```bash
python experimental_reconstruction/src/figure3_fixed_paper_scales.py
python experimental_reconstruction/src/figure3_multiscale.py
python experimental_reconstruction/tests/check_figure3_multiscale.py
python experimental_reconstruction/tests/check_figure3_multiscale_outputs.py
python analysis/build_processed_data.py
python analysis/generate_figures.py
```

Paste-ready, original-style LaTeX replacements are in `experimental_reconstruction/manuscript/FIGURE3_PAPER_REPLACEMENT_METHODS.tex` and `FIGURE3_PAPER_REPLACEMENT_RESULTS.tex`. Copy `experimental_reconstruction/manuscript/figure3_multiscale_plot_paper.csv` into the manuscript `data/` directory as `figure3_multiscale_plot.csv`. Figure 3 is native PGFPlots and inherits the original LaTeX font and plot style. The fixed-grid control is supplemental, not part of the primary Figure 3.\n\nThe new manuscript Table 3 is `data/processed/table3_multiscale_rows.tex` (numerical source: `data/processed/figure3_multiscale_table.csv`), and its pgfplots input is `data/processed/figure3_multiscale_plot.csv`. `figures/figure_03_five_pde_validation.png` now displays only the fresh multiscale results in the original two-panel layout. The immutable historical Table 3 source remains `data/raw/fixed_validation/summary.csv`; `data/processed/fixed_validation.csv` and `fixed_plot.csv` are archival processed views, **not** inputs to the new Figure 3. The auxiliary ground-truth, per-stage and LaTeX renderings are produced by `python experimental_reconstruction/src/render_figure3_multiscale.py`.

**Independently regenerate the Figure 2 numerical sweep:**

```bash
python experimental_reconstruction/tests/check_figure2.py
python experimental_reconstruction/run_driver.py figure2
```

**Rerun the underlying Table 4 and Table 5 numerical experiments:**

```bash
python experiments/run_large_block.py
python experiments/run_b8_optimizer.py
```

These scripts write freshly rerun outputs in `outputs/` rather than overwriting `data/raw/`. The standard main plotting pipeline uses archived source rows for Figures 2, 4 and 5 unless those new experiment outputs are explicitly reconciled and promoted.

**Regenerate all manuscript plotting derivatives and verify the archived values:**

```bash
python analysis/build_processed_data.py
python analysis/verify_results.py
python analysis/generate_figures.py
```

This produces Figures 2–7; Figure 3 uses the new separate experiment, whereas Figures 2, 4, 5–7 use the archived outputs. The historical 24-bit original CUDA timing and original `auto_bound` implementation are **not** reconstructed by this command. The new exact CPU oracle uses an analytically reduced search, so `calls*2**24` is a logical search-space count rather than visited-state or timing measurement. The new general CUDA QUBO-array solver is a separate optional API and is not the Figure 3 backend.

**Rebuild and audit stored QCI hardware results without resubmitting jobs:**

```bash
python analysis/check_qci_input_qubos.py
python analysis/reconstruct_dirac3_pde.py --write
python analysis/check_dirac3_decode.py
python analysis/audit_dirac3.py
python analysis/verify_qci_recovery.py
```

These use recorded hardware bitstrings and archived Schur data. They do not run the Dirac-3 device or reconstruct missing transient forcing/time histories. The representative input polynomial CSVs are mathematical reconstructions, not recovered original uploaded file bytes.

The figure source map is in [`docs/FIGURES.md`](docs/FIGURES.md); journal-style plots use a serif/STIX fallback when LaTeX is not installed.

---

## Hardware signed-decoding correction

A documented correction to derived signed fixed-point decoded values and residuals
is archived in [the Dirac-3 correction note](docs/DIRAC3_DECODING_CORRECTION.md).
Pre-correction snapshots are retained under `data/provenance/pre_fix_signed_decode/`.
All original bitstrings, job identifiers, normalized submitted objectives and sample
counts remain unchanged. Run the independent re-decoding audit:

```bash
python analysis/check_dirac3_decode.py
```

The original normalized QUBO coefficient input files referenced by the hardware
job records are not included in this release and are tracked as a separate
provenance/reproducibility gap.

## Independent QUBO inputs and terminal PDE reconstruction

The [34 directly accessible normalized QUBOs](data/reconstructed_qubos/) can now be checked with `python analysis/check_qci_input_qubos.py`. The [independent hardware-to-PDE reconstruction](docs/INDEPENDENT_QCI_PDE_RECONSTRUCTION.md), run by `python analysis/reconstruct_dirac3_pde.py --write`, recreates all three archived final solution fields from the original device bitstrings and Schur blocks. It uses the archived dense terminal reference to construct `b=A@u_ref`, not the lost original forcing/time histories.

## Original hardware source and reconstructed input QUBOs

The recovered original author preprocessing CSVs and the full saved 34-job QCI device-response JSONL, plus an independently audited 34-input mathematical QUBO reconstruction and corrected offline postprocessing, are preserved in [the dated recovery archive](data/provenance/qci_reconstruction_2026_09_26/README.md). The archive contains original unmodified sources and labels reconstructed coefficient CSVs with `RECONSTRUCTED_`. The original uploaded polynomial-file *bytes* are not recovered: none of the 34 reconstructed CSV hashes matches its historical term hash. Run `python analysis/verify_qci_recovery.py` to reconstruct and audit everything without contacting the device. This is a separate source-level test from the legacy published-result checks.

## Integrity checks

```bash
python analysis/verify_results.py
```

checks the convergence slopes, five-PDE validation numbers, large-block scaling and
clipping, 96-bit optimizer statistics, Dirac-3 instance accounting, exact-hit counts,
device-time total, and end-to-end hardware reconstruction errors.

A successful run ends with:

```text
All archived-result consistency checks passed.
```

---

## Citation

`CITATION.cff` is included so GitHub can expose a **Cite this repository** action.  The
repository is intended to accompany the associated publication while keeping the paper
itself outside the public code/data archive.
