import argparse
from pathlib import Path
from s2ds_starter.fire_analysis import run_fire

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--data',type=Path,default=Path('datasets/forestpulse-daba'))
    p.add_argument('--output',type=Path,default=Path('outputs/forestpulse-daba'))
    a=p.parse_args()
    m=run_fire(a.data,a.output)
    print(f"Real event {m['event']}; valid pixels={m['valid_pixels']}; report={a.output/'report.html'}")
