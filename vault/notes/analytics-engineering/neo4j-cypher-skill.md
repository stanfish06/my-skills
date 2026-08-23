---
title: neo4j-cypher-skill
aliases:
  - neo4j cypher skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-cypher-skill/SKILL.md
created: 2026-08-23
---

# neo4j-cypher-skill

> [!info] What it does
> Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x. Use when writing new Cypher queries, optimizing slow queries, graph pattern matching, vector or fulltext search, subqueries, or batch writes. Covers MATCH, MERGE, CREATE, WITH, RETURN, CALL, UNWIND, FOREACH, LOAD CSV, SEARCH, expressions, functions, indexes, and subqueries. Does NOT handle driver migration or API changes — use neo4j-migration-skill. Does NOT cover DB administration or server ops — use neo4j-cli-tools-skill.

**Source:** [skills/neo4j-cypher-skill/SKILL.md](../../../skills/neo4j-cypher-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-aura-graph-analytics-skill](../../notes/analytics-engineering/neo4j-aura-graph-analytics-skill.md) — Serverless Aura Graph Analytics (AGA) GDS Sessions — covers GdsSessions, AuraGraphDataScience, AuraAPICredentials, DbmsConnectionInfo, SessionMemory, get_or_create, remote graph...
- [neo4j-aura-provisioning-skill](../../notes/analytics-engineering/neo4j-aura-provisioning-skill.md) — Provisions and manages Neo4j Aura instances via CLI (aura-cli v1.7+) or REST API
- [neo4j-cli-tools-skill](../../notes/analytics-engineering/neo4j-cli-tools-skill.md) — Use when working with Neo4j command-line tools — neo4j-cli (modern unified CLI — Cypher via Bolt, schema inspection, Aura management, Docker containers, credential management, agent...
- [neo4j-driver-dotnet-skill](../../notes/analytics-engineering/neo4j-driver-dotnet-skill.md) — Neo4j .NET Driver v6 — IDriver lifecycle, DI registration (singleton), ExecutableQuery fluent API, ExecuteReadAsync/ExecuteWriteAsync managed transactions, IResultCursor (FetchAsync/...
- [neo4j-driver-go-skill](../../notes/analytics-engineering/neo4j-driver-go-skill.md) — Covers the Neo4j Go Driver v6 — driver lifecycle, ExecuteQuery, managed and explicit transactions, session config, error handling, data type mapping, and connection tuning
- [neo4j-driver-java-skill](../../notes/analytics-engineering/neo4j-driver-java-skill.md) — Neo4j Java Driver v6 — driver lifecycle, Maven/Gradle setup, executableQuery, executeRead/Write managed transactions, explicit transactions, async/reactive patterns, error handling...
- [neo4j-driver-javascript-skill](../../notes/analytics-engineering/neo4j-driver-javascript-skill.md) — Neo4j JavaScript/TypeScript Driver v6 — driver lifecycle, executeQuery, managed transactions (executeRead/executeWrite), session.run, Integer handling, JSON serialization, record...
- [neo4j-driver-python-skill](../../notes/analytics-engineering/neo4j-driver-python-skill.md) — Neo4j Python Driver v6 — driver lifecycle, execute_query, managed and explicit transactions, async (AsyncGraphDatabase), result handling, data type mapping, error handling, UNWIND...
- [neo4j-gds-skill](../../notes/analytics-engineering/neo4j-gds-skill.md) — Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph...
- [neo4j-getting-started-skill](../../notes/analytics-engineering/neo4j-getting-started-skill.md) — Orchestrates zero-to-running-app in 8 stages — prerequisites → context → provision → model → load → explore → query → build
- [neo4j-graphql-skill](../../notes/analytics-engineering/neo4j-graphql-skill.md) — Build and configure a GraphQL API backed by Neo4j using @neo4j/graphql v7 (current) or v5 (LTS)
- [neo4j-import-skill](../../notes/analytics-engineering/neo4j-import-skill.md) — Import structured data into Neo4j — LOAD CSV, CALL IN TRANSACTIONS, neo4j-admin database import full (offline bulk), apoc.load.csv/json, apoc.periodic.iterate, driver batch writes
- [neo4j-kafka-skill](../../notes/analytics-engineering/neo4j-kafka-skill.md) — Configure and operate the Neo4j Connector for Kafka (sink + source) and the native Neo4j CDC API
- [neo4j-mcp-skill](../../notes/analytics-engineering/neo4j-mcp-skill.md) — Use when installing, configuring, or troubleshooting the official Neo4j MCP server (neo4j/mcp) — connecting Claude Code, Claude Desktop, Cursor, Windsurf, VS Code, Kiro, or other...
- [neo4j-migration-skill](../../notes/analytics-engineering/neo4j-migration-skill.md) — Migrates Neo4j driver code and Cypher queries from older versions (4.x, 5.x) to current (2025.x/2026.x, Cypher 25)
- [neo4j-modeling-skill](../../notes/analytics-engineering/neo4j-modeling-skill.md) — Design, review, and refactor Neo4j graph data models
- [neo4j-nvl-skill](../../notes/analytics-engineering/neo4j-nvl-skill.md) — Neo4j Visualization Library (NVL) — framework-agnostic graph rendering for the browser
- [neo4j-query-tuning-skill](../../notes/analytics-engineering/neo4j-query-tuning-skill.md) — Diagnoses and fixes slow Neo4j Cypher queries by reading execution plans, identifying bad operators (AllNodesScan, CartesianProduct, Eager, NodeByLabelScan), and prescribing fixes...
- [neo4j-security-skill](../../notes/analytics-engineering/neo4j-security-skill.md) — Programmatic security management in Neo4j — RBAC/ABAC, user lifecycle (CREATE/ALTER/DROP USER), role lifecycle (CREATE/GRANT ROLE/DROP ROLE), privilege grants and denies...
- [neo4j-snowflake-graph-analytics-skill](../../notes/analytics-engineering/neo4j-snowflake-graph-analytics-skill.md) — Run Neo4j Graph Analytics algorithms (PageRank, Louvain, WCC, Dijkstra, KNN, Node2Vec, FastRP, GraphSAGE) directly inside Snowflake without moving data
- [neo4j-spark-skill](../../notes/analytics-engineering/neo4j-spark-skill.md) — Use when reading from or writing to Neo4j with Apache Spark or Databricks using the Neo4j Connector for Apache Spark 6.0 (org.neo4j.connectors:spark) or 5.x...
- [neo4j-spring-data-skill](../../notes/analytics-engineering/neo4j-spring-data-skill.md) — Use when building Spring Boot applications with Neo4j using Spring Data Neo4j (SDN 7.x/8.x) — @Node entity mapping, @Relationship, @RelationshipProperties, Neo4jRepository...
- [neo4j-vector-index-skill](../../notes/analytics-engineering/neo4j-vector-index-skill.md) — Create and manage Neo4j vector indexes, run vector similarity search (ANN/kNN), store embeddings on nodes or relationships, use SEARCH clause (Neo4j 2026.01+, preferred) or...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
