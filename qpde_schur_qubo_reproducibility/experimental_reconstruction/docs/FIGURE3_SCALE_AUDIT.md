# Figure 3: independent refinement-protocol audit (open)

The five PDE definitions, inhomogeneous Dirichlet boundary traces, conditions,
and exact two-scalar oracle are independently tested. The original Table 3
configuration records `GAMMA_MODE="auto_bound"`, the nominal `FIXED_GAMMA`,
three residual-refinement steps, and aggregate energy/residual diagnostics. It
does not record the per-column, per-stage scale or correction bitstrings.

`src/figure3_scale_audit.py` tests **60 explicitly declared hypotheses**: five
PDEs, prepared-reference versus recursively quantized Schur blocks, nominal
fixed scale versus the minimum of nominal and Equation (22) bound, and scales
held constant versus divided by 2 or 8 at each correction stage. It performs
one initial and three correction QUBO solves with the independent exact CPU
oracle, assembles cached inverse blocks, and recomputes final PDE solutions.
It checks both the original solution error and the local residual/energy
aggregates, rather than declaring success from a similar plotted error.

On the archived numeric targets, **0 of 60 hypotheses reproduces all five
metrics** within the declared tolerance. This falsifies the tested schedules;
it does not prove that the paper used an erroneous schedule, nor does it
identify the unique missing implementation. `tests/reference_metrics.json` is
only a reference for accepted numerical comparisons; the authoritative
`data/raw/fixed_validation/<pde>/diagnostics.json` remains untouched.

Run from the main package directory:

```bash
python experimental_reconstruction/src/figure3_scale_audit.py
```

The candidate JSON report is written under `experimental_reconstruction/outputs/`.
The canonical Figure 3, Table 3, and underlying archived data are unchanged.

The next necessary source-level evidence would be an original per-stage gamma
formula, saved 80/160 job bitstrings, or a recoverable history of the original
`auto_bound` driver. New experiments can also establish an independently
reproducible **replacement protocol** with a distinct result table; matching
one or two aggregate metrics is insufficient to call it the original protocol.

The CUDA implementation in `src/exact_oracle.py` is still untested on a real CUDA
device; run `python experimental_reconstruction/run_driver.py oracle --id QCI-001 --backend cuda --chunk-power 16` first on a CUDA-equipped machine.

## Stronger necessary-condition audit

[`src/figure3_initial_scale_constraints.py`](../src/figure3_initial_scale_constraints.py) independently minimizes the *first* inverse-column QUBOs, which are independent of any later Schur recursion. The archived global maximum of all solved QUBO energies must be at least this first-block minimum. That condition excludes the nominal `FIXED_GAMMA=0.01` as the actual first-block initial scale for both Poisson and Helmholtz. Direct unmodified Equation (22) scale is also excluded for Poisson (and for Klein–Gordon under its inverse-norm fallback), under the archived energy definition. The numeric feasibility scan shows multiple admissible gamma samples, so the recorded maximum does **not** uniquely recover the historical scale. No fitting or retroactive editing of data is involved.

The separate [replacement experiment](FIGURE3_REFINEMENT_REPLACEMENT.md) chooses a continuous residual correction *only to set the representable range* and uses the finite-bit exact oracle for every actual column update. It reaches a very different accuracy regime, illustrating that a plausible `auto_bound` interpretation cannot be assumed to reproduce Table 3. Its additional classical range solve changes the cost model and is explicitly **not** the historical experiment.
