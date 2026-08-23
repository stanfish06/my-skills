---
title: tempo
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/tempo/SKILL.md
created: 2026-08-23
---

# tempo

> [!info] What it does
> Stand up Grafana Tempo as a cost-efficient distributed-tracing backend that only needs object storage, and write TraceQL queries against it. Covers OTLP + Jaeger + Zipkin ingestion, the distributor → live-store → block-builder → object-storage write path, metrics-generator for RED spanmetrics + service graphs, Helm `tempo-distributed` deployment, multi-tenant `X-Scope-OrgID`, TraceQL span / resource / event scopes, structural operators (`>>`, `<<`), `rate()` + `quantile_over_time` metrics, and the traces-to-logs / metrics / profiles datasource links. Use when deploying Tempo, writing a TraceQL query for slow / errored requests, debugging "no traces showing in Explore", sizing queriers / compactors, configuring S3 / GCS / Azure block storage, or wiring trace ↔ log ↔ profile correlation — even when the user says "tracing backend", "find slow requests", "show me the service graph", "store traces in S3", "Jaeger compatible store", or "what called this span" without naming Tempo.

**Source:** [skills/tempo/SKILL.md](../../../skills/tempo/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [alloy](../../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [beyla](../../notes/cloud-devops/beyla.md) — Auto-instrument an application's HTTP / gRPC / DB traffic with Grafana Beyla eBPF — no code changes, no SDK, no restart
- [grafana-oss](../../notes/cloud-devops/grafana-oss.md) — Configure Grafana OSS — provisions dashboards from YAML, sets up data sources (Prometheus / Loki / Tempo / Pyroscope), writes dashboard JSON with template variables, builds panel...
- [opentelemetry](../../notes/cloud-devops/opentelemetry.md) — Instrument any app with OpenTelemetry and ship metrics / logs / traces to Grafana Cloud or self-hosted Mimir / Loki / Tempo / Pyroscope
- [pyroscope](../../notes/cloud-devops/pyroscope.md) — Continuously profile applications with Grafana Pyroscope and read the result as flame graphs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
