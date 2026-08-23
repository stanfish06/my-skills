---
title: alloy
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/alloy/SKILL.md
created: 2026-08-23
---

# alloy

> [!info] What it does
> Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus / Loki / Tempo / Pyroscope. Covers the Alloy config language (blocks, `sys.env`, component refs), `prometheus.scrape` → `remote_write`, `loki.source.file` + `loki.process` → `loki.write`, `otelcol.receiver.otlp` → `otelcol.exporter.otlp`, `pyroscope.scrape`, K8s / Docker / EC2 discovery, relabeling, modules (`import.file/git/http`), clustering, Fleet Management `remotecfg`, the Alloy UI at `:12345`, and `alloy fmt` / `alloy validate`. Use when writing a `config.alloy`, replacing Grafana Agent / OTel Collector, scraping K8s pods, parsing logs, ingesting OTLP, or debugging "Alloy isn't sending anything" — even when the user says "set up the agent", "write me a scrape config", "drop these logs before sending", or "OTel collector config" without naming Alloy.

**Source:** [skills/alloy/SKILL.md](../../../skills/alloy/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [adaptive-metrics](../../notes/cloud-devops/adaptive-metrics.md) — Cut Grafana Cloud Metrics cost by shrinking active-series count with Adaptive Metrics aggregation rules — auto-recommendations from query history, custom exact/regex rules, label-drop...
- [app-observability](../../notes/cloud-devops/app-observability.md) — Get RED metrics + service maps + frontend RUM + AI/LLM monitoring out of Grafana Cloud — Application Observability (`traces_spanmetrics_*` from OTel traces, p50/p95/p99 latency...
- [beyla](../../notes/cloud-devops/beyla.md) — Auto-instrument an application's HTTP / gRPC / DB traffic with Grafana Beyla eBPF — no code changes, no SDK, no restart
- [cost-management](../../notes/cloud-devops/cost-management.md) — Cut your Grafana Cloud bill by attributing spend to teams and reducing telemetry volume
- [database-observability](../../notes/cloud-devops/database-observability.md) — Set up Grafana Cloud Database Observability for MySQL and PostgreSQL — enables `pg_stat_statements` / Performance Schema, creates a least-privilege monitoring user, configures the...
- [docker](../../notes/software-dev/docker.md) — Containerizing and shipping applications with Docker — writing efficient Dockerfiles (multi-stage builds, layer caching, small/secure images), docker compose for multi-service local...
- [fleet-management](../../notes/cloud-devops/fleet-management.md) — Manage a fleet of Grafana Alloy collectors with Fleet Management — author Alloy pipelines once, target them via attribute matchers (`env="production"`, regex `region=~"us-.*"`), push...
- [loki](../../notes/cloud-devops/loki.md) — Grafana Loki log aggregation and LogQL query language
- [opentelemetry](../../notes/cloud-devops/opentelemetry.md) — Instrument any app with OpenTelemetry and ship metrics / logs / traces to Grafana Cloud or self-hosted Mimir / Loki / Tempo / Pyroscope
- [private-connectivity](../../notes/cloud-devops/private-connectivity.md) — Set up private network connectivity to Grafana Cloud — AWS PrivateLink, Azure Private Link, GCP Private Service Connect, and Private Data Source Connect (PDC)
- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [pyroscope](../../notes/cloud-devops/pyroscope.md) — Continuously profile applications with Grafana Pyroscope and read the result as flame graphs
- [telemetry](../../notes/hosting-edge-platforms/telemetry.md) — Add and verify lightweight macOS runtime telemetry
- [tempo](../../notes/cloud-devops/tempo.md) — Stand up Grafana Tempo as a cost-efficient distributed-tracing backend that only needs object storage, and write TraceQL queries against it

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
