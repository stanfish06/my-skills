import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


VAULT = Path(__file__).resolve().parents[1]
MODULE_PATH = VAULT / "apply-local-overrides.py"
SPEC = importlib.util.spec_from_file_location("apply_local_overrides", MODULE_PATH)
overrides_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = overrides_module
SPEC.loader.exec_module(overrides_module)


def write_skill(root, name, text):
    path = root / "skills" / name / "SKILL.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class LocalOverrideMechanicsTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)

    def test_pending_override_is_written_and_is_idempotent(self):
        path = write_skill(self.root, "demo", "run docker-compose config\n")
        spec = {"demo": [{"id": "compose-v2", "find": "docker-compose config",
                          "replace": "docker compose config"}]}

        first = overrides_module.apply_overrides(spec, self.root)
        self.assertEqual(first["pending"], ["demo/compose-v2"])
        self.assertEqual(path.read_text(encoding="utf-8"), "run docker compose config\n")

        second = overrides_module.apply_overrides(spec, self.root)
        self.assertEqual(second["applied"], ["demo/compose-v2"])
        self.assertEqual(second["pending"], [])

    def test_check_mode_reports_without_writing(self):
        path = write_skill(self.root, "demo", "run docker-compose config\n")
        spec = {"demo": [{"id": "compose-v2", "find": "docker-compose config",
                          "replace": "docker compose config"}]}

        result = overrides_module.apply_overrides(spec, self.root, write=False)

        self.assertEqual(result["pending"], ["demo/compose-v2"])
        self.assertEqual(path.read_text(encoding="utf-8"), "run docker-compose config\n")

    def test_override_is_stale_when_upstream_rewrote_the_region(self):
        write_skill(self.root, "demo", "upstream rewrote this section\n")
        spec = {"demo": [{"id": "compose-v2", "find": "docker-compose config",
                          "replace": "docker compose config"}]}

        result = overrides_module.apply_overrides(spec, self.root)

        self.assertEqual(result["stale"], ["demo/compose-v2"])
        self.assertEqual(result["pending"], [])

    def test_missing_skill_is_reported(self):
        spec = {"gone": [{"id": "x", "find": "a", "replace": "b"}]}
        result = overrides_module.apply_overrides(spec, self.root)
        self.assertEqual(len(result["missing"]), 1)
        self.assertIn("skills/gone/SKILL.md", result["missing"][0])

    def test_load_rejects_incomplete_and_no_op_overrides(self):
        path = self.root / "overrides.json"
        path.write_text(json.dumps({"demo": [{"id": "x", "find": "a"}]}), encoding="utf-8")
        with self.assertRaises(ValueError):
            overrides_module.load_overrides(path)

        path.write_text(json.dumps({"demo": [{"id": "x", "find": "a", "replace": "a"}]}),
                        encoding="utf-8")
        with self.assertRaises(ValueError):
            overrides_module.load_overrides(path)


class TrackedOverridesTests(unittest.TestCase):
    """The committed tree must already satisfy every recorded override.

    If it does not, an upstream sync reverted a merged fix and nobody noticed --
    the failure mode issue #665 describes.
    """

    def test_every_recorded_override_is_applied_in_the_tracked_tree(self):
        recorded = overrides_module.load_overrides()
        self.assertTrue(recorded, "local-overrides.json should record at least one fix")

        result = overrides_module.apply_overrides(recorded, VAULT.parent, write=False)

        self.assertEqual(result["missing"], [], "override names a skill that is not on disk")
        self.assertEqual(result["stale"], [], "upstream rewrote the region; re-derive the fix")
        self.assertEqual(result["pending"], [], "an upstream sync reverted a local fix")


if __name__ == "__main__":
    unittest.main()
