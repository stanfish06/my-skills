"""
confidence.py — Extract pLDDT and PAE from Boltz-2 output files.

pLDDT is stored as B-factors in the output CIF (CA atoms only).
PAE is NOT in the confidence JSON — Boltz writes it to a separate
pae_<name>_model_<rank>.npz, and only when --write_full_pae is passed.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np


def extract_confidence(
    cif_path: Path,
    confidence_json_path: Path | None,
    pae_npz_path: Path | None = None,
) -> dict:
    """Extract pLDDT, PAE, and chain boundaries from Boltz output.

    Returns:
        {
            "plddt": np.ndarray,           # shape [n_residues], float32
            "pae": np.ndarray | None,      # shape [n_residues, n_residues], float32
                                           # None when Boltz wrote no usable PAE
            "chain_boundaries": [
                {"chain_id": str, "start": int, "end": int}
            ]
        }
    """
    plddt, chain_boundaries = _parse_cif_atoms(cif_path)
    pae = _load_pae(pae_npz_path, confidence_json_path, len(plddt))
    return {
        "plddt": plddt,
        "pae": pae,
        "chain_boundaries": chain_boundaries,
    }


def _read_atom_site_columns(cif_path: Path) -> dict[str, list[str]]:
    """Minimal mmCIF loop reader — extracts _atom_site columns without biopython.

    Finds the loop_ block that declares _atom_site fields, records column
    indices, then collects the data rows that follow.  Only the four columns
    needed for pLDDT/chain extraction are returned; other columns are ignored.
    """
    # Use lowercase keys throughout to avoid case-sensitivity bugs
    WANTED = {
        "_atom_site.label_atom_id",
        "_atom_site.label_seq_id",
        "_atom_site.label_asym_id",
        "_atom_site.b_iso_or_equiv",
    }
    # Map lowercase key → original key for the returned dict
    WANTED_ORIG = {
        "_atom_site.label_atom_id": "_atom_site.label_atom_id",
        "_atom_site.label_seq_id": "_atom_site.label_seq_id",
        "_atom_site.label_asym_id": "_atom_site.label_asym_id",
        "_atom_site.b_iso_or_equiv": "_atom_site.B_iso_or_equiv",
    }

    lines = Path(cif_path).read_text(errors="replace").splitlines()

    # --- locate the _atom_site loop ---
    # Only peek at consecutive field-declaration lines (starting with "_"),
    # so we don't accidentally see fields from a later loop block.
    header_start = None
    for i, line in enumerate(lines):
        if line.strip() != "loop_":
            continue
        for j in range(i + 1, len(lines)):
            s = lines[j].strip()
            if not s or s.startswith("#"):
                continue  # skip blank/comment lines between loop_ and fields
            if s.startswith("_"):
                if s.lower().startswith("_atom_site."):
                    header_start = i
                break  # first non-blank non-comment non-field line → wrong loop
        if header_start is not None:
            break

    if header_start is None:
        return {v: [] for v in WANTED_ORIG.values()}

    # --- collect column names (lowercased) ---
    col_names: list[str] = []
    data_start = header_start + 1
    for i in range(header_start + 1, len(lines)):
        s = lines[i].strip()
        if s.startswith("_"):
            col_names.append(s.split()[0].lower())
            data_start = i + 1
        else:
            data_start = i
            break

    wanted_idx = {name: idx for idx, name in enumerate(col_names) if name in WANTED}

    # Build result with original-case keys
    result: dict[str, list[str]] = {WANTED_ORIG[k]: [] for k in WANTED}

    # --- collect data rows until next loop_ or data_ block ---
    for line in lines[data_start:]:
        s = line.strip()
        if not s or s.startswith("#") or s.startswith("loop_") or s.startswith("data_"):
            if s.startswith("loop_") or s.startswith("data_"):
                break
            continue
        tokens = s.split()
        for lc_name, idx in wanted_idx.items():
            if idx < len(tokens):
                result[WANTED_ORIG[lc_name]].append(tokens[idx])

    return result


def _parse_cif_atoms(cif_path: Path) -> tuple[np.ndarray, list[dict]]:
    """Single-pass CIF parse returning (plddt, chain_boundaries).

    Reads _atom_site records once, extracting CA B-factors (pLDDT) and
    chain boundary information in the same iteration.
    """
    mmcif = _read_atom_site_columns(cif_path)

    atom_ids  = mmcif.get("_atom_site.label_atom_id", [])
    seq_ids   = mmcif.get("_atom_site.label_seq_id", [])
    chain_ids = mmcif.get("_atom_site.label_asym_id", [])
    bfacs     = mmcif.get("_atom_site.B_iso_or_equiv", [])

    if not atom_ids:
        raise ValueError(f"No _atom_site records found in {cif_path}")

    seen: dict[tuple[str, str], float] = {}
    order: list[tuple[str, str]] = []

    for atom, seq, chain, bfac in zip(atom_ids, seq_ids, chain_ids, bfacs):
        if atom.strip() != "CA":
            continue
        key = (chain.strip(), seq.strip())
        if key not in seen:
            seen[key] = float(bfac)
            order.append(key)

    if not seen:
        raise ValueError(
            f"No CA atoms found in {cif_path}. "
            "Check that the CIF file is a valid Boltz output."
        )

    plddt = np.array([seen[k] for k in order], dtype=np.float32)

    boundaries: list[dict] = []
    current_chain = order[0][0]
    start_idx = 0
    for i, (chain, _) in enumerate(order):
        if chain != current_chain:
            boundaries.append({"chain_id": current_chain, "start": start_idx, "end": i - 1})
            current_chain = chain
            start_idx = i
    boundaries.append({"chain_id": current_chain, "start": start_idx, "end": len(order) - 1})

    return plddt, boundaries


def _parse_plddt_from_cif(cif_path: Path) -> np.ndarray:
    """Extract per-residue pLDDT from CIF B-factors (CA atoms only)."""
    plddt, _ = _parse_cif_atoms(cif_path)
    return plddt


def _load_pae(
    pae_npz_path: Path | None,
    confidence_json_path: Path | None,
    n_residues: int,
) -> np.ndarray | None:
    """Load the PAE matrix, or return None when Boltz produced none.

    Boltz writes PAE to pae_<name>_model_<rank>.npz under the "pae" key. The
    confidence JSON carries only scalar scores (confidence_score, ptm, iptm,
    complex_plddt, ...) and never a "pae" key; the JSON is still checked as a
    fallback for AlphaFold-style inputs.

    Returns None rather than a zero matrix — an all-zero PAE renders as
    uniformly confident and would misreport a missing metric as a perfect one.
    """
    pae = None

    if pae_npz_path is not None and Path(pae_npz_path).exists():
        with np.load(pae_npz_path) as npz:
            if "pae" in npz:
                pae = np.array(npz["pae"], dtype=np.float32)

    if pae is None and confidence_json_path is not None and Path(confidence_json_path).exists():
        data = json.loads(Path(confidence_json_path).read_text())
        if "pae" in data:
            pae = np.array(data["pae"], dtype=np.float32)

    if pae is None:
        return None

    # Boltz indexes PAE by token, which need not match the CA-derived residue
    # count once ligands or modified residues are present.
    if pae.ndim != 2 or pae.shape != (n_residues, n_residues):
        return None

    return pae
