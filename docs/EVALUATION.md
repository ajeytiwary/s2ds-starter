# Frozen evaluation and mentor protocol

## Public worked Finnish example
`resources/finnish_split_v1.json` is frozen before candidate comparison. It uses coordinates only, a 10 km connected-component buffer and a fixed hash ordering, allocating 22 train, 8 validation and 10 test sites. Repeated visits stay with their site; neighboring sites stay with their geographic group. Hash the manifest and reference it in every experiment. The runner rejects altered membership or duplicate allocations.

The worked comparison predicts early-summer WTD at the nominal ten-year sampling stage using (a) each site's pre-restoration measurement as persistence and (b) the median ten-year measurement among training sites. It is a field-only teaching baseline. It does not predict WTD from satellites, estimate daily hydrology or demonstrate restoration causality. Treatment plots show all public observations for learning; they must not be used to claim test blindness. Both validation and test metrics are intentionally public worked answers.

The 10 km buffer is a pragmatic teaching choice rather than a scientifically validated decorrelation distance. It does not encode study-author matched pairs. Before scientific evaluation, obtain matching metadata, group author-defined pairs together, check ecosystem/treatment balance and use sensitivity analyses for buffer/region holdouts.

## ForestPulse worked event
A single event with public reference labels is a demonstration, not an independent multi-event benchmark. Fix a conventional dNBR threshold before examining labels. Exclude clouds, water, nodata and ambiguous/ignore labels where supplied, and report valid coverage. Never tune the threshold on the demonstration's reference mask and present the resulting score as held-out generalization. Keep all patches from the event together for future experiments.

## Mentor-controlled assessment for new experiments
1. Mentor selects a new dataset release, AOIs, intervention/control labels and date ranges. Record licenses, source hashes and independent label provenance.
2. Group repeated visits, overlapping imagery, spatial neighbors and matched intervention/control pairs. Allocate groups using geography/events before examining outcomes. Audit balance and coverage; freeze `split.json` and its SHA-256.
3. Provide training labels and validation labels. Keep test targets in a separate private location outside the student repository. Public-source labels cannot be made genuinely secret by deleting one CSV; use a genuinely new assessment dataset or explicitly call the exercise a public holdout.
4. Students log candidate parameters, source commit and validation results. They submit one frozen prediction artifact and its hash before mentor scoring.
5. Mentor scores test predictions once. Archive predictions, submission timestamp, release/split/input hashes, evaluation code and metrics. Any subsequent test-informed change becomes a new development cycle requiring new held-out evidence.
6. Report site/event counts and confidence intervals clustered at the independent sampling unit. Do not compute narrow confidence intervals by treating neighboring pixels or repeated visits as independent.

Deliverable: `experiment.md`, `split.json`, immutable predictions, provenance and a supported-claims note. Real confidential labels and secrets must never be committed. The repository supplies the public teaching split and protocol; it cannot create confidential third-party ground truth automatically.
