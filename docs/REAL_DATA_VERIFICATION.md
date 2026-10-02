# Real-data verification · 2 October 2026

Four Finnish hydrology originals downloaded successfully; all published MD5 checksums matched. Three CSVs inventoried without converting labels. Source API metadata states CC BY 4.0 for each of the five pinned Zenodo records. The study README and raw site table use different singular/plural site filenames; preserved as published.

The original ingestion check covered field tables. The worked field baseline and real optical event below are now executed; satellite-to-WTD modelling remains unimplemented. Finnish hydrology and burned-area metadata downloads were executed; the other recipes were checked against listings/checksums but not executed.

Inventory results:

- `hydrological_data.csv`: 160 rows; columns: ID, Time, WT_ES, WT_MS, pH, EC, ABS, N, P, DOC.
- `sites_data.csv`: 40 rows; columns: ID, N, E, Treatment, Type, Sampling_0, Sampling_2, Sampling_5, Sampling_10.
- `species_groups_data.csv`: 160 rows; columns: ID, Time, Pristine, None, Drainage, Moss_hummock, Moss_lawn, Moss_hollow, Sphagnum_hummock, Sphagnum_lawn, Sphagnum_hollow, Sphagnum_mixed.

## Worked additions

Field join and baseline: 40 sites / 160 rows; frozen 10 km geographic-group split; descriptive treatment plots and field-only baseline errors. Real ForestPulse event: Daba, Georgia, 14 July / 23 August 2017 Sentinel-2 imagery; source event EMSR226; reference mask and member CRC/size plus bundled SHA-256 hashes verified. Source archive was only retrieved in selected ranges, so its full MD5 was not verified.

All 16 tests pass locally. GitHub CI run 37026778502 passed all six jobs: full Jupyter execution of all four notebooks; tests and real examples on Linux/Python 3.10, 3.11, 3.12 and 3.13; and Windows/Python 3.12. Run: https://github.com/ajeytiwary/s2ds-starter/actions/runs/37026778502 . Local notebook cells were additionally executed in process because local socket restrictions block Jupyter kernel startup.

Scientific limits remain explicit: public labels, single optical event, missing dedicated cloud masks, reference pixel alignment assumed, no original scene product IDs, no end-to-end satellite-to-WTD or causal model.
