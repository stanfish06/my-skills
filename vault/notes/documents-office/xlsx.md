---
title: xlsx
tags:
  - skill
  - domain/documents-office
domain: documents-office
status: untried
source: skills/xlsx/SKILL.md
created: 2026-06-09
---

# xlsx

> [!info] What it does
> Spreadsheet toolkit (.xlsx/.csv). Create/edit with formulas/formatting, analyze data, visualization, recalculate formulas, for spreadsheet processing and analysis.

**Source:** [skills/xlsx/SKILL.md](../../../skills/xlsx/SKILL.md)  ·  **Domain:** [Documents, Office & Media](../../maps/documents-office.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [firecrawl-parse](../../notes/web-automation-frontend/firecrawl-parse.md) — Convert a local file (PDF, DOCX, XLSX, HTML, …) to markdown, or answer questions about its content
- [initiate](../../notes/vault-meta/initiate.md) — Initiate coverage — generate both research note (HTML) and Excel model (.xlsx)
- [markitdown](../../notes/documents-office/markitdown.md) — Convert files and office documents to Markdown
- [officecli](../../notes/documents-office/officecli.md) — Create, analyze, proofread, and modify Office documents (.docx, .xlsx, .pptx) using the officecli CLI tool
- [officecli-data-dashboard](../../notes/documents-office/officecli-data-dashboard.md) — Use this skill to build a multi-element Excel dashboard — Dashboard sheet on open, multiple formula-driven KPI cards, multiple charts, sparklines, and conditional formatting — from CSV...
- [officecli-financial-model](../../notes/documents-office/officecli-financial-model.md) — Use this skill when the user wants to build a financial model — 3-statement model, DCF valuation, LBO, SaaS unit economics, sensitivity / scenario analysis, debt schedule, or...
- [officecli-xlsx](../../notes/documents-office/officecli-xlsx.md) — Use this skill any time a .xlsx file is involved -- as input, output, or both

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!note] Vault audit 2026-07-24 — USE-1
> Use this as the raw-OOXML fallback — low-level .xlsx/.csv inspection and data extraction; for authoring formatted workbooks, models, or dashboards use the canonical `officecli-xlsx` (scene layers: `officecli-financial-model`, `officecli-data-dashboard`). Distinguishing axis: raw spreadsheet processing vs officecli workbook generation.

> [!note] Vault audit 2026-07-24 — MNT-8
> The "Visual Enhancement with Scientific Schematics" block in the source skill (hardcoded `scripts/generate_schematic.py` path) is copy-pasted across docx/pptx/xlsx/pdf and can drift; for schematic/diagram generation cross-reference the `scientific-schematics` skill rather than relying on the duplicated block.
