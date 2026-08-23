import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "import-scientific-agents.py"
SPEC = importlib.util.spec_from_file_location("import_scientific_agents", MODULE_PATH)
importer = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = importer
SPEC.loader.exec_module(importer)


class ScientificAgentPatchTests(unittest.TestCase):
    def test_apply_local_patches_replaces_text_and_records_ids(self):
        rendered = (
            "---\n"
            "name: fusion-scientist\n"
            "metadata:\n"
            "  source-commit: abc123\n"
            "  scientific-agents-profile: true\n"
            "---\n"
            "\n"
            "Imported from upstream at commit `abc123`.\n"
            "\n"
            "ITER uses **beryllium** first wall and **tungsten** divertor; carbon is retired.\n"
        )
        patches = {
            "fusion-scientist": [
                {
                    "id": "iter-2024-tungsten-first-wall",
                    "find": "ITER uses **beryllium** first wall and **tungsten** divertor",
                    "replace": (
                        "ITER's 2024 baseline specifies **tungsten** armour "
                        "for the first wall and divertor"
                    ),
                }
            ]
        }

        updated, applied = importer.apply_local_patches(
            rendered, slug="fusion-scientist", patches=patches
        )

        self.assertEqual(applied, ["iter-2024-tungsten-first-wall"])
        self.assertIn("tungsten** armour for the first wall and divertor", updated)
        self.assertNotIn("beryllium** first wall", updated)
        self.assertIn("  local-patches:", updated)
        self.assertIn("    - iter-2024-tungsten-first-wall", updated)
        self.assertIn("vault overlays, not upstream text", updated)

    def test_apply_local_patches_leaves_unmatched_skills_unchanged(self):
        rendered = "---\nname: other\n---\n\nno match\n"
        patches = {
            "fusion-scientist": [
                {"id": "iter-2024-tungsten-first-wall", "find": "x", "replace": "y"}
            ]
        }

        updated, applied = importer.apply_local_patches(
            rendered, slug="other", patches=patches
        )

        self.assertEqual(applied, [])
        self.assertEqual(updated, rendered)

    def test_load_patches_reads_json(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "scientific-agent-patches.json"
        path.write_text(
            json.dumps(
                {
                    "fusion-scientist": [
                        {"id": "iter-2024-tungsten-first-wall", "find": "a", "replace": "b"}
                    ]
                }
            ),
            encoding="utf-8",
        )

        loaded = importer.load_local_patches(path)
        self.assertEqual(
            loaded["fusion-scientist"][0]["id"], "iter-2024-tungsten-first-wall"
        )


if __name__ == "__main__":
    unittest.main()
