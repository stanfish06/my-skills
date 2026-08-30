---
name: claw-metagenomics
description: Shotgun metagenomics profiling — taxonomy, resistome, and functional pathways
license: MIT
metadata:
  version: 0.1.0
  author: Manuel Corpas
  tags:
  - metagenomics
  - antimicrobial-resistance
  - taxonomy
  - functional-profiling
  - environmental
  - WHO-critical-ARGs
  inputs:
  - name: r1
    type: file
    format:
    - fastq
    - fastq.gz
    - fq
    - fq.gz
    description: Forward reads (paired-end FASTQ R1)
  - name: r2
    type: file
    format:
    - fastq
    - fastq.gz
    - fq
    - fq.gz
    description: Reverse reads (paired-end FASTQ R2)
  - name: input
    type: file
    format:
    - fastq
    - fastq.gz
    - fq
    - fq.gz
    description: Single concatenated or interleaved FASTQ (alternative to R1+R2)
  outputs:
  - name: taxonomy_report
    type: file
    format: tsv
    description: Bracken-adjusted species-level taxonomy abundance table
  - name: resistome_profile
    type: file
    format: tsv
    description: RGI/CARD antimicrobial resistance gene hits with WHO priority classification
  - name: functional_pathways
    type: file
    format: tsv
    description: HUMAnN3 pathway abundance table (MetaCyc/UniRef)
  - name: figures
    type: directory
    format:
    - png
    - pdf
    description: Publication-quality figures (taxonomy bar chart, resistome heatmap, WHO-critical ARG summary)
  - name: reproducibility
    type: directory
    description: commands.sh, environment.yml, checksums.sha256
  openclaw:
    category: bioinformatics
    emoji: 🦠
    homepage: https://github.com/ClawBio/ClawBio
    os:
    - darwin
    - linux
    min_python: '3.9'
    dependencies:
    - pandas
    - numpy
    - matplotlib
    - seaborn
    - scipy
    - biopython
    system_dependencies:
    - kraken2
    - bracken
    - rgi
    - humann
    requires:
      bins:
      - python3
    always: false
---

# Shotgun Metagenomics Profiler

> [!note] Vault audit 2026-07-24 — USE-15
> Use this as the single-command shotgun runner emphasizing WHO-critical antimicrobial-resistance (resistome) profiling alongside Bracken/HUMAnN; when you need host-read depletion before profiling use `metagenomics`. Single-command AMR/resistome-focused runner vs host-depletion-aware workflow is the distinguishing axis (these overlap but are not duplicates).

Comprehensive shotgun metagenomics analysis combining taxonomic classification, antimicrobial resistance gene detection, and functional pathway profiling from paired-end FASTQ files.

## What it does

1. Takes paired-end FASTQ files (R1, R2) or a single concatenated FASTQ as input
2. Runs **Kraken2** taxonomic classification against a standard database (e.g., Standard-8, PlusPF)
3. Refines abundances with **Bracken** at species level (read re-estimation)
4. Detects antimicrobial resistance genes with **RGI** against the **CARD** database
5. Classifies detected ARGs by **WHO critical priority pathogen** association
6. Optionally runs **HUMAnN3** for functional pathway profiling (MetaCyc + UniRef)
7. Calculates **alpha diversity metrics** from Bracken-adjusted species abundances:
   - **Shannon diversity index**: H = -sum(p_i * ln(p_i)), where p_i is the proportion of classified reads assigned to species i
   - **Simpson diversity index**: D = 1 - sum(p_i^2)
   - **Pielou evenness**: J = H / ln(S), where S is the number of species detected
   - **Species richness**: S = number of distinct species with at least 1 assigned read
8. Generates four publication-quality figures:
   - **Figure 1**: Taxonomy bar chart, top 20 species by relative abundance
   - **Figure 2**: Resistome heatmap, ARG families by drug class with abundance
   - **Figure 3**: WHO-critical ARG summary, priority-tier breakdown of detected resistance genes
   - **Figure 4**: Alpha diversity summary (Shannon, Simpson, Pielou in a panel)
9. Produces a full reproducibility bundle (commands.sh, environment.yml, checksums.sha256)

## Why this exists

If you ask a general AI to "analyse a metagenome," it will:
- Not know which Kraken2 database to use or how to set confidence thresholds
- Hallucinate Bracken parameters for read-length and taxonomic level
- Miss the connection between detected ARGs and WHO priority pathogen lists
- Skip HUMAnN3 entirely (or misconfigure its database paths)
- Produce a single bar chart with no resistance context
- Skip diversity metric calculations (Shannon, Simpson, Pielou)
- Not provide a reproducibility bundle

This skill encodes the correct methodological decisions:
- Kraken2 confidence threshold of 0.2 (reduces false positives in environmental samples)
- Bracken re-estimation at species level with minimum 10 reads
- RGI `bwt` read mapping against CARD with `--include_wildcard` (Perfect/Strict cut-offs belong to `rgi main` and do not apply to read mapping)
- WHO Bacterial Priority Pathogens List 2024 mapped to detected ARG families and drug classes
- HUMAnN3 with MetaCyc stratification for pathway-level functional context
- Thread count auto-detected from available CPUs
- Full reproducibility bundle for every run

## Validated On

The skill works with any shotgun metagenome but has been validated on:
- **Peru sewage metagenomics study** (6 samples, 3 collection sites: Lima, Cusco, Iquitos)
- Environmental sewage samples with mixed microbial communities
- Read depths ranging from 2M to 15M paired-end reads per sample

## WHO-Critical ARG Detection

Detected resistance genes are classified by WHO priority tier. The list edition
lives in one place — `WHO_BPPL_EDITION` in `metagenomics_profiler.py` — and the
report Methods section reads it from there. Current edition: **WHO Bacterial
Priority Pathogens List 2024** (published 17 May 2024).

| Priority | Pathogen | Resistance |
|----------|----------|------------|
| Critical | *Acinetobacter baumannii* | Carbapenem-resistant |
| Critical | Enterobacterales | 3rd-gen cephalosporin-resistant |
| Critical | Enterobacterales | Carbapenem-resistant |
| Critical | *Mycobacterium tuberculosis* | Rifampicin-resistant |
| High | *Salmonella* Typhi | Fluoroquinolone-resistant |
| High | *Shigella* spp. | Fluoroquinolone-resistant |
| High | *Enterococcus faecium* | Vancomycin-resistant |
| High | *Pseudomonas aeruginosa* | Carbapenem-resistant |
| High | Non-typhoidal *Salmonella* | Fluoroquinolone-resistant |
| High | *Neisseria gonorrhoeae* | 3rd-gen cephalosporin- and/or fluoroquinolone-resistant |
| High | *Staphylococcus aureus* | Methicillin-resistant |
| Medium | Group A streptococci | Macrolide-resistant |
| Medium | *Streptococcus pneumoniae* | Macrolide-resistant |
| Medium | *Haemophilus influenzae* | Ampicillin-resistant |
| Medium | Group B streptococci | Penicillin-resistant |

Classification matches on ARG family and drug class, not on pathogen, so a
carbapenemase is tagged Critical even though 2024 places carbapenem-resistant
*P. aeruginosa* in High.

## Usage

```bash
# Full pipeline (taxonomy + resistome + functional)
python metagenomics_profiler.py \
    --r1 sample_R1.fastq.gz \
    --r2 sample_R2.fastq.gz \
    --output metagenomics_report

# Skip HUMAnN3 (faster — taxonomy + resistome only)
python metagenomics_profiler.py \
    --r1 sample_R1.fastq.gz \
    --r2 sample_R2.fastq.gz \
    --output metagenomics_report \
    --skip-functional

# Single concatenated FASTQ
python metagenomics_profiler.py \
    --input combined.fastq.gz \
    --output metagenomics_report

# Specify Kraken2 database path
python metagenomics_profiler.py \
    --r1 sample_R1.fastq.gz \
    --r2 sample_R2.fastq.gz \
    --output metagenomics_report \
    --kraken2-db /path/to/kraken2_db \
    --read-length 150
```

### Demo (works out of the box)

```bash
python metagenomics_profiler.py --demo --output demo_report
```

The demo uses pre-computed results from the Peru sewage metagenomics study (6 samples, 3 sites) and generates all figures and reports instantly without requiring external tools.

## Example Output

Verbatim from `--demo`:

```
Metagenomics Profiler -- ClawBio
========================================
Mode: demo (pre-computed Peru sewage data)
Samples: 6 (3 sites: Lima, Cusco, Iquitos)

Generating taxonomy data...
  Total classified: 94.2%
  Top species: Escherichia coli (Lima: 12.3%, Cusco: 8.1%, Iquitos: 15.6%)
Generating resistome data...
  Total ARG hits: 24 (Perfect: 8, Strict: 16)
  Drug classes: 12
  WHO-Critical ARGs detected: 7
    - NDM-1, OXA-48, KPC-3, CTX-M-15, CTX-M-27, TEM-1, SHV-12
Generating pathway data...
  Total pathways: 10
  Top: PWY-7219: adenosine ribonucleotides de novo biosynthesis

Generating figures...
  Saved: taxonomy_barplot.png
  Saved: resistome_heatmap.png
  Saved: who_critical_args.png

Generating report...
  Saved: report.md
  Saved: reproducibility/ (commands.sh, environment.yml, checksums.sha256)
```

The Perfect/Strict counts above come from the demo table's own synthetic
`criteria` column. A real run uses `rgi bwt`, whose output has no `Cut_Off`
column, and prints `ARG hits: N (WHO-Critical: M)` instead.

## Pipeline Architecture

```
FASTQ R1 + R2
     |
     v
[Kraken2] --> kraken2_report.txt
     |
     v
[Bracken] --> bracken_species.tsv   --> Figure 1: Taxonomy bar chart
     |
     v
[RGI bwt]  --> *.allele_mapping_data.txt --> Figure 2: Resistome heatmap
     |                                --> Figure 3: WHO-critical ARG summary
     v
[HUMAnN3] --> pathabundance.tsv     (optional, --skip-functional to omit)
     |
     v
[Report] --> report.md + figures/ + reproducibility/
```

## Database Requirements

| Tool | Database | Size | Notes |
|------|----------|------|-------|
| Kraken2 | Standard-8 or PlusPF | 8-70 GB | Set via `--kraken2-db` or `$KRAKEN2_DB` |
| Bracken | (built from Kraken2 DB) | included | Read-length specific (default: 150 bp) |
| RGI | CARD | ~500 MB | Auto-downloaded via `rgi auto_load` |
| HUMAnN3 | ChocoPhlAn + UniRef90 | ~15 GB | Set via `--humann-db` or `$HUMANN_DB` |

## Citations

If you use this skill in a publication, please cite:

- Wood, D.E., Lu, J. & Langmead, B. (2019). Improved metagenomic analysis with Kraken 2. Genome Biology, 20, 257.
- Lu, J. et al. (2017). Bracken: estimating species abundance in metagenomics data. PeerJ Computer Science, 3, e104.
- Alcock, B.P. et al. (2023). CARD 2023: expanded curation, support for machine learning, and resistome prediction at the Comprehensive Antibiotic Resistance Database. Nucleic Acids Research, 51(D1), D419-D430.
- Beghini, F. et al. (2021). Integrating taxonomic, functional, and strain-level profiling of diverse microbial communities with bioBakery 3. eLife, 10, e65088.
- Corpas, M. (2026). ClawBio. https://github.com/ClawBio/ClawBio
