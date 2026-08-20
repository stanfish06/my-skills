---
title: codeql
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/codeql/SKILL.md
created: 2026-06-09
---

# codeql

> [!info] What it does
> Scans a codebase for security vulnerabilities using CodeQL's interprocedural data flow and taint tracking analysis. Triggers on "run codeql", "codeql scan", "build codeql database", "SAST scan", "taint analysis", "dataflow analysis", or "find vulnerabilities in this repo". Covers Python, JavaScript/TypeScript, Go, Java/Kotlin, C/C++, C#, Ruby, and Swift. Supports "run all" (security-and-quality + security-experimental) and "important only" (high-precision) scan modes, and creates data extension models for project-specific sources and sinks. For fast single-file pattern matching, or when no build is available for a compiled language, use the semgrep skill; to parse SARIF that already exists rather than produce it, use the sarif-parsing skill.

**Source:** [skills/codeql/SKILL.md](../../../skills/codeql/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [code-audit](../../notes/security-auditing/code-audit.md) — Use for authorized source-code security review and SAST workflows including Semgrep, CodeQL patterns, dangerous API hunting, and fix verification
- [llm-agent-security-redteam](../../notes/security-auditing/llm-agent-security-redteam.md) — LLM and agent security red teaming with agentic-actions-auditor, supply-chain-risk-auditor, semgrep, codeql, and sarif-parsing
- [sarif-parsing](../../notes/security-auditing/sarif-parsing.md) — Parses and processes SARIF files from static analysis tools like CodeQL, Semgrep, or other scanners
- [semgrep](../../notes/security-auditing/semgrep.md) — Runs a Semgrep security scan over a codebase: detects languages, selects rulesets, presents the plan for explicit approval, then runs every approved ruleset through...
- [variant-analysis](../../notes/security-auditing/variant-analysis.md) — Hunts for the other instances of a bug already found — the variants of one root cause across a codebase

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
