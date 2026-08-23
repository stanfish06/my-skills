---
title: property-based-testing
aliases:
  - property based testing
tags:
  - skill
  - domain/security-auditing
domain: security-auditing
status: untried
source: skills/property-based-testing/SKILL.md
created: 2026-06-09
---

# property-based-testing

> [!info] What it does
> Writes, reviews, and debugs property-based tests — Hypothesis, fast-check, proptest, jqwik, rapid, and Echidna or Medusa for Solidity invariants. Use whenever tests should cover a whole input domain instead of a hand-picked list of examples: encode/decode and serialize/deserialize pairs, parsers, canonicalizers and normalizers, validators, numeric and Decimal types, comparators and sort order, data structures, and smart-contract state invariants. Also use when adding cases to an existing @given, fast-check, or proptest suite, when judging whether existing property tests assert anything real, and when a generator has shrunk a counterexample and you need to tell a wrong property from a genuine bug. Not for coverage-guided binary fuzzing (libFuzzer, AFL), mutation-testing campaigns, static analysis, benchmarking, or end-to-end UI tests.

**Source:** [skills/property-based-testing/SKILL.md](../../../skills/property-based-testing/SKILL.md)  ·  **Domain:** [Security & Auditing](../../maps/security-auditing.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [libfuzzer](../../notes/security-auditing/libfuzzer.md) — Coverage-guided fuzzer built into LLVM for C/C++ projects
- [mutation-testing](../../notes/software-dev/mutation-testing.md) — Configures mewt or muton mutation testing campaigns — scopes targets, tunes timeouts, and optimizes long-running runs

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
