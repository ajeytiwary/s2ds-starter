# MeasureNature · S2DS student starter

ForestPulse / RestoreWatch: reproducible land and water change monitoring.

**Start here:** [student guide](docs/STUDENT_GUIDE.md) · [workshop](docs/WORKSHOP.md) · [project brief](docs/PROJECT_BRIEF.md) · [data contract](docs/DATA.md).

## First working result (Python 3.10–3.13)

The synthetic demo requires no credentials, GPU, external datasets or runtime dependencies. Real-data modelling and notebook checks use the optional extras below. Tests requiring analysis extras are skipped when those extras are absent.

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

## Worked real-data projects (offline after dependency installation)

```bash
python -m pip install -e ".[analysis,notebooks]"
python scripts/run_field_analysis.py
python scripts/run_fire_example.py
python -m unittest discover -s tests -v
```

Open `outputs/field-analysis/report.html` and `outputs/forestpulse-daba/report.html`.

- `03_worked_field_analysis.ipynb`: joins/QC, treatment trajectories, frozen geographic split and field-only water-table baselines.
- `04_real_forestpulse_event.ipynb`: real Daba Sentinel-2 imagery, dNBR baseline, published reference, metrics, maps and GeoTIFF/GeoJSON exports.
- [Student task sheets](docs/STUDENT_TASKS.md), [facilitator solutions](docs/FACILITATOR_SOLUTIONS.md), [frozen evaluation protocol](docs/EVALUATION.md).

The Daba reference lacks a CRS; pixel alignment is explicitly assumed from its paired dimensions and author loader. Cloud/snow/water masks and original Sentinel product IDs are absent. The visible smoke and false positives are part of the learning exercise. This is a single public event, not a credible generalization benchmark. The Finnish public test labels also remain visible; use the mentor protocol for new blind assessments.

Full Jupyter execution check: install `.[analysis,validation]`, then `python scripts/validate_notebooks.py`. CI executes all four notebooks and runs real-data checks on Linux and Windows.

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

[Contribution guide](CONTRIBUTING.md) · [acceptance checklist](docs/ACCEPTANCE.md) · [real datasets and studies](docs/SOURCES.md) · [real-data workshop](docs/REAL_DATA_WORKSHOP.md).

Real dataset download recipes are included; additional downloads are kept outside Git. A small CC BY 4.0 Finnish field dataset is bundled with attribution in `datasets/finnish-hydrology/`; A compact real Daba fire event is also bundled with attribution; other datasets are downloaded on demand. Outputs are ignored by Git. Record licenses before sharing real datasets. Code is provided under MIT; this does not license third-party data or grant rights to the MeasureNature name.
