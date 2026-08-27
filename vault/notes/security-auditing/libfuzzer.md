---
title: libfuzzer
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/libfuzzer/SKILL.md
created: 2026-06-09
---

# libfuzzer

> [!info] What it does
> Sets up and runs libFuzzer, the coverage-guided fuzzer built into LLVM, on C/C++ code that compiles with Clang. Covers harness structure, -fsanitize=fuzzer builds, corpus and dictionary management, sanitizer integration, and campaign triage. Use when writing or debugging an LLVMFuzzerTestOneInput harness, starting fuzzing on a C/C++ library, choosing between libFuzzer and AFL++, or working out why a libFuzzer run finds nothing.

**Source:** [skills/libfuzzer/SKILL.md](../../../skills/libfuzzer/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [aflpp](../../notes/security-auditing/aflpp.md) — Sets up and runs AFL++ for multi-core fuzzing of C/C++ projects built with afl-clang-fast or afl-gcc-fast
- [atheris](../../notes/security-auditing/atheris.md) — Sets up and runs Atheris, the coverage-guided Python fuzzer built on libFuzzer
- [fuzzing-dictionary](../../notes/security-auditing/fuzzing-dictionary.md) — Builds and applies fuzzing dictionaries so a fuzzer can produce the keywords, magic bytes, and tokens a target expects
- [property-based-testing](../../notes/security-auditing/property-based-testing.md) — Writes, reviews, and debugs property-based tests — Hypothesis, fast-check, proptest, jqwik, rapid, and Echidna or Medusa for Solidity invariants
- [triage](../../notes/software-dev/triage.md) — Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
