"""Verify exhaustive torch bit enumeration at small K without CUDA access."""
from pathlib import Path
import sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from exact_oracle import reduced_exact,full_binary_exact

def run():
    try:import torch
    except ImportError:
        print('SKIP: torch not installed; CPU reduced-grid and NumPy brute tests remain available');return
    S=np.array([[1.07056,-.03528],[-.03528,1.07056]])
    for k in range(2,6):
        a=reduced_exact(S,np.array([1.,0.]),.6,K=k)
        b=full_binary_exact(S,np.array([1.,0.]),.6,K=k,chunk_power=11,device='cpu')
        assert a.bitstring==b.bitstring and a.second_bitstring==b.second_bitstring
        assert abs(a.residual_squared-b.residual_squared)<1e-14
        assert abs(a.second_residual_squared-b.second_residual_squared)<1e-14
    print('PASS: torch full bitspace enumerator matches exact reduced-grid minima and second minima for K=2..5 (CPU smoke)')
if __name__=='__main__':run()
