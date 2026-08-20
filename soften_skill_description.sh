#!/usr/bin/env bash
set -euo pipefail

# Rewrite coercive catalog `description:` fields in SKILL.md files.
# Upstream skill packs ship MUST / ALWAYS / "don't ignore" copy that hijacks
# matching; this vault re-applies a trigger-only description after each pull.
#
# Usage:
#   ./soften_skill_description.sh [--dry-run] [VAULT_ROOT]
#
# VAULT_ROOT defaults to this script's directory (the repo root). Skills are
# read from $VAULT_ROOT/skills.

VAULT_DIR="$(cd "$(dirname "$0")" && pwd -P)"
export SOFTEN_DEFAULT_ROOT="$VAULT_DIR"
cd "$VAULT_DIR"

exec python3 - "$@" <<'PY'
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(os.environ["SOFTEN_DEFAULT_ROOT"]).resolve()

# Self-referential catalog coercion only. Domain "must" / "mandatory" inside
# the skill body is left alone; we only rewrite the YAML description.
COERCION_NEEDLES = (
    "always use",
    "always invoke",
    "you must use",
    "you must invoke",
    "you must learn",
    "must be used",
    "mandatory prerequisite",
    "this skill should be used",
    "should be invoked",
    "trigger broadly",
    "this skill should activate",
    "before any response",
    "starting any conversation",
    "used for everything",
    "use this skill proactively",
    "without loading this skill first",
    "don't ignore",
    "do not ignore",
    "rules you must follow",
)

# More specific patterns first. Each pass is idempotent on already-softened text.
REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (r"(?is)\*\*MANDATORY prerequisite\*\*\s*[—–-]\s*", ""),
    (r"(?is)MANDATORY prerequisite\s*[—–-]\s*", ""),
    (r"(?i)you MUST invoke this skill BEFORE every", "Load this skill before every"),
    (r"(?i)NEVER call (`[^`]+`) directly without loading this skill first\.?\s*", ""),
    (r"(?i)Skipping it causes common, hard-to-debug failures\.\s*", ""),
    (r"(?i)You MUST use this before any", "Use before"),
    (r"(?i)MUST be used first when", "Use first when"),
    (r"(?i)This skill MUST be used whenever", "Use when"),
    (r"(?i)MUST be used whenever", "Use when"),
    (
        r"(?i)When you plan or implement a feature, you must learn this skill\.?",
        "Read this skill when planning or implementing a feature.",
    ),
    (r"(?i)you must learn this skill", "read this skill"),
    (r"(?i)is used for EVERYTHING related to", "covers"),
    (r"(?i)used for EVERYTHING related to", "covers"),
    (r"(?i)ALWAYS use this skill when", "Use when"),
    (r"(?i)ALWAYS use when", "Use when"),
    (r"(?i)This skill should be used at the start of any", "Use at the start of"),
    (r"(?i)This skill should be used when", "Use when"),
    (r"(?i)This skill should be used for", "Use for"),
    (r"(?i)This skill should be used to", "Use to"),
    (r"(?i)Should be invoked for", "Use for"),
    (r"(?i)[Ii]t should be invoked\s+when", "Use when"),
    (r"(?i)[Ii]t should be invoked", "Invoke it"),
    (r"(?i)Use this skill proactively\s+when", "Use when"),
    (r"(?i)Use this skill proactively", "Use when relevant"),
    (r"(?i)Trigger broadly\s*[—–-]\s*", ""),
    (r"(?i)\s*this skill should activate\.?", ""),
    (
        r"(?i)Use when starting any conversation\s*[-—–]\s*",
        "Use when discovering which skill applies — ",
    ),
    (
        r"(?i), requiring Skill tool invocation before ANY response including clarifying questions",
        "",
    ),
    (
        r"(?i)requiring Skill tool invocation before ANY response including clarifying questions",
        "helps locate and load the matching skill for the current task",
    ),
    (r"(?i)Rules you must follow for", "Rules for"),
    (r"(?i)don't ignore", "consider"),
    (r"(?i)do not ignore", "consider"),
)


def needs_soften(description: str) -> bool:
    lowered = description.lower()
    return any(needle in lowered for needle in COERCION_NEEDLES)


def soften(description: str) -> str:
    text = description.strip()
    for pattern, replacement in REPLACEMENTS:
        text = re.sub(pattern, replacement, text)
    # Hard rule: no catalog line may tell the agent to "always use" anything.
    text = re.sub(r"(?i)\balways use\b", "Use", text)
    text = re.sub(r"(?i)\balways invoke\b", "Invoke", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r" +([,;:])", r"\1", text)
    text = re.sub(r"\s*[—–]\s*[—–]\s*", " — ", text)
    text = text.strip(" \t—-")
    text = re.sub(r"  +", " ", text)
    if text:
        text = text[0].upper() + text[1:]
    return text


def yaml_double_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def fold_yaml(value: str, width: int = 88, indent: str = "  ") -> str:
    words = value.split()
    lines: list[str] = []
    current: list[str] = []
    length = 0
    for word in words:
        extra = len(word) + (1 if current else 0)
        if current and length + extra > width:
            lines.append(indent + " ".join(current))
            current = [word]
            length = len(word)
        else:
            current.append(word)
            length += extra
    if current:
        lines.append(indent + " ".join(current))
    return "\n".join(lines) + "\n"


def parse_description(frontmatter: str):
    """Return (start, end, parsed_text, style) or None.

    style is one of: 'quoted', 'folded', 'literal', 'plain'.
    """
    match = re.search(
        r"^(description:\s*)(?P<ind>[|>][+-]?)[ \t]*\n(?P<body>(?:[ \t]+.*\n?)*)",
        frontmatter,
        re.M,
    )
    if match:
        body = match.group("body")
        indent_match = re.match(r"[ \t]+", body)
        indent = indent_match.group(0) if indent_match else "  "
        chunks = []
        for raw_line in body.splitlines():
            if not raw_line.strip():
                chunks.append("")
                continue
            if raw_line.startswith(indent):
                chunks.append(raw_line[len(indent) :])
            else:
                chunks.append(raw_line.lstrip())
        indicator = match.group("ind")
        if indicator.startswith(">"):
            parsed = " ".join(part.strip() for part in chunks if part.strip())
            style = "folded"
        else:
            parsed = "\n".join(chunks).strip("\n")
            style = "literal"
        return match.start(), match.end(), parsed, style

    match = re.search(
        r"^(description:\s*)(?P<val>\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|[^\n]+)[ \t]*\n?",
        frontmatter,
        re.M,
    )
    if not match:
        return None
    raw = match.group("val").strip()
    if raw in {">", "|", ">-", "|-", ">+", "|+"}:
        return None
    if raw.startswith('"') and raw.endswith('"'):
        parsed = raw[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        style = "quoted"
    elif raw.startswith("'") and raw.endswith("'"):
        parsed = raw[1:-1].replace("''", "'")
        style = "quoted"
    else:
        parsed = raw
        style = "plain"
    return match.start(), match.end(), parsed, style


def render_description(value: str, style: str) -> str:
    if style == "folded":
        return "description: >\n" + fold_yaml(value)
    if style == "literal":
        indented = "\n".join(
            ("  " + line) if line else "" for line in value.split("\n")
        )
        return "description: |\n" + indented + "\n"
    # quoted / plain: quote whenever the value would be ambiguous YAML
    if style == "plain" and not re.search(r'[:#\[\]{}"\']', value) and "\n" not in value:
        return "description: " + value + "\n"
    return "description: " + yaml_double_quote(value) + "\n"


def split_frontmatter(text: str):
    if not text.startswith("---"):
        return None
    rest = text[3:]
    if rest.startswith("\r\n"):
        rest = rest[2:]
        opener = "---\r\n"
    elif rest.startswith("\n"):
        rest = rest[1:]
        opener = "---\n"
    else:
        return None
    if rest.startswith("---"):
        return None
    end = rest.find("\n---")
    if end < 0:
        return None
    fm = rest[:end]
    closer_and_body = rest[end:]  # starts with \n---
    return opener, fm, closer_and_body


def process_file(path: Path, dry_run: bool) -> bool:
    if path.is_symlink():
        return False
    try:
        original = path.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"skip {path}: {exc}", file=sys.stderr)
        return False
    split = split_frontmatter(original)
    if split is None:
        return False
    opener, frontmatter, closer_and_body = split
    parsed = parse_description(frontmatter)
    if parsed is None:
        return False
    start, end, description, style = parsed
    if not needs_soften(description):
        return False
    softened = soften(description)
    if softened == description:
        return False
    new_fm = frontmatter[:start] + render_description(softened, style) + frontmatter[end:]
    if new_fm == frontmatter:
        return False
    rel = path
    try:
        rel = path.resolve().relative_to(DEFAULT_ROOT)
    except ValueError:
        rel = path
    action = "would soften" if dry_run else "softened"
    print(f"{action} {rel}")
    if not dry_run:
        path.write_text(opener + new_fm + closer_and_body, encoding="utf-8")
    return True


def iter_skill_files(skills_dir: Path):
    skip_dirs = {"node_modules", ".git", "__pycache__"}
    for dirpath, dirnames, filenames in os.walk(skills_dir, followlinks=False):
        dirnames[:] = [name for name in dirnames if name not in skip_dirs]
        if "SKILL.md" not in filenames:
            continue
        yield Path(dirpath) / "SKILL.md"


def resolve_skills_dir(root: Path) -> Path:
    if (root / "skills").is_dir():
        return root / "skills"
    if root.name == "skills" and root.is_dir():
        return root
    raise SystemExit(f"No skills/ directory under {root}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Soften coercive SKILL.md catalog descriptions."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print paths that would change without writing.",
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=str(DEFAULT_ROOT),
        help="Vault root (contains skills/) or a skills/ directory.",
    )
    args = parser.parse_args(argv)
    skills_dir = resolve_skills_dir(Path(args.root).resolve())
    changed = 0
    for skill_file in sorted(iter_skill_files(skills_dir)):
        if process_file(skill_file, args.dry_run):
            changed += 1
    noun = "description" if changed == 1 else "descriptions"
    verb = "would soften" if args.dry_run else "softened"
    print(f"{verb} {changed} skill {noun}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
PY
