---
title: Sequence Analysis, NGS & Phylogenetics
tags:
  - skill-map
created: 2026-06-13
---

# Sequence Analysis, NGS & Phylogenetics

> [!abstract] Scope
> Sequence toolkits, read QC/alignment, phylogenetic inference, and sequence-to-function models.

[Back to Skill Index](../index.md)

**Related maps:** [Genomics, Variants & Population Genetics](genomics-variants.md) | [Single-Cell, RNA-seq & Functional Genomics](single-cell-rnaseq.md) | [Bio Databases, Lab & Cloud Platforms](bio-databases-platforms.md)

## Skills (40)

- [alterlab-qiime2-amplicon](../notes/sequence-phylogenetics/alterlab-qiime2-amplicon.md) — Runs 16S/ITS amplicon (microbiome) analysis with the QIIME 2 amplicon distribution (2026.1
- [analyze-fasta](../notes/sequence-phylogenetics/analyze-fasta.md) — Analyze a single FASTA file (nucleotide or protein), compute sequence-level metrics (GC, ORFs, MW, pI, GRAVY, secondary-structure fractions) with Biopython, and write a Markdown report...
- [bioconductor-bridge](../notes/sequence-phylogenetics/bioconductor-bridge.md) — Bioconductor package discovery, workflow recommendation, setup inspection, and starter code generation grounded in official Bioconductor containers and BiocManager
- [biopython](../notes/sequence-phylogenetics/biopython.md) — Comprehensive molecular biology toolkit
- [bioqc-mcp](../notes/sequence-phylogenetics/bioqc-mcp.md) — Automated sequencing quality control and advanced visualization wrapping FastQC, MultiQC, and custom chart generation
- [bioservices](../notes/sequence-phylogenetics/bioservices.md) — Unified Python interface to 40+ bioinformatics services
- [blast-search](../notes/sequence-phylogenetics/blast-search.md) — Run BLAST sequence similarity searches. Use when the user asks to BLAST a sequence, find similar sequences, identify a gene/protein, or do homology search
- [busco-assessor](../notes/sequence-phylogenetics/busco-assessor.md) — Genome, transcriptome, and protein completeness assessment via BUSCO v6
- [claw-metagenomics](../notes/sequence-phylogenetics/claw-metagenomics.md) — Shotgun metagenomics profiling — taxonomy, resistome, and functional pathways
- [cutadapt](../notes/sequence-phylogenetics/cutadapt.md) — Adapter, primer, and poly-A/T trimming for high-throughput sequencing reads (FASTQ/FASTA)
- [etetoolkit](../notes/sequence-phylogenetics/etetoolkit.md) — Phylogenetic tree toolkit (ETE). Tree manipulation (Newick/NHX), evolutionary event detection, orthology/paralogy, NCBI taxonomy, visualization (PDF/SVG), for phylogenomics
- [evo2-nim](../notes/sequence-phylogenetics/evo2-nim.md) — Generate and analyze DNA sequences using NVIDIA's Evo 2 BioNeMo NIM microservice
- [fastp-fastq-preprocessing](../notes/sequence-phylogenetics/fastp-fastq-preprocessing.md) — All-in-one FASTQ QC and adapter trimming
- [gget](../notes/sequence-phylogenetics/gget.md) — Fast CLI/Python queries to 20+ bioinformatics databases
- [gi-annotation](../notes/sequence-phylogenetics/gi-annotation.md) — Predict gene and transcript structure (intervals, exons, strand) from a DNA sequence using the Genomic Intelligence DNA Annotation model, via the hosted /v1/tasks/annotation/predict API
- [gi-chromatin](../notes/sequence-phylogenetics/gi-chromatin.md) — Predict chromatin state — histone marks, DNase, TF binding — across 919 tracks (DeepSEA-style) for DNA sequences, via the hosted Genomic Intelligence /v1/tasks/chromatin/predict API
- [gi-enhancer](../notes/sequence-phylogenetics/gi-enhancer.md) — Predict enhancer activity in DNA sequences using the Genomic Intelligence G0 DeepSTARR model, via the hosted /v1/tasks/enhancer/predict API
- [gi-expression](../notes/sequence-phylogenetics/gi-expression.md) — Predict tissue / cell-type expression (log TPM + TPM) from a 9,198 bp TSS-centered DNA sequence using the Genomic Intelligence G0 Expression model, via the hosted...
- [gi-promoter](../notes/sequence-phylogenetics/gi-promoter.md) — Detect promoter regions in DNA sequences using the Genomic Intelligence G0 transformer (GENA-LM BERT Large), via the hosted /v1/tasks/promoter/predict API
- [gi-splice](../notes/sequence-phylogenetics/gi-splice.md) — Detect splice donor and acceptor sites in DNA sequences using the Genomic Intelligence G0 BigBird transformer, via the hosted /v1/tasks/splice/predict API
- [metagenomics](../notes/sequence-phylogenetics/metagenomics.md) — Shotgun metagenomics workflow with host-depletion-aware QC, taxonomic profiling, functional profiling, AMR follow-up, and reproducible community output tables
- [msa-search-nim](../notes/sequence-phylogenetics/msa-search-nim.md) — Generate multiple sequence alignments (MSAs) for protein sequences using the ColabFold MSA-Search NIM
- [msa-structure-prediction-pipeline](../notes/sequence-phylogenetics/msa-structure-prediction-pipeline.md) — NOTE: your protein sequence and the retrieved MSA alignment are transmitted to external NVIDIA-hosted APIs (health.api.nvidia.com) on every call
- [multiqc-reporter](../notes/sequence-phylogenetics/multiqc-reporter.md) — Aggregates QC reports from any bioinformatics tool outputs (FastQC, fastp, STAR, Picard, samtools, etc.) into a single MultiQC HTML report plus a ClawBio markdown summary with...
- [ncbi-blast-skill](../notes/sequence-phylogenetics/ncbi-blast-skill.md) — Submit, poll, and summarize NCBI BLAST Common URL API jobs (Blast.cgi) for nucleotide or protein sequences
- [ncbi-datasets](../notes/sequence-phylogenetics/ncbi-datasets.md) — Download genomes, genes, virus sequences, and taxonomy data from NCBI using the datasets and dataformat CLI tools
- [ngs-amplicon-microbiome](../notes/sequence-phylogenetics/ngs-amplicon-microbiome.md) — Kick off public 16S, 18S, ITS, COI, or other marker-gene amplicon microbiome workflows using nf-core/ampliseq, QIIME2, DADA2, and Cutadapt
- [ngs-bcl-to-fastq](../notes/sequence-phylogenetics/ngs-bcl-to-fastq.md) — Validate Illumina BCL run folders and sample sheets, plan demultiplexing, review index/UMI/lane choices, run BCL-to-FASTQ conversion, and interpret demux metrics while surfacing...
- [ngs-cli-toolkit](../notes/sequence-phylogenetics/ngs-cli-toolkit.md) — The core command-line NGS workhorses for going from raw reads to variants — bwa-mem2/minimap2/bowtie2 (alignment), samtools (BAM sort/index/stats/view), bcftools (VCF...
- [ngs-fastq-qc](../notes/sequence-phylogenetics/ngs-fastq-qc.md) — Validate FASTQ inputs, run local FastQC/MultiQC QC, interpret QC signals, and optionally execute fastp or Cutadapt trimming branches without overwriting raw reads
- [ngs-runtime-env](../notes/sequence-phylogenetics/ngs-runtime-env.md) — Check whether public NGS tools and packages already exist before downloading, installing, or running a sequencing pipeline
- [ngs-shotgun-metagenomics](../notes/sequence-phylogenetics/ngs-shotgun-metagenomics.md) — Kick off public shotgun metagenomics QC, host-depletion, taxonomic profiling, and functional profiling workflows using nf-core/taxprofiler, Kraken2, Bracken, MetaPhlAn, and HUMAnN
- [phylogenetics](../notes/sequence-phylogenetics/phylogenetics.md) — Build and analyze phylogenetic trees using MAFFT (multiple alignment), IQ-TREE 2 (maximum likelihood), and FastTree (fast NJ/ML)
- [phylogenetics-builder](../notes/sequence-phylogenetics/phylogenetics-builder.md) — End-to-end ML phylogenetic tree inference — MSA, trimming, ModelFinder, IQ-TREE2/RAxML-NG
- [rnacentral-skill](../notes/sequence-phylogenetics/rnacentral-skill.md) — Submit compact RNAcentral API requests for RNA entry browsing, single-entry lookup, and cross-reference retrieval
- [scikit-bio](../notes/sequence-phylogenetics/scikit-bio.md) — Biological data toolkit. Sequence analysis, alignments, phylogenetic trees, diversity metrics (alpha/beta, UniFrac), ordination (PCoA), PERMANOVA, FASTA/Newick I/O, for microbiome...
- [seq-wrangler](../notes/sequence-phylogenetics/seq-wrangler.md) — NGS read QC, alignment, and BAM processing pipeline
- [sequence-analysis](../notes/sequence-phylogenetics/sequence-analysis.md) — Analyze DNA/RNA/protein sequences. Use when the user provides a sequence and asks for analysis, translation, GC content, ORFs, motifs, restriction sites, or primer design
- [sourmash](../notes/sequence-phylogenetics/sourmash.md) — MinHash/FracMinHash sketching for alignment-free comparison of genomes and metagenomes
- [viennarna-structure-prediction](../notes/sequence-phylogenetics/viennarna-structure-prediction.md) — Predict RNA secondary structure, MFE folding, base-pair probabilities, RNA-RNA interactions via ViennaRNA Python bindings
