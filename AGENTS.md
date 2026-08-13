# AGENTS.md — operating guide for agents

You have access to a curated library of **1,800+ agent skills** at `~/.agents/skills/`
(the `skills/` subtree of this repo, which is rooted at `~/.agents`). A *skill* is a folder with a `SKILL.md` holding battle-tested instructions for
a specific tool, library, or workflow. **Using a relevant skill is faster and more reliable
than improvising.** This file tells you how to find and use them.

### How skills reach you vs. what this vault is for

- **Loading is your agent's job.** Most agents surface skills through their own native
  mechanism (e.g. Claude Code loads every skill's name + description into context and matches
  on it). You usually don't need to look anywhere to *know a skill exists* — it's already
  available to invoke.
- **`install-skills.sh` wires them in.** The script (`npx skills add . -s '*' -g`) symlinks
  every skill in this repo into each agent's own skills folder, so your native loader picks
  them up. The skill folders here are the single source of truth.
- **This vault is the query layer.** `~/.agents/` adds an Obsidian navigation layer on
  top of the raw skills — wrapper notes, per-domain maps, an index, a filterable table,
  aliases, tags, and an optional `graphify-out/` knowledge graph. Reach for it when you
  want **comprehensive discovery** beyond your agent's built-in matching: searching by
  concept/synonym, browsing a whole domain, or querying relationships with `graphify`,
  `obsidian-cli`, or `rg`. For a quick single-skill match, your native mechanism is enough;
  for "what do we have across X?", query the vault.

---

## The two things to do before every task

1. **Look for a skill first.** Before writing code or running commands, check whether a
   skill already covers the task (see *Finding a skill* below). If one exists, read its
   `SKILL.md` and follow it — do not reinvent it from memory.
2. **Establish context before editing.** Don't code against a dependency, framework, or
   unfamiliar repo from assumptions. Pull the **real source** with `opensrc` and/or build a
   queryable map with `graphify`, then work from what's actually there (see *Establishing
   context*).

These two steps are cheap and prevent most wasted work. Do them at the start of a task and
again whenever you hit something unfamiliar.

---

## Finding a skill

Try these in order; stop when you have a match.

1. **Use what's already loaded.** Your agent's native skill mechanism has every installed
   skill's name + description available — match the task to one and invoke it (Skill tool /
   `/name`). This covers most cases. The skill's full instructions live at
   `~/.agents/skills/<name>/SKILL.md`.

2. **Query the vault for comprehensive discovery** (headless, ranked) — when native matching
   isn't enough, or you want everything related to a concept:
   ```bash
   cd ~/.agents
   graphify query "Which skills cover single-cell batch correction?" --graph graphify-out/graph.json --budget 1500
   obsidian-cli search query="single cell batch correction" limit=8
   # zero-dependency fallback (works anywhere ripgrep is installed):
   rg -li "batch correction|integration|harmony" ~/.agents/*.md
   ```
   The `*.md` files under `vault/notes/<domain>/` are one-line "wrapper" notes (description + domain +
   aliases) — the fast index. Read the underlying `<name>/SKILL.md` once you've picked one.

3. **Browse by domain.** [`vault/index.md`](vault/index.md) groups all skills into
   30-odd domains; [`vault/maps/`](vault/maps) has one note per domain and
   [`vault/notes/<domain>/`](vault/notes) holds the wrapper notes themselves;
   [`vault/skills.base`](vault/skills.base) is a filterable table. Coding work lives
   mostly in [`vault/maps/software-dev.md`](vault/maps/software-dev.md),
   [`vault/maps/cloud-devops.md`](vault/maps/cloud-devops.md), and
   [`vault/maps/security-auditing.md`](vault/maps/security-auditing.md).

4. **Not in the vault?** Search the open ecosystem with the `find-skills` skill or
   `npx skills find "<query>"`, then install with `npx skills add <owner/repo> -s <skill>`.

If nothing fits, proceed unaided — but say so, and consider whether the work is worth
capturing as a new skill (`skill-builder` / `writing-skills`).

---

## Establishing context

- **Read a dependency's real code** instead of guessing its API or behavior:
  ```bash
  rg "createServer" $(opensrc path express)        # npm
  cat $(opensrc path pypi:fastapi)/fastapi/routing.py   # PyPI; also crates:, owner/repo
  ```
  Pin a version with `pkg@1.2.3` when it must match what's installed. See
  [`skills/opensrc/SKILL.md`](skills/opensrc/SKILL.md).
- **Understand an unfamiliar codebase or doc set** by turning it into a knowledge graph with
  `graphify`, then query it.
- **For this skills vault itself, query the local graph when present**:
  ```bash
  cd ~/.agents
  graphify query "How is the skill library organized?" --graph graphify-out/graph.json
  ```
  If the graph is missing or stale, rebuild it manually with
  `python3 .skill-vault/build-graphify.py`. This is separate from `build.py` because graph
  extraction can be LLM-backed and heavier than CI should run.
- **Always read the chosen skill's full `SKILL.md`** before acting — the wrapper note is only
  a summary.

---

## Most important skills for coding tasks

Know these by name so you reach for them automatically.

**Context & grounding**
- `opensrc` — read the actual source of any npm/PyPI/crate/GitHub dependency.
- `graphify` — turn a codebase/docs into a queryable knowledge graph (global skill, not in
  this vault).
- `gh-cli` — authenticated GitHub access (PRs, issues, raw files) over ad-hoc curl.
- `find-skills` — discover & install skills you don't have yet.

**Plan & methodology** (the Superpowers suite — use proactively, not just on request)
- `brainstorming` — before any feature/component/behavior change, to pin down intent.
- `writing-plans` → `executing-plans` — turn a spec into a reviewed, checkpointed plan.
- `test-driven-development` — write the failing test first; let it drive the code.
- `systematic-debugging` — for any bug, test failure, or surprise, before proposing a fix.
- `verification-before-completion` — run the checks and show evidence before claiming done.
- `using-git-worktrees` — isolate feature work from the current workspace.
- `requesting-code-review` / `receiving-code-review` — review discipline, both directions.
- `subagent-driven-development` / `dispatching-parallel-agents` — split independent work.

**Build, test & ship**
- `modern-python` — project setup with uv/ruff/ty (pure-Python).
- `conda-bioconda` — reproducible Conda/Bioconda environments (compiled / bio tools).
- `pytest` — Python testing (fixtures, parametrize, coverage).
- `docker` — Dockerfiles, multi-stage builds, compose.
- `fastapi` — Python HTTP/JSON APIs.
- `github-actions-ci` — CI/CD workflows.

**Review, PR & security**
- `check-pr` — resolve unresolved comments / failing checks / weak descriptions on a PR.
- `greploop` — iterate a PR through Greptile review until it's clean.
- `semgrep`, `codeql` — static analysis for bugs and vulnerabilities.
- `agentic-actions-auditor` — audit CI workflows that invoke AI agents for injection risks.

**Authoring skills**
- `skill-builder` / `writing-skills` — when creating or editing a skill.

**Office files**
- For any Word (`.docx`), Excel (`.xlsx`/`.csv`), or PowerPoint (`.pptx`) task,
  invoke `officecli-docx`, `officecli-xlsx`, or `officecli-pptx` before acting;
  use `officecli` for general or cross-format work.
- Also load the matching specialized skill when applicable:
  `officecli-academic-paper`, `officecli-data-dashboard`,
  `officecli-financial-model`, `officecli-pitch-deck`,
  `officecli-word-form`, `morph-ppt`, or `morph-ppt-3d`. Read inherited base
  skills when the scene-layer skill requires them.
- Follow the OfficeCLI skill's help-first and delivery/visual-validation rules;
  run `officecli help` rather than guessing command syntax or properties.

---

## Default loop for a coding task

1. **Skill check** — is there a skill for this? If yes, read its `SKILL.md` and follow it.
2. **Context** — `opensrc`/`graphify` the relevant dependency or codebase; read real code.
3. **Plan** — for anything multi-step, `brainstorming` → `writing-plans`.
4. **Implement** — `test-driven-development`; isolate with `using-git-worktrees` if risky.
5. **Verify** — `verification-before-completion`: run tests/lint, show the output.
6. **Review** — `requesting-code-review`, or `check-pr`/`greploop` on the PR.

---

## Maintaining this library

- Skills are managed by the Vercel `skills` CLI; folders live in `skills/` and are never
  hand-edited by the navigation layer.
- Run [`install-skills.sh`](install-skills.sh) to symlink every skill here into each agent's
  skills folder so their native loaders pick them up. gstack, career-ops, and UI/UX Pro Max
  are optional extras: pass `--extras gstack`, `--extras career`, `--extras ui-ux`, or
  `--extras all` to install them (skipped by default).
- After adding/removing a skill, regenerate wrappers/maps/index:
  `python3 .skill-vault/build.py` (see [`README.md`](README.md)).
- To refresh the optional local graphify graph for vault queries, run
  `python3 .skill-vault/build-graphify.py`. Use `--dry-run` to inspect the command and
  `--full` only when you intentionally want every skill folder included.
- This `AGENTS.md` is the canonical guide; symlink or copy it to wherever each tool looks
  (e.g. a project root, or alongside your tool's global instructions).
