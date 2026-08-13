---
title: variant-analysis
aliases:
  - variant analysis
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/variant-analysis/SKILL.md
created: 2026-06-09
---

# variant-analysis

> [!info] What it does
> Hunts for the other instances of a bug already found — the variants of one root cause across a codebase. Use immediately after a vulnerability, logic bug, or bad pattern turns up in a specific file and the question becomes where else it occurs, including the bare conversational form ("are there others like this?", "is this the same bug?"). Also for generalizing one known instance into a CodeQL or Semgrep query for its whole pattern family, and for triaging a set of look-alike candidates against a known root cause. Not for initial discovery with no bug in hand.

**Source:** [skills/variant-analysis/SKILL.md](../../../skills/variant-analysis/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [codeql](../../notes/security-auditing/codeql.md) — Scans a codebase for security vulnerabilities using CodeQL's interprocedural data flow and taint tracking analysis
- [semgrep](../../notes/security-auditing/semgrep.md) — Runs a Semgrep security scan over a codebase: detects languages, selects rulesets, presents the plan for explicit approval, then runs every approved ruleset through...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
