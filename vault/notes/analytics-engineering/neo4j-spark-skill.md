---
title: neo4j-spark-skill
aliases:
  - neo4j spark skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-spark-skill/SKILL.md
created: 2026-08-23
---

# neo4j-spark-skill

> [!info] What it does
> Use when reading from or writing to Neo4j with Apache Spark or Databricks using the Neo4j Connector for Apache Spark 6.0 (org.neo4j.connectors:spark) or 5.x (org.neo4j:neo4j-connector-apache-spark). Covers SparkSession setup, DataFrame reads via labels/Cypher/relationship scan, DataFrame writes with SaveMode, node.keys for MERGE, relationship write mapping, partition and batch tuning, PySpark and Scala examples, Databricks cluster config, Databricks secrets for credentials, Delta Lake to Neo4j pipelines. Does NOT handle Cypher authoring — use neo4j-cypher-skill. Does NOT handle the Python bolt driver — use neo4j-driver-python-skill. Does NOT handle GDS algorithms — use neo4j-gds-skill.

**Source:** [skills/neo4j-spark-skill/SKILL.md](../../../skills/neo4j-spark-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-driver-python-skill](../../notes/analytics-engineering/neo4j-driver-python-skill.md) — Neo4j Python Driver v6 — driver lifecycle, execute_query, managed and explicit transactions, async (AsyncGraphDatabase), result handling, data type mapping, error handling, UNWIND...
- [neo4j-gds-skill](../../notes/analytics-engineering/neo4j-gds-skill.md) — Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph...
- [setup](../../notes/vault-meta/setup.md) — Verify Daloopa MCP connection and show available skills

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
