---
title: opentelemetry
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/opentelemetry/SKILL.md
created: 2026-08-23
---

# opentelemetry

> [!info] What it does
> Instrument any app with OpenTelemetry and ship metrics / logs / traces to Grafana Cloud or self-hosted Mimir / Loki / Tempo / Pyroscope. Covers SDK auto-instrumentation for Go, Java (Grafana JVM agent), Python (`opentelemetry-instrument`), Node.js, .NET (`Grafana.OpenTelemetry`), Beyla eBPF for zero-code; Grafana Cloud OTLP gateway + Basic-auth (instanceID + API key, base64); env-var config (`OTEL_EXPORTER_OTLP_*`, `OTEL_RESOURCE_ATTRIBUTES`); Alloy / OTel-Collector pipelines; Kubernetes Operator inject-annotations; and head + tail sampling. Use when instrumenting a service, pointing OTLP at Grafana Cloud, switching from Jaeger / Datadog / New Relic, choosing head- vs tail-sampling, or debugging "spans aren't showing in Explore" — even when the user says "auto-instrument my Java app", "send traces to Grafana", "what env vars do I set", "OTLP endpoint", or "Operator inject" without naming OpenTelemetry.

**Source:** [skills/opentelemetry/SKILL.md](../../../skills/opentelemetry/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [alloy](../../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [beyla](../../notes/cloud-devops/beyla.md) — Auto-instrument an application's HTTP / gRPC / DB traffic with Grafana Beyla eBPF — no code changes, no SDK, no restart
- [clickstack-otel-collector](../../notes/analytics-engineering/clickstack-otel-collector.md) — Use when a user wants to wire an OpenTelemetry collector into a Managed ClickStack service on ClickHouse Cloud, either by deploying a new local collector (Docker run or Docker Compose)...
- [configuring-opentelemetry-dotnet](../../notes/dotnet-development/configuring-opentelemetry-dotnet.md) — Configure OpenTelemetry distributed tracing, metrics, and logging in ASP.NET Core using the .NET OpenTelemetry SDK
- [llm-observability-evals](../../notes/analytics-engineering/llm-observability-evals.md) — LLM and agent observability, tracing, and evaluation workflows with langfuse, phoenix-cli, and phoenix-evals
- [logfire-instrumentation](../../notes/analytics-engineering/logfire-instrumentation.md) — Add Pydantic Logfire observability to applications and send as much useful telemetry as possible
- [loki](../../notes/cloud-devops/loki.md) — Grafana Loki log aggregation and LogQL query language
- [matlab-instrument-opentelemetry-tracing](../../notes/matlab-development/matlab-instrument-opentelemetry-tracing.md) — Add OpenTelemetry tracing to MATLAB code
- [mimir](../../notes/cloud-devops/mimir.md) — Stand up Grafana Mimir for horizontally scalable, multi-tenant, long-term Prometheus + OTLP metrics storage
- [observability](../../notes/hosting-edge-platforms/observability.md) — Vercel Observability expert guidance — Drains (logs, traces, speed insights, web analytics), Web Analytics, Speed Insights, runtime logs, custom events, OpenTelemetry integration, and...
- [pyroscope](../../notes/cloud-devops/pyroscope.md) — Continuously profile applications with Grafana Pyroscope and read the result as flame graphs
- [tempo](../../notes/cloud-devops/tempo.md) — Stand up Grafana Tempo as a cost-efficient distributed-tracing backend that only needs object storage, and write TraceQL queries against it

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
