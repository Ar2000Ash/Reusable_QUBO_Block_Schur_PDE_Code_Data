# Figure 3 — independently reconstructed replacement, not the original experiment

The five PDE operators, analytic Dirichlet traces, and exact two-scalar oracle are verified separately. Their original fixed-validation `config.json` files record `GAMMA_MODE=auto_bound`, `FIXED_GAMMA`, three correction passes, and the exact-enumeration workload, but **do not record the actual per-column/per-stage `gamma` values or selected bitstrings**. The original CUDA driver is unavailable. Consequently, the historical Table 3/ Figure 3 *values* cannot currently be independently reproduced from their original source protocol.

`src/figure3_scale_audit.py` checks 60 predeclared initial-scale/recursion/shrinkage hypotheses and finds none satisfies the archived full numerical acceptance test. In particular, simply using the paper's block Eq. (22) scale as a fixed correction scale does not reproduce the source.

`src/figure3_refinement_replacement.py` introduces a **different, explicit, reproducible reference experiment** to separate a missing historical policy from any issue in the reconstructed PDE equations, boundaries, or exact optimizer:

1. Build each Schur block from the previously quantized inverse. At stage zero choose `gamma` by paper Eq. (22) on the current block.
2. At each subsequent correction step form `r=e_j-S@y`; solve `S delta=r` *solely to estimate a representable range*, then set `gamma=1.01*||delta||_inf/(2^M-2^(-K))`.
3. Independently minimize `||S P(gamma) z-r||^2` by the exact reduced-grid oracle. **Never substitute** the continuous correction vector for the finite-bit decoded QUBO result. Perform all four exact QUBO calls per column.
4. Solve the actual Heat/Burgers/Klein–Gordon time evolution or discrete-manufactured Poisson/Helmholtz system, retaining the original inferred boundary functions, operator sizes, and parameters. Write results to **`outputs/figure3_independent_replacement.csv`**, not `data/raw/fixed_validation/` or the published processed Figure 3 dataset.

This is deliberately a **strong classical range oracle**. It is suitable for a controlled *replacement protocol* or an ablation, but it is **not** evidence that the original experimental driver selected such scales, and using a continuous small-Schur solve to choose a scale changes the algorithmic cost model. Do not present the output as the paper's historical Table 3.

A CPU run of the independently defined replacement gives relative errors from roughly `6.5e-16` to `2.5e-13` on these small, well-conditioned systems, versus the historical Table 3's errors from roughly `8.8e-6` to `2.95e-2`. This discrepancy is not a boundary-condition failure or a verified error in the historical manuscript: the two experiments use different refinement protocols.

Run:

```bash
cd qpde_schur_qubo_reproducibility
python experimental_reconstruction/tests/check_figure3_refinement_replacement.py
python experimental_reconstruction/src/figure3_refinement_replacement.py
python experimental_reconstruction/src/figure3_scale_audit.py
```

**Historical acceptance remains blocked:** To claim fresh reproduction of the existing paper's Table 3 and Figure 3, recover the precise gamma-selection and refinement stopping/update rule (ideally stage-by-stage logs). Otherwise, replace the original result in a revised manuscript with a clearly labeled independently rerun protocol and regenerate all associated tables/plots; that is a substantive scientific revision, not a source recovery.
