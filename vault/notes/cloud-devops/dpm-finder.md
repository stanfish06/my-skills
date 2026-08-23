---
title: dpm-finder
aliases:
  - dpm finder
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/dpm-finder/SKILL.md
created: 2026-08-23
---

# dpm-finder

> [!info] What it does
> Find the Prometheus metrics that drive your Grafana Cloud bill. `dpm-finder` is a Grafana Professional Services CLI that ranks metrics by Data Points per Minute (DPM) with per-label-set breakdown, optional `--cost-per-1000-series` pricing, and a Prometheus-exporter mode. Use when investigating high Grafana Cloud spend, hunting noisy / high-cardinality metrics, comparing pre/post recording-rule cardinality, or feeding cost data into dashboards — even when the user says "why is my Mimir bill so high?", "find the biggest metrics", "cardinality offenders", or "optimize Prometheus cost" without naming dpm-finder.

**Source:** [skills/dpm-finder/SKILL.md](../../../skills/dpm-finder/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [mimir](../../notes/cloud-devops/mimir.md) — Stand up Grafana Mimir for horizontally scalable, multi-tenant, long-term Prometheus + OTLP metrics storage
- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [prometheus-cardinality-troubleshooter](../../notes/cloud-devops/prometheus-cardinality-troubleshooter.md) — Diagnostic guide for active Prometheus cardinality problems — slow queries, OOMing Prometheus, high Grafana Cloud Active Series or DPM bills, "too many samples" ingest errors, series...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
