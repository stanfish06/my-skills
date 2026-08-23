---
title: complexa-setup
aliases:
  - complexa setup
tags:
  - skill
  - domain/drug-discovery-chem
domain: drug-discovery-chem
status: untried
source: skills/complexa-setup/SKILL.md
created: 2026-06-28
---

# complexa-setup

> [!info] What it does
> First-time setup, environment configuration, and model-weight installation for Proteina-Complexa. Reach for this skill whenever the user says "set up complexa", "install complexa", "configure my environment file", "first-time setup", "what models do I have installed", "what's in my environment file", "download model weights", "download Complexa / AF2 / RF3 / ProteinMPNN / LigandMPNN / ESM2 / ESMFold checkpoints", "preflight my GPU", "verify environment", "complexa init", "complexa download", "complexa download --status", "complexa validate env", or any time a fresh checkout needs to be made runnable. This is the first skill to run on a new clone — it drives `complexa init`, `complexa download`, and `complexa validate env` end-to-end, edits the required `.env` keys, picks the right runtime (UV vs Docker), and emits a replayable setup artifact.

**Source:** [skills/complexa-setup/SKILL.md](../../../skills/complexa-setup/SKILL.md)  ·  **Domain:** [Drug Discovery, Cheminformatics & Structural Biology](../../maps/drug-discovery-chem.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [docker](../../notes/software-dev/docker.md) — Containerizing and shipping applications with Docker — writing efficient Dockerfiles (multi-stage builds, layer caching, small/secure images), docker compose for multi-service local...
- [setup](../../notes/vault-meta/setup.md) — Verify Daloopa MCP connection and show available skills

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

