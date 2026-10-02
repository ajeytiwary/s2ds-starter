import csv
import json
import tempfile
import unittest
from pathlib import Path
from s2ds_starter.pipeline import fixture, load, metrics, run, split_sites, write_csv


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.features, self.sites = fixture(self.root/'inputs')

    def mutate(self, change):
        with self.features.open() as f:
            rows = list(csv.DictReader(f))
        change(rows)
        write_csv(self.features, rows, list(rows[0]))

    def test_complete_reproducible_run(self):
        first = run(self.features, self.sites, self.root/'a', synthetic=True)
        self.assertEqual(first, run(self.features, self.sites, self.root/'b', synthetic=True))
        self.assertEqual(first['test']['n'], 4)
        for p in ('report.html', 'predictions.csv', 'metrics.json', 'split.json', 'provenance.json'):
            self.assertTrue((self.root/'a'/p).is_file())
        self.assertTrue(json.loads((self.root/'a'/'provenance.json').read_text())['synthetic'])

    def test_disjoint_split(self):
        catalogue, _, _ = load(self.features, self.sites)
        split = split_sites(catalogue)
        self.assertEqual(sum(map(len, split.values())), len(catalogue))
        self.assertFalse(set(split['train']) & set(split['test']))
        self.assertFalse(set(split['validation']) & set(split['test']))

    def test_duplicate_rejected(self):
        self.mutate(lambda rows: rows.append(dict(rows[0])))
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            load(self.features, self.sites)

    def test_nonfinite_rejected(self):
        self.mutate(lambda rows: rows[0].update(ndvi='nan'))
        with self.assertRaisesRegex(ValueError, 'NDVI'):
            load(self.features, self.sites)

    def test_cloud_filter_and_missing_coverage(self):
        self.mutate(lambda rows: rows[0].update(cloud_fraction='1'))
        self.assertEqual(load(self.features, self.sites)[2]['excluded_cloud'], 1)
        self.mutate(lambda rows: [row.update(cloud_fraction='1') for row in rows if row['site_id']=='SYNTHETIC-00'])
        with self.assertRaisesRegex(ValueError, 'need >=3'):
            load(self.features, self.sites)

    def test_test_labels_do_not_select_threshold(self):
        original = run(self.features, self.sites, self.root/'before')['threshold']
        with self.sites.open() as f:
            rows = list(csv.DictReader(f))
        test_ids = set(json.loads((self.root/'before'/'split.json').read_text())['test'])
        for row in rows:
            if row['site_id'] in test_ids:
                row['event_label'] = str(1-int(row['event_label']))
        write_csv(self.sites, rows, list(rows[0]))
        self.assertEqual(original, run(self.features, self.sites, self.root/'after')['threshold'])

    def test_confusion_counts(self):
        catalogue = {'a': {'label': 1}, 'b': {'label': 0}, 'c': {'label': 1}}
        scores = {'a': {'score': .3}, 'b': {'score': .3}, 'c': {'score': 0}}
        m = metrics(list(catalogue), catalogue, scores, .2)
        self.assertEqual((m['tp'], m['fp'], m['fn'], m['tn']), (1, 1, 1, 0))
        self.assertEqual(m['f1'], .5)


if __name__ == '__main__':
    unittest.main()
