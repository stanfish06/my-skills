---
title: fleet-management
aliases:
  - fleet management
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/fleet-management/SKILL.md
created: 2026-08-23
---

# fleet-management

> [!info] What it does
> Manage a fleet of Grafana Alloy collectors with Fleet Management — author Alloy pipelines once, target them via attribute matchers (`env="production"`, regex `region=~"us-.*"`), push remotely via OpAMP without restarting collectors. Covers pipeline create / update / matcher RPCs, collector attribute API, `remotecfg` bootstrap block (standalone + Helm), pre-deploy `alloy fmt` validation, the local Alloy UI at port 12345 for component health, and post-deploy `REMOTE_CONFIG_STATUS_APPLIED` verification. Use when standing up a Cloud Alloy fleet, pushing a config change to 200 collectors, hunting why one collector shows `REMOTE_CONFIG_STATUS_FAILED`, validating River syntax before saving, or wiring `discovery.kubernetes` → `prometheus.remote_write` — even when the user says "configure Alloy", "remote config the collectors", "push pipeline", "OpAMP", "collector is unhealthy", or "manage agent config centrally" without naming Fleet Management.

**Source:** [skills/fleet-management/SKILL.md](../../../skills/fleet-management/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [alloy](../../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [bootstrap](../../notes/web-automation-frontend/bootstrap.md) — Project bootstrapping orchestrator for repos that depend on Vercel-linked resources (databases, auth, and managed integrations)
- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [validation](../../notes/software-dev/validation.md) — Use when Codex is already in the validation phase of a security scan or the user explicitly asks to determine whether one or more candidate security findings are valid
- [verification](../../notes/software-dev/verification.md) — Full-story verification — infers what the user is building, then verifies the complete flow end-to-end: browser → API → data → response

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
