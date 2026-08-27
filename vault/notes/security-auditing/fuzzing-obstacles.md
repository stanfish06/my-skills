---
title: fuzzing-obstacles
aliases:
  - fuzzing obstacles
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/fuzzing-obstacles/SKILL.md
created: 2026-06-09
---

# fuzzing-obstacles

> [!info] What it does
> Patches past the barriers that stop a fuzzer making progress — checksum and hash verification, magic-value validation, time-based seeds, and other non-deterministic global state. Covers locating the blocking check, neutering it behind a fuzzing build flag, and avoiding the false positives a patch can introduce. Use when a fuzzer is stuck at validation, when coverage shows large regions behind a checksum, or when valid inputs are impractical to generate.

**Source:** [skills/fuzzing-obstacles/SKILL.md](../../../skills/fuzzing-obstacles/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [validation](../../notes/software-dev/validation.md) — Use when Codex is already in the validation phase of a security scan or the user explicitly asks to determine whether one or more candidate security findings are valid
- [verification](../../notes/software-dev/verification.md) — Full-story verification — infers what the user is building, then verifies the complete flow end-to-end: browser → API → data → response

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
