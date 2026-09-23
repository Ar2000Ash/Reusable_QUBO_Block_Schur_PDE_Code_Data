# Experiment matrix

This page summarizes the numerical settings represented in the repository. The table below records the numerical settings represented in the repository.

| Study | Main settings | Optimization status | Primary source |
|---|---|---|---|
| Quantization K-sweep | B=2, M=1, K=4...10; Poisson 2D and Klein-Gordon 1D | exact finite-bit enumeration | `data/raw/k_sweep/` |
| Five-PDE validation | B=2, M=1, K=10; Heat, Burgers, Poisson, Helmholtz, Klein-Gordon | exact finite-bit enumeration; three refinement passes | `data/raw/fixed_validation/` |
| Large-block Poisson | N=960; B=2,4,8,16,32; M=1, K=10 | classical inverse + fixed-point quantization; no large-QUBO optimum claim | `experiments/run_large_block.py` |
| B=8 optimizer | N=960; B=8; 96 logical bits; 32 representative QUBOs + 960-column full polish | rounded, greedy, cold SA, warm SA; no exact certificate | `experiments/run_b8_optimizer.py` |
| Dirac-3 hardware | B=2; 24 logical bits; 60 mapped instances; 34 unique submissions | real QCI Dirac-3 samples compared with exact finite-bit references | `data/raw/dirac3/` |

## Exact-oracle accounting

For the B=2, M=1, K=10 validation, one inverse-column QUBO has 24 logical bits and
therefore 2^24 binary candidates. The archived diagnostics record 80 QUBO calls for each
20-variable scalar problem and 160 calls for the 40-variable interleaved Klein-Gordon
problem. No classical inverse column was substituted into the reported cached solutions.

## Large-block interpretation

The large-B study is intentionally a representation experiment. It answers whether the
fixed-point format remains numerically usable as B grows and records the resulting logical
variable/coupling counts. The 96-, 192-, and 384-bit problems were not globally optimized.

## Hardware interpretation

The hardware archive contains 60 mapped PDE inverse-column instances but only 34 unique
submissions because several local QUBOs repeat. The unique-job table records 558 seconds of
metered device usage in total. These values document the experiment and are not a speedup
claim.
