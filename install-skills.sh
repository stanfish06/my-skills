#!/usr/bin/env bash
set -euo pipefail

# This script lives at ~/.agents/install-skills.sh. The vault root is the repo
# root; the skill folders themselves live in the flat ~/.agents/skills/ subtree,
# which is also the skills CLI's canonical global store.
VAULT_DIR="$(cd "$(dirname "$0")" && pwd -P)"

# Relative paths below (`npx skills add .`, `git restore .`, the gstack cleanup
# finds) must resolve against the vault, not the caller's cwd. dot-agents'
# scripts/install.sh invokes this from the repo root, where `git restore .`
# would discard that repo's uncommitted changes.
cd "$VAULT_DIR"

# Optional extras are OFF by default. Enable with:
#   ./install-skills.sh --extras gstack
#   ./install-skills.sh --extras career
#   ./install-skills.sh --extras ui-ux
#   ./install-skills.sh --extras gstack career ui-ux
#   ./install-skills.sh --extras all
EXTRA_GSTACK=0
EXTRA_CAREER=0
EXTRA_UI_UX=0

usage() {
  cat <<'EOF'
Usage: install-skills.sh [options]

Symlink vault skills into each agent, install graphify, and optionally
install heavier extras that are skipped by default.

Options:
  --extras <name>...   Install optional extras (default: none).
                       Names: gstack, career, ui-ux, all
                       Aliases: career-ops, ui-ux-pro-max, uipro
  --extras=<csv>       Comma-separated form (e.g. --extras=gstack,ui-ux)
  -h, --help           Show this help

Examples:
  ./install-skills.sh
  ./install-skills.sh --extras gstack
  ./install-skills.sh --extras career
  ./install-skills.sh --extras ui-ux
  ./install-skills.sh --extras gstack career ui-ux
  ./install-skills.sh --extras all

Environment:
  SKILLS_CLI_VERSION=<ver>   pin the skills CLI version (default: 1.5.20)

Environment (honored when the matching extra is enabled):
  GSTACK_SKIP=1              force-skip gstack even with --extras gstack
  GSTACK_SKIP_BUN=1          skip bun install (browser skills disabled)
  GSTACK_REF=<ref>           pin gstack to a git ref
  CAREER_OPS_SKIP=1          force-skip career-ops even with --extras career
  CAREER_OPS_DIR=<path>      career-ops workspace location (default: ~/career-ops)
  CAREER_OPS_AUTO_UPDATE=0   freeze an existing career-ops checkout
  UI_UX_PRO_MAX_SKIP=1       force-skip UI/UX Pro Max even with --extras ui-ux
  UI_UX_PRO_MAX_CLI_VERSION=<ver>
                             pin its CLI version (default: 2.14.1)
EOF
}

enable_extra() {
  local name="${1//[[:space:]]/}"
  if [ -z "$name" ]; then
    return 0
  fi
  case "$name" in
    gstack)
      EXTRA_GSTACK=1
      ;;
    career|career-ops)
      EXTRA_CAREER=1
      ;;
    ui-ux|ui-ux-pro-max|uipro)
      EXTRA_UI_UX=1
      ;;
    all)
      EXTRA_GSTACK=1
      EXTRA_CAREER=1
      EXTRA_UI_UX=1
      ;;
    *)
      echo "ERROR: unknown extra '$name' (expected: gstack, career, ui-ux, all)" >&2
      exit 1
      ;;
  esac
}

enable_extras_csv() {
  local csv="$1"
  local part
  # Accept comma- and/or space-separated lists.
  csv="${csv//,/ }"
  # shellcheck disable=SC2086
  for part in $csv; do
    enable_extra "$part"
  done
}

while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --extras)
      shift
      if [ $# -eq 0 ] || [[ "$1" == -* ]]; then
        echo "ERROR: --extras requires at least one name (gstack, career, ui-ux, all)" >&2
        exit 1
      fi
      while [ $# -gt 0 ] && [[ "$1" != -* ]]; do
        enable_extras_csv "$1"
        shift
      done
      ;;
    --extras=*)
      value="${1#--extras=}"
      if [ -z "$value" ]; then
        echo "ERROR: --extras= requires at least one name (gstack, career, ui-ux, all)" >&2
        exit 1
      fi
      enable_extras_csv "$value"
      shift
      ;;
    *)
      echo "ERROR: unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

source "$VAULT_DIR/.skill-vault/install-career-ops.sh"
source "$VAULT_DIR/.skill-vault/install-ui-ux-pro-max.sh"

# Temporarily move gstack/ out of the vault so `npx skills add` doesn't
# scan it and leak per-skill symlinks to the vault root. gstack is a
# bundled collection (250MB, own .git) installed by the optional block
# below when --extras gstack is passed, not a set of individual
# vercel-CLI skills.
GSTACK_DIR="$VAULT_DIR/skills/gstack"
GSTACK_STASH=""
BUN_INSTALLER=""

# Idempotent: safe to call on the normal path and again from the EXIT trap.
restore_gstack() {
  [ -n "$GSTACK_STASH" ] || return 0

  if [ -d "$GSTACK_STASH/gstack" ] && [ ! -e "$GSTACK_DIR" ]; then
    mv "$GSTACK_STASH/gstack" "$GSTACK_DIR"
  fi
  rmdir "$GSTACK_STASH" 2>/dev/null || true
  GSTACK_STASH=""
}

# A failed or interrupted run must not leave gstack (250MB, own .git) stranded
# in a temp dir with the vault missing it.
cleanup() {
  local status=$?

  if [ -n "$BUN_INSTALLER" ]; then
    rm -f "$BUN_INSTALLER"
    BUN_INSTALLER=""
  fi
  restore_gstack

  return "$status"
}

# Signal handlers exit so the EXIT trap does the cleanup exactly once.
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' HUP TERM

if [ -d "$GSTACK_DIR/.git" ]; then
  GSTACK_STASH="$(mktemp -d -t gstack-stash.XXXXXX)"
  mv "$GSTACK_DIR" "$GSTACK_STASH/gstack"
fi

if [ "$EXTRA_UI_UX" -eq 1 ]; then
  install_ui_ux_pro_max
else
  echo "ui-ux-pro-max: skipped (pass --extras ui-ux to install)"
fi

# `npx -y` is required: bare `npx` blocks on npm's "Ok to proceed? (y)" prompt
# whenever this version isn't already in the npx cache (fresh machine, cleaned
# cache, or a newly published release). Pinned so an upstream publish can't
# change what gets installed; override with SKILLS_CLI_VERSION=<version>.
SKILLS_CLI_VERSION="${SKILLS_CLI_VERSION:-1.5.20}"
npx -y "skills@$SKILLS_CLI_VERSION" add . -s '*' -g
git restore .

# Some skills-cli hosts create project-style link roots inside the vault even
# for a global install. They are generated artifacts, not source, and Pi
# would rediscover them as project skills when run from this directory.
# `skills/` is scanned as a deep container (maxDepth 3), so a stale link root
# left inside it would be rediscovered as real skills on the next run. Purge
# both roots.
for agent_root in .agents .pi agent; do
  rm -rf -- "$agent_root" "skills/$agent_root"
done

restore_gstack

# Clean up any stray gstack artifacts that gstack's own ./setup may leak
# to the vault root on subsequent runs.
# 1. Remove symlinks whose SKILL.md points into gstack/
find skills -maxdepth 2 -name SKILL.md -type l -lname '*gstack*' -exec sh -c '
  dir=$(dirname "$1"); rm -rf "$dir"
' _ {} \; 2>/dev/null || true
# 2. Remove gstack-prefixed directories created by gstack ./setup --prefix
find skills -maxdepth 1 -name 'gstack-*' -not -name 'gstack-*.md' -exec rm -rf {} \; 2>/dev/null || true

if [ "$EXTRA_CAREER" -eq 1 ]; then
  install_career_ops
else
  echo "career-ops: skipped (pass --extras career to install)"
fi

# ─── gstack (Garry Tan's AI engineering workflow) ───────────────
# Optional via: ./install-skills.sh --extras gstack
#
# gstack is a bundled skill collection — 23 specialist slash commands
# + 8 power tools that turn Claude Code into a virtual engineering team
# (CEO, eng manager, designer, reviewer, QA, security, release eng).
#
# It can't be split into per-skill folders because sub-skills share
# lib/, bin/, browse/ runtime code. Install it as a single bundle via
# its own ./setup script, which auto-detects installed agents (Claude
# Code, Codex, Kiro, Factory, OpenCode) and symlinks the whole
# gstack/ folder into each agent's skills/ directory.
#
# Uses --prefix mode (/gstack-qa, /gstack-ship) to avoid clobbering this
# vault's existing /qa, /review, /ship, /spec, /health, /learn skills.
#
# Source: https://github.com/garrytan/gstack  ·  License: MIT
#
# Env flags (when --extras gstack is enabled):
#   GSTACK_SKIP=1         — force-skip gstack
#   GSTACK_SKIP_BUN=1     — skip bun install (browser skills disabled;
#                           methodology skills still work via manual symlink)
#   GSTACK_REF=<ref>      — pin to a git ref (commit hash or tag). Defaults
#                           to a pinned commit below for reproducibility.
#                           Override to track main: GSTACK_REF=main
GSTACK_REPO="https://github.com/garrytan/gstack.git"
# Pinned to a known-good commit (VERSION 1.58.4.0). Bump deliberately.
# Verify with: git -C gstack log -1 --format='%H %s' 9fd03fa
GSTACK_DEFAULT_REF="9fd03fae9e74f5daa7a138366aca8f86c7367c5c"
GSTACK_REF="${GSTACK_REF:-$GSTACK_DEFAULT_REF}"

install_gstack() {
  if [ -n "${GSTACK_SKIP:-}" ]; then
    echo "gstack: skipped (GSTACK_SKIP=1)"
    return 0
  fi

  # Clone or update — pinned to GSTACK_REF for reproducibility and
  # supply-chain safety. Override with GSTACK_REF=<ref> (e.g. main) to
  # track upstream.
  if [ -d "$GSTACK_DIR/.git" ]; then
    echo "gstack: updating to ref $GSTACK_REF..."
    git -C "$GSTACK_DIR" fetch --depth 1 origin "$GSTACK_REF" 2>/dev/null || true
    git -C "$GSTACK_DIR" checkout --detach "$GSTACK_REF" 2>/dev/null || \
      git -C "$GSTACK_DIR" checkout --detach FETCH_HEAD 2>/dev/null || true
  else
    echo "gstack: cloning (ref $GSTACK_REF)..."
    rm -rf "$GSTACK_DIR"
    git clone --no-checkout --depth 1 "$GSTACK_REPO" "$GSTACK_DIR" 2>/dev/null
    git -C "$GSTACK_DIR" fetch --depth 1 origin "$GSTACK_REF"
    git -C "$GSTACK_DIR" checkout --detach FETCH_HEAD
  fi

  if [ ! -x "$GSTACK_DIR/setup" ]; then
    echo "ERROR: gstack setup script not found at $GSTACK_DIR/setup" >&2
    return 1
  fi

  # gstack's ./setup requires bun to build the browse binary and install
  # playwright. Install bun if missing so the full toolkit works (/browse,
  # /qa, /design-shotgun, /make-pdf, /diagram). Skip with GSTACK_SKIP_BUN=1.
  bun_available=0
  if [ -z "${GSTACK_SKIP_BUN:-}" ] && ! command -v bun >/dev/null 2>&1; then
    echo "gstack: installing bun (required for browser skills)..."
    if command -v curl >/dev/null 2>&1; then
      # Download with TLS + retries, then execute (not piped directly) so
      # a network hiccup can't truncate the script mid-stream.
      # Tracked in BUN_INSTALLER so the single EXIT trap cleans it up; a local
      # `trap ... EXIT` here would clobber that trap and strand gstack.
      BUN_INSTALLER="$(mktemp)"
      if curl --proto '=https' --tlsv1.2 --fail --location --retry 3 \
              --connect-timeout 10 -o "$BUN_INSTALLER" \
              https://bun.sh/install 2>/dev/null && \
         bash "$BUN_INSTALLER" 2>/dev/null; then
        bun_available=1
        export BUN_INSTALL="$HOME/.bun"
        export PATH="$BUN_INSTALL/bin:$PATH"
      else
        echo "WARNING: bun install failed — falling back to symlink-only mode." >&2
        echo "  Browser skills disabled; methodology skills still work." >&2
        echo "  Install bun manually from https://bun.sh for full gstack." >&2
      fi
      rm -f "$BUN_INSTALLER"
      BUN_INSTALLER=""
    else
      echo "WARNING: curl not found, cannot install bun — falling back to symlink-only mode." >&2
    fi
  elif command -v bun >/dev/null 2>&1; then
    bun_available=1
  fi

  # Run gstack's own installer — auto-detects agents, symlinks the bundle
  # into each, builds the browse binary, installs playwright browsers.
  # --prefix  → namespaced skill names (/gstack-qa, /gstack-ship) to avoid
  #             clobbering this vault's existing /qa, /review, /ship skills.
  # --quiet   → suppress non-essential log output.
  # gstack's setup supports: Claude, Codex, Kiro, Factory, OpenCode (auto).
  # Cursor is NOT supported by gstack upstream — only Claude gets the
  # fallback symlink below.
  if [ "$bun_available" -eq 1 ]; then
    echo "gstack: running ./setup --host auto --prefix --quiet..."
    (cd "$GSTACK_DIR" && ./setup --host auto --prefix --quiet)
  else
    # Fallback: bun not available — manually symlink the bundle to Claude
    # Code only. gstack's ./setup generates host-specific skill docs for
    # Codex/OpenCode/Factory/Kiro; symlinking the raw repo there would
    # expose Claude-oriented SKILL.md paths that don't work for those
    # agents. Browser skills don't work without bun, but methodology
    # skills (/gstack-office-hours, /gstack-plan-ceo-review, /gstack-review,
    # /gstack-cso, /gstack-spec, /gstack-retro, /gstack-autoplan,
    # /gstack-careful, /gstack-freeze, /gstack-ship, /gstack-investigate) will.
    echo "gstack: bun not available — Claude-only symlink fallback..."
    claude_skills="$HOME/.claude/skills"
    if [ -d "$(dirname "$claude_skills")" ] || [ -L "$(dirname "$claude_skills")" ]; then
      mkdir -p "$claude_skills"
      ln -snf "$GSTACK_DIR" "$claude_skills/gstack"
      echo "  linked $claude_skills/gstack"
    fi
  fi

  echo "gstack: done. Skills: /gstack-office-hours /gstack-plan-ceo-review /gstack-review /gstack-qa /gstack-ship /gstack-cso /gstack-autoplan /gstack-spec /gstack-retro ..."
}

if [ "$EXTRA_GSTACK" -eq 1 ]; then
  install_gstack
else
  echo "gstack: skipped (pass --extras gstack to install)"
fi

find_graphify() {
  if command -v graphify >/dev/null 2>&1; then
    command -v graphify
    return 0
  fi

  if command -v uv >/dev/null 2>&1; then
    uv_bin_dir=$(uv tool dir --bin 2>/dev/null || true)
    if [ -n "$uv_bin_dir" ] && [ -x "$uv_bin_dir/graphify" ]; then
      printf '%s\n' "$uv_bin_dir/graphify"
      return 0
    fi
  fi

  if command -v pipx >/dev/null 2>&1; then
    pipx_bin_dir=$(pipx environment --value PIPX_BIN_DIR 2>/dev/null || true)
    if [ -n "$pipx_bin_dir" ] && [ -x "$pipx_bin_dir/graphify" ]; then
      printf '%s\n' "$pipx_bin_dir/graphify"
      return 0
    fi
  fi

  return 1
}

install_graphify() {
  if command -v uv >/dev/null 2>&1; then
    uv tool install graphifyy
  elif command -v pipx >/dev/null 2>&1; then
    pipx install graphifyy
  elif command -v pip >/dev/null 2>&1; then
    if ! pip install graphifyy; then
      echo "ERROR: pip install graphifyy failed; install uv/pipx or use a virtualenv. Refusing to retry with --break-system-packages." >&2
      return 1
    fi
  else
    echo "ERROR: graphify is missing and no supported installer was found (uv, pipx, or pip)." >&2
    return 1
  fi
}

# graphify is a separate Python CLI + assistant skill (not managed by the skills
# CLI), so it needs its own installer. PyPI package is `graphifyy` (double-y); the
# CLI command is `graphify`. See: github.com/safishamsi/graphify
graphify_cmd=$(find_graphify || true)
if [ -z "$graphify_cmd" ]; then
  install_graphify
  graphify_cmd=$(find_graphify || true)
fi

if [ -z "$graphify_cmd" ]; then
  echo "ERROR: graphify installed, but the graphify executable was not found. Add the tool bin directory to PATH and retry." >&2
  exit 1
fi

# Register the graphify skill with your assistant. No args auto-detects the
# current platform (writes e.g. ~/.claude/skills/graphify/). Add more as needed:
#   graphify install --platform codex
#   graphify install --platform cursor
"$graphify_cmd" install
