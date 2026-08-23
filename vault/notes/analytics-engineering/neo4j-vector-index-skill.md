---
title: neo4j-vector-index-skill
aliases:
  - neo4j vector index skill
  - ANN
  - kNN
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-vector-index-skill/SKILL.md
created: 2026-08-23
---

# neo4j-vector-index-skill

> [!info] What it does
> Create and manage Neo4j vector indexes, run vector similarity search (ANN/kNN), store embeddings on nodes or relationships, use SEARCH clause (Neo4j 2026.01+, preferred) or db.index.vector.queryNodes() procedure (deprecated 2026.04, still works on 2025.x), configure HNSW and quantization options, pick similarity function and embedding provider dimensions, and batch-update embeddings. Use when tasks involve CREATE VECTOR INDEX, vector.dimensions, cosine/euclidean search, embedding ingestion pipelines, semantic or structural nearest-neighbor lookup, or hybrid search (vector + fulltext, multiple vector sources, or graph-derived scores). Does NOT handle GraphRAG retrieval_query graph traversal — use neo4j-graphrag-skill. Does NOT handle fulltext-only/keyword-only search — use neo4j-cypher-skill. Does NOT compute GDS graph embeddings (FastRP, Node2Vec) — use neo4j-gds-skill.

**Source:** [skills/neo4j-vector-index-skill/SKILL.md](../../../skills/neo4j-vector-index-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-aura-agent-skill](../../notes/analytics-engineering/neo4j-aura-agent-skill.md) — Manages Neo4j Aura Agents via the v2beta1 REST API — create, list, get, update, delete, and invoke Aura agents backed by an AuraDB instance
- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-gds-skill](../../notes/analytics-engineering/neo4j-gds-skill.md) — Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph...
- [neo4j-genai-plugin-skill](../../notes/analytics-engineering/neo4j-genai-plugin-skill.md) — Use Neo4j GenAI Plugin ai.text.* functions and procedures for in-Cypher embedding generation, text completion, structured output, chat, tokenization, and batch ingestion
- [neo4j-graphrag-skill](../../notes/analytics-engineering/neo4j-graphrag-skill.md) — Build GraphRAG retrieval pipelines on Neo4j using the neo4j-graphrag Python package (v1.16.0+)

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
