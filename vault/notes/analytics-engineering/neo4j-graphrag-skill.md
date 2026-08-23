---
title: neo4j-graphrag-skill
aliases:
  - neo4j graphrag skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-graphrag-skill/SKILL.md
created: 2026-08-23
---

# neo4j-graphrag-skill

> [!info] What it does
> Build GraphRAG retrieval pipelines on Neo4j using the neo4j-graphrag Python package (v1.16.0+). Covers retriever selection (VectorRetriever, HybridRetriever, VectorCypherRetriever, HybridCypherRetriever, Text2CypherRetriever, ToolsRetriever), external vector DB retrievers (Weaviate, Pinecone, Qdrant), retrieval_query Cypher fragments, query_params, filters, GraphRAG pipeline wiring (GraphRAG + LLM + prompt), all LLM providers (OpenAI, Anthropic, VertexAI, Bedrock, Cohere, Mistral, Ollama), embedder setup, index creation, token usage tracking, Cypher 25 SEARCH clause, and LangChain/LlamaIndex integration. Does NOT handle KG construction — use neo4j-document-import-skill. Does NOT handle plain vector search — use neo4j-vector-index-skill. Does NOT handle GDS analytics — use neo4j-gds-skill. Does NOT handle agent memory — use neo4j-agent-memory-skill.

**Source:** [skills/neo4j-graphrag-skill/SKILL.md](../../../skills/neo4j-graphrag-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-agent-memory-skill](../../notes/analytics-engineering/neo4j-agent-memory-skill.md) — Authoritative reference for the neo4j-agent-memory Python package — a graph-native memory system for AI agents built on Neo4j — and for the hosted service (NAMS) at memory.neo4jlabs.com
- [neo4j-document-import-skill](../../notes/analytics-engineering/neo4j-document-import-skill.md) — Ingests unstructured and semi-structured documents into Neo4j as a knowledge graph
- [neo4j-driver-python-skill](../../notes/analytics-engineering/neo4j-driver-python-skill.md) — Neo4j Python Driver v6 — driver lifecycle, execute_query, managed and explicit transactions, async (AsyncGraphDatabase), result handling, data type mapping, error handling, UNWIND...
- [neo4j-gds-skill](../../notes/analytics-engineering/neo4j-gds-skill.md) — Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph...
- [neo4j-genai-plugin-skill](../../notes/analytics-engineering/neo4j-genai-plugin-skill.md) — Use Neo4j GenAI Plugin ai.text.* functions and procedures for in-Cypher embedding generation, text completion, structured output, chat, tokenization, and batch ingestion
- [neo4j-vector-index-skill](../../notes/analytics-engineering/neo4j-vector-index-skill.md) — Create and manage Neo4j vector indexes, run vector similarity search (ANN/kNN), store embeddings on nodes or relationships, use SEARCH clause (Neo4j 2026.01+, preferred) or...
- [setup](../../notes/vault-meta/setup.md) — Verify Daloopa MCP connection and show available skills

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
