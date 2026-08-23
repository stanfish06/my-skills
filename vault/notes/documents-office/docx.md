---
title: docx
tags:
  - skill
  - domain/documents-office
domain: documents-office
status: untried
source: skills/docx/SKILL.md
created: 2026-06-09
---

# docx

> [!info] What it does
> Document toolkit (.docx). Create/edit documents, tracked changes, comments, formatting preservation, text extraction, for professional document processing.

**Source:** [skills/docx/SKILL.md](../../../skills/docx/SKILL.md)  ·  **Domain:** [Documents, Office & Media](../../maps/documents-office.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [cite-check](../../notes/literature-discovery/cite-check.md) — Cite-checks a brief, motion, or memo (PDF/Word): verifies each cited case is real, supports the proposition, is good law, and quoted accurately
- [draft-brief](../../notes/finance-investment/draft-brief.md) — Drafts court filings — motions, memoranda of law, appellate briefs — as court-ready .docx, with Midpage research behind every citation
- [draft-long-form-memo](../../notes/finance-investment/draft-long-form-memo.md) — Writes a formal objective legal research memo (Questions Presented, Brief Answers, Facts, IRAC Discussion, Conclusion) as a .docx
- [firecrawl-parse](../../notes/web-automation-frontend/firecrawl-parse.md) — Convert a local file (PDF, DOCX, XLSX, HTML, …) to markdown, or answer questions about its content
- [liteparse](../../notes/documents-office/liteparse.md) — Local document and PDF parsing with spatial text and bounding boxes
- [markitdown](../../notes/documents-office/markitdown.md) — Convert files and office documents to Markdown
- [officecli](../../notes/documents-office/officecli.md) — Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool
- [officecli-academic-paper](../../notes/documents-office/officecli-academic-paper.md) — Use this skill to build academic-style .docx output: journal / conference / thesis chapters carrying formal citation style (APA, Chicago, IEEE, MLA), numbered equations, figure & table...
- [officecli-docx](../../notes/documents-office/officecli-docx.md) — Use this skill any time a .docx file is involved -- as input, output, or both
- [officecli-word-form](../../notes/documents-office/officecli-word-form.md) — Use this skill to create fillable Word forms (.docx) with real Content Controls (SDT) + legacy FormField checkboxes + MERGEFIELD mail-merge placeholders + document protection
- [sharepoint-word-docs](../../notes/comms-productivity/sharepoint-word-docs.md) — Edit SharePoint-hosted Word `.docx` files while preserving document structure and styling

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!note] Vault audit 2026-07-24 — USE-1
> Use this as the raw-OOXML fallback — low-level .docx inspection, text extraction, tracked-changes/comment plumbing; for authoring or richly formatting Word documents use the canonical `officecli-docx` (and its scene layers). Distinguishing axis: raw OOXML processing vs officecli document generation.

> [!note] Vault audit 2026-07-24 — MNT-8
> The "Visual Enhancement with Scientific Schematics" block in the source skill (hardcoded `scripts/generate_schematic.py` path) is copy-pasted across docx/pptx/xlsx/pdf and can drift; for schematic/diagram generation cross-reference the `scientific-schematics` skill rather than relying on the duplicated block.
