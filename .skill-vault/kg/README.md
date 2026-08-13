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

| | description-only (`build_related`) | knowledge graph |
|---|---:|---:|
| edges | 1,277 | 13,007 |
| mean degree | 1.40 | 5.42 |
| skills with **no** relations | **875 (48.1%)** | **133 (7.3%)** |

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
