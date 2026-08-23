---
title: neo4j-query-tuning-skill
aliases:
  - neo4j query tuning skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-query-tuning-skill/SKILL.md
created: 2026-08-23
---

# neo4j-query-tuning-skill

> [!info] What it does
> Diagnoses and fixes slow Neo4j Cypher queries by reading execution plans, identifying bad operators (AllNodesScan, CartesianProduct, Eager, NodeByLabelScan), and prescribing fixes (indexes, hints, query rewrites, runtime selection). Use when a query is slow, when EXPLAIN or PROFILE output needs interpretation, when dbHits or pageCacheHitRatio are poor, when cardinality estimation diverges from actuals, or when deciding between slotted/pipelined/parallel runtimes. Covers USING INDEX / USING SCAN / USING JOIN hints, db.stats.retrieve, SHOW QUERIES, SHOW TRANSACTIONS, TERMINATE TRANSACTION. Does NOT write new Cypher from scratch — use neo4j-cypher-skill. Does NOT cover GDS algorithm tuning — use neo4j-gds-skill. Does NOT cover index/constraint creation syntax details — use neo4j-cypher-skill references/indexes.md.

**Source:** [skills/neo4j-query-tuning-skill/SKILL.md](../../../skills/neo4j-query-tuning-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-gds-skill](../../notes/analytics-engineering/neo4j-gds-skill.md) — Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
