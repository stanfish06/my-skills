---
name: cell-communication
description: Cell-cell / ligand-receptor communication analysis for single-cell data using LIANA+ (recommended consensus default), CellPhoneDB, CellChat (R), and squidpy's ligrec. Use for inferring cell-cell communication, ligand-receptor pairs, source->target signaling from an annotated .h5ad. Trigger terms - "cell-cell communication", "ligand-receptor", "CellPhoneDB", "CellChat", "LIANA", "cell interaction", "ligrec".
license: MIT
metadata: {"version": "1.0", "skill-author": "vault-audit"}
---

# cell-communication

## Overview

Cell-cell communication (CCC) inference predicts which cell types signal to which
others by scoring co-expression of known ligand-receptor (L-R) pairs across
annotated cell populations. Input is an **annotated `.h5ad`** with cell-type labels
in `adata.obs` and log-normalized expression; output is a ranked table of
`source -> target` L-R interactions.

Tool landscape (2026):

- **LIANA+** (`liana`, Python) - **recommended default.** Runs multiple methods
  (CellPhoneDB, NATMI, Connectome, logFC, SingleCellSignalR, CellChat,
  geometric mean) and returns a robust **consensus rank aggregate**. scverse-native
  (AnnData/MuData), also handles spatial and multi-condition data.
- **CellPhoneDB** (v5, Python) - permutation-test statistical method; also DEG-based
  and receptor-activity (CellSign) modes. LIANA reimplements its core scoring.
- **CellChat** (v2, **R only** - GitHub) - pathway-level signaling
  probabilities plus strong built-in visualization (chord, hierarchy, river plots).
  Use from R/Seurat; not a Python package.
- **squidpy `sq.gr.ligrec`** (Python) - CellPhoneDB-style permutation test inside the
  scverse spatial stack; convenient when already in squidpy. For spatially-resolved
  proximity use the `spatialdata-squidpy` skill.

## Installation

LIANA+ requires **Python 3.10-3.13**. Latest release: **liana 1.8.1** (July 2026).

```bash
uv pip install liana            # core (AnnData/scanpy)
uv pip install "liana[extras]"  # tensor-cell2cell / MOFA+ multi-condition tools
```

CellChat is R-based (install in R):
```r
devtools::install_github("jinworks/CellChat")
```

## Core workflow (LIANA on an h5ad)

```python
import scanpy as sc
import liana as li

# 1. Load an ANNOTATED, log-normalized AnnData (cell types already assigned).
adata = sc.read_h5ad("annotated.h5ad")
# adata.X should be log1p-normalized counts (NOT raw counts, NOT scaled/z-scored).
# adata.obs["cell_type"] holds the labels to group by.

# 2. Run the consensus method (runs several methods, aggregates ranks).
li.mt.rank_aggregate(
    adata,
    groupby="cell_type",       # cell-type column in adata.obs
    resource_name="consensus", # human; use "mouseconsensus" for mouse
    expr_prop=0.1,             # drop L-R where either gene is expressed in <10% of a cluster
    use_raw=False,             # read adata.X; set True to read adata.raw
    verbose=True,
)

# 3. Results are a DataFrame in adata.uns["liana_res"].
res = adata.uns["liana_res"]
print(res.columns.tolist())
# source, target, ligand_complex, receptor_complex, magnitude_rank, specificity_rank, ...

# 4. Top robust interactions: lower ranks = more relevant. Sort/filter, then inspect.
top = (res[res["specificity_rank"] <= 0.05]
       .sort_values("magnitude_rank")
       .head(20))
print(top[["source", "target", "ligand_complex", "receptor_complex",
           "magnitude_rank", "specificity_rank"]])

# 5a. Dotplot: colour = magnitude (expression strength), size = specificity.
li.pl.dotplot(
    adata=adata,
    colour="magnitude_rank",
    size="specificity_rank",
    inverse_colour=True,   # invert so stronger interactions look "hotter"
    inverse_size=True,     # invert so more-specific interactions look larger
    source_labels=["Monocyte", "T cell"],   # subset senders (optional)
    target_labels=["B cell", "NK"],         # subset receivers (optional)
    top_n=15,
    orderby="magnitude_rank",
    orderby_ascending=True,
    filter_fun=lambda x: x["specificity_rank"] <= 0.05,
    figure_size=(9, 7),
)

# 5b. Chord / network view: circular source->target network of interactions.
li.pl.circle_plot(adata=adata, groupby="cell_type")
# li.pl.tileplot(...) is another summary view.

# List options if unsure of names:
li.mt.show_methods()      # individual methods (cellphonedb, natmi, cellchat, ...)
li.rs.show_resources()    # available L-R resources (consensus, mouseconsensus, ...)
```

Run an individual method instead of the consensus with e.g. `li.mt.cellphonedb(adata, groupby="cell_type", ...)`; it writes the same `adata.uns["liana_res"]`.

## Gotchas / best practices

- **Annotate first.** CCC is only meaningful over trustworthy cell-type labels.
  Do QC, clustering, and annotation before this step (see related skills). Garbage or
  mixed clusters produce meaningless L-R calls.
- **Feed log-normalized data, not raw counts and not scaled data.** LIANA reads
  `adata.X` (with `use_raw=False`) or `adata.raw`; it expects `normalize_total` +
  `log1p` values. Z-scored/`sc.pp.scale`d matrices give wrong scores.
- **Magnitude vs specificity - interpret both.** *Magnitude* reflects how strongly
  the L-R pair is co-expressed in a `source->target` pair (is the interaction present
  and how strong). *Specificity* reflects how uniquely that pair stands out for those
  two cell types versus all other pairs. A strong-magnitude interaction can be
  non-specific (housekeeping ligands). Prioritize hits that are both high-magnitude
  and high-specificity. In the aggregate, `magnitude_rank`/`specificity_rank` are
  aggregated ranks in [0,1] where **lower = more relevant**; sort ascending and filter
  `specificity_rank <= 0.05`.
- **`source -> target` is directional.** `source` = the ligand-expressing (sender)
  cell type; `target` = the receptor-expressing (receiver). A->B and B->A are distinct.
- **Human vs mouse resources.** `resource_name="consensus"` is human; use
  `"mouseconsensus"` for mouse. For other species or a mixed reference, translate via
  orthologs with `li.rs.get_hcop_orthologs()` / `li.rs.translate_resource()`. Never run
  a human resource on mouse gene symbols.
- **Comparing conditions/batches.** Do not just pool samples. Run per sample/condition
  and compare, or use LIANA+'s multi-sample tools (`by_sample` scoring, plus
  tensor-cell2cell / MOFA+ under `li.multi` in the `[extras]` install) to decompose
  condition-specific communication. Confounded batches inflate apparent signaling; keep
  batch structure explicit. See the LIANA+ docs for the current multi-condition API.
- **`expr_prop` and small clusters.** Very small cell-type clusters and the
  `expr_prop` threshold (default 0.1) heavily affect which pairs survive; report the
  threshold and cluster sizes used.
- **Don't over-invent signatures.** For exact/advanced arguments (spatial `bivariate`,
  `MistyData`, multi-view) consult the LIANA+ docs: https://liana-py.readthedocs.io
  CellChat's chord/pathway plots and CellPhoneDB v5 modes live in their own docs.

## Use this vs related skills

Run `scanpy` / `scrna-preprocessing-clustering` (QC, normalize, cluster) and
`cell-annotation` (assign cell types) **first** to produce the annotated `.h5ad`; use
`spatialdata-squidpy` when you need spatially-resolved ligand-receptor proximity rather
than label-based CCC.
