#!/usr/bin/env python3
"""Export vault/graph/graph.json to RDF (TriG + Turtle).

Optional layer. The zero-dependency JSON graph stays the runtime store that
`query.py` reads; this adds standards interop, real SHACL validation, and
SPARQL competency questions on top. Requires rdflib:

    uv pip install -r .skill-vault/kg/requirements-rdf.txt

Modelling choices worth defending:

  * Provenance uses PROV-O, and edges are partitioned into named graphs by
    provenance level. "PROPOSED must never be retrievable" then becomes a
    property of the data — you exclude a graph — rather than a filter every
    caller has to remember to apply.
  * Domains and disciplines are skos:Concept in a skos:ConceptScheme. They
    already behave like a thesaurus; SKOS says so in a way tools understand.
  * ExpertProfile instances are typed as BOTH vs:ExpertProfile and vs:Skill.
    Without this, shapes and queries targeting vs:Skill silently skip 504 of
    1818 skills — which is exactly how the first version under-counted orphans.
  * Only ASSERTED and PROPOSED edges are reified with a justification. Those
    are the ones a human reviews. Reifying 12k EXTRACTED edges would restate
    what the extraction rule already says, at four times the file size.

Usage:
  python3 .skill-vault/kg/to_rdf.py                    # -> vault/graph/graph.trig + retrievable.ttl
  python3 .skill-vault/kg/to_rdf.py --out /tmp/g.trig
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

try:
    from rdflib import Dataset, Graph, Literal, Namespace, URIRef
    from rdflib.namespace import DCTERMS, PROV, RDF, RDFS, SKOS, XSD
except ImportError:
    sys.exit(
        "rdflib is not installed — this exporter is an optional layer.\n"
        "  uv pip install -r .skill-vault/kg/requirements-rdf.txt\n"
        "The JSON graph and query.py work without it."
    )

ROOT = Path(os.environ.get("SKILL_VAULT_ROOT") or Path(__file__).resolve().parents[2])
GRAPH_JSON = ROOT / "vault" / "graph" / "graph.json"
OUT_TRIG = ROOT / "vault" / "graph" / "graph.trig"
OUT_TTL = ROOT / "vault" / "graph" / "retrievable.ttl"

VS = Namespace("https://skillquarium.dev/ontology/")
VID = Namespace("https://skillquarium.dev/id/")

PROVENANCE_LEVELS = ("ASSERTED", "OBSERVED", "EXTRACTED", "INFERRED", "PROPOSED")
NOT_RETRIEVABLE = {"PROPOSED"}

TYPE_MAP = {
    "Skill": [VS.Skill],
    "ExpertProfile": [VS.ExpertProfile, VS.Skill],   # see module docstring
    "Artifact": [VS.Artifact],
    "Domain": [SKOS.Concept, VS.Domain],
    "Discipline": [SKOS.Concept, VS.Discipline],
    "Recipe": [VS.Recipe],
    "Capability": [VS.Capability],
    "Tool": [VS.Tool],
}


def uri(node_id: str) -> URIRef:
    return VID[node_id.replace(":", "_").replace("/", "_")]


def build(data) -> tuple[Dataset, int]:
    ds = Dataset()
    core = ds.graph(URIRef("urn:vault:core"))
    graphs = {p: ds.graph(URIRef(f"urn:vault:{p}")) for p in PROVENANCE_LEVELS}

    scheme = VID["domain-scheme"]
    core.add((scheme, RDF.type, SKOS.ConceptScheme))
    core.add((scheme, RDFS.label, Literal("Vault domain scheme")))

    # TBox fragment: enough for tools to navigate without a separate ontology file
    core.add((VS.ExpertProfile, RDFS.subClassOf, VS.Skill))
    for level in PROVENANCE_LEVELS:
        activity = VID[f"provenance-{level}"]
        core.add((activity, RDF.type, PROV.Activity))
        core.add((activity, RDFS.label, Literal(level)))

    for n in data["nodes"]:
        u = uri(n["id"])
        for t in TYPE_MAP.get(n.get("type", "Skill"), [VS.Skill]):
            core.add((u, RDF.type, t))
        core.add((u, RDFS.label, Literal(n.get("label") or n["id"])))
        core.add((u, VS.identifier, Literal(n["id"])))
        if n.get("description"):
            core.add((u, DCTERMS.description, Literal(n["description"])))
        if n.get("source"):
            core.add((u, VS.source, Literal(n["source"])))
        if n.get("type") in ("Domain", "Discipline"):
            core.add((u, SKOS.inScheme, scheme))
            core.add((u, SKOS.prefLabel, Literal(n.get("label") or n["id"])))
        if n.get("uses"):
            core.add((u, VS.uses, Literal(int(n["uses"]), datatype=XSD.integer)))
        if n.get("success_rate") is not None:
            core.add((u, VS.successRate, Literal(float(n["success_rate"]), datatype=XSD.decimal)))
        if n.get("deprecated"):
            core.add((u, VS.deprecated, Literal(True)))

    reified = 0
    for e in data["edges"]:
        g = graphs.get(e["provenance"], core)
        s, p, o = uri(e["src"]), VS[e["rel"]], uri(e["dst"])
        g.add((s, p, o))
        if e["provenance"] in ("ASSERTED", "PROPOSED"):
            st = VID[f"stmt-{reified}"]
            g.add((st, RDF.type, VS.Assertion))
            g.add((st, RDF.subject, s))
            g.add((st, RDF.predicate, p))
            g.add((st, RDF.object, o))
            g.add((st, PROV.wasGeneratedBy, VID[f"provenance-{e['provenance']}"]))
            g.add((st, VS.justification, Literal(e["justification"])))
            g.add((st, VS.weight, Literal(float(e.get("weight", 1.0)), datatype=XSD.decimal)))
            reified += 1

    return ds, reified


def flatten_retrievable(ds: Dataset) -> Graph:
    """One graph containing everything an agent may act on.

    PROPOSED is excluded by construction rather than by a filter, so a caller
    that forgets the filter cannot leak an unreviewed edge into a result.
    """
    flat = Graph()
    for g in ds.graphs():
        name = str(g.identifier).rsplit(":", 1)[-1]
        if name in NOT_RETRIEVABLE:
            continue
        for triple in g:
            flat.add(triple)
    return flat


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("--graph", default=str(GRAPH_JSON))
    ap.add_argument("--out", default=str(OUT_TRIG))
    ap.add_argument("--ttl", default=str(OUT_TTL))
    args = ap.parse_args()

    src = Path(args.graph)
    if not src.is_file():
        sys.exit(f"no graph at {src} — run build_kg.py first")
    data = json.loads(src.read_text(encoding="utf-8"))

    ds, reified = build(data)
    total = sum(len(g) for g in ds.graphs())

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    ds.serialize(destination=str(out), format="trig")

    flat = flatten_retrievable(ds)
    ttl = Path(args.ttl)
    flat.serialize(destination=str(ttl), format="turtle")

    named = sorted(str(g.identifier).rsplit(":", 1)[-1] for g in ds.graphs() if len(g))
    print(f"triples          {total} ({reified} reified assertions)")
    print(f"named graphs     {', '.join(named)}")
    print(f"wrote            {out.relative_to(ROOT)} ({out.stat().st_size/1e6:.1f} MB)")
    print(f"wrote            {ttl.relative_to(ROOT)} ({len(flat)} retrievable triples)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
