"""Diagnostic, not a reproduction: falsify explicit Figure-3 refinement hypotheses.

The historical per-column gamma and correction-grid bitstrings are unavailable.
The design is intentionally predeclared: two Schur topologies, two scale choices,
three correction schedules. Published final data are read only for assessment,
never used to select or update an inverse column.
"""
from __future__ import annotations

import json
from pathlib import Path
import numpy as np
from exact_oracle import reduced_exact
from experiments import fixed_operator
from pde_models import cached_solve, extract_blocks, schur_chain, integrate

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT.parent/'data'/'raw'/'fixed_validation'
FIXED_GAMMA={'heat_1d':0.6,'burgers_1d':0.6,'poisson_2d':0.01,
             'helmholtz_2d':0.01,'klein_gordon_1d':1.0}
NAMES=tuple(FIXED_GAMMA)


def dominance_bound(S):
    """The published Equation (22), applied to one actual Schur block."""
    diag=np.abs(np.diag(S))
    alpha=diag-(np.sum(abs(S),axis=1)-diag)
    if np.min(alpha)>0:
        return 0.5/float(np.min(alpha))
    return 0.5*float(np.linalg.norm(np.linalg.inv(S),ord=np.inf))


def simulate(name, *, topology, gamma_mode, shrink):
    A,ell=fixed_operator(name)
    D,L,U=extract_blocks(A)
    Sref,Yref=schur_chain(D,L,U)
    Slist=[];Ylist=[];E=[];G=[];bitstrings=[]
    for idx,D_i in enumerate(D):
        if idx==0:S=D_i.copy()
        else:S=D_i-L[idx-1]@(Yref[idx-1] if topology=='prepared' else Ylist[-1])@U[idx-1]
        Y=np.zeros((2,2))
        base=FIXED_GAMMA[name] if gamma_mode=='fixed' else min(FIXED_GAMMA[name],dominance_bound(S))
        for col in range(2):
            e=np.eye(2)[:,col];y=np.zeros(2)
            for stage in range(4):
                gamma=base/shrink**stage
                z=reduced_exact(S,e-S@y,gamma,M=1,K=10)
                y+=np.asarray(z.decoded)
                E.append(z.residual_squared);G.append(gamma);bitstrings.append(z.bitstring)
            Y[:,col]=y
        Slist.append(S);Ylist.append(Y)
    residuals=np.asarray([np.linalg.norm(S@Y-np.eye(2),ord='fro') for S,Y in zip(Slist,Ylist)])
    if ell is not None:
        _,rhs,_=ell
        yhat=cached_solve(L,U,Ylist,rhs)
        yref=np.linalg.solve(A,rhs)
    else:
        yhat=integrate(name,Ylist,A)
        yref=integrate(name,Yref,A)
    return {'pde':name,'topology':topology,'gamma_mode':gamma_mode,'shrink':shrink,
            'calls':len(E),'rel_dense':float(np.linalg.norm(yhat-yref)/np.linalg.norm(yref)),
            'max_inv_res':float(np.max(residuals)),'mean_inv_res':float(np.mean(residuals)),
            'max_best_energy':float(np.max(E)),'min_best_energy':float(np.min(E)),
            'min_gamma':float(min(G)),'max_gamma':float(max(G)),
            'condition_A':float(np.linalg.cond(A)),
            'solution':yhat,'bitstrings':bitstrings}


def run_suite():
    hypotheses=[(topology,mode,shrink) for topology in ('prepared','quantized_recursive')
                 for mode in ('fixed','capped_eq22') for shrink in (1,2,8)]
    result=[]
    for name in NAMES:
        orig=json.loads((ARCHIVE/name/'diagnostics.json').read_text())
        target={'rel_dense':orig['rel_l2_vs_precise_numeric'],
                'max_inv_res':orig['cache_info']['max_inverse_residual'],
                'mean_inv_res':orig['cache_info']['mean_inverse_residual'],
                'max_best_energy':orig['qubo_stats']['max_best_energy'],
                'min_best_energy':orig['qubo_stats']['min_best_energy']}
        for topology,mode,shrink in hypotheses:
            z=simulate(name,topology=topology,gamma_mode=mode,shrink=shrink)
            z.pop('solution');z.pop('bitstrings')
            delta={k:abs(z[k]-v) for k,v in target.items()}
            z['archived']=target;z['absolute_differences']=delta
            z['accepted']=all(delta[k]<=1e-11+1e-7*abs(target[k]) for k in target)
            result.append(z)
    return result


if __name__=='__main__':
    rows=run_suite()
    path=ROOT/'outputs'/'figure3_scale_hypotheses.json'
    path.parent.mkdir(parents=True,exist_ok=True)
    summary={'scope':'diagnostic only; archived source is not overwritten',
             'hypotheses_per_pde':12,'pde_count':5,
             'accepted':sum(r['accepted'] for r in rows),
             'remaining_historical_uncertainty':'exact initial and each correction gamma; recursive vs prepared Schur; per-column result log missing',
             'results':rows}
    path.write_text(json.dumps(summary,indent=2)+'\n')
    print('Hypotheses accepted:',summary['accepted'],'/',len(rows))
    for name in NAMES:
        rr=[r for r in rows if r['pde']==name]
        exact=[r for r in rr if r['accepted']]
        print(name,'accepted',len(exact),'/',len(rr),
              'min relative-error deviation',min(abs(r['rel_dense']-r['archived']['rel_dense']) for r in rr),
              'min inverse-residual deviation',min(abs(r['max_inv_res']-r['archived']['max_inv_res']) for r in rr))
    print('Report:',path)
