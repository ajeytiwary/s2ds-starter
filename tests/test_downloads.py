import hashlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('download_data', ROOT/'scripts/download_data.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class DownloadTests(unittest.TestCase):
    def test_verified_download(self):
        body = b'ID,Time\n1,0\n'
        record = dict(record_id='123', record_url='https://zenodo.org/records/123',
                      files=[dict(filename='test.csv', md5=hashlib.md5(body).hexdigest())])
        with tempfile.TemporaryDirectory() as temp:
            m = module.download(record, temp, opener=lambda *a, **kw: io.BytesIO(body))
            self.assertEqual((Path(temp)/'test.csv').read_bytes(), body)
            self.assertEqual(m['files'][0]['sha256'], hashlib.sha256(body).hexdigest())

    def test_checksum_failure_preserves_existing_file(self):
        record = dict(record_id='123', record_url='x', files=[dict(filename='test.csv', md5='0'*32)])
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp)/'test.csv'; target.write_bytes(b'original')
            with self.assertRaisesRegex(ValueError, 'checksum'):
                module.download(record, temp, opener=lambda *a, **kw: io.BytesIO(b'bad'))
            self.assertEqual(target.read_bytes(), b'original')
            self.assertFalse((Path(temp)/'test.csv.part').exists())

    def test_path_traversal_rejected(self):
        record = dict(record_id='123', record_url='x', files=[dict(filename='../bad', md5='0'*32)])
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, 'Unsafe'):
                module.download(record, temp)
