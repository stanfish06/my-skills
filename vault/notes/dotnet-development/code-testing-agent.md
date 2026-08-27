---
title: code-testing-agent
aliases:
  - code testing agent
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/code-testing-agent/SKILL.md
created: 2026-07-21
---

# code-testing-agent

> [!info] What it does
> Generates and writes new unit tests for any programming language — scaffolds test projects and configures coverage tooling (coverlet, pytest-cov, @vitest/coverage-v8) as part of test generation. Use when asked to generate tests, generate pytest tests, generate Vitest tests, write unit tests, add tests, improve coverage, comprehensive tests, or scaffold a new test project or suite for an app, service, library, REST API, blueprint, or package — including project-wide, multi-file test generation across services, repositories, routes, and modules. Supports C#/.NET, Python (pytest, Flask/Django), TypeScript/JavaScript (Vitest, Jest, Mocha), Go, Rust, Java (JUnit). Runs a research, planning, and implementation pipeline so tests compile and pass. DO NOT USE FOR: running existing tests (use run-tests); analyzing existing coverage reports (use coverage-analysis or crap-score); writing, fixing, or modernizing MSTest-specific tests, assertions, attributes, or lifecycle (use writing-mstest-tests).

**Source:** [skills/code-testing-agent/SKILL.md](../../../skills/code-testing-agent/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [assertion-quality](../../notes/dotnet-development/assertion-quality.md) — Analyzes the variety and depth of assertions across test suites in any language
- [coverage-analysis](../../notes/security-auditing/coverage-analysis.md) — Measures and interprets what a fuzzing campaign actually reaches, using llvm-cov, lcov, or a fuzzer's own coverage output
- [crap-score](../../notes/dotnet-development/crap-score.md) — Calculates targeted CRAP (Change Risk Anti-Patterns) scores for a named .NET method, class, or single source file
- [jest](../../notes/software-dev/jest.md) — JavaScript testing with Jest — unit tests, mocks, spies, snapshot testing, code coverage, and configuration
- [pytest](../../notes/software-dev/pytest.md) — Testing Python code with pytest — fixtures, parametrization, markers, mocking, coverage, and configuration
- [research](../../notes/software-dev/research.md) — Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo
- [run-tests](../../notes/dotnet-development/run-tests.md) — Recommend or run the exact `dotnet test` command
- [test-anti-patterns](../../notes/dotnet-development/test-anti-patterns.md) — Audits an existing test file or suite in any language for anti-patterns and quality issues — produces a severity-ranked report (Critical/Warning/Info)
- [test-gap-analysis](../../notes/dotnet-development/test-gap-analysis.md) — Performs pseudo-mutation analysis on production code in any language to find gaps in existing tests
- [test-smell-detection](../../notes/dotnet-development/test-smell-detection.md) — Deep-dive audit using the full testsmells.org 19-smell academic catalog for tests in any language
- [vitest](../../notes/software-dev/vitest.md) — JavaScript/TypeScript unit testing with Vitest — fast Vite-native test runner with Jest-compatible API
- [writing-mstest-tests](../../notes/dotnet-development/writing-mstest-tests.md) — Write, create, modernize, or fix comprehensive MSTest unit tests with MSTest 3.x/4.x APIs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!note] Vault audit 2026-07-24 — USE-19
> Use this to generate new tests in any language (C#/.NET, Python, TS/JS, Go, Rust, Java); it is filed under the .NET map but is not .NET-specific — for MSTest-specific authoring/modernization use `writing-mstest-tests`. Distinguishing axis: polyglot test generation vs .NET-only authoring.

