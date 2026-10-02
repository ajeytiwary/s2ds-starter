"""Educational site-level detector. No remote data or inference of causality."""
import csv
import hashlib
import html
import json
import math
import random
import subprocess
from datetime import date, timedelta
from pathlib import Path
from statistics import mean
from . import __version__


def write_csv(path, rows, fields):
    with Path(path).open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def fixture(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    rng = random.Random(42)
    sites, features = [], []
    for i in range(12):
        sid = f'SYNTHETIC-{i:02d}'
        label = i % 2
        sites.append(dict(site_id=sid, event_label=label,
                          evaluation_start='2026-04-01', source='synthetic educational fixture'))
        for j in range(10):
            ndvi = 0.72 + rng.uniform(-0.025, 0.025)
            if j >= 6:
                ndvi -= (0.18 + 0.02 * (i % 3)) if label else 0.025
            features.append(dict(site_id=sid, date=str(date(2026, 1, 1) + timedelta(days=j*15)),
                                 ndvi=round(ndvi, 5), cloud_fraction=0.1,
                                 scene_id=f'SYNTHETIC-{i}-{j}', source='synthetic; no satellite acquisition'))
    write_csv(directory/'sites.csv', sites, ['site_id', 'event_label', 'evaluation_start', 'source'])
    write_csv(directory/'features.csv', features, ['site_id', 'date', 'ndvi', 'cloud_fraction', 'scene_id', 'source'])
    return directory/'features.csv', directory/'sites.csv'


def read_csv(path, required):
    with Path(path).open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f'{path}: missing columns {sorted(required-set(reader.fieldnames or []))}')
        rows = list(reader)
    if not rows:
        raise ValueError(f'{path}: empty table')
    for row in rows:
        if any(not row.get(k) or not row[k].strip() for k in required):
            raise ValueError(f'{path}: empty required value')
    return rows


def load(features_path, sites_path):
    sites = read_csv(sites_path, {'site_id', 'event_label', 'evaluation_start', 'source'})
    catalogue = {}
    for row in sites:
        sid = row['site_id']
        if sid in catalogue:
            raise ValueError('Duplicate site ID')
        if row['event_label'] not in ('0', '1'):
            raise ValueError('Labels must be 0 or 1')
        catalogue[sid] = dict(row, cutoff=date.fromisoformat(row['evaluation_start']), label=int(row['event_label']))
    rows = read_csv(features_path, {'site_id', 'date', 'ndvi', 'cloud_fraction', 'scene_id', 'source'})
    seen, grouped, excluded = set(), {s: [] for s in catalogue}, 0
    for row in rows:
        sid, day = row['site_id'], date.fromisoformat(row['date'])
        if sid not in catalogue:
            raise ValueError('Unknown feature site')
        if (sid, day) in seen:
            raise ValueError('Duplicate site/date')
        seen.add((sid, day))
        ndvi, cloud = float(row['ndvi']), float(row['cloud_fraction'])
        if not math.isfinite(ndvi) or not -1 <= ndvi <= 1:
            raise ValueError('NDVI must be finite and in [-1,1]')
        if not math.isfinite(cloud) or not 0 <= cloud <= 1:
            raise ValueError('Cloud fraction must be finite and in [0,1]')
        if cloud > 0.4:
            excluded += 1
            continue
        grouped[sid].append(dict(row, day=day, value=ndvi))
    scores = {}
    for sid, observations in grouped.items():
        observations.sort(key=lambda x: x['day'])
        pre = [x for x in observations if x['day'] < catalogue[sid]['cutoff']]
        post = [x for x in observations if x['day'] >= catalogue[sid]['cutoff']]
        if len(pre) < 3 or len(post) < 2:
            raise ValueError(f'{sid}: need >=3 valid baseline and >=2 post-cutoff observations')
        scores[sid] = dict(score=mean(x['value'] for x in pre)-mean(x['value'] for x in post[-2:]),
                           baseline_count=len(pre), post_count=len(post),
                           alert_date=str(post[-1]['day']), scene_ids=';'.join(x['scene_id'] for x in pre+post[-2:]))
    return catalogue, scores, dict(total_observations=len(rows), excluded_cloud=excluded,
                                    accepted_observations=len(rows)-excluded, evaluated_sites=len(scores))


def split_sites(catalogue):
    if len(catalogue) < 6:
        raise ValueError('At least six sites are required for three partitions')
    partitions = {k: [] for k in ('train', 'validation', 'test')}
    for i, sid in enumerate(sorted(catalogue)):
        partitions[('train', 'validation', 'test')[i % 3]].append(sid)
    for name in ('validation', 'test'):
        if {catalogue[s]['label'] for s in partitions[name]} != {0, 1}:
            raise ValueError(f'{name} must contain both label classes; revise the frozen site design')
    return partitions


def metrics(ids, catalogue, scores, threshold):
    tp = fp = tn = fn = 0
    for sid in ids:
        y, p = catalogue[sid]['label'], scores[sid]['score'] >= threshold
        tp += int(y == 1 and p)
        fp += int(y == 0 and p)
        tn += int(y == 0 and not p)
        fn += int(y == 1 and not p)
    precision = tp/(tp+fp) if tp+fp else 0.0
    recall = tp/(tp+fn) if tp+fn else 0.0
    return dict(n=len(ids), tp=tp, fp=fp, tn=tn, fn=fn, precision=precision, recall=recall,
                f1=2*precision*recall/(precision+recall) if precision+recall else 0.0)


def run(features_path, sites_path, output, synthetic=False):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    catalogue, scores, qc = load(features_path, sites_path)
    split = split_sites(catalogue)
    candidates = [(t, metrics(split['validation'], catalogue, scores, t)) for t in (0.05, 0.10, 0.15, 0.20, 0.25)]
    threshold, validation = max(candidates, key=lambda x: (x[1]['f1'], x[0]))
    results = dict(data_kind='synthetic' if synthetic else 'user-supplied; provenance requires independent review',
                   threshold=threshold, validation=validation,
                   validation_candidates=[dict(threshold=t, **m) for t, m in candidates],
                   test=metrics(split['test'], catalogue, scores, threshold), qc=qc)
    predictions = [dict(site_id=s, partition=p, label=catalogue[s]['label'],
                         prediction=int(scores[s]['score'] >= threshold), **scores[s])
                   for p, ids in split.items() for s in ids]
    write_csv(output/'predictions.csv', predictions, list(predictions[0]))
    for name, value in [('metrics.json', results), ('split.json', split)]:
        (output/name).write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=Path(__file__).resolve().parents[2], stderr=subprocess.DEVNULL, text=True).strip()
        dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=Path(__file__).resolve().parents[2], text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        commit, dirty = 'unavailable', None
    provenance = dict(package_version=__version__, git_commit=commit, git_dirty=dirty,
                       inputs=[dict(filename=Path(p).name, sha256=hashlib.sha256(Path(p).read_bytes()).hexdigest()) for p in (features_path, sites_path)],
                       parameters=dict(cloud_limit=0.4, post_window=2, threshold_candidates=[x[0] for x in candidates]),
                       split=split, synthetic=synthetic)
    (output/'provenance.json').write_text(json.dumps(provenance, indent=2)+'\n', encoding='utf-8')
    body = ''.join('<tr>'+''.join(f'<td>{html.escape(str(row[k]))}</td>' for k in ('site_id', 'partition', 'score', 'prediction', 'alert_date'))+'</tr>' for row in predictions)
    report = f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>S2DS monitoring report</title>
<style>body{{font:16px system-ui;max-width:1000px;margin:40px auto;padding:20px;color:#173b33}}td,th{{padding:8px;border-bottom:1px solid #ccc;text-align:left}}pre{{white-space:pre-wrap}}.notice{{background:#fff2cc;padding:16px}}</style>
<h1>MeasureNature · S2DS monitoring report</h1><p class="notice">Data: {html.escape(results['data_kind'])}. Educational NDVI detector. No evidence of biodiversity, restoration success or causal impact.</p>
<h2>Holdout metrics</h2><pre>{html.escape(json.dumps(results['test'], indent=2))}</pre><p>Validation-selected threshold: {threshold}. Small samples and synthetic labels cannot establish real-world accuracy.</p>
<h2>Observation coverage</h2><pre>{html.escape(json.dumps(qc, indent=2))}</pre>
<h2>Site decisions</h2><p>Prediction 1 means a retrospective threshold exceedance, requiring investigation.</p><table><tr><th>Site</th><th>Partition</th><th>NDVI departure</th><th>Prediction</th><th>Last observation</th></tr>{body}</table>
<h2>Limitations</h2><p>No seasonality correction, spatial mask, calibrated confidence, cloud-gap imputation, radar or weather integration. Date is the last observation used, not first detection. Sites with insufficient coverage fail validation. Input labels require independent review.</p>
<p><a href="predictions.csv">Predictions and scenes</a> · <a href="metrics.json">Metrics</a> · <a href="split.json">Split</a> · <a href="provenance.json">Provenance</a></p></html>'''
    (output/'report.html').write_text(report, encoding='utf-8')
    return results
