---
name: git-guardrails-claude-code
description: Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean, branch -D, etc.) before they execute. Use when user wants to prevent destructive git operations, add git safety hooks, or block git push/reset in Claude Code.
---

# Setup Git Guardrails

Sets up a PreToolUse hook that intercepts and blocks dangerous git commands before Claude executes them.

## What Gets Blocked

- `git push` (all variants including `--force`)
- `git reset --hard`
- `git clean -f` / `git clean -fd` / `git clean -xdf`
- `git branch -D` / `git branch --delete --force`
- `git checkout .` / `git checkout -- .` / `git restore .` / `git restore --staged .`

The script strips git's global options before matching, so `git -C <path> push`,
`git -c <key>=<val> push` and `git --git-dir=… --work-tree=… push` are blocked too.

When blocked, Claude sees a message telling it that it does not have authority to access these commands.

## Limits

Matching is substring-based on the command text, so it over-blocks (a command that
merely mentions `git push` is refused) and it cannot see through `eval`, a shell
variable, or a script the command invokes. Treat it as a seatbelt against accidents,
not as a security boundary.

## Requires

`jq`, on the `PATH` of every environment the hook runs in — Claude Code does not
bundle it, and the global install in step 1 puts the hook in devcontainers and CI
images too. If `jq` is missing or the payload does not parse, the script exits 2
(blocks) rather than silently permitting.

## Steps

### 1. Ask scope

Ask the user: install for **this project only** (`.claude/settings.json`) or **all projects** (`~/.claude/settings.json`)?

### 2. Copy the hook script

The bundled script is at: [scripts/block-dangerous-git.sh](scripts/block-dangerous-git.sh)

Copy it to the target location based on scope:

- **Project**: `.claude/hooks/block-dangerous-git.sh`
- **Global**: `~/.claude/hooks/block-dangerous-git.sh`

Make it executable with `chmod +x`.

### 3. Add hook to settings

Add to the appropriate settings file:

**Project** (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

**Global** (`~/.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

If the settings file already exists, merge the hook into the existing `hooks.PreToolUse` array. Don't overwrite other settings.

### 4. Ask about customization

Ask if user wants to add or remove any patterns from the blocked list. Edit the copied script accordingly.

### 5. Verify

Run a quick test:

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | <path-to-script>
echo '{"tool_input":{"command":"git -C /tmp push origin main"}}' | <path-to-script>
echo '{}' | <path-to-script>
```

All three should exit with code 2 and print a BLOCKED message to stderr — the last
one confirms the hook fails closed on a payload it cannot read.
