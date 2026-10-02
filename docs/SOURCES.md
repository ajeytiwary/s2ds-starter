# Real datasets and studies

Checked against publisher/author records on 2 October 2026. Full machine-readable catalogue: [datasets.csv](../resources/datasets.csv). Entries have task, coverage, format, license status and limitations. Published records were verified; downloaded-file execution is separately reported below.

## Start with these
| Track | Resource | Why students should use it |
|---|---|---|
| RestoreWatch: first workshop | [Finnish hydrology/vegetation](https://zenodo.org/records/17301631) | Four small files; independent field measures and restored/pristine treatments |
| RestoreWatch: control design | [Finnish BACI v2](https://zenodo.org/records/13929067) | Restored, drained and pristine comparisons; vegetation recovery |
| RestoreWatch: logger QC | [Forsinard](https://zenodo.org/records/11186744) | Dated water-table/soil-moisture records; missing-value and QC exercises |
| RestoreWatch: EO/field pairing | [Bernadouze](https://zenodo.org/records/7554537) | Published Sentinel-2 indices plus hourly water-table records |
| RestoreWatch: unseen sites | [Five UK bogs](https://catalogue.ceh.ac.uk/documents/85a567a6-0a4a-4dc8-90b9-2fac8d1795a3) | Multi-site hydrology; leave-one-site-out design |
| RestoreWatch: pilot AOI | [Peatland ACTION](https://www.nature.scot/climate-change/nature-based-solutions/peatland-action/peatland-action-resources/peatland-action-open-data) | Restoration locations, hydrology and vegetation resources |
| ForestPulse: preferred imagery | [Official FLOGA GeoTIFFs](https://huggingface.co/datasets/orion-ai-lab/FLOGA-GeoTIFFs) | Georeferenced pre/post fire imagery; expert labels |
| ForestPulse: AOI/scene trace | [FLOGA annotations](https://github.com/Orion-AI-Lab/FLOGA-annotations) | Event polygons and updated scene references |
| ForestPulse: alternate benchmark | [Satellite Burned Area Dataset](https://zenodo.org/records/6597139) | Sentinel-1/2, reference delineations, published folds |
| Optional SAR exercise | [Sen1Floods11](https://github.com/cloudtostreet/Sen1Floods11) | Water segmentation; adjacent skill rather than restoration labels |

## Download small real files

```bash
python scripts/download_data.py finnish-hydrology --list
python scripts/download_data.py finnish-hydrology --output data/raw
python scripts/inspect_real_data.py data/raw/finnish-hydrology --output outputs/real-data-inventory.json
```

Also supported: `finnish-baci`, `forsinard`, `bernadouze`, and `burned-area` (metadata only). The downloader pins record IDs and published MD5 checksums, caps each file at 25 MiB, writes atomically and records SHA-256 provenance. The small Finnish hydrology files are also included in `datasets/finnish-hydrology/` for offline use. It downloads originals; it never invents labels, converts intervention treatment to an event label, or feeds these tables directly to the NDVI classifier. Read the publisher documentation and confirm terms before redistributing.

For large FLOGA imagery, use the official dataset page and choose one event first. Do not download multi-GB archives automatically. The official upstream [README](https://github.com/Orion-AI-Lab/FLOGA) links both the original HDF5 release and newer GeoTIFF release. HDF5 requires hdf5plugin for compression support. Label 2 is ambiguous with respect to the selected event and must be excluded. Record the release and scene IDs; version 1 and version 2 are not interchangeable.

## Access/validation status
Publisher listings and the pinned filenames/checksums were checked. The Finnish hydrology download completed and all four original files matched published MD5 values. Its three CSVs were inventoried successfully. They are bundled under datasets/finnish-hydrology with attribution for offline exercises. All five pinned Zenodo records report CC BY 4.0 in their API metadata. Downloader behavior is also tested with mocked responses; the remaining download recipes have metadata/checksum verification but have not been executed end to end. No real-data model benchmark is claimed.

## Studies to read

1. Sdraka et al. (2024), [FLOGA](https://doi.org/10.1109/JSTARS.2024.3381737). Read dataset construction, masks and splits before model architecture. Student task: simple dNBR baseline against expert masks; event-level holdout. Data license CC BY 4.0 in upstream DATA_LICENSE; code MIT.
2. [Relationship between hydrological restoration and vegetation recovery](https://doi.org/10.1111/1365-2664.70197) (2025); [data](https://doi.org/10.5281/zenodo.17301631). Read treatment design and field-variable definitions. Student task: treatment-specific water-table/vegetation trajectories; separate association from causal attribution.
3. Elo et al., [restoration experiment data v2](https://doi.org/10.5281/zenodo.13929067) and [analysis code](https://doi.org/10.5281/zenodo.13934838). Read ecosystem-type and control structure. Student task: reproduce one published comparison with the author's code before adding EO.
4. [Potential for Peatland Water Table Depth Monitoring Using Sentinel-1 SAR Backscatter: Forsinard](https://www.mdpi.com/2072-4292/15/7/1900) (2023). Read preprocessing, field pairing and validation. Student task: linear/seasonal baseline versus a tree model, with held-out sites/time.
5. [Modelling water table depth at rewetted peatlands with Sentinel-1 and Sentinel-2](https://www.sciencedirect.com/science/article/pii/S2666017225000446) (2025). Read feature/ground-truth alignment and validation design; reported results are study-specific, not targets transferable to new sites.
6. Bonafilia et al. (2020), [Sen1Floods11](https://openaccess.thecvf.com/content_CVPRW_2020/html/w11/Bonafilia_Sen1Floods11_A_Georeferenced_Dataset_to_Train_and_Test_Deep_Learning_CVPRW_2020_paper.html). Read annotation methodology; evaluate human-labelled and weak-labelled samples separately.
7. [NatureScot research report 1362](https://www.nature.scot/doc/naturescot-research-report-1362-developing-toolkit-monitoring-success-peatland-restoration-projects). Read practical monitoring design and site variability before planning an EO service.

## Rights and source quality
NatureScot states OGL v3.0; the five-bog EIDC record states OGL. The rendered Zenodo pages did not expose license values reliably; the API metadata confirmed CC BY 4.0 for the five pinned records. Inspect publisher metadata rather than assuming that “Open” means unrestricted reuse. Cite record DOI/version, creators and modifications. Do not copy an unrelated fork's license to Sen1Floods11 data.

Coordinates, acquisition dates and intervention timing must be checked against raw documentation. Finnish pre-restoration measurements can precede Sentinel-1/2 availability; Bernadouze is a sensor/field pairing resource, not automatically a restoration/control experiment. Flood or fire labels do not establish biodiversity or restoration success.
