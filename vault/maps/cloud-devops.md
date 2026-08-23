---
title: Cloud, Infra & MLOps
tags:
  - skill-map
created: 2026-06-13
---

# Cloud, Infra & MLOps

> [!abstract] Scope
> Cloud architecture and operations, resilience testing, containers, developer infrastructure, MLOps, and workflow pipelines.

[Back to Skill Index](../index.md)

**Related maps:** [Machine Learning & AI](ml-ai.md) | [Bio Databases, Lab & Cloud Platforms](bio-databases-platforms.md) | [Vault, Skills & Workflow Meta](vault-meta.md) | [Analytics Engineering & LLM Operations](analytics-engineering.md) | [Security & Auditing](security-auditing.md) | [Software Development & Engineering](software-dev.md) | [.NET & C# Development](dotnet-development.md)

## Skills (69)

- [adaptive-metrics](../notes/cloud-devops/adaptive-metrics.md) — Cut Grafana Cloud Metrics cost by shrinking active-series count with Adaptive Metrics aggregation rules — auto-recommendations from query history, custom exact/regex rules, label-drop...
- [airflow](../notes/cloud-devops/airflow.md) — Queries, manages, and troubleshoots Apache Airflow using the `af` CLI
- [alerting-irm](../notes/cloud-devops/alerting-irm.md) — Configure Grafana Alerting, Incident Response Management (IRM), and SLOs end-to-end — provisions Grafana-managed and data-source-managed alert rules, contact points...
- [alloy](../notes/cloud-devops/alloy.md) — Build a unified telemetry pipeline with Grafana Alloy — one OpenTelemetry-compatible binary that collects metrics, logs, traces, and profiles and ships to Grafana Cloud / Prometheus /...
- [app-observability](../notes/cloud-devops/app-observability.md) — Get RED metrics + service maps + frontend RUM + AI/LLM monitoring out of Grafana Cloud — Application Observability (`traces_spanmetrics_*` from OTel traces, p50/p95/p99 latency...
- [assistant-mcp](../notes/cloud-devops/assistant-mcp.md) — Connect AI coding agents (Claude Code, Cursor, VS Code, OpenAI Codex) to Grafana Cloud via the `mcp-grafana` Model Context Protocol server
- [aws-agentic-ai](../notes/cloud-devops/aws-agentic-ai.md) — AWS Bedrock AgentCore comprehensive expert for deploying and managing AI agents at scale
- [aws-cdk-development](../notes/cloud-devops/aws-cdk-development.md) — AWS Cloud Development Kit (CDK) expert for building cloud infrastructure with TypeScript/Python
- [aws-cost-operations](../notes/cloud-devops/aws-cost-operations.md) — AWS cost optimization, monitoring, and operational excellence expert
- [aws-mcp-setup](../notes/cloud-devops/aws-mcp-setup.md) — Configure AWS MCP servers for documentation search and API access
- [aws-serverless-eda](../notes/cloud-devops/aws-serverless-eda.md) — AWS serverless and event-driven architecture expert based on Well-Architected Framework
- [beyla](../notes/cloud-devops/beyla.md) — Auto-instrument an application's HTTP / gRPC / DB traffic with Grafana Beyla eBPF — no code changes, no SDK, no restart
- [chaos-engineering](../notes/cloud-devops/chaos-engineering.md) — Design and run bounded chaos engineering experiments that test whether a system preserves measurable steady-state behavior during realistic faults
- [ci-cd-and-automation](../notes/cloud-devops/ci-cd-and-automation.md) — Automates CI/CD pipeline setup. Use when setting up or modifying build and deployment pipelines
- [cloud-integrations](../notes/cloud-devops/cloud-integrations.md) — Set up, configure, and troubleshoot Grafana Cloud integrations for AWS, Azure, and other cloud providers
- [cloudformation-to-pulumi](../notes/cloud-devops/cloudformation-to-pulumi.md) — Convert, migrate, or import AWS CloudFormation stacks or templates into Pulumi programs
- [conda-bioconda](../notes/cloud-devops/conda-bioconda.md) — Reproducible Conda/Mamba/micromamba environment management for bioinformatics, with correct Bioconda channel setup, environment files, version pinning, and lockfiles
- [cost-management](../notes/cloud-devops/cost-management.md) — Cut your Grafana Cloud bill by attributing spend to teams and reducing telemetry volume
- [dashboarding](../notes/cloud-devops/dashboarding.md) — Build, modify, and ship Grafana dashboards as JSON via the HTTP API — panel types (timeseries / stat / gauge / table / heatmap / logs / traces / node-graph), `gridPos` 24-column...
- [database-observability](../notes/cloud-devops/database-observability.md) — Set up Grafana Cloud Database Observability for MySQL and PostgreSQL — enables `pg_stat_statements` / Performance Schema, creates a least-privilege monitoring user, configures the...
- [datasources-provisioning](../notes/cloud-devops/datasources-provisioning.md) — Generate a copy-paste Grafana data source provisioning file (YAML or Terraform) for any plugin from its standardized settings schema on the plugins CDN
- [devcontainer-setup](../notes/cloud-devops/devcontainer-setup.md) — Creates devcontainers with Claude Code, language-specific tooling (Python/Node/Rust/Go), and persistent volumes
- [docker-expert](../notes/cloud-devops/docker-expert.md) — You are an advanced Docker containerization expert with comprehensive, practical knowledge of container optimization, security hardening, multi-stage builds, orchestration patterns...
- [dpm-finder](../notes/cloud-devops/dpm-finder.md) — Find the Prometheus metrics that drive your Grafana Cloud bill
- [dvc](../notes/cloud-devops/dvc.md) — Data Version Control (DVC) for tracking large datasets/models with Git-like semantics, defining reproducible data/ML pipelines (dvc.yaml stages that only re-run when their inputs...
- [e2b-sandbox](../notes/cloud-devops/e2b-sandbox.md) — Guide for creating and managing E2B sandboxes using ComputeSDK
- [fleet-management](../notes/cloud-devops/fleet-management.md) — Manage a fleet of Grafana Alloy collectors with Fleet Management — author Alloy pipelines once, target them via attribute matchers (`env="production"`, regex `region=~"us-.*"`), push...
- [grafana-oss](../notes/cloud-devops/grafana-oss.md) — Configure Grafana OSS — provisions dashboards from YAML, sets up data sources (Prometheus / Loki / Tempo / Pyroscope), writes dashboard JSON with template variables, builds panel...
- [hf-cli](../notes/cloud-devops/hf-cli.md) — Hugging Face Hub CLI (`hf`) for downloading, uploading, and managing repositories, models, datasets, and Spaces on the Hugging Face Hub
- [incident-response](../notes/cloud-devops/incident-response.md) — Run an incident response workflow — triage, communicate, and write postmortem
- [k6](../notes/cloud-devops/k6.md) — Generate, validate, and review k6 test scripts — load, stress, spike, soak, smoke, breakpoint, functional, and protocol
- [k6-cloud-investigate-test](../notes/cloud-devops/k6-cloud-investigate-test.md) — Investigate a Grafana Cloud k6 test — describe the script, list run history, identify pass/fail status, pull raw metric time-series and log lines for one or more runs, and (if asked)...
- [k6-docs](../notes/cloud-devops/k6-docs.md) — Write or review k6 documentation across the three k6 repositories - k6-DefinitelyTyped (TypeScript types), k6-docs (user documentation), and k6 (release notes / changelog)
- [k6-manage](../notes/cloud-devops/k6-manage.md) — Interact with Grafana Cloud k6 (GCk6) — manage load tests, test runs, scripts, projects, schedules, env vars, fetch metrics or logs, and run scripts locally — using the `gcx` CLI (or...
- [k6-perf-test-website](../notes/cloud-devops/k6-perf-test-website.md) — Use when the user wants to performance-test, load-test, or stress-test a public website end-to-end with k6
- [k6-test-maintenance](../notes/cloud-devops/k6-test-maintenance.md) — Maintain and improve existing k6 test scripts
- [k6-trend-analysis](../notes/cloud-devops/k6-trend-analysis.md) — Analyze Grafana Cloud k6 test run trends over time
- [kubernetes-specialist](../notes/cloud-devops/kubernetes-specialist.md) — Use when deploying or managing Kubernetes workloads
- [loki](../notes/cloud-devops/loki.md) — Grafana Loki log aggregation and LogQL query language
- [loki-label-analyzer](../notes/cloud-devops/loki-label-analyzer.md) — Expert evaluator for Grafana Loki label strategy
- [mimir](../notes/cloud-devops/mimir.md) — Stand up Grafana Mimir for horizontally scalable, multi-tenant, long-term Prometheus + OTLP metrics storage
- [mlflow-onboarding](../notes/cloud-devops/mlflow-onboarding.md) — Onboards users to MLflow by determining their use case (GenAI agents/apps or traditional ML/deep learning) and guiding them through relevant quickstart tutorials and initial integration
- [modal](../notes/cloud-devops/modal.md) — Modal is a serverless cloud platform for running Python on demand, including on-demand GPUs
- [modern-python](../notes/cloud-devops/modern-python.md) — Configures Python projects with modern tooling (uv, ruff, ty)
- [nextflow](../notes/cloud-devops/nextflow.md) — Build, run, and debug Nextflow data pipelines and nf-core workflows end to end
- [oncall-irm](../notes/cloud-devops/oncall-irm.md) — Route alerts, run on-call rotations, and drive incidents in Grafana IRM / OnCall — integrations (Alertmanager / Grafana Alerting / generic webhook / PagerDuty), Jinja2 routing +...
- [opentelemetry](../notes/cloud-devops/opentelemetry.md) — Instrument any app with OpenTelemetry and ship metrics / logs / traces to Grafana Cloud or self-hosted Mimir / Loki / Tempo / Pyroscope
- [private-connectivity](../notes/cloud-devops/private-connectivity.md) — Set up private network connectivity to Grafana Cloud — AWS PrivateLink, Azure Private Link, GCP Private Service Connect, and Private Data Source Connect (PDC)
- [profilecli-insights](../notes/cloud-devops/profilecli-insights.md) — Query live Pyroscope profiles with profilecli, analyze them with pprof, and correlate hot functions with checked-out source code
- [prometheus](../notes/cloud-devops/prometheus.md) — Prometheus and Grafana Cloud Metrics overview including PromQL query language, Metrics Drilldown, alerting, recording rules, and integration patterns
- [prometheus-cardinality-troubleshooter](../notes/cloud-devops/prometheus-cardinality-troubleshooter.md) — Diagnostic guide for active Prometheus cardinality problems — slow queries, OOMing Prometheus, high Grafana Cloud Active Series or DPM bills, "too many samples" ingest errors, series...
- [prometheus-label-strategy](../notes/cloud-devops/prometheus-label-strategy.md) — Expert evaluator for Prometheus label strategy on Grafana Cloud
- [promql](../notes/cloud-devops/promql.md) — Write, validate, and optimize PromQL for Prometheus / Grafana Mimir / Grafana Cloud Metrics
- [pulumi-arm-to-pulumi](../notes/cloud-devops/pulumi-arm-to-pulumi.md) — Convert or migrate Azure ARM (Azure Resource Manager) templates, Bicep templates, or code to Pulumi, including importing existing Azure resources
- [pulumi-cdk-to-pulumi](../notes/cloud-devops/pulumi-cdk-to-pulumi.md) — Load this skill when a user wants to migrate, convert, port, translate, or move an AWS CDK application (including CDK stacks, constructs, or CloudFormation-synthesized templates) to...
- [pulumi-migrate-from-discovered-stack](../notes/cloud-devops/pulumi-migrate-from-discovered-stack.md) — Migrate a CloudFormation or ARM stack into a Pulumi stack, sourced from a stack that Pulumi Cloud's Discovery feature has already found and exposed via the discovered-stacks API
- [pulumi-neo-handoff](../notes/cloud-devops/pulumi-neo-handoff.md) — Hand off the current thread to a new Pulumi Neo task as a one-way transfer
- [pulumi-terraform-to-pulumi](../notes/cloud-devops/pulumi-terraform-to-pulumi.md) — Migrate Terraform/OpenTofu projects to Pulumi, including translating HCL source code and/or importing Terraform state into a Pulumi stack
- [pulumi-upgrade-provider](../notes/cloud-devops/pulumi-upgrade-provider.md) — Automate Pulumi provider repo upgrades with the `upgrade-provider` tool
- [pyroscope](../notes/cloud-devops/pyroscope.md) — Continuously profile applications with Grafana Pyroscope and read the result as flame graphs
- [ray](../notes/cloud-devops/ray.md) — Distributed Python compute with Ray — @ray.remote tasks/actors for cluster-scale parallelism, Ray Data for large-batch preprocessing, Ray Train for distributed model training...
- [shipping-and-launch](../notes/cloud-devops/shipping-and-launch.md) — Prepares production launches. Use when preparing to deploy to production
- [snakemake-workflow-engine](../notes/cloud-devops/snakemake-workflow-engine.md) — Python-based workflow manager for reproducible, scalable pipelines
- [synthetic-monitoring-checks](../notes/cloud-devops/synthetic-monitoring-checks.md) — Author Grafana Cloud Synthetic Monitoring checks, with deep coverage of k6 scripted and browser checks: SM's single-VU/single-iteration execution model, assertions that actually fail...
- [tempo](../notes/cloud-devops/tempo.md) — Stand up Grafana Tempo as a cost-efficient distributed-tracing backend that only needs object storage, and write TraceQL queries against it
- [terraform](../notes/cloud-devops/terraform.md) — Terraform and OpenTofu infrastructure-as-code (IaC) — declare cloud/SaaS resources in HCL, manage state with remote backends and locking, author and consume modules, and run the...
- [vllm-deploy-simple](../notes/cloud-devops/vllm-deploy-simple.md) — Quick install and deploy vLLM, start serving with a simple LLM, and test OpenAI API
- [wandb-primary](../notes/cloud-devops/wandb-primary.md) — Primary W&B skill for broad or mixed Weights & Biases work: project overviews, W&B runs and artifacts, Weave traces and evaluations, Reports, and Launch workflows
- [wizard](../notes/cloud-devops/wizard.md) — Generate an interactive bash wizard that walks a human through steps only they can perform
