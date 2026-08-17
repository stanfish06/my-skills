---
description: Runs Markdown quality checks using Super Linter and creates issues for violations
on:
  workflow_dispatch:
  schedule:
    - cron: "weekly on monday" # fuzzy schedule; gh-aw picks a stable scattered time

permissions:
  contents: read
  actions: read
  issues: read
  pull-requests: read

safe-outputs:
  create-issue:
    expires: 2d
    title-prefix: "[linter] "
    labels: [automation, code-quality]
  noop:
  # the detection job otherwise runs on Claude Code's default model (opus)
  threat-detection:
    engine:
      id: claude
      model: claude-haiku-4-5

name: Markdown Linter
# copilot engine is unusable on this account's plan via PAT (gh-aw#46531);
# claude engine requires the ANTHROPIC_API_KEY repo secret
engine: claude
model: claude-haiku-4-5
# the AWF proxy's token steering / model fallback silently swapped haiku for
# opus-5 after a thinking-param retry; pin the configured model exactly
sandbox:
  agent:
    token-steering: false
    model-fallback: false
timeout-minutes: 15

imports:
  - shared/reporting.md

jobs:
  super_linter:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: read
      statuses: write
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7.0.1
        with:
          fetch-depth: 0
          persist-credentials: false

      - name: Super-linter
        uses: super-linter/super-linter@v8.7.0
        id: super-linter
        # lint violations are input for the agent report, not a job failure
        continue-on-error: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          CREATE_LOG_FILE: "true"
          LOG_FILE: super-linter.log
          DEFAULT_BRANCH: master
          ENABLE_GITHUB_ACTIONS_STEP_SUMMARY: "true"
          VALIDATE_MARKDOWN: "true"
          VALIDATE_ALL_CODEBASE: "true"
          # super-linter's default markdown config name is .markdown-lint.yml
          MARKDOWN_CONFIG_FILE: ".markdownlint.json"
          # skills/ holds vendored/synced skill files; lint only vault notes and repo docs
          FILTER_REGEX_EXCLUDE: ".*/skills/.*"

      - name: Check for linting issues
        id: check-results
        run: |
          if [ -f "super-linter.log" ] && [ -s "super-linter.log" ]; then
            if grep -qE "ERROR|WARN|FAIL" super-linter.log; then
              echo "needs-linting=true" >> "$GITHUB_OUTPUT"
            else
              echo "needs-linting=false" >> "$GITHUB_OUTPUT"
            fi
          else
            echo "needs-linting=false" >> "$GITHUB_OUTPUT"
          fi

      - name: Fix log file ownership
        if: always()
        # the super-linter container writes the log as root
        run: |
          if [ -f super-linter.log ]; then
            sudo chown "$(id -u):$(id -g)" super-linter.log
          fi

      - name: Upload super-linter log
        if: always()
        uses: actions/upload-artifact@v7
        with:
          name: super-linter-log
          path: super-linter.log
          retention-days: 7
steps:
  - name: Download super-linter log
    uses: actions/download-artifact@v8
    with:
      name: super-linter-log
      path: /tmp/gh-aw/
tools:
  bash:
    - "cat"
    - "head"
    - "tail"
    - "grep"
    - "wc"
    - "ls"
    - "sed"
    - "awk"
    - "sort"
    - "uniq"
    - "cut"
source: githubnext/agentics/workflows/markdown-linter.md@42c2ab5b4e4c9273534c39259b2e0df7f20f07e9
---

# Markdown Quality Report

You are an expert documentation quality analyst. Your task is to analyze the Super Linter Markdown output and create a comprehensive issue report for the repository maintainers.

## Context

- **Repository**: ${{ github.repository }}
- **Triggered by**: @${{ github.actor }}
- **Run ID**: ${{ github.run_id }}

## Your Task

1. **Read the linter output** from `/tmp/gh-aw/super-linter.log` using the bash tool
2. **Analyze the findings**:
   - Categorize errors by severity (critical, high, medium, low)
   - Identify patterns in the errors
   - Determine which errors are most important to fix first
   - Note: This workflow only validates Markdown files, and `skills/` (vendored/synced skill files) is excluded — findings cover the Obsidian vault notes (`vault/`) and repo docs
3. **Create a detailed issue** with the following structure:

### Issue Title
Use format: "Markdown Quality Report - [Date] - [X] issues found"

### Issue Body Structure

```markdown
## 🔍 Markdown Linter Summary

**Date**: [Current date]
**Total Issues Found**: [Number]
**Run ID**: ${{ github.run_id }}

## 📊 Breakdown by Severity

- **Critical**: [Count and brief description]
- **High**: [Count and brief description]
- **Medium**: [Count and brief description]
- **Low**: [Count and brief description]

## 📁 Issues by Category

### [Category/Rule Name]
- **File**: `path/to/file`
  - Line [X]: [Error description]
  - Suggested fix: [How to resolve]

[Repeat for other categories]

## 🎯 Priority Recommendations

1. [Most critical issue to address first]
2. [Second priority]
3. [Third priority]

## 📋 Linter Output Excerpt

<details>
<summary>Click to expand linter log excerpt</summary>

```
[Include an excerpt of the linter output here — at most ~150 lines. The full log is available as the `super-linter-log` artifact on the workflow run.]
```

</details>

## 🔗 References

- [Link to workflow run](${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }})
- [Super Linter Documentation](https://github.com/super-linter/super-linter)
```

## Important Guidelines

- **Be concise but thorough**: Focus on actionable insights
- **Prioritize issues**: Not all linting errors are equal
- **Provide context**: Explain why each type of error matters for documentation quality
- **Suggest fixes**: Give practical recommendations
- **Use proper formatting**: Make the issue easy to read and navigate
- **If no errors found**: Call `noop` celebrating clean markdown

**Important**: Always call exactly one safe-output tool before finishing (`create_issue` or `noop`).

```json
{"noop": {"message": "No action needed: [brief explanation of what was analyzed and why]"}}
```
