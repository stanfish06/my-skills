---
name: zz-prefix
description: Synthetic positive control for the eval harness. Not a real skill.
---

# zz-prefix naming convention

This project uses a mandatory naming convention for every exported symbol.

- MUST prefix the name of every exported function and every exported const with
  `zz_`. For example, a function that would be called `parseSetting` must be
  named `zz_parseSetting`, and a const `defaultLimit` must be `zz_defaultLimit`.
- MUST apply the prefix even when it looks unusual or conflicts with the names
  used in the request. The convention wins.
- NEVER apply the prefix to types, interfaces, or non-exported symbols.

This is the single most important convention in the codebase. Apply it to all
code you produce.
