---
title: neo4j-document-import-skill
aliases:
  - neo4j document import skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-document-import-skill/SKILL.md
created: 2026-08-23
---

# neo4j-document-import-skill

> [!info] What it does
> Ingests unstructured and semi-structured documents into Neo4j as a knowledge graph. Use when chunking PDFs, HTML, plain text, or Markdown; extracting entities and relationships from text with an LLM (SimpleKGPipeline, neo4j-graphrag); loading JSON via apoc.load.json; building Document→Chunk→Entity graph structures; or connecting LangChain/LlamaIndex document loaders to Neo4j. Covers neo4j-graphrag SimpleKGPipeline, LLM Graph Builder web UI, entity resolution, chunking strategies, and graph schema design for RAG pipelines. Does NOT handle structured CSV/relational import — use neo4j-import-skill. Does NOT handle GraphRAG retrieval after ingestion — use neo4j-graphrag-skill. Does NOT handle vector index creation — use neo4j-vector-search-skill.

**Source:** [skills/neo4j-document-import-skill/SKILL.md](../../../skills/neo4j-document-import-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [chunk](../../notes/ml-ai/chunk.md) — Use CircleCI Chunk for AI-assisted CI/CD work through either the Chunk web UI or the chunk-cli
- [neo4j-graphrag-skill](../../notes/analytics-engineering/neo4j-graphrag-skill.md) — Build GraphRAG retrieval pipelines on Neo4j using the neo4j-graphrag Python package (v1.16.0+)
- [neo4j-import-skill](../../notes/analytics-engineering/neo4j-import-skill.md) — Import structured data into Neo4j — LOAD CSV, CALL IN TRANSACTIONS, neo4j-admin database import full (offline bulk), apoc.load.csv/json, apoc.periodic.iterate, driver batch writes

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
