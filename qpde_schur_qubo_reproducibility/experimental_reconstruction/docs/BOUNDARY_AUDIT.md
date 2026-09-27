# Reconstruction audit: five benchmark PDEs and boundary conditions

**Provenance distinction.** These functions are independently reconstructed by matching the paper's PDE *type*, supplied raw manufactured/reference vectors, fixed operator conditioning, continuous/discrete truncation residuals, and precise time-integration endpoints. The paper and `config.json` records do **not** spell out every original function. No original source code is claimed to have been recovered. A function that reproduces a final manufactured field is not logically the unique possible historical function; see the acceptance status.

For fixed validation, the common settings are `B=2, M=1, K=10`, 3 residual-correction solves per initial inverse-column solve, `dt=0.001`, and `T=0.05`. The old config's `GAMMA_MODE="auto_bound"` is **not yet reconstructed exactly**. Its `FIXED_GAMMA` entries are 0.6 (Heat/Burgers), 0.01 (Poisson/Helmholtz), and 1.0 (Klein–Gordon). Therefore the fresh Table 3 candidate metrics are *not* claimed to match the archive.

| PDE | Inferred manufactured solution | Dirichlet trace | Operator and time treatment | Independent fingerprint |
|---|---|---|---|---|
| Heat | `exp(-t)*(sin(pi*x)+x)` | `u(0,t)=0`, `u(1,t)=exp(-t)` | `u_t=0.08*u_xx+f`; backward Euler with new-time forcing and boundary | matrix cond 1.1394339187575457; archived precise first and last reconstructed |
| Burgers | `0.35+0.15*x+0.25*exp(-t)*sin(pi*x)` | `u(0,t)=0.35`, `u(1,t)=0.5` | `u_t + u*u_x=0.04*u_xx+f`, old-time centered advective difference; backward Euler for diffusion; old-time forcing, new-time fixed boundary | matrix cond 1.0697444204176292; archived precise first and last reconstructed |
| Klein–Gordon | `u=cos(1.7*t)*(sin(pi*x)+0.2*x)`, `v=-1.7*sin(1.7*t)*(sin(pi*x)+0.2*x)` | `u(0,t)=v(0,t)=0`, `u(1,t)=0.2*cos(1.7*t)`, `v(1,t)=-0.34*sin(1.7*t)` | `u_t=v`, `v_t=1.1^2*u_xx-2^2*u+f`, new-time implicit coupled 2x2 interleaved state | matrix cond 6.350787754621465; max Schur cond 2.785090451255385; archived precise first u/v |
| Poisson 2D | `sin(pi*x)*sin(2*pi*y)+0.15*x+0.3*y+0.15*x*y` | analytic trace at all four sides; **nonzero generally** | `-Delta` on `10x2`, `hx=1/11`, `hy=1/3`, recorded discrete manufacture `b=A@u_exact` | cond 26.655602086111447; continuous/discrete max residual 10.753981592795974 |
| Helmholtz 2D | `cos(2*pi*x)*sin(pi*y)+0.1*x+0.05*y` | analytic trace; **nonzero generally** | `-Delta-9I` on `10x2`, `hx=1/11`, `hy=1/3`; discrete manufactured RHS | cond 50.21037880064371; continuous/discrete max residual 1.6048685801218667 |

The 2D discrete manufactured convention can be written `f_discrete=A@u_exact-boundary_load`, and the assembled right-hand side is `f_discrete+boundary_load=A@u_exact`. This is **not** equivalent to claiming the sampled continuous differential forcing alone generated the archived fixed-validation RHS. A separate diagnostic confirms the corresponding continuous-vs-discrete truncation residual. Boundary loads are positive multiples of `g` associated with off-diagonal `-h^-2` stencil entries.

**Figure 2 has now been independently reconstructed and numerically accepted.**
The prior note below is superseded by `docs/FIGURE2_RECONSTRUCTION.md`.
The Poisson sweep (6×2 grid) uses **zero Dirichlet traces** and the discrete
manufactured field `(sin(pi*x)+0.2*sin(2*pi*x))*sin(pi*y)`. The six-point,
20-step Klein–Gordon sweep uses zero Dirichlet traces and **no forcing**,
with initial `u=sin(pi*x), v=0` and analytic angular frequency
`sqrt(pi*pi+1.25*1.25)`. The exact sweep QUBO objectives use the *previous
quantized inverse* to form the next Schur block; classical Schur inverses
remain separate reference data for diagnostic errors. The recovered code
reproduces all fourteen archived numerical rows, including the six fitted
slopes, using independent exact finite-bit minimization. This sweep protocol
must not be substituted for the five fixed-validation experiments.

**Figure 3 residual refinement remains unresolved.** The historical config has `GAMMA_MODE=auto_bound`, a `FIXED_GAMMA` parameter and 3 residual-refinement stages. Neither its exact scale-selection rule nor its per-stage correction scale is in the archived source. Holding gamma constant or choosing ad-hoc reduction schedules fails Table 3 acceptance. In particular, matching a convergence slope or a single final error would be insufficient; every benchmark's relative field error, cached inverse residual, and solve count must match.
