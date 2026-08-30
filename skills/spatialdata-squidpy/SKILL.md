---
name: spatialdata-squidpy
description: Spatial omics workflows with SpatialData and Squidpy alongside scanpy, anndata, and napari-viz. Use when working with Visium, Xenium, CosMx, MERFISH, Slide-seq, spatial transcriptomics, spatial proteomics, tissue images linked to AnnData, spatial neighbor graphs, spatial autocorrelation, ligand-receptor proximity, image features, or napari-spatialdata.
---

# SpatialData + Squidpy

Use this skill for spatial omics analysis in the scverse ecosystem. Prefer it when a task combines expression matrices, spatial coordinates, segmentation labels, microscopy/pathology images, or platform-specific outputs from 10x Visium/Xenium, NanoString CosMx, Vizgen MERFISH, Slide-seq, or related assays.

Reference versions: `spatialdata` 0.8.0, `spatialdata-io` 0.7.1, `squidpy` 1.8.3.

```bash
pip install spatialdata spatialdata-io squidpy
```

## Routing

- Use `scanpy` for ordinary scRNA-seq preprocessing and clustering.
- Use `anndata` when the main issue is object structure, layers, backed mode, or h5ad I/O.
- Use this skill when spatial coordinates, images, regions, or spatial statistics matter.
- Use `napari-viz` for headless rendering/inspection of microscopy volumes or labels.

## The SpatialData Object

A `SpatialData` object holds five element dicts plus a set of named coordinate systems. Elements are not merged into one array; they are co-registered by transformations.

| Attribute | Holds | Type per element |
|---|---|---|
| `sdata.images` | microscopy / H&E rasters | `DataArray` (single scale) or `DataTree` (multiscale) |
| `sdata.labels` | segmentation masks | `DataArray` / `DataTree`, integer-valued |
| `sdata.points` | transcript locations | dask `DataFrame` |
| `sdata.shapes` | circles / polygons | `GeoDataFrame` |
| `sdata.tables` | expression + obs | `AnnData` |
| `sdata.coordinate_systems` | registered systems | `list[str]`, `"global"` by default |

A table is linked to the element it annotates by `adata.uns["spatialdata_attrs"]`: `region` (element name), `region_key` (obs column naming the region), `instance_key` (obs column matching label ids / shape index). `sdata.tables` is a dict — a SpatialData object can carry several tables annotating different elements.

## Reading Platform Data

`spatialdata_io` readers return a `SpatialData` object directly. Every reader takes the run directory as its first argument.

```python
import spatialdata_io as sdio

sdata = sdio.xenium("path/to/xenium_run")        # cells+nucleus boundaries, labels, transcripts, morphology images, table
sdata = sdio.visium("path/to/visium_out")        # spots as circles, hires/lowres images, table
sdata = sdio.visium_hd("path/to/vishd_out", bin_size=[8, 16])
sdata = sdio.merscope("path/to/merscope_out")    # z_layers=3 by default
sdata = sdio.cosmx("path/to/cosmx_out")
```

Other readers: `codex`, `curio`, `dbit`, `macsima`, `mcmicro`, `seqfish`, `steinbock`, `stereoseq`, plus `generic` / `image` / `geojson` for loose files and `xenium_aligned_image(image_path, alignment_file)` for post-hoc aligned images.

Reading a platform run is slow and parses many files. Convert once to Zarr, then read the Zarr from then on:

```python
import spatialdata as sd

sdata.write("run.zarr")                 # overwrite=False by default; raises if the store exists
sdata = sd.read_zarr("run.zarr")
sdata = sd.read_zarr("run.zarr", selection=("images", "tables"))   # partial read
```

After adding an element to a Zarr-backed object, `sdata.write_element("clusters")` persists just that element. Rewriting an element that Dask is already backing from the same store fails — write the object to a new path instead.

## Coordinate Systems and Transformations

This is where spatial analyses go wrong. Elements do not share one pixel grid — each carries a transformation per coordinate system, and the system decides what units your coordinates are in.

```python
from spatialdata.transformations import (
    get_transformation, set_transformation, Identity, Scale, Translation, Affine, Sequence,
)

get_transformation(sdata.images["morphology_focus"])                 # to "global"
get_transformation(sdata.images["morphology_focus"], get_all=True)   # dict per coordinate system

# register the image into a micron-scale system (0.2125 um/px is the Xenium pixel size)
set_transformation(
    sdata.images["morphology_focus"],
    Scale([0.2125, 0.2125], axes=("y", "x")),
    to_coordinate_system="microns",
)
print(sdata.coordinate_systems)          # ['global', 'microns']
```

Check the physical extent before overlaying anything:

```python
sd.get_extent(sdata, coordinate_system="global")   # {'y': (0.0, 512.0), 'x': (0.0, 512.0)}
```

`sdata.transform_element_to_coordinate_system("morphology_focus", "microns")` takes the element *name* and returns the element with coordinates actually resampled; `sdata.filter_by_coordinate_system("microns")` drops elements not registered there.

## Cropping and Querying

```python
crop = sd.bounding_box_query(
    sdata,
    axes=("y", "x"),
    min_coordinate=[0, 0],
    max_coordinate=[256, 256],
    target_coordinate_system="global",
)
```

Every element in `crop` is cut consistently and the table is filtered to the surviving instances (`filter_table=True` by default). `sd.polygon_query(...)` does the same for an arbitrary shape; both are also reachable as `sdata.query.bounding_box(...)` / `sdata.query.polygon(...)`.

## Linking Tables to Elements

```python
# pull a table column onto the element it annotates
values = sd.get_values("channel_0_sum", sdata=sdata, element_name="blobs_labels", table_name="table")

# align element rows and table rows for joint work
elements, table = sd.join_spatialelement_table(
    sdata=sdata, spatial_element_names="blobs_labels", table_name="table", how="left"
)
```

Attaching a new table requires the annotation metadata, or it will not write:

```python
from spatialdata.models import TableModel

adata = TableModel.parse(
    adata, region="cell_labels", region_key="region", instance_key="cell_id"
)
sdata.tables["clusters"] = adata
```

## Spatial Graphs (Squidpy)

`sq.gr.spatial_neighbors` is **deprecated** since squidpy 1.7.0 and is removed in 1.9.0. Use the mode-specific builders. Each takes an `AnnData` or a `SpatialData` — with a SpatialData, name the element and the table:

```python
import squidpy as sq

# cell-resolved platforms (Xenium, MERFISH, CosMx): kNN or Delaunay
sq.gr.spatial_neighbors_knn(
    sdata,
    elements_to_coordinate_systems={"cell_labels": "global"},
    table_key="table",
    n_neighs=6,
)

# Visium-style lattice: grid mode, n_rings controls how far out
sq.gr.spatial_neighbors_grid(adata, n_neighs=6, n_rings=2)

# physical interaction scale rather than a fixed k
sq.gr.spatial_neighbors_radius(adata, radius=30.0)
sq.gr.spatial_neighbors_delaunay(adata)
```

Grid mode assumes an approximately regular lattice — on a Xenium point cloud its ring distances are meaningless. Multi-slide objects need `library_key=` so edges are not built across slides. Results land in `table.obsp["spatial_connectivities"]` and `table.obsp["spatial_distances"]`.

## Spatial Statistics

```python
sq.gr.spatial_autocorr(sdata, table_key="table", mode="moran", n_perms=100, seed=0)
# -> table.uns["moranI"]: I, pval_norm, pval_sim, pval_z_sim + fdr_bh-corrected columns
sq.gr.spatial_autocorr(sdata, table_key="table", mode="geary")

sq.gr.nhood_enrichment(sdata, cluster_key="cluster", table_key="table", n_perms=1000, seed=0)
# -> table.uns["cluster_nhood_enrichment"]

sq.gr.co_occurrence(sdata, cluster_key="cluster", table_key="table", interval=50)
sq.gr.ripley(adata, cluster_key="cluster", mode="L")
sq.gr.ligrec(adata, cluster_key="cluster")
```

`spatial_autocorr` already applies `corr_method="fdr_bh"`; read `pval_norm_fdr_bh` / `pval_sim_fdr_bh`, not the raw p-values. `nhood_enrichment` and `spatial_autocorr` are permutation tests — set `seed=` or results are not reproducible.

Plotting: `sq.pl.nhood_enrichment`, `sq.pl.co_occurrence`, `sq.pl.centrality_scores`, `sq.pl.interaction_matrix`, `sq.pl.ripley`, `sq.pl.ligrec`, `sq.pl.spatial_scatter`, `sq.pl.spatial_segment`, `sq.pl.var_by_distance`.

## Core Workflow

1. Read the run with the platform reader, then `sdata.write("run.zarr")` once and work from the Zarr.
2. Inspect `print(sdata)` — element names, shapes, and the coordinate systems each is registered in.
3. Confirm the units. `get_transformation(..., get_all=True)` and `sd.get_extent(...)` before any overlay or radius.
4. Preprocess the table with Scanpy (QC, normalize, HVGs, PCA, neighbors, UMAP, clustering) — expression preprocessing is not spatial.
5. Build the spatial graph with the mode that matches the geometry (grid for Visium, kNN/Delaunay for cell-resolved).
6. Run the spatial statistics, with `seed=` set.
7. Crop with `bounding_box_query` / `polygon_query` rather than slicing arrays by hand.
8. Write results back: `sdata.write(...)` for the whole object, `sdata.write_element(...)` for a newly added element.

## Quality Checks

- Confirm whether coordinates are pixels, microns, array indices, or platform-specific units; a radius in the wrong system is silently wrong, not an error.
- Check image origin and axis orientation before overlaying labels or points — `sd.get_extent` per coordinate system.
- `region` / `region_key` / `instance_key` must be set on every table, or the table will not write and cannot be joined to its element.
- Keep tissue masks and segmentation labels versioned; most downstream errors come from silent coordinate or mask mismatch.
- Stratify spatial statistics by sample/slide (`library_key=`); do not pool slides unless batch and geometry are comparable.
- Report neighborhood graph parameters — mode, `n_neighs`/`radius`/`n_rings`, coordinate system — because they strongly affect spatial-enrichment calls.
- Permutation-based results (`nhood_enrichment`, `spatial_autocorr`, `ligrec`) need `seed=` and `n_perms=` reported.
