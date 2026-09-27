# Figure 2: independent reconstruction and source-level acceptance

**Status: independently reproduced across all 14 archived sweep rows.** This result
uses the previous quantized Schur inverse to construct the next Schur block. The
original stage-one candidate incorrectly formed every sweep QUBO using *dense*
classical reference Schur blocks and transplanted the fixed-validation boundary
functions into the sweep. Those shortcuts reproduced neither the aggregate
inverse/QUBO data nor the PDE solutions.

## Reconstructed numerical protocol

- Two scalar components per block, `B=2`, one integer magnitude bit and one sign
  bit, `M=1`; fractional precision `K=4,5,6,7,8,9,10`. Exactly
  `2**(2*(K+2))` states for each QUBO, with the independent reduced-grid exact
  CPU oracle providing a mathematical minimizer; full binary-space PyTorch/CUDA
  enumeration is separately implemented but has not yet run on an actual GPU.
- Prepare a *separate classical reference* Schur chain for inverse and residual
  diagnostics. In the quantized experiment set `S[0]=D[0]` and, subsequently,
  `S[i]=D[i]-L[i-1]@Y[i-1]@U[i-1]`, where `Y[i-1]` contains the **finite-bit
  optimized inverse columns of the previous block**. Minimize every local
  `||S[i]@y-e_j||**2` exactly; no residual-refinement stage in Figure 2.
- **Poisson:** `nx=6, ny=2`, `h_x=1/7`, `h_y=1/3`, `gamma=0.01`. A discrete
  manufactured reference field, inferred from archived complete numerical
  fingerprints, is
  `u=(sin(pi*x)+0.2*sin(2*pi*x))*sin(pi*y)`.
  All four Dirichlet traces are **zero**. Construct the manufactured discrete
  right-hand side as `b=A@u` and use the quantized Schur factors in the
  forward/backward solve.
- **Klein--Gordon:** six interior spatial points, `dt=0.015`, `T=0.3`,
  `c=1`, `mu=1.25`, and `gamma=1`. Both components have **zero Dirichlet
  boundary values**. The PDE is unforced, with `u(x,0)=sin(pi*x)` and
  `v(x,0)=0`. The analytic comparison uses
  `omega=sqrt(c*c*pi*pi+mu*mu)` and
  `(u,v)=(sin(pi*x)*cos(omega*t),
  -omega*sin(pi*x)*sin(omega*t))`. The numerical dense reference uses the
  same implicit 20-step discretization and exact classical Schur factors.

These reconstructed source functions are supported by agreement of independent
aggregate diagnostic *columns*, not just a fit to one plotted solution error.
They are not claimed to be byte-for-byte recovered historical source files.
The fixed-validation Table 3 benchmarks have **different** inputs and must not
be overwritten with these Figure 2 fields.

## Reproducibility and acceptance

From `qpde_schur_qubo_reproducibility`:

```bash
python experimental_reconstruction/tests/check_figure2.py
python experimental_reconstruction/run_driver.py sweep-preview
python experimental_reconstruction/run_driver.py figure2 --out experimental_reconstruction/outputs/figure2_independent.csv
```

The source-level test regenerates 14 complete rows from the PDE and exact oracle,
then compares each nonempty numerical field it reconstructs with
`data/raw/k_sweep/k_sweep_results.csv`, and independently compares all six fitted
log2 slopes with `data/raw/k_sweep/convergence_slopes.csv`. Historical elapsed
seconds are machine-dependent and intentionally excluded from acceptance.
The canonical immutable archived tables and published figures are not modified.

The Figure 3 fixed-validation experiment is **still unresolved**. Its original
`GAMMA_MODE=auto_bound` and stage-specific three-pass correction-scale rule are
not reconstructible by blindly reusing Figure 2 settings. The Figure 3 model
and source diagnostics are retained, while unmatched candidate outputs stay
experimental and clearly labeled.
