# MeasureNature · S2DS student starter

ForestPulse / RestoreWatch: reproducible land and water change monitoring.

**Start here:** [student guide](docs/STUDENT_GUIDE.md) · [workshop](docs/WORKSHOP.md) · [project brief](docs/PROJECT_BRIEF.md) · [data contract](docs/DATA.md).

## First working result (Python 3.10–3.13)

No credentials, GPU, external datasets or runtime dependencies are required.

```bash
python -m venv .venv
# Linux / macOS
source .venv/bin/activate
# Windows PowerShell instead: .venv\Scripts\Activate.ps1
python -m pip install -e .
python -m s2ds_starter demo --output outputs/demo
python -m unittest discover -s tests -v
```

Open `outputs/demo/report.html` in a browser. It contains the holdout metrics, alerts and limitations. The run also produces input CSVs, predictions, a split manifest and provenance hashes. All demo observations and event labels are **synthetic**; its scores are not evidence of ecological performance.

Optional notebook environment: `python -m pip install -e '.[notebooks]'`, then `jupyter lab`. Run `notebooks/01_first_result.ipynb` from the repository root.

## Bring your own verified data

```bash
python -m s2ds_starter run --features data/features.csv --sites data/sites.csv --output outputs/real
```

Follow [DATA.md](docs/DATA.md). This baseline detects persistent negative NDVI departures from a pre-event baseline. It does not estimate biodiversity, water-table depth, carbon benefit or restoration causality. RestoreWatch needs field ground truth, controls and a separate hydrological baseline before those questions can be assessed.

## Contents

- Dependency-free, deterministic baseline and offline fixture generator.
- Site-disjoint train/validation/test workflow; threshold selected on validation only.
- CSV validation, observation dates, cloud filtering, scene provenance and report export.
- Student notebook, three-hour workshop, five-week plan and facilitator notes.
- Meaningful unit/integration checks and GitHub Actions across Python versions.

[Contribution guide](CONTRIBUTING.md) · [acceptance checklist](docs/ACCEPTANCE.md) · [source catalogue](docs/SOURCES.md).

No external data is bundled. Outputs are ignored by Git. Record licenses before sharing real datasets. Code is provided under MIT; this does not license third-party data or grant rights to the MeasureNature name.
