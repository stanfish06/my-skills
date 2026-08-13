import os
from pathlib import Path
import shlex
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
HELPER = REPO_ROOT / ".skill-vault" / "install-ui-ux-pro-max.sh"
BUNDLE_SKILLS = (
    "ui-ux-pro-max",
    "banner-design",
    "brand",
    "design-system",
    "design",
    "slides",
    "ui-styling",
)


class UiUxProMaxInstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.home = self.root / "home"
        self.home.mkdir()
        self.skills_dir = self.home / ".agents" / "skills"
        self.log_path = self.root / "commands.log"

    def run_installer(self, **overrides):
        environment = os.environ.copy()
        environment.update(
            {
                "HOME": str(self.home),
                "COMMAND_LOG": str(self.log_path),
            }
        )
        environment.update(overrides)

        names = " ".join(BUNDLE_SKILLS)
        script = f"""
source {shlex.quote(str(HELPER))}
npx() {{
  printf 'npx' >> "$COMMAND_LOG"
  printf ' %s' "$@" >> "$COMMAND_LOG"
  printf '\n' >> "$COMMAND_LOG"

  mkdir -p "$HOME/.agents/skills"
  case "${{FAKE_INSTALL_RESULT:-complete}}" in
    complete)
      for name in {names}; do
        mkdir -p "$HOME/.agents/skills/$name"
        printf '%s\n' "$name" > "$HOME/.agents/skills/$name/SKILL.md"
      done
      ;;
    incomplete)
      mkdir -p "$HOME/.agents/skills/ui-ux-pro-max"
      printf 'ui-ux-pro-max\n' > "$HOME/.agents/skills/ui-ux-pro-max/SKILL.md"
      ;;
    fail)
      mkdir -p "$HOME/.agents/skills/ui-ux-pro-max"
      printf 'partial\n' > "$HOME/.agents/skills/ui-ux-pro-max/SKILL.md"
      return 23
      ;;
  esac
}}
install_ui_ux_pro_max
"""
        return subprocess.run(
            ["bash", "-c", script],
            cwd=REPO_ROOT,
            env=environment,
            text=True,
            capture_output=True,
            check=False,
        )

    def command_log(self):
        if not self.log_path.exists():
            return []
        return self.log_path.read_text().splitlines()

    def test_installs_complete_bundle_with_pinned_cli_in_canonical_store(self):
        result = self.run_installer()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.command_log(),
            [
                "npx -y ui-ux-pro-max-cli@2.14.1 init "
                "--ai universal --global --force"
            ],
        )
        for name in BUNDLE_SKILLS:
            self.assertTrue((self.skills_dir / name / "SKILL.md").is_file())
        self.assertEqual(
            (self.skills_dir / ".ui-ux-pro-max-managed").read_text(),
            "2.14.1\n",
        )

    def test_skip_avoids_all_work(self):
        result = self.run_installer(UI_UX_PRO_MAX_SKIP="1")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.command_log(), [])
        self.assertIn("skipped", result.stdout)

    def test_refuses_to_overwrite_unmanaged_bundle_name(self):
        collision = self.skills_dir / "design"
        collision.mkdir(parents=True)
        (collision / "SKILL.md").write_text("user-owned\n")

        result = self.run_installer()

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.command_log(), [])
        self.assertIn("refusing to overwrite unmanaged skill", result.stderr)
        self.assertEqual((collision / "SKILL.md").read_text(), "user-owned\n")

    def test_managed_bundle_can_be_refreshed_with_version_override(self):
        self.skills_dir.mkdir(parents=True)
        (self.skills_dir / ".ui-ux-pro-max-managed").write_text("2.14.1\n")
        for name in BUNDLE_SKILLS:
            skill_dir = self.skills_dir / name
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text("old\n")

        result = self.run_installer(UI_UX_PRO_MAX_CLI_VERSION="2.15.0")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.command_log(),
            [
                "npx -y ui-ux-pro-max-cli@2.15.0 init "
                "--ai universal --global --force"
            ],
        )
        self.assertEqual(
            (self.skills_dir / ".ui-ux-pro-max-managed").read_text(),
            "2.15.0\n",
        )

    def test_failed_first_install_removes_partial_bundle(self):
        result = self.run_installer(FAKE_INSTALL_RESULT="fail")

        self.assertEqual(result.returncode, 23)
        for name in BUNDLE_SKILLS:
            self.assertFalse((self.skills_dir / name).exists())
        self.assertFalse((self.skills_dir / ".ui-ux-pro-max-managed").exists())

    def test_incomplete_first_install_is_rejected_and_cleaned_up(self):
        result = self.run_installer(FAKE_INSTALL_RESULT="incomplete")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("did not install the complete bundle", result.stderr)
        for name in BUNDLE_SKILLS:
            self.assertFalse((self.skills_dir / name).exists())
        self.assertFalse((self.skills_dir / ".ui-ux-pro-max-managed").exists())

    def test_root_installer_exposes_ui_ux_extra_and_aliases(self):
        installer = REPO_ROOT / "install-skills.sh"
        source = installer.read_text()

        self.assertIn(
            'source "$VAULT_DIR/.skill-vault/install-ui-ux-pro-max.sh"', source
        )
        self.assertIn("EXTRA_UI_UX", source)
        self.assertEqual(source.count("install_ui_ux_pro_max"), 1)
        self.assertIn(
            "ui-ux-pro-max: skipped (pass --extras ui-ux to install)", source
        )

        help_result = subprocess.run(
            ["bash", str(installer), "--help"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(help_result.returncode, 0, help_result.stderr)
        self.assertIn("ui-ux", help_result.stdout)
        self.assertIn("ui-ux-pro-max", help_result.stdout)
        self.assertIn("uipro", help_result.stdout)


class UiUxProMaxNavigationTests(unittest.TestCase):
    def test_bundle_skill_names_are_transient_install_state(self):
        build_source = (REPO_ROOT / ".skill-vault" / "build.py").read_text()

        for name in BUNDLE_SKILLS:
            self.assertIn(f'"{name}"', build_source)
        self.assertIn("def is_ui_ux_pro_max_skill", build_source)
        self.assertIn("is_ui_ux_pro_max_skill(s)", build_source)
        self.assertIn("generated_wrapper_count", build_source)


if __name__ == "__main__":
    unittest.main()
