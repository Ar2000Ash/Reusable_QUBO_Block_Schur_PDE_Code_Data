"""Produce honest archived-vs-reconstructed status; never overwrite originals."""
from __future__ import annotations
import sys,json,csv
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from experiments import benchmark,k_sweep_one

ROOT=Path(__file__).resolve().parents[1]
REF=json.loads((ROOT/'tests/reference_metrics.json').read_text())
OUT=ROOT/'outputs';OUT.mkdir(exist_ok=True)

def compare():
    report={'method':'independent CPU exact oracle; verified Figure 2 quantized Schur recursion; Figure 3 refinement remains candidate',
        'definition':'values reported as match only when independently reproduced to numerical tolerance',
        'fixed':[],'sweep':[]}
    fixedrows=[];sweeprows=[]
    for name,source in REF['five_pde'].items():
        o=benchmark(name,passes=3,schedule='fixed')
        row={'pde':name,'recorded_condition':source['cond_A'],'reconstructed_condition':o['condition_A'],
            'recorded_rel_dense':source['rel_dense'],'reconstructed_rel_dense':o['rel_dense'],
            'recorded_max_inv_res':source['max_inv_res'],'reconstructed_max_inv_res':o['max_inverse_residual'],
            'recorded_calls':source['calls'],'reconstructed_calls':o['calls']}
        row['operator_and_count_pass']=abs(row['recorded_condition']-row['reconstructed_condition'])<1e-10 and row['recorded_calls']==row['reconstructed_calls']
        row['full_results_pass']=abs(row['recorded_rel_dense']-row['reconstructed_rel_dense'])<1e-9 and abs(row['recorded_max_inv_res']-row['reconstructed_max_inv_res'])<1e-9
        fixedrows.append(row)
    for name,source in REF['sweep'].items():
        for k in range(4,11):
            r=k_sweep_one(name,k)
            row={'pde':name,'K':k}
            for key in ('rel_error','mean_inverse_error','mean_energy'):
                row['archived_'+key]=source[key][k-4];row['reconstructed_'+key]=r[key]
                row[key+'_match']=abs(source[key][k-4]-r[key])<1e-10
            sweeprows.append(row)
    report['fixed']=fixedrows;report['sweep']=sweeprows
    report['fixed_exact_match_count']=sum(x['full_results_pass'] for x in fixedrows)
    report['sweep_row_exact_match_count']=sum(all(x[k+'_match'] for k in ('rel_error','mean_inverse_error','mean_energy')) for x in sweeprows)
    report['overall_status']=('FIGURE 2 VERIFIED; FIGURE 3 INCOMPLETE: historical auto_bound/refinement details not yet recovered; do not replace archived Table 3 outputs')
    (OUT/'consistency_report.json').write_text(json.dumps(report,indent=2)+'\n')
    for name,rows in [('fixed_candidate.csv',fixedrows),('k_sweep_candidate.csv',sweeprows)]:
        with (OUT/name).open('w',newline='') as f:
            w=csv.DictWriter(f,rows[0].keys());w.writeheader();w.writerows(rows)
    print('Exact fixed-PDE output matches:',report['fixed_exact_match_count'],'/ 5')
    print('Exact K-sweep complete-row matches:',report['sweep_row_exact_match_count'],'/ 14')
    assert report['sweep_row_exact_match_count']==14, 'Figure 2 independent reproduction regressed'
    print('Wrote outputs/consistency_report.json: unresolved values are NOT asserted as reproduced')
    return report
if __name__=='__main__':compare()
