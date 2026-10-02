# Real imagery and burn reference

Colomba, L.; Farasin, A.; Monaco, S.; Greco, S.; Garza, P.; Apiletti, D.; Baralis, E.; Cerquitelli, T. (2022). Satellite Burned Area Dataset. Zenodo. https://doi.org/10.5281/zenodo.6597139

Related paper: A Dataset for Burned Area Delineation and Severity Estimation from Satellite Imagery. CIKM 2022. https://doi.org/10.1145/3511808.3557528

CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ (confirmed via Zenodo record API). Contains Copernicus Sentinel data (2017); reference event: https://mapping.emergency.copernicus.eu/activations/EMSR226/ .

The two Sentinel-2 TIFFs, reference mask and supplied coverage PNGs are unchanged members of part5.zip. Member byte lengths and ZIP CRC32 were verified; SHA-256 hashes are recorded. The whole 1.5 GB archive was not downloaded and its MD5 was not checked. The source manifest and event metadata JSON were added by MeasureNature.

Reference mask has no CRS but matches both imagery arrays in shape; the worked runner explicitly assumes pixel alignment following the dataset author loader. Its exported reference derives georeferencing from the imagery; this derived file is a modification and should not be described as the original reference geometry. Cloud/snow/water masks are not supplied for this event. Coverage/validity does not prove cloud-free acquisition. Original Sentinel product IDs are not available in the bundle; retain the known acquisition dates without inventing scene IDs.
