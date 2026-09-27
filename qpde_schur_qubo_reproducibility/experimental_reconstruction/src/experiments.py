"""Figure 2 and Figure 3 experiment reconstruction.

Scientific provenance: boundary/forcing formulas independently inferred from
archived manufactured fields; see docs/BOUNDARY_AUDIT.md. All exact finite-bit
inversions use reduced_exact, never a dense inverse as a substitute for output.
"""
from __future__ import annotations
import math
import numpy as np
from dataclasses import dataclass
from exact_oracle import reduced_exact
from pde_models import (elliptic_blocks,heat_matrix,kg_matrix,manufacture,extract_blocks,schur_chain,cached_solve,integrate)


def solve_columns(ss:list[np.ndarray],gamma:float,K:int=10,M:int=1,passes:int=0,schedule:str='fixed'):
    out=[];statistics=[]
    for blockno,S in enumerate(ss):
        inv=np.zeros((2,2));stats=[]
        for col in range(2):
            target=np.eye(2)[:,col];y=np.zeros(2)
            for stage in range(passes+1):
                res=target-S@y
                g=correction_gamma(gamma,stage,schedule,S,res)
                sol=reduced_exact(S,res,g,M,K)
                y+=np.array(sol.decoded)
                stats.append({'block':blockno,'column':col,'stage':stage,'gamma':g,
                        'min_energy':sol.residual_squared,'bitstring':sol.bitstring,
                        'residual_after':float(np.linalg.norm(S@y-target))})
            inv[:,col]=y
        out.append(inv);statistics.extend(stats)
    return out,statistics


def correction_gamma(gamma:float,pass_index:int,schedule:str,S:np.ndarray,residual:np.ndarray)->float:
    if schedule=='fixed':return gamma
    if schedule=='powers10':return gamma/10**pass_index
    if schedule=='powers2':return gamma/2**pass_index
    if schedule=='powers4':return gamma/4**pass_index
    if schedule=='adaptive':
        if pass_index==0:return gamma
        # Reduced gamma chosen to represent the correction without clipping.
        delta=np.linalg.solve(S,residual)
        return max(1e-14,max(abs(delta))*0.6)
    raise KeyError(schedule)


def fixed_operator(name:str):
    if name=='heat_1d':A,*_=heat_matrix(20,nu=.08);return A,None
    if name=='burgers_1d':A,*_=heat_matrix(20,nu=.04);return A,None
    if name=='klein_gordon_1d':A,*_=kg_matrix(20,.001,1.1,2.);return A,None
    if name in ('poisson_2d','helmholtz_2d'):
        d,l,u,A,exact,b,bc=elliptic_blocks(name,10,2);return A,(exact,b,bc)
    raise KeyError(name)


def benchmark(name:str,K:int=10,passes:int=3,schedule:str='fixed',gamma:float|None=None):
    default_g={'heat_1d':.6,'burgers_1d':.6,'poisson_2d':.01,'helmholtz_2d':.01,'klein_gordon_1d':1.}
    gamma=default_g[name] if gamma is None else gamma
    A,ell=fixed_operator(name);d,l,u=extract_blocks(A)
    ss,dense_inv=schur_chain(d,l,u)
    approx,stats=solve_columns(ss,gamma,K=K,passes=passes,schedule=schedule)
    if ell is None:
        x=integrate(name,approx,A);reference=integrate(name,dense_inv,A)
        grid=np.arange(1,21)/21
        if name=='klein_gordon_1d':exact=np.stack((manufacture('kg_u',grid,t=.05),manufacture('kg_v',grid,t=.05)),axis=1).ravel()
        else:exact=manufacture(name,grid,t=.05)
    else:
        exact,b,bc=ell;x=cached_solve(l,u,approx,b);reference=np.linalg.solve(A,b)
    residual=float(np.linalg.norm(A@x-b,np.inf)) if ell is not None else None
    max_inv=float(max(np.linalg.norm(S@Y-np.eye(2),ord='fro') for S,Y in zip(ss,approx)))
    mean_inv=float(np.mean([np.linalg.norm(S@Y-np.eye(2),ord='fro') for S,Y in zip(ss,approx)]))
    return {'pde':name,'K':K,'gamma':gamma,'passes':passes,'schedule':schedule,
        'rel_dense':float(np.linalg.norm(x-reference)/np.linalg.norm(reference)),
        'rel_exact':float(np.linalg.norm(x-exact)/np.linalg.norm(exact)),
        'max_inverse_residual':max_inv,'mean_inverse_residual':mean_inv,'max_schur_cond':float(max(np.linalg.cond(S) for S in ss)),
        'condition_A':float(np.linalg.cond(A)),'calls':len(stats),'bits':2*(K+2),
        'candidates_accounting':len(stats)*2**(2*(K+2)),
        'mean_qubo_energy':float(np.mean([v['min_energy'] for v in stats])),
        'max_qubo_energy':float(np.max([v['min_energy'] for v in stats])),
        'final_solution':x,'dense_solution':reference,'exact_field':exact,'stats':stats}



def k_sweep_one(name:str,K:int):
    """Verified Figure 2 sweep using the quantized recursive Schur chain.

    The original candidate used the *dense* Schur chain to build all local
    QUBOs and imported the fixed-validation boundary data into the sweep.
    Both are contradicted by the archived numerical fingerprints. See
    figure2_exact_reconstruction and tests/check_figure2.py.
    """
    from figure2_exact_reconstruction import run_one
    row=run_one(name,K)
    row['rel_error']=(row['rel_l2_vs_discrete_exact'] if name=='poisson_2d'
                      else row['rel_l2_vs_dense_final'])
    row['mean_inverse_error']=row['mean_inv_fro_error']
    row['mean_energy']=row['mean_qubo_energy']
    row['max_energy']=row['max_qubo_energy']
    row['solves']=row['num_qubo_column_solves']
    row['condition_A']=float(np.linalg.cond(fixed_operator(name)[0])) if name not in ('klein_gordon_1d','poisson_2d') else None
    return row
