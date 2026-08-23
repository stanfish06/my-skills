---
title: synthetic-monitoring-checks
aliases:
  - synthetic monitoring checks
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/synthetic-monitoring-checks/SKILL.md
created: 2026-08-23
---

# synthetic-monitoring-checks

> [!info] What it does
> Author Grafana Cloud Synthetic Monitoring checks, with deep coverage of k6 scripted and browser checks: SM's single-VU/single-iteration execution model, assertions that actually fail probe_success (expect() and fail() vs bare check()), secrets, deterministic scripts, robust browser locators, local validation with k6 run, deployment via UI/API/Terraform, verifying probe_success, and rollback. Also helps choose the simplest sufficient check type (HTTP/ping/DNS/TCP, MultiHTTP, scripted, browser). Use when writing a synthetic check, monitoring a login/checkout/signup flow in production, converting a k6 script or an OpenAPI spec into a check, authoring a browser check, validating a user journey, or asking "is my site up from multiple regions". NOT for load, stress, or performance testing — SM runs one iteration per execution; for load tests use the grafana-k6 plugin or Grafana Cloud k6. For the broad Grafana Cloud Testing overview (SM + k6 Cloud + Faro), use the testing skill.

**Source:** [skills/synthetic-monitoring-checks/SKILL.md](../../../skills/synthetic-monitoring-checks/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [k6](../../notes/cloud-devops/k6.md) — Generate, validate, and review k6 test scripts — load, stress, spike, soak, smoke, breakpoint, functional, and protocol
- [terraform](../../notes/cloud-devops/terraform.md) — Terraform and OpenTofu infrastructure-as-code (IaC) — declare cloud/SaaS resources in HCL, manage state with remote backends and locking, author and consume modules, and run the...
- [validation](../../notes/software-dev/validation.md) — Use when Codex is already in the validation phase of a security scan or the user explicitly asks to determine whether one or more candidate security findings are valid

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
