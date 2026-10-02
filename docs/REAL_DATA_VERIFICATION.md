# Real-data verification · 2 October 2026

Four Finnish hydrology originals downloaded successfully; all published MD5 checksums matched. Three CSVs inventoried without converting labels. Source API metadata states CC BY 4.0 for each of the five pinned Zenodo records. The study README and raw site table use different singular/plural site filenames; preserved as published.

No EO extraction or predictive real-data performance is claimed. The remaining download recipes were checked against publisher listings and checksums but not executed.

Inventory results:

- `hydrological_data.csv`: 160 rows; columns: ID, Time, WT_ES, WT_MS, pH, EC, ABS, N, P, DOC.
- `sites_data.csv`: 40 rows; columns: ID, N, E, Treatment, Type, Sampling_0, Sampling_2, Sampling_5, Sampling_10.
- `species_groups_data.csv`: 160 rows; columns: ID, Time, Pristine, None, Drainage, Moss_hummock, Moss_lawn, Moss_hollow, Sphagnum_hummock, Sphagnum_lawn, Sphagnum_hollow, Sphagnum_mixed.
