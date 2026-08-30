"""
gwas_catalog.py — NHGRI-EBI GWAS Catalog REST API.

Endpoint:
  GET /singleNucleotidePolymorphisms/{rsid}/associations?projection=associationByStudy

The unprojected association resource carries neither `efoTraits` nor `study`;
`associationByStudy` inlines both, so the trait and the study accession come
back in one request. The risk allele lives at
`loci[0].strongestRiskAlleles[0].riskAlleleName`; `riskFrequency` is top-level.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .base_client import BaseClient

BASE_URL = "https://www.ebi.ac.uk/gwas/rest/api"
RATE_INTERVAL = 0.25


def _make_client(cache_dir: Optional[Path], use_cache: bool) -> BaseClient:
    return BaseClient(
        base_url=BASE_URL,
        rate_interval=RATE_INTERVAL,
        cache_dir=cache_dir,
        use_cache=use_cache,
    )


def get_associations(rsid: str, max_hits: int = 100, cache_dir: Optional[Path] = None, use_cache: bool = True) -> dict:
    """Fetch GWAS associations for a given rsID from the GWAS Catalog."""
    client = _make_client(cache_dir, use_cache)
    try:
        data = client.get(
            f"singleNucleotidePolymorphisms/{rsid}/associations",
            params={"projection": "associationByStudy"},
        )
    except Exception as e:
        return {"source": "gwas_catalog", "status": "error", "message": str(e)}

    embedded = data.get("_embedded", {})
    raw_assocs = embedded.get("associations", [])

    associations = []
    incomplete = 0
    for a in raw_assocs[:max_hits]:
        traits = [t.get("trait", "") for t in (a.get("efoTraits") or [])]

        loci = a.get("loci") or []
        strongest = (loci[0].get("strongestRiskAlleles") or [{}])[0] if loci else {}
        risk_allele = strongest.get("riskAlleleName", "") or ""
        risk_freq = a.get("riskFrequency", "") or ""

        study = a.get("study") or {}
        study_accession = study.get("accessionId", "") or ""

        if not traits or not study_accession:
            incomplete += 1

        associations.append({
            "pvalue": a.get("pvalue"),
            "pvalue_mlog": a.get("pvalueMantissa"),
            "pvalue_exponent": a.get("pvalueExponent"),
            "risk_allele": risk_allele,
            "risk_frequency": risk_freq,
            "or_beta": a.get("orPerCopyNum"),
            "beta_num": a.get("betaNum"),
            "beta_direction": a.get("betaDirection"),
            "beta_unit": a.get("betaUnit"),
            "ci": a.get("range", ""),
            "traits": traits,
            "study_accession": study_accession,
        })

    # a row with statistics but no trait label is not a usable association;
    # say so rather than returning it under status "ok"
    status = "ok"
    warning = ""
    if associations and incomplete:
        status = "partial"
        warning = (
            f"{incomplete} of {len(associations)} associations returned without "
            "a trait label or study accession"
        )

    result = {
        "source": "gwas_catalog",
        "status": status,
        "rsid": rsid,
        "total_associations": len(raw_assocs),
        "associations": associations,
    }
    if warning:
        result["message"] = warning
    return result
