---
title: test-smell-detection
aliases:
  - test smell detection
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/test-smell-detection/SKILL.md
created: 2026-07-21
---

# test-smell-detection

> [!info] What it does
> Deep-dive audit using the full testsmells.org 19-smell academic catalog for tests in any language. Every finding maps to a named, citable smell from the research literature (Assertion Roulette, Duplicate Assert, Mystery Guest, Eager Test, Sensitive Equality, Conditional Test Logic, Sleepy Test, Magic Number Test, etc.) with research-backed severity. Polyglot: .NET (MSTest/xUnit/NUnit/TUnit), Python (pytest/unittest), TS/JS (Jest/Vitest/Mocha/node:test), Java (JUnit/TestNG), Go, Ruby (RSpec/Minitest), Rust, Swift, Kotlin (JUnit/Kotest), PowerShell (Pester), C++ (GoogleTest/Catch2). INVOKE ONLY when explicitly asked for the testsmells.org 19-smell academic catalog or citable smell names from the literature. DO NOT USE FOR: general or pragmatic audits — use test-anti-patterns; writing new tests (use code-testing-agent, or writing-mstest-tests for MSTest); running tests (use run-tests); framework migration.

**Source:** [skills/test-smell-detection/SKILL.md](../../../skills/test-smell-detection/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [code-testing-agent](../../notes/dotnet-development/code-testing-agent.md) — Generates and writes new unit tests for any programming language — scaffolds test projects and configures coverage tooling (coverlet, pytest-cov, @vitest/coverage-v8) as part of test...
- [jest](../../notes/software-dev/jest.md) — JavaScript testing with Jest — unit tests, mocks, spies, snapshot testing, code coverage, and configuration
- [pytest](../../notes/software-dev/pytest.md) — Testing Python code with pytest — fixtures, parametrization, markers, mocking, coverage, and configuration
- [research](../../notes/software-dev/research.md) — Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo
- [run-tests](../../notes/dotnet-development/run-tests.md) — Recommend or run the exact `dotnet test` command
- [test-analysis-extensions](../../notes/dotnet-development/test-analysis-extensions.md) — Provides file paths to language-specific reference files for the test ANALYSIS skills (assertion-quality, test-anti-patterns, test-gap-analysis, test-smell-detection, test-tagging)
- [test-anti-patterns](../../notes/dotnet-development/test-anti-patterns.md) — Audits an existing test file or suite in any language for anti-patterns and quality issues — produces a severity-ranked report (Critical/Warning/Info)
- [vitest](../../notes/software-dev/vitest.md) — JavaScript/TypeScript unit testing with Vitest — fast Vite-native test runner with Jest-compatible API
- [writing-mstest-tests](../../notes/dotnet-development/writing-mstest-tests.md) — Write, create, modernize, or fix comprehensive MSTest unit tests with MSTest 3.x/4.x APIs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

