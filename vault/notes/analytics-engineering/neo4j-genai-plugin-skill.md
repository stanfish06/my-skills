---
title: neo4j-genai-plugin-skill
aliases:
  - neo4j genai plugin skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-genai-plugin-skill/SKILL.md
created: 2026-08-23
---

# neo4j-genai-plugin-skill

> [!info] What it does
> Use Neo4j GenAI Plugin ai.text.* functions and procedures for in-Cypher embedding generation, text completion, structured output, chat, tokenization, and batch ingestion. Covers ai.text.embed(), ai.text.embedBatch(), ai.text.completion(), ai.text.structuredCompletion(), ai.text.aggregateCompletion(), ai.text.chat(), ai.text.tokenCount(), ai.text.chunkByTokenLimit(), and provider configuration for OpenAI, Azure OpenAI, VertexAI, and Amazon Bedrock. Requires CYPHER 25. Replaces deprecated genai.vector.encode(). Use when writing pure-Cypher GraphRAG, embedding nodes in-graph, generating structured maps from prompts, or calling LLMs inside Cypher queries. Does NOT handle neo4j-graphrag Python library pipelines — use neo4j-graphrag-skill. Does NOT handle vector index creation/search — use neo4j-vector-index-skill.

**Source:** [skills/neo4j-genai-plugin-skill/SKILL.md](../../../skills/neo4j-genai-plugin-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-graphrag-skill](../../notes/analytics-engineering/neo4j-graphrag-skill.md) — Build GraphRAG retrieval pipelines on Neo4j using the neo4j-graphrag Python package (v1.16.0+)
- [neo4j-vector-index-skill](../../notes/analytics-engineering/neo4j-vector-index-skill.md) — Create and manage Neo4j vector indexes, run vector similarity search (ANN/kNN), store embeddings on nodes or relationships, use SEARCH clause (Neo4j 2026.01+, preferred) or...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
