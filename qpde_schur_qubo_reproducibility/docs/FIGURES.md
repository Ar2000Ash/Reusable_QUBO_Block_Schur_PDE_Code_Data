# Figure regeneration map

All figures in `figures/` are deterministic derivatives of `data/processed/` and can be
recreated with:

```bash
python analysis/generate_figures.py
```

| Figure file | Source data | Purpose |
|---|---|---|
| `figure_02_quantization_convergence.png` | `k_sweep_compact.csv` | fixed-point convergence for Poisson and Klein--Gordon |
| `figure_03_five_pde_validation.png` | `fixed_plot.csv` | end-to-end error and cached inverse residual across five PDEs |
| `figure_04_large_block_scaling.png` | `largeB.csv` | block-size resource growth and propagated accuracy |
| `figure_05_b8_optimizer.png` | `b8_optimizer_plot.csv`, `b8_full_solve.csv` | 96-bit optimizer comparison and full cached solve |
| `figure_06_dirac3_audit.png` | `dirac_plot_summary.csv`, `dirac_scatter.csv` | hardware exact-hit and residual/objective audit |
| `figure_07_dirac3_reconstructions.png` | `dirac_heat.csv`, `dirac_poisson_slices.csv`, `dirac_kg.csv` | end-to-end hardware-derived PDE reconstructions |

The plotting script uses LaTeX text rendering when LaTeX is installed.  Axis ranges and
small boundary margins are chosen so that endpoint markers remain fully visible.
