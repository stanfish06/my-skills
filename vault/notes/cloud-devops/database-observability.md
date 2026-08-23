---
title: database-observability
aliases:
  - database observability
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/database-observability/SKILL.md
created: 2026-08-23
---

# database-observability

> [!info] What it does
> Set up Grafana Cloud Database Observability for MySQL and PostgreSQL — enables `pg_stat_statements` / Performance Schema, creates a least-privilege monitoring user, configures the `database_observability.postgres` / `database_observability.mysql` Alloy components, ships query samples + visual explain plans + RED metrics + schema details to Grafana Cloud, and correlates slow queries with application traces via `db.statement` / `db.system` OTel attributes. Use when monitoring database performance, diagnosing slow queries, setting up DB observability for RDS / Aurora / Cloud SQL / Azure Database / self-managed instances, correlating DB metrics with APM, or alerting on query latency — even when the user says "my database is slow", "find the slow queries", or "monitor RDS" without saying "observability".

**Source:** [skills/database-observability/SKILL.md](../../../skills/database-observability/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [alloy](../../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [observability](../../notes/hosting-edge-platforms/observability.md) — Vercel Observability expert guidance — Drains (logs, traces, speed insights, web analytics), Web Analytics, Speed Insights, runtime logs, custom events, OpenTelemetry integration, and...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
