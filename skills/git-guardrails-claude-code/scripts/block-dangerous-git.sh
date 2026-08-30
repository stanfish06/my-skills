#!/bin/bash
# PreToolUse hook: exit 2 blocks the tool call, anything else permits it.
# Every path that cannot establish what command it is inspecting exits 2 (fail closed).
set -uo pipefail

if ! command -v jq >/dev/null 2>&1; then
  echo "BLOCKED: git guardrails hook requires jq, which is not on PATH. Install jq or remove the hook." >&2
  exit 2
fi

INPUT=$(cat)
if [ -z "$INPUT" ]; then
  echo "BLOCKED: git guardrails hook received an empty hook payload." >&2
  exit 2
fi

TOOL=$(printf '%s' "$INPUT" | jq -r '.tool_name // "Bash"' 2>/dev/null) || TOOL=""
if [ -z "$TOOL" ]; then
  echo "BLOCKED: git guardrails hook could not parse the hook payload." >&2
  exit 2
fi
[ "$TOOL" = "Bash" ] || exit 0

COMMAND=$(printf '%s' "$INPUT" | jq -er '.tool_input.command' 2>/dev/null) || {
  echo "BLOCKED: git guardrails hook could not read .tool_input.command from the hook payload." >&2
  exit 2
}

# Collapse whitespace, then strip git's global options repeatedly so that
# `git -C /repo push`, `git -c user.name=x push` and `git --git-dir=/r/.git push`
# all normalise to `git push` before matching.
NORM=$(printf '%s' "$COMMAND" | tr '\n\t' '  ' | sed -E 's/ {2,}/ /g')
PREV=""
while [ "$NORM" != "$PREV" ]; do
  PREV=$NORM
  NORM=$(printf '%s' "$NORM" | sed -E 's/(^|[;&|(]) ?git (-C [^ ]+|-c [^ ]+|--git-dir[= ][^ ]+|--work-tree[= ][^ ]+|--namespace[= ][^ ]+|--exec-path[= ][^ ]+|--no-pager|--paginate|--bare|--no-replace-objects|--literal-pathspecs|--glob-pathspecs|--noglob-pathspecs|--icase-pathspecs) /\1git /g')
done

DANGEROUS_PATTERNS=(
  "git +push"
  "push +(-[a-zA-Z]*f|--force)"
  "git +reset +[^;&|]*--hard"
  "reset +--hard"
  "git +clean +[^;&|]*-[a-zA-Z]*f"
  "git +branch +[^;&|]*-[a-zA-Z]*D"
  "git +branch +[^;&|]*(--delete[^;&|]*--force|--force[^;&|]*--delete)"
  "git +checkout +(-- +)?\.( |$)"
  "git +restore +([^;&|]* )?\.( |$)"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if printf '%s\n%s\n' "$COMMAND" "$NORM" | grep -qE "$pattern"; then
    echo "BLOCKED: '$COMMAND' matches dangerous pattern '$pattern'. The user has prevented you from doing this." >&2
    exit 2
  fi
done

exit 0
