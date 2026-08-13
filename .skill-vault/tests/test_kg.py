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
            write(root / f"vault/notes/testing/{name}.md",
                  f"---\ntitle: {name}\ndomain: testing\nsource: skills/{name}/SKILL.md\n---\n")
        write(root / "vault/recipes/demo.md",
              "---\ntitle: Demo pipeline\n---\n# Demo\n\n"
              "1. **[alpha](../notes/testing/alpha.md)** — start here.\n"
              "2. **[beta](../notes/testing/beta.md)** — then this.\n")
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
        """Recipes must be recoverable from a partial hit — the COMP fix."""
        edges = [e for e in self.graph["edges"] if e["rel"] == "co_occurs_with"]
        self.assertGreater(len(edges), 0, "no hyperedge-derived co-occurrence")

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


if __name__ == "__main__":
    unittest.main()
