---
title: beyla
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/beyla/SKILL.md
created: 2026-08-23
---

# beyla

> [!info] What it does
> Auto-instrument an application's HTTP / gRPC / DB traffic with Grafana Beyla eBPF — no code changes, no SDK, no restart. Covers requirements (Linux 5.8+ with BTF, CAP_SYS_ADMIN, host PID), language matrix (Go / Java / Python / Ruby / Node / .NET / Rust / C++ / PHP), Docker + Helm + DaemonSet install, port- / process- / Kubernetes-metadata discovery, OTLP traces + Prometheus metrics export, routes decorator (cardinality control), trace sampling, and Grafana Cloud via Alloy. Use when adding observability to a service you can't recompile, instrumenting a closed-source binary, getting RED metrics + spans onto Tempo/Mimir without touching the app, or rolling Beyla as a cluster-wide DaemonSet — even when the user says "zero-code APM", "instrument legacy app", "trace this binary", "eBPF observability", or "no SDK" without naming Beyla.

**Source:** [skills/beyla/SKILL.md](../../../skills/beyla/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [alloy](../../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [docker](../../notes/software-dev/docker.md) — Containerizing and shipping applications with Docker — writing efficient Dockerfiles (multi-stage builds, layer caching, small/secure images), docker compose for multi-service local...
- [mimir](../../notes/cloud-devops/mimir.md) — Stand up Grafana Mimir for horizontally scalable, multi-tenant, long-term Prometheus + OTLP metrics storage
- [observability](../../notes/hosting-edge-platforms/observability.md) — Vercel Observability expert guidance — Drains (logs, traces, speed insights, web analytics), Web Analytics, Speed Insights, runtime logs, custom events, OpenTelemetry integration, and...
- [opentelemetry](../../notes/cloud-devops/opentelemetry.md) — Instrument any app with OpenTelemetry and ship metrics / logs / traces to Grafana Cloud or self-hosted Mimir / Loki / Tempo / Pyroscope
- [prometheus](../../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [tempo](../../notes/cloud-devops/tempo.md) — Stand up Grafana Tempo as a cost-efficient distributed-tracing backend that only needs object storage, and write TraceQL queries against it

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
