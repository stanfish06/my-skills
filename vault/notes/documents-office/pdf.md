---
title: pdf
tags:
  - skill
  - domain/documents-office
domain: documents-office
status: untried
source: skills/pdf/SKILL.md
created: 2026-06-09
---

# pdf

> [!info] What it does
> PDF manipulation toolkit. Extract text/tables, create PDFs, merge/split, fill forms, for programmatic document processing and analysis.

**Source:** [skills/pdf/SKILL.md](../../../skills/pdf/SKILL.md)  ·  **Domain:** [Documents, Office & Media](../../maps/documents-office.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [academic-paper](../../notes/academic-pipelines/academic-paper.md) — 12-agent academic paper writing pipeline
- [cite-check](../../notes/literature-discovery/cite-check.md) — Cite-checks a brief, motion, or memo (PDF/Word): verifies each cited case is real, supports the proposition, is good law, and quoted accurately
- [clinical-decision-support](../../notes/clinical-medical/clinical-decision-support.md) — Generate professional clinical decision support (CDS) documents for pharmaceutical and clinical research settings, including patient cohort analyses (biomarker-stratified with...
- [etetoolkit](../../notes/sequence-phylogenetics/etetoolkit.md) — Phylogenetic tree toolkit (ETE). Tree manipulation (Newick/NHX), evolutionary event detection, orthology/paralogy, NCBI taxonomy, visualization (PDF/SVG), for phylogenomics
- [firecrawl-parse](../../notes/web-automation-frontend/firecrawl-parse.md) — Convert a local file (PDF, DOCX, XLSX, HTML, …) to markdown, or answer questions about its content
- [liteparse](../../notes/documents-office/liteparse.md) — Local document and PDF parsing with spatial text and bounding boxes
- [markitdown](../../notes/documents-office/markitdown.md) — Convert files and office documents to Markdown
- [matplotlib](../../notes/data-science-compute/matplotlib.md) — Low-level plotting library for full customization
- [nature-figure](../../notes/academic-pipelines/nature-figure.md) — Create, revise, audit, and export submission-grade scientific figures for Nature-family and other high-impact venues in Python (matplotlib/seaborn) or R...
- [nature-paper2ppt](../../notes/academic-pipelines/nature-paper2ppt.md) — Build a complete Nature-style Chinese PPTX presentation from a scientific paper, preprint, PDF, article text, figure legends, or reading notes
- [nature-reader](../../notes/academic-pipelines/nature-reader.md) — Build full-paper Chinese-English side-by-side, figure/table-aware, source-grounded Markdown readers for journal or conference papers from PDF, DOI, arXiv, publisher HTML, or pasted text
- [neo4j-import-skill](../../notes/analytics-engineering/neo4j-import-skill.md) — Import structured data into Neo4j — LOAD CSV, CALL IN TRANSACTIONS, neo4j-admin database import full (offline bulk), apoc.load.csv/json, apoc.periodic.iterate, driver batch writes
- [paper-2-web](../../notes/research-writing/paper-2-web.md) — Use when converting academic papers into promotional and presentation formats including interactive websites (Paper2Web), presentation videos (Paper2Video), and conference posters...
- [paper-lookup](../../notes/literature-discovery/paper-lookup.md) — Search 10 academic literature APIs for papers, preprints, citations, and open-access full text, and return results with reproducible provenance
- [pptx-posters](../../notes/research-writing/pptx-posters.md) — Create research posters using HTML/CSS that can be exported to PDF or PPTX
- [pyzotero](../../notes/research-writing/pyzotero.md) — Interact with Zotero reference management libraries using the pyzotero Python client
- [report-template](../../notes/documents-office/report-template.md) — Publication-quality PDF report generation using Typst templates
- [sec-report](../../notes/proteomics-metabolomics/sec-report.md) — SEC (size-exclusion chromatography) analysis with peak detection, oligomer classification, and publication-quality PDF report generation via Typst templates
- [treatment-plans](../../notes/clinical-medical/treatment-plans.md) — Generate concise (3-4 page), focused medical treatment plans in LaTeX/PDF format for all clinical specialties
- [twilio-enterprise-knowledge](../../notes/saas-platforms/twilio-enterprise-knowledge.md) — Use when building Twilio Enterprise Knowledge workflows for AI or human agents, including provisioning a knowledge base, adding website, PDF, or text sources, semantic search, or...
- [wes-clinical-report-en](../../notes/clinical-medical/wes-clinical-report-en.md) — Generates professional clinical PDF reports in English from WES (Whole Exome Sequencing) data with clinical interpretation summary, pharmacogenomic alerts, and follow-up recommendations
- [wes-clinical-report-es](../../notes/clinical-medical/wes-clinical-report-es.md) — Generates professional clinical PDF reports in Spanish from WES (Whole Exome Sequencing) data with clinical interpretation, pharmacogenomic alerts, and follow-up recommendations

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!note] Vault audit 2026-07-24 — USE-1
> Use this for PDF-specific work — extract text/tables, merge/split, fill forms, create PDFs programmatically (no officecli PDF equivalent exists); for authoring .docx/.pptx/.xlsx use the canonical `officecli` family. Distinguishing axis: PDF manipulation vs officecli Office-document generation.

> [!note] Vault audit 2026-07-24 — MNT-8
> The "Visual Enhancement with Scientific Schematics" block in the source skill (hardcoded `scripts/generate_schematic.py` path) is copy-pasted across docx/pptx/xlsx/pdf and can drift; for schematic/diagram generation cross-reference the `scientific-schematics` skill rather than relying on the duplicated block.
