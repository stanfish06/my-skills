---
name: skills-hub
description: Browse and install community skills from the BioClaw Skills Hub. Use when a user's task is not covered by built-in skills, or when the user asks about available skills, advanced workflows, or specialized analysis pipelines. Triggers on "skills hub", "more skills", "install skill", "community skills", "find a skill for".
---

# Skills Hub Browser

> [!note] Vault audit 2026-07-24 — USE-10
> Use this to browse/install bioinformatics community skills from the BioClaw Skills Hub; for discovering skills across the general skill ecosystem use `find-skills`. Distinguishing axis: bio/BioClaw domain vs general ecosystem.

Search, browse, and install community-contributed skills from the [BioClaw Skills Hub](https://github.com/zongtingwei/Bioclaw_Skills_Hub).

The Hub contains 70+ specialized bioinformatics skills organized into domains. Skills downloaded from the Hub are cached locally so they persist for the rest of the session.

## When to Use

- User requests an analysis not covered by the built-in skills listed in your system prompt
- User asks "what other skills are available" or "do you have a skill for X"
- User needs a specialized pipeline (e.g., protein design, EHR analysis, spatial transcriptomics workflows beyond the built-in)

## Hub Structure

The Hub organizes skills into these domains:

| Domain | Examples |
|--------|----------|
| `core-bioinformatics` | alignment-and-mapping, read-qc, sequence-io, database-access |
| `transcriptomics` | bulk-rna-expression, differential-expression |
| `single-cell-and-spatial` | scrna-preprocessing, spatial-transcriptomics, cell-annotation |
| `epigenomics-and-regulation` | atac-seq, chip-seq, dna-methylation |
| `genomics-and-variation` | variant-calling, genome-assembly, long-read-genomics |
| `metagenomics-and-microbiome` | metagenomics, phylogenetics, microbial-community |
| `proteomics-and-metabolomics` | mass-spec, metabolomics |
| `multi-omics-and-systems` | multi-omics-integration, pathway-analysis |
| `protein-design` | alphafold2-multimer, proteinmpnn, rfdiffusion, boltzgen (nested under `protein-design/skills/`) |
| `ehr-analysis` | electronic health record analysis (single `SKILL.md`, no per-skill directory) |

## How to Execute

### Step 1: Fetch the taxonomy (skill index)

```bash
curl -sL "https://raw.githubusercontent.com/zongtingwei/Bioclaw_Skills_Hub/main/catalog/taxonomy.yaml"
```

This returns the full skill catalog organized by domain. Use it to find the skill name that matches the user's need.

### Step 2: Resolve the SKILL.md path

Domains do not share one on-disk layout, so never build the path from a template.
`protein-design` nests its skills under `skills/protein-design/skills/<skill>/SKILL.md`
and `ehr-analysis` is a single file at `skills/ehr-analysis/SKILL.md`, while the other
eight domains use `skills/<domain>/<skill>/SKILL.md`. Read the real path out of the
repository tree:

```bash
curl -sL "https://api.github.com/repos/zongtingwei/Bioclaw_Skills_Hub/git/trees/main?recursive=1" \
  | python3 -c "
import json, sys
tree = json.load(sys.stdin)
paths = [t['path'] for t in tree['tree'] if t['path'].endswith('SKILL.md')]
for p in paths:
    print(p)
"
```

Filter that list for the skill you want. To list the skills in one domain, keep the
paths under `skills/<domain>/` and take the directory that immediately precedes
`SKILL.md`.

### Step 3: Download and read a skill

```bash
# SKILL_PATH is the repo-relative path resolved in Step 2, e.g.
#   skills/single-cell-and-spatial/cell-annotation/SKILL.md
#   skills/protein-design/skills/alphafold2-multimer/SKILL.md
#   skills/ehr-analysis/SKILL.md
SKILL_PATH="<path from step 2>"
SKILL="<skill-name>"
CACHE_DIR="/workspace/group/.hub-skills/${SKILL}"
mkdir -p "${CACHE_DIR}"
curl -fsSL "https://raw.githubusercontent.com/zongtingwei/Bioclaw_Skills_Hub/main/${SKILL_PATH}" \
  -o "${CACHE_DIR}/SKILL.md"
```

`curl -f` makes a 404 fail loudly instead of caching GitHub's error page as the skill.

Then read the downloaded skill:
```
read_file({ file_path: "/workspace/group/.hub-skills/<skill-name>/SKILL.md" })
```

### Step 4: Install dependencies (if needed)

Some Hub skills require extra Python packages. Check the SKILL.md for a "Preferred Tools" or "Dependencies" section. Install with:

```bash
pip install <package> --quiet 2>/dev/null
```

### Step 5: Execute the skill

Follow the workflow described in the downloaded SKILL.md, just like any built-in skill.

## Important Notes

- Always check built-in skills first before fetching from the Hub
- Downloaded skills are cached in `/workspace/group/.hub-skills/` for the session
- The Hub is a community resource — skills may reference tools not installed in the container; install them with pip/apt as needed
- If GitHub is unreachable, inform the user and suggest using built-in skills instead
