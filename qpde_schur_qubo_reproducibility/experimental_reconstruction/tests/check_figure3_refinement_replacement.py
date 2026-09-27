"""Test explicitly independent replacement; never change the original raw tables."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from figure3_refinement_replacement import run_case
from figure3_scale_audit import FIXED_GAMMA

REF = {'heat_1d':4.5236039579553765e-5,
       'burgers_1d':8.764191726908332e-6,
       'poisson_2d':1.5853441711359274e-4,
       'helmholtz_2d':1.8759084307613292e-4,
       'klein_gordon_1d':.0295203171584415}

def test():
    rows=[run_case(name) for name in FIXED_GAMMA]
    assert len(rows)==5
    for row in rows:
        assert row['algorithm']=='INDEPENDENT_REPLACEMENT_NOT_HISTORICAL'
        assert row['calls']==(160 if row['pde']=='klein_gordon_1d' else 80)
        assert row['rel_dense']<1e-10,row
        assert row['max_inverse_residual']<1e-11,row
        assert abs(row['rel_dense']-REF[row['pde']])>1e-8,'replacement should not be labeled historical'
    print('PASS: five independently reconstructed PDEs solved with exact finite-bit correction steps; replacement is demonstrably different from historical Table 3.')

if __name__=='__main__':test()
