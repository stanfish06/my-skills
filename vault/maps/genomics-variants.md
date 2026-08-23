---
title: Genomics, Variants & Population Genetics
tags:
  - skill-map
created: 2026-06-13
---

# Genomics, Variants & Population Genetics

> [!abstract] Scope
> DNA sequencing, variant calling/annotation, GWAS, fine-mapping, and population & personal genomics.

[Back to Skill Index](../index.md)

**Related maps:** [Single-Cell, RNA-seq & Functional Genomics](single-cell-rnaseq.md) | [Sequence Analysis, NGS & Phylogenetics](sequence-phylogenetics.md) | [Bio Databases, Lab & Cloud Platforms](bio-databases-platforms.md) | [Clinical, Medical & Pharmacogenomics](clinical-medical.md)

## Skills (55)

- [alphagenome-single-variant-analysis](../notes/genomics-variants/alphagenome-single-variant-analysis.md) — Analyzes genetic variant effects on gene expression (RNA-seq), chromatin accessibility (DNASE), histone marks (ChIP), and transcription factors using the AlphaGenome API
- [archaic-introgression](../notes/genomics-variants/archaic-introgression.md) — Detect Neanderthal and Denisovan introgression segments from modern human genomes
- [biobankjapan-phewas-skill](../notes/genomics-variants/biobankjapan-phewas-skill.md) — Fetch compact BioBank Japan PheWAS summaries for single variants by accepting rsID, GRCh38, or GRCh37 input and resolving to the required GRCh37 query
- [civic-skill](../notes/genomics-variants/civic-skill.md) — Submit compact CIViC GraphQL requests for cancer variant interpretation schema inspection and targeted evidence retrieval
- [claw-ancestry-pca](../notes/genomics-variants/claw-ancestry-pca.md) — Ancestry decomposition PCA against the Simons Genome Diversity Project
- [clinical-variant-reporter](../notes/genomics-variants/clinical-variant-reporter.md) — Classify germline variants from VCF/BCF files according to the ACMG/AMP 2015 28-criteria evidence framework and generate clinical-grade interpretation reports with per-variant evidence...
- [clinvar-variation-skill](../notes/genomics-variants/clinvar-variation-skill.md) — Submit compact ClinVar Clinical Tables and NCBI Variation requests for search, VCV, RCV, SCV, and RefSNP lookups
- [dnasp](../notes/genomics-variants/dnasp.md) — Full reimplementation of DnaSP 6 for population genetics analysis of aligned DNA sequences
- [eqtl-catalogue-region-fetch](../notes/genomics-variants/eqtl-catalogue-region-fetch.md) — Fetch a region of cis-eQTL summary statistics from EBI eQTL Catalogue v7+ via tabix-on-FTP
- [eqtl-catalogue-skill](../notes/genomics-variants/eqtl-catalogue-skill.md) — Submit compact eQTL Catalogue API requests for association retrieval and documented metadata endpoints
- [equity-scorer](../notes/genomics-variants/equity-scorer.md) — Compute HEIM diversity and equity metrics from VCF or ancestry data
- [fastreer](../notes/genomics-variants/fastreer.md) — Phylogenetic distance matrices and trees from VCF or FASTA data using the fastreeR hybrid Java/Python toolkit (VCF2TREE, VCF2DIST, DIST2TREE, FASTA2DIST)
- [fine-mapping](../notes/genomics-variants/fine-mapping.md) — Statistical fine-mapping of GWAS loci using SuSiE, SuSiE-inf, and Approximate Bayes Factors to identify credible sets and posterior inclusion probabilities (PIPs) for causal variant...
- [finngen-phewas-skill](../notes/genomics-variants/finngen-phewas-skill.md) — Fetch compact FinnGen PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query
- [genebass-gene-burden-skill](../notes/genomics-variants/genebass-gene-burden-skill.md) — Submit compact Genebass gene burden requests for one Ensembl gene ID and one burden set
- [geniml](../notes/genomics-variants/geniml.md) — Use when working with genomic interval data (BED files) for machine learning tasks
- [genome-compare](../notes/genomics-variants/genome-compare.md) — Compare your genome to George Church (PGP-1) and estimate ancestry composition via IBS and EM admixture
- [genome-match](../notes/genomics-variants/genome-match.md) — Score genetic compatibility across all male-female pairings in a Genomebook generation
- [genomics-workflow-acceleration](../notes/genomics-variants/genomics-workflow-acceleration.md) — Use when accelerating existing genomics workflows with NVIDIA Parabricks, improving runtime or price/performance, converting pipeline steps to GPUs, or comparing CPU and GPU workflow...
- [gnomad-graphql-skill](../notes/genomics-variants/gnomad-graphql-skill.md) — Submit compact gnomAD GraphQL requests for frequency, gene constraint, and variant context queries
- [gtars](../notes/genomics-variants/gtars.md) — High-performance toolkit for genomic interval analysis in Rust with Python bindings
- [gtex-eqtl-skill](../notes/genomics-variants/gtex-eqtl-skill.md) — Fetch GTEx single-tissue eQTL associations from one variant input by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query for the GTEx v2 API
- [gwas-catalog-region-fetch](../notes/genomics-variants/gwas-catalog-region-fetch.md) — Fetch a region of GWAS summary statistics from the NHGRI-EBI GWAS Catalog harmonised collection via tabix-on-FTP
- [gwas-catalog-skill](../notes/genomics-variants/gwas-catalog-skill.md) — Submit compact GWAS Catalog REST API v2 requests for studies, associations, SNPs, EFO traits, genes, publications, loci, and metadata
- [gwas-lookup](../notes/genomics-variants/gwas-lookup.md) — Federated variant lookup across 9 genomic databases — GWAS Catalog, Open Targets, PheWeb (UKB, FinnGen, BBJ), GTEx, eQTL Catalogue, and more
- [gwas-pipeline](../notes/genomics-variants/gwas-pipeline.md) — End-to-end GWAS automation wrapping PLINK2 for genotype QC and REGENIE for two-step whole-genome regression association testing
- [gwas-prs](../notes/genomics-variants/gwas-prs.md) — Calculate polygenic risk scores from DTC genetic data using the PGS Catalog
- [hla-typing](../notes/genomics-variants/hla-typing.md) — HLA allele typing from WGS/WES VCF data
- [ld-1000g-region-compute](../notes/genomics-variants/ld-1000g-region-compute.md) — Compute pairwise r² between a lead variant and every variant in a window using the 1000 Genomes Phase 3 GRCh38 reference panel, ancestry-stratified
- [locus-to-gene-mapper-skill](../notes/genomics-variants/locus-to-gene-mapper-skill.md) — Map GWAS loci to ranked candidate genes using a deterministic multi-skill chain (EFO -> GWAS -> coordinates -> Open Targets L2G/coloc -> eQTL -> burden/coding context), with...
- [locuscompare-region-render](../notes/genomics-variants/locuscompare-region-render.md) — Render a 4-panel regional LocusCompare diagnostic for one (lead variant, exposure study, outcome study) tuple - overlays GWAS Manhattan, QTL Manhattan, GENCODE gene track, and...
- [marker-dominance-mapper](../notes/genomics-variants/marker-dominance-mapper.md) — Deterministic marker-dominance region mapping from local spot-count CSVs
- [mendelian-randomisation](../notes/genomics-variants/mendelian-randomisation.md) — Two-sample Mendelian Randomisation from GWAS summary statistics with IVW, MR-Egger, weighted median/mode, and full sensitivity analysis (Cochran Q, Egger intercept, Steiger...
- [ncbi-datasets-skill](../notes/genomics-variants/ncbi-datasets-skill.md) — Submit compact NCBI Datasets v2 requests for assembly, genome, taxonomy, and related metadata endpoints
- [nfcore-sarek-wrapper](../notes/genomics-variants/nfcore-sarek-wrapper.md) — ClawBio wrapper around nf-core/sarek 3.8.1 covering mapping through annotation for germline, tumor-only, and somatic paired analyses
- [ngs-analysis-router](../notes/genomics-variants/ngs-analysis-router.md) — Route BCL, FASTQ, BAM/CRAM, count-matrix, or VCF sequencing requests to the right public NGS analysis skill and ask only the missing assay-specific setup questions
- [ngs-dna-germline-variants](../notes/genomics-variants/ngs-dna-germline-variants.md) — Run or plan deep germline WGS, WES, targeted-panel, cohort, or trio variant-calling workflows with reference-build, known-sites, QC, joint-calling, and annotation checks
- [ngs-dna-somatic-variants](../notes/genomics-variants/ngs-dna-somatic-variants.md) — Run or plan tumor-normal, tumor-only, WGS, WES, or cancer-panel somatic variant workflows with pairing, contamination, panel-of-normals, purity, QC, and annotation checks
- [ngs-dna-umi-panel-variants](../notes/genomics-variants/ngs-dna-umi-panel-variants.md) — Run or plan targeted DNA panel variant workflows that use UMIs, duplex consensus reads, molecular barcodes, low-frequency calling, target coverage, and panel-specific QC
- [ngs-dna-variant-calling](../notes/genomics-variants/ngs-dna-variant-calling.md) — Dispatch WGS, WES, or targeted DNA variant requests to germline, somatic, or UMI-panel skills, then plan public nf-core/sarek, GATK4, DeepVariant, samtools, or bcftools workflows
- [pacsomatic](../notes/genomics-variants/pacsomatic.md) — Operator toolkit for nf-core/pacsomatic matched tumor-normal workflows from BAM inputs
- [parabricks](../notes/genomics-variants/parabricks.md) — Route NVIDIA Parabricks pbrun tools, assess GPU/runtime readiness, and provide version-aware command guidance for FASTQ/BAM processing, RNA-seq, variant calling, BAM QC, and GVCF...
- [polars-bio](../notes/genomics-variants/polars-bio.md) — High-performance genomic interval operations and bioinformatics file I/O on Polars DataFrames
- [pybedtools](../notes/genomics-variants/pybedtools.md) — Python genomic interval arithmetic with BEDTools, complementing pysam, polars, and query for downstream tables
- [pysam](../notes/genomics-variants/pysam.md) — Genomic file toolkit. Read/write SAM/BAM/CRAM alignments, VCF/BCF variants, FASTA/FASTQ sequences, extract regions, calculate coverage, for NGS data processing pipelines
- [recombinator](../notes/genomics-variants/recombinator.md) — Produce offspring genomes from parent pairs via meiotic recombination, mutation, and clinical evaluation
- [sample-qc-triage](../notes/genomics-variants/sample-qc-triage.md) — Deterministic multi-sample QC triage for identity, sex, contamination, and batch-shift outliers
- [soul2dna](../notes/genomics-variants/soul2dna.md) — Compile SOUL.md character profiles into synthetic diploid genomes (.genome.json) via trait-to-allele mapping
- [tiledbvcf](../notes/genomics-variants/tiledbvcf.md) — Efficient storage and retrieval of genomic variant data using TileDB
- [tpmi-phewas-skill](../notes/genomics-variants/tpmi-phewas-skill.md) — Fetch compact TPMI PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query
- [ukb-ppp-region-fetch](../notes/genomics-variants/ukb-ppp-region-fetch.md) — Fetch a regional slice of plasma pQTL summary statistics from the UK Biobank Pharma Proteomics Project (UKB-PPP
- [ukb-topmed-phewas-skill](../notes/genomics-variants/ukb-topmed-phewas-skill.md) — Fetch compact UKB-TOPMed PheWAS summaries for single variants by accepting rsID, GRCh37, or GRCh38 input and resolving to the required GRCh38 query
- [variant-annotation](../notes/genomics-variants/variant-annotation.md) — Annotate VCF variants with Ensembl VEP REST, ClinVar significance, gnomAD/population frequency context, and prioritized variant ranking
- [vcf-annotator](../notes/genomics-variants/vcf-annotator.md) — Annotate VCF variants with Ensembl VEP, ClinVar, and gnomAD
- [wgs-prs](../notes/genomics-variants/wgs-prs.md) — End-to-end WGS to polygenic risk score pipeline
