#!/usr/bin/env python3
"""Report lock entries and imported profiles that upstream has moved past.

`update-skills.yml` exits 0 whether or not `skills update` actually pulled
anything, so a source can sit frozen for months while the daily run stays green
(issue #786: four sources had a single `updatedAt` equal to their `installedAt`).
This compares the vault's recorded provenance against the upstream repository
itself, which is the check that surfaced that.

Two provenance kinds, two checks:

* `.skill-lock.json` — for each entry, look up `skillPath`'s folder in the
  source repo's git tree and compare its sha to `skillFolderHash`.
  - **behind**: the folder exists upstream and its sha differs. The vault's copy
    is stale; the sync should have pulled it and did not.
  - **unreachable**: the recorded folder no longer exists upstream (renamed,
    moved, or deleted). `skills update` classifies these as "deleted upstream"
    and skips them, so they can *never* update until `skillPath` is repointed.
* `metadata.source-repo` frontmatter — the expert profiles imported by
  `import-scientific-agents.py` are outside the lock entirely. Compare each
  pinned `source-commit` against the source repo's current HEAD.

Reads only public GitHub APIs. `GITHUB_TOKEN` / `GH_TOKEN` is used to raise the
rate limit.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOCK_PATH = ROOT / ".skill-lock.json"
API = "https://api.github.com"
TIMEOUT = 30


def api_get(path: str):
    request = urllib.request.Request(
        f"{API}{path}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "skillquarium-drift"},
    )
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            return json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def repo_tree(source: str):
    """Recursive git tree, trying the same refs the skills CLI tries."""
    for ref in ("HEAD", "main", "master"):
        data = api_get(f"/repos/{source}/git/trees/{ref}?recursive=1")
        if data and data.get("tree"):
            return data
    return None


def folder_of(skill_path: str) -> str:
    normalized = skill_path.replace("\\", "/").rstrip("/")
    if normalized.lower().endswith("/skill.md"):
        return normalized[: -len("/SKILL.md")]
    return normalized


def check_lock(lock_path: Path) -> tuple[dict, list[str]]:
    with lock_path.open(encoding="utf-8") as f:
        skills = json.load(f).get("skills", {})
    by_source = collections.defaultdict(list)
    for name, entry in skills.items():
        by_source[entry.get("source")].append((name, entry))

    report, errors = {}, []
    for source, items in sorted(by_source.items(), key=lambda pair: -len(pair[1])):
        if not source:
            continue
        tree = repo_tree(source)
        if tree is None:
            errors.append(f"{source}: could not read the upstream git tree")
            continue
        if tree.get("truncated"):
            errors.append(f"{source}: upstream git tree was truncated; counts are partial")
        shas = {e["path"]: e["sha"] for e in tree["tree"] if e["type"] == "tree"}
        buckets = {"current": [], "behind": [], "unreachable": []}
        for name, entry in sorted(items):
            path = entry.get("skillPath")
            if not path:
                continue
            sha = shas.get(folder_of(path))
            if sha is None:
                buckets["unreachable"].append(name)
            elif sha != entry.get("skillFolderHash"):
                buckets["behind"].append(name)
            else:
                buckets["current"].append(name)
        report[source] = buckets
    return report, errors


def pinned_profiles(root: Path) -> dict:
    """Skills whose provenance lives in frontmatter instead of the lock."""
    by_repo = collections.defaultdict(collections.Counter)
    for skill_md in sorted(root.glob("skills/*/SKILL.md")):
        repo = commit = None
        with skill_md.open(encoding="utf-8") as f:
            for index, line in enumerate(f):
                if index > 40:
                    break
                stripped = line.strip()
                if stripped.startswith("source-repo:"):
                    repo = stripped.split(":", 1)[1].strip()
                elif stripped.startswith("source-commit:"):
                    commit = stripped.split(":", 1)[1].strip()
        if repo and commit:
            by_repo[repo][commit] += 1
    return by_repo


def check_profiles(root: Path) -> list[tuple[str, list[tuple[str, int]], str | None]]:
    rows = []
    for repo, commits in sorted(pinned_profiles(root).items()):
        head = api_get(f"/repos/{repo}/commits?per_page=1")
        head_sha = head[0]["sha"] if head else None
        rows.append((repo, sorted(commits.items()), head_sha))
    return rows


def render(report: dict, errors: list, profiles: list) -> tuple[str, int]:
    lines = ["| source | tracked | current | behind | unreachable |",
             "| --- | --- | --- | --- | --- |"]
    behind = unreachable = 0
    for source, buckets in report.items():
        total = sum(len(v) for v in buckets.values())
        behind += len(buckets["behind"])
        unreachable += len(buckets["unreachable"])
        lines.append(f"| `{source}` | {total} | {len(buckets['current'])} | "
                     f"{len(buckets['behind'])} | {len(buckets['unreachable'])} |")
    lines.append("")
    lines.append(f"**{behind} behind upstream, {unreachable} unreachable** "
                 f"(recorded `skillPath` no longer exists upstream, so "
                 f"`skills update` skips them permanently).")

    stale_profiles = 0
    if profiles:
        lines += ["", "Imported profiles pinned in frontmatter (outside the lock):", ""]
        for repo, commits, head_sha in profiles:
            for commit, count in commits:
                current = commit == head_sha
                if not current:
                    stale_profiles += count
                state = "current" if current else f"behind HEAD `{(head_sha or '?')[:12]}`"
                lines.append(f"- `{repo}` — {count} skills pinned at "
                             f"`{commit[:12]}`, {state}")

    if errors:
        lines += ["", "Errors:", ""] + [f"- {e}" for e in errors]

    return "\n".join(lines), behind + unreachable + stale_profiles


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--lock", type=Path, default=LOCK_PATH)
    parser.add_argument("--skip-profiles", action="store_true")
    parser.add_argument("--fail-on-drift", action="store_true",
                        help="Exit 1 when anything is behind or unreachable")
    args = parser.parse_args()

    report, errors = check_lock(args.lock)
    profiles = [] if args.skip_profiles else check_profiles(args.root.resolve())
    text, drift = render(report, errors, profiles)
    print(text)

    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("## Upstream drift\n\n" + text + "\n")

    if errors and args.fail_on_drift:
        return 1
    return 1 if drift and args.fail_on_drift else 0


if __name__ == "__main__":
    sys.exit(main())
