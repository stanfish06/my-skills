import {
  BoxRenderable,
  InputRenderable,
  InputRenderableEvents,
  LinearScrollAccel,
  ScrollBoxRenderable,
  TextAttributes,
  TextRenderable,
  type CliRenderer,
  type KeyEvent,
  type MouseEvent,
} from "@opentui/core"

import type { Catalog, Product, SkillBackend, SkillRecord } from "./backend"

const COLORS = {
  background: "#111318",
  panel: "#181b22",
  panelAlt: "#20242d",
  border: "#4b5563",
  accent: "#7dd3fc",
  selected: "#263449",
  text: "#e5e7eb",
  muted: "#9ca3af",
  enabled: "#86efac",
  disabled: "#fca5a5",
  mixed: "#fde68a",
  error: "#f0abfc",
}

const NAME_COLUMN_GROW = 3
const CATEGORY_COLUMN_GROW = 2
const NAME_COLUMN_MIN_WIDTH = 14
const CATEGORY_COLUMN_MIN_WIDTH = 12
const MARK_COLUMN_WIDTH = 5
const PRODUCT_COLUMN_WIDTH = 9

export const STATUS_FILTERS = [
  "all",
  "enabled",
  "disabled",
  "mixed",
  "error",
  "claude:on",
  "claude:off",
  "codex:on",
  "codex:off",
] as const

export type StatusFilter = (typeof STATUS_FILTERS)[number]

function fuzzyTokenScore(token: string, value: string): number | null {
  const direct = value.indexOf(token)
  if (direct >= 0) return 200 - direct - Math.max(0, value.length - token.length) * 0.01

  let cursor = 0
  let first = -1
  let previous = -1
  let gaps = 0
  for (const character of token) {
    const index = value.indexOf(character, cursor)
    if (index < 0) return null
    if (first < 0) first = index
    if (previous >= 0) gaps += index - previous - 1
    previous = index
    cursor = index + 1
  }
  return 100 - first - gaps * 2
}

export function fuzzyScore(query: string, skill: SkillRecord): number | null {
  const tokens = query.toLocaleLowerCase().trim().split(/\s+/).filter(Boolean)
  if (tokens.length === 0) return 0
  const identity = `${skill.name} ${skill.key} ${skill.category}`.toLocaleLowerCase()
  const description = skill.description.toLocaleLowerCase()
  let score = 0
  for (const token of tokens) {
    const identityScore = fuzzyTokenScore(token, identity)
    const descriptionIndex = description.indexOf(token)
    const tokenScore = identityScore ?? (descriptionIndex >= 0 ? 75 - descriptionIndex * 0.01 : null)
    if (tokenScore === null) return null
    score += tokenScore
  }
  return score
}

function matchesStatus(skill: SkillRecord, filter: StatusFilter): boolean {
  switch (filter) {
    case "all":
      return true
    case "enabled":
    case "disabled":
    case "mixed":
    case "error":
      return skill.state === filter
    case "claude:on":
      return skill.claude_enabled === true
    case "claude:off":
      return skill.claude_enabled === false
    case "codex:on":
      return skill.codex_enabled === true
    case "codex:off":
      return skill.codex_enabled === false
  }
}

export function filterSkills(
  skills: SkillRecord[],
  query: string,
  statusFilter: StatusFilter,
  categoryFilter: string,
): SkillRecord[] {
  return skills
    .map((skill) => ({ skill, score: fuzzyScore(query, skill) }))
    .filter(
      (entry): entry is { skill: SkillRecord; score: number } =>
        entry.score !== null &&
        matchesStatus(entry.skill, statusFilter) &&
        (categoryFilter === "all" || entry.skill.category === categoryFilter),
    )
    .sort((left, right) => right.score - left.score || left.skill.name.localeCompare(right.skill.name))
    .map((entry) => entry.skill)
}

function stateColor(skill: SkillRecord): string {
  return COLORS[skill.state]
}

function productLabel(enabled: boolean | null): string {
  if (enabled === null) return "! error"
  return enabled ? "● on" : "○ off"
}

function productColor(enabled: boolean | null): string {
  if (enabled === null) return COLORS.error
  return enabled ? COLORS.enabled : COLORS.disabled
}

interface ButtonParts {
  box: BoxRenderable
  label: TextRenderable
}

export class SkillToggleApp {
  private catalogData: Catalog
  private query = ""
  private statusFilter: StatusFilter = "all"
  private categoryFilter = "all"
  private categories: string[]
  private filtered: SkillRecord[] = []
  private selectedKey: string | null = null
  private readonly markedKeys = new Set<string>()
  private busy = false
  private resetArmedAt = 0

  private readonly root: BoxRenderable
  private readonly search: InputRenderable
  private readonly summary: TextRenderable
  private readonly statusButton: ButtonParts
  private readonly categoryButton: ButtonParts
  private readonly list: ScrollBoxRenderable
  private readonly detail: TextRenderable
  private readonly message: TextRenderable
  private rows: BoxRenderable[] = []
  private rowByKey = new Map<string, BoxRenderable>()
  private markCellByKey = new Map<string, TextRenderable>()

  constructor(
    private readonly renderer: CliRenderer,
    private readonly backend: SkillBackend,
    catalog: Catalog,
    initialQuery = "",
  ) {
    this.catalogData = catalog
    this.categories = ["all", ...catalog.categories]
    this.query = initialQuery

    this.root = new BoxRenderable(renderer, {
      id: "skill-toggle-app",
      width: "100%",
      height: "100%",
      flexDirection: "column",
      backgroundColor: COLORS.background,
      padding: 1,
      gap: 1,
    })

    const heading = new BoxRenderable(renderer, {
      id: "heading",
      width: "100%",
      height: 2,
      flexDirection: "row",
      justifyContent: "space-between",
    })
    heading.add(
      new TextRenderable(renderer, {
        id: "title",
        content: "Skill Invocation Control",
        fg: COLORS.accent,
        attributes: TextAttributes.BOLD,
        height: 1,
      }),
    )
    this.summary = new TextRenderable(renderer, {
      id: "summary",
      content: "",
      fg: COLORS.muted,
      height: 1,
    })
    heading.add(this.summary)
    this.root.add(heading)

    const searchBar = new BoxRenderable(renderer, {
      id: "search-bar",
      width: "100%",
      height: 3,
      borderStyle: "rounded",
      borderColor: COLORS.border,
      backgroundColor: COLORS.panel,
      paddingX: 1,
      flexDirection: "row",
      alignItems: "center",
      gap: 1,
    })
    searchBar.add(
      new TextRenderable(renderer, {
        id: "search-label",
        content: "Search",
        fg: COLORS.muted,
        width: 7,
        height: 1,
      }),
    )
    this.search = new InputRenderable(renderer, {
      id: "search-input",
      value: initialQuery,
      placeholder: "fuzzy find by name, description, or category…",
      flexGrow: 1,
      backgroundColor: COLORS.panelAlt,
      focusedBackgroundColor: COLORS.selected,
      textColor: COLORS.text,
      cursorColor: COLORS.accent,
    })
    this.search.on(InputRenderableEvents.INPUT, (value: string) => {
      this.query = value
      this.applyFilters()
    })
    searchBar.add(this.search)
    searchBar.add(this.createButton("save", "Save", 9, () => void this.saveSnapshot()).box)
    searchBar.add(this.createButton("reload", "Reload", 10, () => void this.loadSnapshot()).box)
    searchBar.add(this.createButton("reset", "Activate all", 14, () => void this.armOrReset()).box)
    this.root.add(searchBar)

    const filters = new BoxRenderable(renderer, {
      id: "filters",
      width: "100%",
      height: 3,
      borderStyle: "rounded",
      borderColor: COLORS.border,
      backgroundColor: COLORS.panel,
      paddingX: 1,
      flexDirection: "row",
      alignItems: "center",
      gap: 1,
    })
    filters.add(
      new TextRenderable(renderer, {
        id: "filter-label",
        content: "Filters",
        fg: COLORS.muted,
        width: 7,
        height: 1,
      }),
    )
    this.statusButton = this.createButton("status-filter", "", 20, (event) =>
      this.cycleStatus(event.modifiers.ctrl ? -1 : 1),
    )
    this.categoryButton = this.createButton("category-filter", "", 30, (event) =>
      this.cycleCategory(event.modifiers.ctrl ? -1 : 1),
    )
    filters.add(this.statusButton.box)
    filters.add(this.categoryButton.box)
    filters.add(this.createButton("reset-filters", "Reset", 9, () => this.resetFilters()).box)
    filters.add(
      new TextRenderable(renderer, {
        id: "filter-help",
        content: "click / Ctrl-click to cycle",
        fg: COLORS.muted,
        flexGrow: 1,
        flexBasis: 0,
        minWidth: 0,
        overflow: "hidden",
        height: 1,
      }),
    )
    this.root.add(filters)

    const content = new BoxRenderable(renderer, {
      id: "content",
      width: "100%",
      flexGrow: 1,
      flexDirection: "row",
      gap: 1,
      overflow: "hidden",
    })
    const listPanel = new BoxRenderable(renderer, {
      id: "list-panel",
      flexGrow: 2,
      flexBasis: 0,
      // Keep the minimums in the same 2:1 proportion as flex growth so the
      // outer pane ratio stays stable at every usable terminal width.
      minWidth: 48,
      flexShrink: 1,
      height: "100%",
      borderStyle: "rounded",
      borderColor: COLORS.border,
      title: " Skills ",
      titleColor: COLORS.accent,
      backgroundColor: COLORS.panel,
      flexDirection: "column",
      // No overflow: "hidden" here: OpenTUI 0.5.1 offsets the hit-grid
      // scissor of a bordered box by its border, which makes the last inner
      // column (the scrollbar) unreachable by the mouse. The scrollbox below
      // clips its own content, so nothing can overflow this panel anyway.
    })
    const columns = new BoxRenderable(renderer, {
      id: "columns",
      width: "100%",
      height: 1,
      flexDirection: "row",
      backgroundColor: COLORS.panelAlt,
      // The scrollbox reserves one terminal cell for its scrollbar. Match
      // that inset so headers and row cells share the same column geometry.
      paddingRight: 1,
    })
    columns.add(
      this.tableCell(
        "column-mark",
        "Mark",
        COLORS.muted,
        undefined,
        undefined,
        MARK_COLUMN_WIDTH,
      ),
    )
    columns.add(
      this.tableCell(
        "column-name",
        "Skill",
        COLORS.muted,
        NAME_COLUMN_GROW,
        NAME_COLUMN_MIN_WIDTH,
        undefined,
        2,
      ),
    )
    columns.add(
      this.tableCell(
        "column-category",
        "Category",
        COLORS.muted,
        CATEGORY_COLUMN_GROW,
        CATEGORY_COLUMN_MIN_WIDTH,
      ),
    )
    columns.add(
      this.tableCell("column-claude", "Claude", COLORS.muted, undefined, undefined, PRODUCT_COLUMN_WIDTH),
    )
    columns.add(
      this.tableCell("column-codex", "Codex", COLORS.muted, undefined, undefined, PRODUCT_COLUMN_WIDTH),
    )
    listPanel.add(columns)
    this.list = new ScrollBoxRenderable(renderer, {
      id: "skill-list",
      width: "100%",
      flexGrow: 1,
      scrollY: true,
      scrollAcceleration: new LinearScrollAccel(),
      viewportCulling: true,
      scrollbarOptions: {
        showArrows: false,
        trackOptions: {
          foregroundColor: COLORS.accent,
          backgroundColor: COLORS.panelAlt,
        },
      },
      contentOptions: {
        flexDirection: "column",
      },
    })
    // A focused scrollbox consumes ↑↓/j/k/PgUp/PgDn itself, fighting the
    // app-level selection movement. All list scrolling goes through
    // moveSelection, so keep keyboard focus away from it.
    this.list.focusable = false
    this.installScrollbarDrag()
    listPanel.add(this.list)
    content.add(listPanel)

    const detailPanel = new BoxRenderable(renderer, {
      id: "detail-panel",
      flexGrow: 1,
      flexBasis: 0,
      flexShrink: 1,
      minWidth: 24,
      height: "100%",
      borderStyle: "rounded",
      borderColor: COLORS.border,
      title: " Details ",
      titleColor: COLORS.accent,
      backgroundColor: COLORS.panel,
      overflow: "hidden",
    })
    const detailContent = new BoxRenderable(renderer, {
      id: "detail-content",
      width: "100%",
      height: "100%",
      padding: 1,
      overflow: "hidden",
    })
    this.detail = new TextRenderable(renderer, {
      id: "detail-text",
      content: "",
      fg: COLORS.text,
      width: "100%",
      height: "100%",
    })
    detailContent.add(this.detail)
    detailPanel.add(detailContent)
    content.add(detailPanel)
    this.root.add(content)

    const footer = new BoxRenderable(renderer, {
      id: "footer",
      width: "100%",
      height: 2,
      flexDirection: "column",
    })
    footer.add(
      new TextRenderable(renderer, {
        id: "shortcuts",
        content: "/ search   ↑↓ move   M mark   C Claude   X Codex   Space both   F status   G category   Ctrl-S/R/P   Q quit",
        fg: COLORS.muted,
        height: 1,
      }),
    )
    this.message = new TextRenderable(renderer, {
      id: "message",
      content: "Ready",
      fg: COLORS.accent,
      height: 1,
    })
    footer.add(this.message)
    this.root.add(footer)

    this.renderer.root.add(this.root)
    this.renderer.keyInput.on("keypress", this.handleKey)
    this.applyFilters()
    this.search.focus()
  }

  private cellText(
    id: string,
    content: string,
    width: number | "auto" | `${number}%`,
    color: string,
  ): TextRenderable {
    return new TextRenderable(this.renderer, {
      id,
      content,
      width,
      height: 1,
      fg: color,
      selectable: false,
    })
  }

  private tableCell(
    id: string,
    content: string,
    color: string,
    flexGrow?: number,
    minWidth?: number,
    width?: number,
    paddingLeft = 1,
  ): BoxRenderable {
    const cell = new BoxRenderable(this.renderer, {
      id,
      flexGrow,
      flexBasis: flexGrow === undefined ? undefined : 0,
      minWidth,
      width,
      height: 1,
      paddingLeft,
      paddingRight: 1,
      overflow: "hidden",
    })
    cell.add(
      new TextRenderable(this.renderer, {
        id: `${id}-label`,
        content,
        width: "100%",
        height: 1,
        fg: color,
        selectable: false,
      }),
    )
    return cell
  }

  private createButton(
    id: string,
    content: string,
    width: number,
    action: (event: MouseEvent) => void,
  ): ButtonParts {
    const box = new BoxRenderable(this.renderer, {
      id: `button-${id}`,
      width,
      height: 1,
      backgroundColor: COLORS.panelAlt,
      onMouseDown: (event) => {
        event.stopPropagation()
        this.search?.blur()
        action(event)
      },
      onMouseOver: () => {
        box.backgroundColor = COLORS.selected
      },
      onMouseOut: () => {
        box.backgroundColor = COLORS.panelAlt
      },
    })
    const label = this.cellText(`button-${id}-label`, ` ${content}`, "100%", COLORS.text)
    box.add(label)
    return { box, label }
  }

  private installScrollbarDrag(): void {
    // The renderer only captures the drag target once the pointer has
    // produced a drag event while still over the 1-cell scrollbar column.
    // A press on the thumb followed by a diagonal move captures a list row
    // instead and the thumb never follows. Track thumb presses ourselves and
    // forward every bubbled drag/up back to the slider's own handlers.
    const slider = this.list.verticalScrollBar.slider
    const listeners = (slider as unknown as {
      _mouseListeners: Record<string, (event: MouseEvent) => void>
    })._mouseListeners
    const sliderDown = listeners["down"]
    const sliderDrag = listeners["drag"]
    const sliderUp = listeners["up"]
    if (!sliderDown || !sliderDrag || !sliderUp) return
    let dragging = false
    slider.onMouseDown = (event: MouseEvent) => {
      dragging = true
      sliderDown.call(slider, event)
    }
    this.list.onMouse = (event: MouseEvent) => {
      if (!dragging) return
      if (event.type === "drag") {
        sliderDrag.call(slider, event)
      } else if (event.type === "up") {
        dragging = false
        sliderUp.call(slider, event)
      } else if (event.type === "down" && event.target !== slider) {
        // The release happened outside the list (never bubbled here); a new
        // press ends the stale drag without moving the thumb.
        dragging = false
      }
    }
  }

  private applyFilters(preserveScroll = false): void {
    this.filtered = filterSkills(
      this.catalogData.skills,
      this.query,
      this.statusFilter,
      this.categoryFilter,
    )
    this.retainVisibleMarks()
    if (!this.selectedKey || !this.filtered.some((skill) => skill.key === this.selectedKey)) {
      this.selectedKey = this.filtered[0]?.key ?? null
    }
    this.rebuildRows(preserveScroll)
    this.updateFilterLabels()
    this.updateSummary()
    this.updateDetail()
  }

  private retainVisibleMarks(): void {
    const visible = new Set(this.filtered.map((skill) => skill.key))
    for (const key of this.markedKeys) {
      if (!visible.has(key)) this.markedKeys.delete(key)
    }
  }

  private rebuildRows(preserveScroll = false): void {
    const previousScrollTop = this.list.scrollTop
    for (const row of this.rows) row.destroyRecursively()
    this.rows = []
    this.rowByKey.clear()
    this.markCellByKey.clear()

    for (const skill of this.filtered) {
      const row = new BoxRenderable(this.renderer, {
        id: `skill-${skill.key}`,
        width: "100%",
        height: 1,
        flexDirection: "row",
        backgroundColor: skill.key === this.selectedKey ? COLORS.selected : COLORS.panel,
        onMouseDown: (event) => {
          event.stopPropagation()
          this.search.blur()
          this.selectKey(skill.key)
        },
        onMouseOver: () => {
          if (skill.key !== this.selectedKey) row.backgroundColor = COLORS.panelAlt
        },
        onMouseOut: () => {
          if (skill.key !== this.selectedKey) row.backgroundColor = COLORS.panel
        },
        onMouseScroll: (event) => {
          const direction = event.scroll?.direction
          if (direction !== "up" && direction !== "down") return
          event.stopPropagation()
          const distance = Math.max(1, Math.round(event.scroll?.delta ?? 1))
          this.moveSelection(direction === "down" ? distance : -distance)
        },
      })
      const markCell = this.tableCell(
        `mark-${skill.key}`,
        this.markedKeys.has(skill.key) ? "[x]" : "[ ]",
        this.markedKeys.has(skill.key) ? COLORS.accent : COLORS.muted,
        undefined,
        undefined,
        MARK_COLUMN_WIDTH,
      )
      row.add(markCell)
      const markLabel = markCell.findDescendantById(`mark-${skill.key}-label`)
      if (markLabel) this.markCellByKey.set(skill.key, markLabel as TextRenderable)
      row.add(
        this.tableCell(
          `name-${skill.key}`,
          skill.name,
          stateColor(skill),
          NAME_COLUMN_GROW,
          NAME_COLUMN_MIN_WIDTH,
          undefined,
          2,
        ),
      )
      row.add(
        this.tableCell(
          `category-${skill.key}`,
          skill.category,
          COLORS.muted,
          CATEGORY_COLUMN_GROW,
          CATEGORY_COLUMN_MIN_WIDTH,
        ),
      )
      row.add(this.productCell(skill, "claude", PRODUCT_COLUMN_WIDTH))
      row.add(this.productCell(skill, "codex", PRODUCT_COLUMN_WIDTH))
      this.list.add(row)
      this.rows.push(row)
      this.rowByKey.set(skill.key, row)
    }
    this.list.scrollTo(preserveScroll ? previousScrollTop : 0)
  }

  private productCell(skill: SkillRecord, product: Exclude<Product, "both">, width: number): BoxRenderable {
    const enabled = product === "claude" ? skill.claude_enabled : skill.codex_enabled
    const box = new BoxRenderable(this.renderer, {
      id: `${product}-${skill.key}`,
      width,
      height: 1,
      paddingLeft: 1,
      paddingRight: 1,
      backgroundColor: "transparent",
      onMouseDown: (event) => {
        event.stopPropagation()
        this.search.blur()
        this.selectKey(skill.key)
        void this.toggleProduct(product, skill.key)
      },
      onMouseOver: () => {
        box.backgroundColor = COLORS.selected
      },
      onMouseOut: () => {
        box.backgroundColor = "transparent"
      },
    })
    box.add(this.cellText(`${product}-${skill.key}-label`, productLabel(enabled), "100%", productColor(enabled)))
    return box
  }

  private selectKey(key: string): void {
    const previous = this.selectedKey
    this.selectedKey = key
    if (previous) {
      const previousRow = this.rowByKey.get(previous)
      if (previousRow) previousRow.backgroundColor = COLORS.panel
    }
    const row = this.rowByKey.get(key)
    if (row) row.backgroundColor = COLORS.selected
    this.updateDetail()
  }

  private updateDetail(): void {
    const skill = this.catalogData.skills.find((candidate) => candidate.key === this.selectedKey)
    if (!skill) {
      this.detail.content = "No skills match the active filters."
      return
    }
    this.detail.content = [
      skill.name,
      "",
      `Category  ${skill.category}`,
      `State     ${skill.state}`,
      `Claude    ${productLabel(skill.claude_enabled)}`,
      `Codex     ${productLabel(skill.codex_enabled)}`,
      "",
      skill.description,
      "",
      skill.directory,
      skill.error ? `\nError: ${skill.error}` : "",
    ].join("\n")
  }

  private updateSummary(): void {
    const total = this.catalogData.skills.length
    const enabled = this.catalogData.skills.filter((skill) => skill.state === "enabled").length
    const disabled = this.catalogData.skills.filter((skill) => skill.state === "disabled").length
    const mixed = this.catalogData.skills.filter((skill) => skill.state === "mixed").length
    this.summary.content = `${this.filtered.length}/${total} shown   ${enabled} enabled   ${disabled} disabled   ${mixed} mixed   ${this.markedKeys.size} marked`
  }

  private updateFilterLabels(): void {
    this.statusButton.label.content = ` Status: ${this.statusFilter}`
    this.categoryButton.label.content = ` Category: ${this.categoryFilter}`
  }

  private cycleStatus(direction: number): void {
    this.search.blur()
    const index = STATUS_FILTERS.indexOf(this.statusFilter)
    this.statusFilter = STATUS_FILTERS[(index + direction + STATUS_FILTERS.length) % STATUS_FILTERS.length]
    this.applyFilters()
  }

  private cycleCategory(direction: number): void {
    this.search.blur()
    const index = Math.max(0, this.categories.indexOf(this.categoryFilter))
    this.categoryFilter = this.categories[(index + direction + this.categories.length) % this.categories.length]
    this.applyFilters()
  }

  private resetFilters(): void {
    this.search.blur()
    this.statusFilter = "all"
    this.categoryFilter = "all"
    this.applyFilters()
    this.setMessage("Filters reset")
  }

  private moveSelection(amount: number): void {
    if (this.filtered.length === 0) return
    const current = this.filtered.findIndex((skill) => skill.key === this.selectedKey)
    const next = Math.max(0, Math.min(this.filtered.length - 1, (current < 0 ? 0 : current) + amount))
    const skill = this.filtered[next]
    this.selectKey(skill.key)
    this.list.scrollChildIntoView(`skill-${skill.key}`)
  }

  private selectedSkill(): SkillRecord | undefined {
    return this.catalogData.skills.find((skill) => skill.key === this.selectedKey)
  }

  private toggleMark(): void {
    const skill = this.selectedSkill()
    if (!skill || skill.error) {
      this.setMessage(skill?.error || "Cannot mark this skill")
      return
    }
    if (this.markedKeys.has(skill.key)) this.markedKeys.delete(skill.key)
    else this.markedKeys.add(skill.key)
    // Update the mark cell in place: rebuilding the rows here would reset
    // the scroll position and make the viewport jump on every keystroke.
    const markLabel = this.markCellByKey.get(skill.key)
    if (markLabel) {
      const marked = this.markedKeys.has(skill.key)
      markLabel.content = marked ? "[x]" : "[ ]"
      markLabel.fg = marked ? COLORS.accent : COLORS.muted
    }
    this.updateSummary()
  }

  private toggleTargets(): SkillRecord[] {
    const keys =
      this.markedKeys.size > 0
        ? this.markedKeys
        : new Set(this.selectedKey ? [this.selectedKey] : [])
    return this.catalogData.skills.filter((skill) => keys.has(skill.key) && !skill.error)
  }

  private productIsEnabled(skill: SkillRecord, product: Product): boolean {
    if (product === "both") {
      return skill.claude_enabled === true && skill.codex_enabled === true
    }
    return product === "claude"
      ? skill.claude_enabled === true
      : skill.codex_enabled === true
  }

  private async toggleProduct(product: Product, singleKey?: string): Promise<void> {
    if (this.busy) return
    const targets = singleKey
      ? this.catalogData.skills.filter((skill) => skill.key === singleKey && !skill.error)
      : this.toggleTargets()
    if (targets.length === 0) {
      const selected = this.selectedSkill()
      this.setMessage(selected?.error || "No changeable skills selected")
      return
    }
    const enabled = !targets.every((skill) => this.productIsEnabled(skill, product))
    const keys = targets.map((skill) => skill.key)
    const noun = keys.length === 1 ? "skill" : "skills"
    this.busy = true
    this.setMessage(`Updating ${keys.length} ${noun} for ${product}…`)
    try {
      await this.backend.setProducts(keys, product, enabled)
      await this.refreshCatalog()
      this.setMessage(`${product} ${enabled ? "enabled" : "disabled"} for ${keys.length} ${noun}`)
    } catch (error) {
      this.setMessage(`Error: ${error instanceof Error ? error.message : String(error)}`)
    } finally {
      this.busy = false
    }
  }

  private async refreshCatalog(): Promise<void> {
    this.catalogData = await this.backend.catalog()
    this.categories = ["all", ...this.catalogData.categories]
    if (!this.categories.includes(this.categoryFilter)) this.categoryFilter = "all"
    // Toggling a skill refreshes the catalog; keep the viewport where it was.
    this.applyFilters(true)
  }

  private async saveSnapshot(): Promise<void> {
    if (this.busy) return
    this.busy = true
    this.setMessage("Saving invocation states…")
    try {
      this.setMessage(await this.backend.saveSnapshot())
    } catch (error) {
      this.setMessage(`Error: ${error instanceof Error ? error.message : String(error)}`)
    } finally {
      this.busy = false
    }
  }

  private async loadSnapshot(): Promise<void> {
    if (this.busy) return
    this.busy = true
    this.setMessage("Reloading saved invocation states…")
    try {
      this.setMessage(await this.backend.loadSnapshot())
      await this.refreshCatalog()
    } catch (error) {
      this.setMessage(`Error: ${error instanceof Error ? error.message : String(error)}`)
    } finally {
      this.busy = false
    }
  }

  private async armOrReset(): Promise<void> {
    const now = Date.now()
    if (now - this.resetArmedAt > 5_000) {
      this.resetArmedAt = now
      this.setMessage("Pre-commit reset armed: click Activate all or press Ctrl-P again within 5 seconds")
      return
    }
    if (this.busy) return
    this.resetArmedAt = 0
    this.busy = true
    this.setMessage("Saving current state and activating every skill for both products…")
    try {
      this.setMessage(await this.backend.preCommitReset())
      await this.refreshCatalog()
    } catch (error) {
      this.setMessage(`Error: ${error instanceof Error ? error.message : String(error)}`)
    } finally {
      this.busy = false
    }
  }

  private setMessage(value: string): void {
    this.message.content = value
  }

  private readonly handleKey = (key: KeyEvent): void => {
    if (key.eventType === "release") return
    if (key.ctrl && key.name === "s") {
      void this.saveSnapshot()
      return
    }
    if (key.ctrl && key.name === "r") {
      void this.loadSnapshot()
      return
    }
    if (key.ctrl && key.name === "p") {
      void this.armOrReset()
      return
    }

    const searchFocused = this.renderer.currentFocusedRenderable === this.search
    if (searchFocused) {
      if (key.name === "escape" || key.name === "return") this.search.blur()
      return
    }

    switch (key.name) {
      case "q":
      case "escape":
        this.renderer.destroy()
        return
      case "/":
        this.search.focus()
        return
      case "up":
      case "k":
        this.moveSelection(-1)
        return
      case "down":
      case "j":
        this.moveSelection(1)
        return
      case "pageup":
        this.moveSelection(-10)
        return
      case "pagedown":
        this.moveSelection(10)
        return
      case "home":
        this.moveSelection(-this.filtered.length)
        return
      case "end":
        this.moveSelection(this.filtered.length)
        return
      case "space": {
        void this.toggleProduct("both")
        return
      }
      case "c": {
        void this.toggleProduct("claude")
        return
      }
      case "x": {
        void this.toggleProduct("codex")
        return
      }
      case "m": {
        this.toggleMark()
        return
      }
      case "f":
        this.cycleStatus(key.shift ? -1 : 1)
        return
      case "g":
        this.cycleCategory(key.shift ? -1 : 1)
        return
    }
  }
}
