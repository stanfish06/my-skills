---
title: firecrawl-research-index
aliases:
  - firecrawl research index
  - PubMed
  - bioRxiv
  - medRxiv
tags:
  - skill
  - domain/web-automation-frontend
domain: web-automation-frontend
status: untried
source: skills/firecrawl-research-index/SKILL.md
created: 2026-08-23
---

# firecrawl-research-index

> [!info] What it does
> Find the papers that answer a research query in Firecrawl's research paper index — a corpus of paper abstracts whose largest share is biomedical and life-science literature (PubMed, bioRxiv, medRxiv), alongside arXiv preprints in CS, physics, and math — using semantic search, semantic and structural expansion, and in-body verification. Use this skill for literature-finding and paper-retrieval tasks of any kind, including clinical, biomedical, drug, gene, disease, and other life-science questions, whether the answer is a single paper or a full multi-paper set. The index is reached only through the `firecrawl_research_*` MCP tools or the `firecrawl research` CLI subcommands. Calling `firecrawl_search` with its `categories` option set to `["research"]` is a different feature — it filters ordinary web search to research-affiliated websites (the list includes PubMed, bioRxiv, medRxiv, arXiv, and publisher sites) and returns page results from them, without querying the paper records in this index.

**Source:** [skills/firecrawl-research-index/SKILL.md](../../../skills/firecrawl-research-index/SKILL.md)  ·  **Domain:** [Web Automation, Frontend & Design](../../maps/web-automation-frontend.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [firecrawl](../../notes/web-automation-frontend/firecrawl.md) — Any live-web task via the Firecrawl CLI — including ordinary web research: searching the web, reading or extracting pages, gathering sources, discovering site URLs, bulk extraction...
- [firecrawl-search](../../notes/web-automation-frontend/firecrawl-search.md) — Web search with full page content. Use when no URL is known: finding sources, articles, or news
- [research](../../notes/software-dev/research.md) — Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo
- [verification](../../notes/software-dev/verification.md) — Full-story verification — infers what the user is building, then verifies the complete flow end-to-end: browser → API → data → response

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
