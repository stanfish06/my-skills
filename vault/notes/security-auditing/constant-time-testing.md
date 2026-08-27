---
title: constant-time-testing
aliases:
  - constant time testing
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/constant-time-testing/SKILL.md
created: 2026-06-09
---

# constant-time-testing

> [!info] What it does
> Measures timing side channels in cryptographic implementations by running them, using dudect for statistical analysis and Timecop over Valgrind for dynamic tracing. Covers the formal, symbolic, dynamic, and statistical tool categories and how to read a result. Use when testing whether a running implementation is constant-time, measuring timing variance on a compiled binary, or investigating a suspected timing attack. Not for statically inspecting compiler output — the constant-time-analysis plugin covers that.

**Source:** [skills/constant-time-testing/SKILL.md](../../../skills/constant-time-testing/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [constant-time-analysis](../../notes/security-auditing/constant-time-analysis.md) — Detects timing side-channel vulnerabilities in cryptographic code

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!warning] Vault audit 2026-07-24 — MNT-9 / USE-9
> Workflow defers to `dudect`/`timecop` helper skills that don't exist in this vault, and near-duplicates `constant-time-analysis`. This skill is the dynamic-statistical methodology / tool survey; use `constant-time-analysis` for the runnable static-analysis pass.
> _Remote-managed skill — the durable fix belongs upstream; this wrapper note is the local record._
