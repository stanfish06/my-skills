---
title: research-lookup
aliases:
  - research lookup
tags:
  - skill
  - domain/literature-discovery
domain: literature-discovery
status: untried
source: skills/research-lookup/SKILL.md
created: 2026-06-09
---

# research-lookup

> [!info] What it does
> Look up current research information using parallel-cli search (primary, fast web search) or the Parallel Chat API (deep research). Automatically routes queries to the best backend. Use for finding papers, gathering research data, and verifying scientific information.

**Source:** [skills/research-lookup/SKILL.md](../../../skills/research-lookup/SKILL.md)  ·  **Domain:** [Literature Search & Knowledge Discovery](../../maps/literature-discovery.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [infographics](../../notes/documents-office/infographics.md) — Create professional infographics using Nano Banana Pro AI with smart iterative refinement
- [market-research-reports](../../notes/documents-office/market-research-reports.md) — Generate comprehensive market research reports (50+ pages) in the style of top consulting firms (McKinsey, BCG, Gartner)
- [research](../../notes/software-dev/research.md) — Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo
- [scientific-writing](../../notes/research-writing/scientific-writing.md) — Core skill for the deep research and writing tool

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!note] Vault audit 2026-07-24 — USE-4
> Explicit alias — this is a thin router over `parallel-web` (dispatching to parallel-cli search or the Parallel deep-research API); prefer `parallel-web` directly, use `exa-search` for Exa-backed scholarly filtering, and `paper-lookup` for a scholarly-DB paper hunt. Distinguishing axis: convenience wrapper, not a separate backend.
