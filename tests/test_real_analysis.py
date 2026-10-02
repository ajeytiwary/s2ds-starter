import copy
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
try:
    import numpy as np
    import rasterio
    HAS_ANALYSIS=True
except ImportError:
    HAS_ANALYSIS=False
from s2ds_starter.field_analysis import join_records, geographic_split, distance, baseline_metrics
if HAS_ANALYSIS:
    from s2ds_starter.fire_analysis import normalized_difference, confusion, run_fire

ROOT=Path(__file__).resolve().parents[1]


@unittest.skipUnless(HAS_ANALYSIS,"Install the analysis extra to run real-data integration tests")
class RealAnalysisTests(unittest.TestCase):
    def test_source_bytes(self):
        for folder in ('finnish-hydrology','forestpulse-daba'):
            root=ROOT/'datasets'/folder
            path=root/('download_manifest.json' if folder=='finnish-hydrology' else 'source_manifest.json')
            for item in json.loads(path.read_text())['files']:
                self.assertEqual(hashlib.sha256((root/item['filename']).read_bytes()).hexdigest(),item['sha256'])

    def test_join_and_missing_data(self):
        catalogue,rows,missing=join_records(ROOT/'datasets/finnish-hydrology')
        self.assertEqual((len(catalogue),len(rows)),(40,160))
        self.assertEqual(len({(r['site_id'],r['time']) for r in rows}),160)
        self.assertEqual(missing['WT_ES'],1)
        self.assertTrue(any(r['WT_ES'] is None for r in rows))

    def test_geographic_buffer(self):
        cat,_,_=join_records(ROOT/'datasets/finnish-hydrology')
        split=geographic_split(cat)
        self.assertEqual(split,json.loads((ROOT/'resources/finnish_split_v1.json').read_text()))
        allocation={s:p for p,ids in split['partitions'].items() for s in ids}
        for a in cat:
            for b in cat:
                if distance(cat[a],cat[b])<=10:
                    self.assertEqual(allocation[a],allocation[b])

    def test_holdout_targets_cannot_fit_constant(self):
        cat,rows,_=join_records(ROOT/'datasets/finnish-hydrology');split=geographic_split(cat)
        before=baseline_metrics(rows,cat,split)
        modified=copy.deepcopy(rows)
        for r in modified:
            if r['site_id'] in split['partitions']['test'] and r['time']==10:
                r['WT_ES']=1000
        after=baseline_metrics(modified,cat,split)
        self.assertEqual(before['train_constant_cm'],after['train_constant_cm'])
        self.assertEqual(before['validation'],after['validation'])

    def test_zero_denominator_and_masked_scores(self):
        result=normalized_difference(np.array([1.,0.]),np.array([1.,0.]))
        self.assertEqual(result[0],0);self.assertTrue(np.isnan(result[1]))
        m=confusion(np.array([True,False,True]),np.array([True,True,False]),np.array([True,True,False]))
        self.assertEqual((m['tp'],m['fp'],m['fn']),(1,1,0))
        self.assertAlmostEqual(m['iou'],.5)
        with self.assertRaisesRegex(ValueError,'No valid'):
            confusion(np.array([True]),np.array([True]),np.array([False]))

    def test_complete_real_fire_and_georeferenced_export(self):
        import rasterio
        with tempfile.TemporaryDirectory() as tmp:
            m=run_fire(ROOT/'datasets/forestpulse-daba',tmp)
            self.assertGreater(m['tp'],0)
            self.assertEqual(m['total_pixels'],531*647)
            self.assertTrue(m['label_pixel_alignment_assumed'])
            with rasterio.open(Path(tmp)/'predicted_burn.tif') as s:
                self.assertEqual(str(s.crs),'EPSG:4326')
                self.assertEqual(s.nodata,255)
                self.assertEqual(s.shape,(531,647))
