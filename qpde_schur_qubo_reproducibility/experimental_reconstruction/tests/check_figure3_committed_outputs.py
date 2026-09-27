"""Check committed NEW fixed-gamma CSV + manuscript plot against rerun source.
CPU timing is intentionally excluded: hardware/runtime/environment dependent.
"""
from pathlib import Path
import csv
import sys
import tempfile
import math
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from figure3_fixed_paper_scales import generate
from render_figure3_fixed_scales import render


def get(path):
    with path.open(newline='') as f:return list(csv.DictReader(f))


def run():
    original=get(ROOT/'outputs'/'figure3_fixed_paper_scales.csv')
    stages=get(ROOT/'outputs'/'figure3_fixed_scale_stage_log.csv')
    with tempfile.TemporaryDirectory(prefix='qpde_fig3_fixed_') as td:
        fresh=generate(Path(td))
        copy=get(Path(td)/'figure3_fixed_paper_scales.csv')
        copy_stages=get(Path(td)/'figure3_fixed_scale_stage_log.csv')
    assert len(original)==len(copy)==5
    assert len(stages)==len(copy_stages)==480
    excluded={'precompute_cpu_reduced_seconds'}
    for before,after in zip(original,copy):
        for k in before:
            if k in excluded:continue
            x,y=before[k],after[k]
            try:
                a,b=float(x),float(y)
                assert math.isclose(a,b,rel_tol=3e-11,abs_tol=5e-13),(before['pde'],k,a,b)
            except ValueError:assert x==y,(before['pde'],k,x,y)
    for a,b in zip(stages,copy_stages):
        assert a['pde']==b['pde'] and a['block']==b['block'] and a['column']==b['column'] and a['stage']==b['stage']
        assert a['bitstring']==b['bitstring'] and a['gamma']==b['gamma']
        for key in ('delta0','delta1','energy','post_column_residual'):
            assert math.isclose(float(a[key]),float(b[key]),rel_tol=1e-10,abs_tol=5e-13),(key,a,b)
    plot=get(ROOT/'manuscript'/'figure3_fixed_plot.csv')
    assert len(plot)==5
    for i,(r,p) in enumerate(zip(original,plot)):
        assert float(r['rel_dense'])==float(p['rel_dense'])
        assert float(r['max_inv_res'])==float(p['max_inv_res'])
    assert (ROOT/'manuscript'/'TABLE3_NEW_FIXED_SCALES_rows.tex').read_text().count(' / 0 \\\\')==5
    for filename in ('figure3_fixed_paper_scales.svg','figure3_fixed_scale_stages.svg'):
        f=ROOT/'figures'/filename
        assert f.exists() and '<svg' in f.read_text() and f.stat().st_size>5000
    print('PASS: new committed Figure 3 tables, 480 stage records, five figure-point rows and vector plots agree with fresh source run (CPU times excluded).')

if __name__=='__main__':run()
