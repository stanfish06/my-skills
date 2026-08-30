---
name: archaic-introgression
description: Detect Neanderthal and Denisovan introgression segments from modern human genomes
license: MIT
metadata:
  version: 0.1.0
  author: Manuel Corpas
  domain: genomics
  inputs:
  - format: VCF
    description: Modern human genotypes
    required: true
  - format: VCF
    description: Archaic reference genotypes (Neanderthal/Denisovan)
    required: true
  outputs:
  - format: JSON
    description: Introgression segments with scores and summary statistics
  - format: BED
    description: Genomic coordinates of introgressed segments
  openclaw:
    requires:
      bins:
      - python3
    always: false
    emoji: 🦴
    homepage: https://github.com/ClawBio/ClawBio
    os:
    - darwin
    - linux
    trigger_keywords:
    - archaic introgression
    - Neanderthal DNA
    - Denisovan ancestry
    - IBDmix
    - introgressed segments
---

# Archaic Introgression Detector

## Trigger

**Fire when:**
- User asks about Neanderthal or Denisovan DNA in modern humans
- User wants to detect archaic introgression segments
- User mentions IBDmix or archaic-segment calling
- User has modern + archaic VCF files and wants to compare them

**Do NOT fire when:**
- User asks about general ancestry or population structure (use claw-ancestry-pca)
- User asks about pharmacogenomics or clinical variants
- User wants admixture proportions without segment-level detail

## Why This Exists

Between 1-4% of non-African modern human genomes derive from archaic hominins
(Neanderthals, Denisovans). Identifying these segments matters for understanding
human evolution, disease susceptibility, and immune adaptation. This skill wraps
IBDmix (Chen et al. 2020) and falls back to a pure-Python LOD heuristic when the
IBDmix binaries are not installed.

## Core Capabilities

1. **IBDmix**: `generate_gt` merges the modern and archaic VCFs into a genotype table, then `ibdmix -g … -o … -d <LOD>` calls segments
2. **Pure-Python fallback**: LOD-style segment calling when `ibdmix`/`generate_gt` are not on PATH — prints a warning and labels every segment `ibdmix_fallback`
3. **EIGENSTRAT support**: Read .ind/.snp/.geno files (text and binary packed formats)
4. **Summary statistics**: Per-individual introgression burden, segment count, mean length

## Scope

One skill, one task: detect and report archaic introgression segments. Does not
perform downstream functional annotation of introgressed variants (chain with
vcf-annotator for that).

## Input Formats

- **Modern genotypes**: VCF (uncompressed or .vcf.gz with .tbi index)
- **Archaic genotypes**: VCF (Neanderthal/Denisovan reference panel)
- **EIGENSTRAT**: .ind + .snp + .geno files (text or binary packed format)

## Workflow

1. Parse modern VCF to extract sample names and genotype matrix (numpy array)
2. Parse archaic VCF to extract reference genotypes at matching positions
3. Identify shared variant positions between modern and archaic panels
4. Run IBDmix (generate_gt → ibdmix) or, if its binaries are absent, the pure-Python LOD fallback
5. Collect IntrogressionSegment results per sample
6. Compute per-individual summary statistics
7. Write JSON report and optional BED file

## CLI Reference

```bash
# Run with IBDmix on VCF inputs
python archaic_introgression.py \
  --input modern.vcf --archaic archaic.vcf \
  --method ibdmix --output /tmp/introgression

# Run demo with synthetic data
python archaic_introgression.py --demo --output /tmp/introgression_demo

# Filter to specific samples
python archaic_introgression.py \
  --input modern.vcf --archaic archaic.vcf \
  --samples SAMPLE01,SAMPLE02 --output /tmp/introgression

# Adjust LOD threshold
python archaic_introgression.py \
  --input modern.vcf --archaic archaic.vcf \
  --lod 5.0 --output /tmp/introgression
```

## Demo

```bash
python archaic_introgression.py --demo --output /tmp/introgression_demo
```

Runs on bundled `examples/demo_modern.vcf` (3 samples, 10 SNPs on chr22) and
`examples/demo_archaic.vcf` (1 Neanderthal sample, same positions).

## Example Queries

- "How much Neanderthal DNA do I have?"
- "Detect archaic introgression in my VCF"
- "Run IBDmix on my genotype data"
- "Show me introgressed segments from Denisova"
- "Compare my genome against the Vindija Neanderthal"

## Output Structure

```
output_dir/
  introgression_results.json   # Full results with segments and summary
  segments.bed                 # BED file of introgressed regions
```

### JSON structure

The top-level `method` records what actually ran, not what `--method` requested:
`ibdmix` only when the binaries were found and succeeded, otherwise
`ibdmix_fallback`.

```json
{
  "method": "ibdmix",
  "lod_threshold": 3.0,
  "num_samples": 3,
  "segments": [
    {
      "sample": "SAMPLE01",
      "chrom": "chr22",
      "start": 16050075,
      "end": 16051249,
      "archaic_source": "Neanderthal",
      "method": "ibdmix",
      "score": 4.2,
      "num_variants": 6,
      "length": 1174
    }
  ],
  "summary": {
    "SAMPLE01": {
      "total_segments": 1,
      "total_length_bp": 1174,
      "mean_segment_length": 1174.0,
      "mean_score": 4.2
    }
  }
}
```

## Dependencies

- Python 3.11+
- numpy
- Optional: IBDmix (`generate_gt` and `ibdmix` binaries, https://github.com/PrincetonUniversity/IBDmix)
- Optional: bcftools (for indexed VCF extraction)

## Gotchas

1. **The model will want to report percentage of genome that is Neanderthal from 10 SNPs.** Do not. Demo data is too sparse for genome-wide estimates. State the segment coordinates and LOD scores only.
2. **The model will want to assume all archaic segments are Neanderthal.** Do not. Check the archaic source label. Denisovan segments have different frequency distributions in different populations.
3. **The fallback is not IBDmix.** Its per-site scores are an unvalidated heuristic, not the IBDmix LOD model. Segments it emits carry `"method": "ibdmix_fallback"` and the run prints a warning on stderr. Report them as heuristic calls on demo-scale data, never as IBDmix results, and install IBDmix for anything real.
4. **The model will want to interpret introgression as harmful.** Do not. Many introgressed segments are adaptive (e.g., immune genes, altitude adaptation). Present findings neutrally.
5. **The model will want to use text .geno parsing for binary packed files.** Do not. Check for the 'GENO' magic header and switch to binary unpacking (2-bit per genotype).

## Safety

ClawBio is a research and educational tool. It is not a medical device and does
not provide clinical diagnoses. Consult a healthcare professional before making
any medical decisions.

## Agent Boundary

The agent dispatches queries and explains results. The skill executes the
computational pipeline. The agent should not attempt to reimplement IBDmix
LOD scoring outside this module.

## Chaining Partners

- **vcf-annotator**: annotate introgressed variants with ClinVar/gnomAD significance
- **equity-scorer**: assess representation of archaic ancestry detection across populations
- **claw-ancestry-pca**: combine with PCA to contextualise introgression within population structure

## Maintenance

- Review quarterly against new archaic genome releases
- Update when new IBDmix versions change option names or output columns
- Deprecate if a unified tool supersedes IBDmix

## Citations

- Chen L, Wolf AB, Fu W, Li L, Akey JM. Identifying and interpreting apparent Neanderthal ancestry in African individuals. Cell. 2020;180(4):677-687. (IBDmix)
