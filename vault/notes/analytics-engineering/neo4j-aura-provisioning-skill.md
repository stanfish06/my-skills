---
title: neo4j-aura-provisioning-skill
aliases:
  - neo4j aura provisioning skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-aura-provisioning-skill/SKILL.md
created: 2026-08-23
---

# neo4j-aura-provisioning-skill

> [!info] What it does
> Provisions and manages Neo4j Aura instances via CLI (aura-cli v1.7+) or REST API. Use when creating, pausing, resuming, resizing, or deleting AuraDB Free/Professional/Business Critical/VDC instances; downloading credentials; scripting CI/CD pipelines; polling async status; or using the Terraform neo4j/neo4j-aura provider. Covers auth setup (client credentials OAuth2), credential lifecycle (download once — never recoverable), instance type selection, region codes, and Python provisioning scripts. Does NOT handle Cypher queries — use neo4j-cypher-skill. Does NOT cover Graph Data Science algorithms — use neo4j-gds-skill or neo4j-aura-graph-analytics-skill. Does NOT cover neo4j-admin/cypher-shell — use neo4j-cli-tools-skill.

**Source:** [skills/neo4j-aura-provisioning-skill/SKILL.md](../../../skills/neo4j-aura-provisioning-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [auth](../../notes/security-auditing/auth.md) — Authentication integration guidance — Clerk (native Vercel Marketplace), Descope, and Auth0 setup for Next.js applications
- [neo4j-aura-agent-skill](../../notes/analytics-engineering/neo4j-aura-agent-skill.md) — Manages Neo4j Aura Agents via the v2beta1 REST API — create, list, get, update, delete, and invoke Aura agents backed by an AuraDB instance
- [neo4j-aura-graph-analytics-skill](../../notes/analytics-engineering/neo4j-aura-graph-analytics-skill.md) — Serverless Aura Graph Analytics (AGA) GDS Sessions — covers GdsSessions, AuraGraphDataScience, AuraAPICredentials, DbmsConnectionInfo, SessionMemory, get_or_create, remote graph...
- [neo4j-cli-tools-skill](../../notes/analytics-engineering/neo4j-cli-tools-skill.md) — Use when working with Neo4j command-line tools — neo4j-cli (modern unified CLI — Cypher via Bolt, schema inspection, Aura management, Docker containers, credential management, agent...
- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-gds-skill](../../notes/analytics-engineering/neo4j-gds-skill.md) — Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph...
- [neo4j-mcp-skill](../../notes/analytics-engineering/neo4j-mcp-skill.md) — Use when installing, configuring, or troubleshooting the official Neo4j MCP server (neo4j/mcp) — connecting Claude Code, Claude Desktop, Cursor, Windsurf, VS Code, Kiro, or other...
- [setup](../../notes/vault-meta/setup.md) — Verify Daloopa MCP connection and show available skills
- [terraform](../../notes/cloud-devops/terraform.md) — Terraform and OpenTofu infrastructure-as-code (IaC) — declare cloud/SaaS resources in HCL, manage state with remote backends and locking, author and consume modules, and run the...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
