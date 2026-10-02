"""Worked, observational analysis of published Finnish field records."""
import csv
import hashlib
import json
import math
import random
from pathlib import Path
from statistics import mean, median
from .pipeline import write_csv

FIELDS = ('WT_ES', 'WT_MS', 'pH', 'EC', 'ABS', 'N', 'P', 'DOC')
MISSING = {'', 'na', 'nan', 'null', '-9999'}


def table(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f, delimiter=';'))


def numeric(value):
    if value is None or value.strip().lower() in MISSING:
        return None
    n = float(value)
    if not math.isfinite(n):
        raise ValueError('Nonfinite field value')
    return n


def join_records(directory):
    directory = Path(directory)
    sites = table(directory/'sites_data.csv')
    if len({s['ID'] for s in sites}) != len(sites):
        raise ValueError('Duplicate site ID')
    catalogue = {s['ID']: s for s in sites}
    hydrology = table(directory/'hydrological_data.csv')
    vegetation = table(directory/'species_groups_data.csv')
    def index(rows):
        indexed = {}
        for row in rows:
            key = row['ID'], row['Time']
            if key in indexed:
                raise ValueError('Duplicate ID/Time')
            if row['ID'] not in catalogue:
                raise ValueError('Unknown field site')
            if row['Time'] not in ('0', '2', '5', '10'):
                raise ValueError('Unexpected sampling time')
            indexed[key] = row
        return indexed
    h, v = index(hydrology), index(vegetation)
    if set(h) != set(v):
        raise ValueError('Hydrology/vegetation key mismatch')
    joined = []
    missing = {k: 0 for k in FIELDS}
    for key in sorted(h, key=lambda k: (int(k[0]), int(k[1]))):
        sid, t = key; site = catalogue[sid]
        values = {k: numeric(h[key][k]) for k in FIELDS}
        for k, value in values.items():
            missing[k] += value is None
        sphagnum = [numeric(x) for k, x in v[key].items() if k.startswith('Sphagnum_')]
        joined.append(dict(site_id=sid, time=int(t), sampling_year=int(site['Sampling_'+t]),
                           treatment=site['Treatment'], ecosystem_type=site['Type'],
                           latitude=float(site['N']), longitude=float(site['E']),
                           sphagnum_cover=sum(sphagnum) if all(x is not None for x in sphagnum) else None,
                           **values))
    return catalogue, joined, missing


def distance(a, b):
    lat1, lat2 = math.radians(float(a['N'])), math.radians(float(b['N']))
    dlat, dlon = lat2-lat1, math.radians(float(b['E'])-float(a['E']))
    q = math.sin(dlat/2)**2+math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6371*2*math.asin(min(1, math.sqrt(q)))


def geographic_split(catalogue, buffer_km=10):
    # Connected components keep all nearby sites together, without reading outcomes.
    parent = {s: s for s in catalogue}
    def root(s):
        while parent[s] != s:
            s = parent[s]
        return s
    ids = sorted(catalogue, key=int)
    for i, a in enumerate(ids):
        for b in ids[i+1:]:
            if distance(catalogue[a], catalogue[b]) <= buffer_km:
                parent[root(b)] = root(a)
    groups = {}
    for sid in ids:
        groups.setdefault(root(sid), []).append(sid)
    ordered = sorted(groups.values(), key=lambda g: hashlib.sha256((','.join(g)+'|s2ds-v1').encode()).hexdigest())
    split = {k: [] for k in ('train', 'validation', 'test')}
    target = {'train': .6*len(ids), 'validation': .2*len(ids), 'test': .2*len(ids)}
    for group in ordered:
        p = min(split, key=lambda k: len(split[k])/target[k])
        split[p].extend(group)
    if any(not values for values in split.values()):
        raise ValueError('Too few independent geographic groups')
    return dict(version='finnish-v1', buffer_km=buffer_km, groups=ordered, partitions=split,
                role='public teaching split; not a secret blind benchmark')


def bootstrap_interval(values, seed=42):
    if not values:
        return None
    rng = random.Random(seed)
    means = sorted(mean(rng.choices(values, k=len(values))) for _ in range(1000))
    return [means[24], means[974]]


def baseline_metrics(rows, catalogue, split):
    by_key = {(r['site_id'], r['time']): r for r in rows}
    train = [by_key[s, 10]['WT_ES'] for s in split['partitions']['train'] if (s, 10) in by_key and by_key[s, 10]['WT_ES'] is not None]
    if not train:
        raise ValueError('No train targets')
    constant = median(train)
    output = {'target': 'early-summer WTD at Time=10', 'units': 'cm; negative below surface', 'train_constant_cm': constant}
    for p in ('validation', 'test'):
        evaluation = [(by_key[s, 0]['WT_ES'], by_key[s, 10]['WT_ES']) for s in split['partitions'][p] if (s, 0) in by_key and (s, 10) in by_key]
        evaluation = [(a, b) for a, b in evaluation if a is not None and b is not None]
        if not evaluation:
            raise ValueError('No evaluation targets')
        output[p] = {}
        for name, errors in [('persistence', [a-b for a,b in evaluation]), ('train_median', [constant-b for a,b in evaluation])]:
            output[p][name] = dict(n=len(errors), mae_cm=mean(abs(e) for e in errors), rmse_cm=math.sqrt(mean(e*e for e in errors)))
    return output


def run_field(directory, output, split_path):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    catalogue, joined, missing = join_records(directory)
    split = json.loads(Path(split_path).read_text())
    allocated = [s for ids in split['partitions'].values() for s in ids]
    if len(allocated)!=len(set(allocated)) or set(allocated)!=set(catalogue):
        raise ValueError('Frozen split must allocate every site exactly once')
    expected = geographic_split(catalogue)
    if split != expected:
        raise ValueError('Frozen split differs from outcome-independent geographic design')
    write_csv(output/'joined.csv', joined, list(joined[0]))
    trajectories=[]
    for treatment in sorted({r['treatment'] for r in joined}):
        for time in (0, 2, 5, 10):
            subset=[r for r in joined if r['treatment']==treatment and r['time']==time]
            for variable in ('WT_ES','WT_MS','sphagnum_cover'):
                values=[r[variable] for r in subset if r[variable] is not None]
                trajectories.append(dict(treatment=treatment,time=time,variable=variable,n=len(values),mean=mean(values) if values else None))
    write_csv(output/'trajectories.csv',trajectories,list(trajectories[0]))
    changes={}
    lookup={(r['site_id'],r['time']):r for r in joined}
    for treatment in ('restored','pristine'):
        values=[lookup[s,10]['WT_ES']-lookup[s,0]['WT_ES'] for s in catalogue if catalogue[s]['Treatment']==treatment and lookup[s,10]['WT_ES'] is not None and lookup[s,0]['WT_ES'] is not None]
        changes[treatment]=dict(n=len(values),mean_change_cm=mean(values),site_bootstrap_95_interval=bootstrap_interval(values))
    results=dict(sites=len(catalogue),joined_rows=len(joined),missing_counts=missing,changes=changes,
                 baselines=baseline_metrics(joined,catalogue,split),
                 claim='Observational teaching analysis; not a replication of published inferential results or an EO/causal model. Bootstrap treats sites as independent; spatial correlation can make intervals optimistic.')
    (output/'metrics.json').write_text(json.dumps(results,indent=2)+'\n')
    inputs=[dict(filename=p.name,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(Path(directory).glob('*.csv'))]
    (output/'provenance.json').write_text(json.dumps(dict(inputs=inputs,split_sha256=hashlib.sha256(Path(split_path).read_bytes()).hexdigest(),source='10.5281/zenodo.17301631',code='field_analysis.py',code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,2,figsize=(10,4))
    for ax,var,title in zip(axes,('WT_ES','sphagnum_cover'),('Early-summer water table (cm)','Sphagnum cover (%)')):
        for treatment in ('restored','pristine'):
            points=[x for x in trajectories if x['variable']==var and x['treatment']==treatment]
            ax.plot([x['time'] for x in points],[x['mean'] for x in points],marker='o',label=treatment)
        ax.set(title=title,xlabel='Sampling stage (nominal years)',xticks=[0,2,5,10]);ax.legend();ax.grid(alpha=.2)
    fig.tight_layout();fig.savefig(output/'trajectories.png',dpi=150);plt.close(fig)
    (output/'report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>Finnish field analysis</title><h1>Finnish restoration field records</h1><p>'+results['claim']+'</p><img src="trajectories.png" alt="Observed treatment group mean trajectories"><h2>Metrics and QC</h2><pre>'+json.dumps(results,indent=2)+'</pre><p>WT is negative below surface. A positive change means a shallower water table. Treatment comparisons are descriptive; ecosystem mix and sampling dates can confound them.</p><a href="joined.csv">Joined records</a> · <a href="provenance.json">Provenance</a></html>')
    return results
