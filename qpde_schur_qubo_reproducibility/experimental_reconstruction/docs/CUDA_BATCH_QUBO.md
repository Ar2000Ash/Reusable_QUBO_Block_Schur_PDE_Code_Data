# Sequential CUDA QUBO array solver (new, independent utility)

`src/batch_qubo_cuda.py` accepts a NumPy array of shape `(jobs, n, n)` or an iterable of square NumPy matrices (possibly with different sizes). It solves the QUBOs **one at a time** on one CUDA GPU, preserving the input order and returning a bitstring and objective for every job. It does not change any PDE model, Figure 2/3 protocol, or archived output.

The convention is **`E(x) = x.T @ Q @ x`**, `x` binary. Diagonal coefficients are linear terms because `x_i**2 = x_i`. An upper-triangular matrix supplies each pair coefficient once; if the matrix is symmetric, its off-diagonal coefficients contribute twice. There is no implicit QUBO normalization or sign reversal.

```python
import numpy as np
from batch_qubo_cuda import solve_qubos_cuda

qubos = np.array([
    [[-1.0,  0.5], [0.0,  0.2]],
    [[ 0.0, -2.0], [0.0,  1.0]],
], dtype=np.float64)
results = solve_qubos_cuda(qubos, chunk_power=16, prefix_batch=32)
for r in results:
    print(r.bitstring, r.energy, r.states_evaluated, r.elapsed_seconds)
```

Import from the repository's reconstruction source directory (`PYTHONPATH=experimental_reconstruction/src` when running from the package root) or add that directory to `sys.path`. `solve_qubos(qubos, device='cpu', ...)` offers a small-problem verification backend. Install a CUDA-enabled PyTorch build matching the host CUDA/driver; the root `requirements.txt` intentionally does not force a CUDA wheel. A missing CUDA device raises an error; no automatic CPU fallback occurs.

The search is exhaustive **enumeration of all binary configurations** under float64 arithmetic: the solver partitions each bitstring into a reusable suffix and a streamed prefix, evaluates the algebraically equivalent quadratic objective for each pair, and retains only the best energy and index on the GPU. The same suffix bit table is reused for consecutive jobs of the same size. `prefix_batch` controls the transient GPU score buffer; `chunk_power` controls the suffix table. Defaults are 16 suffix bits and 32 prefixes at a time. This bounds memory independently of the number of QUBOs and avoids transferring per-chunk candidate scores to the CPU. Ties choose the smallest index (most-significant bit first).

Default `max_bits=24` is a guard, not a claim that 24-bit exhaustive search is fast on every GPU. Each 24-bit job covers `2**24 = 16,777,216` *logical states*, not measured threads or GPU throughput. More than 24 bits requires an explicit larger `max_bits` (at most 30), and exhaustive runtime grows exponentially. The reported duration includes upload and synchronization; it is not evidence of historical hardware timing. This general matrix solver does not exploit the special rank-two least-squares structure of the separate `exact_oracle.py` Schur-column routines. Near-degenerate float64 ties require additional precision to serve as rigorous mathematical certificates.

Verification:

```bash
python experimental_reconstruction/tests/check_batch_qubo_cuda.py
```

The test independently enumerates random, upper-triangular, full, tied and mixed-sized QUBOs on CPU, and runs the same comparisons on CUDA only when an actual GPU is available. The device-dependent path has not been validated unless that second test completes on the target GPU.
