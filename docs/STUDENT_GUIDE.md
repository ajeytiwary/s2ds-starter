# Student start

1. Clone the repository, create the environment and run the commands in README.
2. Open the HTML report and trace one alert back to the feature CSV and its scene IDs.
3. Inspect `split.json`: sites never overlap across partitions. Inspect validation scores in `metrics.json`.
4. Run the notebook. Explain why using test labels to choose a threshold invalidates evaluation.
5. Complete the workshop exercises, then select one track in the project brief.

## Troubleshooting
- `No module named s2ds_starter`: activate the environment and run `python -m pip install -e .` from the repository root.
- PowerShell activation blocked: use `.venv\Scripts\python.exe -m pip install -e .` and run that Python directly; do not weaken system security policy.
- Jupyter cannot import the package: install the notebook extra in the active environment and launch Jupyter from it.
- Not enough baseline/post-event observations: inspect cloud filtering and dates; collect more observations instead of silently filling missing labels.
- Real CSV validation fails: read DATA.md and fix the source table; the CLI returns a nonzero exit code.

## Expected first result
Twelve synthetic sites, four per partition, a report and a reproducible manifest. Scores depend on the fixture; learn the procedure, not its apparent accuracy. Train is reserved for future fitted models; the current baseline uses each site's pre-cutoff observations and validation-only threshold selection.
