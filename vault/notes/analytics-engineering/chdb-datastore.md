---
title: chdb-datastore
aliases:
  - chdb datastore
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/chdb-datastore/SKILL.md
created: 2026-08-23
---

# chdb-datastore

> [!info] What it does
> Use when the user has tabular data (pandas DataFrame, parquet, csv, Arrow, json) and wants to filter, group, aggregate, join, or speed up slow pandas. Provides chDB DataStore — same pandas API, ClickHouse engine underneath. Also handles reading from S3, MySQL, PostgreSQL, MongoDB, ClickHouse Cloud, Iceberg, Delta Lake as DataFrames and joining across sources. TRIGGER when: user mentions DataFrame, parquet, csv, "fast pandas", "speed up pandas", or cross-source DataFrame joins; user imports `chdb.datastore` or `from datastore import DataStore`. SKIP this skill for raw SQL syntax (use chdb-sql instead), ClickHouse server administration, or non-Python DataStore API work.

**Source:** [skills/chdb-datastore/SKILL.md](../../../skills/chdb-datastore/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [chdb-sql](../../notes/analytics-engineering/chdb-sql.md) — Use when the user wants to run SQL — especially analytical SQL — on local files (parquet/csv/json), URLs, S3 paths, or remote databases (Postgres, MySQL, MongoDB, ClickHouse Cloud...
- [pandas](../../notes/data-science-compute/pandas.md) — The workhorse library for in-memory tabular data in Python

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
