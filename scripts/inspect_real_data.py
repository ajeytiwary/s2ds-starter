"""Inventory original CSVs without inventing source-specific field mappings."""
import argparse
import csv
import hashlib
import json
from pathlib import Path


def inspect(directory):
    result = []
    for path in sorted(Path(directory).glob('*.csv')):
        with path.open(encoding='utf-8-sig', newline='') as f:
            sample = f.read(8192); f.seek(0)
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=',;\t')
            except csv.Error:
                dialect = csv.excel
            reader = csv.DictReader(f, dialect=dialect)
            fields = reader.fieldnames or []
            missing = {k: 0 for k in fields}; preview = []; n = 0
            for row in reader:
                n += 1
                if len(preview) < 3:
                    preview.append(row)
                for key in fields:
                    if row.get(key) is None or row[key].strip().lower() in ('', '-9999', 'na', 'nan', 'null'):
                        missing[key] += 1
        result.append(dict(filename=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                           delimiter=dialect.delimiter, rows=n, columns=fields,
                           potential_missing_counts=missing, preview=preview))
    if not result:
        raise ValueError('No CSV files found')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        result = inspect(args.directory)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    except (ValueError, OSError) as e:
        parser.exit(2, f'Inventory failed: {e}\n')
    print(f'Inventoried {len(result)} CSVs: {args.output}')
