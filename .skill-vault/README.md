# .skill-vault — how this repo stays navigable

This repo is rooted at `~/.agents`, which is also the Vercel skills CLI's home
directory. That means `skills/` is the CLI's flat canonical store and must stay
a flat list of skill folders — categorising it into subdirectories would make
the CLI copy every skill back out to a flat path on the next install. The
navigation layer is therefore what gets structured, not the skill tree.

This repo is two layers over the same folders:

- **Agent layer** — each `skills/<skill>/SKILL.md` is the real, executable skill. These
  are managed by the [Vercel skills CLI](https://github.com/vercel-labs/skills)
  (`npx skills`). Navigation tooling never edits them; `skill-toggle` changes only
  their explicit Claude Code/Codex invocation fields at the user's request.
- **Human layer** — generated for Obsidian / Neovim navigation, all under `vault/`:
  - `vault/notes/<domain>/<skill>.md` — a wrapper note per skill, grouped by
    domain (your *Personal notes* section and your `status` / `rating` /
    `aliases` frontmatter edits survive every rebuild)
  - `vault/maps/<domain>.md` — one map (MOC) per domain
  - `vault/index.md` — the master A–Z + by-domain index
  - `vault/skills.base` — the filterable table
  - `vault/recipes/` — hand-written, goal-oriented workflows

  Generated links are emitted as true relative paths, so they resolve in
  Obsidian and in any plain markdown renderer. `build.py` is the only writer of
  everything above except `recipes/`.

This directory holds the machinery that keeps the human layer in sync.

## Files

| File | Purpose |
|------|---------|
| `build.py` | Regenerates the human layer from the `SKILL.md` files. Idempotent; preserves hand edits. Run: `python3 .skill-vault/build.py` |
| `build-graphify.py` | Rebuilds the optional local Graphify graph in `graphify-out/`. Manual only; can run LLM-backed extraction, so it is deliberately separate from CI's lightweight `build.py`. Run: `python3 .skill-vault/build-graphify.py` |
| `apply-local-overrides.py` | Re-applies the fixes in `local-overrides.json` after each upstream pull. Run: `python3 .skill-vault/apply-local-overrides.py [--check]` |
| `local-overrides.json` | The in-vault fixes to upstream-managed skills, as `find`/`replace` pairs keyed by skill name. |
| `skill_toggle.py` | Safe metadata backend for `./skill-toggle`: catalog JSON, product-specific changes, snapshots, reload, and metadata-only Git reset. |
| `tui/` | OpenTUI 0.5.1 application with mouse/keyboard navigation, fuzzy search, status/category filters, and separate Claude Code/Codex controls. |
| *(none)* | The CLI's provenance lock is the tracked `.skill-lock.json` at the repo root, not a copy in here. It records where each skill came from so CI can update them. |

## Scientific expert taxonomy

`.skill-vault/scientific-expert-taxonomy.json` is the authority for assigning
503 catalog profiles to 10 disciplines. The `scientific-agents` dispatcher is
separate and is not one of those 503 profiles. Generated maps, wrapper notes,
and Graphify output are views of the manifest, not classification sources.
Normal builds are deterministic and never classify profiles with heuristics or
an LLM.

When the upstream catalog adds or removes a profile, update the manifest in the
same change. Each profile has one `primary` discipline, may appear under
`secondary` disciplines as cross-disciplinary, and declares `bridge_domains`
that link discipline pages to broader capability maps.

The generated hierarchy starts at
`maps/scientific-expert-profiles.md`, with one page per discipline at
`maps/scientific-expert-profiles/<discipline-id>.md`. Discipline pages list
primary experts first, then cross-disciplinary experts, and expose relevant
capability-map bridges. Build and audit in that order: generated-output audits
expect the maps to be current, so rebuild before running the tests.

```sh
python3 .skill-vault/build.py
python3 -m unittest discover -s .skill-vault/tests -p 'test_*.py' -v
```

The builder validates the manifest against both the catalog and discovered
profile folders before writing any navigation files, so invalid or incomplete
assignments fail without a partial rebuild.

## GitHub Actions

Two workflows in `.github/workflows/` (both share a `vault-write` concurrency
group so they never push at the same time):

1. **`rebuild-index.yml`** — on every push to `master` (and manual dispatch).
   Runs `build.py` and commits the regenerated navigation layer. Fast, no network.
2. **`update-skills.yml`** — daily at 06:17 UTC (and manual dispatch). Runs
   `npx skills update -g -y` to pull the latest version of every skill, rebuilds
   the navigation layer, and commits the result (including the refreshed
   `.skill-lock.json`).

Bot commits use the default `GITHUB_TOKEN`, so they **do not** re-trigger the
workflows (no infinite loop); the `[skip ci]` marker is belt-and-suspenders.

### How CI updates skills in place

The CLI installs global skills into its canonical dir `~/.agents/skills` and
tracks provenance in `~/.agents/.skill-lock.json`. **This repo is laid out as
`~/.agents` itself**, so both are tracked files and CI only has to point the
CLI's home at the checkout:

```sh
rm -rf "$HOME/.agents"
ln -sfn "$GITHUB_WORKSPACE" "$HOME/.agents"   # CLI home -> checkout
npx -y skills@1.5.10 update -g -y             # updates the repo in place (pinned)
```

No snapshot copy in either direction: `$HOME/.agents/skills` resolves to the
tracked `skills/` subtree and `$HOME/.agents/.skill-lock.json` to the tracked
lock at the repo root.

### Source coverage in CI

`skills update` only auto-updates skills whose lock entry is **`sourceType: github`**
(installed via `owner/repo` or an https GitHub URL): it diffs each skill's folder
hash against the GitHub API and reinstalls the ones that changed. Skills installed
from raw `git@github.com:…`/SSH remotes (`sourceType: git`) or local paths are
**not** auto-updated by the CLI — so every skill in this vault is kept as a `github`
source. If you later add a skill from an SSH remote, convert it once with

```sh
npx skills add <owner/repo> -s <skill> -g -y   # re-tracks it as a github source
```

`GITHUB_TOKEN` is only used to raise the API rate limit; all current sources are public.

### Fixing a skill that has a lock entry

`skills update` reinstalls a github-sourced skill whenever its upstream folder
hash changes, so an in-vault fix to one of those skills is overwritten on the
next sync — silently, with no failure and no conflict. That is how PR #302's
`docker-expert` fix was reverted a week after it merged (#665).

Record the fix in `.skill-vault/local-overrides.json` as well as editing the
`SKILL.md`, keyed by skill name:

```json
{
  "docker-expert": [
    { "id": "compose-v2-cli", "issue": 298,
      "source": "sickn33/antigravity-awesome-skills",
      "find": "docker-compose config", "replace": "docker compose config" }
  ]
}
```

`update-skills.yml` runs `apply-local-overrides.py` right after the pull and
before `soften_skill_description.sh`, so the fix goes back on every time. An
override whose `find` *and* `replace` are both gone means upstream rewrote that
region: the run fails and the fix has to be re-derived rather than disappearing.
`test_local_overrides.py` asserts the committed tree already satisfies every
recorded override, so a revert that slips through shows up as a red test.

Use `--check` to verify without writing. Skills with no lock entry are locally
authored — fix those in place, no override needed.

## Keeping the lock fresh

`.skill-lock.json` is the CLI's own file at the repo root, so adding or removing
a skill locally updates it in place — there is no snapshot to sync. Just
regenerate the navigation layer and commit both:

```sh
python3 .skill-vault/build.py        # regenerate nav for the new/removed skills
git add .skill-lock.json skills/     # the lock travels with the skill change
```

## Vendored bundles (no lock entry)

Some upstream collections are **copied in by hand** rather than installed through
the skills CLI, so they have no `.skill-lock.json` entry and the CLI will not
update them. Record each one here and refresh it manually.

| Bundle | Upstream | Vendored at | What we took |
|--------|----------|-------------|--------------|
| MATLAB Agentic Toolkit | [matlab/matlab-agentic-toolkit](https://github.com/matlab/matlab-agentic-toolkit) @ `9556aee` | 2026-07-26 | The 6 base-MATLAB skill groups (30 skills), flattened from `skills-catalog/<group>/<skill>/` to `<skill>/` at the vault root |

Upstream ships 151 skills across 23 groups. We deliberately take only the groups
that need no toolbox licence beyond base MATLAB — `matlab-core`,
`matlab-software-development`, `matlab-app-building`,
`matlab-data-import-and-analysis`, `matlab-external-language-interfaces`,
`matlab-programming` — because `install-skills.sh` installs every vault skill
globally, and MathWorks' own guidance is to load only the groups you use
(agents trigger skills more reliably when fewer are loaded). The toolbox groups
(RF, automotive, radar, wireless, test-and-measurement, …) are intentionally
omitted; add a group only if you start using that toolbox.

To refresh, re-clone upstream and re-copy those group folders over the existing
`matlab-*` directories, keeping the per-skill `LICENSE.md`. The MathWorks licence
permits redistribution in source and binary form **provided the copyright notice,
conditions, and disclaimer are retained** — hence a copy of `LICENSE.md` inside
every vendored skill directory. Do not drop those files. Note that upstream
frontmatter labels these terms `MathWorks BSD-3-Clause`, but the text is *not*
OSI BSD-3-Clause and is not an OSI-approved open-source licence: it is the
BSD-2-Clause body with the non-endorsement clause replaced by a field-of-use
restriction — the software "and all modifications and derivatives … shall be,
licensed to you solely for use in conjunction with MathWorks products and
service offerings." Upstream does not accept pull requests, so local fixes
cannot be sent back; prefer filing an issue there over editing a vendored
`SKILL.md`.

Note that `matlab/` itself is *not* part of this bundle — it is a separate,
independently authored MATLAB/Octave language reference that predates it.

## Optional Graphify graph

For graph-backed local queries over the vault, rebuild `graphify-out/` manually:

```sh
python3 .skill-vault/build-graphify.py
```

By default this builds a lightweight graph over the navigation layer (root wrapper
notes, `maps/`, repo docs, and vault tooling). Use `--full` only when you really
want every skill folder included; that can be much slower and may consume LLM
tokens. Use `--dry-run` to see the exact `graphify` commands without rebuilding.
