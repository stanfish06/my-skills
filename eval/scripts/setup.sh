#!/usr/bin/env bash
# Materialize eval/.env from the repo-root key file, then install deps.
set -euo pipefail
cd "$(dirname "$0")/.."

KEY_FILE="${AI_GATEWAY_KEY_FILE:-../vercel-api.txt}"

if [ ! -f .env ]; then
  if [ -f "$KEY_FILE" ]; then
    printf 'AI_GATEWAY_API_KEY=%s\n' "$(tr -d '[:space:]' < "$KEY_FILE")" > .env
    chmod 600 .env
    echo "setup: wrote .env from $KEY_FILE"
  else
    echo "setup: no .env and no $KEY_FILE — set AI_GATEWAY_API_KEY yourself" >&2
  fi
fi

[ -d node_modules ] || bun install
echo "setup: ok"
