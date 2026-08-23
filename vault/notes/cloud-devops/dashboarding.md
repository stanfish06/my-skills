---
title: dashboarding
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/dashboarding/SKILL.md
created: 2026-08-23
---

# dashboarding

> [!info] What it does
> Build, modify, and ship Grafana dashboards as JSON via the HTTP API — panel types (timeseries / stat / gauge / table / heatmap / logs / traces / node-graph), `gridPos` 24-column layout, units, thresholds, template + datasource + chained variables, transformations (`organize` / `calculateField` / `filterByValue`), panel + dashboard links with `${__field.labels.x}` / `${__from}`, and Loki/Prometheus annotations. Use when scripting dashboard creation, writing the dashboard JSON for a new service, adding a `$job` dropdown variable, computing an "Error %" column with a transformation, overlaying deploys as annotations, or pushing a dashboard via `POST /api/dashboards/db` — even when the user says "create a dashboard for this metric", "add a service dropdown", "show errors as percentage", "overlay our deploys", or "export the dashboard JSON" without naming the API or schema. After every API push, verify with the returned `version` plus a GET on the dashboard UID.

**Source:** [skills/dashboarding/SKILL.md](../../../skills/dashboarding/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [loki](../../notes/cloud-devops/loki.md) — Grafana Loki log aggregation and LogQL query language
- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [template](../../notes/vault-meta/template.md) — Canonical rules and HTML/CSS contract for the page chrome (head boilerplate, cover, table of contents, section block, sources-section wrapper, footer, outlook-badge, design tokens)...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
