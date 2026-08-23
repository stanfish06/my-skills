---
title: mimir
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/mimir/SKILL.md
created: 2026-08-23
---

# mimir

> [!info] What it does
> Stand up Grafana Mimir for horizontally scalable, multi-tenant, long-term Prometheus + OTLP metrics storage. Covers monolithic / read-write / microservices deployment, S3 / GCS / Azure / filesystem block storage, Prometheus `remote_write` and OTLP ingestion, multi-tenancy with `X-Scope-OrgID`, ingester replication factor, compactor retention, and per-tenant limits. Use when running Mimir locally or on Kubernetes (Helm `mimir-distributed`), scaling Prometheus past a single node, picking ingest / query / backend split, configuring tenants and ingestion rate, debugging `/ready` 503s or `429 Too Many Requests`, or pointing Grafana at a Mimir datasource — even when the user says "I need long-term Prometheus storage", "scale Prometheus", "multi-tenant metrics backend", "Cortex replacement", "remote_write target", or "store 10M active series" without naming Mimir.

**Source:** [skills/mimir/SKILL.md](../../../skills/mimir/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [adaptive-metrics](../../notes/cloud-devops/adaptive-metrics.md) — Cut Grafana Cloud Metrics cost by shrinking active-series count with Adaptive Metrics aggregation rules — auto-recommendations from query history, custom exact/regex rules, label-drop...
- [beyla](../../notes/cloud-devops/beyla.md) — Auto-instrument an application's HTTP / gRPC / DB traffic with Grafana Beyla eBPF — no code changes, no SDK, no restart
- [dpm-finder](../../notes/cloud-devops/dpm-finder.md) — Find the Prometheus metrics that drive your Grafana Cloud bill
- [opentelemetry](../../notes/cloud-devops/opentelemetry.md) — Instrument any app with OpenTelemetry and ship metrics / logs / traces to Grafana Cloud or self-hosted Mimir / Loki / Tempo / Pyroscope
- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [promql](../../notes/cloud-devops/promql.md) — Write, validate, and optimize PromQL for Prometheus / Grafana Mimir / Grafana Cloud Metrics

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
