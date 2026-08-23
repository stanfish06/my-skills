---
title: assistant-mcp
aliases:
  - assistant mcp
tags:
  - skill
  - domain/cloud-devops
domain: cloud-devops
status: untried
source: skills/assistant-mcp/SKILL.md
created: 2026-08-23
---

# assistant-mcp

> [!info] What it does
> Connect AI coding agents (Claude Code, Cursor, VS Code, OpenAI Codex) to Grafana Cloud via the `mcp-grafana` Model Context Protocol server. Installs the server with `go install`, generates a Grafana service-account token, wires `~/.claude/settings.json` or `~/.cursor/mcp.json` with the `command` + `env` block, runs `--disable-write` for safer read-only sessions, switches to SSE transport for team-shared / VS Code setups, and verifies with `/mcp` + a `list_datasources` round-trip. Use when connecting Claude Code to Grafana, setting up MCP for Grafana, configuring the Grafana MCP server, using Grafana tools in Cursor/VS Code, querying Grafana from an AI agent, sharing the MCP server across a team — even when the user says "give my agent Grafana access", "let Claude see my metrics", or "Cursor + Grafana" without saying "MCP".

**Source:** [skills/assistant-mcp/SKILL.md](../../../skills/assistant-mcp/SKILL.md)  ·  **Domain:** [Cloud, Infra & MLOps](../../maps/cloud-devops.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

_None auto-detected. Add your own links here, e.g. `[[scanpy]]`._

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
