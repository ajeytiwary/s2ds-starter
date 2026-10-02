"""Download pinned small published files; verify bytes and retain provenance."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

CATALOGUE = Path(__file__).resolve().parents[1]/'resources/downloads.json'
LIMIT = 25*1024*1024


def download(record, output, opener=urlopen):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    manifest = dict(record_url=record['record_url'], files=[])
    for entry in record['files']:
        name = entry['filename']
        if Path(name).name != name or name in ('.', '..'):
            raise ValueError('Unsafe filename')
        url = f"https://zenodo.org/api/records/{record['record_id']}/files/{quote(name, safe='')}/content"
        destination, partial = output/name, output/(name+'.part')
        md5, sha, size = hashlib.md5(), hashlib.sha256(), 0
        try:
            with opener(url, timeout=30) as response, partial.open('wb') as f:
                while True:
                    chunk = response.read(65536)
                    if not chunk:
                        break
                    size += len(chunk)
                    if size > LIMIT:
                        raise ValueError(f'{name}: exceeds 25 MiB download cap')
                    md5.update(chunk); sha.update(chunk); f.write(chunk)
            if md5.hexdigest() != entry['md5']:
                raise ValueError(f'{name}: checksum mismatch; not installed')
            partial.replace(destination)
        finally:
            partial.unlink(missing_ok=True)
        manifest['files'].append(dict(filename=name, url=url, size_bytes=size,
                                      md5=md5.hexdigest(), sha256=sha.hexdigest()))
    (output/'download_manifest.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest


def main():
    catalogue = json.loads(CATALOGUE.read_text())
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('dataset', choices=sorted(catalogue))
    p.add_argument('--output', type=Path, default=Path('data/raw'))
    p.add_argument('--list', action='store_true')
    args = p.parse_args()
    record = catalogue[args.dataset]
    if args.list:
        print(json.dumps(record, indent=2)); return
    try:
        result = download(record, args.output/args.dataset)
    except (OSError, ValueError) as e:
        p.exit(2, f'Download failed: {e}\n')
    print(f"Verified {len(result['files'])} original files in {args.output/args.dataset}")


if __name__ == '__main__':
    main()
