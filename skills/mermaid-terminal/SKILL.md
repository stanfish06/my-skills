---
name: mermaid-terminal
description: Render Mermaid source locally and preview it in Ghostty, Kitty, or another Kitty-graphics-compatible terminal. Use when a user wants to see a Mermaid diagram without opening a browser; do not use for general image viewing or non-Mermaid diagrams.
---

# Mermaid Terminal

Use the bundled renderer to turn Mermaid source into a PNG and send it to the
current terminal with the Kitty graphics protocol.

## Preview a diagram

Locate this skill directory, then run:

```bash
python3 <skill-dir>/scripts/mermaid_terminal.py diagram.mmd
```

The script also accepts Mermaid source on standard input:

```bash
printf '%s\n' 'flowchart LR' '  A --> B' \
  | python3 <skill-dir>/scripts/mermaid_terminal.py -
```

It accepts a Markdown file or stdin containing a fenced `mermaid` block and
renders the first block. Use `--output diagram.png --no-display` when the caller
needs a persistent file instead of an inline terminal preview.

## Workflow

1. Preserve or create editable Mermaid source before rendering.
2. Use a temporary `.mmd` file unless the user asked to keep the source.
3. Run the bundled script. It prefers `mmdc` on `PATH`; otherwise it uses a
   pinned Mermaid CLI through Bun or npm. The fallback downloads into the
   package-manager cache on first use but never sends diagram source to a
   rendering service.
   When an agent shell captures stdout, the script finds the nearest parent
   terminal device, reads geometry with an ioctl (never a terminal query — the
   agent host owns the terminal's input and would swallow the reply), and shows
   the diagram on the alternate screen. By default it holds until interrupted:
   the user dismisses it with Esc or Ctrl-C (which makes the host kill the
   command; SIGTERM/SIGINT handlers restore the screen), and the Bash timeout
   is the backstop. Tell the user how to dismiss it. Pass `--hold-seconds N`
   for a timed preview that restores by itself when you need the shell back
   without user action.
4. Report Mermaid syntax errors with the source path and keep the editable
   source available for correction.
5. If inline display is unavailable, rerun with `--output` and return the PNG
   path. Do not claim the diagram appeared in the user's terminal when the
   command was run without a TTY or with `--no-display`.

Use `--theme neutral` for a light terminal and `--theme dark` for a dark
terminal when automatic selection is wrong. Pass `--help` for the complete
script interface.

## Neovim and Snacks

Snacks can render fenced Mermaid blocks inside Neovim when its `image` module
is enabled, the Markdown Tree-sitter parser is installed, and `mmdc` is on
`PATH`. Do not edit the user's Neovim configuration unless they explicitly ask.
The bundled script is the default path because it works independently of editor
configuration and uses the same Kitty graphics capability exposed by Ghostty.

## Constraints

- Keep rendering local; do not upload diagram source to Kroki or another remote
  service without explicit permission.
- Display through `kitten icat` using streamed image data so the terminal does
  not need to read the renderer's temporary file.
- In a captured shell, never let `kitten icat` query the terminal or wait for a
  keypress: pass `--use-window-size` from the ioctl geometry and use the timed
  hold. Both reads race against the agent host's own terminal reader.
- Treat Mermaid source as untrusted input to the renderer. Do not interpolate it
  into a shell command.
