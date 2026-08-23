---
title: oncall-irm
aliases:
  - oncall irm
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/oncall-irm/SKILL.md
created: 2026-08-23
---

# oncall-irm

> [!info] What it does
> Route alerts, run on-call rotations, and drive incidents in Grafana IRM / OnCall — integrations (Alertmanager / Grafana Alerting / generic webhook / PagerDuty), Jinja2 routing + grouping templates, escalation chains (wait → notify schedule → notify team → webhook → auto-resolve), schedules (web + iCal + Terraform `grafana_oncall_schedule`), Slack chatops with Acknowledge/Resolve/Silence, and the P1-P4 incident lifecycle. Use when wiring Alertmanager to OnCall, deciding which team gets paged, building rotations from a Google Calendar / iCal, hooking up Slack notifications, or declaring an incident from an alert — even when the user says "page the platform team on critical alerts", "send Prometheus alerts to Slack", "set up our on-call rota", "escalation policy", or "auto-resolve when the alert clears" without naming OnCall / IRM. Heads up — OnCall OSS is in maintenance mode (archived March 2026); Grafana Cloud users should use IRM.

**Source:** [skills/oncall-irm/SKILL.md](../../../skills/oncall-irm/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [slack](../../notes/web-automation-frontend/slack.md) — Read Slack context, route to the right Slack workflow, and prepare or perform Slack writes that match the user's intent
- [terraform](../../notes/cloud-devops/terraform.md) — Terraform and OpenTofu infrastructure-as-code (IaC) — declare cloud/SaaS resources in HCL, manage state with remote backends and locking, author and consume modules, and run the...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
