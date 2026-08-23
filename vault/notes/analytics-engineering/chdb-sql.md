---
title: chdb-sql
aliases:
  - chdb sql
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/chdb-sql/SKILL.md
created: 2026-08-23
---

# chdb-sql

> [!info] What it does
> Use when the user wants to run SQL — especially analytical SQL — on local files (parquet/csv/json), URLs, S3 paths, or remote databases (Postgres, MySQL, MongoDB, ClickHouse Cloud, Iceberg, Delta Lake) without setting up a server. Provides chDB — embedded ClickHouse SQL in Python with 1000+ functions, Session for stateful multi-step pipelines, parametrized queries, and cross-source joins via `s3()`, `mysql()`, `postgresql()`, `iceberg()`, `deltaLake()`, `remoteSecure()` table functions. TRIGGER when: user wants SQL on parquet/csv/files or across remote analytical sources; uses ClickHouse SQL features (window functions, windowFunnel, geoToH3, JSON path ops, Session, parametrized queries); imports `chdb` or calls `chdb.query()`. SKIP this skill for pandas-style DataFrame method-chaining (use chdb-datastore instead) or ClickHouse server administration.

**Source:** [skills/chdb-sql/SKILL.md](../../../skills/chdb-sql/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [chdb-datastore](../../notes/analytics-engineering/chdb-datastore.md) — Use when the user has tabular data (pandas DataFrame, parquet, csv, Arrow, json) and wants to filter, group, aggregate, join, or speed up slow pandas

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
