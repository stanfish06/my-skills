from __future__ import annotations

import importlib.util
import os
import subprocess
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

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
            MODULE.display(Path("diagram.png"), hold_seconds=8.0)

        command = run.call_args.args[0]
        self.assertEqual(command[:2], ["/usr/bin/kitten", "icat"])
        self.assertIn("--transfer-mode=stream", command)
        self.assertIn("--fit=both", command)
        self.assertEqual(command[-1], "diagram.png")

    def test_uses_controlling_terminal_when_stdout_is_captured(self) -> None:
        completed = subprocess.CompletedProcess([], 0)
        terminal = MagicMock()
        terminal.isatty.return_value = True
        terminal.fileno.return_value = 9
        terminal.__enter__.return_value = terminal
        with (
            patch.object(MODULE.shutil, "which", return_value="/usr/bin/kitten"),
            patch.object(MODULE.sys.stdout, "isatty", return_value=False),
            patch.object(MODULE, "terminal_device_paths", return_value=["/dev/tty"]),
            patch.object(
                MODULE, "terminal_geometry", return_value=(40, 120, 1080, 720)
            ),
            patch.object(MODULE.time, "sleep") as sleep,
            patch("builtins.open", return_value=terminal) as open_terminal,
            patch.object(MODULE.subprocess, "run", return_value=completed) as run,
        ):
            MODULE.display(Path("diagram.png"), hold_seconds=5.0)

        open_terminal.assert_called_once_with("/dev/tty", "r+b", buffering=0)
        command = run.call_args.args[0]
        self.assertIn("--use-window-size=120,40,1080,720", command)
        self.assertIn("--place=116x37@2x1", command)
        self.assertNotIn("--hold", command)
        self.assertIs(run.call_args.kwargs["stdin"], subprocess.DEVNULL)
        self.assertIs(run.call_args.kwargs["stdout"], terminal)
        sleep.assert_called_once_with(5.0)
        writes = [call.args[0] for call in terminal.write.call_args_list]
        self.assertTrue(writes[0].startswith(b"\x1b[?1049h"))
        self.assertIn(b"Mermaid preview - closing in 5s", writes[1])
        self.assertEqual(writes[-1], b"\x1b[?1049l")

    def test_infinite_hold_restores_screen_on_interrupt(self) -> None:
        completed = subprocess.CompletedProcess([], 0)
        terminal = MagicMock()
        terminal.isatty.return_value = True
        terminal.fileno.return_value = 9
        terminal.__enter__.return_value = terminal
        with (
            patch.object(MODULE.shutil, "which", return_value="/usr/bin/kitten"),
            patch.object(MODULE.sys.stdout, "isatty", return_value=False),
            patch.object(MODULE, "terminal_device_paths", return_value=["/dev/tty"]),
            patch.object(
                MODULE, "terminal_geometry", return_value=(40, 120, 1080, 720)
            ),
            patch.object(MODULE.time, "sleep", side_effect=KeyboardInterrupt) as sleep,
            patch("builtins.open", return_value=terminal),
            patch.object(MODULE.subprocess, "run", return_value=completed),
            self.assertRaises(KeyboardInterrupt),
        ):
            MODULE.display(Path("diagram.png"), hold_seconds=0.0)

        sleep.assert_called_once_with(3600)
        writes = [call.args[0] for call in terminal.write.call_args_list]
        self.assertIn(b"interrupt (Esc or Ctrl-C) to close", writes[1])
        self.assertEqual(writes[-1], b"\x1b[?1049l")

    def test_geometry_estimates_missing_pixel_size(self) -> None:
        packed = MODULE.struct.pack("HHHH", 24, 80, 0, 0)
        with patch.object(MODULE.fcntl, "ioctl", return_value=packed):
            self.assertEqual(MODULE.terminal_geometry(9), (24, 80, 720, 432))

    def test_rejects_captured_output_without_controlling_terminal(self) -> None:
        with (
            patch.object(MODULE.shutil, "which", return_value="/usr/bin/kitten"),
            patch.object(MODULE.sys.stdout, "isatty", return_value=False),
            patch.object(MODULE, "terminal_device_paths", return_value=["/dev/tty"]),
            patch("builtins.open", side_effect=OSError),
            self.assertRaisesRegex(MODULE.PreviewError, "controlling terminal"),
        ):
            MODULE.display(Path("diagram.png"), hold_seconds=8.0)


if __name__ == "__main__":
    unittest.main()
