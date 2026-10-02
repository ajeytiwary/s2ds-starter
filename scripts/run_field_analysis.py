import argparse
from pathlib import Path
from s2ds_starter.field_analysis import run_field

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--data',type=Path,default=Path('datasets/finnish-hydrology'))
    p.add_argument('--output',type=Path,default=Path('outputs/field-analysis'))
    p.add_argument('--split',type=Path,default=Path('resources/finnish_split_v1.json'))
    a=p.parse_args()
    result=run_field(a.data,a.output,a.split)
    print(f"Joined {result['joined_rows']} records from {result['sites']} sites. Report: {a.output/'report.html'}")
