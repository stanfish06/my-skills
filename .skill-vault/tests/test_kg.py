#!/usr/bin/env python3
"""Regression tests for the vault knowledge graph.

Two kinds, kept apart on purpose:

  * unit tests on extraction behaviour, run against a synthetic fixture vault so
    they are fast and independent of what upstream ships today;
  * competency-question regressions on the real committed graph, which are the
    ontology's actual acceptance criteria (Manchester methodology: an ontology
    is tested by the questions it must answer, not by its size).

Run:  python3 -m unittest discover -s .skill-vault/tests -p 'test_*.py'
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
KG = REPO / ".skill-vault" / "kg"
sys.path.insert(0, str(KG))


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class FixtureVault:
    """A miniature vault with a known-correct answer for every assertion."""

    def __init__(self, root: Path):
        self.root = root
        write(root / "skills/alpha/SKILL.md",
              "---\nname: alpha\ndescription: Produces FASTQ reads for downstream work.\n---\n"
              "# alpha\nEmits fastq files. Pairs with `beta` for the next step.\n")
        write(root / "skills/beta/SKILL.md",
              "---\nname: beta\ndescription: Aligns FASTQ to BAM using alpha output.\n---\n"
              "# beta\nTakes fastq and writes bam. See alpha.\n")
        write(root / "skills/gamma/SKILL.md",
              "---\nname: gamma\ndescription: Unrelated document formatting helper.\n---\n"
              "# gamma\nNothing to do with sequencing.\n")
        # `workflow` is a common English word: it must not link everything.
        write(root / "skills/workflow/SKILL.md",
              "---\nname: workflow\ndescription: Generic workflow helper.\n---\n# workflow\n")
        for name in ("alpha", "beta", "gamma", "workflow"):
            # every skill mentions "workflow" in prose — the generic-name trap
            p = root / f"skills/{name}/SKILL.md"
            p.write_text(p.read_text() + "\nThis workflow is standard.\n", encoding="utf-8")
            aliases = "aliases:\n  - calorie counter\n" if name == "alpha" else ""
            write(root / f"vault/notes/testing/{name}.md",
                  f"---\ntitle: {name}\ndomain: testing\nsource: skills/{name}/SKILL.md\n"
                  f"{aliases}---\n")
        write(root / "vault/recipes/demo.md",
              "---\ntitle: Demo pipeline\n---\n# Demo\n\n"
              "1. **[alpha](../notes/testing/alpha.md)** — start here. "
              "Alternative: **[gamma](../notes/testing/gamma.md)**.\n"
              "2. **[beta](../notes/testing/beta.md)** — then this.\n")
        write(root / "vault/notes/testing/alpha.md",
              "---\ntitle: alpha\ndomain: testing\nsource: skills/alpha/SKILL.md\n"
              "aliases:\n  - calorie counter\n---\n")
        # minimal ontology copied from the real one
        for f in ("schema.json", "lexicon.json"):
            src = REPO / ".skill-vault/ontology" / f
            write(root / ".skill-vault/ontology" / f, src.read_text(encoding="utf-8"))

    def build(self):
        env = dict(os.environ, SKILL_VAULT_ROOT=str(self.root))
        subprocess.run([sys.executable, str(KG / "build_kg.py")],
                       env=env, capture_output=True, check=True)
        return json.loads((self.root / "vault/graph/graph.json").read_text(encoding="utf-8"))


class TestExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.graph = FixtureVault(Path(cls.tmp.name)).build()
        cls.edges = cls.graph["edges"]
        cls.rels = {(e["src"], e["rel"], e["dst"]) for e in cls.edges}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_skill_nodes_discovered(self):
        ids = {n["id"] for n in self.graph["nodes"] if n.get("type") == "Skill"}
        self.assertEqual(ids, {"alpha", "beta", "gamma", "workflow"})

    def test_name_mention_creates_symmetric_reference(self):
        self.assertIn(("beta", "references", "alpha"), self.rels)
        self.assertIn(("alpha", "references", "beta"), self.rels)

    def test_generic_name_does_not_link_everything(self):
        """`workflow` appears in every body as prose. It must not become a hub —
        this is the contamination that gave the real vault a 745-edge `workflow`."""
        hub = [e for e in self.edges
               if e["rel"] == "references" and "workflow" in (e["src"], e["dst"])]
        self.assertLessEqual(len(hub), 2, f"generic name leaked into prose: {hub}")

    def test_unrelated_skill_is_not_linked(self):
        self.assertNotIn(("alpha", "references", "gamma"), self.rels)

    def test_artifact_touches_extracted(self):
        self.assertIn(("alpha", "touches", "artifact:fastq"), self.rels)
        self.assertIn(("beta", "touches", "artifact:bam"), self.rels)

    def test_recipe_order_yields_direction(self):
        """Recipe step order is the only cheap, trustworthy direction source."""
        self.assertIn(("alpha", "chains_to", "beta"), self.rels)
        self.assertNotIn(("beta", "chains_to", "alpha"), self.rels)

    def test_every_edge_carries_provenance_and_justification(self):
        for e in self.edges:
            self.assertIn(e["provenance"],
                          {"ASSERTED", "OBSERVED", "EXTRACTED", "INFERRED", "PROPOSED"})
            self.assertTrue(e["justification"], f"edge without justification: {e}")

    def test_proposed_edges_are_never_retrievable(self):
        for e in self.edges:
            if e["provenance"] == "PROPOSED":
                self.assertEqual(e["status"], "proposed")

    def test_recipe_auxiliary_links_are_members_not_steps(self):
        """A numbered item's later links are alternatives, not consecutive stages."""
        recipe = next(r for r in self.graph["recipes"] if r["id"] == "recipe:demo")
        self.assertEqual(recipe["steps"], ["alpha", "beta"])
        self.assertIn("gamma", recipe["members"])
        self.assertNotIn(("alpha", "chains_to", "gamma"), self.rels)

    def test_aliases_are_stored_on_nodes(self):
        node = next(n for n in self.graph["nodes"] if n["id"] == "alpha")
        self.assertIn("calorie counter", node.get("aliases", []))


class TestCommittedGraph(unittest.TestCase):
    """Competency questions against the real graph. Skipped if not yet built."""

    @classmethod
    def setUpClass(cls):
        path = REPO / "vault/graph/graph.json"
        if not path.is_file():
            raise unittest.SkipTest("graph.json not built")
        cls.graph = json.loads(path.read_text(encoding="utf-8"))
        cls.metrics = cls.graph["metrics"]

    def test_orphan_rate_beats_the_description_only_baseline(self):
        """The gate that decides whether this design was worth building at all."""
        self.assertLess(self.metrics["orphan_rate"], 0.15,
                        "orphan rate regressed toward the 48.1% baseline")

    def test_graph_is_substantially_denser_than_build_related(self):
        self.assertGreater(self.metrics["edges"], 5000,
                           "edge count fell back toward the 1277-edge string-match graph")

    def test_cq5_set_completion(self):
        """Every recipe must be recoverable from its first step alone.

        The previous version of this test only asserted that co_occurs_with
        edges existed at all, so it would have passed on a graph where no
        recipe was actually recoverable — it did not test the thing it is
        named for. This walks each recipe the way retrieval does.
        """
        adj = defaultdict(set)
        for e in self.graph["edges"]:
            if e["rel"] in ("co_occurs_with", "chains_to"):
                adj[e["src"]].add(e["dst"])
                adj[e["dst"]].add(e["src"])
        checked = 0
        for r in self.graph.get("recipes", []):
            steps = r["steps"]
            if len(steps) < 2:
                continue
            checked += 1
            recovered = adj[steps[0]] & set(steps[1:])
            self.assertTrue(recovered,
                            f"{r['id']}: nothing of {steps[1:]} reachable from {steps[0]} — "
                            f"set-completion cannot rebuild this workflow")
        self.assertGreater(checked, 0, "no multi-step recipes to check")

    def test_retrieval_is_deterministic_across_hash_seeds(self):
        """Adjacency is stored in sets and graph-derived picks share a handful of
        constant scores, so any unsorted traversal leaks PYTHONHASHSEED into the
        result order. That shipped once: `raw fastq to enriched pathways` returned
        two different result sets across seeds 0-5."""
        outs = set()
        for seed in ("0", "1", "7"):
            env = dict(os.environ, PYTHONHASHSEED=seed)
            proc = subprocess.run(
                [sys.executable, str(KG / "query.py"),
                 "raw fastq to enriched pathways", "--k", "8", "--json"],
                env=env, capture_output=True, text=True, check=True)
            outs.add(tuple(r["skill"] for r in json.loads(proc.stdout)["results"]))
        self.assertEqual(len(outs), 1,
                         f"retrieval varies with PYTHONHASHSEED: {outs}")

    def test_retrieval_knobs_are_pinned(self):
        """The scores, quota, nudge passes and neighbour cap in query.py are
        unmeasured magic numbers. Nothing else would notice if they got worse,
        so pin the observable contract they produce: a stable, mixed result set
        that is not pure lexical ranking."""
        from query import VaultGraph, retrieve  # noqa: PLC0415
        g = VaultGraph(REPO / "vault/graph/graph.json")
        results, _ = retrieve(g, "batch correct single cell data and find marker genes", k=8)
        self.assertEqual(len(results), 8, "result set is not filled to k")
        derived = [r for r in results if r["why"] != "matched the query directly"]
        self.assertGreaterEqual(len(derived), 1, "graph expansion contributed nothing")
        self.assertLessEqual(len(derived), 4, "graph expansion crowded out lexical matches")
        self.assertTrue(all(r["why"] for r in results),
                        "every result must explain why it was included")
        names = {r["skill"] for r in results}
        self.assertTrue(
            names & {"scrna-orchestrator", "scvi-tools", "harmonypy", "scanpy"},
            f"no core single-cell skill retrieved: {sorted(names)}",
        )

    def test_cq1_fastq_reaches_pathway_analysis(self):
        from query import VaultGraph, retrieve  # noqa: E402
        g = VaultGraph(REPO / "vault/graph/graph.json")
        results, _ = retrieve(g, "raw fastq reads to enriched pathways", k=8)
        names = {r["skill"] for r in results}
        self.assertTrue(names, "retrieval returned nothing")
        self.assertTrue(any("rnaseq" in n or "fastq" in n or "pathway" in n for n in names),
                        f"no sequencing skill retrieved: {sorted(names)}")

    def test_retrieval_reserves_slots_for_graph_derived_skills(self):
        """Without reserved slots, BM25 fills every slot and the graph adds nothing."""
        from query import VaultGraph, retrieve  # noqa: E402
        g = VaultGraph(REPO / "vault/graph/graph.json")
        results, _ = retrieve(g, "batch correct single cell data and find marker genes", k=8)
        derived = [r for r in results if r["why"] != "matched the query directly"]
        self.assertTrue(derived, "graph expansion contributed nothing to the result set")

    def test_every_recipe_step_resolves(self):
        ids = {n["id"] for n in self.graph["nodes"]}
        for r in self.graph.get("recipes", []):
            for step in r["steps"]:
                self.assertIn(step, ids, f"{r['id']} references missing skill {step}")

    def test_recipe_steps_use_only_the_primary_link(self):
        bulk = next(
            (r for r in self.graph.get("recipes", []) if r["id"] == "recipe:bulk-rnaseq-to-pathways"),
            None,
        )
        if bulk is None:
            self.skipTest("bulk-rnaseq-to-pathways recipe missing")
        self.assertNotIn(("pydeseq2", "chains_to", "rnaseq-de"),
                         {(e["src"], e["rel"], e["dst"]) for e in self.graph["edges"]})
        self.assertIn("rnaseq-de", bulk["members"])
        self.assertNotIn("rnaseq-de", bulk["steps"])

    def test_alias_query_finds_the_skill(self):
        from query import VaultGraph, retrieve  # noqa: E402
        g = VaultGraph(REPO / "vault/graph/graph.json")
        results, _ = retrieve(g, "calorie counter", k=8)
        self.assertIn("fitness-nutrition", {r["skill"] for r in results},
                      "curated alias was not indexed for seed retrieval")

    def test_dispatcher_is_not_an_expert_profile(self):
        node = next((n for n in self.graph["nodes"] if n["id"] == "scientific-agents"), None)
        if node is None:
            self.skipTest("scientific-agents node missing")
        self.assertNotEqual(node.get("type"), "ExpertProfile")

    def test_metrics_omit_wall_clock_date(self):
        self.assertNotIn("built", self.metrics)


class TestRDFLayer(unittest.TestCase):
    """The optional RDF/SHACL layer. Skipped entirely when rdflib is absent, so
    the zero-dependency path stays the one that must always work."""

    @classmethod
    def setUpClass(cls):
        try:
            import rdflib  # noqa: F401
            import pyshacl  # noqa: F401
        except ImportError:
            raise unittest.SkipTest("optional RDF layer not installed")
        cls.ttl = REPO / "vault/graph/retrievable.ttl"
        if not cls.ttl.is_file():
            raise unittest.SkipTest("retrievable.ttl not exported")
        from rdflib import Graph
        cls.g = Graph().parse(str(cls.ttl), format="turtle")

    def test_expert_profiles_are_also_skills(self):
        """Expert profiles must also be typed as vs:Skill, or every shape and
        query targeting Skill silently skips them."""
        rows = list(self.g.query(
            "PREFIX vs: <https://skillquarium.dev/ontology/> "
            "SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE { ?s a vs:ExpertProfile . ?s a vs:Skill }"))
        self.assertGreater(int(rows[0][0]), 400, "expert profiles are not typed as Skill")

    def test_no_proposed_edges_in_retrievable_graph(self):
        """PROPOSED is excluded by construction, not by a filter callers must remember."""
        rows = list(self.g.query(
            'PREFIX prov: <http://www.w3.org/ns/prov#> '
            'PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> '
            'SELECT ?s WHERE { ?s prov:wasGeneratedBy ?a . ?a rdfs:label "PROPOSED" }'))
        self.assertEqual(len(rows), 0, "unreviewed edge reachable in the retrievable graph")

    def test_sparql_orphan_count_matches_json_metrics(self):
        """Cross-validation: two independent implementations of the same metric."""
        cq = (REPO / ".skill-vault/ontology/cq/cq6-gaps.rq").read_text(encoding="utf-8")
        rows = [r for r in self.g.query(cq) if str(r[0]) == "orphan-skill"]
        metrics = json.loads((REPO / "vault/graph/graph.json").read_text(encoding="utf-8"))["metrics"]
        self.assertEqual(len(rows), metrics["orphan_count"],
                         "SPARQL and Python disagree on the orphan definition")

    def test_every_committed_sparql_query_parses_and_runs(self):
        """Only cq6 had a caller, so a typo in cq1/cq3/cq8 was invisible.
        Executing each file is what makes a committed query a live artifact."""
        cq_dir = REPO / ".skill-vault/ontology/cq"
        files = sorted(cq_dir.glob("*.rq"))
        self.assertTrue(files, "no committed competency questions")
        for path in files:
            with self.subTest(cq=path.name):
                rows = list(self.g.query(path.read_text(encoding="utf-8")))
                self.assertTrue(rows, f"{path.name} returned no rows — "
                                      f"the graph or the query has drifted")

    def test_shacl_shapes_conform(self):
        from pyshacl import validate
        from rdflib import Graph
        shapes = Graph().parse(str(REPO / ".skill-vault/ontology/shapes.ttl"), format="turtle")
        conforms, _, text = validate(self.g, shacl_graph=shapes, advanced=True, inference="none")
        self.assertTrue(conforms, f"SHACL violations:\n{text[:2000]}")

    def test_rdf_export_is_byte_deterministic(self):
        """A committed artifact regenerated by a daily cron must not churn.
        rdflib emits named graphs in arbitrary order, so the exporter sorts
        N-Quads lines; without that, every rebuild rewrites the whole file."""
        nq = REPO / "vault/graph/graph.nq"
        if not nq.is_file():
            self.skipTest("graph.nq not exported")
        before = nq.read_bytes()
        subprocess.run([sys.executable, str(KG / "to_rdf.py")],
                       capture_output=True, check=True)
        self.assertEqual(before, nq.read_bytes(),
                         "RDF export is not byte-deterministic across runs")

    def test_shacl_detects_an_injected_cycle(self):
        """A validator that only ever passes is worthless — prove it can fail."""
        from pyshacl import validate
        from rdflib import Graph, Namespace, Literal, URIRef
        from rdflib.namespace import RDF, RDFS
        VS = Namespace("https://skillquarium.dev/ontology/")
        VID = Namespace("https://skillquarium.dev/id/")
        g = Graph()
        for t in self.g:
            g.add(t)
        dom = URIRef("https://skillquarium.dev/id/domain_software-dev")
        for a, b in (("cyc_a", "cyc_b"), ("cyc_b", "cyc_a")):
            g.add((VID[a], RDF.type, VS.Skill))
            g.add((VID[a], RDFS.label, Literal(a)))
            g.add((VID[a], VS.in_domain, dom))
            g.add((VID[a], VS.chains_to, VID[b]))
        shapes = Graph().parse(str(REPO / ".skill-vault/ontology/shapes.ttl"), format="turtle")
        conforms, _, text = validate(g, shacl_graph=shapes, advanced=True, inference="none")
        self.assertFalse(conforms, "SHACL failed to detect a chains_to cycle")
        self.assertIn("cycle", text.lower())


class TestObservationAndAssertionGuards(unittest.TestCase):
    def test_malformed_observation_records_are_skipped(self):
        import build_kg  # noqa: PLC0415
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        write(root / ".skill-vault/observations/episodes.jsonl",
              "null\n[]\n\"text\"\n"
              '{"used": ["alpha"], "outcome": "success", "ts": "2026-01-01"}\n'
              '{"used": "alpha", "outcome": "success"}\n')
        original = build_kg.OBSERVATIONS_DIR
        build_kg.OBSERVATIONS_DIR = root / ".skill-vault" / "observations"
        self.addCleanup(setattr, build_kg, "OBSERVATIONS_DIR", original)
        episodes = build_kg.load_observations()
        self.assertEqual(len(episodes), 1)
        self.assertEqual(episodes[0]["used"], ["alpha"])

    def test_last_used_keeps_the_latest_timestamp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        fixture = FixtureVault(root)
        write(root / ".skill-vault/observations/episodes.jsonl",
              '{"used": ["alpha"], "outcome": "success", "ts": "2026-01-01"}\n'
              '{"used": ["alpha"], "outcome": "success", "ts": "2026-08-01"}\n'
              '{"used": ["alpha"], "outcome": "success", "ts": "2026-03-01"}\n')
        graph = fixture.build()
        node = next(n for n in graph["nodes"] if n["id"] == "alpha")
        self.assertEqual(node["last_used"], "2026-08-01")
        observed = [e for e in graph["edges"] if e["provenance"] == "OBSERVED"]
        self.assertTrue(all(e["weight"] < 1.0 for e in observed) or not observed)

    def test_unknown_assertion_endpoints_are_rejected(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        fixture = FixtureVault(root)
        write(root / ".skill-vault/ontology/assertions/bad.json",
              json.dumps({"edges": [{
                  "src": "scanppy", "rel": "alternative_to", "dst": "alpha",
                  "justification": "typo should not create an asserted edge",
              }]}))
        graph = fixture.build()
        rels = {(e["src"], e["rel"], e["dst"]) for e in graph["edges"]}
        self.assertNotIn(("scanppy", "alternative_to", "alpha"), rels)
        self.assertNotIn("scanppy", {n["id"] for n in graph["nodes"]})


if __name__ == "__main__":
    unittest.main()
