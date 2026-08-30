---
title: find-untested-sources
aliases:
  - find untested sources
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/find-untested-sources/SKILL.md
created: 2026-07-21
---

# find-untested-sources

> [!info] What it does
> Parse-only static analysis that pairs source files with the tests referencing them and emits JSON listing untested files ordered by API surface, each with a suggested_test_path. Roslyn engine for C#/.NET (namespace-aware), tree-sitter engine for polyglot repos (Python, TS/JS, Go, Java, Rust, Ruby). USE FOR: where to write tests next, which files have no tests, find untested code, build a source-to-test pairing map, prioritized test-gap worklist. DO NOT USE FOR: line/branch coverage or CRAP risk (use coverage-analysis); whether existing tests are strong (use test-gap-analysis or assertion-quality).

**Source:** [skills/find-untested-sources/SKILL.md](../../../skills/find-untested-sources/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [assertion-quality](../../notes/dotnet-development/assertion-quality.md) — Analyzes the variety and depth of assertions across test suites in any language
- [coverage-analysis](../../notes/security-auditing/coverage-analysis.md) — Measures and interprets what a fuzzing campaign actually reaches, using llvm-cov, lcov, or a fuzzer's own coverage output
- [test-gap-analysis](../../notes/dotnet-development/test-gap-analysis.md) — Performs pseudo-mutation analysis on production code in any language to find gaps in existing tests

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

