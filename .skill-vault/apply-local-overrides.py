#!/usr/bin/env python3
"""Re-apply the vault's local fixes to upstream-managed skills.

`skills update` reinstalls every github-sourced skill whose upstream folder hash
changed, overwriting fixes merged here. That already happened once: PR #302 fixed
`docker-expert`, and the next scheduled sync restored both defects with no
failure and no conflict (issue #665).

Each local fix is recorded in `local-overrides.json` as a find/replace pair and
re-applied after every pull, the same post-update re-application that
`soften_skill_description.sh` does for descriptions and that
`scientific-agent-patches.json` does for imported expert profiles.

An override whose `find` and `replace` are both absent is *stale*: upstream
rewrote that region, so the fix has to be re-derived. Stale overrides are
reported as errors rather than skipped, so a fix cannot disappear silently
a second time.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OVERRIDES_PATH = Path(__file__).resolve().parent / "local-overrides.json"


def load_overrides(path: Path | None = None) -> dict:
    path = path or OVERRIDES_PATH
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("local overrides file must be an object keyed by skill name")
    for skill, entries in data.items():
        if not isinstance(entries, list):
            raise ValueError(f"{skill}: overrides must be a list")
        for entry in entries:
            missing = {"id", "find", "replace"} - set(entry)
            if missing:
                raise ValueError(f"{skill}: override missing {sorted(missing)}")
            if entry["find"] == entry["replace"]:
                raise ValueError(f"{skill}/{entry['id']}: find and replace are identical")
    return data


def override_state(text: str, entry: dict) -> str:
    """One of "pending" (defect present), "applied", or "stale" (neither)."""
    if entry["find"] in text:
        return "pending"
    if entry["replace"] in text:
        return "applied"
    return "stale"


def apply_overrides(overrides: dict, root: Path, *, write: bool = True) -> dict:
    result: dict[str, list[str]] = {"pending": [], "applied": [], "stale": [], "missing": []}
    for skill, entries in sorted(overrides.items()):
        for entry in entries:
            relative = f"skills/{skill}/{entry.get('file', 'SKILL.md')}"
            path = root / relative
            label = f"{skill}/{entry['id']}"
            if not path.is_file():
                result["missing"].append(f"{label} ({relative})")
                continue
            text = path.read_text(encoding="utf-8")
            state = override_state(text, entry)
            if state == "pending":
                if write:
                    path.write_text(text.replace(entry["find"], entry["replace"]),
                                    encoding="utf-8")
                result["pending"].append(label)
            else:
                result[state].append(label)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT, help="Skills vault root")
    parser.add_argument("--overrides", type=Path, default=OVERRIDES_PATH)
    parser.add_argument("--check", action="store_true",
                        help="Report without writing; fail if any override is not applied")
    args = parser.parse_args()

    overrides = load_overrides(args.overrides)
    result = apply_overrides(overrides, args.root.resolve(), write=not args.check)

    total = sum(len(v) for v in result.values())
    verb = "would re-apply" if args.check else "re-applied"
    print(f"local overrides: {total} recorded, {len(result['applied'])} already applied, "
          f"{len(result['pending'])} {verb}")
    for label in result["pending"]:
        print(f"  {'stale in tree' if args.check else 're-applied'}: {label}")
    for label in result["stale"]:
        print(f"  STALE: {label} — upstream rewrote this region; re-derive the fix",
              file=sys.stderr)
    for label in result["missing"]:
        print(f"  MISSING: {label}", file=sys.stderr)

    if result["stale"] or result["missing"]:
        return 1
    return 1 if args.check and result["pending"] else 0


if __name__ == "__main__":
    sys.exit(main())
