---
title: coverage-analysis
aliases:
  - coverage analysis
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/coverage-analysis/SKILL.md
created: 2026-06-09
---

# coverage-analysis

> [!info] What it does
> Measures and interprets what a fuzzing campaign actually reaches, using llvm-cov, lcov, or a fuzzer's own coverage output. Covers baselining a new campaign, reading coverage reports, and turning uncovered regions into harness, seed, or dictionary work. Use when a fuzzer plateaus, when judging whether a harness is effective, after changing a harness, or when asking why some code is never reached.

**Source:** [skills/coverage-analysis/SKILL.md](../../../skills/coverage-analysis/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [code-testing-agent](../../notes/dotnet-development/code-testing-agent.md) — Generates and writes new unit tests for any programming language — scaffolds test projects and configures coverage tooling (coverlet, pytest-cov, @vitest/coverage-v8) as part of test...
- [crap-score](../../notes/dotnet-development/crap-score.md) — Calculates targeted CRAP (Change Risk Anti-Patterns) scores for a named .NET method, class, or single source file
- [find-untested-sources](../../notes/dotnet-development/find-untested-sources.md) — Parse-only static analysis that pairs source files with the tests referencing them and emits JSON listing untested files ordered by API surface, each with a suggested_test_path
- [test-anti-patterns](../../notes/dotnet-development/test-anti-patterns.md) — Audits an existing test file or suite in any language for anti-patterns and quality issues — produces a severity-ranked report (Critical/Warning/Info)

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
