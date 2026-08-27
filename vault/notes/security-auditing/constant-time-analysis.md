---
title: constant-time-analysis
aliases:
  - constant time analysis
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/constant-time-analysis/SKILL.md
created: 2026-06-09
---

# constant-time-analysis

> [!info] What it does
> Detects timing side-channel vulnerabilities in cryptographic code. Use when implementing or reviewing crypto code, encountering division on secrets, secret-dependent branches, or constant-time programming questions in C, C++, Go, Rust, Swift, Java, Kotlin, C#, PHP, JavaScript, TypeScript, Python, or Ruby.

**Source:** [skills/constant-time-analysis/SKILL.md](../../../skills/constant-time-analysis/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [constant-time-testing](../../notes/security-auditing/constant-time-testing.md) — Measures timing side channels in cryptographic implementations by running them, using dudect for statistical analysis and Timecop over Valgrind for dynamic tracing

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!note] Vault audit 2026-07-24 — USE-9
> Use this for the runnable static-analysis pass that flags timing side-channels in crypto source; for the dynamic-statistical testing methodology / tool survey use `constant-time-testing`. Distinguishing axis: static analyzer vs testing methodology.
