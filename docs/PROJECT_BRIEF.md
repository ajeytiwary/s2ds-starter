# Project brief

## Decision and user
A restoration project manager needs an auditable list of sites worth investigating, with dated observations and uncertainty, rather than an unexplained ecological score.

## Two research tracks
**ForestPulse:** detect persistent forest vegetation change using Sentinel-2 indices, then assess Sentinel-1 robustness during cloudy periods. Investigate disturbance labels and reference mapping. Distinguish seasonal decline, harvest, fire and sensor artifacts where ground truth allows.

**RestoreWatch:** investigate whether peatland restoration changes observable wetness proxies, using dated interventions, matched controls, Sentinel-1/2, ERA5 covariates and water-table observations. Estimate associations first; causal claims need a defensible intervention/control design and confounder checks.

Both share a site catalogue, quality filtering, baseline, disjoint evaluation, provenance and exported report. This starter implements only a simple ForestPulse time-series baseline; RestoreWatch is a student extension.

## Deliverables
A reproducible run on one verified public AOI, a source/scene catalogue, leakage-safe experiment manifest, baseline comparison, uncertainty/limitations analysis and a manager-facing report. A spatial change mask and GeoJSON export are stretch deliverables; neither is implemented here.

## Five-week plan for five students
| Week | Deliverable | Review gate |
|---|---|---|
| 1 | Environment, fixture run, AOI/source selection, data contract | Mentor approves licenses and usable ground truth |
| 2 | Real extraction and QC; scene/date provenance | Independent student reproduces feature table |
| 3 | Baseline and validation-only model comparison | Frozen split, no test tuning |
| 4 | Error analysis, robustness, control/field comparisons | Claims supported by labels and uncertainty |
| 5 | Frozen evaluation, report, demonstration and handover | Acceptance checklist and reproducible archive |

Suggested primary owners: data/provenance; optical features; radar/weather; evaluation; reporting/integration. Pair each owner with a reviewer and rotate roles. Do not let one person become the only person able to reproduce a stage.

## Success measures
Report precision/recall/F1 with counts, false alerts per monitored site, coverage after QC, event detection delay when dated labels permit it, and performance by site/season. Do not invent numeric product targets before confirming label quality and customer costs of misses versus false alerts.
