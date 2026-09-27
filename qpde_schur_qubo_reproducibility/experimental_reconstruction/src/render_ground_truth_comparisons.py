"""Reproducible fixed-paper-scale QPDE solution vs ground-truth plot generator.

Loads the *new* field values from outputs/figure3_fixed_scale_fields.csv and
computes independently reconstructed manufactured/analytical reference values
from src/pde_models.py.  Dense numerical fields in the CSV are from a classical
solve of the same discretization.  It does not read historical auto_bound data.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from pde_models import manufacture

DATA = ROOT / 'outputs' / 'figure3_fixed_scale_fields.csv'
OUT = ROOT / 'figures' / 'ground_truth'
DISPLAY = {'heat_1d':'Heat 1D', 'burgers_1d':'Burgers 1D',
           'poisson_2d':'Poisson 2D', 'helmholtz_2d':'Helmholtz 2D',
           'klein_gordon_1d':'Klein–Gordon 1D'}
T = 0.05


def source_arrays():
    raw = list(csv.DictReader(DATA.open(newline='', encoding='utf8')))
    by = {name: [] for name in DISPLAY}
    for r in raw:
        by[r['pde']].append(r)
    if any(len(by[x]) != (40 if x == 'klein_gordon_1d' else 20) for x in by):
        raise AssertionError('incomplete source fields')
    result = {}
    for name, recs in by.items():
        recs.sort(key=lambda x: int(x['component_index']))
        for i, rec in enumerate(recs):
            assert int(rec['component_index']) == i
        fixed = np.array([float(r['new_fixed_scale']) for r in recs])
        dense = np.array([float(r['dense_numerical']) for r in recs])
        if name in ('heat_1d','burgers_1d'):
            xx = np.arange(1,21)/21
            manufactured = manufacture(name, xx, t=T)
        elif name in ('poisson_2d','helmholtz_2d'):
            coords = np.array([(i/11, j/3) for i in range(1,11) for j in range(1,3)])
            manufactured = manufacture(name, coords[:,0], coords[:,1])
        else:
            xx = np.arange(1,21)/21
            manufactured = np.stack((manufacture('kg_u',xx,t=T),
                                     manufacture('kg_v',xx,t=T)),axis=1).ravel()
        assert len(fixed) == len(dense) == len(manufactured)
        if name in ('poisson_2d','helmholtz_2d'):
            assert np.max(np.abs(dense-manufactured)) < 1e-12, name
        result[name] = (fixed, dense, manufactured)
    return result


def export(fig, filename: str):
    OUT.mkdir(parents=True,exist_ok=True)
    fig.savefig(OUT/f'{filename}.png', dpi=220, bbox_inches='tight')
    fig.savefig(OUT/f'{filename}.svg', bbox_inches='tight')
    plt.close(fig)


def one_dim(name, fixed, dense, analytical):
    x=np.arange(1,21)/21
    fig,ax=plt.subplots(figsize=(8.4,4.7))
    ax.plot(x, analytical, ':', linewidth=2.0, label='Manufactured analytical field')
    ax.plot(x, dense, '-', linewidth=2.0, label='Dense numerical reference')
    ax.plot(x, fixed, '--o', linewidth=1.35, markersize=3.8, label='New fixed-scale QUBO factors')
    ax.set(xlabel='Spatial coordinate x',ylabel='u(x,T)',title=f'{DISPLAY[name]} | T = {T:g}')
    ax.grid(alpha=.23)
    ax.legend(loc='best',fontsize=9)
    export(fig,f'{name}_vs_ground_truth')
    error_graph(name,np.arange(1,21),fixed,dense,analytical,'Grid index',f'{DISPLAY[name]} | error at T={T:g}')


def elliptic(name, fixed, dense, analytical):
    x=np.arange(1,11)/11
    fig,ax=plt.subplots(figsize=(8.4,4.7))
    for j, y in enumerate((1/3,2/3)):
        ax.plot(x,dense[j::2],linewidth=2.0,linestyle=('-' if j==0 else ':'),label=f'Dense = manufactured | y={y:.3f}')
        ax.plot(x,fixed[j::2],linestyle='--',marker=('o' if j==0 else 's'),
                markersize=4.0,linewidth=1.4,label=f'New fixed-scale QUBO | y={y:.3f}')
    ax.set(xlabel='Spatial coordinate x',ylabel='u(x,y)',title=f'{DISPLAY[name]} | 10 × 2 interior grid')
    ax.grid(alpha=.23)
    ax.legend(loc='best',fontsize=8.5)
    export(fig,f'{name}_vs_ground_truth')
    error_graph(name,np.arange(1,21),fixed,dense,analytical,'Flattened grid index (x-major, y-fast)',f'{DISPLAY[name]} | pointwise error')


def kg_component(component, fixed, dense, analytical):
    name=f'klein_gordon_{component}'
    index = 0 if component == 'u' else 1
    x=np.arange(1,21)/21
    f=fixed[index::2];d=dense[index::2];a=analytical[index::2]
    fig,ax=plt.subplots(figsize=(8.4,4.7))
    ax.plot(x,a,':',linewidth=2.0,label='Manufactured analytical field')
    ax.plot(x,d,'-',linewidth=2.0,label='Dense numerical reference')
    ax.plot(x,f,'--o',linewidth=1.35,markersize=3.8,label='New fixed-scale QUBO factors')
    ax.set(xlabel='Spatial coordinate x',ylabel=f'{component}(x,T)',title=f'Klein–Gordon | {"displacement u" if component=="u" else "velocity v"} | T={T:g}')
    ax.grid(alpha=.23)
    ax.legend(loc='best',fontsize=9)
    export(fig,f'{name}_vs_ground_truth')
    error_graph(name,np.arange(1,21),f,d,a,'Spatial index',f'Klein–Gordon {component} | pointwise error')


def error_graph(name, x, fixed, dense, analytical, xlabel, title):
    fig,ax=plt.subplots(figsize=(8.4,4.2))
    ax.plot(x,np.abs(fixed-dense),'-o',markersize=3.3,label='|QUBO − dense|')
    if name not in ('poisson_2d','helmholtz_2d'):
        ax.plot(x,np.abs(dense-analytical),'--',label='|Dense − analytical|')
        ax.plot(x,np.abs(fixed-analytical),':',label='|QUBO − analytical|')
    ax.set(xlabel=xlabel,ylabel='Absolute pointwise error',title=title)
    ax.grid(alpha=.23)
    ax.legend(fontsize=9)
    export(fig,f'{name}_pointwise_errors')


def main():
    sets=source_arrays()
    metrics=[]
    for name,(fixed,dense,analytic) in sets.items():
        r={'pde':name, 'num_entries':len(fixed),
           'rel_l2_vs_dense':float(np.linalg.norm(fixed-dense)/np.linalg.norm(dense)),
           'max_abs_error_vs_dense':float(np.max(np.abs(fixed-dense))),
           'rel_l2_dense_vs_manufactured':float(np.linalg.norm(dense-analytic)/np.linalg.norm(analytic)),
           'rel_l2_qubo_vs_manufactured':float(np.linalg.norm(fixed-analytic)/np.linalg.norm(analytic))}
        if name=='klein_gordon_1d':
            for j,label in ((0,'u'),(1,'v')):
                f,d,a=fixed[j::2],dense[j::2],analytic[j::2]
                r[f'{label}_rel_l2_vs_dense']=float(np.linalg.norm(f-d)/np.linalg.norm(d))
            kg_component('u',fixed,dense,analytic)
            kg_component('v',fixed,dense,analytic)
        elif name in ('poisson_2d','helmholtz_2d'):
            elliptic(name,fixed,dense,analytic)
        else:
            one_dim(name,fixed,dense,analytic)
        metrics.append(r)
    summary={'scope':'new fixed-paper-scale benchmark, not historical auto_bound data',
             'ground_truth':'dense discrete reference; manufactured continuous field shown separately',
             'metrics':metrics,
             'plots':[p.name for p in sorted(OUT.glob('*.png'))]}
    (OUT/'comparison_metrics.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))
    # Original new Table 3 numbers are recomputed directly from saved fields.
    records=list(csv.DictReader((ROOT/'outputs'/'figure3_fixed_paper_scales.csv').open(newline='')))
    table={r['pde']:r for r in records}
    for r in metrics:
        assert abs(r['rel_l2_vs_dense']-float(table[r['pde']]['rel_dense']))<3e-14, r['pde']
    print('PASS: all five field-based relative errors agree with new Figure 3 table')

if __name__=='__main__':main()
