---
title: neo4j-snowflake-graph-analytics-skill
aliases:
  - neo4j snowflake graph analytics skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-snowflake-graph-analytics-skill/SKILL.md
created: 2026-08-23
---

# neo4j-snowflake-graph-analytics-skill

> [!info] What it does
> Run Neo4j Graph Analytics algorithms (PageRank, Louvain, WCC, Dijkstra, KNN, Node2Vec, FastRP, GraphSAGE) directly inside Snowflake without moving data. Use when running graph algorithms against Snowflake tables via the Neo4j Snowflake Native App ("GDS Snowflake", "graph algorithms in Snowflake", "Neo4j Graph Analytics"). Covers the explore → prepare projection views → project-compute-write flow, the strict view/column type rules the graph engine requires, exact SQL CALL syntax, and privilege setup in both modes — app-identity grants and execute-as-user / per-user PAT auth (programmatic access token, set_enable_custom_credentials, register_user_role, caller grants). Does NOT cover Cypher or Neo4j DBMS queries — use neo4j-cypher-skill. Does NOT cover Aura Graph Analytics — use neo4j-aura-graph-analytics-skill. Does NOT cover self-managed GDS — use neo4j-gds-skill.

**Source:** [skills/neo4j-snowflake-graph-analytics-skill/SKILL.md](../../../skills/neo4j-snowflake-graph-analytics-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [auth](../../notes/security-auditing/auth.md) — Authentication integration guidance — Clerk (native Vercel Marketplace), Descope, and Auth0 setup for Next.js applications
- [neo4j-aura-graph-analytics-skill](../../notes/analytics-engineering/neo4j-aura-graph-analytics-skill.md) — Serverless Aura Graph Analytics (AGA) GDS Sessions — covers GdsSessions, AuraGraphDataScience, AuraAPICredentials, DbmsConnectionInfo, SessionMemory, get_or_create, remote graph...
- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-gds-skill](../../notes/analytics-engineering/neo4j-gds-skill.md) — Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph...
- [setup](../../notes/vault-meta/setup.md) — Verify Daloopa MCP connection and show available skills

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
