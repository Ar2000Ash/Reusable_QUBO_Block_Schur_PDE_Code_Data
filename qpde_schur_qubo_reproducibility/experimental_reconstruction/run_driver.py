#!/usr/bin/env python3
"""Reconstruction entry point. Run from root or as python path/to/run_driver.py."""
from __future__ import annotations
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from exact_oracle import reduced_exact,cuda_full_exact
from experiments import benchmark,k_sweep_one
from figure2_exact_reconstruction import all_rows

ARCHIVE=ROOT.parent/'qpde_qci_end_to_end_recovery'/'source'/'preprocessed'/'qci_60qubo_exact_minima_preprocessed_summary.csv'
FIXTURE=ROOT/'fixtures'/'qci_60qubo_exact_minima_preprocessed_summary.csv'
REPO=ROOT.parent/'data'/'raw'/'dirac3'/'reconstructed_60_instances.csv'

def archive_path(specified):
    if specified:return specified
    return REPO if REPO.exists() else ARCHIVE if ARCHIVE.exists() else FIXTURE

def qci(args):
    source=archive_path(args.raw)
    if not source.exists():raise SystemExit('Specify --raw archived reconstructed_60_instances.csv')
    seen=set();out=[]
    for row in csv.DictReader(source.open()):
        id=row['qci_id']; rep=row.get('representative_qci_id') or tuple(row[k] for k in ('S00','S01','S10','S11','gamma','column'))
        if not args.all and id!=args.id:continue
        if args.all and rep in seen:continue
        seen.add(rep)
        S=np.array([[float(row['S00']),float(row['S01'])],[float(row['S10']),float(row['S11'])]])
        target=np.eye(2)[:,int(row['column'])]
        inp=(S,target,float(row['gamma']))
        if args.backend=='cuda':r=cuda_full_exact(*inp,M=int(row['M']),K=int(row['K']),chunk_power=args.chunk_power)
        else:r=reduced_exact(*inp,M=int(row['M']),K=int(row['K']))
        target_bitstring=row['global_min_bitstring'].zfill(int(row['bits']))
        max_diff=abs(r.residual_squared-float(row['global_min_energy']))
        second_diff=abs(r.second_residual_squared-float(row['second_energy']))
        out.append({'qci_id':id,'method':r.method,'n_states':r.examined,'bitstring':r.bitstring,
            'reference_bitstring':target_bitstring,'bitstring_match':r.bitstring==target_bitstring,
            'residual_squared':r.residual_squared,'second_best':r.second_residual_squared,
            'energy_gap':r.second_residual_squared-r.residual_squared,
            'ground_energy_abs_error':max_diff,'second_energy_abs_error':second_diff})
    if not out:raise SystemExit('QCI id not found in raw CSV')
    if args.out:
        args.out.parent.mkdir(parents=True,exist_ok=True)
        with args.out.open('w',newline='') as f:
            wr=csv.DictWriter(f,out[0]);wr.writeheader();wr.writerows(out)
    print(json.dumps({'n_jobs':len(out),'matching_archived_ground_states':sum(x['bitstring_match'] for x in out),
        'max_ground_energy_error':max(x['ground_energy_abs_error'] for x in out),
        'max_second_energy_error':max(x['second_energy_abs_error'] for x in out),
        'backend':args.backend,'records':out if len(out)<=4 else out[:4]},indent=2))
    if any(not x['bitstring_match'] or x['ground_energy_abs_error']>2e-12 or x['second_energy_abs_error']>2e-12 for x in out):
        raise SystemExit('FAILED archived comparison')

def main():
    parser=argparse.ArgumentParser(description=__doc__);sub=parser.add_subparsers(dest='command',required=True)
    qo=sub.add_parser('oracle',help='certify archived QCI minimum and second minimum');qo.add_argument('--raw',type=Path)
    qo.add_argument('--id',default='QCI-001');qo.add_argument('--all',action='store_true');qo.add_argument('--backend',choices=['cpu_reduced','cuda'],default='cpu_reduced');qo.add_argument('--chunk-power',type=int,default=16);qo.add_argument('--out',type=Path)
    bx=sub.add_parser('five-preview',help='candidate Table 3 output (DOES NOT match archive yet)');bx.add_argument('--schedule',choices=['fixed','powers2','powers4','powers10','adaptive'],default='fixed')
    ks=sub.add_parser('sweep-preview',help='accepted Figure 2 sweep output from PDE and exact oracle')
    fig=sub.add_parser('figure2',help='write independently reproduced 14-row Figure 2 table')
    fig.add_argument('--out',type=Path,default=ROOT/'outputs'/'figure2_independent.csv')
    args=parser.parse_args()
    if args.command=='oracle':qci(args)
    elif args.command=='five-preview':
        for n in ['heat_1d','burgers_1d','poisson_2d','helmholtz_2d','klein_gordon_1d']:
            r=benchmark(n,passes=3,schedule=args.schedule)
            print(n,'calls',r['calls'],'rel_dense',r['rel_dense'],'max_inverse_residual',r['max_inverse_residual'])
    elif args.command=='figure2':
        rows=all_rows();columns=list(dict.fromkeys(k for row in rows for k in row))
        args.out.parent.mkdir(parents=True,exist_ok=True)
        with args.out.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
        print('Wrote',len(rows),'independently reconstructed Figure 2 rows:',args.out)
    elif args.command=='sweep-preview':
        for n in ['poisson_2d','klein_gordon_1d']:
            for K in range(4,11):
                r=k_sweep_one(n,K);print(n,K,r['rel_error'],r['mean_inverse_error'],r['mean_energy'])
if __name__=='__main__':main()
