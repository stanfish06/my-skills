---
title: literature-review
aliases:
  - systematic review
  - literature review
tags:
  - skill
  - domain/literature-discovery
domain: literature-discovery
status: untried
source: skills/literature-review/SKILL.md
created: 2026-06-09
---

# literature-review

> [!info] What it does
> Conduct comprehensive, systematic literature reviews using multiple academic databases (PubMed, arXiv, bioRxiv, Semantic Scholar, etc.). Use when conducting systematic literature reviews, meta-analyses, research synthesis, or comprehensive literature searches across biomedical, scientific, and technical domains. Creates professionally formatted markdown documents and PDFs with verified citations in multiple citation styles (APA, Nature, Vancouver, etc.).

**Source:** [skills/literature-review/SKILL.md](../../../skills/literature-review/SKILL.md)  ·  **Domain:** [Literature Search & Knowledge Discovery](../../maps/literature-discovery.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [citations](../../notes/literature-discovery/citations.md) — Canonical rules and HTML/CSS contract for inline `[n]` citation references, end-of-document Citations blocks, and optional per-section citation recaps used across Moody's Agentic...
- [research](../../notes/software-dev/research.md) — Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!warning] Vault audit 2026-07-24 — MNT-6
> `gget search pubmed` / `gget search biorxiv` (SKILL.md ~L97–98, 304, 322) don't exist — `gget search` is Ensembl-gene-only and has no bioRxiv module, so those commands fail. Use the `paper-lookup` skill / NCBI Entrez / the bioRxiv API for literature search instead.
> _Remote-managed skill — the durable fix belongs upstream; this wrapper note is the local record._
