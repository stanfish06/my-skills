---
name: cell-detection
description: Cell segmentation in fluorescence microscopy images. Supports Cellpose/cpsam (Cellpose 4.0) with additional backends
  planned. Produces segmentation masks, per-cell morphology metrics (area, diameter, centroid, eccentricity), overlay figures,
  and a report.md.
license: MIT
metadata:
  version: 0.1.0
  author: ClawBio
  tags:
  - microscopy
  - segmentation
  - cellpose
  - fluorescence
  - imaging
  - cell-biology
  openclaw:
    requires:
      bins:
      - python3
    always: false
    emoji: 🔬
    homepage: https://github.com/ClawBio/ClawBio
    os:
    - darwin
    - linux
    install:
    - kind: pip
      package: cellpose>=4.0
    - kind: pip
      package: tifffile
    - kind: pip
      package: czifile>=2019.7.2.2
    - kind: pip
      package: nd2>=0.11.1
    - kind: pip
      package: Pillow
    - kind: pip
      package: scikit-image
    trigger_keywords:
    - cellpose
    - cpsam
    - cell segmentation
    - nucleus segmentation
    - fluorescence microscopy
    - microscopy image
    - image segmentation
    - cell counting
    - segmentation mask
---

# 🔬 Cell Segmentation

You are the **cell-detection** agent, a specialised ClawBio skill for cell
segmentation in fluorescence microscopy images. The default backend is `cpsam`
(Cellpose 4.0); additional backends (e.g. StarDist) are planned.

## Why This Exists

Manual cell counting and segmentation are slow, inconsistent, and hard to reproduce.

- **Without it**: Users open ImageJ, draw ROIs by hand, export CSVs with no provenance.
- **With it**: One command segments cells, extracts morphology metrics, saves an overlay figure, and writes a reproducible `report.md`.
- **Why ClawBio**: Fully local, no data upload, structured outputs ready for downstream analysis.

## Core Capabilities

1. **Segment**: Run `cpsam` on TIFF, CZI, ND2, PNG, or JPG fluorescence images
2. **Measure**: Extract area, equivalent diameter, centroid, and eccentricity per cell
3. **Report**: Produce `report.md`, `{stem}_measurements.csv`, and histogram figures
4. **Execution control**: GPU auto by default, with explicit `--use_gpu` / `--use_cpu` override flags

## Input Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| Greyscale TIFF | `.tif`, `.tiff` | H×W — passed directly |
| 2-channel TIFF | `.tif`, `.tiff` | H×W×2 — cytoplasm + nuclear, any order |
| 3-channel TIFF | `.tif`, `.tiff` | H×W×3 — H&E or fluorescence, any order |
| >3-channel TIFF | `.tif`, `.tiff` | First 3 channels used; remainder truncated with warning |
| Zeiss microscopy | `.czi` | Reads CZI via `czifile` and uses CZI axis metadata (`CziFile.axes`) to map C/Z/Y/X deterministically |
| Nikon microscopy | `.nd2` | Reads ND2 via `nd2` and uses ND2 named dimensions (`ND2File.sizes`) for deterministic C/Z/Y/X mapping |
| PNG / JPEG | `.png`, `.jpg`, `.jpeg` | Greyscale or RGB |

**Channel handling:** cpsam is channel-order invariant for 2D inputs — cytoplasm and nuclear channels can be in any order. For 2D segmentation, if you have more than 3 channels, the first 3 are used and the rest are truncated with a warning. For 3D segmentation (`--do_3D`) with `--z_projection none`, 4D stacks are preserved as `Z×C×Y×X` (no channel truncation at load time).

## Workflow

1. **Load** image; detect greyscale vs multi-channel
2. **Prepare**
   - 2D mode: pass 1–3 channels through unchanged; truncate >3 to first 3 with a warning
   - 3D mode (`--do_3D` + `--z_projection none`): keep 4D volume as `Z×C×Y×X`
3. **Segment** with `CellposeModel()`
   - 2D mode: no explicit channel mapping needed
   - 3D multichannel mode: call with `z_axis=0`, `channel_axis=1`
   - Device mode: defaults to GPU-auto; `--use_cpu` forces CPU
4. **Metrics** via `skimage.measure.regionprops`
5. **Figures** — overlay + size distribution histogram
6. **Report** — `report.md` + `{stem}_measurements.csv` + reproducibility bundle (`commands.sh`, `environment.yml`, `checksums.sha256`)

## CLI Reference

```bash
# Standard usage — greyscale or multi-channel (cpsam handles channels automatically)
python skills/cell-detection/cell_detection.py \
  --input <image.tif> --output <report_dir>

# Override diameter estimate (pixels)
python skills/cell-detection/cell_detection.py \
  --input <image.tif> --diameter 30 --output <report_dir>

# Demo (synthetic image, no user file needed)
python skills/cell-detection/cell_detection.py --demo --output /tmp/cell_detection_demo

# Override 4D stack Z handling (default is max projection)
python skills/cell-detection/cell_detection.py \
  --input <image.nd2> --z_projection none --do_3D --output <report_dir>

# Force CPU mode
python skills/cell-detection/cell_detection.py \
  --input <image.tif> --use_cpu --output <report_dir>
```

## Demo

```bash
python skills/cell-detection/cell_detection.py --demo --output /tmp/cell_detection_demo
```

Expected output: report.md with ~67 cells detected from a synthetic 512×512 blob image (67 blobs generated).

## Algorithm / Methodology

1. Load image with `tifffile` (TIFF), `czifile` (CZI), `nd2` (ND2), or `PIL` (PNG/JPG); use CZI/ND2 metadata axes to assign C/Z/Y/X
2. Channel preparation:
   - 2D mode: if >3 channels, truncate to first 3 with a warning
   - 3D mode with `--z_projection none`: preserve 4D volume as `Z×C×Y×X`
3. Instantiate `CellposeModel(gpu=<flag>)`
4. Call `model.eval(img, diameter=<arg_or_None>)`
   - 2D: no `channels`/`channel_axis` needed (cpsam is channel-order invariant)
   - 3D `Z×C×Y×X`: pass `z_axis=0`, `channel_axis=1`
5. Extract per-cell stats from `masks` via `skimage.measure.regionprops`
6. Save `{stem}_measurements.csv`, figures, `report.md`

**Key parameters**:
- Model: `cpsam` (Cellpose 4.0 unified model — channel-order invariant)
- Channels:
  - 2D: channel-order invariant; first 3 channels are used when input has >3 channels
  - 3D with `--z_projection none`: multichannel 4D stacks are kept as `Z×C×Y×X`
- Diameter: `None` leaves the image at native scale; a positive value rescales objects toward Cellpose's 30-pixel training diameter
- 4D stack policy:
  - `--z_projection max` (default): max-project over Z while preserving channels for 2D segmentation (`H×W×C`)
  - `--z_projection none`: preserve Z; 4D stacks remain volumetric (`Z×C×Y×X`) for 3D segmentation
- 3D guardrails:
  - `--do_3D` requires volumetric input (`Z×Y×X` or `Z×C×Y×X`)
  - non-volumetric input with `--do_3D` falls back to 2D mode when safe, otherwise errors

## Notes

- Measurements are reported in pixel units (px, px²). Physical calibration metadata (um/pixel) is not currently propagated into per-cell metrics.
- For volumetric segmentation outputs, outlines PNG is replaced with a note file (`{stem}_cp_outlines_unavailable.txt`) because Cellpose does not emit 3D outlines PNGs.

## Example Queries

- "Segment the cells in my DAPI image"
- "How many cells are in this microscopy image?"
- "Run cellpose on my TIFF and give me a cell count"
- "Segment my fluorescence image and export morphology metrics"

## Output Structure

```
output_dir/
├── report.md
├── {stem}_measurements.csv
├── {stem}_cp_masks.tif
├── {stem}_seg.npy
├── figures/
│   ├── {stem}_cp_outlines.png
│   └── {stem}_histogram.png
└── reproducibility/
    ├── checksums.sha256
    ├── commands.sh
    └── environment.yml
```

## Dependencies

- `cellpose>=4.0` — cpsam model
- `tifffile` — TIFF I/O
- `czifile>=2019.7.2.2` — Zeiss CZI I/O (manually verified with 2019.7.2.2)
- `nd2>=0.11.1` — Nikon ND2 I/O (manually verified with 0.11.1)
- `Pillow` — PNG/JPG loading
- `numpy` — array ops
- `matplotlib` — figures
- `scikit-image` — regionprops metrics

## Safety

- Local-first: no image data leaves the machine
- Every report includes the ClawBio medical disclaimer
- Reproducibility bundle (`commands.sh`, `environment.yml`, `checksums.sha256`) records the exact invocation, dependencies, and output integrity

## Integration with Bio Orchestrator

**Trigger conditions**:
- Input is a TIFF/PNG/JPG microscopy image
- User mentions "cellpose", "segment", "cell counting", "microscopy"

**Chaining partners**:
- Future: export ROI centroids to spatial transcriptomics workflows

## Citations

- [Pachitariu, Rariden & Stringer (2025) *Cellpose-SAM: superhuman generalization for cellular segmentation*. bioRxiv 2025.04.28.651001](https://doi.org/10.1101/2025.04.28.651001) — CellposeSAM / cpsam model
