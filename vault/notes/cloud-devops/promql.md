---
title: promql
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/promql/SKILL.md
created: 2026-08-23
---

# promql

> [!info] What it does
> Write, validate, and optimize PromQL for Prometheus / Grafana Mimir / Grafana Cloud Metrics. Covers `rate` vs `irate` vs `increase`, label matchers and regex, `sum / avg / topk / by / without` aggregation, classic + native `histogram_quantile`, ratios with divide-by-zero guards, `absent` / `changes` for staleness, time offsets and `predict_linear`, recording-rule naming, SLO + burn-rate math, and a cardinality-hunting playbook. Use when writing a metric query, fixing wrong p95s, building an error-budget alert, debugging "query is slow", finding the noisy label that blew up cardinality, or migrating a dashboard query to a recording rule — even when the user says "calculate the error rate", "p99 latency", "sum by service", "why is this query slow", or "what's filling Mimir" without naming PromQL.

**Source:** [skills/promql/SKILL.md](../../../skills/promql/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [mimir](../../notes/cloud-devops/mimir.md) — Stand up Grafana Mimir for horizontally scalable, multi-tenant, long-term Prometheus + OTLP metrics storage
- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
