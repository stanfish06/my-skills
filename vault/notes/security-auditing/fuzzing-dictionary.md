---
title: fuzzing-dictionary
aliases:
  - fuzzing dictionary
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/fuzzing-dictionary/SKILL.md
created: 2026-06-09
---

# fuzzing-dictionary

> [!info] What it does
> Builds and applies fuzzing dictionaries so a fuzzer can produce the keywords, magic bytes, and tokens a target expects. Covers extracting tokens from source, headers, binaries, and specifications, dictionary syntax, and wiring one into libFuzzer or AFL++. Use when fuzzing a parser, protocol, or file format, when coverage stalls at input validation, or when a target compares against fixed strings.

**Source:** [skills/fuzzing-dictionary/SKILL.md](../../../skills/fuzzing-dictionary/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [libfuzzer](../../notes/security-auditing/libfuzzer.md) — Sets up and runs libFuzzer, the coverage-guided fuzzer built into LLVM, on C/C++ code that compiles with Clang
- [validation](../../notes/software-dev/validation.md) — Use when Codex is already in the validation phase of a security scan or the user explicitly asks to determine whether one or more candidate security findings are valid

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
