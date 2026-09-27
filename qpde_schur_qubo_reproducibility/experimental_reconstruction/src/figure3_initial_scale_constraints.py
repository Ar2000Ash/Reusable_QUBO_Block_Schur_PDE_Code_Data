"""Audit historical Figure 3's initial-scale constraints without fitting any gamma.

The *first* Schur block equals the first diagonal block regardless of whether
subsequent Schur factors use exact or quantized inverses. Every recorded inverse
column solve has a nonnegative squared residual and the archive's max_best_energy
must bound the first-block initial exact finite-grid energy.

This program checks predefined nominal gamma and paper Eq (22) candidates, and
counts multiple mathematically feasible sample scales. It cannot identify the
unrecorded historical scale sequence from aggregate energies alone.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
from exact_oracle import reduced_exact
from experiments import fixed_operator
from figure3_scale_audit import FIXED_GAMMA, dominance_bound
from pde_models import extract_blocks

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT.parent/'data'/'raw'/'fixed_validation'
# Immutable regression fingerprint copied from each archived diagnostics.json;
# CI checks equality to the original files when available.
REFERENCE_MAX_ENERGY={
 'heat_1d':1.0141765742018713e-7,
 'burgers_1d':1.1404527367503242e-7,
 'poisson_2d':1.1043039103854288e-7,
 'helmholtz_2d':1.1565834781090524e-7,
 'klein_gordon_1d':2.0866401496573804e-7,
}

def first_block_minimum_max(S:np.ndarray,gamma:float)->float:
    return max(reduced_exact(S,np.eye(2)[:,j],float(gamma)).residual_squared
               for j in range(2))

def inspect(name:str,scan:int=301):
    target=REFERENCE_MAX_ENERGY[name]
    orig=ARCHIVE/name/'diagnostics.json'
    if orig.exists():
        source=json.loads(orig.read_text())
        recorded=float(source['qubo_stats']['max_best_energy'])
        assert abs(recorded-target)<1e-20, (name,'reference fingerprint changed')
        assert source['qubo_stats']['calls']==(160 if name=='klein_gordon_1d' else 80)
        assert int(source['qubo_stats']['max_bits_seen'])==24
    A,_=fixed_operator(name)
    S=extract_blocks(A)[0][0]
    nominal=FIXED_GAMMA[name]
    eq22=dominance_bound(S)
    nom_e=first_block_minimum_max(S,nominal)
    bound_e=first_block_minimum_max(S,eq22)
    # This is a *necessary condition*, not a fit: first-block energy <= the
    # archived maximum of all completed QUBO calls.
    no_fixed=nom_e>target+1e-15
    no_eq22=bound_e>target+1e-15
    result={'pde':name,'original_max_best_energy':target,'first_schur_block':S.tolist(),
            'nominal_gamma':nominal,'paper_eq22_gamma':eq22,
            'first_block_max_energy_if_nominal':nom_e,
            'first_block_max_energy_if_eq22':bound_e,
            'nominal_first_scale_excluded_by_energy':no_fixed,
            'eq22_first_scale_excluded_by_energy':no_eq22}
    if name in ('poisson_2d','helmholtz_2d'):
        grid=np.geomspace(.0008,.015,scan)
        feasible=[float(g) for g in grid if first_block_minimum_max(S,g)<=target+1e-15]
        result['nonfitting_feasibility_scan']={
            'gamma_scan_low':float(grid[0]),'gamma_scan_high':float(grid[-1]),
            'sample_points':scan,'sampled_feasible_count':len(feasible),
            'minimum_feasible_sample':min(feasible) if feasible else None,
            'maximum_feasible_sample':max(feasible) if feasible else None,
            'conclusion':'Multiple feasible gamma samples: aggregate max energy does not identify gamma'}
    return result

def run():
    data=[inspect(n) for n in FIXED_GAMMA]
    path=ROOT/'outputs'/'figure3_initial_scale_constraints.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps({'source':'archived fixed_validation/<pde>/diagnostics.json; operator independently reconstructed',
        'logical_constraint':'The archive-wide maximum energy upper-bounds the exact first-block initial QUBO energy',
        'scope':'necessary constraints only; no historical gamma inferred',
        'results':data},indent=2)+'\n')
    for x in data:
        print(x['pde'], 'nominal excluded?',x['nominal_first_scale_excluded_by_energy'],
              'Eq22 excluded?',x['eq22_first_scale_excluded_by_energy'],
              'nominal first energy=',x['first_block_max_energy_if_nominal'],
              'archived maximum=',x['original_max_best_energy'])
    assert next(x for x in data if x['pde']=='poisson_2d')['nominal_first_scale_excluded_by_energy']
    assert next(x for x in data if x['pde']=='helmholtz_2d')['nominal_first_scale_excluded_by_energy']
    assert all(x['nonfitting_feasibility_scan']['sampled_feasible_count']>=2
               for x in data if 'nonfitting_feasibility_scan' in x)
    print('PASS: necessary initial-scale constraints confirmed; historical scale remains unidentified')
    print('Wrote',path)
    return data

if __name__=='__main__':run()
