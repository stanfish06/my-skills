---
title: neo4j-gds-skill
aliases:
  - neo4j gds skill
  - GDS
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-gds-skill/SKILL.md
created: 2026-08-23
---

# neo4j-gds-skill

> [!info] What it does
> Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph catalog operations, stream/stats/mutate/write modes, memory estimation, PageRank, Louvain, WCC, FastRP, KNN, Node Similarity, ML pipelines, and cleanup. Use for Aura Pro, self-managed, local, or offline Neo4j DBMS with the GDS plugin installed. Does NOT cover Aura Graph Analytics GDS Sessions, AuraGraphDataScience, GdsSessions, gds.graph.project.remote, or AuraDB Cypher API projection/session management — use neo4j-aura-graph-analytics-skill. Does NOT handle Cypher authoring — use neo4j-cypher-skill. Does NOT cover driver setup — use neo4j-driver-python-skill or other driver skill.

**Source:** [skills/neo4j-gds-skill/SKILL.md](../../../skills/neo4j-gds-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-aura-graph-analytics-skill](../../notes/analytics-engineering/neo4j-aura-graph-analytics-skill.md) — Serverless Aura Graph Analytics (AGA) GDS Sessions — covers GdsSessions, AuraGraphDataScience, AuraAPICredentials, DbmsConnectionInfo, SessionMemory, get_or_create, remote graph...
- [neo4j-aura-provisioning-skill](../../notes/analytics-engineering/neo4j-aura-provisioning-skill.md) — Provisions and manages Neo4j Aura instances via CLI (aura-cli v1.7+) or REST API
- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-driver-python-skill](../../notes/analytics-engineering/neo4j-driver-python-skill.md) — Neo4j Python Driver v6 — driver lifecycle, execute_query, managed and explicit transactions, async (AsyncGraphDatabase), result handling, data type mapping, error handling, UNWIND...
- [neo4j-graphrag-skill](../../notes/analytics-engineering/neo4j-graphrag-skill.md) — Build GraphRAG retrieval pipelines on Neo4j using the neo4j-graphrag Python package (v1.16.0+)
- [neo4j-kafka-skill](../../notes/analytics-engineering/neo4j-kafka-skill.md) — Configure and operate the Neo4j Connector for Kafka (sink + source) and the native Neo4j CDC API
- [neo4j-query-tuning-skill](../../notes/analytics-engineering/neo4j-query-tuning-skill.md) — Diagnoses and fixes slow Neo4j Cypher queries by reading execution plans, identifying bad operators (AllNodesScan, CartesianProduct, Eager, NodeByLabelScan), and prescribing fixes...
- [neo4j-snowflake-graph-analytics-skill](../../notes/analytics-engineering/neo4j-snowflake-graph-analytics-skill.md) — Run Neo4j Graph Analytics algorithms (PageRank, Louvain, WCC, Dijkstra, KNN, Node2Vec, FastRP, GraphSAGE) directly inside Snowflake without moving data
- [neo4j-spark-skill](../../notes/analytics-engineering/neo4j-spark-skill.md) — Use when reading from or writing to Neo4j with Apache Spark or Databricks using the Neo4j Connector for Apache Spark 6.0 (org.neo4j.connectors:spark) or 5.x...
- [neo4j-vector-index-skill](../../notes/analytics-engineering/neo4j-vector-index-skill.md) — Create and manage Neo4j vector indexes, run vector similarity search (ANN/kNN), store embeddings on nodes or relationships, use SEARCH clause (Neo4j 2026.01+, preferred) or...
- [setup](../../notes/vault-meta/setup.md) — Verify Daloopa MCP connection and show available skills

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
