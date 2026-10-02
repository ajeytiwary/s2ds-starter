import argparse
from pathlib import Path
from .pipeline import fixture, run


def main():
    parser = argparse.ArgumentParser(description='MeasureNature S2DS educational baseline')
    commands = parser.add_subparsers(dest='command', required=True)
    demo = commands.add_parser('demo', help='Generate synthetic inputs and a complete report')
    demo.add_argument('--output', type=Path, default=Path('outputs/demo'))
    real = commands.add_parser('run', help='Validate and evaluate supplied CSVs')
    real.add_argument('--features', required=True, type=Path)
    real.add_argument('--sites', required=True, type=Path)
    real.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'demo':
            features, sites = fixture(args.output/'inputs')
        else:
            features, sites = args.features, args.sites
        result = run(features, sites, args.output, synthetic=args.command == 'demo')
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Input/run error: {exc}\n')
    print(f'Report: {(args.output / "report.html").resolve()}')
    print(f'Data: {result["data_kind"]}; test sites: {result["test"]["n"]}')


if __name__ == '__main__':
    main()
