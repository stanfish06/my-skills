---
title: private-connectivity
aliases:
  - private connectivity
  - PDC
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/private-connectivity/SKILL.md
created: 2026-08-23
---

# private-connectivity

> [!info] What it does
> Set up private network connectivity to Grafana Cloud — AWS PrivateLink, Azure Private Link, GCP Private Service Connect, and Private Data Source Connect (PDC). Provisions VPC endpoints, private endpoints, or PSC forwarding rules per signal type (metrics / logs / traces / profiles); wires Alloy to push to the private DNS endpoint instead of the public one; verifies private DNS resolution + endpoint approval state. Use when sending telemetry to Grafana Cloud without traversing the public internet, eliminating cloud egress costs, meeting PCI-DSS / HIPAA / data-residency compliance, configuring PDC for private data-source queries, or connecting AWS / Azure / GCP workloads to Grafana — even when the user says "stop paying egress", "keep our telemetry off the public internet", or "PCI compliance for Grafana" without naming PrivateLink.

**Source:** [skills/private-connectivity/SKILL.md](../../../skills/private-connectivity/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [alloy](../../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [telemetry](../../notes/hosting-edge-platforms/telemetry.md) — Add and verify lightweight macOS runtime telemetry

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
