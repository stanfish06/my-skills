---
title: msa-structure-prediction-pipeline
aliases:
  - msa structure prediction pipeline
  - ColabFold
tags:
  - skill
  - domain/sequence-phylogenetics
domain: sequence-phylogenetics
status: untried
source: skills/msa-structure-prediction-pipeline/SKILL.md
created: 2026-06-28
---

# msa-structure-prediction-pipeline

> [!info] What it does
> NOTE: your protein sequence and the retrieved MSA alignment are transmitted to external NVIDIA-hosted APIs (health.api.nvidia.com) on every call. Use local NIM containers for confidential or proprietary sequences. Run a complete protein structure prediction pipeline using NVIDIA BioNeMo NIMs: search for MSA alignments with MSA-Search (ColabFold), then predict the structure with OpenFold3 using the retrieved alignments. Use this skill whenever the user wants to predict a protein structure with maximum accuracy using MSA context, run the full AlphaFold3-style pipeline, generate MSA-informed structure predictions, or improve structure prediction accuracy by providing evolutionary information. Triggers on: MSA structure prediction pipeline, structure prediction pipeline, MSA-informed prediction, OpenFold3, ColabFold MSA, AlphaFold3 pipeline, protein structure, homology search, a3m alignment, UniRef30, NIM microservice. This pipeline chains MSA-Search and OpenFold3.

**Source:** [skills/msa-structure-prediction-pipeline/SKILL.md](../../../skills/msa-structure-prediction-pipeline/SKILL.md)  ·  **Domain:** [Sequence Analysis, NGS & Phylogenetics](../../maps/sequence-phylogenetics.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [colabfold](../../notes/drug-discovery-chem/colabfold.md) — Fast AlphaFold2/ColabFold protein structure prediction

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

