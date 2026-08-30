---
name: claw-ancestry-pca
description: Ancestry decomposition PCA against the Simons Genome Diversity Project
license: MIT
metadata:
  version: 0.1.0
  author: Manuel Corpas
  tags:
  - population-genetics
  - PCA
  - ancestry
  - SGDP
  - global-diversity
  inputs:
  - name: vcf
    type: file
    format:
    - vcf
    - vcf.gz
    description: VCF file with genotype data for your study cohort
  - name: pop-map
    type: file
    format:
    - tsv
    - txt
    description: Tab-separated file mapping sample IDs to population labels
  outputs:
  - name: figure
    type: file
    format: png
    description: Multi-panel PCA composite figure showing ancestry decomposition
  - name: report
    type: file
    format: markdown
    description: Ancestry analysis report with population assignments and statistics
  openclaw:
    category: bioinformatics
    emoji: 🧬
    homepage: https://github.com/ClawBio/ClawBio
    os:
    - darwin
    - linux
    min_python: '3.9'
    dependencies:
    - pandas
    - numpy
    - matplotlib
    - scikit-learn
    requires:
      bins:
      - python3
    always: false
---

# 🦖 Ancestry Decomposition PCA

Compute a principal-component decomposition of your own cohort's genotypes from a VCF, coloured by population label, and write a report plus a 4-panel figure.

## What it does

1. Takes your VCF + optional population map as input
2. Parses genotypes into a sample × variant matrix (0/1/2, `-1` missing)
3. Mean-imputes missing genotypes per variant
4. Runs `sklearn.decomposition.PCA` on that matrix
5. Generates a 4-panel figure:
   - **Panel A**: PC1 vs PC2
   - **Panel B**: PC2 vs PC3
   - **Panel C**: PC1 vs PC3
   - **Panel D**: Scree plot — per-PC and cumulative variance explained
6. Produces `report.md`, `result.json`, and `tables/` with PC coordinates and variance explained

## Scope and limits

Read these before interpreting the output.

- **Single cohort only.** No reference panel ships with this skill and none is downloaded. Samples are not placed in global context, and the figure has no reference-vs-cohort marker distinction and no confidence ellipses.
- **No PLINK, no bcftools.** The script never shells out; PCA is computed in-process with scikit-learn.
- **No Patterson standardisation.** Genotypes are not divided by `sqrt(p(1-p))`, so PCs are not on the standard population-genetics scale.
- **No LD pruning and no relatedness (IBD) filtering.** Prune and remove related individuals upstream — otherwise PCs will track LD blocks and cryptic relatedness rather than ancestry.
- **No contig-name normalisation.** Supply one consistent naming scheme (`chr1` or `1`).

## Requirements

The script imports `clawbio.common` (VCF parsing, checksums, report helpers) from three directory levels above itself, and reads its demo data from `examples/`. Both come from https://github.com/ClawBio/ClawBio — run this skill from inside a ClawBio checkout, or put `clawbio/` and `examples/` on that path. Without them the script fails at import.

## Usage

```bash
python ancestry_pca.py \
    --input your_cohort.vcf.gz \
    --pop-map your_populations.csv \
    --output ancestry_report
```

Omit `--output` for a text summary on stdout. `--pop-map` is a CSV/TSV with `sample_id` and `population` columns; unmapped samples are labelled `UNKNOWN`.

### Demo

```bash
python ancestry_pca.py --demo --output demo_report
```

The demo runs on `examples/demo_populations.vcf` from the ClawBio checkout — 50 samples, 500 variants, 5 population labels.

## Example Output

Verbatim from `--demo`:

```
Parsing VCF...
  50 samples, 500 variants
  Populations: AFR (n=8), AMR (n=5), EAS (n=7), EUR (n=22), SAS (n=8)
Computing PCA (10 components)...
  PC1: 7.6%  PC2: 4.9%
Generating figures...
Generating report...

Done.
  Report: demo_report/report.md
  Figures: demo_report/figures
```

Written under the output directory:

```
report.md
result.json
figures/pca_composite.png
tables/pc_coordinates.csv
tables/variance_explained.csv
```

## Interpretation Guide

- **PC1/PC2** capture the largest axes of variation *in the supplied cohort* — with no reference panel these are cohort-relative, not global, axes
- Variance explained is low and spread across many PCs when the cohort is genetically homogeneous; check Panel D before reading structure into A–C
- Unstandardised, unpruned PCs are sensitive to LD blocks and relatedness — confirm both were handled upstream before calling a cluster "ancestry"

## Citation

If you use this skill in a publication, please cite:

- Corpas, M. (2026). ClawBio. https://github.com/ClawBio/ClawBio
