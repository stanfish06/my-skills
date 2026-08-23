---
title: prometheus-cardinality-troubleshooter
aliases:
  - prometheus cardinality troubleshooter
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/prometheus-cardinality-troubleshooter/SKILL.md
created: 2026-08-23
---

# prometheus-cardinality-troubleshooter

> [!info] What it does
> Diagnostic guide for active Prometheus cardinality problems — slow queries, OOMing Prometheus, high Grafana Cloud Active Series or DPM bills, "too many samples" ingest errors, series churn, or rapid memory growth. Walks through tsdb status endpoints, per-metric and per-label drill-downs, common-culprit galleries, and remediation paths. Use when the user is *currently experiencing* a cardinality fire. For preventing cardinality issues at the source, route to prometheus-label-strategy. For post-ingest aggregation, route to adaptive-metrics. For DPM-specific analysis, route to dpm-finder.

**Source:** [skills/prometheus-cardinality-troubleshooter/SKILL.md](../../../skills/prometheus-cardinality-troubleshooter/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [adaptive-metrics](../../notes/cloud-devops/adaptive-metrics.md) — Cut Grafana Cloud Metrics cost by shrinking active-series count with Adaptive Metrics aggregation rules — auto-recommendations from query history, custom exact/regex rules, label-drop...
- [dpm-finder](../../notes/cloud-devops/dpm-finder.md) — Find the Prometheus metrics that drive your Grafana Cloud bill
- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [prometheus-label-strategy](../../notes/cloud-devops/prometheus-label-strategy.md) — Expert evaluator for Prometheus label strategy on Grafana Cloud

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
