# Real-data workshop: field evidence before model fitting

Use the Finnish hydrology dataset for a small download, Forsinard for logger QC, or Bernadouze for optical/field pairing. Follow SOURCES.md download commands. This is a schema and study-design exercise; it does not bypass independent-label requirements in DATA.md.

## 60–90 minute extension
1. Download originals, verify checksums, retain manifest and open the publisher README.
2. Run the inventory script; inspect delimiter, columns, row counts, missing markers and previews.
3. For Finnish hydrology join `sites_data.csv` to hydrology/species tables on `ID`; longitudinal tables also use `Time`. The publisher README calls its site file `site_data.csv`, while the download is named `sites_data.csv`; retain the actual filename and document the discrepancy.
4. Confirm coordinates/CRS. The README lists EPSG:4258 and uses approximate WGS84 wording: resolve CRS deliberately before making an AOI, rather than relabelling coordinates.
5. Keep `WT_ES` and `WT_MS` in cm, with negative values below the surface. Sampling years are vegetation visit years; do not assume exact restoration dates from them.
6. Count treatments, ecosystem types and repeated site observations. Identify whether site clusters or controls cross proposed partitions.
7. For Forsinard treat -9999 as missing and apply the published QC flags before aggregation. Never treat missing data as deep water table.
8. For Bernadouze document aggregation of hourly WTD and its spatial match to vegetation-specific Sentinel-2 indices. Do not merge nearest timestamps without a tolerance and coverage rule.
9. Produce a one-page feasibility note: question, available labels, AOI/date overlap, unresolved license/coordinates, split design, supported claims and next extraction task.

## Extension to a real benchmark
Build dedicated hydrological regression or event-mask adapters; the current CSV CLI only accepts its own site-level NDVI contract. For WTD report MAE/RMSE in explicit units, seasonal-baseline comparison and held-out-site results. For fire masks report event-level IoU/F1, cloud/water/ambiguous-pixel exclusions and spatial footprints. No direct converter is supplied because forcing treatment labels into “event_label” would produce misleading metrics.

Mentor acceptance: all file bytes verified, columns explained using source documentation, no fabricated scene IDs/intervention dates, overlap and rights confirmed, and benchmark task chosen before model selection.
