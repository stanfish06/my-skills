---
title: authoring-github-workflows
aliases:
  - authoring github workflows
tags:
  - skill
  - domain/dotnet-development
domain: dotnet-development
status: untried
source: skills/authoring-github-workflows/SKILL.md
created: 2026-07-21
---

# authoring-github-workflows

> [!info] What it does
> Author and review GitHub Actions workflow YAML safely so syntactically-valid YAML can't ship a workflow that GitHub Actions refuses to run. USE FOR: editing, adding, or reviewing any file under .github/workflows/, writing run-name/name/if/env/run values that contain ${{ }} expressions, diagnosing a run that fails with 'This run likely failed because of a workflow file issue' and no jobs starting, deciding when a workflow scalar must be quoted, validating workflows with actionlint. DO NOT USE FOR: authoring application YAML unrelated to GitHub Actions, Azure Pipelines, GitLab CI, or non-workflow YAML. SCOPE: this skill covers *syntactic/structural* correctness of workflow YAML (quoting, parsing, actionlint); for *semantic and functional* workflow design (what a workflow should do, agentic-workflow behavior), see .github/agents/agentic-workflows.agent.md — the two are complementary. INVOKES: actionlint (downloaded pinned binary) plus git/grep for inspection.

**Source:** [skills/authoring-github-workflows/SKILL.md](../../../skills/authoring-github-workflows/SKILL.md)  ·  **Domain:** [.NET & C# Development](../../maps/dotnet-development.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [agentic-workflows](../../notes/software-dev/agentic-workflows.md) — Route gh-aw workflow design/create/debug/upgrade requests to the right prompts
- [github](../../notes/software-dev/github.md) — Triage and orient GitHub repository, pull request, and issue work through the connected GitHub app
- [workflow](../../notes/software-dev/workflow.md) — Vercel Workflow DevKit (WDK) expert guidance

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

