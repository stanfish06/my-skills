---
title: pyroscope
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/pyroscope/SKILL.md
created: 2026-08-23
---

# pyroscope

> [!info] What it does
> Continuously profile applications with Grafana Pyroscope and read the result as flame graphs. Covers three instrumentation paths — language SDK push (Go / Java / Python / Ruby / Node / .NET / Rust), Alloy eBPF auto-instrumentation (no code change, requires kernel 5.8+ with BTF), and SDK → Alloy receiver — plus ProfileQL queries, profile types (CPU / memory / allocations / goroutines / mutex), Grafana Cloud Profiles endpoint, and Span Profiles trace-to-profile linking. Use when adding profiling to a service, deploying Alloy as a cluster-wide eBPF profiler, hunting CPU / memory hotspots from a flame graph, comparing two profiles to find a regression, or correlating a slow Tempo trace to its profile — even when the user says "find what's burning CPU", "flame graph this app", "continuous profiling", "heap hotspots", or "why is allocation so high" without naming Pyroscope.

**Source:** [skills/pyroscope/SKILL.md](../../../skills/pyroscope/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [alloy](../../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [grafana-oss](../../notes/cloud-devops/grafana-oss.md) — Configure Grafana OSS — provisions dashboards from YAML, sets up data sources (Prometheus / Loki / Tempo / Pyroscope), writes dashboard JSON with template variables, builds panel...
- [opentelemetry](../../notes/cloud-devops/opentelemetry.md) — Instrument any app with OpenTelemetry and ship metrics / logs / traces to Grafana Cloud or self-hosted Mimir / Loki / Tempo / Pyroscope
- [profilecli-insights](../../notes/cloud-devops/profilecli-insights.md) — Query live Pyroscope profiles with profilecli, analyze them with pprof, and correlate hot functions with checked-out source code
- [tempo](../../notes/cloud-devops/tempo.md) — Stand up Grafana Tempo as a cost-efficient distributed-tracing backend that only needs object storage, and write TraceQL queries against it

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
