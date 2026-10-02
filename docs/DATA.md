# Input data contract (CSV, UTF-8)

## sites.csv
`site_id,event_label,evaluation_start,source`

One row per site; binary `event_label` (0/1), ISO date `evaluation_start`, and a nonempty source/citation. Evaluation start is a monitoring cutoff, not necessarily the true onset. Labels must come from independent references, not the index being evaluated. All sites need enough observations on both sides of their cutoff.

## features.csv
`site_id,date,ndvi,cloud_fraction,scene_id,source`

Unique site/date; finite NDVI in [-1,1], cloud fraction in [0,1], ISO date, nonempty scene ID/source. Observations with cloud fraction >0.4 are excluded. At least three valid pre-cutoff and two valid on/after-cutoff observations are required per site. The score is pre-cutoff mean NDVI minus the mean of the final two post-cutoff NDVI values. This is an educational, retrospective site-level detector, not a calibrated near-real-time alert system.

The baseline split sorts site IDs and assigns successive sites to train/validation/test (four each in the demo). This deterministic split is only a starting point: real studies must freeze geographically separated or cluster-aware partitions, avoid shared pixels, and account for season, site selection and intervention matching. Both validation and test require positive and negative labels. Validation picks among thresholds 0.05, 0.10, 0.15, 0.20, 0.25; F1 ties prefer the higher threshold.

## Real source catalogue requirements
Record AOI geometry/CRS, owner/license, site ID, intervention/control status, intervention dates, ground-truth variable/units/method, label annotator, satellite product IDs, acquisition/processing dates, cloud masks, radar orbit/polarization, weather grid/time aggregation, feature code version and split membership. None of these may be replaced with synthetic values in a real validation report.

Archive raw immutable inputs separately, obey redistribution restrictions, and record SHA-256 hashes. Input hashes prove byte identity, not correctness. The provenance manifest records the code version and Git commit when available. Event labels are included in this educational fixture; arrange a mentor-controlled label release for a genuinely blind evaluation.
