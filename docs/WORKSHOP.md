# Three-hour workshop

| Minutes | Activity | Evidence |
|---|---|---|
| 0–20 | Research question, claims and source limitations | One decision statement per group |
| 20–45 | Setup and offline demo | HTML report opens |
| 45–70 | Notebook and alert provenance | One alert traced to dated inputs |
| 70–80 | Break | |
| 80–110 | QC and leakage exercises | Test output and explanation |
| 110–140 | Design a real AOI experiment | Site/control/source catalogue draft |
| 140–165 | Workstream ownership and peer review | Five issues with acceptance criteria |
| 165–180 | Show findings and uncertainty | Three-minute group handover |

## Exercises
1. Change a cloud fraction to 1.0 and rerun into a new directory. Explain excluded observations and coverage.
2. Add a duplicate site/date row. Confirm validation fails rather than double-counting the scene.
3. Move post-event measurements before the evaluation start; observe the coverage failure and discuss date leakage.
4. Add an extreme NDVI value. Confirm it is rejected. Do not clip invalid input silently.
5. Compare threshold candidates using validation counts only. Explain why a high F1 on four synthetic test sites is weak evidence.
6. Design a seasonal baseline and a matched-control RestoreWatch experiment on paper. Identify what the fixture cannot answer.

## Facilitator preparation
Run the demo and tests before the session. Distribute a repository ZIP for participants without Git, and verify Python availability. The core demo needs no network after package setup; with setuptools already installed, `PYTHONPATH=src python -m s2ds_starter demo` also works on Linux/macOS without installation. Reserve real download/authentication work for after the offline workflow succeeds. Do not promise live satellite extraction in this session.

Facilitator prompts: What decision does this alert support? Is NDVI decline equivalent to biodiversity loss? Who holds the test labels? What happens if cloud filtering removes all observations? What evidence would distinguish weather from restoration?
