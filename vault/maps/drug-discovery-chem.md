---
title: Drug Discovery, Cheminformatics & Structural Biology
tags:
  - skill-map
created: 2026-06-13
---

# Drug Discovery, Cheminformatics & Structural Biology

> [!abstract] Scope
> Small-molecule and protein modeling: cheminformatics, docking, structure prediction, and target validation.

[Back to Skill Index](../index.md)

**Related maps:** [Proteomics & Metabolomics](proteomics-metabolomics.md) | [Sequence Analysis, NGS & Phylogenetics](sequence-phylogenetics.md) | [Bio Databases, Lab & Cloud Platforms](bio-databases-platforms.md) | [Machine Learning & AI](ml-ai.md)

## Skills (66)

- [adaptyv](../notes/drug-discovery-chem/adaptyv.md) — How to use the Adaptyv Bio Foundry API and Python SDK for protein experiment design, submission, and results retrieval
- [alphafold-skill](../notes/drug-discovery-chem/alphafold-skill.md) — Submit compact AlphaFold Protein Structure Database API requests for prediction, UniProt summary, sequence summary, and annotation lookups
- [bindingdb-skill](../notes/drug-discovery-chem/bindingdb-skill.md) — Submit compact BindingDB REST API requests for ligand-target binding lookups by PDB, UniProt, or similarity search
- [boltz-check-status](../notes/drug-discovery-chem/boltz-check-status.md) — Boltz job status and result recovery. Use when listing jobs, checking progress, resuming downloads, recovering results, or downloading an existing job ID
- [boltz-cli-setup](../notes/drug-discovery-chem/boltz-cli-setup.md) — Boltz CLI setup and auth. Use when installing, updating, verifying, or authenticating `boltz-api`, or fixing missing CLI, PATH, sandbox, browser login, or auth errors
- [boltz-protein-design](../notes/drug-discovery-chem/boltz-protein-design.md) — Design new protein binders with Boltz. Use when generating protein, peptide, antibody, nanobody, or custom binder candidates for a target
- [boltz-protein-screen](../notes/drug-discovery-chem/boltz-protein-screen.md) — Screen existing protein binders with Boltz
- [boltz-small-molecule-adme](../notes/drug-discovery-chem/boltz-small-molecule-adme.md) — Predict Tier-1 ADME/ADMET for small molecules with Boltz from bare SMILES — no target, no docking
- [boltz-small-molecule-design](../notes/drug-discovery-chem/boltz-small-molecule-design.md) — Design new small-molecule binders with Boltz
- [boltz-small-molecule-screen](../notes/drug-discovery-chem/boltz-small-molecule-screen.md) — Screen existing small-molecule libraries with Boltz
- [boltz-structure-and-binding](../notes/drug-discovery-chem/boltz-structure-and-binding.md) — Predict structures and binding for one defined complex with Boltz
- [boltz2-nim](../notes/drug-discovery-chem/boltz2-nim.md) — Use Boltz2 NIM for biomolecular structure prediction and binding affinity
- [chebi-skill](../notes/drug-discovery-chem/chebi-skill.md) — Submit compact ChEBI 2.0 API requests for chemical search, compound lookup, ontology traversal, and structure metadata
- [chembl-skill](../notes/drug-discovery-chem/chembl-skill.md) — Submit compact ChEMBL API requests for activity, molecule, target, mechanism, and text-search endpoints
- [cobrapy](../notes/drug-discovery-chem/cobrapy.md) — Constraint-based metabolic modeling (COBRA)
- [colabfold](../notes/drug-discovery-chem/colabfold.md) — Fast AlphaFold2/ColabFold protein structure prediction
- [complexa-design](../notes/drug-discovery-chem/complexa-design.md) — End-to-end Proteina-Complexa design pipeline driver
- [complexa-evaluate-pdbs](../notes/drug-discovery-chem/complexa-evaluate-pdbs.md) — Standalone evaluation of an existing PDB directory with Proteina-Complexa
- [complexa-setup](../notes/drug-discovery-chem/complexa-setup.md) — First-time setup, environment configuration, and model-weight installation for Proteina-Complexa
- [complexa-slurm](../notes/drug-discovery-chem/complexa-slurm.md) — Use when launching Proteina-Complexa jobs on a remote SLURM cluster, including binder search, LaProteina design or training, multi-node runs, sbatch, remote GPU jobs, Hydra sweeps...
- [complexa-sweep](../notes/drug-discovery-chem/complexa-sweep.md) — Use this skill whenever the user wants to run a parameter sweep over a Proteina-Complexa design pipeline — cartesian-product hyperparameter scans, Pareto search over...
- [complexa-target](../notes/drug-discovery-chem/complexa-target.md) — Use this skill whenever the user wants to add, register, edit, list, show, or validate a Proteina-Complexa design target for any pipeline — protein binder (default), ligand binder, or...
- [crispr-screen-triage](../notes/drug-discovery-chem/crispr-screen-triage.md) — Deterministic CRISPR screen hit ranking from local guide-level count tables
- [datamol](../notes/drug-discovery-chem/datamol.md) — Pythonic wrapper around RDKit with simplified interface and sensible defaults
- [deepchem](../notes/drug-discovery-chem/deepchem.md) — Molecular ML with diverse featurizers and pre-built datasets
- [depmap](../notes/drug-discovery-chem/depmap.md) — Query the Cancer Dependency Map (DepMap) for cancer cell line gene dependency scores (CRISPR Chronos), drug sensitivity data, and gene effect profiles
- [diffdock](../notes/drug-discovery-chem/diffdock.md) — DiffDock and DiffDock-L molecular docking
- [diffdock-nim](../notes/drug-discovery-chem/diffdock-nim.md) — Run DiffDock molecular docking via NVIDIA NIM to predict small-molecule binding poses against protein targets
- [drug-discovery-pipeline](../notes/drug-discovery-chem/drug-discovery-pipeline.md) — NOTE: molecule and target inputs and your NGC_API_KEY are transmitted to external NVIDIA-hosted API endpoints on every call
- [drug-repurposing-screen](../notes/drug-discovery-chem/drug-repurposing-screen.md) — Objective-driven pooled viability screen analysis: QC, hit calling, context-selectivity, biomarker sweep, and ranked repurposing candidates
- [esm](../notes/drug-discovery-chem/esm.md) — Use when working directly with the `esm` Python SDK, ESM3 or ESMC model IDs, Forge/Biohub inference clients, or ESMFold2 folding workflows
- [foldseek-structural-search](../notes/drug-discovery-chem/foldseek-structural-search.md) — Performs 3D structural searches of proteins against various databases (PDB, AlphaFold, CATH, MGnify, etc.) using the Foldseek API
- [genmol-nim](../notes/drug-discovery-chem/genmol-nim.md) — Generate novel drug-like molecules using the GenMol NIM microservice
- [hmdb-skill](../notes/drug-discovery-chem/hmdb-skill.md) — Submit compact HMDB search requests for metabolites, proteins, diseases, and pathways
- [kermt-add-cmim-pretrain](../notes/drug-discovery-chem/kermt-add-cmim-pretrain.md) — Convert a grover_base checkpoint (encoder-only or encoder + vocab heads) into a hybrid checkpoint by adding a randomly-initialized cMIM decoder + latent_dist, then continue pretraining...
- [kermt-continue-pretrain](../notes/drug-discovery-chem/kermt-continue-pretrain.md) — Continue pretraining from an existing KERMT checkpoint
- [kermt-embed](../notes/drug-discovery-chem/kermt-embed.md) — Extract per-molecule embeddings from any encoder-bearing KERMT checkpoint (grover_base / cmim / hybrid / finetuned)
- [kermt-finetune](../notes/drug-discovery-chem/kermt-finetune.md) — Finetune a pretrained KERMT encoder on a labeled CSV
- [kermt-infer](../notes/drug-discovery-chem/kermt-infer.md) — Run predictions with a finetuned KERMT checkpoint on a SMILES-only CSV
- [kermt-monitor](../notes/drug-discovery-chem/kermt-monitor.md) — Check progress for a detached KERMT run (pretrain, finetune, or any kermt_run_detached invocation)
- [kermt-pretrain-scratch](../notes/drug-discovery-chem/kermt-pretrain-scratch.md) — Pretrain a fresh KERMT model from scratch on a user-provided corpus
- [kermt-setup](../notes/drug-discovery-chem/kermt-setup.md) — Bootstrap the KERMT agent environment — verify host docker + nvidia-container-toolkit, build the kermt:latest image from the repo's Dockerfile if it doesn't yet exist, and run a GPU...
- [medchem](../notes/drug-discovery-chem/medchem.md) — Medicinal chemistry filters for compound triage
- [molecular-docking](../notes/drug-discovery-chem/molecular-docking.md) — Use when running classical protein-ligand docking with AutoDock Vina, smina, or GNINA, including receptor or ligand preparation, search-box setup, docking, pose analysis, virtual...
- [molecular-dynamics](../notes/drug-discovery-chem/molecular-dynamics.md) — Run and analyze molecular dynamics simulations with OpenMM and MDAnalysis
- [molfeat](../notes/drug-discovery-chem/molfeat.md) — Molecular featurization for ML (100+ featurizers)
- [molmim-nim](../notes/drug-discovery-chem/molmim-nim.md) — Use this skill for MolMIM, NVIDIA's BioNeMo NIM microservice for small-molecule latent-space generation and optimization
- [nvmolkit-usage](../notes/drug-discovery-chem/nvmolkit-usage.md) — Write code that calls the installed nvMolKit Python API for GPU-accelerated, batched RDKit-style operations - Morgan fingerprints, Tanimoto/cosine similarity, ETKDG conformer...
- [omics-target-evidence-mapper](../notes/drug-discovery-chem/omics-target-evidence-mapper.md) — Aggregate public target-level evidence across omics and translational sources for research triage
- [openfold2-nim](../notes/drug-discovery-chem/openfold2-nim.md) — Use this skill for OpenFold2, NVIDIA's BioNeMo NIM microservice for monomer protein structure prediction
- [openfold3-nim](../notes/drug-discovery-chem/openfold3-nim.md) — Use this skill for OpenFold3, NVIDIA's BioNeMo NIM microservice for biomolecular structure prediction
- [pharmgkb-skill](../notes/drug-discovery-chem/pharmgkb-skill.md) — Submit compact PharmGKB API requests for genes, variants, clinical annotations, dosing guidelines, and search
- [proteinmpnn-nim](../notes/drug-discovery-chem/proteinmpnn-nim.md) — Run ProteinMPNN inverse folding via NVIDIA NIM to design protein sequences for a target backbone
- [pubchem-pug-skill](../notes/drug-discovery-chem/pubchem-pug-skill.md) — Submit compact PubChem PUG REST requests for compound properties, descriptions, assay summaries, and substance metadata
- [pymol](../notes/drug-discovery-chem/pymol.md) — Visualize, analyze, and render protein and molecular structures using PyMOL
- [pytdc](../notes/drug-discovery-chem/pytdc.md) — Therapeutics Data Commons. AI-ready drug discovery datasets (ADME, toxicity, DTI), benchmarks, scaffold splits, molecular oracles, for therapeutic ML and pharmacological prediction
- [rcsb-pdb-skill](../notes/drug-discovery-chem/rcsb-pdb-skill.md) — Submit compact RCSB PDB requests for core metadata, Search API queries, and FASTA downloads
- [rdkit](../notes/drug-discovery-chem/rdkit.md) — Cheminformatics toolkit for fine-grained molecular control
- [rfdiffusion-nim](../notes/drug-discovery-chem/rfdiffusion-nim.md) — Run RFDiffusion protein backbone design via NVIDIA NIM
- [rhea-skill](../notes/drug-discovery-chem/rhea-skill.md) — Submit compact Rhea reaction search requests for biochemical reactions and reaction IDs
- [rowan](../notes/drug-discovery-chem/rowan.md) — Rowan is a cloud-native molecular modeling and medicinal-chemistry workflow platform with a Python API
- [struct-predictor](../notes/drug-discovery-chem/struct-predictor.md) — Protein structure prediction with Boltz-2
- [structural-biology](../notes/drug-discovery-chem/structural-biology.md) — Structure retrieval, confidence-aware AlphaFold DB usage, coordinate download, PAE and pLDDT interpretation, and structure-guided biological annotation
- [target-validation-scorer](../notes/drug-discovery-chem/target-validation-scorer.md) — Evidence-grounded target validation scoring with GO/NO-GO decisions for drug discovery campaigns
- [torchdrug](../notes/drug-discovery-chem/torchdrug.md) — PyTorch-native graph neural networks for molecules and proteins
- [vmd-mdanalysis-viz](../notes/drug-discovery-chem/vmd-mdanalysis-viz.md) — Headless molecular visualization and trajectory analysis with VMD, MDAnalysis, and GROMACS
