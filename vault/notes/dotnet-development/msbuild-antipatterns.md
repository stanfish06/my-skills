---
title: msbuild-antipatterns
aliases:
  - msbuild antipatterns
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/msbuild-antipatterns/SKILL.md
created: 2026-07-21
---

# msbuild-antipatterns

> [!info] What it does
> Detect and fix MSBuild anti-patterns in project and build files. USE WHEN asked to review, audit, lint, clean up, or code-review a .csproj/.vbproj/.fsproj/.props/.targets/.proj (or Directory.Build.props/.targets) file, when asked 'is this project file correct?' or 'what's wrong with my build file?', or when hunting subtle build bugs caused by how a project is authored. Each anti-pattern has a symptom and a concrete BAD→GOOD fix. DO NOT USE FOR: non-MSBuild build systems (npm, Maven, CMake), or migrating a project to SDK-style (use msbuild-modernization).

**Source:** [skills/msbuild-antipatterns/SKILL.md](../../../skills/msbuild-antipatterns/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [code-review](../../notes/software-dev/code-review.md) — Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the...
- [extension-points](../../notes/dotnet-development/extension-points.md) — Guide for MSBuild extensibility: CustomBefore/CustomAfter hooks, wildcard imports with alphabetic ordering, import gating with control properties, NuGet package build extension layout...
- [item-management](../../notes/dotnet-development/item-management.md) — Patterns for managing MSBuild item groups: Include/Remove/Update semantics, item metadata, batching with %(Metadata), transforms, per-item filtering, and cross-product batching pitfalls
- [msbuild-modernization](../../notes/dotnet-development/msbuild-modernization.md) — Guide for modernizing and migrating MSBuild project files to SDK-style format
- [property-patterns](../../notes/dotnet-development/property-patterns.md) — MSBuild property definition patterns: conditional defaults, composition/concatenation, path normalization, trailing-slash handling, TFM detection helpers, and evaluation order
- [target-authoring](../../notes/dotnet-development/target-authoring.md) — Canonical patterns for writing custom MSBuild targets

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

