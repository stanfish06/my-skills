# Vault knowledge graph

Turns the vault from a description-matched skill list into a graph agents can
**grow**, **retrieve**, and **validate**. Design and measurements:
[`docs/superpowers/specs/2026-08-12-vault-knowledge-graph-design.md`](../../docs/superpowers/specs/2026-08-12-vault-knowledge-graph-design.md).

## Use it

```bash
python3 .skill-vault/kg/query.py "batch correct single cell data and find markers"
python3 .skill-vault/kg/query.py "raw fastq to enriched pathways" --k 10 --json
```

## Rebuild it

```bash
python3 .skill-vault/kg/build_kg.py     # skills/ + vault/ + observations/ -> vault/graph/graph.json
python3 .skill-vault/kg/validate.py     # shape constraints + competency questions
python3 -m unittest discover -s .skill-vault/tests -p 'test_kg.py'
```

Both run in CI after `build.py`, which must go first — the graph reads domain
assignments from the notes layer.

## Why it beats description matching

Counts below are from the last rebuild and shift as upstream skills land;
the ratios are the point. `build_kg.py` prints current figures.

| | description-only (`build_related`) | knowledge graph |
|---|---:|---:|
| edges | 1,277 | 13,459 |
| mean degree | 1.40 | 5.51 |
| skills with **no** relations | **875 (48.1%)** | **126 (6.7%)** |

Two measured facts drive the whole design:

1. **Scope, not cleverness, was the bottleneck.** `build_related` searched only the
   ~350-char frontmatter description. Searching the SKILL.md body instead is what
   collapses the orphan rate — no model, no embeddings, no new dependencies.
2. **Skill ids that are common English words poison everything.** `github` appears in
   42% of bodies, `workflow` 41%, `start` 37%. Matched naively they make every skill
   a neighbour of every other. IDF separates them automatically (df > 2% ⇒ match only
   in backticks, `skills/<id>` paths, or links), so no hand-maintained blocklist rots.

## Stdlib only

No `requirements.txt`, matching CI (`python3.12` + `unittest`). Nothing here needs a
server, a model, or a network call.

## What is deliberately not built yet

`Capability` and `Tool` are unpopulated, so `alternative_to` (rule R4) is **disabled** —
firing it on a sparse TBox would assert near-equivalence on no evidence. `validate.py`
reports these as `NOT_YET`, not `FAIL`, so the roadmap stays visible instead of hidden
behind a red build. Direction (`consumes`/`produces`) comes only from human-authored
recipe order today; regex direction extraction was measured at 4% coverage with
substantially wrong hits, and was rejected.

## Optional RDF / SHACL layer

The JSON graph stays the runtime store — `query.py` reads it with zero
dependencies, and that property is deliberate. On top of it:

```bash
uv pip install -r .skill-vault/kg/requirements-rdf.txt
python3 .skill-vault/kg/to_rdf.py            # -> vault/graph/graph.nq (+ retrievable.ttl)
python3 .skill-vault/kg/validate.py --shacl  # real pySHACL against ontology/shapes.ttl
```

Measured on the real graph: **~28k triples**, 0.7 s to export, **8 s** to
validate with pySHACL. Without the
packages installed, `--shacl` reports `NOT_YET` and everything else still runs.

### What RDF buys that the stdlib validator cannot do

| | stdlib validator | SHACL |
|---|---|---|
| `chains_to` cycles | hand-rolled DFS with a colour map | `?x vs:chains_to+ ?x` |
| `alternative_to` symmetry | manual pair bookkeeping | `FILTER NOT EXISTS` |
| typo'd / invented predicate | **cannot detect** — only checks fields it knows | `sh:closed` |
| shapes | imperative Python | reviewable data in `shapes.ttl` |
| provenance | a string field | PROV-O activities + named graphs |

The provenance modelling is the substantive win. Edges are partitioned into
named graphs by level, so "PROPOSED must never be retrievable" becomes a
property of the data — you exclude a graph — instead of a filter every caller
has to remember. In the JSON path that rule was only ever a convention.

### Competency questions as SPARQL

`.skill-vault/ontology/cq/*.rq` — declarative, portable, reviewable, and they
run in 1–270 ms. Writing CQ6 this way is what exposed that "orphan" meant two
different things in two places; the SPARQL and Python implementations now
cross-validate at the same number, and a test asserts they agree.

### Interop

`vault/graph/graph.nq` is committed, so it loads into GraphDB, Protégé, Stardog,
or Neo4j n10s without installing the exporter.

It is **sorted N-Quads rather than TriG on purpose.** TriG is prettier and half
the size, but rdflib emits its named graphs in non-deterministic order, so every
rebuild rewrote all 2.5 MB — which the daily cron would commit as pure churn.
Sorted N-Quads is byte-identical for identical input, so git stores only the
statements that actually changed. Run `to_rdf.py --trig` for a readable copy
locally; it is gitignored, as is the `retrievable.ttl` validation intermediate.

### Still not doing OWL 2 DL

No Protégé, HermiT, or tableaux reasoning. The needed expressivity remains
RL-shaped forward chaining plus constraint checking, and pySHACL covers it in
pure Python. That part of the original call stands; ruling out **rdflib** along
with it did not.
