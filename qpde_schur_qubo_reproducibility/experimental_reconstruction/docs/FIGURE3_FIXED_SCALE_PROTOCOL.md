# Fixed nominal paper-scale Figure 3: reproducible new benchmark

**Scope:** This is an independently rerun alternative to the lost historical `auto_bound` implementation, not a recovery of its original coefficients/bitstrings/GPU times. The immutable original Table 3 data and figure remain archived. Figure 2, hardware submissions and other figures are unaffected.

## Fixed settings, including boundary data

For every column, use the paper's stated nominal scale **unchanged across all blocks and stages**: Heat and Burgers `0.60`, Poisson and Helmholtz `0.01`, Klein–Gordon `1.00`. Use `B=2`, `M=1`, `K=10` (24 bits), one initial exact QUBO minimization and precisely three correction minimizations. Build each Schur block recursively from the preceding **finite-bit decoded inverse**, as verified for Figure 2. No `auto_bound`, stage-dependent shrink, classical continuous correction range oracle or historical target data are used by `figure3_fixed_paper_scales.py`. The CPU oracle is the independent exact reduced-grid 2-scalar search, not a newly measured full-space GPU run. Candidate work `calls × 2^24` is the logical exhaustive search-space size, not actual candidate evaluations on CPU.

Unchanged PDEs and traces (see `docs/BOUNDARY_AUDIT.md`):

- Heat: 20 interior grid nodes, `nu=.08`, `dt=.001`, `T=.05`, `u=exp(-t)(sin(pi*x)+x)`, Dirichlet `u(0,t)=0`, `u(1,t)=exp(-t)`; backward Euler, forcing at new time.
- Burgers: 20 nodes, `nu=.04`, same time grid, `u=.35+.15*x+.25*exp(-t)*sin(pi*x)`, Dirichlet `.35` and `.50`; explicit old-time centered convection and forcing, implicit diffusion with new-time boundary.
- Poisson: interior grid `10×2`, Dirichlet trace of `sin(pi*x)*sin(2*pi*y)+.15*x+.3*y+.15*x*y`; discrete manufactured `b=A@u_exact` (boundary-load-plus-discrete-source convention).
- Helmholtz: `10×2`, operator `-Delta-9I`, Dirichlet trace of `cos(2*pi*x)*sin(pi*y)+.1*x+.05*y`; discrete manufacture.
- Klein–Gordon: 20 spatial nodes, 40 interleaved `(u,v)` entries, `c=1.1`, `mu=2`, `dt=.001`, `T=.05`; manufactured displacement `cos(1.7t)*(sin(pi*x)+.2*x)` and velocity `-1.7*sin(1.7t)*(sin(pi*x)+.2*x)`; implicit coupled first-order step and corresponding nonzero right Dirichlet traces.

The manufactured functions were **independently inferred** from archived numerical fingerprints; they are not byte-identical original historical source.

## Result and scientific interpretation

The new five-PDE run returns 480 QUBO solves: 120 initial + 360 correction solves. **Every correction decodes to exactly the all-zero 24-bit string.** The unchanged signed fixed-point grid does not resolve further corrections after the initial exact minimizer in these benchmark instances. This baseline is NOT evidence of improvement from residual refinement. The three nominal correction passes add work without changing the cached factors. See the complete per-stage `outputs/figure3_fixed_scale_stage_log.csv` and the companion `figures/figure3_fixed_scale_stages.svg`.

The resulting relative errors and local inverse residuals are in `outputs/figure3_fixed_paper_scales.csv`. `figures/figure3_fixed_paper_scales.svg` and `manuscript/figure3_fixed_plot.csv` are generated solely from the fresh table; `manuscript/FIGURE3_FIXED_SCALE_REVISION.tex` is a replacement Methods/Table 3/Figure 3/Results/Limitations/Conclusion section. Historical GPU precomputation times are NOT reused. Any CPU elapsed seconds are one-run environment-specific diagnostics, not hardware speed measurements.

## Reproduction

From package root (`qpde_schur_qubo_reproducibility`), with root `requirements.txt` installed:

```bash
python experimental_reconstruction/src/figure3_fixed_paper_scales.py
python experimental_reconstruction/src/render_figure3_fixed_scales.py
python experimental_reconstruction/tests/check_figure3_fixed_paper_scales.py
```

The test independently decodes each initial bitstring, checks its equality to the final factor, checks all 360 correction bitstrings are zero, reconstructs the quantized Schur recursion, verifies the classical time-integrator and final right-hand-side residual, and checks the five original system condition numbers. Original historical data are not replaced or used as acceptance targets for new outputs.

## Remaining external validation

The optional `exact_oracle.py` full-bitspace CUDA path is implemented but has **not** been executed on a real GPU in this environment. The numerical ground states here are certified by the independent reduced-grid exact CPU method, not claims of new CUDA timing or fresh Dirac-3 hardware runs.
