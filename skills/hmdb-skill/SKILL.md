---
name: hmdb-skill
description: Submit compact HMDB search requests for metabolites, proteins, diseases, and pathways. Use when a user wants concise HMDB summaries
---

## Operating rules
- hmdb.ca publishes no JSON API and sits behind a Cloudflare interactive challenge: every path, including `/`, `/downloads`, `/metabolites/<id>` and `/unearth/q`, answers a scripted request with HTTP 403 and `cf-mitigated: challenge`. `scripts/rest_request.py` cannot retrieve HMDB content. Say so rather than reporting an empty result.
- To act on an HMDB accession, map it to a database that does serve an API: UniChem source 18 is HMDB, and `POST https://www.ebi.ac.uk/unichem/api/v1/compounds` with `{"type":"sourceID","compound":"<HMDB id>","sourceID":18}` returns the ChEBI, ChEMBL, PubChem and DrugBank identifiers for the same structure. Hand those to `chebi-skill`, `chembl-skill`, or `pubchem-pug-skill`.
- Bulk HMDB XML is distributed from https://hmdb.ca/downloads, which a person can fetch in a browser; there is no scripted route to it.
- Re-run requests in long conversations instead of relying on older tool output.
- Treat displayed `...` in tool previews as UI truncation, not literal request content.

## Execution behavior
- Return concise markdown summaries from the script JSON by default.
- If the user needs the full payload, set `save_raw=true` and report the saved file path.

## Input
- Read one JSON object from stdin.
- Required fields: `base_url`, `path`
- Optional fields: `method`, `params`, `headers`, `json_body`, `form_body`, `record_path`, `response_format`, `max_items`, `max_depth`, `timeout_sec`, `save_raw`, `raw_output_path`
- Identifier cross-reference pattern:
  - `{"base_url":"https://www.ebi.ac.uk/unichem/api/v1","path":"compounds","method":"POST","json_body":{"type":"sourceID","compound":"HMDB0000259","sourceID":18},"record_path":"compounds.0.sources","max_items":10}`

## Output
- Success returns `ok`, `source`, `path`, `method`, `status_code`, `warnings`, and either compact `records` or a compact `summary`.
- Use `raw_output_path` when `save_raw=true`.
- Failure returns `ok=false` with `error.code` and `error.message`.

## Execution
```bash
echo '{"base_url":"https://www.ebi.ac.uk/unichem/api/v1","path":"compounds","method":"POST","json_body":{"type":"sourceID","compound":"HMDB0000259","sourceID":18},"record_path":"compounds.0.sources","max_items":10}' | python scripts/rest_request.py
```

## References
- No additional runtime references are required; keep the import package limited to this file and `scripts/rest_request.py`.
