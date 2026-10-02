# Student task sheets

Run from repository root. Install the analysis extra as described in README. Each task needs a reviewer and a short PR explaining results, units and limitations. Worked answers are in FACILITATOR_SOLUTIONS.md; try independently first.

| Task / suggested owner | Inputs | Expected deliverable | Acceptance |
|---|---|---|---|
| 1 · Data/provenance | Bundled originals and source README | Joined table, QC counts, source/hash ledger | Unique ID/Time; 40 sites and 160 rows; missing markers preserved; joins fail on duplicates |
| 2 · Field analysis | Task 1 table | Treatment plots and WTD change table | cm/sign documented; no invented intervention dates; missing-target counts reported |
| 3 · Evaluation | Frozen geographic split | Persistence/train-median comparison and experiment record | No shared sites/groups; train-only constant; validation/test counts and MAE/RMSE |
| 4 · Optical change | Real event manifest and imagery | dNBR, valid mask, predicted GeoTIFF, metrics and map | Reference/image grids agree; bands explicit; validity/nodata checks; missing cloud QA explicitly flagged; no test tuning |
| 5 · Integration/reporting | Outputs of 1–4 | Reproducible manager demonstration | Runs from clean checkout; outputs link to source; actual versus unsupported claims explicit |

## Stretch work after the first result
- Radar/weather owner: choose an AOI with dated field records, verify Sentinel-1 orbit/polarization and ERA5 spatial/temporal support. Produce aligned features and QC before fitting a model.
- Evaluation owner: author-defined matched controls, ecosystem balance, geographic buffer sensitivity and cluster bootstrap.
- Optical owner: multiple event holdouts, seasonal alternative and false-alert audit outside burns.
- Reporting owner: AOI GeoJSON and map with acquisition dates, legend and coverage; avoid a biodiversity score from NDVI alone.

## Definition of done for every student
The reproduction command works; input hashes are present; units and sampling support are explained; peer review completed; meaningful tests cover one failure mode; performance claims match the evaluated sampling unit. Report uncertainties and unresolved source issues instead of filling gaps with fabricated values.
