# Revision checklist: new Figure 3 (fixed initial scales + geometric correction scales)

The accompanying `FIGURE3_MULTISCALE_REVISION.tex` is a **replacement for the five-PDE part of the numerical-methods section, Table 3, Figure 3, and corresponding results/limitations statements**, not a recovered historical driver. It is generated/checked against fresh source tables in `outputs/figure3_multiscale.csv`, `outputs/figure3_multiscale_stage_log.csv`, and `manuscript/figure3_multiscale_plot.csv`.

Preserve Figure 2 and its independent sweep reproduction; large-block and 96-bit studies; and original hardware Figures 6–7. Their QUBOs, precision settings and hardware evidence are unaffected. Preserve historical `data/raw/fixed_validation` unchanged.

Update methods explicitly: `gamma_p=gamma0*8^(-p)` for `p=0,1,2,3`; initial `gamma0` values unchanged and `B=2,M=1,K=10`; classical exact correction solves are used **only in the representability audit**, not in range selection or bitstring choice. Schur blocks use preceding quantized inverse. There are 480 total CPU exact reduced-grid QUBO calls, but this is **not** 480 full-space 2^24 candidate enumerations and not GPU timing.

Replace Table 3 numerical values, Figure 3 plot input and caption, and the adjacent discussion. Include separate Klein–Gordon velocity and displacement component metrics. In the discussion explain the fixed-grid stagnation from the separate baseline and that the narrower correction scales provide new resolution. Retain the provenance caveat about independently inferred boundary/forcing functions and the distinction between continuous and dense numerical reference. Do not claim the historic missing `auto_bound` stage scales were recovered.

For a direct LaTeX-source update, copy `manuscript/figure3_multiscale_plot.csv` into the manuscript's `data/` directory and replace the existing `\label{tab:fixed_validation}` and `\label{fig:fixed_validation}` blocks with the supplied LaTeX. Old abstract, discussion, conclusions and data availability sentences quoting historical Table 3 error ranges must be updated. No other figure's source data should be touched.
