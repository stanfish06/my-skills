---
title: neo4j-migration-skill
aliases:
  - neo4j migration skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-migration-skill/SKILL.md
created: 2026-08-23
---

# neo4j-migration-skill

> [!info] What it does
> Migrates Neo4j driver code and Cypher queries from older versions (4.x, 5.x) to current (2025.x/2026.x, Cypher 25). Covers Python, JavaScript/Node.js, Java, .NET, and Go drivers — package renames, removed APIs, version requirements, diff-ready fixes. Also handles Cypher syntax migration — QPE paths, CALL subqueries, id() → elementId(), PERIODIC COMMIT → CALL IN TRANSACTIONS, and all Cypher 25 removals. Does NOT write new Cypher queries — use neo4j-cypher-skill. Does NOT cover DB administration or server ops — use neo4j-cli-tools-skill. Does NOT provision new Neo4j instances — use neo4j-getting-started-skill.

**Source:** [skills/neo4j-migration-skill/SKILL.md](../../../skills/neo4j-migration-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [neo4j-cli-tools-skill](../../notes/analytics-engineering/neo4j-cli-tools-skill.md) — Use when working with Neo4j command-line tools — neo4j-cli (modern unified CLI — Cypher via Bolt, schema inspection, Aura management, Docker containers, credential management, agent...
- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-driver-dotnet-skill](../../notes/analytics-engineering/neo4j-driver-dotnet-skill.md) — Neo4j .NET Driver v6 — IDriver lifecycle, DI registration (singleton), ExecutableQuery fluent API, ExecuteReadAsync/ExecuteWriteAsync managed transactions, IResultCursor (FetchAsync/...
- [neo4j-driver-go-skill](../../notes/analytics-engineering/neo4j-driver-go-skill.md) — Covers the Neo4j Go Driver v6 — driver lifecycle, ExecuteQuery, managed and explicit transactions, session config, error handling, data type mapping, and connection tuning
- [neo4j-driver-java-skill](../../notes/analytics-engineering/neo4j-driver-java-skill.md) — Neo4j Java Driver v6 — driver lifecycle, Maven/Gradle setup, executableQuery, executeRead/Write managed transactions, explicit transactions, async/reactive patterns, error handling...
- [neo4j-driver-javascript-skill](../../notes/analytics-engineering/neo4j-driver-javascript-skill.md) — Neo4j JavaScript/TypeScript Driver v6 — driver lifecycle, executeQuery, managed transactions (executeRead/executeWrite), session.run, Integer handling, JSON serialization, record...
- [neo4j-driver-python-skill](../../notes/analytics-engineering/neo4j-driver-python-skill.md) — Neo4j Python Driver v6 — driver lifecycle, execute_query, managed and explicit transactions, async (AsyncGraphDatabase), result handling, data type mapping, error handling, UNWIND...
- [neo4j-getting-started-skill](../../notes/analytics-engineering/neo4j-getting-started-skill.md) — Orchestrates zero-to-running-app in 8 stages — prerequisites → context → provision → model → load → explore → query → build
- [neo4j-spring-data-skill](../../notes/analytics-engineering/neo4j-spring-data-skill.md) — Use when building Spring Boot applications with Neo4j using Spring Data Neo4j (SDN 7.x/8.x) — @Node entity mapping, @Relationship, @RelationshipProperties, Neo4jRepository...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
