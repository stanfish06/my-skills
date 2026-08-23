---
title: neo4j-aura-agent-skill
aliases:
  - neo4j aura agent skill
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/neo4j-aura-agent-skill/SKILL.md
created: 2026-08-23
---

# neo4j-aura-agent-skill

> [!info] What it does
> Manages Neo4j Aura Agents via the v2beta1 REST API — create, list, get, update, delete, and invoke Aura agents backed by an AuraDB instance. Use when configuring Aura Agent tools (CypherTemplate, SimilaritySearch, Text2Cypher), setting system prompts, deploying agents to REST or MCP endpoints, or invoking agents with natural language queries. Covers OAuth2 auth, organization/project scoping, tool parameter schemas, and InvokeAgentResponse format. Does NOT cover AuraDB instance provisioning — use neo4j-aura-provisioning-skill. Does NOT cover vector index creation — use neo4j-vector-index-skill.

**Source:** [skills/neo4j-aura-agent-skill/SKILL.md](../../../skills/neo4j-aura-agent-skill/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [auth](../../notes/security-auditing/auth.md) — Authentication integration guidance — Clerk (native Vercel Marketplace), Descope, and Auth0 setup for Next.js applications
- [neo4j-aura-provisioning-skill](../../notes/analytics-engineering/neo4j-aura-provisioning-skill.md) — Provisions and manages Neo4j Aura instances via CLI (aura-cli v1.7+) or REST API
- [neo4j-vector-index-skill](../../notes/analytics-engineering/neo4j-vector-index-skill.md) — Create and manage Neo4j vector indexes, run vector similarity search (ANN/kNN), store embeddings on nodes or relationships, use SEARCH clause (Neo4j 2026.01+, preferred) or...

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
