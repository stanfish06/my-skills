#!/usr/bin/env python3
"""Build the human-navigation layer for the skills vault.

Generates, for every skill folder in skills/ that contains a SKILL.md:
  - vault/notes/<domain>/<skill>.md
                          a wrapper note, grouped by domain (safe to hand-edit;
                          the "Personal notes" section AND your frontmatter
                          edits to status / rating / aliases survive a re-run)
  - vault/maps/<domain>.md
                          one map (MOC) note per domain, linking to wrappers
  - vault/index.md        master index linking to maps + every wrapper (A-Z)

Links are emitted as true relative paths so they resolve both in Obsidian and
in plain markdown renderers.

The original skills/<skill>/SKILL.md files are never touched, so an external
skills CLI can keep managing them remotely — skills/ is that CLI's flat
canonical store and must stay a flat list of skill folders. Hand-authored files
(vault/skills.base, vault/recipes/*, README.md, .obsidian/*) are also never
touched.

Usage:  python3 .skill-vault/build.py
"""
import os
import re
import stat
import sys
import tempfile
from datetime import date
from pathlib import Path

from expert_taxonomy import (
    DISPATCHER,
    EXPERT_DOMAIN,
    ExpertTaxonomy,
    ProfileAssignment,
    TaxonomyValidationError,
    load_catalog_profiles,
    load_taxonomy,
)

DEFAULT_VAULT_DIR = Path(__file__).resolve().parents[1]
VAULT_DIR = Path(
    os.environ.get("SKILL_VAULT_ROOT") or DEFAULT_VAULT_DIR
).resolve()
ROOT = str(VAULT_DIR)
# Skill sources live in their own subtree. The Vercel skills CLI treats
# ~/.agents/skills as its flat canonical store, so this directory stays a flat
# list of skill folders and the generated human layer lives beside it, not in
# it. See .skill-vault/README.md.
SKILLS_SUBDIR = "skills"
SKILLS_DIR = VAULT_DIR / SKILLS_SUBDIR
# The generated human layer lives under vault/, keeping the repo root down to a
# handful of entries. Wrapper notes are grouped by domain under vault/notes/ so
# the tree is browsable; maps and the index keep their relative positions.
HUMAN_SUBDIR = "vault"
HUMAN_DIR = VAULT_DIR / HUMAN_SUBDIR
NOTES_DIR = HUMAN_DIR / "notes"
MAPS_DIR = HUMAN_DIR / "maps"
TAXONOMY_PATH = VAULT_DIR / ".skill-vault/scientific-expert-taxonomy.json"
CATALOG_PATH = SKILLS_DIR / "scientific-agents/references/catalog.json"
EXPERT_MAPS_DIR = HUMAN_DIR / "maps/scientific-expert-profiles"
def skills_root():
    """Directory holding the flat list of skill folders.

    Derived from ROOT at call time rather than frozen at import, so overriding
    ROOT relocates skill discovery with it.
    """
    return os.path.join(ROOT, SKILLS_SUBDIR)


def human_root():
    """Directory holding the generated human layer (notes, maps, index)."""
    return os.path.join(ROOT, HUMAN_SUBDIR)


def notes_root():
    """Directory holding the per-skill wrapper notes, grouped by domain."""
    return os.path.join(human_root(), "notes")


def note_path(skill, key):
    """Absolute path of a skill's wrapper note."""
    return os.path.join(notes_root(), key, wrapper_filename(skill))


def note_link(skill, domain_by_skill, prefix=""):
    """Link to a skill's wrapper note from an emitter `prefix` above vault/.

    Maps and the index keep their positions relative to each other, so only
    links that point *at a note* need the notes/<domain>/ component.
    """
    key = domain_by_skill.get(skill, "uncategorized")
    return f"{prefix}notes/{key}/{wrapper_filename(skill)}"


TODAY = date.today().isoformat()
# one-time: regenerate aliases even if a wrapper already has an aliases key.
# Do NOT use after you have hand-curated aliases.
FORCE_ALIASES = "--force-aliases" in sys.argv
# delete root wrapper notes whose skill folder no longer exists (orphans).
PRUNE = "--prune" in sys.argv
# rewrite .obsidian/graph.json color groups + filter (run with the graph CLOSED,
# or Obsidian will overwrite it from memory).
GRAPH = "--graph" in sys.argv

# distinct graph colors per domain (24-bit RGB ints), keyed by category key.
PALETTE = {
    "genomics-variants": 15079755, "single-cell-rnaseq": 3978315,
    "proteomics-metabolomics": 16769305, "drug-discovery-chem": 4416472,
    "sequence-phylogenetics": 16089649, "bio-databases-platforms": 9510580,
    "clinical-medical": 4379892, "imaging-signals": 15741670, "ml-ai": 12578629,
    "data-science-compute": 16432852, "quantum-physics": 4626832,
    "research-writing": 14466815, "academic-pipelines": 10117924,
    "literature-discovery": 16775880, "documents-office": 8388608,
    "cloud-devops": 11206595, "vault-meta": 8421376, "reasoning-ideation": 117,
    "web-automation-frontend": 5832703, "analytics-engineering": 16753920,
    "security-auditing": 13382451, "software-dev": 1752220,
    "scientific-expert-profiles": 10040012, "matlab-development": 30376,
    "saas-platforms": 14702492,
    "hosting-edge-platforms": 3064502,
    "comms-productivity": 8085503,
    "finance-investment": 3050327,
    "mobile-native-dev": 16747074,
    "game-development": 10233776,
    "data-visualization": 42733,
}
EXPERT_PALETTE = {
    "biology-life-sciences": 0x2CA02C,
    "medicine-health": 0xD62728,
    "chemistry-materials": 0xFF7F0E,
    "physics-astronomy": 0x1F77B4,
    "earth-environmental-sciences": 0x17BECF,
    "agriculture-food-animal-sciences": 0xBCBD22,
    "mathematics-statistics": 0x9467BD,
    "computing-data-science": 0x7F7F7F,
    "engineering-technology": 0x8C564B,
    "social-behavioral-sciences": 0xE377C2,
}
GRAPH_SEARCH = "tag:#skill OR tag:#skill-map OR tag:#recipe OR tag:#moc"
PERSONAL_MARKER = "%% ---8<--- personal notes below are preserved on re-run ---8<--- %%"
GENERATED_EXPERT_MARKER = "generated: scientific-expert-taxonomy"

# acronyms too generic to be useful aliases
STOP = {"API", "CLI", "ML", "AI", "QC", "DNA", "RNA", "GPU", "CPU", "PDF", "CSV",
        "JSON", "HTML", "REST", "SDK", "LLM", "GO", "3D", "2D", "ID", "OS", "UI",
        "NGS", "PCA", "URL", "HTTP", "IO", "OK", "FAIR"}

# Curated human search terms that a fuzzy finder would NOT match as a subsequence
# of the skill id (the only aliases worth hard-coding). Extend freely; on rebuild,
# these only apply to skills that don't yet have an `aliases:` key.
SYNONYMS = {
    "pydeseq2": ["DESeq2"], "rnaseq-de": ["DESeq2", "edgeR"],
    "variant-annotation": ["VEP"], "vcf-annotator": ["VEP"],
    "scanpy": ["single cell", "scRNA-seq"], "scvi-tools": ["scVI", "scANVI"],
    "cellxgene-census": ["CELLxGENE"], "gwas-pipeline": ["PLINK", "REGENIE"],
    "struct-predictor": ["Boltz", "AlphaFold"], "esm": ["ESMFold", "ESM3"],
    "molecular-dynamics": ["OpenMM", "GROMACS"], "proteomics-de": ["MaxQuant", "DIA-NN"],
    "pyopenms": ["OpenMS"], "phylogenetics": ["IQ-TREE", "MAFFT"],
    "phylogenetics-builder": ["IQ-TREE"], "nextflow": ["nf-core"],
    "hf-cli": ["huggingface", "hugging face"], "transformers": ["huggingface"],
    "optimize-for-gpu": ["CUDA", "cuDF"], "methylation-clock": ["epigenetic age"],
    "umap-learn": ["UMAP"], "geopandas": ["GIS"], "pysam": ["samtools"],
    "ncbi-datasets": ["NCBI"], "literature-review": ["systematic review"],
    "consciousness-council": ["panel", "council"], "diffdock": ["docking"],
    "spatialdata-squidpy": ["SpatialData", "Squidpy", "Visium", "Xenium"],
    "harmonypy": ["Harmony"], "scirpy-immune-repertoire": ["Scirpy", "TCR", "BCR"],
    "pybedtools": ["BEDTools"], "colabfold": ["AlphaFold2", "ColabFold"],
    "fragpipe-pyteomics-proteomics": ["FragPipe", "MSFragger", "Pyteomics"],
    "cellpose-stardist-bioimage": ["Cellpose", "StarDist"],
    "monai-medical-imaging-ai": ["MONAI"], "llm-observability-evals": ["Langfuse", "Phoenix"],
    "llm-agent-security-redteam": ["OWASP LLM Top 10", "prompt injection"],
    "xarray-pandera-duckdb": ["xarray", "Pandera", "DuckDB"],
    "ngs-cli-toolkit": ["samtools", "bcftools", "bwa", "GATK", "minimap2", "plink2"],
    "seurat": ["Seurat", "single cell", "scRNA-seq"],
    "optuna": ["hyperparameter optimization", "HPO", "hyperparameter tuning", "Bayesian optimization"],
    "adjusttext": ["adjustText", "ggrepel", "label placement", "text labels"],
    "conda-bioconda": ["conda", "mamba", "micromamba", "Bioconda"],
    "github-actions-ci": ["GitHub Actions", "CI/CD", "workflows"],
    "agentic-workflows": ["gh-aw", "GitHub Agentic Workflows", "Agentics templates", "agentic Actions"],
    "test-driven-development": ["TDD"], "using-git-worktrees": ["git worktree"],
    "worktrunk": ["git worktree", "worktree manager", "parallel agents"],
    "caveman": ["plain language", "ELI5", "dumb it down", "no jargon"],
    "fitness-nutrition": ["meal planning", "workout planner", "calorie counter", "TDEE", "one-rep max"],
    "web-artifacts-builder": ["artifacts", "shadcn"],
    "opensrc": ["source code", "package source", "dependency source", "read library source"],
    "greploop": ["Greptile", "PR review loop"], "check-pr": ["PR review", "merge request", "Greptile"],
    "hunk-review": ["Hunk", "interactive diff review"],
    "ast-grep": ["structural code search", "AST search"],
    "ast-grep-outline": ["code outline", "source structure map"],
    "design-md-library": ["DESIGN.md", "design tokens", "brand style", "look like Stripe", "Stitch"],
    "chaos-engineering": ["resilience testing", "fault injection", "LitmusChaos", "Chaos Mesh"],
}

# ---------------------------------------------------------------------------
# Domain definition: ordered. key -> (title, scope, related_keys, [skills])
# ---------------------------------------------------------------------------
CATEGORIES = [
    ("genomics-variants", "Genomics, Variants & Population Genetics",
     "DNA sequencing, variant calling/annotation, GWAS, fine-mapping, and population & personal genomics.",
     ["single-cell-rnaseq", "sequence-phylogenetics", "bio-databases-platforms", "clinical-medical"],
     ["variant-annotation", "vcf-annotator", "clinical-variant-reporter", "gwas-pipeline",
      "gwas-lookup", "gwas-prs", "gwas-catalog-region-fetch", "fine-mapping",
      "mendelian-randomisation", "ld-1000g-region-compute", "eqtl-catalogue-region-fetch",
      "ukb-ppp-region-fetch", "locuscompare-region-render", "hla-typing", "archaic-introgression",
      "dnasp", "fastreer", "tiledbvcf", "pysam", "wgs-prs", "sample-qc-triage", "equity-scorer",
      "claw-ancestry-pca", "genome-compare", "genome-match", "recombinator", "soul2dna",
      "geniml", "gtars", "polars-bio", "nfcore-sarek-wrapper", "pacsomatic",
      "marker-dominance-mapper", "pybedtools",
      "genomics-workflow-acceleration", "parabricks"]),

    ("single-cell-rnaseq", "Single-Cell, RNA-seq & Functional Genomics",
     "scRNA-seq and bulk RNA-seq pipelines, differential expression, and pathway/network analysis.",
     ["genomics-variants", "proteomics-metabolomics", "sequence-phylogenetics", "bio-databases-platforms"],
     ["scanpy", "anndata", "scvi-tools", "scvelo", "cellxgene-census", "scrna-embedding",
      "scrna-orchestrator", "nfcore-scrnaseq-wrapper", "bulk-rnaseq", "rnaseq-de", "pydeseq2",
      "nfcore-rnaseq-wrapper", "rare-disease-rnaseq", "de-summary", "diff-visualizer", "arboreto",
      "deeptools", "pathway-enricher", "pathway-enrichment", "spatialdata-squidpy",
      "harmonypy", "scirpy-immune-repertoire", "seurat",
      "atac-seq", "chip-seq", "cell-annotation", "scrna-preprocessing-clustering",
      "differential-expression", "pybigwig"]),

    ("proteomics-metabolomics", "Proteomics & Metabolomics",
     "Mass-spec and affinity proteomics, metabolomics spectral analysis, and glycoengineering.",
     ["single-cell-rnaseq", "drug-discovery-chem", "sequence-phylogenetics"],
     ["proteomics-de", "proteomics-clock", "affinity-proteomics", "pyopenms", "matchms",
      "glycoengineering", "fragpipe-pyteomics-proteomics",
      "proteomics", "sec-report", "sds-gel-review"]),

    ("drug-discovery-chem", "Drug Discovery, Cheminformatics & Structural Biology",
     "Small-molecule and protein modeling: cheminformatics, docking, structure prediction, and target validation.",
     ["proteomics-metabolomics", "sequence-phylogenetics", "bio-databases-platforms", "ml-ai"],
     ["rdkit", "datamol", "deepchem", "molfeat", "medchem", "pytdc", "torchdrug", "diffdock",
      "struct-predictor", "esm", "molecular-dynamics", "cobrapy", "rowan", "adaptyv",
      "target-validation-scorer", "drug-repurposing-screen", "depmap", "crispr-screen-triage",
      "omics-target-evidence-mapper", "colabfold", "vmd-mdanalysis-viz",
      "structural-biology",
      "boltz2-nim", "complexa-design", "complexa-evaluate-pdbs", "complexa-setup",
      "complexa-slurm", "complexa-sweep", "complexa-target", "diffdock-nim",
      "drug-discovery-pipeline", "genmol-nim", "kermt-add-cmim-pretrain",
      "kermt-continue-pretrain", "kermt-embed", "kermt-finetune", "kermt-infer",
      "kermt-monitor", "kermt-pretrain-scratch", "kermt-setup", "molmim-nim",
      "nvmolkit-usage", "openfold2-nim", "openfold3-nim", "proteinmpnn-nim",
      "rfdiffusion-nim"]),

    ("sequence-phylogenetics", "Sequence Analysis, NGS & Phylogenetics",
     "Sequence toolkits, read QC/alignment, phylogenetic inference, and sequence-to-function models.",
     ["genomics-variants", "single-cell-rnaseq", "bio-databases-platforms"],
     ["biopython", "bioservices", "gget", "scikit-bio", "phylogenetics", "phylogenetics-builder",
      "etetoolkit", "busco-assessor", "analyze-fasta", "seq-wrangler", "multiqc-reporter",
      "bioqc-mcp", "claw-metagenomics", "ncbi-datasets", "bioconductor-bridge",
      "gi-annotation", "gi-chromatin", "gi-enhancer", "gi-expression", "gi-promoter", "gi-splice",
      "ngs-cli-toolkit",
      "sequence-analysis", "blast-search", "metagenomics",
      "evo2-nim", "msa-search-nim", "msa-structure-prediction-pipeline",
      "cutadapt", "sourmash"]),

    ("bio-databases-platforms", "Bio Databases, Lab & Cloud Platforms",
     "Biomedical databases, knowledge graphs, ELNs, lab automation, and bioinformatics cloud platforms.",
     ["genomics-variants", "sequence-phylogenetics", "clinical-medical", "cloud-devops"],
     ["database-lookup", "primekg", "turingdb-graph", "clinpgx", "article-data-fetcher",
      "ukb-navigator", "galaxy-bridge", "flow-bio", "dnanexus-integration", "latchbio-integration",
      "benchling-integration", "labstep", "labarchive-integration", "omero-integration", "lamindb",
      "protocols-io", "protocolsio-integration", "ginkgo-cloud-lab", "opentrons-integration",
      "pylabrobot", "illumina-bridge", "bigquery-public",
      "query-alphafold", "query-clinvar", "query-ensembl", "query-geo", "query-interpro",
      "query-kegg", "query-opentarget", "query-pdb", "query-reactome", "query-stringdb",
      "query-uniprot", "bio-tools"]),

    ("clinical-medical", "Clinical, Medical & Pharmacogenomics",
     "Clinical reporting, decision support, trials, pharmacogenomics, and patient-facing genomic reports.",
     ["genomics-variants", "bio-databases-platforms", "imaging-signals"],
     ["clinical-reports", "clinical-decision-support", "treatment-plans", "clinical-trial-finder",
      "wes-clinical-report-en", "wes-clinical-report-es", "pharmgx-reporter", "nutrigx-advisor",
      "drug-photo", "pyhealth", "iso-13485-certification", "profile-report", "methylation-clock",
      "fitness-nutrition"]),

    ("imaging-signals", "Imaging, Microscopy & Biosignals",
     "Microscopy and pathology images, medical imaging, electrophysiology, flow cytometry, and biosignals.",
     ["clinical-medical", "ml-ai", "bio-databases-platforms"],
     ["cell-detection", "histolab", "pathml", "pydicom", "neuropixels-analysis", "flowio",
      "neurokit2", "bids", "imaging-data-commons", "cellpose-cell-segmentation",
      "cellpose-stardist-bioimage", "monai-medical-imaging-ai", "napari-viz"]),

    ("ml-ai", "Machine Learning & AI",
     "General ML/DL frameworks, model interpretability, RL, graph learning, and scientific model hubs.",
     ["data-science-compute", "drug-discovery-chem", "cloud-devops"],
     ["scikit-learn", "pytorch-lightning", "transformers", "shap", "stable-baselines3", "pufferlib",
      "pufferlib-v2", "pufferlib-v3", "torch-geometric", "umap-learn", "aeon", "timesfm-forecasting", "hugging-science",
      "optuna", "cuequivariance", "crewai",
      # pydantic/skills — Pydantic AI agents + harness
      "building-pydantic-ai-agents", "pydantic-ai-harness"]),

    ("data-science-compute", "Data Science, Stats & Scientific Computing",
     "DataFrames, big-data tooling, statistics, optimization, simulation, geospatial, and plotting.",
     ["ml-ai", "quantum-physics", "research-writing", "analytics-engineering",
      "matlab-development"],
     ["polars", "dask", "vaex", "zarr-python", "networkx", "sympy", "statsmodels",
      "statistical-analysis", "scikit-survival", "pymc", "pymoo", "simpy", "geomaster", "geopandas",
      "exploratory-data-analysis", "optimize-for-gpu", "usfiscaldata", "matplotlib", "seaborn",
      "adjusttext", "build-complexheatmaps",
      "xarray", "pandera-validation", "xarray-pandera-duckdb", "attach-db", "duckdb-docs",
      "install-duckdb", "query", "read-file", "paraview", "ttk-viz"]),

    ("quantum-physics", "Quantum, Physics & Materials",
     "Quantum computing frameworks, open quantum systems, astronomy, fluid dynamics, and materials science.",
     ["data-science-compute", "ml-ai"],
     ["qiskit", "cirq", "pennylane", "qutip", "astropy", "fluidsim", "pymatgen"]),

    ("research-writing", "Scientific Writing, Figures & Publishing",
     "Manuscript writing, figures and schematics, posters/slides, reference management, and pre-submission review.",
     ["academic-pipelines", "literature-discovery", "documents-office", "reasoning-ideation",
      "web-automation-frontend"],
     ["scientific-writing", "scientific-visualization", "scientific-slides", "scientific-schematics",
      "cns-plot",
      "scientific-critical-thinking", "citation-management", "peer-review", "research-grants",
      "venue-templates", "latex-posters", "pptx-posters", "paper-2-web", "markdown-mermaid-writing",
      "figure-designer", "scholar-evaluation", "tech-paper-template", "benchmark-paper-template",
      "intro-drafter", "pre-submission-reviewer", "pyzotero",
      "bio-manuscript-pipeline", "bio-innovation-check", "bio-task-system", "bio-dataset-search",
      "bio-metric-system", "bio-analysis-system", "bio-figure-design", "bio-manuscript-text",
      "bio-human-feedback", "bio-manuscript-refine", "bio-ppt-generate"]),

    ("academic-pipelines", "Academic Paper & Nature Pipelines",
     "End-to-end multi-agent paper pipelines and the Nature-family writing/review/translation suite.",
     ["research-writing", "literature-discovery", "reasoning-ideation"],
     ["academic-paper", "academic-paper-reviewer", "academic-pipeline", "deep-research",
      "nature-academic-search", "nature-citation", "nature-data", "nature-figure", "nature-paper2ppt",
      "nature-polishing", "nature-reader", "nature-response", "nature-reviewer", "nature-writing"]),

    ("scientific-expert-profiles", "Scientific Expert Profiles",
     "Discipline-specific scientific and engineering operating profiles adapted from K-Dense scientific-agents.",
     ["research-writing", "academic-pipelines", "reasoning-ideation", "data-science-compute"],
     []),

    ("literature-discovery", "Literature Search & Knowledge Discovery",
     "Paper search across databases, web research, content extraction, and knowledge bases.",
     ["research-writing", "academic-pipelines", "documents-office"],
     ["paper-lookup", "pubmed-summariser", "lit-synthesizer", "research-lookup", "exa-search",
      "parallel-web", "bgpt-mcp", "bgpt-paper-search", "paperzilla", "open-notebook", "defuddle",
      "literature-review", "data-extractor", "claw-semantic-sim", "pubmed-search"]),

    ("documents-office", "Documents, Office & Media",
     "Office document toolkits (docx/pptx/pdf/xlsx), file-to-markdown conversion, and image/report generation.",
     ["research-writing", "literature-discovery"],
     ["docx", "pptx", "pdf", "xlsx", "markitdown", "liteparse", "infographics", "generate-image",
      "market-research-reports", "doc-coauthoring", "internal-comms", "report-template",
      "officecli", "officecli-docx", "officecli-xlsx", "officecli-pptx",
      "officecli-academic-paper", "officecli-data-dashboard", "officecli-financial-model",
      "officecli-pitch-deck", "officecli-word-form", "morph-ppt", "morph-ppt-3d"]),

    ("cloud-devops", "Cloud, Infra & MLOps",
     "Cloud architecture and operations, resilience testing, containers, developer infrastructure, MLOps, and workflow pipelines.",
     ["ml-ai", "bio-databases-platforms", "vault-meta", "analytics-engineering", "security-auditing", "software-dev", "dotnet-development"],
     ["aws-agentic-ai", "aws-cdk-development", "aws-cost-operations", "aws-mcp-setup",
      "aws-serverless-eda", "modal", "hf-cli", "nextflow", "snakemake-workflow-engine",
      "e2b-sandbox", "devcontainer-setup", "modern-python", "conda-bioconda",
      "docker-expert", "kubernetes-specialist", "chaos-engineering", "ci-cd-and-automation", "shipping-and-launch",
      "dvc", "ray"]),

    ("software-dev", "Software Development & Engineering",
     "General software-engineering methodology and tooling: TDD, debugging, code review, planning, git worktrees, source-grounded implementation, plus core app primitives (pytest, Docker, FastAPI, CI).",
     ["vault-meta", "security-auditing", "cloud-devops", "reasoning-ideation", "dotnet-development",
      "matlab-development"],
     ["test-driven-development", "systematic-debugging", "verification-before-completion",
      "requesting-code-review", "receiving-code-review", "brainstorming", "writing-plans",
      "executing-plans", "subagent-driven-development", "dispatching-parallel-agents",
      "finishing-a-development-branch", "using-git-worktrees", "worktrunk", "using-superpowers",
      "using-agent-skills", "writing-skills", "api-and-interface-design",
      "code-review-and-quality", "code-simplification", "context-engineering",
      "debugging-and-error-recovery", "deprecation-and-migration", "documentation-and-adrs",
      "doubt-driven-development", "git-workflow-and-versioning", "incremental-implementation",
      "planning-and-task-breakdown", "source-driven-development", "spec-driven-development",
      "spec-kit",
      "pytest", "jest", "vitest", "docker", "fastapi", "github-actions-ci", "agentic-workflows",
      "opensrc", "check-pr", "greploop",
      "hunk-review", "ast-grep", "ast-grep-outline",
      "linear", "cavekit-methodology", "cavekit-validation-first", "cavekit-revision",
      "cavekit-design-system"]),

    ("vault-meta", "Vault, Skills & Workflow Meta",
     "Obsidian authoring, skill building/discovery, reproducibility, orchestration, and resource detection.",
     ["cloud-devops", "reasoning-ideation", "security-auditing", "software-dev"],
     ["obsidian-markdown", "obsidian-bases", "obsidian-cli", "json-canvas", "skill-builder",
      "find-skills", "autoskill", "clawpathy-autoresearch", "repro-enforcer", "bio-orchestrator",
      "get-available-resources", "mcp-builder", "auditing-skills", "plugin-creator",
      "dynamic-resources", "skills-hub"]),

    ("reasoning-ideation", "Reasoning, Ideation & Decision",
     "Multi-perspective deliberation, brainstorming, hypothesis generation, idea evaluation, and scenario analysis.",
     ["research-writing", "academic-pipelines", "vault-meta"],
     ["consciousness-council", "what-if-oracle", "dhdna-profiler", "scientific-brainstorming",
      "hypothesis-generation", "idea-evaluator", "idea-refine", "interview-me",
      "vibe-research-workflow", "hypogenic", "caveman", "caveman-compress", "cavecrew", "caveman-help", "caveman-review", "caveman-stats", "caveman-commit"]),

    ("web-automation-frontend", "Web Automation, Frontend & Design",
     "Browser automation, Playwright testing, frontend design guidance, React/Next.js patterns, Figma workflows, and design-to-code loops.",
     ["cloud-devops", "documents-office", "research-writing", "analytics-engineering", "dotnet-development"],
     ["agent-browser", "agentcore", "core", "dogfood", "electron", "slack", "vercel-sandbox",
      "playwright-cli", "playwright-best-practices", "webapp-testing", "frontend-design",
      "browser-testing-with-devtools", "frontend-ui-engineering", "performance-optimization",
      "web-design-guidelines", "vercel-composition-patterns", "vercel-react-best-practices",
      "vercel-react-view-transitions", "figma-use", "figma-generate-design",
      "figma-generate-library", "figma-implement-design", "web-artifacts-builder",
      "brand-guidelines", "theme-factory", "algorithmic-art", "brandkit",
      "design-md-library",
      "design-taste-frontend", "design-taste-frontend-v1", "full-output-enforcement",
      "gpt-taste", "high-end-visual-design", "image-to-code",
      "imagegen-frontend-mobile", "imagegen-frontend-web", "industrial-brutalist-ui",
      "minimalist-ui", "redesign-existing-projects", "stitch-design-taste",
      "ui-css-primitives", "screenshot-cli",
      # ibelick/ui-skills first-party pack
      "baseline-ui", "fixing-accessibility", "fixing-metadata",
      "fixing-motion-performance", "improve-ui"]),

    ("analytics-engineering", "Analytics Engineering & LLM Operations",
     "dbt analytics engineering, semantic layers, warehouse querying, lineage diagrams, LLM observability, prompt tracing, and evaluation workflows.",
     ["data-science-compute", "cloud-devops", "ml-ai", "security-auditing"],
     ["adding-dbt-unit-test", "answering-natural-language-questions-with-dbt",
      "building-dbt-semantic-layer", "configuring-dbt-mcp-server", "creating-mermaid-dbt-dag",
      "fetching-dbt-docs", "running-dbt-commands", "troubleshooting-dbt-job-errors",
      "using-dbt-for-analytics-engineering", "working-with-dbt-mesh",
      "migrating-dbt-core-to-fusion", "migrating-dbt-project-across-platforms",
      "langfuse", "phoenix-cli", "phoenix-evals", "llm-observability-evals",
      "observability-and-instrumentation",
      # pydantic/skills — Logfire observability
      "logfire-instrumentation", "logfire-query", "logfire-ui"]),

    ("security-auditing", "Security & Auditing",
     "Secure development, code auditing, static analysis, SARIF, fuzzing, agent security, supply-chain risk, and smart-contract review helpers.",
     ["cloud-devops", "vault-meta", "analytics-engineering", "web-automation-frontend", "dotnet-development"],
     ["llm-agent-security-redteam", "audit-context-building", "audit-prep-assistant",
      "code-maturity-assessor", "secure-workflow-guide", "differential-review", "gh-cli",
      "codeql", "sarif-parsing", "semgrep", "semgrep-rule-creator", "property-based-testing",
      "c-review", "constant-time-analysis", "constant-time-testing", "harness-writing",
      "coverage-analysis", "fuzzing-dictionary", "fuzzing-obstacles", "libfuzzer",
      "cargo-fuzz", "atheris", "ossfuzz", "aflpp", "supply-chain-risk-auditor",
      "agentic-actions-auditor", "insecure-defaults", "sharp-edges", "variant-analysis",
      "zeroize-audit", "fp-check", "guidelines-advisor", "entry-point-analyzer",
      "token-integration-analyzer", "spec-to-code-compliance", "security-and-hardening"]),

    ("saas-platforms", "SaaS & Vendor Platform Integrations",
     "Vendor product platforms and their SDKs: messaging and voice, commerce, CRM, analytics, and design/collaboration SaaS.",
     ["hosting-edge-platforms", "comms-productivity", "web-automation-frontend", "software-dev"],
     [
      "airtable-cli", "airtable-filters", "airtable-overview", "base44-cli", "base44-sdk",
      "base44-troubleshooter", "box-content-api", "brighthire", "build-zoom-bot",
      "build-zoom-contact-center-app", "build-zoom-meeting-app", "build-zoom-meeting-sdk-app",
      "build-zoom-phone-integration", "build-zoom-rest-api-app", "build-zoom-team-chat-app",
      "build-zoom-video-sdk-app", "build-zoom-virtual-agent", "canva-branded-presentation",
      "canva-resize-for-all-social-media", "canva-translate-design", "catalyst-by-zoho",
      "chat-sdk", "choose-zoom-approach", "conversation-intelligence", "debug-zoom",
      "debug-zoom-integration", "hex", "heygen-avatar", "heygen-video", "hubspot",
      "hubspot-crm-data-hygiene", "hubspot-customer-prep", "hubspot-pipeline-health",
      "hyperframes", "hyperframes-cli", "hyperframes-registry", "inflection", "magicpath",
      "marketplace", "mixpanel-auth", "mixpanel-headless-setup", "mixpanelyst", "payments",
      "plan-zoom-integration", "plan-zoom-product", "posthog", "probe-sdk", "replay-qa-api",
      "replayio", "rivet-sdk", "search-company-knowledge", "sentry", "setup-zoom-oauth",
      "setup-zoom-webhooks", "setup-zoom-websockets", "shopify-admin",
      "shopify-app-store-review", "shopify-custom-data", "shopify-customer", "shopify-dev",
      "shopify-functions", "shopify-hydrogen", "shopify-liquid", "shopify-onboarding-dev",
      "shopify-onboarding-merchant", "shopify-partner", "shopify-payments-apps",
      "shopify-polaris-admin-extensions", "shopify-polaris-app-home",
      "shopify-polaris-checkout-extensions", "shopify-polaris-customer-account-extensions",
      "shopify-pos-ui", "shopify-storefront-graphql", "shopify-use-shopify-cli",
      "stripe-best-practices", "superhuman-mail", "twilio-account-setup",
      "twilio-agent-augmentation-architect", "twilio-agent-connect",
      "twilio-ai-agent-architect", "twilio-call-recordings", "twilio-cli-reference",
      "twilio-compliance-onboarding", "twilio-compliance-traffic", "twilio-conference-calls",
      "twilio-content-template-builder", "twilio-conversation-orchestrator",
      "twilio-conversations-classic-api", "twilio-customer-memory",
      "twilio-customer-support-architect", "twilio-debugging-observability",
      "twilio-email-deliverability-advisor", "twilio-email-send",
      "twilio-enterprise-knowledge", "twilio-iam-auth-setup",
      "twilio-identity-verification-advisor", "twilio-isv-sms-best-practices",
      "twilio-lookup-phone-intelligence", "twilio-marketing-promotions-advisor",
      "twilio-messaging-channel-advisor", "twilio-messaging-overview",
      "twilio-messaging-services", "twilio-messaging-webhooks",
      "twilio-notifications-alerts-advisor", "twilio-numbers-senders",
      "twilio-organizations-setup", "twilio-rcs-messaging",
      "twilio-regulatory-compliance-bundles", "twilio-reliability-patterns",
      "twilio-security-api-auth", "twilio-security-compliance-hipaa",
      "twilio-security-hardening", "twilio-send-message", "twilio-sendgrid-account-setup",
      "twilio-sendgrid-deliverability-advisor", "twilio-sendgrid-email-send",
      "twilio-sendgrid-email-settings", "twilio-sendgrid-engagement-quality",
      "twilio-sendgrid-inbound-parse", "twilio-sendgrid-suppressions",
      "twilio-sendgrid-webhooks", "twilio-sms-send-message", "twilio-taskrouter-routing",
      "twilio-verify-send-otp", "twilio-voice-conversation-relay",
      "twilio-voice-outbound-calls", "twilio-voice-twiml", "twilio-webhook-architecture",
      "twilio-whatsapp-manage-senders", "twilio-whatsapp-send-message", "ucp",
      "upgrade-stripe", "website-to-hyperframes", "wix-app", "wix-design-system",
      "wix-headless", "wix-manage", "zoom-apps-sdk", "zoom-cobrowse-sdk",
      "zoom-contact-center-android", "zoom-contact-center-ios", "zoom-contact-center-web",
      "zoom-general", "zoom-meeting-sdk-android", "zoom-meeting-sdk-electron",
      "zoom-meeting-sdk-ios", "zoom-meeting-sdk-linux", "zoom-meeting-sdk-macos",
      "zoom-meeting-sdk-react-native", "zoom-meeting-sdk-unreal", "zoom-meeting-sdk-web",
      "zoom-meeting-sdk-windows", "zoom-oauth", "zoom-rtms", "zoom-video-sdk-android",
      "zoom-video-sdk-flutter", "zoom-video-sdk-ios", "zoom-video-sdk-linux",
      "zoom-video-sdk-macos", "zoom-video-sdk-react-native", "zoom-video-sdk-unity",
      "zoom-video-sdk-web", "zoom-video-sdk-windows", "zoom-virtual-agent-android",
      "zoom-virtual-agent-ios", "zoom-virtual-agent-web"
     ]),

    ("hosting-edge-platforms", "Hosting, Edge & Deployment Platforms",
     "Application hosting and edge runtimes, managed databases, CI providers, and the deploy/runtime plumbing that goes with them.",
     ["cloud-devops", "saas-platforms", "web-automation-frontend", "software-dev"],
     [
      "building-ai-agent-on-cloudflare", "building-mcp-server-on-cloudflare",
      "circleci-builds", "circleci-cli", "circleci-config", "cloudflare", "cron-jobs",
      "deployments-cicd", "durable-objects", "env-vars", "native-data-fetching", "ncc",
      "neon-postgres", "neon-postgres-egress-optimizer", "netlify-ai-gateway", "netlify-blobs",
      "netlify-caching", "netlify-cli-and-deploy", "netlify-config", "netlify-deploy",
      "netlify-edge-functions", "netlify-forms", "netlify-frameworks", "netlify-functions",
      "netlify-identity", "netlify-image-cdn", "observability", "provision-droplet",
      "render-background-workers", "render-blueprints", "render-cli", "render-cron-jobs",
      "render-debug", "render-deploy", "render-disks", "render-docker", "render-domains",
      "render-env-vars", "render-keyvalue", "render-mcp", "render-migrate-from-heroku",
      "render-monitor", "render-networking", "render-postgres", "render-private-services",
      "render-scaling", "render-static-sites", "render-web-services", "render-workflows",
      "routing-middleware", "runtime-cache", "sandbox-sdk", "sign-in-with-vercel", "supabase",
      "supabase-postgres-best-practices", "telemetry", "temporal-developer", "vercel-agent",
      "vercel-api", "vercel-cli", "vercel-firewall", "vercel-flags", "vercel-functions",
      "vercel-queues", "vercel-services", "vercel-storage", "workers-best-practices",
      "wrangler"
     ]),

    ("comms-productivity", "Communication & Productivity Suites",
     "Mail, calendar, chat and document suites (Outlook, Google Workspace, Teams, Slack, SharePoint, Notion) plus the briefing and triage workflows over them.",
     ["documents-office", "saas-platforms", "reasoning-ideation"],
     [
      "batch-draft-writer", "bulk-qa-answers", "capture-tasks-from-meeting-notes", "email",
      "eod-wrapup", "generate-status-report", "gmail", "gmail-inbox-triage", "google-calendar",
      "google-calendar-daily-brief", "google-calendar-free-up-time",
      "google-calendar-group-scheduler", "google-calendar-meeting-prep", "google-docs",
      "google-drive", "google-drive-comments", "google-sheets", "google-slides", "irl-tracker",
      "meeting-scheduler", "morning-briefing", "notion-knowledge-capture",
      "notion-meeting-intelligence", "notion-research-documentation",
      "notion-spec-to-implementation", "outlook-calendar", "outlook-calendar-daily-brief",
      "outlook-calendar-free-up-time", "outlook-calendar-group-scheduler",
      "outlook-calendar-meeting-prep", "outlook-calendar-shared-calendars", "outlook-email",
      "outlook-email-inbox-triage", "outlook-email-reply-drafting",
      "outlook-email-shared-mailboxes", "outlook-email-subscription-cleanup",
      "outlook-email-task-extraction", "scribe", "sharepoint", "sharepoint-powerpoint",
      "sharepoint-shared-doc-maintenance", "sharepoint-site-discovery",
      "sharepoint-spreadsheet-formula-builder", "sharepoint-spreadsheets",
      "sharepoint-word-docs", "slack-channel-summarization", "slack-daily-digest",
      "slack-notification-triage", "slack-outgoing-message", "slack-reply-drafting",
      "smart-file-renaming", "teams", "teams-channel-summarization", "teams-daily-digest",
      "teams-messages", "teams-notification-triage", "teams-planner-task-management",
      "teams-reply-drafting", "window-management"
     ]),

    ("finance-investment", "Finance, Investment & Business Analysis",
     "Valuation and deal work, fund and issuer research, earnings workflows, and recurring business reporting.",
     ["analytics-engineering", "documents-office", "reasoning-ideation"],
     [
      "bull-bear", "capital-allocation", "chronograph-cashflow-forecast",
      "chronograph-gp-meeting-prep", "chronograph-portfolio-company-one-pager", "comp-sheet",
      "comps", "dcf", "deal-tracker", "draft-brief", "draft-long-form-memo", "earnings-flash",
      "earnings-prep", "earnings-review", "fa-jobs-to-be-done", "fund-comparison",
      "fund-screener", "fund-summarizer", "guidance-tracker", "ib-deck", "industry",
      "litigation-update-post", "metric-pack-designer", "moody-s-company-analysis",
      "moody-s-earnings-brief", "moody-s-explore-mcp", "moody-s-issuer-brief",
      "moody-s-peer-analysis", "moody-s-rating-analysis", "moody-s-sector-brief",
      "precedent-transactions", "risk-analysis-audit", "supply-chain", "tearsheet",
      "unit-economics", "vdr-index-setup", "working-capital"
     ]),

    ("mobile-native-dev", "Mobile & Native App Development",
     "iOS, Android and desktop-native development: Expo/React Native, SwiftUI and AppKit, device debugging, signing and distribution.",
     ["web-automation-frontend", "software-dev", "game-development"],
     [
      "android-emulator-qa", "android-performance", "appkit-interop", "building-native-ui",
      "codex-expo-run-actions", "expo-api-routes", "expo-cicd-workflows", "expo-deployment",
      "expo-dev-client", "expo-module", "expo-tailwind-setup", "expo-ui-jetpack-compose",
      "expo-ui-swift-ui", "ios-app-intents", "ios-debugger-agent", "ios-ettrace-performance",
      "ios-memgraph-leaks", "ios-simulator-browser", "liquid-glass", "packaging-notarization",
      "signing-entitlements", "swiftpm-macos", "swiftui-liquid-glass", "swiftui-patterns",
      "swiftui-performance-audit", "swiftui-ui-patterns", "swiftui-view-refactor",
      "upgrading-expo", "use-dom"
     ]),

    ("game-development", "Game Development & Interactive 3D",
     "Game engines and loops, sprite and 3D asset pipelines, real-time rendering, and simulation/digital-twin tooling.",
     ["web-automation-frontend", "mobile-native-dev", "imaging-signals"],
     [
      "game-playtest", "game-studio", "game-ui-frontend", "omniverse-cad-to-simready",
      "omniverse-realtime-viewer", "omniverse-usd-performance-tuning", "phaser-2d-game",
      "physical-ai-infrastructure-setup-and-resilient-scaling",
      "physical-ai-neural-reconstruction", "react-three-fiber-game", "sprite-pipeline",
      "three-webgl-game", "web-3d-asset-pipeline", "web-game-foundations"
     ]),

    ("data-visualization", "Data Visualization & Charting",
     "Charting and dashboard libraries, diagram and layout engines, and the craft guidance for building and critiquing visualizations.",
     ["data-science-compute", "web-automation-frontend", "research-writing"],
     [
      "canvas2d-data-visualization", "d3-data-visualization", "dashboard-expert",
      "dashboards-and-real-time-visualization", "data-visualization",
      "gantt-chart-visualization", "geospatial-and-cartographic-visualization",
      "grammar-of-graphics-and-declarative-visualization", "json-render",
      "node-link-and-diagram-layout", "react-and-nextjs-data-visualization", "satori",
      "scrollytelling-and-parallax-data-visualization",
      "statistical-and-uncertainty-visualization", "testing-data-visualizations",
      "threejs-data-visualization", "typescript-data-visualization-engineering",
      "uml-and-software-architecture-visualization", "visualization-strategy-and-critique"
     ]),

    ("dotnet-development", ".NET & C# Development",
     "The official dotnet/skills catalog: C# language/runtime tooling, MSBuild build performance and modernization, .NET/xUnit/MSTest testing and migration, ASP.NET Core and Blazor web development, .NET MAUI mobile/desktop, EF Core, native interop, crash/performance diagnostics, project templates, and cross-version migration.",
     ["software-dev", "cloud-devops", "web-automation-frontend", "security-auditing"],
     ["analyzing-dotnet-performance", "android-tombstone-symbolication",
      "apple-crash-symbolication", "assertion-quality", "author-component",
      "authoring-github-workflows", "binlog-failure-analysis", "binlog-generation",
      "build-parallelism", "build-perf-baseline", "build-perf-diagnostics",
      "check-bin-obj-clash", "clr-activation-debugging", "code-testing-agent",
      "code-testing-extensions", "collect-user-input", "configure-auth",
      "configuring-opentelemetry-dotnet", "convert-blazor-server-to-webapp", "convert-to-cpm",
      "coordinate-components", "copy-to-output-directory", "crap-score",
      "create-blazor-project", "csharp-scripts", "detect-static-dependencies",
      "directory-build-organization", "dotnet-aot-compat", "dotnet-coverage-analysis",
      "dotnet-maui-doctor", "dotnet-pinvoke", "dotnet-trace-collect", "dotnet-webapi",
      "dump-collect", "eval-performance", "exp-mock-usage-analysis", "exp-simd-vectorization",
      "exp-test-maintainability", "extension-points", "fetch-and-send-data", "filter-syntax",
      "find-untested-sources", "generate-testability-wrappers", "grade-tests",
      "including-generated-files", "incremental-build", "item-management",
      "maui-app-lifecycle", "maui-collectionview", "maui-data-binding",
      "maui-dependency-injection", "maui-safe-area", "maui-shell-navigation", "maui-theming",
      "mcp-csharp-create", "mcp-csharp-debug", "mcp-csharp-publish", "mcp-csharp-test",
      "microbenchmarking", "migrate-dotnet10-to-dotnet11", "migrate-dotnet8-to-dotnet9",
      "migrate-dotnet9-to-dotnet10", "migrate-mstest-v1v2-to-v3", "migrate-mstest-v3-to-v4",
      "migrate-nullable-references", "migrate-static-to-wrapper", "migrate-vstest-to-mtp",
      "migrate-xunit-to-mstest", "migrate-xunit-to-xunit-v3", "minimal-api-file-upload",
      "msbuild-antipatterns", "msbuild-modernization", "msbuild-server", "mtp-hot-reload",
      "nuget-trusted-publishing", "optimizing-ef-core-queries", "plan-ui-change",
      "platform-detection", "property-patterns", "resolve-project-references", "run-tests",
      "setup-local-sdk", "support-prerendering", "system-text-json-net11", "target-authoring",
      "technology-selection", "template-authoring", "template-comparison",
      "template-discovery", "template-instantiation", "template-smart-defaults",
      "template-validation", "test-analysis-extensions", "test-anti-patterns",
      "test-gap-analysis", "test-smell-detection", "test-tagging", "thread-abort-migration",
      "use-js-interop", "writing-mstest-tests"]),

    ("matlab-development", "MATLAB Development",
     "MATLAB language and toolchain work: the base-MATLAB skill groups of MathWorks' matlab-agentic-toolkit (core debugging/testing/review, live scripts, software development and toolbox packaging, app building, table and timetable analysis, Python and MEX interfaces, argument validation) plus the general MATLAB/Octave language reference.",
     ["data-science-compute", "software-dev", "imaging-signals", "ml-ai"],
     ["matlab",
      # matlab-agentic-toolkit — MATLAB Core
      "matlab-create-live-script", "matlab-debugging", "matlab-install-products",
      "matlab-list-products", "matlab-read-doc", "matlab-review-code", "matlab-testing",
      # matlab-agentic-toolkit — MATLAB Software Development
      "matlab-analyze-dependencies", "matlab-assess-toolbox", "matlab-build-toolbox",
      "matlab-create-buildfile", "matlab-create-project", "matlab-define-toolbox-api",
      "matlab-document-toolbox", "matlab-exclude-files",
      "matlab-instrument-opentelemetry-tracing", "matlab-modernize-code",
      "matlab-optimize-memory", "matlab-optimize-performance", "matlab-publish-toolbox",
      "matlab-write-help", "matlab-write-performance-tests",
      # matlab-agentic-toolkit — MATLAB App Building
      "matlab-build-app", "matlab-build-chart", "matlab-theming",
      # matlab-agentic-toolkit — MATLAB Data Import and Analysis
      "matlab-analyze-data", "matlab-choose-bigdata-solution",
      # matlab-agentic-toolkit — MATLAB External Language Interfaces
      "matlab-call-python", "matlab-upgrade-mex-ic",
      # matlab-agentic-toolkit — MATLAB Programming
      "matlab-validate-function-arguments"]),
]


# ---------------------------------------------------------------------------
def read_description(skill):
    path = os.path.join(skills_root(), skill, "SKILL.md")
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return None
    fm = m.group(1)
    desc_lines, capturing = [], False
    for line in fm.splitlines():
        if not capturing:
            km = re.match(r"^description:\s*(.*)$", line)
            if km:
                capturing = True
                rest = km.group(1).strip()
                if rest and rest not in (">", "|", ">-", "|-"):
                    desc_lines.append(rest)
        else:
            if re.match(r"^[A-Za-z0-9_-]+:(\s|$)", line) or line.strip() == "---":
                break
            desc_lines.append(line.strip())
    raw = " ".join(p for p in desc_lines if p).strip()
    if len(raw) >= 2 and raw[0] == '"' == raw[-1]:
        # double-quoted scalars carry \" and \\ escapes; unescape in one pass
        raw = re.sub(r'\\(["\\])', r"\1", raw[1:-1])
    else:
        raw = raw.strip("'\"")
    desc = raw.strip()
    return " ".join(desc.split()) or None


def one_liner(desc, limit=185):
    if not desc:
        return "(no description)"
    parts = re.split(r"(?<=[.;])\s+", desc)
    out = ""
    for p in parts:
        out = (out + " " + p).strip() if out else p
        if len(out) >= 40:
            break
    out = " ".join(out.split()).rstrip(" .;,")
    if len(out) > limit:
        out = out[:limit].rsplit(" ", 1)[0].rstrip(" .;,") + "..."
    return out


def gen_aliases(skill, desc):
    """Search synonyms: curated terms + spaced id + tool acronyms in the FIRST sentence."""
    al = list(SYNONYMS.get(skill, []))
    if "-" in skill:
        al.append(skill.replace("-", " "))
    first = re.split(r"(?<=[.;])\s+", desc or "", maxsplit=1)[0] if desc else ""
    for m in re.finditer(r"\(([^)]{1,40})\)", first):
        for tok in re.split(r"[,/]| or | and ", m.group(1)):
            tok = tok.strip()
            if (re.fullmatch(r"[A-Za-z][A-Za-z0-9.+-]{1,14}", tok)
                    and any(c.isupper() for c in tok)
                    and tok.upper() not in STOP
                    and tok.lower() != skill.lower()):
                al.append(tok)
    seen, out = set(), []
    for a in al:
        if a.lower() not in seen:
            seen.add(a.lower()); out.append(a)
    return out[:5]


def discover_skills():
    found = set()
    for name in os.listdir(skills_root()):
        if name.startswith("."):
            continue
        p = os.path.join(skills_root(), name)
        if os.path.isdir(p) and os.path.isfile(os.path.join(p, "SKILL.md")):
            found.add(name)
    # Recurse into bundled skill collections (e.g. gstack/) that ship their
    # own sub-skills as gstack/<subskill>/SKILL.md. These are registered as
    # "gstack/<subskill>" IDs so source: links resolve correctly, while the
    # wrapper filename uses "gstack-<subskill>.md" (see wrapper_filename()).
    for bundle in ("gstack",):
        bundle_dir = os.path.join(skills_root(), bundle)
        if not os.path.isdir(bundle_dir):
            continue
        for sub in os.listdir(bundle_dir):
            if sub.startswith("."):
                continue
            sub_p = os.path.join(bundle_dir, sub)
            if os.path.isdir(sub_p) and os.path.isfile(
                os.path.join(sub_p, "SKILL.md")
            ):
                found.add(f"{bundle}/{sub}")
    return found


def wrapper_filename(skill):
    """Map a skill ID to its wrapper note filename.

    Top-level skills: "scanpy" -> "scanpy.md"
    Bundled sub-skills: "gstack/office-hours" -> "gstack-office-hours.md"
    """
    return skill.replace("/", "-") + ".md"


def is_gstack_subskill(skill):
    """Transient gstack bundle sub-skills / install artifacts. The optional
    gstack extra (skipped by default) installs each sub-skill as a top-level
    ``gstack-<name>/`` dir and also ships a ``gstack/<name>`` bundle tree; those
    wrappers are gitignored and come/go with the install. They are excluded from
    the index count, the flat A–Z list, and the Uncategorized section so the
    committed navigation does not churn with install state. The bare ``gstack``
    entry point is excluded too: its folder is gitignored, so CI cannot
    reproduce any navigation derived from it. See VAULT-AUDIT SCALE-3 / MNT-12."""
    return (
        skill == "gstack"
        or skill.startswith("gstack/")
        or skill.startswith("gstack-")
        or skill.startswith("_gstack")
    )


UI_UX_PRO_MAX_SKILLS = frozenset({
    "ui-ux-pro-max",
    "banner-design",
    "brand",
    "design-system",
    "design",
    "slides",
    "ui-styling",
})


def is_ui_ux_pro_max_skill(skill):
    """Transient folders generated only when the optional UI/UX extra is
    installed. Keep them out of committed navigation so build output is a
    fixed point whether or not a machine has opted into the bundle."""
    return skill in UI_UX_PRO_MAX_SKILLS


def is_scientific_agents_profile(skill):
    path = os.path.join(skills_root(), skill, "SKILL.md")
    if not os.path.isfile(path):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read(4096)
    except OSError:
        return False
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return False
    fm = m.group(1)
    return bool(
        re.search(r"(?m)^\s*scientific-agents-profile:\s*true\b", fm)
        or re.search(r"(?m)^\s*source-repo:\s*K-Dense-AI/scientific-agents\b", fm)
    )


# Skill ids that are common English words — their whole-word match against other
# skills' descriptions produces spurious edges (e.g. "linear" matching "linear algebra"
# in matlab/shap/sympy). They are never used as a search pattern against *other*
# descriptions; they still gain edges when a specific skill name appears in their own.
GENERIC_NAMES = {"linear", "core", "query", "find-skills"}


def build_related(skills, full_desc):
    patterns = {s: re.compile(r"(?<![\w-])" + re.escape(s) + r"(?![\w-])", re.IGNORECASE)
                for s in skills}
    edges = {s: set() for s in skills}
    for s in skills:
        d = full_desc.get(s) or ""
        if not d:
            continue
        for t in skills:
            if t != s and t not in GENERIC_NAMES and patterns[t].search(d):
                edges[s].add(t); edges[t].add(s)
    return edges


def build_related_excluding(skills, full_desc, excluded):
    """Build exact-name edges without allowing excluded skills to participate."""
    excluded = set(excluded)
    candidates = [skill for skill in skills if skill not in excluded]
    related = build_related(candidates, full_desc)
    for skill in skills:
        related.setdefault(skill, set())
    return related


def find_existing_note(skill, key):
    """Locate a skill's current wrapper note, wherever it currently sits.

    Normally that is notes/<key>/<skill>.md. When a skill is recategorised the
    note is still in its previous domain folder, so fall back to a scan: without
    it the rebuild would start from scratch and silently reset `created`,
    `status`, `rating`, aliases and the personal-notes section. --prune removes
    the stale copy afterwards.
    """
    path = note_path(skill, key)
    if os.path.isfile(path):
        return path
    filename = wrapper_filename(skill)
    try:
        domains = sorted(os.listdir(notes_root()))
    except OSError:
        return None
    for domain in domains:
        candidate = os.path.join(notes_root(), domain, filename)
        if os.path.isfile(candidate):
            return candidate
    return None


def parse_existing(skill, key):
    """Read user-editable bits from an existing wrapper so re-runs preserve them."""
    path = find_existing_note(skill, key)
    if path is None:
        return None
    with open(path, encoding="utf-8") as wrapper_file:
        txt = wrapper_file.read()
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.DOTALL)
    fm = m.group(1) if m else ""
    data = {}
    for key in ("created", "status", "rating"):
        km = re.search(rf"^{key}:\s*(.+)$", fm, re.MULTILINE)
        if km:
            data[key] = km.group(1).strip()
    # None => no aliases key at all (auto-generate); [] => user set it empty (respect)
    aliases = None
    block = re.search(r"^aliases:\s*\n((?:[ \t]*-[ \t].*\n?)+)", fm, re.MULTILINE)
    inline = re.search(r"^aliases:\s*\[(.*)\]\s*$", fm, re.MULTILINE)
    empty = re.search(r"^aliases:\s*(\[\s*\]|)\s*$", fm, re.MULTILINE)
    if block:
        aliases = []
        for line in block.group(1).splitlines():
            lm = re.match(r"[ \t]*-[ \t]+(.*)$", line)
            if lm:
                aliases.append(lm.group(1).strip().strip("'\""))
    elif inline:
        aliases = [a.strip().strip("'\"") for a in inline.group(1).split(",") if a.strip()]
    elif empty:
        aliases = []
    data["aliases"] = aliases
    idx = txt.find(PERSONAL_MARKER)
    data["personal"] = txt[idx:] if idx != -1 else None
    return data


def existing_created(path):
    """Preserve generated note creation dates across rebuilds."""
    if not os.path.isfile(path):
        return TODAY
    try:
        with open(path, encoding="utf-8") as f:
            txt = f.read(1024)
    except OSError:
        return TODAY
    m = re.search(r"^created:\s*(.+)$", txt, re.MULTILINE)
    return m.group(1).strip() if m else TODAY


def expert_map_path(directory, discipline_id):
    """Resolve one nested map path and reject paths outside its directory."""
    root = Path(directory).resolve()
    candidate = (root / f"{discipline_id}.md").resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise TaxonomyValidationError(
            (f"discipline path escapes expert map directory: {discipline_id}",)
        ) from exc
    return candidate


def atomic_write_text(path, content):
    """Atomically replace a generated text file via a temporary sibling."""
    path = Path(path)
    mode = stat.S_IMODE(path.stat().st_mode) if path.exists() else 0o644
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
        temporary_path.chmod(mode)
        os.replace(temporary_path, path)
    except BaseException:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise


def render_expert_master_map(*, taxonomy, title, scope, created, domain_by_skill=None):
    """Render the scientific expert profile master map."""
    domain_by_skill = domain_by_skill or {}
    lines = [
        "---",
        f"title: {title}",
        "tags:",
        "  - skill-map",
        GENERATED_EXPERT_MARKER,
        f"created: {created}",
        "---",
        "",
        f"# {title}",
        "",
        "> [!abstract] Scope",
        f"> {scope}",
        "",
        "[Back to Skill Index](../index.md)",
        "",
        "## Profile Dispatcher",
        "",
        f"- [scientific-agents]("
        f"{note_link('scientific-agents', domain_by_skill, '../')}) - Route a question "
        "to the most relevant scientific expert profile.",
        "",
        "## Browse By Discipline",
        "",
    ]
    for discipline in taxonomy.disciplines:
        primary_count = len(taxonomy.primary_profiles(discipline.id))
        cross_count = len(taxonomy.secondary_profiles(discipline.id))
        lines.append(
            f"- [{discipline.title}]"
            f"({EXPERT_DOMAIN}/{discipline.id}.md) - "
            f"{primary_count} primary, {cross_count} cross-disciplinary"
        )
    lines.append("")
    return "\n".join(lines)


def render_expert_discipline_map(
    *,
    discipline,
    taxonomy,
    short_descriptions,
    category_titles,
    bridge_domain_order,
    created,
    domain_by_skill=None,
):
    """Render one scientific expert discipline map."""
    domain_by_skill = domain_by_skill or {}
    primary = taxonomy.primary_profiles(discipline.id)
    secondary = taxonomy.secondary_profiles(discipline.id)
    bridges = taxonomy.bridge_domains_for_discipline(
        discipline.id, bridge_domain_order
    )
    lines = [
        "---",
        f"title: {discipline.title}",
        "tags:",
        "  - skill-map",
        GENERATED_EXPERT_MARKER,
        f"created: {created}",
        "---",
        "",
        f"# {discipline.title}",
        "",
        "> [!abstract] Scope",
        f"> {discipline.description}",
        "",
        "[Back to Scientific Expert Profiles](../scientific-expert-profiles.md)",
        "",
        "## Relevant capability maps",
        "",
    ]
    if bridges:
        lines += [
            f"- [{category_titles[domain]}](../{domain}.md)"
            for domain in bridges
        ]
    else:
        lines.append("_No capability maps assigned._")
    lines += ["", "## Primary experts", ""]
    if primary:
        lines += [
            f"- [{slug}]({note_link(slug, domain_by_skill, '../../')}) - "
            f"{short_descriptions[slug]}"
            for slug in primary
        ]
    else:
        lines.append("_No primary experts._")
    lines += ["", "## Cross-disciplinary experts", ""]
    if secondary:
        lines += [
            f"- [{slug}]({note_link(slug, domain_by_skill, '../../')}) - "
            f"{short_descriptions[slug]}"
            for slug in secondary
        ]
    else:
        lines.append("_No cross-disciplinary experts._")
    lines.append("")
    return "\n".join(lines)


def prune_stale_expert_maps(directory, discipline_ids):
    """Remove obsolete generated direct-child maps without touching other files."""
    current = set(discipline_ids)
    pruned = []
    for path in Path(directory).glob("*.md"):
        if not path.is_file() or path.stem in current:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        frontmatter = re.match(r"^---\s*\n(.*?)\n---(?:\s*\n|$)", text, re.DOTALL)
        if (
            frontmatter is not None
            and GENERATED_EXPERT_MARKER in frontmatter.group(1).splitlines()
        ):
            path.unlink()
            pruned.append(path.name)
    return tuple(sorted(pruned))


def emit_alias_block(aliases):
    if not aliases:
        return []
    out = ["aliases:"]
    for a in aliases:
        out.append(f'  - "{a}"' if re.search(r'[:#\[\],&*?{}|<>=!%@`"]', a) else f"  - {a}")
    return out


def render_wrapper(
    skill,
    *,
    key,
    domain_title,
    description,
    short_descriptions,
    related,
    existing,
    today,
    force_aliases,
    domain_by_skill=None,
    expert_assignment: ProfileAssignment | None = None,
    discipline_titles=None,
    category_titles=None,
    bridge_domain_order=(),
):
    """Render one wrapper without reading from or writing to the vault."""
    domain_by_skill = domain_by_skill or {}
    discipline_titles = discipline_titles or {}
    category_titles = category_titles or {}
    if existing:
        created = existing.get("created", today)
        status = existing.get("status", "untried")
        rating = existing.get("rating")
        aliases = existing.get("aliases")
        if aliases is None or force_aliases:
            aliases = gen_aliases(skill, description)
        personal = existing.get("personal")
    else:
        created, status, rating = today, "untried", None
        aliases = gen_aliases(skill, description)
        personal = None

    lines = ["---", f"title: {skill}"]
    lines += emit_alias_block(aliases)
    lines += ["tags:", "  - skill"]
    if key != "uncategorized":
        lines.append(f"  - domain/{key}")
        lines.append(f"domain: {key}")
    if expert_assignment is not None:
        lines.append(f"expert_primary: {expert_assignment.primary}")
        if expert_assignment.secondary:
            lines.append("expert_secondary:")
            lines += [f"  - {value}" for value in expert_assignment.secondary]
        lines.append("bridge_domains:")
        lines += [f"  - {value}" for value in expert_assignment.bridge_domains]
    lines.append(f"status: {status}")
    if rating is not None:
        lines.append(f"rating: {rating}")
    lines.append(f"source: {SKILLS_SUBDIR}/{skill}/SKILL.md")
    lines.append(f"created: {created}")
    lines += [
        "---",
        "",
        f"# {skill}",
        "",
        "> [!info] What it does",
        f"> {description or '(no description)'}",
        "",
    ]

    # A note sits at vault/notes/<key>/<skill>.md: ../.. reaches vault/, and
    # ../../.. reaches the repo root where skills/ lives.
    source_rel = f"{SKILLS_SUBDIR}/{skill}/SKILL.md"
    nav = [f"**Source:** [{source_rel}](../../../{source_rel})"]
    if key != "uncategorized":
        nav.append(f"**Domain:** [{domain_title}](../../maps/{key}.md)")
    if expert_assignment is not None:
        primary = expert_assignment.primary
        nav.append(
            "**Primary:** "
            f"[{discipline_titles[primary]}]"
            f"(../../maps/{EXPERT_DOMAIN}/{primary}.md)"
        )
        if expert_assignment.secondary:
            secondary_links = ", ".join(
                f"[{discipline_titles[value]}]"
                f"(../../maps/{EXPERT_DOMAIN}/{value}.md)"
                for value in expert_assignment.secondary
            )
            nav.append(f"**Secondary:** {secondary_links}")
    nav += [
        "**Table:** [skills.base](../../skills.base)",
        "**Index:** [Skills Index](../../index.md)",
    ]
    lines += ["  ·  ".join(nav), ""]

    if expert_assignment is not None:
        lines += ["## Relevant capability domains", ""]
        bridges = set(expert_assignment.bridge_domains)
        lines += [
            f"- [{category_titles[domain]}](../../maps/{domain}.md)"
            for domain in bridge_domain_order
            if domain in bridges
        ]
    else:
        lines += ["## Related skills", ""]
        rel = sorted(related)
        if rel:
            lines += [
                f"- [{other}]({note_link(other, domain_by_skill, '../../')}) — "
                f"{short_descriptions[other]}"
                for other in rel
            ]
        else:
            lines.append(
                "_None auto-detected. Add your own links here, e.g. "
                "`[[scanpy]]`._"
            )
    lines.append("")
    if personal:
        lines.append(personal)
    else:
        lines += [PERSONAL_MARKER, "", "## Notes", ""]
    return "\n".join(lines)


def expert_graph_groups(taxonomy):
    """Build expert color groups after checking taxonomy/palette coverage."""
    discipline_ids = tuple(
        discipline.id for discipline in taxonomy.disciplines
    )
    taxonomy_domains = set(discipline_ids)
    palette_domains = set(EXPERT_PALETTE)
    missing = sorted(taxonomy_domains - palette_domains)
    unexpected = sorted(palette_domains - taxonomy_domains)
    if missing or unexpected:
        raise TaxonomyValidationError((
            "expert graph palette domains mismatch: "
            f"missing={', '.join(missing) or 'none'}; "
            f"unexpected={', '.join(unexpected) or 'none'}",
        ))
    return [
        {
            "query": f"[expert_primary:{discipline_id}]",
            "color": {"a": 1, "rgb": EXPERT_PALETTE[discipline_id]},
        }
        for discipline_id in discipline_ids
    ]


def update_graph(taxonomy):
    """Rewrite graph.json color groups + filter, preserving all other settings."""
    import json
    expert_groups = expert_graph_groups(taxonomy)
    path = os.path.join(ROOT, ".obsidian", "graph.json")
    cfg = {}
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8") as graph_file:
                cfg = json.load(graph_file)
        except (OSError, ValueError):
            cfg = {}
    if cfg.get("close") is False:
        print("WARNING: graph.json says the Graph view is OPEN; close it first or "
              "Obsidian may overwrite these colors.", file=sys.stderr)
    cfg["search"] = GRAPH_SEARCH
    cfg["showOrphans"] = False
    domain_groups = [
        {"query": f"tag:#domain/{key}", "color": {"a": 1, "rgb": PALETTE[key]}}
        for key, *_ in CATEGORIES if key in PALETTE
    ]
    cfg["colorGroups"] = expert_groups + domain_groups
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print(f"graph.json: wrote {len(cfg['colorGroups'])} color groups + filter")


# Manual domain assignments for skills not enumerated in a CATEGORIES skills list.
# Bridges the gap until domains are derived from each SKILL.md's frontmatter (MNT-7).
# Keys must be valid CATEGORIES domain keys; applied only if the skill exists on disk
# and is not already assigned via CATEGORIES.
EXTRA_ASSIGNMENTS = {
    # Bulk-imported vendor and tool packs routed into existing domains
    # (2026-08-09 sweep of the 574 previously uncategorized skills).
    # -> bio-databases-platforms
    "biostudies-arrayexpress-skill": "bio-databases-platforms",
    "cbioportal-skill": "bio-databases-platforms",
    "cellxgene-skill": "bio-databases-platforms",
    "clinicaltrials-skill": "bio-databases-platforms",
    "efo-ontology-skill": "bio-databases-platforms",
    "ensembl-skill": "bio-databases-platforms", "epigraphdb-skill": "bio-databases-platforms",
    "eva-skill": "bio-databases-platforms",
    "human-protein-atlas-skill": "bio-databases-platforms",
    "ipd-skill": "bio-databases-platforms", "metabolights-skill": "bio-databases-platforms",
    "mgnify-skill": "bio-databases-platforms",
    "ncbi-clinicaltables-skill": "bio-databases-platforms",
    "ncbi-entrez-skill": "bio-databases-platforms",
    "opentargets-skill": "bio-databases-platforms", "pride-skill": "bio-databases-platforms",
    "proteomexchange-skill": "bio-databases-platforms",
    "quickgo-skill": "bio-databases-platforms", "reactome-skill": "bio-databases-platforms",
    "research-router-skill": "bio-databases-platforms",
    "string-skill": "bio-databases-platforms", "uniprot-skill": "bio-databases-platforms",
    # -> data-science-compute
    "deepnote": "data-science-compute", "deepnote-data-execution": "data-science-compute",
    "deepnote-links": "data-science-compute",
    "deepnote-notebook-editing": "data-science-compute",
    "deepnote-notebooks": "data-science-compute",
    # -> documents-office
    "reports-pdfs-and-slide-automation": "documents-office",
    # -> drug-discovery-chem
    "alphafold-skill": "drug-discovery-chem", "bindingdb-skill": "drug-discovery-chem",
    "boltz-check-status": "drug-discovery-chem", "boltz-cli-setup": "drug-discovery-chem",
    "boltz-protein-design": "drug-discovery-chem",
    "boltz-protein-screen": "drug-discovery-chem",
    "boltz-small-molecule-adme": "drug-discovery-chem",
    "boltz-small-molecule-design": "drug-discovery-chem",
    "boltz-small-molecule-screen": "drug-discovery-chem",
    "boltz-structure-and-binding": "drug-discovery-chem", "chebi-skill": "drug-discovery-chem",
    "chembl-skill": "drug-discovery-chem", "hmdb-skill": "drug-discovery-chem",
    "pharmgkb-skill": "drug-discovery-chem", "pubchem-pug-skill": "drug-discovery-chem",
    "rcsb-pdb-skill": "drug-discovery-chem", "rhea-skill": "drug-discovery-chem",
    # -> genomics-variants
    "biobankjapan-phewas-skill": "genomics-variants", "civic-skill": "genomics-variants",
    "clinvar-variation-skill": "genomics-variants",
    "eqtl-catalogue-skill": "genomics-variants", "finngen-phewas-skill": "genomics-variants",
    "genebass-gene-burden-skill": "genomics-variants",
    "gnomad-graphql-skill": "genomics-variants", "gtex-eqtl-skill": "genomics-variants",
    "gwas-catalog-skill": "genomics-variants",
    "locus-to-gene-mapper-skill": "genomics-variants",
    "ncbi-datasets-skill": "genomics-variants", "ngs-analysis-router": "genomics-variants",
    "ngs-dna-germline-variants": "genomics-variants",
    "ngs-dna-somatic-variants": "genomics-variants",
    "ngs-dna-umi-panel-variants": "genomics-variants",
    "ngs-dna-variant-calling": "genomics-variants", "tpmi-phewas-skill": "genomics-variants",
    "ukb-topmed-phewas-skill": "genomics-variants",
    # -> literature-discovery
    "biorxiv-skill": "literature-discovery", "citations": "literature-discovery",
    "cite-check": "literature-discovery", "ncbi-pmc-skill": "literature-discovery",
    "research-note": "literature-discovery", "zotero": "literature-discovery",
    # -> ml-ai
    "agents-sdk": "ml-ai", "ai-elements": "ml-ai", "ai-gateway": "ml-ai",
    "ai-generation-persistence": "ml-ai", "ai-sdk": "ml-ai", "aiq-deploy": "ml-ai",
    "aiq-research": "ml-ai", "build-chatgpt-app": "ml-ai", "build-model": "ml-ai",
    "chatgpt-app-submission": "ml-ai", "chunk": "ml-ai", "cuopt-user-rules": "ml-ai",
    "huggingface-community-evals": "ml-ai", "huggingface-datasets": "ml-ai",
    "huggingface-gradio": "ml-ai", "huggingface-jobs": "ml-ai",
    "huggingface-llm-trainer": "ml-ai", "huggingface-paper-publisher": "ml-ai",
    "huggingface-papers": "ml-ai", "huggingface-trackio": "ml-ai",
    "huggingface-vision-trainer": "ml-ai", "nemoclaw-user-get-started": "ml-ai",
    "openai-ads-conversions-setup": "ml-ai", "openai-api-troubleshooting": "ml-ai",
    "openai-platform-api-key": "ml-ai", "transformers-js": "ml-ai",
    # -> security-auditing
    "attack-path-analysis": "security-auditing", "auth": "security-auditing",
    "deep-security-scan": "security-auditing", "finding-discovery": "security-auditing",
    "fix-finding": "security-auditing", "propose-security-hardening": "security-auditing",
    "security-diff-scan": "security-auditing", "security-scan": "security-auditing",
    "threat-model": "security-auditing", "track-findings": "security-auditing",
    "triage-finding": "security-auditing", "vulnerability-writeup": "security-auditing",
    # reverse-skill pack (zhaoxuya520/reverse-skill): reversing, pentest,
    # offensive-security and defensive tooling all land in security-auditing
    "api-security": "security-auditing", "apk-reverse": "security-auditing",
    "attack-chain": "security-auditing", "binary-diff": "security-auditing",
    "browser-automation": "security-auditing", "browser-extension-reverse": "security-auditing",
    "case-review": "security-auditing", "cloud-k8s": "security-auditing",
    "code-audit": "security-auditing",
    "database-security": "security-auditing", "diagram-generator": "software-dev",
    "digital-forensics": "security-auditing", "docs-generator": "software-dev",
    "dotnet-reverse": "security-auditing", "edr-bypass-re": "security-auditing",
    "email-security": "security-auditing", "firmware-pentest": "security-auditing",
    "ghidra-reverse": "security-auditing", "go-rust-reverse": "security-auditing",
    "hardware-security": "security-auditing", "ida-reverse": "security-auditing",
    "identity-federation": "security-auditing", "js-reverse": "security-auditing",
    "llm-security": "security-auditing", "macos-reverse": "security-auditing",
    "malware-analysis": "security-auditing", "mobile-reverse": "security-auditing",
    "ot-ics": "security-auditing", "patch-diff-exploit": "security-auditing",
    "pentest-tools": "security-auditing", "protocol-reverse": "security-auditing",
    "pwn-chain": "security-auditing", "radare2": "security-auditing",
    "radio-sdr": "security-auditing", "reverse-engineering": "security-auditing",
    "reverse-skill-router": "security-auditing", "supply-chain-security": "security-auditing",
    "thick-client": "security-auditing", "threat-hunting": "security-auditing",
    "wifi-wireless": "security-auditing", "windows-ad": "security-auditing",
    # -> sequence-phylogenetics
    "ncbi-blast-skill": "sequence-phylogenetics",
    "ngs-amplicon-microbiome": "sequence-phylogenetics",
    "ngs-bcl-to-fastq": "sequence-phylogenetics", "ngs-fastq-qc": "sequence-phylogenetics",
    "ngs-runtime-env": "sequence-phylogenetics",
    "ngs-shotgun-metagenomics": "sequence-phylogenetics",
    "rnacentral-skill": "sequence-phylogenetics",
    # -> single-cell-rnaseq
    "bgee-skill": "single-cell-rnaseq", "encode-skill": "single-cell-rnaseq",
    "ngs-atacseq-peaks-qc": "single-cell-rnaseq", "ngs-bulk-rnaseq": "single-cell-rnaseq",
    "ngs-bulk-rnaseq-counts-qc": "single-cell-rnaseq",
    "ngs-bulk-rnaseq-differential-expression": "single-cell-rnaseq",
    "ngs-chip-cutrun-peaks-qc": "single-cell-rnaseq",
    "ngs-epigenomics-peaks": "single-cell-rnaseq", "ngs-scrna-seq": "single-cell-rnaseq",
    "scrna-seq-qc": "single-cell-rnaseq",
    # -> software-dev
    "build-run-debug": "software-dev", "code-review": "software-dev",
    "document-quality-check": "software-dev", "dynamo-interconnect-check": "software-dev",
    "dynamo-router-starter": "software-dev", "gap-analysis": "software-dev",
    "gh-address-comments": "software-dev", "gh-fix-ci": "software-dev",
    "github": "software-dev", "investigation-mode": "software-dev",
    "launch-readiness-orchestrator": "software-dev", "spec-to-backlog": "software-dev",
    "test-triage": "software-dev", "triage-issue": "software-dev",
    "validation": "software-dev", "verification": "software-dev",
    "view-refactor": "software-dev", "workflow": "software-dev",
    # -> vault-meta
    "evaluate-plugin": "vault-meta", "evaluate-skill": "vault-meta",
    "improve-skill": "vault-meta", "initiate": "vault-meta", "minimal-skill": "vault-meta",
    "plugin-eval": "vault-meta", "setup": "vault-meta", "start": "vault-meta",
    "template": "vault-meta", "yeet": "vault-meta",
    # -> web-automation-frontend
    "accessibility-and-inclusive-visualization": "web-automation-frontend",
    "agent-browser-verify": "web-automation-frontend", "bootstrap": "web-automation-frontend",
    "cms": "web-automation-frontend", "figma-code-connect": "web-automation-frontend",
    "figma-create-new-file": "web-automation-frontend",
    "figma-design-to-code": "web-automation-frontend",
    "figma-generate-diagram": "web-automation-frontend",
    "figma-implement-motion": "web-automation-frontend",
    "figma-swiftui": "web-automation-frontend", "figma-use-figjam": "web-automation-frontend",
    "figma-use-motion": "web-automation-frontend",
    "figma-use-slides": "web-automation-frontend",
    "frontend-app-builder": "web-automation-frontend",
    "frontend-testing-debugging": "web-automation-frontend",
    "geist": "web-automation-frontend", "geistdocs": "web-automation-frontend",
    "gsap": "web-automation-frontend", "micro": "web-automation-frontend",
    "next-forge": "web-automation-frontend", "nextjs": "web-automation-frontend",
    "react-best-practices": "web-automation-frontend",
    "remotion-best-practices": "web-automation-frontend", "shadcn": "web-automation-frontend",
    "swr": "web-automation-frontend", "turbopack": "web-automation-frontend",
    "turborepo": "web-automation-frontend", "ui-toolkit": "web-automation-frontend",
    "v0-dev": "web-automation-frontend", "web-perf": "web-automation-frontend",
    # Cloud, Infra & MLOps
    "airflow": "cloud-devops", "mlflow-onboarding": "cloud-devops",
    "vllm-deploy-simple": "cloud-devops", "wandb-primary": "cloud-devops",
    "terraform": "cloud-devops", "wizard": "cloud-devops",
    # Data Science, Stats & Scientific Computing
    "numba": "data-science-compute", "lifelines": "data-science-compute",
    "great-expectations": "data-science-compute", "scikit-image": "data-science-compute",
    "pandas": "data-science-compute", "plotly": "data-science-compute",
    # Machine Learning & AI
    "dspy": "ml-ai", "jax-best-practices": "ml-ai",
    "llamaindex-development": "ml-ai", "qdrant-clients-sdk": "ml-ai",
    # Single-Cell, RNA-seq & Functional Genomics
    "mofaplus-multi-omics": "single-cell-rnaseq",
    "muon-multiomics-singlecell": "single-cell-rnaseq",
    "cell-communication": "single-cell-rnaseq",
    # Drug Discovery, Cheminformatics & Structural Biology
    "pymol": "drug-discovery-chem", "molecular-docking": "drug-discovery-chem",
    # Sequence Analysis, NGS & Phylogenetics
    "alterlab-qiime2-amplicon": "sequence-phylogenetics",
    "fastp-fastq-preprocessing": "sequence-phylogenetics",
    "viennarna-structure-prediction": "sequence-phylogenetics",
    # Scientific Writing, Figures & Publishing
    "edit-article": "research-writing", "writing-beats": "research-writing",
    "writing-fragments": "research-writing", "writing-shape": "research-writing",
    # Software Development & Engineering
    "codebase-design": "software-dev", "diagnosing-bugs": "software-dev",
    "domain-modeling": "software-dev", "git-guardrails-claude-code": "software-dev",
    "handoff": "software-dev", "implement": "software-dev",
    "improve-codebase-architecture": "software-dev", "migrate-to-shoehorn": "software-dev",
    "prototype": "software-dev", "qa": "software-dev",
    "request-refactor-plan": "software-dev", "resolving-merge-conflicts": "software-dev",
    "setup-pre-commit": "software-dev", "tdd": "software-dev",
    "to-tickets": "software-dev", "to-spec": "software-dev", "triage": "software-dev",
    "ubiquitous-language": "software-dev", "teach": "software-dev",
    "scaffold-exercises": "software-dev", "modern-typescript": "software-dev",
    "research": "software-dev", "claude-handoff": "software-dev",
    "setup-ts-deep-modules": "software-dev",
    # Vault, Skills & Workflow Meta
    "ask-matt": "vault-meta", "obsidian-vault": "vault-meta",
    "setup-matt-pocock-skills": "vault-meta", "writing-great-skills": "vault-meta",
    "writing-for-agents": "vault-meta",
    # Reasoning, Ideation & Decision
    "decision-mapping": "reasoning-ideation", "grill-me": "reasoning-ideation",
    "grill-with-docs": "reasoning-ideation", "grilling": "reasoning-ideation",
    "wayfinder": "reasoning-ideation", "loop-me": "reasoning-ideation",
    # Communication & Productivity Suites
    "to-questionnaire": "comms-productivity", "wait-what": "comms-productivity",
    # Web Automation, Frontend & Design
    "design-an-interface": "web-automation-frontend",
    "ui-ux-pro-max": "web-automation-frontend",
    "banner-design": "web-automation-frontend", "brand": "web-automation-frontend",
    "design-system": "web-automation-frontend", "design": "web-automation-frontend",
    "slides": "web-automation-frontend", "ui-styling": "web-automation-frontend",
    # .NET & C# Development
    "migrate-dotnetfx-to-net": "dotnet-development",
}


def main():
    title_by_key = {k: t for k, t, _, _, _ in CATEGORIES}
    key_by_skill, assigned = {}, {}
    for key, title, scope, related, skills in CATEGORIES:
        for s in skills:
            if s in assigned:
                print(f"WARNING: {s} in both {assigned[s]} and {key}", file=sys.stderr)
            assigned[s] = key
            key_by_skill[s] = key

    try:
        on_disk = discover_skills()
    except OSError as exc:
        print(f"ERROR: cannot discover skills in {VAULT_DIR}: {exc}", file=sys.stderr)
        return 1
    imported_profiles = {
        skill
        for skill in on_disk
        if skill != DISPATCHER and is_scientific_agents_profile(skill)
    }
    valid_bridge_domains = tuple(
        key for key, *_ in CATEGORIES if key != EXPERT_DOMAIN
    )
    try:
        catalog_profiles = load_catalog_profiles(CATALOG_PATH)
        taxonomy: ExpertTaxonomy = load_taxonomy(
            TAXONOMY_PATH,
            catalog_profiles=catalog_profiles,
            discovered_profiles=imported_profiles,
            valid_bridge_domains=valid_bridge_domains,
        )
    except TaxonomyValidationError as exc:
        print(exc, file=sys.stderr)
        return 1

    try:
        discipline_paths = {
            discipline.id: expert_map_path(EXPERT_MAPS_DIR, discipline.id)
            for discipline in taxonomy.disciplines
        }
    except TaxonomyValidationError as exc:
        print(exc, file=sys.stderr)
        return 1

    discipline_ids = tuple(
        discipline.id for discipline in taxonomy.disciplines
    )
    if GRAPH:
        try:
            update_graph(taxonomy)
        except TaxonomyValidationError as exc:
            print(exc, file=sys.stderr)
            return 1

    os.makedirs(human_root(), exist_ok=True)
    os.makedirs(notes_root(), exist_ok=True)
    os.makedirs(MAPS_DIR, exist_ok=True)
    os.makedirs(EXPERT_MAPS_DIR, exist_ok=True)

    expert_skills = set(imported_profiles)
    if DISPATCHER in on_disk:
        expert_skills.add(DISPATCHER)
    for skill in expert_skills:
        assigned[skill] = EXPERT_DOMAIN
        key_by_skill[skill] = EXPERT_DOMAIN
    # Auto-categorize bundled sub-skills (e.g. gstack/office-hours) into
    # the same domain as their parent bundle.
    for skill in on_disk:
        if "/" in skill and skill not in assigned:
            parent = skill.split("/")[0]
            parent_key = key_by_skill.get(parent)
            if parent_key and parent_key != "uncategorized":
                assigned[skill] = parent_key
                key_by_skill[skill] = parent_key
    for skill, key in EXTRA_ASSIGNMENTS.items():
        if skill in on_disk and skill not in assigned and key in title_by_key:
            assigned[skill] = key
            key_by_skill[skill] = key
    unsorted = sorted(on_disk - set(assigned))
    if unsorted:
        print(f"WARNING: not categorized: {unsorted}", file=sys.stderr)
    for s in unsorted:
        key_by_skill[s] = "uncategorized"

    skills_by_key = {key: [] for key, *_ in CATEGORIES}
    for s in on_disk:
        if is_gstack_subskill(s) or is_ui_ux_pro_max_skill(s):
            continue  # transient optional extras: keep out of committed navigation
        skills_by_key.setdefault(key_by_skill.get(s, "uncategorized"), []).append(s)

    skills_sorted = sorted(on_disk)
    full_desc = {s: read_description(s) for s in skills_sorted}
    short = {s: one_liner(full_desc[s]) for s in skills_sorted}
    # Transient gstack sub-skills are already kept out of cards/maps/subtotals
    # (SCALE-3, above). Exclude them from related-links too, or the committed
    # wrappers churn with install state: with the gstack extra installed, skills
    # like qa/review/pdf gain a dozen gstack-* "Related skills" entries that
    # vanish again on a machine without it. Same intent as is_gstack_subskill's
    # docstring; related-links were the one generated surface it missed.
    related = build_related_excluding(
        skills_sorted,
        full_desc,
        set(expert_skills) | {
            s for s in skills_sorted
            if is_gstack_subskill(s) or is_ui_ux_pro_max_skill(s)
        },
    )
    discipline_titles = {
        discipline.id: discipline.title for discipline in taxonomy.disciplines
    }

    # ---- wrapper notes -----------------------------------------------------
    for s in skills_sorted:
        if is_ui_ux_pro_max_skill(s):
            continue
        key = key_by_skill.get(s, "uncategorized")
        dtitle = title_by_key.get(key, "Uncategorized")
        ex = parse_existing(s, key)
        rendered = render_wrapper(
            s,
            key=key,
            domain_title=dtitle,
            description=full_desc[s],
            short_descriptions=short,
            related=related.get(s, set()),
            existing=ex,
            today=TODAY,
            force_aliases=FORCE_ALIASES,
            domain_by_skill=key_by_skill,
            expert_assignment=taxonomy.profiles.get(s),
            discipline_titles=discipline_titles,
            category_titles=title_by_key,
            bridge_domain_order=valid_bridge_domains,
        )
        destination = note_path(s, key)
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        with open(destination, "w", encoding="utf-8") as f:
            f.write(rendered)

    # ---- map notes ---------------------------------------------------------
    for key, title, scope, related_keys, skills in CATEGORIES:
        path = os.path.join(MAPS_DIR, f"{key}.md")
        created = existing_created(path)
        if key == EXPERT_DOMAIN:
            expert_outputs = [
                (
                    Path(path),
                    render_expert_master_map(
                        taxonomy=taxonomy,
                        title=title,
                        scope=scope,
                        created=created,
                        domain_by_skill=key_by_skill,
                    ),
                )
            ]
            for discipline in taxonomy.disciplines:
                discipline_path = discipline_paths[discipline.id]
                discipline_created = existing_created(discipline_path)
                expert_outputs.append(
                    (
                        discipline_path,
                        render_expert_discipline_map(
                            discipline=discipline,
                            taxonomy=taxonomy,
                            short_descriptions=short,
                            category_titles=title_by_key,
                            bridge_domain_order=valid_bridge_domains,
                            created=discipline_created,
                            domain_by_skill=key_by_skill,
                        ),
                    )
                )
            for output_path, rendered in expert_outputs:
                atomic_write_text(output_path, rendered)
            if discipline_ids:
                prune_stale_expert_maps(EXPERT_MAPS_DIR, discipline_ids)
            continue
        live = sorted(skills_by_key.get(key, []))
        L = ["---", f"title: {title}", "tags:", "  - skill-map", f"created: {created}", "---", "",
             f"# {title}", "", "> [!abstract] Scope", f"> {scope}", "",
             "[Back to Skill Index](../index.md)", ""]
        rel = [f"[{title_by_key[r]}]({r}.md)" for r in related_keys if r in title_by_key]
        if rel:
            L += ["**Related maps:** " + " | ".join(rel), ""]
        L += [f"## Skills ({len(live)})", ""]
        L += [
            f"- [{s}]({note_link(s, key_by_skill, '../')}) — {short[s]}" for s in live
        ]
        L.append("")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(L))

    # ---- index -------------------------------------------------------------
    # Count excludes transient optional-extra install state.
    total = sum(
        1 for s in on_disk
        if not is_gstack_subskill(s) and not is_ui_ux_pro_max_skill(s)
    )
    index_path = os.path.join(human_root(), "index.md")
    index_created = existing_created(index_path)
    I = ["---", "title: Skills Index", "tags:", "  - moc", "  - skill-index",
         f"created: {index_created}", "---", "", "# Skills Index", "",
         f"A navigable map of the **{total} agent skills** in this vault, grouped into "
         f"{len(CATEGORIES)} domains. Each entry links to a per-skill note that wraps the "
         f"original `SKILL.md` and holds your personal notes, status, and aliases.", "",
         "> [!tip] How to navigate",
         "> - **Find by name/synonym:** quick-switcher or grep (skills carry aliases like `DESeq2`, `single cell`).",
         "> - **Browse a domain:** open a map below for grouped, cross-linked skills.",
         "> - **Filter by attribute:** open [skills.base](skills.base) to sort/filter by domain, status, rating.",
         "> - **Navigate by goal:** see [Workflows & recipes](recipes/index.md).",
         "> - **See connections:** Obsidian Graph view is color-grouped by domain.", "",
         "## Quick access", "",
         "- [Filterable table — skills.base](skills.base)  ·  sort & filter all skills by domain / status / rating",
         "- [Workflows & recipes](recipes/index.md)  ·  goal-oriented chains of skills",
         "", "## Browse by domain", ""]
    for key, title, scope, related_keys, skills in CATEGORIES:
        live = sorted(skills_by_key.get(key, []))
        I += [f"### [{title}](maps/{key}.md)  ·  {len(live)} skills", "", scope, ""]
        preview = live[:6]
        chips = ", ".join(f"[{s}]({note_link(s, key_by_skill)})" for s in preview)
        more = f" … [see all {len(live)} →](maps/{key}.md)" if len(live) > len(preview) else ""
        I += [chips + more, ""]
    # Flat A–Z excludes the expert-persona profiles (browse them via the
    # Scientific Expert Profiles map) and bundled sub-skills (e.g. gstack/*),
    # so the actionable tool skills stay scannable. See VAULT-AUDIT USE-3 / SCALE-3.
    az_skills = [
        s for s in on_disk
        if key_by_skill.get(s) != EXPERT_DOMAIN
        and "/" not in s
        and not is_gstack_subskill(s)
        and not is_ui_ux_pro_max_skill(s)
    ]
    persona_count = len(skills_by_key.get(EXPERT_DOMAIN, []))
    I += ["## All skills (A–Z)", "",
          f"_{len(az_skills)} tool skills. The {persona_count} expert-persona entries "
          f"(discipline profiles + the scientific-agents dispatcher) are omitted here to "
          f"keep this list scannable — browse them via "
          f"[Scientific Expert Profiles](maps/{EXPERT_DOMAIN}.md)._", ""]
    cur, bucket = None, []
    def flush():
        if bucket:
            I.append(" · ".join(bucket)); I.append("")
    for s in sorted(az_skills, key=str.lower):
        letter = s[0].upper()
        if letter != cur:
            flush(); bucket = []; cur = letter; I.append(f"**{letter}**")
        bucket.append(f"[{s}]({note_link(s, key_by_skill)})")
    flush()
    unsorted_display = [
        s for s in unsorted
        if not is_gstack_subskill(s) and not is_ui_ux_pro_max_skill(s)
    ]
    if unsorted_display:
        I += ["## Uncategorized", ""]
        I += [
            f"- [{s}]({note_link(s, key_by_skill)}) — {short[s]}"
            for s in unsorted_display
        ]
        I.append("")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("\n".join(I))

    # ---- prune orphaned wrappers ------------------------------------------
    pruned = []
    if PRUNE:
        # A wrapper is live if it sits at the exact path this build would write
        # it to; anything else under vault/notes/ is an orphan, including notes
        # left behind at a previous domain when a skill was recategorised.
        live_notes = {note_path(s, key_by_skill.get(s, "uncategorized")) for s in on_disk}
        for directory, _, filenames in os.walk(notes_root()):
            for f in filenames:
                if not f.endswith(".md") or f.startswith("."):
                    continue
                p = os.path.join(directory, f)
                if p in live_notes:
                    continue
                try:
                    txt = open(p, encoding="utf-8").read()
                except OSError:
                    continue
                # only delete files that are clearly generated wrappers
                if re.search(r"^source:\s*.+/SKILL\.md\s*$", txt, re.MULTILINE) or PERSONAL_MARKER in txt:
                    os.remove(p)
                    pruned.append(f[:-3])
        # Drop domain folders emptied by the sweep.
        for directory, _, _ in sorted(os.walk(notes_root()), reverse=True):
            if directory != notes_root() and not os.listdir(directory):
                os.rmdir(directory)
        if pruned:
            print(f"PRUNED {len(pruned)} orphan wrapper(s): {', '.join(sorted(pruned))}",
                  file=sys.stderr)

    edge_count = sum(len(v) for v in related.values()) // 2
    generated_wrapper_count = sum(
        1 for s in on_disk if not is_ui_ux_pro_max_skill(s)
    )
    print(f"OK: {generated_wrapper_count} wrappers ({total} indexed skills), {len(CATEGORIES)} maps, "
          f"{edge_count} related-links, unsorted={len(unsorted_display)} "
          f"(+{len(unsorted) - len(unsorted_display)} gstack), pruned={len(pruned)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
