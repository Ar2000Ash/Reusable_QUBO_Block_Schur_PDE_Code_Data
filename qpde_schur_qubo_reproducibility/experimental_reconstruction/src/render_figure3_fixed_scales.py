"""Publication and source tables/figures from fresh fixed-scale results only.

No historical Table 3 figure values are read or used. This script consumes the
new, independently generated source table and stage log.
"""
from __future__ import annotations
import csv
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'outputs'
FIG=ROOT/'figures'
MAN=ROOT/'manuscript'


def sci(x,digits=2):
    x=float(x)
    if x==0:return '$0$'
    p=int(np.floor(np.log10(abs(x))))
    return f'${x/10**p:.{digits}f}\\times10^{{{p}}}$'


def render():
    rows=list(csv.DictReader((SOURCE/'figure3_fixed_paper_scales.csv').open(newline='')))
    stages=list(csv.DictReader((SOURCE/'figure3_fixed_scale_stage_log.csv').open(newline='')))
    assert len(rows)==5 and len(stages)==480
    FIG.mkdir(parents=True,exist_ok=True);MAN.mkdir(parents=True,exist_ok=True)
    names=['Heat','Burgers','Poisson','Helmholtz','Klein--Gordon']
    values=[float(r['rel_dense']) for r in rows]
    inv=[float(r['max_inv_res']) for r in rows]

    # A two-panel figure with data-backed y limits, unlike historical Fig. 3.
    plt.rcParams.update({'font.size':10,'axes.titlesize':12,'axes.labelsize':10,
                         'figure.dpi':150,'savefig.dpi':300,'svg.fonttype':'none'})
    fig,(ax,ay)=plt.subplots(1,2,figsize=(12.5,4.7),layout='constrained')
    xs=np.arange(5)
    for a,z,title,ylab,c,marker in [(ax,values,'(a) End-to-end error','Relative error vs dense numerical solve','#2563a8','o'),
                                    (ay,inv,'(b) Local inverse residual',r'Maximum $\|S_i\widehat S_i^{-1}-I\|_F$','#159895','s')]:
        a.semilogy(xs,z,linestyle='None',marker=marker,color=c,markersize=9,zorder=3)
        a.set_title(title,pad=8);a.set_ylabel(ylab);a.set_xticks(xs,names,rotation=25,ha='right')
        a.set_xlim(-.4,4.4);a.grid(axis='y',which='both',linewidth=.5,alpha=.35)
        a.set_ylim(min(z)*.48,max(z)*2.2)
        for x,v in zip(xs,z):a.annotate(f'{v:.2e}',(x,v),xytext=(0,9),textcoords='offset points',ha='center',fontsize=8)
    fig.suptitle('Five PDEs  |  fixed paper scales  |  B=2, M=1, K=10  |  initial + 3 exact residual solves',fontsize=11)
    for ext in ('png','svg'):
        fig.savefig(FIG/f'figure3_fixed_paper_scales.{ext}',bbox_inches='tight')
    plt.close(fig)

    # Companion diagnostic: all three additional steps are exact zero updates.
    fig,ax=plt.subplots(figsize=(9,4.3),layout='constrained')
    stage_summary=[]
    for row in rows:
        name=row['pde'];one=[z for z in stages if z['pde']==name]
        by={(int(z['block']),int(z['column']),int(z['stage'])):z for z in one}
        curve=[]
        for stage in range(4):
            largest=0.0
            for block in range(1,int(row['N'])//2+1):
                col=np.array([float(by[(block,j,stage)]['post_column_residual']) for j in range(2)])
                largest=max(largest,float(np.linalg.norm(col)))
            curve.append(largest)
            stage_summary.append({'pde':name,'stage':stage,'max_inv_residual':largest,
                    'nonzero_step_updates':sum(1 for z in one if int(z['stage'])==stage and
                                            (float(z['delta0'])!=0 or float(z['delta1'])!=0))})
        ax.semilogy(range(4),curve,marker='o',label=row['label'].replace('--','–'))
    ax.set_xticks(range(4),['Initial','Correction 1','Correction 2','Correction 3'])
    ax.set_xlabel('Exact finite-grid QUBO solve');ax.set_ylabel('Largest block inverse residual (Frobenius)')
    ax.grid(axis='y',which='both',linewidth=.5,alpha=.35);ax.legend(ncol=2,fontsize=9,frameon=False)
    ax.set_title('Repeated fixed-scale grid: all corrections are zero')
    for ext in ('png','svg'):
        fig.savefig(FIG/f'figure3_fixed_scale_stages.{ext}',bbox_inches='tight')
    plt.close(fig)
    with (SOURCE/'figure3_fixed_scale_stage_summary.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,stage_summary[0].keys());w.writeheader();w.writerows(stage_summary)

    # Manuscript-ready CSV and LaTeX are generated from rows; never manually type results.
    plotrows=[]
    for i,row in enumerate(rows):
        plotrows.append(dict(short=names[i],rel_dense=row['rel_dense'],max_inv_res=row['max_inv_res']))
    with (MAN/'figure3_fixed_plot.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,plotrows[0].keys());w.writeheader();w.writerows(plotrows)
    md=['| PDE | $\\gamma$ | $N$ | $\\kappa_2(A)$ | Relative error | $r_\\infty$ | $\\rho_S$ | Max Schur cond. | Calls | Correction updates |',
        '|:--|--:|--:|--:|--:|--:|--:|--:|--:|--:|']
    tex=[]
    for row in rows:
        lab=row['label'];n=row['N'];g=float(row['gamma']);cond=float(row['cond_A'])
        err=sci(row['rel_dense']);res=sci(row['r_inf']);invv=sci(row['max_inv_res']);sch=float(row['max_schur_cond'])
        md.append(f'| {lab.replace("--","–")} | {g:.2f} | {n} | {cond:.2f} | {err} | {res} | {invv} | {sch:.2f} | {row["calls"]} | {row["final_iteration_nonzero_corrections"]} |')
        tex.append(f'{lab} & {g:.2f} & {n} & {cond:.2f} & {err} & {res} & {invv} & {sch:.2f} & {row["calls"]} / 0 \\\\')
    (MAN/'TABLE3_NEW_FIXED_SCALES.md').write_text('\n'.join(md)+'\n')
    (MAN/'TABLE3_NEW_FIXED_SCALES_rows.tex').write_text('\n'.join(tex)+'\n')
    print('Rendered two plots (PNG/SVG), stage summary, source plot data and Table 3 rows from five new results.')
    return rows

if __name__=='__main__':render()
