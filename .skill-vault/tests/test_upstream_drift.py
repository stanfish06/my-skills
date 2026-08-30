import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


VAULT = Path(__file__).resolve().parents[1]
MODULE_PATH = VAULT / "check-upstream-drift.py"
SPEC = importlib.util.spec_from_file_location("check_upstream_drift", MODULE_PATH)
drift = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = drift
SPEC.loader.exec_module(drift)


def lock_file(root, skills):
    path = root / ".skill-lock.json"
    path.write_text(json.dumps({"version": 3, "skills": skills}), encoding="utf-8")
    return path


class FolderResolutionTests(unittest.TestCase):
    def test_skill_md_suffix_is_stripped_case_insensitively(self):
        self.assertEqual(drift.folder_of("skills/adaptyv/SKILL.md"), "skills/adaptyv")
        self.assertEqual(drift.folder_of("skills/adaptyv/skill.md"), "skills/adaptyv")
        self.assertEqual(drift.folder_of("skills\\adaptyv\\SKILL.md"), "skills/adaptyv")


class LockClassificationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.original = drift.repo_tree
        self.addCleanup(lambda: setattr(drift, "repo_tree", self.original))

    def stub_tree(self, folders):
        tree = {"tree": [{"path": p, "type": "tree", "sha": s} for p, s in folders.items()]}
        drift.repo_tree = lambda source: tree

    def test_entries_split_into_current_behind_and_unreachable(self):
        self.stub_tree({"skills/kept": "aaa", "skills/moved": "bbb"})
        path = lock_file(self.root, {
            "kept": {"source": "o/r", "skillPath": "skills/kept/SKILL.md",
                     "skillFolderHash": "aaa"},
            "moved": {"source": "o/r", "skillPath": "skills/moved/SKILL.md",
                      "skillFolderHash": "old"},
            "renamed": {"source": "o/r", "skillPath": "old-dir/renamed/SKILL.md",
                        "skillFolderHash": "ccc"},
        })

        report, errors = drift.check_lock(path)

        self.assertEqual(errors, [])
        self.assertEqual(report["o/r"]["current"], ["kept"])
        self.assertEqual(report["o/r"]["behind"], ["moved"])
        self.assertEqual(report["o/r"]["unreachable"], ["renamed"])

    def test_unreadable_source_is_an_error_not_a_silent_pass(self):
        drift.repo_tree = lambda source: None
        path = lock_file(self.root, {
            "x": {"source": "o/r", "skillPath": "skills/x/SKILL.md", "skillFolderHash": "a"},
        })

        report, errors = drift.check_lock(path)

        self.assertEqual(report, {})
        self.assertEqual(len(errors), 1)
        self.assertIn("o/r", errors[0])

    def test_drift_count_drives_the_exit_code(self):
        clean = {"o/r": {"current": ["a"], "behind": [], "unreachable": []}}
        dirty = {"o/r": {"current": [], "behind": ["a"], "unreachable": ["b"]}}
        self.assertEqual(drift.render(clean, [], [])[1], 0)
        self.assertEqual(drift.render(dirty, [], [])[1], 2)


class PinnedProfileTests(unittest.TestCase):
    def test_frontmatter_pins_are_grouped_by_repo_and_commit(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        for name in ("botanist", "geochemist"):
            path = root / "skills" / name / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "---\nname: %s\nmetadata:\n  source-repo: K-Dense-AI/scientific-agents\n"
                "  source-commit: 896ed6ed\n---\n" % name,
                encoding="utf-8",
            )

        pinned = drift.pinned_profiles(root)

        self.assertEqual(dict(pinned["K-Dense-AI/scientific-agents"]), {"896ed6ed": 2})


if __name__ == "__main__":
    unittest.main()
