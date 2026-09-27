"""Independent *replacement* refinement protocol; NOT a reproduction of historical Table 3.

This module makes an explicitly specified, source-rerunnable choice where the
unpreserved GAMMA_MODE='auto_bound' per-stage implementation is ambiguous.

Initial scale: paper Eq. (22), based on the current 2x2 Schur block.
Correction scale: reconstruct delta=S^{-1}r only to define representable range,
never to substitute delta for a finite-bit oracle result. With 1% guard, take
  gamma = 1.01 ||delta||_inf / (2^M - 2^{-K}).
Every initial and correction inverse column is obtained by reduced_exact.
The reconstructed Schur chain uses the prior quantized inverse, as verified
independently for Figure 2. Boundary/forcing data are unmodified.

The intentionally separate outputs are NOT used by original Table 3/Figure 3.
They must not be passed off as original experimental measurements.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np

from exact_oracle import reduced_exact
from figure3_scale_audit import FIXED_GAMMA, dominance_bound
from experiments import fixed_operator
from pde_models import extract_blocks, schur_chain, cached_solve, integrate

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT.parent / 'data' / 'raw' / 'fixed_validation'


def run_case(name: str, *, K: int = 10, M: int = 1, guard: float = 1.01):
    """Return new algorithm measurements; no archived figure values enter solve."""
    if name not in FIXED_GAMMA:
        raise ValueError(f'unknown benchmark {name}')
    if guard <= 1 or K < 1 or M < 1:
        raise ValueError('guard >1 and positive integer/fractional bits required')
    A, elliptic = fixed_operator(name)
    D, L, U = extract_blocks(A)
    _, dense_inverse = schur_chain(D, L, U)
    S_list, Y_list, stages = [], [], []
    limit = 2**M - 2**(-K)
    for i, Di in enumerate(D):
        S = Di.copy() if i == 0 else Di - L[i-1] @ Y_list[-1] @ U[i-1]
        inv = np.empty((2, 2))
        for j in range(2):
            target = np.eye(2)[:, j]
            y = np.zeros(2)
            for stage in range(4):
                residual = target - S @ y
                if stage == 0:
                    gamma = dominance_bound(S)
                else:
                    delta_for_range_only = np.linalg.solve(S, residual)
                    gamma = float(np.max(np.abs(delta_for_range_only))) * guard / limit
                    gamma = max(gamma, float(np.finfo(float).tiny))
                result = reduced_exact(S, residual, gamma, M=M, K=K)
                y += np.asarray(result.decoded)
                stages.append({'block': i+1, 'column': j, 'stage': stage,
                               'gamma': gamma, 'bitstring': result.bitstring,
                               'energy': result.residual_squared,
                               'post_residual': float(np.linalg.norm(target-S@y))})
            inv[:, j] = y
        Y_list.append(inv)
        S_list.append(S)
    if elliptic is None:
        quantum = integrate(name, Y_list, A)
        dense = integrate(name, dense_inverse, A)
    else:
        _, rhs, _ = elliptic
        quantum = cached_solve(L, U, Y_list, rhs)
        dense = np.linalg.solve(A, rhs)
    resid = [float(np.linalg.norm(S @ Y - np.eye(2), ord='fro'))
             for S, Y in zip(S_list, Y_list)]
    energies = [r['energy'] for r in stages]
    return {
        'pde': name, 'algorithm': 'INDEPENDENT_REPLACEMENT_NOT_HISTORICAL',
        'initial_scale': 'paper_eq22_current_schur',
        'correction_scale': '1.01*infinity_norm_continuous_correction/positive_grid_endpoint',
        'recursion': 'quantized_schur', 'B': 2, 'M': M, 'K': K,
        'calls': len(stages), 'candidates_accounting': len(stages) * 2**(2*(1+M+K)),
        'rel_dense': float(np.linalg.norm(quantum-dense)/np.linalg.norm(dense)),
        'max_inverse_residual': max(resid),
        'mean_inverse_residual': float(np.mean(resid)),
        'max_energy': max(energies), 'min_energy': min(energies),
        'min_gamma': min(s['gamma'] for s in stages),
        'max_gamma': max(s['gamma'] for s in stages),
        'condition_A': float(np.linalg.cond(A)),
    }


def main():
    out = ROOT/'outputs'/'figure3_independent_replacement.csv'
    out.parent.mkdir(parents=True, exist_ok=True)
    results = [run_case(name) for name in FIXED_GAMMA]
    with out.open('w',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader();writer.writerows(results)
    print('INDEPENDENT REPLACEMENT: archived Table 3 unchanged')
    for rec in results:
        archived_path = RAW/rec['pde']/'diagnostics.json'
        if archived_path.exists():
            archived = json.loads(archived_path.read_text())
            rec['archived_relative_error'] = archived['rel_l2_vs_precise_numeric']
            rec['archived_max_inverse_residual'] = archived['cache_info']['max_inverse_residual']
            rec['archive_match'] = abs(rec['rel_dense']-rec['archived_relative_error'])<1e-11 and abs(rec['max_inverse_residual']-rec['archived_max_inverse_residual'])<1e-11
        print(rec['pde'],'calls=',rec['calls'],'new relative error=',format(rec['rel_dense'],'.8e'),
              'new maximum inverse residual=',format(rec['max_inverse_residual'],'.8e'),
              'historical archive matched?',rec.get('archive_match','unavailable'))
    print('Saved separate replacement table:',out)
    return results


if __name__ == '__main__':
    main()
