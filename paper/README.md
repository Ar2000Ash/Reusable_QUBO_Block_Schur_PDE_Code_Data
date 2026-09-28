# Manuscript figure source

The complete manuscript uses native LaTeX/PGFPlots typography. The files here provide the Figure 3 plot and data directly from the five-PDE experiment:

- `figure3.tex` — two-panel PGFPlots Figure 3, with the paper's legend, metrics and labels.
- `data/figure3_multiscale_plot.csv` — numerical data used by the two panels.
- `qpde_figure_style.tex` — the figure palette, axis style and TikZ definitions.

Include the shared figure style in the manuscript preamble and place the data CSV under the manuscript's `data/` directory. Figure 3's numerical rows and Table 3 are also written automatically to `data/processed/` by `analysis/build_processed_data.py`. The source experiment is `finite_bit/src/figure3_multiscale.py`.

For the other numerical figures, run `python analysis/generate_figures.py`; the plotting code reads the corresponding generated tables in `data/processed/` and uses TeX-rendered fonts when LaTeX is installed.
