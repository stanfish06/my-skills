---
title: neo4j-kafka-skill
aliases:
  - neo4j kafka skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-kafka-skill/SKILL.md
created: 2026-08-23
---

# neo4j-kafka-skill

> [!info] What it does
> Configure and operate the Neo4j Connector for Kafka (sink + source) and the native Neo4j CDC API. Covers Cypher/Pattern/CUD sink strategies, CDC-based and query-based source, exactly-once semantics, DLQ error handling, Confluent Cloud managed connector, schema registry (Avro/JSON), and native db.cdc.query cursor-loop patterns (Neo4j 5.13+ Enterprise/Aura BC/VDC). Use when streaming Kafka events into Neo4j, streaming Neo4j changes to Kafka, or querying Neo4j change events without Kafka. Does NOT handle Cypher query authoring — use neo4j-cypher-skill. Does NOT handle bulk CSV/file import — use neo4j-import-skill. Does NOT handle GDS algorithms — use neo4j-gds-skill.

**Source:** [skills/neo4j-kafka-skill/SKILL.md](../../../skills/neo4j-kafka-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-gds-skill](../../notes/analytics-engineering/neo4j-gds-skill.md) — Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph...
- [neo4j-import-skill](../../notes/analytics-engineering/neo4j-import-skill.md) — Import structured data into Neo4j — LOAD CSV, CALL IN TRANSACTIONS, neo4j-admin database import full (offline bulk), apoc.load.csv/json, apoc.periodic.iterate, driver batch writes

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
