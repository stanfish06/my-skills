# ATAC Seq Technical Reference

## QC Interpretation

### TSS Enrichment

| TSS enrichment | Interpretation |
|---|---|
| `< 5` | poor |
| `5-7` | weak |
| `> 7` | acceptable |
| `> 10` | strong |

### FRiP

| FRiP | Interpretation |
|---|---|
| `< 0.1` | weak |
| `0.1-0.2` | usable |
| `> 0.2` | strong |

## Why ATAC Uses Different Peak Settings

Transposition footprints differ from ChIP fragment modeling assumptions, so ATAC skips the ChIP shifting model. Two mutually exclusive routes:

- `-f BAMPE` — pile up the real fragments from the read pairs. MACS3 sets `--shift` to `0` for `BAMPE`/`BEDPE`/`FRAG` and takes fragment length from the pairs, so `--nomodel`, `--shift`, and `--extsize` have no effect here.
- `-f BAM --nomodel --shift -100 --extsize 200` — pile up Tn5 insertion sites, each 5' end moved 100 bp toward 5' and extended to 200 bp.

## Failure Modes

- weak TSS enrichment and no periodicity
  - likely poor library quality
- many peaks but poor FRiP
  - likely noisy open chromatin signal
- footprinting requested on shallow data
  - report that confidence is low before proceeding
