---
title: prometheus-label-strategy
aliases:
  - prometheus label strategy
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/prometheus-label-strategy/SKILL.md
created: 2026-08-23
---

# prometheus-label-strategy

> [!info] What it does
> Expert evaluator for Prometheus label strategy on Grafana Cloud. Audits, designs, and improves label schemas using cardinality scoring, access-pattern alignment, static vs. dynamic label rules, histogram bucket discipline, and instrumentation hygiene. Prevents high cardinality at the source — in application code and scrape target labels — without dropping labels that make series unique (which breaks the data). For reducing the cost of series already in Grafana Cloud, routes to the adaptive-metrics skill. Use when the user asks to evaluate, audit, design, or improve Prometheus labels — or asks how to prevent high cardinality at the source. For "why is my Prometheus slow / expensive right now" triage, see prometheus-cardinality-troubleshooter.

**Source:** [skills/prometheus-label-strategy/SKILL.md](../../../skills/prometheus-label-strategy/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [adaptive-metrics](../../notes/cloud-devops/adaptive-metrics.md) — Cut Grafana Cloud Metrics cost by shrinking active-series count with Adaptive Metrics aggregation rules — auto-recommendations from query history, custom exact/regex rules, label-drop...
- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [prometheus-cardinality-troubleshooter](../../notes/cloud-devops/prometheus-cardinality-troubleshooter.md) — Diagnostic guide for active Prometheus cardinality problems — slow queries, OOMing Prometheus, high Grafana Cloud Active Series or DPM bills, "too many samples" ingest errors, series...
- [triage](../../notes/software-dev/triage.md) — Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
