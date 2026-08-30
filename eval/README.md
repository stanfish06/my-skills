# Skill eval suite (v0)

Measures whether a skill changes what a model writes. One skill at a time — no
combinatorial skill interaction.

```bash
./run-eval.sh              # smoke: 1 model, 2 tasks, 3 skills, k=3  (~15 generations)
./run-eval.sh full         # 4 models, k=5
./run-eval.sh replay       # re-score the last run offline, zero API calls
./run-eval.sh report [id]  # print a saved run
./run-eval.sh runs         # list saved runs
```

Or the mise tasks directly: `mise run smoke | full | replay | report | runs`.

## What it measures

Every task ships a **rubric** — a list of traits describing what good code for
that task looks like. Each trait is tagged with which skill prescribes it:

- `skill%` — traits the skill under test prescribes. Adherence: did the
  guidance land?
- `full%` — the whole rubric, including **blind traits** that no skill asks for
  (`prescribedBy: []`). Catches a skill that wins on its own traits while making
  the rest of the code worse.

Both arms are scored against the same rubric, so the number that matters is the
delta, not the level.

## Arms

`baseline` (task only) and `skill` (task + skill). `placebo` — a length-matched
filler system prompt — is a third value in the enum but is not run in v0. Until
it is, a delta cannot separate "the skill's content helped" from "a longer
system prompt helped".

Baseline generations are keyed by `(model, task, rep)` and shared by every skill
paired with that task, so N skills on one task cost one baseline, not N.

## Injection

Skills reach the model two ways, declared per skill in `src/config.ts`:

| injection | skill | mechanism |
|---|---|---|
| `prose` | `modern-typescript`, `zz-prefix` | `SKILL.md` pasted into the system prompt |
| `tool` | `use-modern-go` | its CLI exposed as AI SDK tools |

`use-modern-go` has zero rules in its `SKILL.md` — 378 words telling the agent to
shell out to the Modern Go Guidelines CLI. Pasting it would hand the model
instructions for a command it cannot run, so the harness wires `list` and
`explain` as tools and leaves the skill body verbatim. The report shows median
tool calls per generation, which separates a routing failure (never called the
tool) from an application failure (called it, ignored the answer).

## Gates

Trait scores are only computed on code that survives a gate.

- TS: `tsc --noEmit --strict --noUncheckedIndexedAccess`
- Go: `go build` → `go vet` → `go test -run Test` against harness-owned tests

`trunc` in the report counts generations that hit the output cap and returned
nothing. Those are held separate from gate failures on purpose — reporting an
empty generation as a compile failure would read as the skill breaking the code.

## Trait self-test

Every trait carries a `fixture` with a `satisfies` and a `violates` sample. The
harness scores both before it scores anything real and aborts if a pattern
misclassifies its own fixture. A brittle pattern fails loudly at startup instead
of silently skewing a run.

## The positive control

`control/zz-prefix` is a synthetic skill demanding every exported symbol be
prefixed `zz_`. No model does that unprompted, so baseline should score ~0% and
the skill arm ~100%. If that delta does not appear, the harness is broken — not
the skill. Check it before trusting any other row.

## Reading the bench numbers

`allocs/op` and `B/op` are stable across re-runs on the same code. `ns/op` is
not — a replay of identical code moved 36750 → 51132 ns/op on an otherwise busy
machine. Compare arms on allocations and bytes; treat wall time as indicative
only.

## Output

`runs/<runId>/` holds `cells.jsonl` (one row per generation: full system prompt,
prompt, raw response, extracted code, tool calls, usage, gate detail, per-trait
results, bench), `manifest.json` (config plus skill folder hashes and the
guidelines CLI version, so an old run stays interpretable after a skill drifts),
`report.md`, and `summary.json`.

Generations are content-addressed in `.cache/gen/` by
`(model, system, prompt, rep)`, so a re-run only pays for cells that changed.
Truncated and empty generations are never cached.

## Known v0 limits

- No placebo arm, so prompt-length effects are not separated out.
- Reasoning effort is not pinned per model; `think` (median reasoning tokens)
  is reported so the confound is at least visible.
- Trait matching is regex over comment-stripped source. Tokens inside string
  literals still count. `kind: "ast-grep"` is wired for structural patterns but
  unused so far.
- k=3 in smoke is enough to see a large effect, not a small one.
