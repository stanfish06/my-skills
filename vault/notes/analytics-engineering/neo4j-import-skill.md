---
title: neo4j-import-skill
aliases:
  - neo4j import skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-import-skill/SKILL.md
created: 2026-08-23
---

# neo4j-import-skill

> [!info] What it does
> Import structured data into Neo4j — LOAD CSV, CALL IN TRANSACTIONS, neo4j-admin database import full (offline bulk), apoc.load.csv/json, apoc.periodic.iterate, driver batch writes. Covers method selection, header file format, type coercion, null handling, ON ERROR modes, CONCURRENT TRANSACTIONS, pre-import constraint setup, and post-import validation. Use when importing CSV/JSON/Parquet files, migrating relational data to graph, or bulk-loading large datasets. Does NOT handle unstructured document/PDF/vector chunking pipelines — use neo4j-document-import-skill. Does NOT handle live app write patterns (MERGE/CREATE) — use neo4j-cypher-skill. Does NOT handle neo4j-admin backup/restore/config — use neo4j-cli-tools-skill.

**Source:** [skills/neo4j-import-skill/SKILL.md](../../../skills/neo4j-import-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-cli-tools-skill](../../notes/analytics-engineering/neo4j-cli-tools-skill.md) — Use when working with Neo4j command-line tools — neo4j-cli (modern unified CLI — Cypher via Bolt, schema inspection, Aura management, Docker containers, credential management, agent...
- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-document-import-skill](../../notes/analytics-engineering/neo4j-document-import-skill.md) — Ingests unstructured and semi-structured documents into Neo4j as a knowledge graph
- [neo4j-kafka-skill](../../notes/analytics-engineering/neo4j-kafka-skill.md) — Configure and operate the Neo4j Connector for Kafka (sink + source) and the native Neo4j CDC API
- [neo4j-modeling-skill](../../notes/analytics-engineering/neo4j-modeling-skill.md) — Design, review, and refactor Neo4j graph data models
- [pdf](../../notes/documents-office/pdf.md) — PDF manipulation toolkit. Extract text/tables, create PDFs, merge/split, fill forms, for programmatic document processing and analysis
- [setup](../../notes/vault-meta/setup.md) — Verify Daloopa MCP connection and show available skills
- [validation](../../notes/software-dev/validation.md) — Use when Codex is already in the validation phase of a security scan or the user explicitly asks to determine whether one or more candidate security findings are valid

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
