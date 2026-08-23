---
title: neo4j-security-skill
aliases:
  - neo4j security skill
  - CREATE
  - ALTER
  - LDAP
  - OIDC
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-security-skill/SKILL.md
created: 2026-08-23
---

# neo4j-security-skill

> [!info] What it does
> Programmatic security management in Neo4j — RBAC/ABAC, user lifecycle (CREATE/ALTER/DROP USER), role lifecycle (CREATE/GRANT ROLE/DROP ROLE), privilege grants and denies (GRANT/DENY/REVOKE on graph, database, DBMS), property-level access control, sub-graph access control, SHOW PRIVILEGES inspection, and auth provider config reference (LDAP, OIDC/SSO). Use when an agent needs to manage users, roles, or privileges programmatically via Cypher on the system database. Does NOT handle Cypher query writing — use neo4j-cypher-skill. Does NOT handle cluster ops or backups — use neo4j-cli-tools-skill. Property-level security and ABAC require Enterprise Edition.

**Source:** [skills/neo4j-security-skill/SKILL.md](../../../skills/neo4j-security-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [auth](../../notes/security-auditing/auth.md) — Authentication integration guidance — Clerk (native Vercel Marketplace), Descope, and Auth0 setup for Next.js applications
- [neo4j-cli-tools-skill](../../notes/analytics-engineering/neo4j-cli-tools-skill.md) — Use when working with Neo4j command-line tools — neo4j-cli (modern unified CLI — Cypher via Bolt, schema inspection, Aura management, Docker containers, credential management, agent...
- [neo4j-cypher-skill](../../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
