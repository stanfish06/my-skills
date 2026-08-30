# 🦖 ClawBio VCF Annotator Report

**Input**: demo_variants.vcf (synthetic)  
**Data**: SYNTHETIC — not real annotations  
**Date**: 2026-08-30 11:48 UTC  
**Total variants**: 5  
**HIGH impact**: 2 | **MODERATE**: 3 | **LOW**: 0  
**ClinVar Pathogenic/Likely Pathogenic**: 3

---

## Summary

**Synthetic illustrative data — invented coordinates, frequencies and pathogenicity calls, not real annotations. Run without --demo to annotate against Ensembl VEP, ClinVar and gnomAD.** These 5 records were not annotated against any database. 2 variant(s) carry HIGH impact consequences. 3 variant(s) are classified as Pathogenic or Likely Pathogenic in ClinVar. Variants are ranked by predicted functional impact below.

---

## Variant Table

| # | Gene | Variant | Consequence | Impact | ClinVar | gnomAD AF |
|---|------|---------|-------------|--------|---------|-----------|
| 1 | BRCA2 | 13:32316461 C>T | stop_gained | **HIGH** | Pathogenic | 0.000004 |
| 2 | CFTR | 7:117548628 CTTT>C | frameshift_variant | **HIGH** | Pathogenic | 0.021000 |
| 3 | BRCA1 | 17:43044295 G>A | missense_variant | **MODERATE** | Pathogenic | 0.000008 |
| 4 | APOE | 19:11089199 T>C | missense_variant | **MODERATE** | Risk factor | 0.147000 |
| 5 | MTHFR | 1:69515 G>A | missense_variant | **MODERATE** | Benign/Likely benign | 0.312000 |

---

## Detailed Annotations

### 1. BRCA2 — 13:32316461 C>T

| Field | Value |
|-------|-------|
| **rsID** | DEMO_VAR_2 |
| **HGVS** | N/A |
| **Consequence** | stop_gained |
| **Impact** | HIGH |
| **SIFT** | deleterious |
| **PolyPhen** | probably_damaging |
| **ClinVar** | Pathogenic |
| **ClinVar Condition** | Familial cancer of breast |
| **gnomAD AF (global)** | 0.000004 |
| **gnomAD AF (AFR)** | 0.000000 |
| **gnomAD AF (EUR)** | 0.000006 |

### 2. CFTR — 7:117548628 CTTT>C

| Field | Value |
|-------|-------|
| **rsID** | DEMO_VAR_3 |
| **HGVS** | N/A |
| **Consequence** | frameshift_variant |
| **Impact** | HIGH |
| **SIFT** | deleterious |
| **PolyPhen** | N/A |
| **ClinVar** | Pathogenic |
| **ClinVar Condition** | Cystic fibrosis |
| **gnomAD AF (global)** | 0.021000 |
| **gnomAD AF (AFR)** | 0.000300 |
| **gnomAD AF (EUR)** | 0.033000 |

### 3. BRCA1 — 17:43044295 G>A

| Field | Value |
|-------|-------|
| **rsID** | DEMO_VAR_1 |
| **HGVS** | N/A |
| **Consequence** | missense_variant |
| **Impact** | MODERATE |
| **SIFT** | deleterious |
| **PolyPhen** | probably_damaging |
| **ClinVar** | Pathogenic |
| **ClinVar Condition** | Hereditary breast and ovarian cancer syndrome |
| **gnomAD AF (global)** | 0.000008 |
| **gnomAD AF (AFR)** | 0.000000 |
| **gnomAD AF (EUR)** | 0.000012 |

### 4. APOE — 19:11089199 T>C

| Field | Value |
|-------|-------|
| **rsID** | DEMO_VAR_4 |
| **HGVS** | N/A |
| **Consequence** | missense_variant |
| **Impact** | MODERATE |
| **SIFT** | tolerated |
| **PolyPhen** | benign |
| **ClinVar** | Risk factor |
| **ClinVar Condition** | Alzheimer disease |
| **gnomAD AF (global)** | 0.147000 |
| **gnomAD AF (AFR)** | 0.232000 |
| **gnomAD AF (EUR)** | 0.143000 |

### 5. MTHFR — 1:69515 G>A

| Field | Value |
|-------|-------|
| **rsID** | DEMO_VAR_5 |
| **HGVS** | N/A |
| **Consequence** | missense_variant |
| **Impact** | MODERATE |
| **SIFT** | tolerated |
| **PolyPhen** | benign |
| **ClinVar** | Benign/Likely benign |
| **ClinVar Condition** | Homocystinuria |
| **gnomAD AF (global)** | 0.312000 |
| **gnomAD AF (AFR)** | 0.198000 |
| **gnomAD AF (EUR)** | 0.367000 |

---

---
*ClawBio VCF Annotator is a research tool. Not a clinical diagnostic device. Always consult a qualified geneticist for clinical decisions.*
