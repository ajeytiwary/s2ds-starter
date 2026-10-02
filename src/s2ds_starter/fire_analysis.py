"""Single-event, retrospective optical change demonstration on real imagery."""
import hashlib
import json
from pathlib import Path
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject


def normalized_difference(a, b):
    denominator = a+b
    return np.divide(a-b, denominator, out=np.full(a.shape, np.nan, dtype='float32'), where=np.isfinite(denominator)&(np.abs(denominator)>1e-8))


def confusion(reference, predicted, valid):
    if not np.any(valid):
        raise ValueError('No valid pixels')
    y, p = reference[valid], predicted[valid]
    tp=int(np.sum(y&p));fp=int(np.sum(~y&p));fn=int(np.sum(y&~p));tn=int(np.sum(~y&~p))
    return dict(valid_pixels=int(valid.sum()),tp=tp,fp=fp,fn=fn,tn=tn,
                precision=tp/(tp+fp) if tp+fp else 0,recall=tp/(tp+fn) if tp+fn else 0,
                f1=2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 0,
                iou=tp/(tp+fp+fn) if tp+fp+fn else 0)


def run_fire(directory, output, threshold=0.1):
    directory,output=Path(directory),Path(output)
    output.mkdir(parents=True,exist_ok=True)
    manifest=json.loads((directory/'source_manifest.json').read_text())
    for entry in manifest['files']:
        if hashlib.sha256((directory/entry['filename']).read_bytes()).hexdigest()!=entry['sha256']:
            raise ValueError('Source hash mismatch')
    pre_path=directory/'sentinel2_2017-07-14.tiff';post_path=directory/'sentinel2_2017-08-23.tiff'
    label_path=directory/'EMSR226_01DABA_02GRADING_MAP_v1_vector_mask.tiff'
    with rasterio.open(pre_path) as a,rasterio.open(post_path) as b,rasterio.open(label_path) as l:
        if (a.crs,a.transform,a.shape)!=(b.crs,b.transform,b.shape):
            raise ValueError('Pre/post image grids do not match')
        if a.count!=13 or b.count!=13:
            raise ValueError('Expected 12 spectral bands plus validity band')
        pre,post=a.read().astype('float32'),b.read().astype('float32')
        # Dataset author code maps zero-based 7/11 to B08/B12; last band is data validity.
        raw_label=l.read(1)
        pixel_alignment_assumed = l.crs is None and l.shape == a.shape
        aligned = pixel_alignment_assumed or (l.crs,l.transform,l.shape)==(a.crs,a.transform,a.shape)
        if l.crs is None and not pixel_alignment_assumed:
            raise ValueError('Unreferenced label dimensions must match the paired source imagery')
        if not aligned:
            labels=np.full(a.shape,255,dtype='uint8')
            reproject(raw_label,labels,src_transform=l.transform,src_crs=l.crs,
                      dst_transform=a.transform,dst_crs=a.crs,resampling=Resampling.nearest,
                      src_nodata=l.nodata,dst_nodata=255)
        else:
            labels=raw_label
        profile=a.profile.copy();bounds=list(a.bounds);crs=str(a.crs)
        # Validity bands indicate data availability, not cloud/snow/water classification.
        valid=(pre[12]>0)&(post[12]>0)&np.all(np.isfinite(pre[:12]),axis=0)&np.all(np.isfinite(post[:12]),axis=0)
        if l.nodata is not None:
            valid &= labels!=l.nodata
        valid &= (labels>=0)&(labels<=255)
        nbr_pre=normalized_difference(pre[7],pre[11]);nbr_post=normalized_difference(post[7],post[11])
        dnbr=nbr_pre-nbr_post
        ndvi_change=normalized_difference(pre[7],pre[3])-normalized_difference(post[7],post[3])
        valid &= np.isfinite(dnbr)&np.isfinite(ndvi_change)
        reference=labels>=37 # Author baseline: 0..36 unburned, 37..255 burned severity.
        predicted=dnbr>=threshold
    m=confusion(reference,predicted,valid)
    m.update(event='EMSR226_01DABA',pre_date='2017-07-14',post_date='2017-08-23',threshold=threshold,
             total_pixels=int(valid.size),valid_fraction=float(valid.mean()),label_reprojected=not aligned,label_pixel_alignment_assumed=pixel_alignment_assumed,
             crs=crs,bounds=bounds,reference_classes=np.unique(raw_label).tolist(),
             role='single public event demonstration; no independent event holdout',
             limitations=['No dedicated cloud/snow/water masks supplied for this event; band 13 is data validity, not cloud-free evidence.',
                          'Acquisition dates are known from dataset filenames; original Sentinel product identifiers are not supplied in this bundle.',
                          'Reference severity mask has no CRS; pixel alignment is assumed from its paired event/file dimensions following author loading code, not independently verified. Exported reference inherits the image grid.',
                          'Fixed teaching threshold 0.1 chosen before scoring; not calibrated on independent events. No pixel-independent confidence interval.'])
    profile.update(count=1,compress='deflate',dtype='float32',nodata=-9999)
    for name,data in [('dnbr.tif',dnbr),('ndvi_departure.tif',ndvi_change)]:
        with rasterio.open(output/name,'w',**profile) as dst:
            dst.write(np.where(valid,data,-9999).astype('float32'),1)
    profile.update(dtype='uint8',nodata=255)
    with rasterio.open(output/'predicted_burn.tif','w',**profile) as dst:
        dst.write(np.where(valid,predicted.astype('uint8'),255),1)
    with rasterio.open(output/'reference_burn.tif','w',**profile) as dst:
        dst.write(np.where(valid,reference.astype('uint8'),255),1)
    with rasterio.open(output/'valid_mask.tif','w',**dict(profile,nodata=None)) as dst:
        dst.write(valid.astype('uint8'),1)
    (output/'metrics.json').write_text(json.dumps(m,indent=2)+'\n')
    (output/'provenance.json').write_text(json.dumps(dict(source=manifest,band_mapping={'NIR':'B08 at band 8','SWIR2':'B12 at band 12','red':'B04 at band 4','validity':'band 13'},threshold=threshold,code='fire_analysis.py',code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
    footprint={'type':'FeatureCollection','features':[{'type':'Feature','properties':{'event':m['event'],'pre_date':m['pre_date'],'post_date':m['post_date'],'geometry_role':'imagery bounding box, not fire perimeter'},'geometry':{'type':'Polygon','coordinates':[[[bounds[0],bounds[1]],[bounds[2],bounds[1]],[bounds[2],bounds[3]],[bounds[0],bounds[3]],[bounds[0],bounds[1]]]]}}]}
    if crs!='EPSG:4326':
        raise ValueError('This fixed demonstration expects WGS84 imagery for GeoJSON')
    (output/'aoi.geojson').write_text(json.dumps(footprint,indent=2)+'\n')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(1,4,figsize=(15,4))
    extent=[bounds[0],bounds[2],bounds[1],bounds[3]]
    rgb=np.moveaxis(post[[3,2,1]],0,-1)
    rgb=np.clip(rgb/np.nanpercentile(rgb,98),0,1)
    axes[0].imshow(rgb,extent=extent);axes[0].set_title('Post-fire · 23 Aug 2017')
    image=axes[1].imshow(np.where(valid,dnbr,np.nan),vmin=-.3,vmax=.7,cmap='RdYlGn_r',extent=extent);axes[1].set_title('dNBR (pre minus post)');fig.colorbar(image,ax=axes[1],shrink=.7)
    axes[2].imshow(np.where(valid,reference,np.nan),vmin=0,vmax=1,cmap='gray_r',extent=extent);axes[2].set_title('Published reference · burn=black')
    axes[3].imshow(np.where(valid,predicted,np.nan),vmin=0,vmax=1,cmap='gray_r',extent=extent);axes[3].set_title('Fixed threshold · burn=black')
    for ax in axes:ax.set(xlabel='Longitude',ylabel='Latitude');ax.tick_params(labelsize=7)
    fig.suptitle('Daba, Georgia · real Sentinel-2 demonstration · cloud status unverified')
    fig.tight_layout();fig.savefig(output/'map.png',dpi=150);plt.close(fig)
    (output/'report.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>ForestPulse real event</title><h1>ForestPulse · Daba, Georgia</h1><p>Real Sentinel-2 images and published reference. One public event; cloud status unverified. This demonstrates a workflow, not product accuracy.</p><img style="max-width:100%" src="map.png" alt="Post-fire imagery, dNBR, reference and prediction"><pre>'+json.dumps(m,indent=2)+'</pre><p><a href="predicted_burn.tif">Prediction GeoTIFF</a> · <a href="aoi.geojson">Imagery footprint</a> · <a href="provenance.json">Provenance</a></p></html>')
    return m
