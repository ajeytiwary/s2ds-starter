# Facilitator worked answers

## Offline exercises
Duplicate site/date and invalid NDVI inputs must fail. Cloud fraction 1 removes an observation; enough excluded observations must fail coverage. Changing test labels must not change the chosen threshold. NDVI decline is not evidence of biodiversity loss, and a water segmentation label is not WTD ground truth.

## Finnish joins and QC
Join site metadata on ID and longitudinal tables on ID/Time. Expect 40 sites, 160 hydrology rows, 160 vegetation rows and 160 joined rows. The originals use semicolon delimiters. Missing counts: WT_ES=1, WT_MS=1 and each of pH/EC/ABS/N/P/DOC=2. Unknown IDs, duplicate keys and mismatched longitudinal keys fail validation. Sphagnum cover sums the four published Sphagnum groups; it is a descriptive species-group feature, not biodiversity richness.

WT is in cm and negative below the surface. Mean early-summer change from stage 0 to 10 is approximately +13.02 cm for 24 restored sites and -1.91 cm for 15 pristine sites with complete paired measurements. Positive means shallower. The simple site-bootstrap intervals are exploratory and assume independent sites; spatial dependence and ecosystem differences undermine a causal reading. These numbers are a teaching calculation, not a reproduction of the study's full statistical model.

## Frozen baseline answers
The geographic split has 22 train / 8 validation / 10 test sites in 19 components. The train ten-year WTD median is -15.115 cm. Validation MAE: persistence 9.5675 cm; train median 6.52 cm. Public test MAE: persistence 11.686 cm; train median 6.565 cm. A more accurate pooled baseline does not establish a useful EO model; it uses no satellite features. The held-out site supplies its own stage-0 measurement for persistence; target-stage observations are never used to fit that baseline.

## AOI and claims
EPSG:4258 is the publisher's stated CRS. The README also says approximate WGS84; resolve coordinate transformations and spatial precision rather than silently relabelling. Sampling_0/2/5/10 are vegetation sampling years, not exact restoration dates. Early visits can predate Sentinel-1/2. Do not invent scenes or interventions to produce a finished-looking benchmark.

## Mentor blind evaluation
The bundled original labels and worked scores are public. This package cannot make them confidential. The mentor protocol must use new/private assessment labels or be honestly described as a public holdout. Review predictions/hash before test scoring, and cluster uncertainty at site/event level.

## Real Daba fire demonstration

The fixed dNBR threshold 0.1 produces 66,113 true positives, 108,870 false positives, 387 false negatives and 168,187 true negatives over 343,557 available-data pixels. F1 is approximately 0.548 and IoU 0.377. The weak precision is useful teaching evidence: a fixed spectral threshold and available-data mask do not provide reliable real-world alerts. Visible smoke, seasonal differences and reference/pixel alignment need investigation. No confidence interval based on independent pixels is reported. Do not raise the threshold using this public label mask and then claim unseen-event performance.

Source labels are severity values 0, 64, 128 and 192; the author baseline maps 0–36 to unburned and 37–255 to burned. The mask has no CRS; source dimensions match the imagery (531 × 647), and the runner records its pixel-alignment assumption. This assumption should be independently checked before spatial validation claims.
