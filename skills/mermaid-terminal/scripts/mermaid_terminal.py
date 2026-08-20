#!/usr/bin/env python3
"""Render Mermaid source locally and preview it with Kitty graphics."""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

MERMAID_CLI_VERSION = "11.16.0"
MARKDOWN_SUFFIXES = {".md", ".mdown", ".markdown", ".mdx"}
FENCE_START = re.compile(r"^\s*(`{3,}|~{3,})\s*mermaid(?:\s+.*)?$", re.IGNORECASE)


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


def display(output: Path) -> None:
    kitten = shutil.which("kitten")
    if not kitten:
        raise PreviewError("inline display requires the kitten executable")
    if not sys.stdout.isatty():
        raise PreviewError(
            "inline display requires an interactive terminal; use --no-display --output FILE"
        )
    command = [
        kitten,
        "icat",
        "--align=left",
        "--transfer-mode=stream",
        "--stdin=no",
        str(output),
    ]
    completed = subprocess.run(command, check=False)
    if completed.returncode != 0:
        raise PreviewError(
            "terminal image display failed; verify Ghostty/Kitty graphics support or use --no-display"
        )


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
    args = parser.parse_args(argv)
    if args.scale <= 0:
        parser.error("--scale must be greater than zero")
    if args.no_display and args.output is None:
        parser.error("--no-display requires --output so the result is not discarded")
    return args


def run(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
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
                display(output)
            if args.output is not None:
                print(output)
        return 0
    except (OSError, PreviewError) as error:
        print(f"mermaid-terminal: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(run())
