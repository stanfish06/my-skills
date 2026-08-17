---
name: agentic-workflows
description: Route gh-aw workflow design/create/debug/upgrade requests and find Agentics starter workflows.
disable-model-invocation: false
---

# Agentic Workflows Router

Use this skill when a user asks to find a template for, design, create, update, debug, or upgrade GitHub Agentic Workflows in this repository.

This skill is a dispatcher: identify the task type, load the matching workflow prompt/skill file, and follow it directly. Keep responses concise and ask a clarifying question if the correct prompt is unclear.

## Agentics template library

Use the bundled `templates/` Git submodule when the user asks for an existing workflow, example, starting point, or recommendation. It pins [`githubnext/agentics`](https://github.com/githubnext/agentics) inside this skill; do not copy the entire collection into a repository's `.github/workflows/` directory.

Read progressively:

1. If the user names a template or slug, load `templates/workflows/<slug>.md`. Follow a `redirect` frontmatter entry when present.
2. If the request is goal-based, read the matching section of `templates/README.md`, then load only one to three candidate workflows.
3. Read `templates/docs/<slug>.md` only when installation notes, behavior, or customization details are needed.
4. Load `templates/workflows/shared/<name>.md` only when the chosen workflow needs reusable tools, MCP servers, formatting, or reporting fragments.

Route common goals as follows:

- Maintenance and moderation: `issue-triage.md`, `daily-issue-triage.md`, `repo-assist.md`, `ai-moderator.md`
- CI faults, optimization, and cost: `ci-doctor.md`, `ci-coach.md`, `cost-tracker.md`, `pr-fix.md`
- Pull request and contribution review: `grumpy-reviewer.md`, `pr-nitpick-reviewer.md`, `contribution-check.md`, `contribution-guidelines-checker.md`
- Research, planning, and status: `weekly-research.md`, `weekly-issue-activity.md`, `repo-status.md`, `team-status.md`, `plan.md`, `repo-chronicle.md`, `weekly-repo-map.md`
- Documentation and wikis: `update-docs.md`, `doc-updater.md`, `agentic-wiki-writer.md`, `agentic-wiki-coder.md`, `glossary-maintainer.md`, `link-checker.md`, `markdown-linter.md`, `unbloat-docs.md`
- Analysis and quality reports: `accessibility-review.md`, `adhoc-qa.md`, `large-file-simplifier.md`, `duplicate-code-detector.md`, `repository-quality-improver.md`, `multi-device-docs-tester.md`
- Code-changing improvements: `code-simplifier.md`, `test-improver.md`, `perf-improver.md`, `efficiency-improver.md`
- Command-triggered assistance: `archie.md`, `plan.md`, `pr-fix.md`, `repo-ask.md`
- Security and formal verification: `malicious-code-scan.md`, `vex-generator.md`, `lean-squad.md`
- Issue organization and farming: `issue-arborist.md`, `sub-issue-closer.md`, `issue-monster.md`, `discussion-task-miner.md`
- Workflow optimization: `q.md`

Before recommending or adapting a template, inspect its triggers, `permissions`, tools, network access, secrets, safe outputs, integrity settings, scheduled frequency, and expected cost. State material risks and repository-specific changes. Templates are starting points, not trusted drop-ins.

When the user authorizes installation, prefer the template's documented `gh aw add-wizard githubnext/agentics/<slug>` command, then inspect the generated source, adapt it to the target repository, compile it, and validate it. Do not install, compile, or activate a workflow merely because the user asked to compare templates.

If `templates/README.md` is absent, the submodule is not initialized. In this vault checkout, initialize it with `git submodule update --init --recursive skills/agentic-workflows/templates`; otherwise report that the bundled templates are unavailable instead of guessing their contents.

Repository overlay (optional):
- If `.github/aw/instructions.md` exists, load it with `@.github/aw/instructions.md` after loading the matched prompt/skill.
- Precedence: repository overlay instructions override upstream defaults when they conflict.

Read only the files you need:
Load these files from `github/gh-aw` (they are not available locally).
- `.github/aw/action-container-substitutions.md`
- `.github/aw/agent-runtime-instructions.md`
- `.github/aw/agentic-chat.md`
- `.github/aw/agentic-workflows-mcp.md`
- `.github/aw/asciicharts.md`
- `.github/aw/campaign.md`
- `.github/aw/charts-trending.md`
- `.github/aw/charts.md`
- `.github/aw/cli-commands.md`
- `.github/aw/configure-agentic-engine.md`
- `.github/aw/context.md`
- `.github/aw/create-agentic-workflow-trigger-details.md`
- `.github/aw/create-agentic-workflow.md`
- `.github/aw/create-shared-agentic-workflow.md`
- `.github/aw/debug-agentic-workflow.md`
- `.github/aw/dependabot.md`
- `.github/aw/deployment-status.md`
- `.github/aw/designer-mappings.md`
- `.github/aw/designer.md`
- `.github/aw/enclaves.md`
- `.github/aw/evals.md`
- `.github/aw/experiments.md`
- `.github/aw/github-agentic-workflows.md`
- `.github/aw/github-mcp-server-pagination.md`
- `.github/aw/github-mcp-server.md`
- `.github/aw/instructions.md`
- `.github/aw/linter-workflows.md`
- `.github/aw/llms.md`
- `.github/aw/loop.md`
- `.github/aw/lsp.md`
- `.github/aw/maintainer.md`
- `.github/aw/mcp-clis.md`
- `.github/aw/memory-stateful-patterns.md`
- `.github/aw/memory.md`
- `.github/aw/messages.md`
- `.github/aw/multi-agent-research.md`
- `.github/aw/network.md`
- `.github/aw/optimize-agentic-workflow.md`
- `.github/aw/patterns.md`
- `.github/aw/pr-reviewer.md`
- `.github/aw/release-workflow.md`
- `.github/aw/report.md`
- `.github/aw/reuse.md`
- `.github/aw/safe-outputs-automation.md`
- `.github/aw/safe-outputs-content.md`
- `.github/aw/safe-outputs-management.md`
- `.github/aw/safe-outputs-runtime.md`
- `.github/aw/safe-outputs.md`
- `.github/aw/serena-tool.md`
- `.github/aw/shared-safe-jobs.md`
- `.github/aw/skills.md`
- `.github/aw/subagents.md`
- `.github/aw/syntax-agentic.md`
- `.github/aw/syntax-core.md`
- `.github/aw/syntax-engine.md`
- `.github/aw/syntax-tools-imports.md`
- `.github/aw/syntax.md`
- `.github/aw/test-coverage.md`
- `.github/aw/test-expression.md`
- `.github/aw/token-optimization-caching-budgets.md`
- `.github/aw/token-optimization-observability.md`
- `.github/aw/token-optimization.md`
- `.github/aw/triggers.md`
- `.github/aw/update-agentic-workflow.md`
- `.github/aw/upgrade-agentic-workflows.md`
- `.github/aw/visual-regression.md`
- `.github/aw/workflow-constraints.md`
- `.github/aw/workflow-editing.md`
- `.github/aw/workflow-patterns.md`

After loading the matching workflow prompt or skill, follow it directly:
- Design workflows from scratch via interview: `.github/aw/designer.md`
- Create new workflows: `.github/aw/create-agentic-workflow.md`
- Configure or add declarative engines: `.github/aw/configure-agentic-engine.md`
- Update existing workflows: `.github/aw/update-agentic-workflow.md`
- Debug, audit, or investigate workflows: `.github/aw/debug-agentic-workflow.md`
- Upgrade workflows and fix deprecations: `.github/aw/upgrade-agentic-workflows.md`
- Create shared components or MCP wrappers: `.github/aw/create-shared-agentic-workflow.md`
- Create report-generating workflows: `.github/aw/report.md`
- Fix Dependabot manifest PRs: `.github/aw/dependabot.md`
- Analyze coverage workflows: `.github/aw/test-coverage.md`
- Render compact markdown charts: `.github/aw/asciicharts.md`
- Map CLI commands to MCP usage: `.github/aw/cli-commands.md`
- Choose workflow architecture and patterns: `.github/aw/patterns.md`
- Optimize token usage and cost: `.github/aw/token-optimization.md`
- Design long-running multi-agent research workflows: `.github/aw/multi-agent-research.md`

When the task involves OTEL, OTLP, traces, observability backends, or telemetry-driven analysis, also read and follow `skills/otel-queries/SKILL.md` after loading the matching workflow prompt or skill.
