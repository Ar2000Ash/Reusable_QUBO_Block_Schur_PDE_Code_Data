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
