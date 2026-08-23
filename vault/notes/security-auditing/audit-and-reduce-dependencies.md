---
title: audit-and-reduce-dependencies
aliases:
  - audit and reduce dependencies
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/audit-and-reduce-dependencies/SKILL.md
created: 2026-08-23
---

# audit-and-reduce-dependencies

> [!info] What it does
> Reduces JavaScript dependency footprint with pnpm while preserving lockfile, workspace layout, and dependency range style. Runs /check-npm first, then removes unused deps, dedupes versions, ranks transitive closure, and reports Keep/Replace/Remove triage. Use when cleaning up pnpm dependencies, reducing lockfile size, or shrinking node_modules in Grafana plugins; not for Go modules or full GitHub Actions workflow audits.

**Source:** [skills/audit-and-reduce-dependencies/SKILL.md](../../../skills/audit-and-reduce-dependencies/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [check-npm](../../notes/security-auditing/check-npm.md) — Audit a JavaScript/TypeScript repo's npm, yarn, or pnpm configuration for supply-chain hardening: tool version, lifecycle scripts, unsafe dependency protocols, and minimum release age...
- [github](../../notes/software-dev/github.md) — Triage and orient GitHub repository, pull request, and issue work through the connected GitHub app
- [triage](../../notes/software-dev/triage.md) — Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs
- [workflow](../../notes/software-dev/workflow.md) — Vercel Workflow DevKit (WDK) expert guidance

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
