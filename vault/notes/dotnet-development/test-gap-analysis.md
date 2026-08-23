---
title: test-gap-analysis
aliases:
  - test gap analysis
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/test-gap-analysis/SKILL.md
created: 2026-07-21
---

# test-gap-analysis

> [!info] What it does
> Performs pseudo-mutation analysis on production code in any language to find gaps in existing tests. Use when the user asks to find weak or shallow tests, discover untested edge cases, or check whether tests would catch a bug — e.g. "would my tests catch it if someone changed the code", "would a subtle logic or boundary change slip past the current tests", "are my tests strong enough to catch a subtle bug". Evaluates test effectiveness through mutation-style reasoning: analyzes mutation points (boundaries, boolean flips, null returns, exception removal, arithmetic changes) and checks whether tests would detect each. Polyglot: .NET, Python, TS/JS, Java, Go, Ruby, Rust, Swift, Kotlin, PowerShell, C++. DO NOT USE FOR: writing new tests (use code-testing-agent, or writing-mstest-tests for MSTest), detecting anti-patterns (use test-anti-patterns), measuring assertion diversity (use assertion-quality), or running actual mutation testing tools (Stryker, mutmut, PIT, cargo-mutants).

**Source:** [skills/test-gap-analysis/SKILL.md](../../../skills/test-gap-analysis/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [assertion-quality](../../notes/dotnet-development/assertion-quality.md) — Analyzes the variety and depth of assertions across test suites in any language
- [code-testing-agent](../../notes/dotnet-development/code-testing-agent.md) — Generates and writes new unit tests for any programming language — scaffolds test projects and configures coverage tooling (coverlet, pytest-cov, @vitest/coverage-v8) as part of test...
- [find-untested-sources](../../notes/dotnet-development/find-untested-sources.md) — Parse-only static analysis that pairs source files with the tests referencing them and emits JSON listing untested files ordered by API surface, each with a suggested_test_path
- [test-analysis-extensions](../../notes/dotnet-development/test-analysis-extensions.md) — Provides file paths to language-specific reference files for the test ANALYSIS skills (assertion-quality, test-anti-patterns, test-gap-analysis, test-smell-detection, test-tagging)
- [test-anti-patterns](../../notes/dotnet-development/test-anti-patterns.md) — Audits an existing test file or suite in any language for anti-patterns and quality issues — produces a severity-ranked report (Critical/Warning/Info)
- [writing-mstest-tests](../../notes/dotnet-development/writing-mstest-tests.md) — Write, create, modernize, or fix comprehensive MSTest unit tests with MSTest 3.x/4.x APIs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

