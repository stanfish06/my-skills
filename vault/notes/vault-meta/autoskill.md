---
title: autoskill
tags:
  - skill
  - domain/vault-meta
domain: vault-meta
status: untried
source: skills/autoskill/SKILL.md
created: 2026-06-09
---

# autoskill

> [!info] What it does
> Observe the user's screen via screenpipe, detect repeated research workflows, match them against existing scientific-agent-skills, and draft new skills (or composition recipes that chain existing ones) for the patterns not yet covered. Use when the user asks to analyze their recent work and propose skills based on what they actually do. Requires the screenpipe daemon (https://github.com/screenpipe/screenpipe) running locally on port 3030 — the skill has no other data source and will refuse to run if screenpipe is unreachable. All detection runs locally; only redacted cluster summaries reach the LLM.

**Source:** [skills/autoskill/SKILL.md](../../../skills/autoskill/SKILL.md)  ·  **Domain:** [Vault, Skills & Workflow Meta](../../maps/vault-meta.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [github](../../notes/software-dev/github.md) — Triage and orient GitHub repository, pull request, and issue work through the connected GitHub app
- [research](../../notes/software-dev/research.md) — Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

> [!warning] Vault audit 2026-07-24 — MNT-10
> References a superseded model id `claude-opus-4-7` and hardcodes a stale sibling count ("135 skills") in two places — both are drift. Use a current model id and don't trust the hardcoded count (the vault has ~1250 skills).
> _Remote-managed skill — the durable fix belongs upstream; this wrapper note is the local record._

> [!note] Vault audit 2026-07-24 — USE-10
> Use this to auto-draft skills from repeated workflows observed on your screen (screenpipe); to hand-scaffold a new skill from a spec use `skill-builder`, to eval-tune an existing skill use `clawpathy-autoresearch`, to package a plugin bundle use `plugin-creator`. Distinguishing axis: authoring mode (screen-observation vs manual scaffold vs eval-tuning vs plugin packaging).
