---
title: test-anti-patterns
aliases:
  - test anti patterns
  - Critical
  - Warning
  - Info
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/test-anti-patterns/SKILL.md
created: 2026-07-21
---

# test-anti-patterns

> [!info] What it does
> Audits an existing test file or suite in any language for anti-patterns and quality issues — produces a severity-ranked report (Critical/Warning/Info). INVOKE whenever asked to audit or review tests, find what's wrong with a suite, judge whether tests are any good, or check for: tests that pass but verify nothing, missing assertions, swallowed exceptions, self-comparing / tautological assertions, coverage-touching tests, broad exceptions, flaky or order-dependent tests (Thread.Sleep, DateTime.Now, shared state), duplicated tests, or magic values — in .NET, Python/pytest, TS/Jest, Java, Go, Ruby or C++. DO NOT USE FOR: writing new tests (use code-testing-agent, or writing-mstest-tests for MSTest); running tests (use run-tests); migration; assertion-diversity metrics (use assertion-quality); coverage/CRAP metrics (use coverage-analysis); the testsmells.org academic catalog (use test-smell-detection); fixing or modernizing MSTest tests, assertions, attributes, or lifecycle (use writing-mstest-tests).

**Source:** [skills/test-anti-patterns/SKILL.md](../../../skills/test-anti-patterns/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [assertion-quality](../../notes/dotnet-development/assertion-quality.md) — Analyzes the variety and depth of assertions across test suites in any language
- [code-testing-agent](../../notes/dotnet-development/code-testing-agent.md) — Generates and writes new unit tests for any programming language — scaffolds test projects and configures coverage tooling (coverlet, pytest-cov, @vitest/coverage-v8) as part of test...
- [coverage-analysis](../../notes/security-auditing/coverage-analysis.md) — Coverage analysis measures code exercised during fuzzing
- [dotnet-coverage-analysis](../../notes/dotnet-development/dotnet-coverage-analysis.md) — Project-wide code coverage and CRAP (Change Risk Anti-Patterns) score analysis for .NET projects
- [exp-test-maintainability](../../notes/dotnet-development/exp-test-maintainability.md) — Detects duplicate boilerplate, copy-paste tests, and structural maintainability issues across .NET test suites
- [grade-tests](../../notes/dotnet-development/grade-tests.md) — Grades a specified set of test methods individually and produces a concise table mapping each test (fully-qualified name) to a letter grade (A–F), a score band, and a one-line note —...
- [jest](../../notes/software-dev/jest.md) — JavaScript testing with Jest — unit tests, mocks, spies, snapshot testing, code coverage, and configuration
- [pytest](../../notes/software-dev/pytest.md) — Testing Python code with pytest — fixtures, parametrization, markers, mocking, coverage, and configuration
- [run-tests](../../notes/dotnet-development/run-tests.md) — Recommend or run the exact `dotnet test` command
- [test-analysis-extensions](../../notes/dotnet-development/test-analysis-extensions.md) — Provides file paths to language-specific reference files for the test ANALYSIS skills (assertion-quality, test-anti-patterns, test-gap-analysis, test-smell-detection, test-tagging)
- [test-gap-analysis](../../notes/dotnet-development/test-gap-analysis.md) — Performs pseudo-mutation analysis on production code in any language to find gaps in existing tests
- [test-smell-detection](../../notes/dotnet-development/test-smell-detection.md) — Deep-dive audit using the full testsmells.org 19-smell academic catalog for tests in any language
- [writing-mstest-tests](../../notes/dotnet-development/writing-mstest-tests.md) — Write, create, modernize, or fix comprehensive MSTest unit tests with MSTest 3.x/4.x APIs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!note] Vault audit 2026-07-24 — USE-19
> Use this for language-agnostic test anti-pattern audits across any suite; it is filed under the .NET map but is not .NET-specific — for .NET/MSTest authoring use `writing-mstest-tests` and for .NET coverage/CRAP use `dotnet-coverage-analysis`. Distinguishing axis: polyglot test analysis vs .NET-only tooling.

