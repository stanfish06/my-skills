"""
open_targets.py — Open Targets Genetics GraphQL API.

Endpoint:
  POST https://api.platform.opentargets.org/api/v4/graphql
  Query: variant(variantId: "chr_pos_ref_alt") → credible sets, V2G scores
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from .base_client import BaseClient

BASE_URL = "https://api.platform.opentargets.org/api/v4"
RATE_INTERVAL = 0.35

# Open Targets Platform schema, not the retired Genetics Portal one: the
# Variant type exposes rsIds/referenceAllele/alternateAllele, gnomAD
# frequencies as alleleFrequencies rows, mostSevereConsequence as a
# SequenceOntologyTerm object, and credibleSets as a paginated CredibleSets
# with count/rows.
VARIANT_QUERY = """
query VariantQuery($variantId: String!) {
  variant(variantId: $variantId) {
    id
    rsIds
    chromosome
    position
    referenceAllele
    alternateAllele
    mostSevereConsequence {
      id
      label
    }
    alleleFrequencies {
      populationName
      alleleFrequency
    }
    transcriptConsequences {
      distanceFromFootprint
      target {
        id
        approvedSymbol
      }
    }
  }
}
"""

CREDIBLE_SET_QUERY = """
query CredibleSetQuery($variantId: String!, $size: Int!) {
  variant(variantId: $variantId) {
    id
    credibleSets(page: { index: 0, size: $size }) {
      count
      rows {
        studyLocusId
        studyId
        studyType
        beta
        pValueMantissa
        pValueExponent
        finemappingMethod
        confidence
        study {
          id
          traitFromSource
        }
      }
    }
  }
}
"""

# gnomAD population keys the Platform returns, mapped to the labels this skill
# reports. The API suffixes them `_adj`.
_POPULATION_KEYS = {"NFE": "nfe_adj", "AFR": "afr_adj", "EAS": "eas_adj",
                    "AMR": "amr_adj", "FIN": "fin_adj"}


def _make_client(cache_dir: Optional[Path], use_cache: bool) -> BaseClient:
    return BaseClient(
        base_url=BASE_URL,
        rate_interval=RATE_INTERVAL,
        cache_dir=cache_dir,
        use_cache=use_cache,
    )


def _pvalue(mantissa, exponent):
    """Rebuild a p-value from the mantissa/exponent pair the Platform returns."""
    if mantissa is None or exponent is None:
        return None
    try:
        return float(mantissa) * (10 ** int(exponent))
    except (TypeError, ValueError, OverflowError):
        return None


def _build_variant_id(chr: str, pos: int, ref: str, alt: str) -> str:
    """Build Open Targets variant ID: chr_pos_ref_alt."""
    return f"{chr}_{pos}_{ref}_{alt}"


def get_variant(
    chr: str,
    pos: int,
    ref: str,
    alt: str,
    cache_dir: Optional[Path] = None,
    use_cache: bool = True,
) -> dict:
    """Fetch variant info from Open Targets GraphQL API."""
    client = _make_client(cache_dir, use_cache)
    variant_id = _build_variant_id(chr, pos, ref, alt)

    try:
        data = client.post("graphql", json_body={
            "query": VARIANT_QUERY,
            "variables": {"variantId": variant_id},
        })
    except Exception as e:
        return {"source": "open_targets", "status": "error", "message": str(e)}

    variant = data.get("data", {}).get("variant")
    if not variant:
        return {"source": "open_targets", "status": "empty", "message": f"No data for {variant_id}"}

    # nearest gene = the transcript consequence with the smallest footprint distance
    nearest_gene = ""
    nearest_distance = None
    for tc in variant.get("transcriptConsequences") or []:
        d = tc.get("distanceFromFootprint")
        if d is None:
            continue
        if nearest_distance is None or d < nearest_distance:
            nearest_distance = d
            nearest_gene = (tc.get("target") or {}).get("approvedSymbol", "") or ""

    freqs = {
        row.get("populationName"): row.get("alleleFrequency")
        for row in (variant.get("alleleFrequencies") or [])
    }
    rsids = variant.get("rsIds") or []
    consequence = (variant.get("mostSevereConsequence") or {}).get("label", "")

    return {
        "source": "open_targets",
        "status": "ok",
        "variant_id": variant_id,
        "rsid": rsids[0] if rsids else "",
        "nearest_gene": nearest_gene,
        "nearest_gene_distance": nearest_distance,
        "consequence": consequence,
        "population_frequencies": {
            label: freqs.get(key) for label, key in _POPULATION_KEYS.items()
        },
    }


def get_credible_sets(
    chr: str,
    pos: int,
    ref: str,
    alt: str,
    cache_dir: Optional[Path] = None,
    use_cache: bool = True,
    max_sets: int = 50,
) -> dict:
    """Fetch credible set membership from Open Targets."""
    client = _make_client(cache_dir, use_cache)
    variant_id = _build_variant_id(chr, pos, ref, alt)

    try:
        data = client.post("graphql", json_body={
            "query": CREDIBLE_SET_QUERY,
            "variables": {"variantId": variant_id, "size": max_sets},
        })
    except Exception as e:
        return {"source": "open_targets_credsets", "status": "error", "message": str(e)}

    variant = data.get("data", {}).get("variant")
    if not variant:
        return {"source": "open_targets_credsets", "status": "empty", "message": f"No data for {variant_id}"}

    container = variant.get("credibleSets") or {}
    total = container.get("count")
    credible_sets = []
    for cs in container.get("rows") or []:
        study = cs.get("study") or {}
        credible_sets.append({
            "study_locus_id": cs.get("studyLocusId", ""),
            "study_id": cs.get("studyId", "") or study.get("id", ""),
            "study_type": cs.get("studyType", ""),
            "trait": study.get("traitFromSource", ""),
            "pval": _pvalue(cs.get("pValueMantissa"), cs.get("pValueExponent")),
            "beta": cs.get("beta"),
            "finemapping_method": cs.get("finemappingMethod", ""),
            "confidence": cs.get("confidence", ""),
        })

    result = {
        "source": "open_targets_credsets",
        "status": "ok",
        "variant_id": variant_id,
        "total_credible_sets": total,
        "credible_sets": credible_sets,
    }
    if total is not None and total > len(credible_sets):
        result["message"] = (
            f"showing {len(credible_sets)} of {total} credible sets "
            f"(--max-sets {max_sets})"
        )
    return result
