# Vault Knowledge Graph — design

**Status:** design
**Date:** 2026-08-12
**Scope:** turn `skillquarium` from a description-matched skill list into a
continuously-growing knowledge base that agents can **grow**, **retrieve**, and
**validate**.

---

## 1. The problem, measured

Everything below was measured against this repo at `b8c7914f`, not assumed.

| Measure | Value | Implication |
|---|---:|---|
| Skills with a frontmatter description | 1818 | — |
| Total description text | **~162k tokens** | Knowing *what exists* costs a whole context window |
| Median description length | 344 chars | Prose, not structure — nothing is queryable |
| `build_related` graph: nodes / edges | 1818 / **1239** | — |
| Mean degree | **1.36** | — |
| **Skills with zero relations** | **920 (51%)** | Half the vault is disconnected |
| Median degree | **0** | The typical skill has *no* neighbours |
| `graphify-out/` | **absent** | The graph layer `AGENTS.md` advertises does not exist |
| Skills carrying usage feedback | **0** | `status: untried` on all 1818; nothing writes back |

Three distinct failures hide behind "search by description is inefficient":

**(a) Retrieval is flat and past its scaling limit.** Claude Code loads all 1818
name+description pairs and pattern-matches on prose. Tool-retrieval research puts
the breakdown point for flat retrieval at roughly one thousand tools; we are at
1818. The fix in the literature is uniformly hierarchical or cluster-based
retrieval, not better descriptions.

**(b) The "graph" is a string match, not a graph.** `build_related()` draws an
edge only when skill B's *literal name* appears in skill A's description. That is
why `scanpy` links to `harmonypy` (whose description says "scanpy") but 920
skills link to nothing. Degree-0 is the median. There is no relation *type* — an
edge means "mentioned", which is not a fact you can reason with.

**(c) Nothing closes the loop.** No skill records that it was used, worked, or
failed. The vault cannot get better from being used, which is the entire
difference between a library and a knowledge base.

A fourth issue is latent but decisive: **the vault's own vocabulary is
ambiguous.** Probing for data-format terms, `rds` matches both R's serialized
data objects and Amazon RDS; `alignment` matches sequence alignment and text
alignment. Strings cannot carry that distinction. Identifiers can. This is the
concrete argument for an ontology here, and it emerged from measurement rather
than from taste.

---

## 2. What the prior art already settled

The user's instinct — "people are doing that already" — is correct, and the
convergence is strong enough to borrow rather than invent.

- **[SkillGraph](https://arxiv.org/html/2605.12039)** organises agent skills as a
  *directed, typed* graph and co-evolves it with use. Edge types: `prerequisite`,
  `enhancement`, `co-occurrence`. Nodes carry `usage`, `success`, `success_rate`.
  Graph operations: **insert** (from failed trajectories), **merge** (>85%
  neighbourhood Jaccard), **split** (moderate success + high usage), **deprecate**
  (≥20 uses, <15% success). Edges reinforce on success (+0.05), decay
  multiplicatively (γ=0.99), and prune below w=0.05. Retrieval is backward BFS for
  prerequisites, forward beam for dependents, then topological sort, capped at 8.
  **This is precisely the grow/retrieve/validate loop being asked for**, already
  specified with thresholds.

- **[Agent-as-a-Graph](https://arxiv.org/pdf/2511.18194)** hybridises vector seed
  selection with graph traversal: **15–25% recall improvement** on queries needing
  tool composition, **~30% fewer irrelevant suggestions**, at ~5ms traversal
  overhead. The gains concentrate exactly where flat retrieval fails — composition.

- **[Tools Are Not Islands (HYSET)](https://arxiv.org/html/2607.25718v2)** is the
  sharpest result for our case: a retriever with **Recall@3 of 68.6%** had
  **COMP@3 of only 39.7%**. Individually-relevant is not collectively-sufficient.
  Retrieving *sets* (hyperedges) beat top-k: **77.55% vs 70.01% COMP@5**.

- **[MCP-Zero](https://arxiv.org/pdf/2506.01056)** and hierarchical retrievers
  (AnyTool's category→tool→API, ToolRerank) confirm the coarse-to-fine routing shape.

The HYSET gap is the one to internalise. An agent that finds `scanpy` but misses
`harmonypy`, `pydeseq2`, and `pathway-enrichment` has high recall and has still
failed the user. **The vault already knows these sets — they are the 8 hand-written
recipes.** Eight hyperedges for 1818 skills is the asset that is under-exploited.

---

## 3. Design principles

1. **`skills/<name>/SKILL.md` stays the source of truth.** It is upstream-managed;
   the KG is a sibling layer, never an edit to it. Non-negotiable — it is what
   `update-skills.yml` depends on.
2. **Every edge carries provenance and confidence.** Retrieval consumes only edges
   above a floor. An LLM suggestion is not a fact.
3. **Deterministic where possible, LLM only where bounded.** The measured
   extraction results (§5) decide this per relation, rather than a blanket policy.
4. **Stdlib only, no services.** CI is `python3.12` + `unittest` with no
   `requirements.txt`; the vault prizes a `ripgrep` fallback. The KG must degrade
   to grep, never require a server.
5. **Humans keep Obsidian.** The graph *enriches* `build.py` output; it does not
   replace the navigation layer.
6. **Absence of an edge is not absence of a relation.** Open-world by default;
   closed-world only inside explicit validation shapes.

### Deliberate non-goal: OWL 2 DL

An OWL 2 DL ontology with Protégé and HermiT is the wrong instrument. Required
expressivity is transitive closure over chaining, SKOS-style broader/narrower over
domains, and constraint checks — that is **OWL 2 RL / Datalog-shaped
forward-chaining**, at an ABox of 1818 nodes, inside an agent's CLI latency budget.
A Java toolchain and tableaux reasoning buy nothing here and would be the
"brittle symbolic tower disconnected from data" failure mode.

We ship **JSON-LD + Turtle export** so the graph *can* be loaded into GraphDB or
Protégé if that ever changes. The runtime store stays deliberately dumb: SQLite
(stdlib `sqlite3`, FTS5 for lexical search, single rebuildable file).

---

## 4. The ontology (TBox)

### Entity types

| Type | Meaning | Count (est.) |
|---|---|---|
| `Skill` | a `SKILL.md` folder — the unit of instruction | 1818 |
| `Tool` | underlying software a skill wraps (Scanpy, samtools, IQ-TREE) | ~400 |
| `Artifact` | a **typed** data object (`artifact:fastq`, `artifact:h5ad`) | ~120 |
| `Capability` | a verb-phrase of what gets done (`cap:batch-correction`) | ~200 |
| `Domain` | existing 32 domains, as a SKOS scheme with `broader`/`narrower` | 32 |
| `Discipline` | existing `scientific-expert-taxonomy.json` disciplines | 12 |
| `Recipe` | a named **hyperedge**: ordered skill set achieving a goal | 8 → grows |
| `Observation` | an episode: query, retrieved, used, outcome | grows |

`Artifact` and `Tool` are the two new entity types doing the real work.
Artifacts make *chaining* computable; tools make *alternatives* computable
(`scanpy` and `seurat` are alternatives because they implement the same
capabilities over the same artifacts via different tools).

Terms are **identifiers, not strings** — `artifact:r-serialized-data` and
`service:aws-rds` are distinct nodes that the token `rds` maps to ambiguously.
The lexicon records that ambiguity explicitly instead of silently picking one.

### Object properties

```
implements      Skill    → Capability
wraps           Skill    → Tool
consumes        Skill    → Artifact
produces        Skill    → Artifact
touches         Skill    → Artifact      # undirected fallback; high recall
in_domain       Skill    → Domain        # n:m — was 1:1, which was already lossy
prerequisite_of Skill    → Skill
enhances        Skill    → Skill
co_occurs_with  Skill    → Skill         # weighted, learned from use
alternative_to  Skill    → Skill
specializes     Skill    → Skill         # scrna-preprocessing-clustering ⊏ scanpy
supersedes      Skill    → Skill         # deprecation
has_step        Recipe   → Skill         # ordered
```

### Materialised rules (forward-chained, RL-profile)

```
chains_to(A,B)      ⟸ produces(A,x) ∧ consumes(B,x) ∧ A≠B
alternative_to(A,B) ⟸ implements(A,c) ∧ implements(B,c)
                      ∧ wraps(A,t₁) ∧ wraps(B,t₂) ∧ t₁≠t₂
                      ∧ jaccard(sig(A),sig(B)) ≥ 0.5
co_occurs_with(A,B) ⟸ ∃ Recipe r: has_step(r,A) ∧ has_step(r,B)
```

`alternative_to` is near-equivalence, so it is **never** asserted from embedding
similarity or an LLM suggestion alone — it requires the shared-capability *and*
signature-overlap conditions, or human assertion.

### Edge record

```json
{"src","rel","dst","weight","provenance","justification",
 "status","first_seen","last_seen"}
```

`provenance` ∈ `ASSERTED` (curated file) · `EXTRACTED` (deterministic parse) ·
`INFERRED` (rule-derived) · `OBSERVED` (usage telemetry) · `PROPOSED` (LLM,
unreviewed). **`PROPOSED` edges never participate in retrieval until promoted.**

### Node statistics (SkillGraph)

```
uses · successes · success_rate · last_used · first_seen · deprecated
```

---

## 5. Extraction: what is deterministic, and what is not

This section is empirical. Both experiments were run over all 1818 skills.

**Artifact *mention* extracts reliably.** A lexicon of file formats and data-type
names matched **1438 / 1818 skills (79%)**, mean 1.5 artifacts per skill, with
domain-meaningful density (`h5ad` 129, `fastq` 90, `vcf` 85, `bam` 54, `PDB` 38,
`SMILES` 30). → `touches` is EXTRACTED, cheap, high-recall.

**Artifact *direction* does not extract by regex.** Directional cue patterns
("from FASTQ", "produces …", "converts … to") reached only **9% consumes / 9%
produces / 4% both**, and inspection showed the hits are substantially wrong:

| Skill | Extracted | Reality |
|---|---|---|
| `airtable-cli` | consumes `rds` | Amazon RDS — wrong sense entirely |
| `atac-seq` | BAM → SAM | backwards |
| `bio-orchestrator` | PDB/SAM/VCF → FASTQ | badly backwards |

4375 candidate `chains_to` edges from a 4% base is a hairball, not knowledge.
**Rejected.** Direction must come from higher-confidence sources instead:

| Source | Provenance | Coverage | Notes |
|---|---|---|---|
| Recipes (ordered steps + mermaid flowcharts) | `ASSERTED` | 8 recipes, free | Direction is already human-authored |
| Usage episodes (A ran before B on the same data) | `OBSERVED` | grows | Strongest signal; the learning loop |
| Per-skill LLM signature proposal | `PROPOSED` | all, gated | Bounded task, reviewed before promotion |

This is where the LLM belongs: proposing a **typed signature for one skill at a
time** against a closed lexicon — a bounded, checkable task — never inventing
edges *between* skills, and never asserting `alternative_to`.

**Consequence for the build:** the graph is **staged by confidence**. It is
useful on day one from EXTRACTED `touches` + ASSERTED recipes, and the directed
skeleton fills in as episodes accumulate. That staging *is* the continuous
learning, rather than a caveat about it.

---

## 6. Retrieval

One entry point: `vault-query "<task>" [--budget TOKENS] [--k N]`.

**Stage A — Route (cheap).** Match the query against `Capability` and `Domain`
labels only. That index is ~200 capabilities + 32 domains ≈ **2k tokens, versus
162k** for every description. Coarse-to-fine, as in AnyTool.

**Stage B — Seed.** Within the routed subgraph, rank skills by BM25 (FTS5) over
name + aliases + description + capability labels, weighted by node prior
(`success_rate`, recency).

**Stage C — Expand** (Agent-as-a-Graph):
- backward BFS depth 2 over `prerequisite_of` → foundations
- forward beam width 3 over `chains_to` → pipeline completion
- one hop over `alternative_to` → options, **labelled as alternatives, not additions**

**Stage D — Set-complete (the HYSET lesson).** If the candidate set intersects a
`Recipe` hyperedge by ≥2 members, pull that recipe's remaining steps. This is a
deterministic stand-in for learned hyperedge prediction — and it is exactly what
the vault's recipes already encode. It is the single highest-leverage stage,
because COMP, not Recall, is what makes an agent's answer complete.

**Stage E — Order and budget.** Topological sort by `chains_to` / `prerequisite_of`,
cap at K (default 8, per SkillGraph), emit under the token budget.

Every returned skill ships **why it was included**, as the edge path:

```
pathway-enrichment
  why: bulk-rnaseq-to-pathways step 4 ← recipe set-completion (ASSERTED)
  ← rnaseq-de produces artifact:ranked-gene-list which it consumes
```

The explanation is the audit trail. A retrieval that cannot say why it returned
something cannot be validated, and an agent cannot judge whether to trust it.

---

## 7. Growth

Four sources, in increasing autonomy:

1. **Upstream sync** — exists. New `SKILL.md` → extractor → node + EXTRACTED edges.
   Hooks into the existing `update-skills.yml`.
2. **Observation ingestion** — new. Agents append JSONL episodes; this accrues
   `co_occurs_with`, node stats, and directional evidence. Must be near-zero-cost
   to emit or it will not happen: one append per skill invocation, via the hook
   mechanism agents already have.
3. **Gap mining** — new. Queries that route to nothing, plus capabilities with zero
   skills, become a reviewable queue feeding `skill-builder` / `find-skills`.
   **This is what makes the vault grow rather than merely reorganise.**
4. **LLM proposal pass** — new, gated. Periodically proposes signatures and
   capability assignments as `PROPOSED`; promotion is a separate reviewed step.

Graph maintenance runs SkillGraph's operations on the accumulated statistics:
merge >0.85 neighbourhood Jaccard, split moderate-success/high-usage nodes,
deprecate ≥20 uses at <15% success, reinforce +0.05 on success, decay γ=0.99,
prune below w=0.05.

---

## 8. Validation

`vault-validate`, run in CI beside the existing `unittest` suite.

**Shape checks** (SHACL-shaped, stdlib — logical consistency is not the risk here,
data quality is):
- every `Skill` has ≥1 `Capability` and ≥1 `Domain`
- **orphan rate must not regress** — the headline metric, 51% today, target <5%
- every non-EXTRACTED edge carries a justification
- `alternative_to` is symmetric; `prerequisite_of` and `chains_to` are acyclic
- no `PROPOSED` edge is reachable by retrieval
- deprecated skills are unreferenced by active recipes
- every lexicon term maps to exactly one identifier, or is explicitly marked ambiguous

**Competency questions** — the ontology's real test suite. Each is a query with
expected bindings, and a regression test:

| # | Question | Exercises |
|---|---|---|
| CQ1 | FASTQ → pathway results: what chain? | `chains_to` closure |
| CQ2 | Python alternative to Seurat? | `wraps` + `alternative_to` |
| CQ3 | What must I know before `scvi-tools`? | `prerequisite_of` backward BFS |
| CQ4 | What covers batch correction? | `implements` |
| CQ5 | "single-cell analysis" → a *complete* set | set-completion (COMP, not Recall) |
| CQ6 | Which capabilities have no skill? | gap mining |
| CQ7 | Which skills are stale or failing? | node statistics |

CQ5 and CQ6 matter most: CQ5 is the HYSET failure this design exists to fix, and
CQ6 is the query that makes the vault *grow*.

---

## 9. Layout

```
.skill-vault/ontology/schema.json        TBox, schema_version'd  (follows the
                                         existing scientific-expert-taxonomy pattern)
.skill-vault/ontology/lexicon.json       Tool / Artifact / Capability vocabularies,
                                         with explicit ambiguity records
.skill-vault/ontology/assertions/*.json  Curated ASSERTED edges (small, reviewed)
.skill-vault/kg/build_kg.py              extract + infer → graph.json
.skill-vault/kg/query.py                 the retrieval CLI
.skill-vault/kg/validate.py              shapes + competency questions
.skill-vault/observations/*.jsonl        append-only episode log
vault/graph/graph.json                   built, committed, diffable
vault/graph/graph.db                     derived SQLite, gitignored, rebuildable
```

`build.py` gains a read from `graph.json` so wrapper notes get **typed**, non-empty
`Related skills` — the 51% orphan problem surfaces in Obsidian too, and this is
where humans would notice it fixed.

---

## 10. Sequencing

| Phase | Delivers | Gate |
|---|---|---|
| 1 | Schema, lexicon, extractor, `graph.json`, validator, CQ tests | Orphan rate <5%; CQ1–4,6,7 pass |
| 2 | `vault-query` CLI with routing + expansion + set-completion | CQ5 passes; retrieval under budget |
| 3 | Observation ingestion + node stats + `co_occurs_with` | Episodes flow from a real session |
| 4 | Graph maintenance ops; gap queue → `skill-builder` | First LLM-proposed edge promoted by review |
| 5 | `build.py` enrichment; JSON-LD/Turtle export | Obsidian shows typed relations |

Phase 1 is the honest test of the whole design: if the orphan rate does not
collapse from a deterministic pass, the ontology is wrong and the rest should not
be built.

---

## Sources

- [SkillGraph: Skill-Augmented Reinforcement Learning for Agents via Evolving Skill Graphs](https://arxiv.org/html/2605.12039)
- [Agent-as-a-Graph: Knowledge Graph-Based Tool and Agent Retrieval for LLM Multi-Agent Systems](https://arxiv.org/pdf/2511.18194)
- [Tools Are Not Islands: Set-Level Tool Retrieval via Query-Conditioned Hyperedge Prediction](https://arxiv.org/html/2607.25718v2)
- [MCP-Zero: Active Tool Discovery for Autonomous LLM Agents](https://arxiv.org/pdf/2506.01056)
- [Tool-to-Agent Retrieval: Bridging Tools and Agents for Scalable LLM Multi-Agent Systems](https://arxiv.org/abs/2511.01854)
- [A Survey of Graph Retrieval-Augmented Generation for Customized Large Language Models](https://arxiv.org/pdf/2501.13958)
- [Awesome-GraphRAG](https://github.com/DEEP-PolyU/Awesome-GraphRAG)

---

## Addendum (2026-08-12): the RDF layer, and a correction

Section 3 rejected "OWL 2 DL with Protégé and HermiT" and then treated that as
settling RDF altogether. Those are two different questions and bundling them was
wrong. `rdflib` and `pyshacl` are pure-Python pip installs, not a Java stack, and
hand-writing a SHACL-*shaped* validator in Python bought nothing that the real
thing does not do better.

Measured on the real graph before deciding:

| | |
|---|---|
| RDF export | 29,952 triples, **2.5 MB** TriG — smaller than the 5.2 MB JSON |
| export time | 0.7 s |
| pySHACL validation | **8.0 s**, conforms |
| SPARQL competency questions | 1–270 ms |
| injected violations caught | 5/5 classes (missing domain, cycle, asymmetry, leaked PROPOSED, out-of-range rate) |

**What changed.** Added `to_rdf.py`, `ontology/shapes.ttl`, `ontology/cq/*.rq`,
and a `--shacl` mode on `validate.py`. Provenance now uses PROV-O with edges
partitioned into named graphs per level, so excluding `PROPOSED` is structural
rather than a convention every caller must honour. Domains are `skos:Concept`.

**What did not change.** The JSON graph remains the runtime store and `query.py`
remains dependency-free — that is the property the vault prizes and the one
agents rely on. The RDF layer is additive and degrades to `NOT_YET`.

**Two bugs the RDF layer surfaced that the Python validator hid.**

1. `ExpertProfile` was not a subclass of `Skill`, so every shape and query
   targeting `Skill` silently skipped 504 of 1818 nodes. Instances are now typed
   as both.
2. "Orphan" meant two different things in two places — the metric excluded
   `touches` while the prose implied otherwise. The SPARQL and Python paths now
   cross-validate at 133, with a test asserting they agree.

Writing constraints declaratively is what made both visible. That is the
argument for this layer, more than interop is.

**Still rejected:** OWL 2 DL, Protégé, HermiT, tableaux reasoning. The required
expressivity is unchanged — RL-shaped forward chaining plus constraint checking —
and pySHACL covers it without a Java toolchain.
