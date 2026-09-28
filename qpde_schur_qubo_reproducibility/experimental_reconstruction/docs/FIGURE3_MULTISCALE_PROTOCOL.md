# Five-PDE Figure 3: predetermined geometric multiscale residual refinement

**Status:** Fresh, source-reproducible numerical experiment. This is not recovery of the original historical `auto_bound` driver, nor a retrospective change to the archived Figure 3 / Table 3 inputs. It supersedes the *new fixed-grid* experiment as the recommended revised-manuscript Figure 3; the fixed-grid outputs are retained as an explicit ablation.

## PDE and mathematical formulation

The discretizations, manufactured/continuous forcing, initial data, nonhomogeneous Dirichlet traces, interleaved Klein–Gordon state, end time, and matrix ordering are exactly the same independently reconstructed five-PDE models in `src/pde_models.py` and `docs/BOUNDARY_AUDIT.md`. In particular, no boundary value or RHS was tuned to the output. The local QUBO remains a 24-bit signed fixed-point least-squares objective

\[
    z_p^* \in \arg\min_{z\in\{0,1\}^{24}}
       \|S_i P(\gamma_p)z-r_p\|_2^2,
    \quad r_p=e_j-S_i y_p,\quad y_{p+1}=y_p+P(\gamma_p)z_p^*.
\]

Use `B=2`, `M=1`, `K=10`, one initial solve and exactly three correction solves for **every** inverse column, with the initial *paper* scale `gamma0=0.60` for Heat/Burgers, `0.01` for Poisson/Helmholtz, and `1.00` for Klein–Gordon. The sole protocol change relative to the fixed-grid baseline is a **predeclared, nonadaptive** scale schedule:

\[
    \gamma_p=\gamma_0/8^p,\quad p=0,1,2,3.
\]

For instance Klein–Gordon uses `[1, 0.125, 0.015625, 0.001953125]`; the other schedules are exactly the same four multipliers times their fixed initial gamma. No classical inverse or continuous correction is used to propose the QUBO answer or select the scale. A continuous `np.linalg.solve(S, r)` is invoked **only after the scale has been decided**, for a diagnostic that checks whether the exact continuous correction is inside the finite grid. The binary oracle itself uses the independent two-scalar conditional convex search in `src/exact_oracle.py` and returns a decoded 24-bit minimizer. Schur blocks are recursively formed using the previously cached **quantized** inverse. The approximate inverse columns are used as such in the final block solve.

The same original PDE time steps `dt=0.001`, `T=0.05`, operator sizes 20 (Heat/Burgers/elliptic) and 40 (Klein–Gordon), and unchanged manufactured/Dirichlet data are retained. Elliptic reference uses discrete-manufactured `b=A@u_exact`, so the dense numerical field is the manufactured discrete field; for transient tests dense numerical and continuous analytical references are distinct. The residual of a final transient algebraic system uses the **actual last-step approximate right-hand side** rather than an unrelated endpoint field.

## Reproducibility and cost accounting

- `python experimental_reconstruction/src/figure3_multiscale.py` regenerates the five-PDE table, the complete 480-call/per-stage 24-bit decoded log, and 120 field-value rows.
- `python experimental_reconstruction/src/render_figure3_multiscale.py` regenerates the new Figure 3 (with fixed-grid control), a four-stage Schur residual plot, a six-panel solution-vs-ground-truth plot, the data for a paper pgfplots figure, and LaTeX/Markdown tables, including the separate Klein–Gordon displacement and velocity errors.
- `python experimental_reconstruction/tests/check_figure3_multiscale.py` tests the stated hyperparameters, every bitstring/gamma, every QUBO residual objective, all source fields, the updated Schur chain and absence of continuous-correction clipping.
- `python experimental_reconstruction/tests/check_figure3_multiscale_outputs.py` reruns all five PDEs and checks the committed numerical CSVs against new source outputs.

The exact reduced-grid CPU oracle is **not** full CUDA enumeration. The reported `logical_states_per_call = 2^24` is a problem-space size and `logical_state_space_accounting = calls * 2^24` is *not a measurement of states visited or GPU throughput*. The CPU timing is environment-specific and is not comparable to historical GPU or QCI device timings. On the new fixed schedule there are 80 QUBO calls each for Heat, Burgers, Poisson and Helmholtz and 160 for Klein–Gordon (480 total). The 360 residual-correction calls all produce nonzero updates, and 0 of 480 audit-stage continuous corrections is out of representable range in the tested systems. The numerical evidence concerns these systems, not a universal no-clipping theorem or hardware coefficient-precision guarantee.

## Manuscript implications

Replace the *five-PDE part* of the methods and the **new** Figure 3 / Table 3 with `manuscript/FIGURE3_MULTISCALE_REVISION.tex` and `manuscript/figure3_multiscale_plot.csv`. Do not edit archived historical source results in `data/raw/fixed_validation/`. Preserve Figure 2, the large-block/96-bit studies and the archived hardware Figures 6–7: they intentionally test different protocols. Do not attribute the improved multiscale results to the original QCI Dirac-3 jobs. State that the new scale schedule is predetermined rather than the lost historical `auto_bound` method, and that the existing fixed-grid baseline stagnated because repeated optimization on the same lattice returned zero corrections. The original fixed-K no-clipping error bounds remain applicable under their assumptions; no new global multiscale convergence theorem is claimed.
