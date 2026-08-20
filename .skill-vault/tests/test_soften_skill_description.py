import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "soften_skill_description.sh"


def write_skill(root: Path, name: str, description: str, body: str = "# Body\nMUST stay.\n") -> Path:
    folder = root / "skills" / name
    folder.mkdir(parents=True)
    path = folder / "SKILL.md"
    path.write_text(
        f"---\nname: {name}\n{description}---\n\n{body}",
        encoding="utf-8",
    )
    return path


def description_of(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    fm = text.split("\n---\n", 1)[0]
    lines = fm.splitlines()[1:]  # drop opening ---
    # reassemble description, possibly folded
    out = []
    capturing = False
    folded = False
    for line in lines:
        if line.startswith("description:"):
            rest = line[len("description:") :].strip()
            if rest in {">", ">-", ">+"}:
                capturing = True
                folded = True
                continue
            if rest.startswith('"') and rest.endswith('"'):
                return rest[1:-1].replace('\\"', '"')
            return rest
        if capturing:
            if line.startswith("  "):
                out.append(line.strip())
            elif not line.strip():
                continue
            else:
                break
    return " ".join(out) if folded else " ".join(out)


class SoftenSkillDescriptionTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        mode = SCRIPT.stat().st_mode
        if not mode & stat.S_IXUSR:
            self.fail(f"{SCRIPT} is not executable")

    def run_script(self, *extra):
        return subprocess.run(
            ["bash", str(SCRIPT), *extra, str(self.root)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_softens_must_always_and_mandatory_catalog_copy(self):
        figma = write_skill(
            self.root,
            "figma-use",
            'description: "**MANDATORY prerequisite** — you MUST invoke this skill BEFORE every `use_figma` tool call. NEVER call `use_figma` directly without loading this skill first. Trigger whenever the user wants to edit nodes."\n',
        )
        brain = write_skill(
            self.root,
            "brainstorming",
            'description: "You MUST use this before any creative work - creating features."\n',
        )
        superpowers = write_skill(
            self.root,
            "using-superpowers",
            "description: Use when starting any conversation - establishes how to find and use skills, requiring Skill tool invocation before ANY response including clarifying questions\n",
        )
        shopify = write_skill(
            self.root,
            "shopify-custom-data",
            'description: "MUST be used first when prompts mention Metafields or Metaobjects."\n',
        )
        resources = write_skill(
            self.root,
            "get-available-resources",
            "description: This skill should be used at the start of any computationally intensive scientific task to detect GPUs.\n",
        )
        aeon = write_skill(
            self.root,
            "aeon",
            "description: This skill should be used for time series machine learning tasks including classification.\n",
        )
        run_tests = write_skill(
            self.root,
            "run-tests",
            "description: >\n  Recommend the exact dotnet test command. ALWAYS use when the\n  user asks to run .NET tests.\n",
        )
        briefing = write_skill(
            self.root,
            "morning-briefing",
            'description: "Generates a morning briefing. Use this skill whenever someone asks. Trigger broadly — if someone wants a summary, this skill should activate."\n',
        )
        base44 = write_skill(
            self.root,
            "base44-cli",
            'description: "The base44 CLI is used for EVERYTHING related to base44 projects. When you plan or implement a feature, you must learn this skill"\n',
        )
        untouched = write_skill(
            self.root,
            "pandas",
            "description: Use when working with tabular data in Python.\n",
            body="# Body\nYou MUST follow pandas dtypes.\n",
        )

        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("softened 9 skill descriptions", result.stdout)

        figma_desc = description_of(figma)
        self.assertNotIn("MANDATORY", figma_desc)
        self.assertNotIn("MUST invoke", figma_desc)
        self.assertNotIn("NEVER call", figma_desc)
        self.assertIn("Load this skill before every", figma_desc)
        self.assertIn("`use_figma`", figma_desc)

        self.assertTrue(description_of(brain).startswith("Use before"))
        self.assertNotIn("MUST", description_of(brain))

        sp = description_of(superpowers)
        self.assertNotIn("any conversation", sp.lower())
        self.assertNotIn("ANY response", sp)
        self.assertIn("discovering which skill applies", sp)

        self.assertTrue(description_of(shopify).startswith("Use first when"))
        self.assertIn("Use at the start of", description_of(resources))
        self.assertTrue(description_of(aeon).startswith("Use for time series"))
        self.assertNotRegex(description_of(run_tests), r"(?i)always use")
        self.assertIn("Use when the user asks", description_of(run_tests))

        briefing_desc = description_of(briefing)
        self.assertNotIn("Trigger broadly", briefing_desc)
        self.assertNotIn("this skill should activate", briefing_desc)

        base_desc = description_of(base44)
        self.assertNotIn("EVERYTHING", base_desc)
        self.assertNotIn("must learn", base_desc.lower())

        self.assertEqual(
            description_of(untouched),
            "Use when working with tabular data in Python.",
        )
        self.assertIn("You MUST follow pandas dtypes.", untouched.read_text(encoding="utf-8"))

        again = self.run_script()
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn("softened 0 skill descriptions", again.stdout)

    def test_dry_run_does_not_write(self):
        path = write_skill(
            self.root,
            "figma-use",
            'description: "MUST be used first when prompts mention Metafields."\n',
        )
        before = path.read_text(encoding="utf-8")
        result = self.run_script("--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("would soften", result.stdout)
        self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_skips_symlinked_skill_files(self):
        real = write_skill(
            self.root,
            "real-skill",
            'description: "You MUST use this before any creative work."\n',
        )
        alias_dir = self.root / "skills" / "alias-skill"
        alias_dir.mkdir()
        os.symlink(real, alias_dir / "SKILL.md")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.count("softened "), 2)  # one path line + summary
        self.assertIn("skills/real-skill/SKILL.md", result.stdout)
        self.assertNotIn("alias-skill", result.stdout)
