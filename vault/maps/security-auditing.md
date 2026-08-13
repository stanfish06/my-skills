---
title: Security & Auditing
tags:
  - skill-map
created: 2026-06-13
---

# Security & Auditing

> [!abstract] Scope
> Secure development, code auditing, static analysis, SARIF, fuzzing, agent security, supply-chain risk, and smart-contract review helpers.

[Back to Skill Index](../index.md)

**Related maps:** [Cloud, Infra & MLOps](cloud-devops.md) | [Vault, Skills & Workflow Meta](vault-meta.md) | [Analytics Engineering & LLM Operations](analytics-engineering.md) | [Web Automation, Frontend & Design](web-automation-frontend.md) | [.NET & C# Development](dotnet-development.md)

## Skills (48)

- [aflpp](../notes/security-auditing/aflpp.md) — AFL++ is a fork of AFL with better fuzzing performance and advanced features
- [agentic-actions-auditor](../notes/security-auditing/agentic-actions-auditor.md) — Audits GitHub Actions workflows for security vulnerabilities in AI agent integrations including Claude Code Action, Gemini CLI, OpenAI Codex, and GitHub AI Inference
- [atheris](../notes/security-auditing/atheris.md) — Atheris is a coverage-guided Python fuzzer based on libFuzzer
- [attack-path-analysis](../notes/security-auditing/attack-path-analysis.md) — Use when Codex is already in the attack-path-analysis phase of a security scan or the user explicitly asks to trace a security finding from source to sink and calibrate severity
- [audit-context-building](../notes/security-auditing/audit-context-building.md) — Understand a codebase before looking for bugs in it - what each function assumes, what it guarantees, and what it depends on elsewhere
- [audit-prep-assistant](../notes/security-auditing/audit-prep-assistant.md) — Prepares codebases for security review using Trail of Bits' checklist
- [auth](../notes/security-auditing/auth.md) — Authentication integration guidance — Clerk (native Vercel Marketplace), Descope, and Auth0 setup for Next.js applications
- [c-review](../notes/security-auditing/c-review.md) — Performs comprehensive C/C++ security review for memory corruption, integer overflows, race conditions, and platform-specific vulnerabilities
- [cargo-fuzz](../notes/security-auditing/cargo-fuzz.md) — cargo-fuzz is the de facto fuzzing tool for Rust projects using Cargo
- [code-maturity-assessor](../notes/security-auditing/code-maturity-assessor.md) — Systematic code maturity assessment using Trail of Bits' 9-category framework
- [codeql](../notes/security-auditing/codeql.md) — Scans a codebase for security vulnerabilities using CodeQL's interprocedural data flow and taint tracking analysis
- [constant-time-analysis](../notes/security-auditing/constant-time-analysis.md) — Detects timing side-channel vulnerabilities in cryptographic code
- [constant-time-testing](../notes/security-auditing/constant-time-testing.md) — Constant-time testing detects timing side channels in cryptographic code
- [coverage-analysis](../notes/security-auditing/coverage-analysis.md) — Coverage analysis measures code exercised during fuzzing
- [deep-security-scan](../notes/security-auditing/deep-security-scan.md) — Use when the user asks for a deep, exhaustive, multi-pass, or variance-reducing repository-wide or scoped-path Codex Security scan
- [differential-review](../notes/security-auditing/differential-review.md) — Performs security-focused differential review of code changes (PRs, commits, diffs)
- [entry-point-analyzer](../notes/security-auditing/entry-point-analyzer.md) — Analyzes smart contract codebases to identify state-changing entry points for security auditing
- [finding-discovery](../notes/security-auditing/finding-discovery.md) — Use when Codex is already in the finding-discovery phase of a security scan or the user explicitly asks to discover candidate security findings in a repository or code change
- [fix-finding](../notes/security-auditing/fix-finding.md) — Use when the user explicitly asks to fix and verify a validated or plausible security finding
- [fp-check](../notes/security-auditing/fp-check.md) — Systematically verifies suspected security bugs to eliminate false positives, producing a TRUE POSITIVE or FALSE POSITIVE verdict with documented evidence for each
- [fuzzing-dictionary](../notes/security-auditing/fuzzing-dictionary.md) — Fuzzing dictionaries guide fuzzers with domain-specific tokens
- [fuzzing-obstacles](../notes/security-auditing/fuzzing-obstacles.md) — Techniques for patching code to overcome fuzzing obstacles
- [gh-cli](../notes/security-auditing/gh-cli.md) — Enforces authenticated gh CLI workflows over unauthenticated curl/WebFetch patterns
- [guidelines-advisor](../notes/security-auditing/guidelines-advisor.md) — Smart contract development advisor based on Trail of Bits' best practices
- [harness-writing](../notes/security-auditing/harness-writing.md) — Techniques for writing effective fuzzing harnesses across languages
- [insecure-defaults](../notes/security-auditing/insecure-defaults.md) — Detects fail-open insecure defaults (hardcoded secrets, weak auth, permissive security) that allow apps to run insecurely in production
- [libfuzzer](../notes/security-auditing/libfuzzer.md) — Coverage-guided fuzzer built into LLVM for C/C++ projects
- [llm-agent-security-redteam](../notes/security-auditing/llm-agent-security-redteam.md) — LLM and agent security red teaming with agentic-actions-auditor, supply-chain-risk-auditor, semgrep, codeql, and sarif-parsing
- [ossfuzz](../notes/security-auditing/ossfuzz.md) — OSS-Fuzz provides free continuous fuzzing for open source projects
- [property-based-testing](../notes/security-auditing/property-based-testing.md) — Provides guidance for property-based testing across multiple languages and smart contracts
- [propose-security-hardening](../notes/security-auditing/propose-security-hardening.md) — Develop evidence-backed structural and architectural security hardening proposals from vulnerability disclosures, supplied findings, incident or assessment documents, source code, or a...
- [sarif-parsing](../notes/security-auditing/sarif-parsing.md) — Parses and processes SARIF files from static analysis tools like CodeQL, Semgrep, or other scanners
- [secure-workflow-guide](../notes/security-auditing/secure-workflow-guide.md) — Guides through Trail of Bits' 5-step secure development workflow
- [security-and-hardening](../notes/security-auditing/security-and-hardening.md) — Hardens code against vulnerabilities. Use when handling user input, authentication, data storage, or external integrations
- [security-diff-scan](../notes/security-auditing/security-diff-scan.md) — Use when the user asks for a security review of a pull request, commit, branch diff, working-tree patch, or other Git-backed change set
- [security-scan](../notes/security-auditing/security-scan.md) — Use for a standard, single-pass security audit of an entire repository or a scoped path, package folder, or submodule with no diff to review
- [semgrep](../notes/security-auditing/semgrep.md) — Runs a Semgrep security scan over a codebase: detects languages, selects rulesets, presents the plan for explicit approval, then runs every approved ruleset through...
- [semgrep-rule-creator](../notes/security-auditing/semgrep-rule-creator.md) — Creates custom Semgrep rules for detecting security vulnerabilities, bug patterns, and code patterns
- [sharp-edges](../notes/security-auditing/sharp-edges.md) — Identifies error-prone APIs, dangerous configurations, and footgun designs that enable security mistakes
- [spec-to-code-compliance](../notes/security-auditing/spec-to-code-compliance.md) — Check code against the documentation that specifies it - which requirements hold, which the code contradicts, which are absent, and what the code does that no document mentions
- [supply-chain-risk-auditor](../notes/security-auditing/supply-chain-risk-auditor.md) — Audits a project's dependencies for supply-chain risk: version-matched advisories for direct dependencies and the full lockfile tree, abandoned or archived upstreams, npm publisher...
- [threat-model](../notes/security-auditing/threat-model.md) — Use when Codex is already in the threat-modeling phase of a security scan, the user explicitly invokes $threat-model, or the user explicitly asks to create, update, or persist a...
- [token-integration-analyzer](../notes/security-auditing/token-integration-analyzer.md) — Token integration and implementation analyzer based on Trail of Bits' token integration checklist
- [track-findings](../notes/security-auditing/track-findings.md) — Track validated Codex Security findings in Linear, Jira, GitHub issues, or draft GitHub security advisories
- [triage-finding](../notes/security-auditing/triage-finding.md) — Use when the user supplies or imports existing security findings, vulnerability reports, or security/vulnerability Jira/Linear tickets from scanners, advisories, GitHub, Atlassian...
- [variant-analysis](../notes/security-auditing/variant-analysis.md) — Hunts for the other instances of a bug already found — the variants of one root cause across a codebase
- [vulnerability-writeup](../notes/security-auditing/vulnerability-writeup.md) — Write up vulnerabilities from disclosure documents, rough notes, supplied findings, PoCs, source code, or Codex Security scan output into polished, self-contained, source-backed reports
- [zeroize-audit](../notes/security-auditing/zeroize-audit.md) — Detects missing zeroization of sensitive data in source code and identifies zeroization removed by compiler optimizations, with assembly-level analysis, and control-flow verification
