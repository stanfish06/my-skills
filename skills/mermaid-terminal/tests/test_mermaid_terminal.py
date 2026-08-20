from __future__ import annotations

import importlib.util
import os
import subprocess
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).parents[1] / "scripts" / "mermaid_terminal.py"
SPEC = importlib.util.spec_from_file_location("mermaid_terminal", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class MermaidSourceTests(unittest.TestCase):
    def test_extracts_first_fenced_mermaid_block(self) -> None:
        text = """# Diagram

```mermaid
flowchart LR
  A --> B
```

```mermaid
flowchart TD
  C --> D
```
"""
        self.assertEqual(
            MODULE.mermaid_source(text, markdown=True), "flowchart LR\n  A --> B\n"
        )

    def test_accepts_tilde_fence_and_label_options(self) -> None:
        text = """~~~~mermaid title=Example
sequenceDiagram
  A->>B: Ping
~~~~
"""
        self.assertEqual(
            MODULE.mermaid_source(text, markdown=True),
            "sequenceDiagram\n  A->>B: Ping\n",
        )

    def test_rejects_markdown_without_mermaid(self) -> None:
        with self.assertRaisesRegex(MODULE.PreviewError, "no fenced Mermaid"):
            MODULE.mermaid_source("# No diagram\n", markdown=True)

    def test_rejects_unclosed_fence(self) -> None:
        with self.assertRaisesRegex(MODULE.PreviewError, "missing its closing"):
            MODULE.mermaid_source("```mermaid\nflowchart LR\n", markdown=True)

    def test_raw_source_is_preserved(self) -> None:
        self.assertEqual(
            MODULE.mermaid_source("flowchart LR\n A --> B\n", False),
            "flowchart LR\n A --> B\n",
        )


class ThemeTests(unittest.TestCase):
    def test_auto_theme_defaults_to_dark(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(MODULE.resolve_theme("auto"), "dark")

    def test_auto_theme_uses_neutral_for_light_background(self) -> None:
        with patch.dict(os.environ, {"COLORFGBG": "0;15"}, clear=True):
            self.assertEqual(MODULE.resolve_theme("auto"), "neutral")

    def test_explicit_theme_wins(self) -> None:
        self.assertEqual(MODULE.resolve_theme("forest"), "forest")


class DisplayTests(unittest.TestCase):
    def test_streams_png_through_kitten(self) -> None:
        completed = subprocess.CompletedProcess([], 0)
        with (
            patch.object(MODULE.shutil, "which", return_value="/usr/bin/kitten"),
            patch.object(MODULE.sys.stdout, "isatty", return_value=True),
            patch.object(MODULE.subprocess, "run", return_value=completed) as run,
        ):
            MODULE.display(Path("diagram.png"))

        command = run.call_args.args[0]
        self.assertEqual(command[:2], ["/usr/bin/kitten", "icat"])
        self.assertIn("--transfer-mode=stream", command)
        self.assertEqual(command[-1], "diagram.png")

    def test_rejects_captured_output(self) -> None:
        with (
            patch.object(MODULE.shutil, "which", return_value="/usr/bin/kitten"),
            patch.object(MODULE.sys.stdout, "isatty", return_value=False),
            self.assertRaisesRegex(MODULE.PreviewError, "interactive terminal"),
        ):
            MODULE.display(Path("diagram.png"))


if __name__ == "__main__":
    unittest.main()
