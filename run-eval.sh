#!/usr/bin/env bash
# Entry point for the skill eval suite.
#   ./run-eval.sh              -> smoke run (1 model, 3 skills, k=3)
#   ./run-eval.sh full         -> all configured models
#   ./run-eval.sh replay [id]  -> re-score a saved run offline, no API calls
#   ./run-eval.sh report [id]  -> print a saved run's report
#   ./run-eval.sh runs         -> list saved runs
set -euo pipefail
cd "$(dirname "$0")/eval"

command -v mise >/dev/null || { echo "run-eval: mise is required (see mise.jdx.dev)" >&2; exit 1; }
mise trust --quiet . 2>/dev/null || true

case "${1:-smoke}" in
  smoke)  mise run setup && exec mise exec -- bun run src/cli.ts run --config smoke "${@:2}" ;;
  full)   mise run setup && exec mise exec -- bun run src/cli.ts run --config full  "${@:2}" ;;
  replay) exec mise exec -- bun run src/cli.ts replay "${@:2}" ;;
  report) exec mise exec -- bun run src/cli.ts report "${@:2}" ;;
  runs)   exec mise exec -- bun run src/cli.ts runs ;;
  *)      echo "usage: $0 [smoke|full|replay|report|runs] [runId]" >&2; exit 2 ;;
esac
