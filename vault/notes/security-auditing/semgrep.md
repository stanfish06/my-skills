---
title: semgrep
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/semgrep/SKILL.md
created: 2026-06-09
---

# semgrep

> [!info] What it does
> Runs a Semgrep security scan over a codebase: detects languages, selects rulesets, presents the plan for explicit approval, then runs every approved ruleset through scripts/run-scans.sh, which batches the semgrep processes and writes scans.json, and merges the output to SARIF. Supports two scan modes, "run all" for full ruleset coverage and "important only" for security findings at medium-to-high confidence and impact. Uses Semgrep Pro for cross-file taint analysis when it is available. Use when asked to scan code for vulnerabilities, run a security audit with Semgrep, find bugs, or perform static analysis. For the same scan without the approval gate, use the /static-analysis:semgrep-scan workflow.

**Source:** [skills/semgrep/SKILL.md](../../../skills/semgrep/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [code-audit](../../notes/security-auditing/code-audit.md) — Use for authorized source-code security review and SAST workflows including Semgrep, CodeQL patterns, dangerous API hunting, and fix verification
- [codeql](../../notes/security-auditing/codeql.md) — Scans a codebase for security vulnerabilities using CodeQL's interprocedural data flow and taint tracking analysis
- [llm-agent-security-redteam](../../notes/security-auditing/llm-agent-security-redteam.md) — LLM and agent security red teaming with agentic-actions-auditor, supply-chain-risk-auditor, semgrep, codeql, and sarif-parsing
- [sarif-parsing](../../notes/security-auditing/sarif-parsing.md) — Parses and processes SARIF files from static analysis tools like CodeQL, Semgrep, or other scanners
- [semgrep-rule-creator](../../notes/security-auditing/semgrep-rule-creator.md) — Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns
- [variant-analysis](../../notes/security-auditing/variant-analysis.md) — Hunts for the other instances of a bug already found — the variants of one root cause across a codebase
- [workflow](../../notes/software-dev/workflow.md) — Vercel Workflow DevKit (WDK) expert guidance

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!warning] Vault audit 2026-07-24 — MNT-9
> Cross-references a nonexistent `semgrep-rule-variant-creator` skill — the actual skill is `semgrep-rule-creator`. Use that name.
> _Remote-managed skill — the durable fix belongs upstream; this wrapper note is the local record._
