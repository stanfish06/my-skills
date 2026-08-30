---
title: crap-score
aliases:
  - crap score
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/crap-score/SKILL.md
created: 2026-07-21
---

# crap-score

> [!info] What it does
> Calculates targeted CRAP (Change Risk Anti-Patterns) scores for a named .NET method, class, or single source file. Use when the user explicitly asks to compute CRAP scores or assess risky untested code for a specific target, combining Cobertura coverage data with cyclomatic complexity analysis. DO NOT USE FOR: project-wide coverage analysis, coverage plateau or "stuck coverage" diagnosis, what's blocking coverage, or where to add tests across a project (use coverage-analysis); writing tests; running tests without CRAP context.

**Source:** [skills/crap-score/SKILL.md](../../../skills/crap-score/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [code-testing-agent](../../notes/dotnet-development/code-testing-agent.md) — Generates and writes new unit tests for any programming language — scaffolds test projects and configures coverage tooling (coverlet, pytest-cov, @vitest/coverage-v8) as part of test...
- [coverage-analysis](../../notes/security-auditing/coverage-analysis.md) — Measures and interprets what a fuzzing campaign actually reaches, using llvm-cov, lcov, or a fuzzer's own coverage output
- [dotnet-coverage-analysis](../../notes/dotnet-development/dotnet-coverage-analysis.md) — Project-wide code coverage and CRAP (Change Risk Anti-Patterns) score analysis for .NET projects

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!warning] Vault audit 2026-07-24 — MNT-11
> Its DO-NOT-USE-FOR redirect sends project-wide coverage to the generic `coverage-analysis`; for .NET projects route to `dotnet-coverage-analysis` instead.
> _Remote-managed skill — the durable fix belongs upstream; this wrapper note is the local record._

