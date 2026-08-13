# Observations

Append-only usage episodes, one JSON object per line, in `*.jsonl` files here.
These are the vault's learning signal: they accrue node statistics
(`uses` / `successes` / `success_rate`) and `OBSERVED` co-occurrence edges when
`build_kg.py` runs.

```json
{"ts":"2026-08-12","query":"batch correct single cell","retrieved":["scanpy","harmonypy"],"used":["scanpy","harmonypy"],"outcome":"success"}
```

- `outcome` is `success` or `failure`.
- `used` drives statistics; `retrieved` but unused is itself a retrieval signal.
- Malformed lines are skipped, never fatal — a bad episode must not break a build.
- A skill reaching >=20 uses at <15% success is auto-deprecated and drops out of
  retrieval (SkillGraph thresholds).

Nothing here is required for the graph to build; it is how the graph improves.
