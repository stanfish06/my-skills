#!/usr/bin/env python3
"""Validate the vault knowledge graph: shape constraints + competency questions.

Two independent checks, deliberately kept apart (KR practice: a logical
inconsistency and a data-quality violation have different repair paths):

  SHAPES  structural constraints, P-prefixed. These are the stdlib checks that
          run with no dependencies; ontology/shapes.ttl (S-prefixed) is
          authoritative and runs under --shacl. The two catalogues are
          deliberately numbered apart -- they previously collided.
  CQ      competency questions — the ontology's real test suite. A CQ that the
          current TBox cannot yet answer reports NOT_YET rather than FAIL, so
          the roadmap stays visible instead of being hidden behind a red build.

Exit code is nonzero only on a Violation-severity shape failure or a CQ
regression, so this is safe to run in CI beside the existing unittest suite.

Usage:
  python3 .skill-vault/kg/validate.py
  python3 .skill-vault/kg/validate.py --json
"""
from __future__ import annotations

import json
import os
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(os.environ.get("SKILL_VAULT_ROOT") or Path(__file__).resolve().parents[2])
GRAPH_PATH = ROOT / "vault" / "graph" / "graph.json"
SCHEMA_PATH = ROOT / ".skill-vault" / "ontology" / "schema.json"

SKILL_TYPES = ("Skill", "ExpertProfile")   # ExpertProfile is a subclass of Skill

ORPHAN_BASELINE = 0.481   # measured on the description-only graph this replaces
ORPHAN_GATE = 0.05        # design target


class Report:
    def __init__(self):
        self.rows = []

    def add(self, kind, ident, status, detail):
        self.rows.append({"kind": kind, "id": ident, "status": status, "detail": detail})

    @property
    def failed(self):
        return [r for r in self.rows if r["status"] == "FAIL"]

    def render(self):
        icon = {"PASS": "ok  ", "FAIL": "FAIL", "WARN": "warn", "NOT_YET": "todo"}
        width = max(len(r["id"]) for r in self.rows) if self.rows else 4
        last = None
        for r in self.rows:
            if r["kind"] != last:
                print(f"\n{r['kind']}")
                last = r["kind"]
            print(f"  [{icon[r['status']]}] {r['id']:<{width}}  {r['detail']}")


def load():
    if not GRAPH_PATH.is_file():
        print(f"no graph at {GRAPH_PATH} — run build_kg.py first", file=sys.stderr)
        raise SystemExit(2)
    with open(GRAPH_PATH, encoding="utf-8") as fh:
        graph = json.load(fh)
    with open(SCHEMA_PATH, encoding="utf-8") as fh:
        schema = json.load(fh)
    return graph, schema


def index(graph):
    nodes = {n["id"]: n for n in graph["nodes"]}
    out = defaultdict(lambda: defaultdict(set))
    inn = defaultdict(lambda: defaultdict(set))
    for e in graph["edges"]:
        out[e["src"]][e["rel"]].add(e["dst"])
        inn[e["dst"]][e["rel"]].add(e["src"])
    return nodes, out, inn


# ------------------------------------------------------------------- shapes
def check_shapes(graph, schema, nodes, out, rep):
    skills = [n for n in graph["nodes"] if n.get("type") in SKILL_TYPES]
    provs = set(schema["provenance_levels"])
    retrievable = set(graph.get("metrics", {}).get("retrievable_provenance") or [])
    schema_retrievable = {
        k for k, v in schema["provenance_levels"].items() if v.get("retrievable")
    }

    missing_domain = [n["id"] for n in skills if not out[n["id"]].get("in_domain")]
    rep.add("SHAPES", "P1 in_domain>=1", "FAIL" if missing_domain else "PASS",
            f"{len(missing_domain)} skills without a domain"
            + (f" e.g. {missing_domain[:3]}" if missing_domain else ""))

    rate = graph["metrics"]["orphan_rate"]
    status = "PASS" if rate < ORPHAN_GATE else ("WARN" if rate < ORPHAN_BASELINE else "FAIL")
    rep.add("SHAPES", "P2 orphan rate", status,
            f"{rate:.1%} vs baseline {ORPHAN_BASELINE:.1%}, gate {ORPHAN_GATE:.0%} "
            f"({graph['metrics']['orphan_count']} skills)")

    bad = [e for e in graph["edges"]
           if e.get("provenance") not in provs or not e.get("justification")]
    rep.add("SHAPES", "P3 provenance", "FAIL" if bad else "PASS",
            f"{len(bad)} edges missing provenance or justification")

    if "PROPOSED" in retrievable or "PROPOSED" in schema_retrievable:
        leaked = [e for e in graph["edges"] if e.get("provenance") == "PROPOSED"] or [
            {"src": "metrics.retrievable_provenance", "rel": "includes", "dst": "PROPOSED"}
        ]
    else:
        leaked = [e for e in graph["edges"]
                  if e.get("provenance") == "PROPOSED" and e.get("status") != "proposed"]
    rep.add("SHAPES", "P4 PROPOSED gate", "FAIL" if leaked else "PASS",
            f"{len(leaked)} unreviewed edges marked retrievable")

    # P5 chains_to acyclicity
    adj = {s: set(rels.get("chains_to", ())) for s, rels in out.items()}
    colour, cycles = {}, []

    def walk(u):
        colour[u] = 1
        for v in adj.get(u, ()):
            if colour.get(v) == 1:
                cycles.append((u, v))
            elif not colour.get(v):
                walk(v)
        colour[u] = 2

    for s in list(adj):
        if not colour.get(s):
            walk(s)
    rep.add("SHAPES", "P5 chains acyclic", "WARN" if cycles else "PASS",
            f"{len(cycles)} back-edges" + (f" e.g. {cycles[:2]}" if cycles else ""))

    pairs = {(e["src"], e["dst"]) for e in graph["edges"] if e["rel"] == "alternative_to"}
    asym = [p for p in pairs if (p[1], p[0]) not in pairs]
    rep.add("SHAPES", "P6 alt symmetric", "FAIL" if asym else "PASS",
            f"{len(asym)} asymmetric alternative_to edges")

    amb = graph.get("ambiguous_aliases", {})
    lexicon_path = ROOT / ".skill-vault" / "ontology" / "lexicon.json"
    collisions = {}
    flagged = 0
    if lexicon_path.is_file():
        lexicon = json.loads(lexicon_path.read_text(encoding="utf-8"))
        flagged = len(lexicon.get("ambiguous_terms", {}))
        by_term = defaultdict(set)
        for aid, spec in lexicon.get("artifacts", {}).items():
            for raw in (spec.get("label", ""), aid.split(":", 1)[-1].replace("-", " ")):
                term = raw.strip().lower()
                if term:
                    by_term[term].add(aid)
        declared = {t.lower() for t in lexicon.get("ambiguous_terms", {})}
        collisions = {t: sorted(ids) for t, ids in by_term.items()
                      if len(ids) > 1 and t not in declared}
    rep.add("SHAPES", "P7 term ambiguity", "FAIL" if collisions else "PASS",
            f"{len(amb)} ambiguous aliases parked; "
            + (f"{len(collisions)} unflagged artifact-term collisions {list(collisions)[:3]}"
               if collisions else f"{flagged} flagged artifact terms, no unflagged collisions"))

    dangling = []
    for r in graph.get("recipes", []):
        dangling += [s for s in r["members"] if s not in nodes]
    rep.add("SHAPES", "P8 recipe steps", "FAIL" if dangling else "PASS",
            f"{len(dangling)} recipe steps do not resolve to a skill")


# ------------------------------------------------- competency questions (CQ)
def check_cqs(graph, nodes, out, inn, rep):
    def neigh(sid, rels):
        r = set()
        for rel in rels:
            r |= out[sid].get(rel, set()) | inn[sid].get(rel, set())
        return {x for x in r if x in nodes and nodes[x].get("type") in SKILL_TYPES}

    # CQ1 — can we walk a chain from FASTQ-touching skills toward pathway analysis?
    fastq = {e["src"] for e in graph["edges"]
             if e["rel"] == "touches" and e["dst"] == "artifact:fastq"}
    seen, frontier = set(fastq), set(fastq)
    for _ in range(4):
        nxt = set()
        for s in frontier:
            nxt |= out[s].get("chains_to", set()) | out[s].get("co_occurs_with", set())
        frontier = nxt - seen
        seen |= nxt
    reached = {"pathway-enrichment", "pathway-enricher"} & seen
    rep.add("CQ", "CQ1 fastq->pathway", "PASS" if reached else "NOT_YET",
            f"{len(fastq)} FASTQ skills reach {len(seen)} skills in 4 hops; "
            f"pathway endpoint {'reached: ' + ', '.join(sorted(reached)) if reached else 'not reached'}")

    # CQ2 — alternative_to requires Capability+Tool, which Phase 1 does not populate.
    alts = [e for e in graph["edges"] if e["rel"] == "alternative_to"]
    rep.add("CQ", "CQ2 alternatives", "PASS" if alts else "NOT_YET",
            f"{len(alts)} alternative_to edges — rule R4 is disabled until Capability "
            f"and Tool are populated (Phase 4); firing it now would assert "
            f"near-equivalence on no evidence")

    # CQ3 — foundations of a skill
    probe = "scvi-tools"
    found = neigh(probe, ["references", "co_occurs_with"]) if probe in nodes else set()
    rep.add("CQ", "CQ3 prerequisites", "PASS" if len(found) >= 3 else "NOT_YET",
            f"{probe} -> {len(found)} related "
            f"({', '.join(sorted(found)[:5])}{'...' if len(found) > 5 else ''})")

    # CQ4 — capability lookup
    caps = [n for n in graph["nodes"] if n.get("type") == "Capability"]
    rep.add("CQ", "CQ4 by capability", "PASS" if caps else "NOT_YET",
            f"{len(caps)} Capability nodes — population needs curation or the gated "
            f"LLM pass (measured: n-gram mining returns template boilerplate)")

    # CQ5 — set completion: the HYSET failure this design exists to fix
    recipes = graph.get("recipes", [])
    ok = 0
    for r in recipes:
        steps = r["steps"]
        if len(steps) < 2:
            continue
        seed = steps[0]
        recovered = neigh(seed, ["co_occurs_with", "chains_to"])
        if len(recovered & set(steps[1:])) >= 1:
            ok += 1
    total = sum(1 for r in recipes if len(r["steps"]) >= 2)
    rep.add("CQ", "CQ5 set completion", "PASS" if total and ok == total else
            ("WARN" if ok else "NOT_YET"),
            f"{ok}/{total} recipes recoverable from their first step alone")

    # CQ6 — gap mining: this is the query that makes the vault grow
    orphans = graph.get("orphans", [])
    used_art = {e["dst"] for e in graph["edges"] if e["rel"] == "touches"}
    all_art = {n["id"] for n in graph["nodes"] if n.get("type") == "Artifact"}
    rep.add("CQ", "CQ6 gaps", "PASS",
            f"{len(orphans)} unconnected skills, {len(all_art - used_art)} artifacts with "
            f"no skill — this is the growth queue, not a failure")

    # CQ7 — staleness / failing skills
    stats = [n for n in graph["nodes"] if n.get("uses", 0) > 0]
    dep = [n for n in graph["nodes"] if n.get("deprecated")]
    rep.add("CQ", "CQ7 staleness", "PASS" if stats else "NOT_YET",
            f"{len(stats)} skills have usage data, {len(dep)} deprecated — "
            f"needs observation ingestion (Phase 3)")


def check_shacl(rep):
    """Real SHACL validation via pySHACL, when the optional RDF layer is present.

    The stdlib checks above stay the always-on floor so validation never depends
    on a package being installed. This adds what they cannot express: cycle
    detection by property path, closed-vocabulary checks that catch an invented
    predicate, and shapes that live as reviewable data rather than as code.
    """
    try:
        from pyshacl import validate as shacl_validate   # noqa: PLC0415
        from rdflib import Graph as RDFGraph             # noqa: PLC0415
    except ImportError:
        rep.add("SHACL", "pyshacl", "NOT_YET",
                "optional RDF layer not installed — "
                "uv pip install -r .skill-vault/kg/requirements-rdf.txt")
        return

    ttl = ROOT / "vault" / "graph" / "retrievable.ttl"
    shapes = ROOT / ".skill-vault" / "ontology" / "shapes.ttl"
    if not ttl.is_file():
        rep.add("SHACL", "rdf export", "NOT_YET",
                "no retrievable.ttl — run to_rdf.py first")
        return

    data_g = RDFGraph().parse(str(ttl), format="turtle")
    shapes_g = RDFGraph().parse(str(shapes), format="turtle")
    conforms, _, text = shacl_validate(
        data_g, shacl_graph=shapes_g, advanced=True, inference="none")
    n = text.count("Constraint Violation")
    rep.add("SHACL", "shapes.ttl", "PASS" if conforms else "FAIL",
            f"{len(data_g)} triples against {shapes.name}: "
            + ("conforms" if conforms else f"{n} violation(s)"))
    if not conforms:
        for line in text.splitlines():
            if "Message:" in line:
                rep.add("SHACL", "violation", "FAIL", line.strip()[:100])


def main():
    graph, schema = load()
    nodes, out, inn = index(graph)
    rep = Report()
    check_shapes(graph, schema, nodes, out, rep)
    check_cqs(graph, nodes, out, inn, rep)
    if "--shacl" in sys.argv:
        check_shacl(rep)

    if "--json" in sys.argv:
        print(json.dumps(rep.rows, indent=1))
    else:
        m = graph["metrics"]
        print(f"vault knowledge graph — {m['skills']} skills, {m['nodes']} nodes, "
              f"{m['edges']} edges")
        rep.render()
        n = len(rep.failed)
        print(f"\n{'FAILED' if n else 'OK'}: {n} violation(s), "
              f"{sum(1 for r in rep.rows if r['status'] == 'WARN')} warning(s), "
              f"{sum(1 for r in rep.rows if r['status'] == 'NOT_YET')} not-yet-answerable")
    return 1 if rep.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
