---
title: adaptive-metrics
aliases:
  - adaptive metrics
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/adaptive-metrics/SKILL.md
created: 2026-08-23
---

# adaptive-metrics

> [!info] What it does
> Cut Grafana Cloud Metrics cost by shrinking active-series count with Adaptive Metrics aggregation rules — auto-recommendations from query history, custom exact/regex rules, label-drop config, unused-metric detection, and Alloy remote_write fallback. Use when investigating a high Mimir/Grafana Cloud bill, hunting high-cardinality labels (`pod_uid`, `service_instance_id`, `version`), pre-aggregating counters/gauges, dropping unused metrics, or measuring `grafanacloud_instance_active_series` before/after — even when the user says "reduce cardinality", "too many series", "metrics spend", "active series count is exploding", or "drop the version label" without naming Adaptive Metrics.

**Source:** [skills/adaptive-metrics/SKILL.md](../../../skills/adaptive-metrics/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [alloy](../../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [mimir](../../notes/cloud-devops/mimir.md) — Stand up Grafana Mimir for horizontally scalable, multi-tenant, long-term Prometheus + OTLP metrics storage
- [prometheus-cardinality-troubleshooter](../../notes/cloud-devops/prometheus-cardinality-troubleshooter.md) — Diagnostic guide for active Prometheus cardinality problems — slow queries, OOMing Prometheus, high Grafana Cloud Active Series or DPM bills, "too many samples" ingest errors, series...
- [prometheus-label-strategy](../../notes/cloud-devops/prometheus-label-strategy.md) — Expert evaluator for Prometheus label strategy on Grafana Cloud

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
