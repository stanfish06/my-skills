---
title: run-tests
aliases:
  - run tests
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/run-tests/SKILL.md
created: 2026-07-21
---

# run-tests

> [!info] What it does
> Recommend or run the exact `dotnet test` command. Use when the user asks to run, filter, or troubleshoot .NET tests or wants the precise command, flags, or argument order — the right syntax depends on the test platform (VSTest vs Microsoft.Testing.Platform) and SDK version and is easy to get wrong from memory. USE FOR: running all tests or a subset (a specific class, category, or trait) via filters; a single framework in a multi-TFM project (`--framework`); TRX reports; crash or hang dumps; whether MTP args need the `--` separator (SDK 8/9) or pass directly (SDK 10+); diagnosing why `dotnet test` fails or uses wrong argument syntax. Detects the platform (VSTest vs MTP) and framework (MSTest/xUnit/NUnit/TUnit), then picks the matching command and filter flag (--filter, --filter-class, --filter-trait, --filter-query, --treenode-filter). DO NOT USE FOR: writing test code (use code-testing-agent), iterating on failing tests without rebuilding (use mtp-hot-reload), CI/CD config, or debugging test logic.

**Source:** [skills/run-tests/SKILL.md](../../../skills/run-tests/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [code-testing-agent](../../notes/dotnet-development/code-testing-agent.md) — Generates and writes new unit tests for any programming language — scaffolds test projects and configures coverage tooling (coverlet, pytest-cov, @vitest/coverage-v8) as part of test...
- [dotnet-coverage-analysis](../../notes/dotnet-development/dotnet-coverage-analysis.md) — Project-wide code coverage and CRAP (Change Risk Anti-Patterns) score analysis for .NET projects
- [filter-syntax](../../notes/dotnet-development/filter-syntax.md) — Reference data for test filter syntax across all platform and framework combinations: VSTest --filter expressions, MTP filters for MSTest/NUnit/xUnit v3/TUnit, and VSTest-to-MTP filter...
- [mtp-hot-reload](../../notes/dotnet-development/mtp-hot-reload.md) — Suggests using Microsoft Testing Platform (MTP) hot reload to iterate fixes on failing tests without rebuilding
- [platform-detection](../../notes/dotnet-development/platform-detection.md) — Reference data for detecting the test platform (VSTest vs Microsoft.Testing.Platform) and test framework (MSTest, xUnit, NUnit, TUnit) from project files
- [test-anti-patterns](../../notes/dotnet-development/test-anti-patterns.md) — Audits an existing test file or suite in any language for anti-patterns and quality issues — produces a severity-ranked report (Critical/Warning/Info)
- [test-smell-detection](../../notes/dotnet-development/test-smell-detection.md) — Deep-dive audit using the full testsmells.org 19-smell academic catalog for tests in any language
- [writing-mstest-tests](../../notes/dotnet-development/writing-mstest-tests.md) — Write, create, modernize, or fix comprehensive MSTest unit tests with MSTest 3.x/4.x APIs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

