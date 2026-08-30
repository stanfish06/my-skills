# Expected output: r² between SORT1 lead and three nearby variants

Input: `examples/input.json` (computes pairwise r² between `1_109274968_G_T`
(rs646776) and three nearby variants on the 1000G EUR Phase 3 reference).

## What you get

`OnDemandLDResult` dataclass with:

- `panel_id`: `1000g_phase3_v5b_grch38_basic`
- `panel_version`: `5b_remote_2019_03_12`
- `super_pop`: `EUR`
- `plink_version`: `PLINK v1.90b6.27 ...`
- `n_partners_returned`: 3 (the lead self-match is excluded; a partner absent
  from the panel is named in `notes`, so a shortfall is never unexplained)
- `pairs`: list of `OnDemandLDPair` (partner_variant_id, r2)

Sample expected output (real values vary):

```
panel: 1000g_phase3_v5b_grch38_basic (EUR)
plink: PLINK v1.90b6.27 64-bit (2023-05-09)
pairs:
  1_109274500_C_T    r² = 0.892
  1_109275500_A_G    r² = 0.765
  1_109280000_C_T    r² = 0.412
```

## Reproducing

```bash
bash run_example.sh
```

Network required on first call (~5-50 MB region VCF fetch from EBI 1000G FTP).
Subsequent calls hit the local cache at `~/.clawbio/locuscompare_cache/1000g/`.

Requires `plink` (1.9) on PATH (or `PLINK_BIN` env var pointing to it).
