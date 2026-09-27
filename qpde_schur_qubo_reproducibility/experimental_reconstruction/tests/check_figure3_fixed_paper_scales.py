"""Validate NEW fixed nominal-scale experiment against its own specification.

Do not compare new results to the archived auto_bound numerical targets: these
are intentionally distinct methods and should not match historically.
"""
from __future__ import annotations
import csv
import sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from exact_oracle import decode_bits, reduced_exact
from figure3_fixed_paper_scales import (NAMES,GAMMA,M,K,PASSES,B,DT,T,compute,
                                        factorize_fixed,integrate_with_last_rhs,generate)
from experiments import fixed_operator
from pde_models import extract_blocks, manufacture, cached_solve

COND={'heat_1d':1.1394339187575457,'burgers_1d':1.0697444204176292,
      'poisson_2d':26.655602086111447,'helmholtz_2d':50.21037880064371,
      'klein_gordon_1d':6.350787754621465}
EXPECTED_G={'heat_1d':.6,'burgers_1d':.6,'poisson_2d':.01,
            'helmholtz_2d':.01,'klein_gordon_1d':1.0}


def run():
    assert GAMMA==EXPECTED_G and (B,M,K,PASSES,DT,T)==(2,1,10,3,.001,.05)
    total=0;correction_count=0
    for name in NAMES:
        row,sol,dense,records,ss,Y=compute(name)
        A,ell=fixed_operator(name)
        diag,lo,up=extract_blocks(A)
        assert abs(row['cond_A']-COND[name])<1e-10,(name,row['cond_A'])
        assert row['N']==(40 if name=='klein_gordon_1d' else 20)
        assert len(ss)==row['N']//B
        assert row['calls']==(160 if row['N']==40 else 80)
        assert row['theoretical_candidate_product']==row['calls']*2**24
        assert all(x['gamma']==GAMMA[name] for x in records)
        assert all(len(x['bitstring'])==24 for x in records)
        assert all(x['stage'] in (0,1,2,3) for x in records)
        assert row['correction_passes']==3
        assert row['final_iteration_nonzero_corrections']==0,(name,'unexpected correction')
        assert row['max_correction_magnitude']==0
        # Reconstruct columns exclusively from the independently certified
        # *stage-zero bitstrings*. Verify stage 1..3 are all exactly zero.
        f=[]
        for blockno in range(len(ss)):
            reconstructed=np.column_stack([decode_bits(next(x['bitstring'] for x in records
                              if x['block']==blockno+1 and x['column']==j and x['stage']==0),
                              GAMMA[name],M,K) for j in (0,1)])
            np.testing.assert_array_equal(reconstructed,Y[blockno])
            if blockno:
                np.testing.assert_allclose(ss[blockno],diag[blockno]-lo[blockno-1]@f[-1]@up[blockno-1],atol=2e-14)
            f.append(reconstructed)
        for q in records:
            if q['stage']>0:
                correction_count+=1
                assert q['delta0']==0. and q['delta1']==0.,q
                assert q['bitstring']=='0'*24,q
        _,li,ui=extract_blocks(A)
        if ell is not None:
            _,rhs,_=ell
            np.testing.assert_allclose(sol,cached_solve(li,ui,f,rhs),atol=5e-13)
            np.testing.assert_allclose(dense,np.linalg.solve(A,rhs),atol=5e-13)
        else:
            computed,rhs=integrate_with_last_rhs(name,f,A)
            np.testing.assert_allclose(sol,computed,atol=5e-13)
        assert abs(row['r_inf']-max(abs(A@sol-rhs)))<2e-12
        assert row['max_inv_res']==max(float(np.linalg.norm(S@Yi-np.eye(2),'fro')) for S,Yi in zip(ss,Y))
        # Original reference endpoint fingerprints are preserved by unchanged BCs.
        if name=='heat_1d':assert abs(manufacture(name,np.array(1.),t=T)-np.exp(-T))<1e-15
        if name=='burgers_1d':assert manufacture(name,np.array(0.),t=T)==.35
        assert np.isfinite(row['rel_dense']) and row['rel_dense']>0
        total+=len(records)
    assert total==480 and correction_count==360
    print('PASS: 5/5 PDEs, 480 exact CPU QUBO solves, 360/360 exact zero updates; all nominal scales fixed; independently recomputed PDE and boundary checks.')
    return True

if __name__=='__main__':run()
