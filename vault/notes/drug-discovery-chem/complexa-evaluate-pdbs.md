---
title: complexa-evaluate-pdbs
aliases:
  - complexa evaluate pdbs
tags:
  - skill
  - domain/drug-discovery-chem
domain: drug-discovery-chem
status: untried
source: skills/complexa-evaluate-pdbs/SKILL.md
created: 2026-06-28
---

# complexa-evaluate-pdbs

> [!info] What it does
> Standalone evaluation of an existing PDB directory with Proteina-Complexa. Use when the user wants to "evaluate PDB files", "re-fold these designs", "compute interface pAE", "compute i_pLDDT for a folder", "run AF2 / RF3 / ESMFold on my designs", "score binder candidates", "designability of this folder", "scRMSD for designs", "motif RMSD for these PDBs", "complexa analysis", "complexa evaluate from a PDB directory", "evaluate from pdb dir", or to score third-party outputs (BindCraft, AlphaProteo, RFdiffusion, hand-curated decoys). Picks the correct evaluate_*.yaml config, wires ++dataset.pdb_dir and the folding backend, runs the evaluate → analyze chain, parses the result CSV, and reports pass-rates against the right result_type thresholds.

**Source:** [skills/complexa-evaluate-pdbs/SKILL.md](../../../skills/complexa-evaluate-pdbs/SKILL.md)  ·  **Domain:** [Drug Discovery, Cheminformatics & Structural Biology](../../maps/drug-discovery-chem.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

_None auto-detected. Add your own links here, e.g. `[[scanpy]]`._

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes

