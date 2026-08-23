---
title: app-observability
aliases:
  - app observability
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/app-observability/SKILL.md
created: 2026-08-23
---

# app-observability

> [!info] What it does
> Get RED metrics + service maps + frontend RUM + AI/LLM monitoring out of Grafana Cloud — Application Observability (`traces_spanmetrics_*` from OTel traces, p50/p95/p99 latency, exemplar-to-trace, traces-to-logs / profiles), Frontend Observability with the Faro Web SDK (Core Web Vitals, session replay, `pushError`, React + router integration, `TracingInstrumentation` for browser → backend trace correlation), and AI Observability via OpenLIT (token / cost / latency, GPU, hallucination + toxicity evals). Use when standing up APM for a service, wiring an Alloy OTLP receiver + forwarding to Cloud, instrumenting a React frontend for RUM, debugging why service-map edges are missing, monitoring LLM cost drift, or correlating a frontend error to its backend trace — even when the user says "set up APM", "show service map", "monitor browser perf", "session replay", "RUM SDK", or "watch our OpenAI bill" without naming App / Frontend / AI Observability.

**Source:** [skills/app-observability/SKILL.md](../../../skills/app-observability/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [alloy](../../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [observability](../../notes/hosting-edge-platforms/observability.md) — Vercel Observability expert guidance — Drains (logs, traces, speed insights, web analytics), Web Analytics, Speed Insights, runtime logs, custom events, OpenTelemetry integration, and...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
