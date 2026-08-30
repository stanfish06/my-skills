# HPO (Human Phenotype Ontology)

## Base URL
```
https://ontology.jax.org/api
```

## Auth
No API key required.

## Important: URL-encode colons in IDs — `HP:0001250` becomes `HP%3A0001250`

## Key Endpoints

| Endpoint | Description |
|----------|-------------|
| `/hp/search?q={query}&limit={n}&page={p}` | Search HPO terms by name. `limit` is the page size — `max` is ignored and the default is 10 |
| `/hp/terms/{id}` | Term details (plural `terms`) |
| `/hp/terms/{id}/children` | Child terms in hierarchy |
| `/hp/terms/{id}/parents` | Parent terms |
| `/hp/terms/{id}/descendants` | All descendant terms |
| `/network/annotation/{id}` | Annotations for an HP term, gene, or disease. Not under `/hp` |

`/network/annotation/{id}` keys off the identifier: `HP:0001250` returns `diseases`, `genes`, `assays`, `medicalActions`; `NCBIGene:6323` returns `diseases`, `phenotypes`; `OMIM:607208` and `ORPHA:33069` return `disease`, `categories`, `genes`, `medicalActions`. There are no `/hp/terms/{id}/genes` or `/hp/terms/{id}/diseases` routes.

## Example Calls
```
# Search for "seizure"
https://ontology.jax.org/api/hp/search?q=seizure&limit=5

# Term details for Seizure
https://ontology.jax.org/api/hp/terms/HP%3A0001250

# Genes and diseases annotated to Seizure
https://ontology.jax.org/api/network/annotation/HP%3A0001250

# Phenotypes for SCN1A (Entrez 6323)
https://ontology.jax.org/api/network/annotation/NCBIGene%3A6323

# Phenotypes for Dravet syndrome
https://ontology.jax.org/api/network/annotation/OMIM%3A607208
```

## Response Format
JSON. Search returns `{terms: [...], totalCount}`. A term carries `id`, `name`, `definition`, `comment`, `descendantCount`, `synonyms`, `xrefs`, `publicationReferences`, `translations`. Annotation lists carry `{id, name}` pairs — genes as `NCBIGene:####`, diseases as `OMIM:######` / `ORPHA:#####` with a `mondoId`.

## Rate Limits
No published limits. Bulk annotation files at https://hpo.jax.org/data/annotations
