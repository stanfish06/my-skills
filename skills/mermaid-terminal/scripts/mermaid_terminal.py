#!/usr/bin/env python3
"""Render Mermaid source locally and preview it with Kitty graphics."""

from __future__ import annotations

import argparse
import contextlib
import fcntl
import os
import re
import shutil
import signal
import struct
import subprocess
import sys
import tempfile
import termios
import time
from collections.abc import Iterator
from pathlib import Path
from typing import BinaryIO

MERMAID_CLI_VERSION = "11.16.0"
MARKDOWN_SUFFIXES = {".md", ".mdown", ".markdown", ".mdx"}
FENCE_START = re.compile(r"^\s*(`{3,}|~{3,})\s*mermaid(?:\s+.*)?$", re.IGNORECASE)
ALTERNATE_SCREEN_ENTER = b"\x1b[?1049h\x1b[2J\x1b[H"
ALTERNATE_SCREEN_EXIT = b"\x1b[?1049l"


class PreviewError(RuntimeError):
    """A user-actionable rendering or display failure."""


def extract_mermaid_block(text: str) -> str | None:
    """Return the first fenced Mermaid block, or None when no block exists."""

    lines = text.splitlines()
    for start, line in enumerate(lines):
        match = FENCE_START.match(line)
        if not match:
            continue
        fence = match.group(1)
        closing = re.compile(rf"^\s*{re.escape(fence[0])}{{{len(fence)},}}\s*$")
        body: list[str] = []
        for candidate in lines[start + 1 :]:
            if closing.match(candidate):
                return "\n".join(body).strip() + "\n"
            body.append(candidate)
        raise PreviewError("Mermaid fence is missing its closing delimiter")
    return None


def mermaid_source(text: str, markdown: bool) -> str:
    block = extract_mermaid_block(text)
    if block is not None:
        source = block
    elif markdown:
        raise PreviewError("Markdown input contains no fenced Mermaid block")
    else:
        source = text.strip() + "\n"
    if not source.strip():
        raise PreviewError("Mermaid source is empty")
    return source


def resolve_theme(requested: str) -> str:
    if requested != "auto":
        return requested
    background = os.environ.get("COLORFGBG", "").rsplit(";", 1)[-1]
    return "neutral" if background in {"7", "15"} else "dark"


def renderer_command(no_bootstrap: bool) -> list[str]:
    if executable := shutil.which("mmdc"):
        return [executable]
    if no_bootstrap:
        raise PreviewError(
            "mmdc is not on PATH; install @mermaid-js/mermaid-cli or remove --no-bootstrap"
        )
    package = f"@mermaid-js/mermaid-cli@{MERMAID_CLI_VERSION}"
    if executable := shutil.which("bunx"):
        return [executable, "--bun", package]
    if executable := shutil.which("npx"):
        return [executable, "--yes", "--package", package, "mmdc"]
    raise PreviewError("rendering requires mmdc, Bun, or npm/npx")


def render(
    source: Path,
    output: Path,
    theme: str,
    scale: float,
    background: str,
    no_bootstrap: bool,
) -> None:
    command = renderer_command(no_bootstrap)
    command.extend(
        [
            "-i",
            str(source),
            "-o",
            str(output),
            "-t",
            theme,
            "-b",
            background,
            "-s",
            str(scale),
        ]
    )
    completed = subprocess.run(command, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        detail = (
            completed.stderr.strip()
            or completed.stdout.strip()
            or "unknown renderer error"
        )
        raise PreviewError(f"Mermaid rendering failed:\n{detail}")
    if not output.is_file() or output.stat().st_size == 0:
        raise PreviewError(f"renderer produced no PNG at {output}")


def terminal_device_paths() -> Iterator[str]:
    seen: set[str] = set()
    controlling_terminal = os.ctermid()
    if controlling_terminal:
        seen.add(controlling_terminal)
        yield controlling_terminal

    ps = shutil.which("ps")
    if not ps:
        return
    pid = os.getppid()
    for _ in range(12):
        completed = subprocess.run(
            [ps, "-o", "ppid=,tty=", "-p", str(pid)],
            text=True,
            capture_output=True,
            check=False,
        )
        fields = completed.stdout.split()
        if completed.returncode != 0 or len(fields) < 2:
            return
        parent_pid, tty = fields[:2]
        if tty not in {"?", "??", "-"}:
            path = tty if tty.startswith("/dev/") else f"/dev/{tty}"
            if path not in seen:
                seen.add(path)
                yield path
        try:
            next_pid = int(parent_pid)
        except ValueError:
            return
        if next_pid <= 1 or next_pid == pid:
            return
        pid = next_pid


@contextlib.contextmanager
def terminal_output() -> Iterator[BinaryIO | None]:
    if sys.stdout.isatty():
        yield None
        return

    for path in terminal_device_paths():
        try:
            with open(path, "r+b", buffering=0) as terminal:
                if terminal.isatty():
                    yield terminal
                    return
        except OSError:
            continue
    raise PreviewError(
        "inline display requires a controlling terminal; no terminal device was found"
    )


def terminal_geometry(fd: int) -> tuple[int, int, int, int]:
    """Return (rows, cols, xpix, ypix) without querying the terminal."""

    rows = cols = xpix = ypix = 0
    with contextlib.suppress(OSError):
        packed = fcntl.ioctl(fd, termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0))
        rows, cols, xpix, ypix = struct.unpack("HHHH", packed)
    if rows <= 0 or cols <= 0:
        cols, rows = 80, 24
    # estimate pixels when the terminal leaves winsize pixel fields at zero
    if xpix <= 0 or ypix <= 0:
        xpix, ypix = cols * 9, rows * 18
    return rows, cols, xpix, ypix


def run_icat(
    command: list[str],
    stdin: int | BinaryIO | None = None,
    stdout: int | BinaryIO | None = None,
) -> None:
    try:
        completed = subprocess.run(
            command,
            stdin=stdin,
            stdout=stdout,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise PreviewError("kitten icat did not finish within 30s") from error
    if completed.returncode != 0:
        detail = (completed.stderr or b"").decode(errors="replace").strip()
        raise PreviewError(
            "terminal image display failed; verify Ghostty/Kitty graphics support "
            f"or use --no-display\n{detail}".rstrip()
        )


def display(output: Path, hold_seconds: float) -> None:
    kitten = shutil.which("kitten")
    if not kitten:
        raise PreviewError("inline display requires the kitten executable")
    command = [
        kitten,
        "icat",
        "--align=left",
        "--transfer-mode=stream",
        "--stdin=no",
    ]
    with terminal_output() as terminal:
        if terminal is None:
            # attached to a real terminal: icat may query it directly
            command.extend(["--fit=both", str(output)])
            run_icat(command)
            return

        # Captured shell (agent host owns the terminal): icat must not query the
        # terminal or read keys - the host's input reader swallows the replies.
        # Supply geometry from ioctl and hold the preview for a fixed time.
        rows, cols, xpix, ypix = terminal_geometry(terminal.fileno())
        place_cols = max(cols - 4, 10)
        place_rows = max(rows - 3, 5)
        command.extend(
            [
                f"--use-window-size={cols},{rows},{xpix},{ypix}",
                f"--place={place_cols}x{place_rows}@2x1",
                str(output),
            ]
        )
        terminal.write(ALTERNATE_SCREEN_ENTER)
        try:
            run_icat(command, stdin=subprocess.DEVNULL, stdout=terminal)
            footer = (
                "Mermaid preview - interrupt (Esc or Ctrl-C) to close"
                if hold_seconds == 0
                else f"Mermaid preview - closing in {hold_seconds:g}s"
            )[:cols]
            terminal.write(f"\x1b[{rows};1H".encode() + footer.encode())
            if hold_seconds == 0:
                while True:
                    time.sleep(3600)
            time.sleep(hold_seconds)
        finally:
            terminal.write(ALTERNATE_SCREEN_EXIT)
        print(f"preview shown on the session terminal for {hold_seconds:g}s")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render Mermaid source and preview it through the Kitty graphics protocol."
    )
    parser.add_argument(
        "input", nargs="?", default="-", help=".mmd/Markdown file or - for stdin"
    )
    parser.add_argument(
        "--output", type=Path, help="keep the rendered PNG at this path"
    )
    parser.add_argument(
        "--no-display", action="store_true", help="render without terminal display"
    )
    parser.add_argument(
        "--theme",
        choices=["auto", "default", "forest", "dark", "neutral", "base"],
        default="auto",
    )
    parser.add_argument(
        "--background", default="transparent", help="Mermaid CLI background color"
    )
    parser.add_argument(
        "--scale", type=float, default=1.5, help="Mermaid CLI scale factor"
    )
    parser.add_argument(
        "--no-bootstrap",
        action="store_true",
        help="require mmdc on PATH instead of using Bun or npm",
    )
    parser.add_argument(
        "--hold-seconds",
        type=float,
        default=0.0,
        help="captured-shell preview duration; 0 holds until interrupted (default)",
    )
    args = parser.parse_args(argv)
    if args.scale <= 0:
        parser.error("--scale must be greater than zero")
    if args.hold_seconds < 0:
        parser.error("--hold-seconds must be zero or greater")
    if args.no_display and args.output is None:
        parser.error("--no-display requires --output so the result is not discarded")
    return args


def terminate(signum: int, _frame: object) -> None:
    raise SystemExit(128 + signum)


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    # restore the screen (display's finally) when the agent host or Bash
    # timeout tears the preview down
    signal.signal(signal.SIGTERM, terminate)
    signal.signal(signal.SIGHUP, terminate)
    try:
        if args.input == "-":
            text = sys.stdin.read()
            markdown = extract_mermaid_block(text) is not None
        else:
            input_path = Path(args.input).expanduser().resolve()
            if not input_path.is_file():
                raise PreviewError(f"input file not found: {input_path}")
            text = input_path.read_text(encoding="utf-8")
            markdown = input_path.suffix.lower() in MARKDOWN_SUFFIXES

        source_text = mermaid_source(text, markdown)
        with tempfile.TemporaryDirectory(prefix="mermaid-terminal-") as temp_dir:
            source = Path(temp_dir) / "diagram.mmd"
            source.write_text(source_text, encoding="utf-8")
            output = (
                args.output.expanduser().resolve()
                if args.output is not None
                else Path(temp_dir) / "diagram.png"
            )
            output.parent.mkdir(parents=True, exist_ok=True)
            render(
                source,
                output,
                resolve_theme(args.theme),
                args.scale,
                args.background,
                args.no_bootstrap,
            )
            if not args.no_display:
                display(output, args.hold_seconds)
            if args.output is not None:
                print(output)
        return 0
    except KeyboardInterrupt:
        return 130
    except (OSError, PreviewError) as error:
        print(f"mermaid-terminal: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
