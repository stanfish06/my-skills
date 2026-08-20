---
title: detect-static-dependencies
aliases:
  - detect static dependencies
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/detect-static-dependencies/SKILL.md
created: 2026-07-21
---

# detect-static-dependencies

> [!info] What it does
> Scan C# source files for hard-to-test static dependencies — DateTime.Now/UtcNow, File.*, Directory.*, Environment.*, HttpClient, Console.*, Process.*, and other untestable statics. Produces a ranked report of static call sites by frequency. USE FOR: find untestable statics, scan for static dependencies, testability audit, identify hard-to-mock code, find DateTime.Now usage, detect static coupling, testability report, static analysis for testability. DO NOT USE FOR: generating wrappers (use generate-testability-wrappers), migrating code (use migrate-static-to-wrapper), general code review, or finding statics that are already behind abstractions.

**Source:** [skills/detect-static-dependencies/SKILL.md](../../../skills/detect-static-dependencies/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [generate-testability-wrappers](../../notes/dotnet-development/generate-testability-wrappers.md) — Generate wrapper interfaces and DI registration for hard-to-test static dependencies in C#, when the abstraction does NOT exist yet
- [migrate-static-to-wrapper](../../notes/dotnet-development/migrate-static-to-wrapper.md) — Replace existing static dependency call sites with a wrapper or built-in abstraction that already exists or is registered in DI

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

