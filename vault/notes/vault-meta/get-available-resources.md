---
title: get-available-resources
aliases:
  - get available resources
  - GPUs
tags:
  - skill
  - domain/vault-meta
domain: vault-meta
status: untried
source: skills/get-available-resources/SKILL.md
created: 2026-06-09
---

# get-available-resources

> [!info] What it does
> Use at the start of computationally intensive scientific task to detect and report available system resources (CPU cores, GPUs, memory, disk space). It creates a JSON file with resource information and strategic recommendations that inform computational approach decisions such as whether to use parallel processing (joblib, multiprocessing), out-of-core computing (Dask, Zarr), GPU acceleration (PyTorch, JAX), or memory-efficient strategies. Use this skill before running analyses, training models, processing large datasets, or any task where resource constraints matter.

**Source:** [skills/get-available-resources/SKILL.md](../../../skills/get-available-resources/SKILL.md)  ·  **Domain:** [Vault, Skills & Workflow Meta](../../maps/vault-meta.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [dask](../../notes/data-science-compute/dask.md) — Distributed computing for larger-than-RAM pandas/NumPy workflows
- [start](../../notes/vault-meta/start.md) — Use when starting Zoom work

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
