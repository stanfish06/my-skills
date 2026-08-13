import { afterEach, describe, expect, test } from "bun:test"
import { type BoxRenderable, type ScrollBoxRenderable, type TextRenderable } from "@opentui/core"
import { createTestRenderer, type TestRendererSetup } from "@opentui/core/testing"

import { SkillToggleApp, filterSkills, fuzzyScore } from "./app"
import type { Catalog, Product, SkillBackend, SkillRecord } from "./backend"

function makeSkill(
  key: string,
  category = "software-dev",
  claude = true,
  codex = true,
): SkillRecord {
  return {
    key,
    name: key,
    description: `${key} description`,
    directory: `/skills/${key}`,
    category,
    claude_enabled: claude,
    codex_enabled: codex,
    state: claude && codex ? "enabled" : !claude && !codex ? "disabled" : "mixed",
    error: null,
  }
}

class FakeBackend implements SkillBackend {
  calls: Array<{ keys: string[]; product: Product; enabled: boolean }> = []

  constructor(readonly data: Catalog) {}

  async catalog(): Promise<Catalog> {
    return structuredClone(this.data)
  }

  async setProducts(keys: string[], product: Product, enabled: boolean): Promise<void> {
    this.calls.push({ keys, product, enabled })
    for (const key of keys) {
      const skill = this.data.skills.find((candidate) => candidate.key === key)
      if (!skill) throw new Error(`unknown skill ${key}`)
      if (product === "both" || product === "claude") skill.claude_enabled = enabled
      if (product === "both" || product === "codex") skill.codex_enabled = enabled
      skill.state =
        skill.claude_enabled && skill.codex_enabled
          ? "enabled"
          : !skill.claude_enabled && !skill.codex_enabled
            ? "disabled"
            : "mixed"
    }
  }

  async saveSnapshot(): Promise<string> {
    return "saved"
  }

  async loadSnapshot(): Promise<string> {
    return "loaded"
  }

  async preCommitReset(): Promise<string> {
    return "reset"
  }
}

let setup: TestRendererSetup | undefined

afterEach(() => {
  setup?.renderer.destroy()
  setup = undefined
})

describe("catalog filtering", () => {
  const skills = [
    makeSkill("academic-paper", "academic-pipelines", true, false),
    makeSkill("atac-seq", "single-cell-omics", false, false),
    makeSkill("playwright", "software-dev", true, true),
  ]

  test("fuzzy search matches non-contiguous names", () => {
    expect(fuzzyScore("acppr", skills[0])).toBeNumber()
    expect(fuzzyScore("zzzz", skills[0])).toBeNull()
  })

  test("combines status and category filters", () => {
    expect(filterSkills(skills, "", "mixed", "academic-pipelines").map((skill) => skill.key)).toEqual([
      "academic-paper",
    ])
    expect(filterSkills(skills, "", "codex:off", "all").map((skill) => skill.key)).toEqual([
      "academic-paper",
      "atac-seq",
    ])
  })
})

describe("OpenTUI interaction", () => {
  test("renders the table and mouse-clicks Claude independently", async () => {
    const catalog: Catalog = {
      skills: [makeSkill("alpha"), makeSkill("beta", "science", true, false)],
      categories: ["science", "software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 28 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const frame = setup.captureCharFrame()
    expect(frame).toContain("Skill Invocation Control")
    expect(frame).toContain("alpha")
    expect(frame).toContain("Claude")
    expect(frame).toContain("Codex")

    const cell = setup.renderer.root.findDescendantById("claude-alpha") as BoxRenderable
    expect(cell).toBeDefined()
    await setup.mockMouse.click(cell.screenX + 1, cell.screenY)
    await setup.waitFor(() => backend.calls.length === 1)

    expect(backend.calls).toEqual([{ keys: ["alpha"], product: "claude", enabled: false }])
  })

  test("scrolls a long skill list with the mouse wheel", async () => {
    const catalog: Catalog = {
      skills: Array.from({ length: 80 }, (_, index) => makeSkill(`skill-${String(index).padStart(2, "0")}`)),
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 24 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const list = setup.renderer.root.findDescendantById("skill-list") as ScrollBoxRenderable
    const firstRow = setup.renderer.root.findDescendantById("skill-skill-00") as BoxRenderable
    expect(list.scrollTop).toBe(0)
    expect(list.scrollHeight).toBeGreaterThan(list.height)
    for (let index = 0; index < 20; index++) {
      await setup.mockMouse.scroll(firstRow.screenX + 5, firstRow.screenY, "down")
    }
    await setup.renderOnce()

    expect(list.scrollTop).toBeGreaterThan(0)
  })

  test("keeps keyboard focus in sync with mouse wheel scrolling", async () => {
    const catalog: Catalog = {
      skills: [
        makeSkill("agent-browser"),
        makeSkill("ai-elements"),
        ...Array.from({ length: 78 }, (_, index) =>
          makeSkill(`skill-${String(index).padStart(2, "0")}`),
        ),
      ],
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 24 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const focusedRow = setup.renderer.root.findDescendantById("skill-agent-browser") as BoxRenderable
    const detail = setup.renderer.root.findDescendantById("detail-text") as TextRenderable

    expect(detail.content.chunks.map((chunk) => chunk.text).join("")).toStartWith("agent-browser")
    await setup.mockMouse.scroll(focusedRow.screenX + 5, focusedRow.screenY, "down")
    await setup.renderOnce()

    expect(detail.content.chunks.map((chunk) => chunk.text).join("")).toStartWith("ai-elements")

    const nextRow = setup.renderer.root.findDescendantById("skill-ai-elements") as BoxRenderable
    await setup.mockMouse.scroll(nextRow.screenX + 5, nextRow.screenY, "up")
    await setup.renderOnce()

    expect(detail.content.chunks.map((chunk) => chunk.text).join("")).toStartWith("agent-browser")
  })

  test("keeps pane widths stable and table columns aligned across detail lengths", async () => {
    const short = makeSkill("a-short-skill")
    short.description = "Short description."
    const long = makeSkill("z-long-skill")
    long.description = "Long detail content that wraps without changing pane geometry. ".repeat(20)
    const catalog: Catalog = {
      skills: [short, long],
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 28 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const listPanel = setup.renderer.root.findDescendantById("list-panel") as BoxRenderable
    const detailPanel = setup.renderer.root.findDescendantById("detail-panel") as BoxRenderable
    const initialWidths = [listPanel.width, detailPanel.width]

    expect(Math.abs(listPanel.width - detailPanel.width * 2)).toBeLessThanOrEqual(1)

    const frame = setup.captureCharFrame()
    expect(frame).not.toContain("▲")
    expect(frame).not.toContain("▼")
    expect(frame).toContain("[ ]")

    for (const [headerId, rowId] of [
      ["column-mark", "mark-a-short-skill"],
      ["column-name", "name-a-short-skill"],
      ["column-category", "category-a-short-skill"],
      ["column-claude", "claude-a-short-skill"],
      ["column-codex", "codex-a-short-skill"],
    ]) {
      const header = setup.renderer.root.findDescendantById(headerId)!
      const row = setup.renderer.root.findDescendantById(rowId)!
      expect([header.screenX, header.width]).toEqual([row.screenX, row.width])
    }

    const longRow = setup.renderer.root.findDescendantById("skill-z-long-skill") as BoxRenderable
    await setup.mockMouse.click(longRow.screenX + 1, longRow.screenY)
    setup.mockInput.pressKey("m")
    await setup.renderOnce()

    expect(setup.captureCharFrame()).toContain("[x]")
    expect([listPanel.width, detailPanel.width]).toEqual(initialWidths)
  })

  test("Ctrl-click cycles filters backward and Reset returns both to all", async () => {
    const catalog: Catalog = {
      skills: [makeSkill("alpha", "science"), makeSkill("beta", "software-dev", false, false)],
      categories: ["science", "software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 28 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const status = setup.renderer.root.findDescendantById("button-status-filter") as BoxRenderable
    const category = setup.renderer.root.findDescendantById("button-category-filter") as BoxRenderable

    await setup.mockMouse.click(status.screenX + 1, status.screenY)
    expect(setup.captureCharFrame()).toContain("Status: enabled")
    await setup.mockMouse.click(status.screenX + 1, status.screenY, 0, { modifiers: { ctrl: true } })
    expect(setup.captureCharFrame()).toContain("Status: all")

    await setup.mockMouse.click(status.screenX + 1, status.screenY)
    await setup.mockMouse.click(category.screenX + 1, category.screenY)
    expect(setup.captureCharFrame()).toContain("Category: science")

    const reset = setup.renderer.root.findDescendantById("button-reset-filters") as BoxRenderable
    expect(reset).toBeDefined()
    await setup.mockMouse.click(reset.screenX + 1, reset.screenY)

    const resetFrame = setup.captureCharFrame()
    expect(resetFrame).toContain("Status: all")
    expect(resetFrame).toContain("Category: all")
  })

  test("marks rows with M and normalizes a mixed Claude batch", async () => {
    const catalog: Catalog = {
      skills: [
        makeSkill("alpha", "software-dev", true, true),
        makeSkill("beta", "science", false, true),
      ],
      categories: ["science", "software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 28 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    setup.mockInput.pressEnter()
    setup.mockInput.pressKey("m")
    setup.mockInput.pressArrow("down")
    setup.mockInput.pressKey("m")
    setup.mockInput.pressKey("c")
    await setup.waitFor(() => backend.calls.length === 1)

    expect(backend.calls).toEqual([
      { keys: ["alpha", "beta"], product: "claude", enabled: true },
    ])
  })

  test("normalizes a fully enabled marked group off for both products", async () => {
    const catalog: Catalog = {
      skills: [makeSkill("alpha"), makeSkill("beta")],
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 28 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    setup.mockInput.pressEnter()
    setup.mockInput.pressKey("m")
    setup.mockInput.pressArrow("down")
    setup.mockInput.pressKey("m")
    setup.mockInput.pressKey(" ")
    await setup.waitFor(() => backend.calls.length === 1)

    expect(backend.calls).toEqual([
      { keys: ["alpha", "beta"], product: "both", enabled: false },
    ])
  })

  test("normalizes a mixed Codex batch on", async () => {
    const catalog: Catalog = {
      skills: [
        makeSkill("alpha", "software-dev", true, true),
        makeSkill("beta", "software-dev", true, false),
      ],
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 28 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    setup.mockInput.pressEnter()
    setup.mockInput.pressKey("m")
    setup.mockInput.pressArrow("down")
    setup.mockInput.pressKey("m")
    setup.mockInput.pressKey("x")
    await setup.waitFor(() => backend.calls.length === 1)

    expect(backend.calls).toEqual([
      { keys: ["alpha", "beta"], product: "codex", enabled: true },
    ])
  })

  test("drops marks hidden by a filter before batch toggling", async () => {
    const catalog: Catalog = {
      skills: [makeSkill("alpha"), makeSkill("beta", "software-dev", false, false)],
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 28 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    setup.mockInput.pressEnter()
    setup.mockInput.pressKey("m")
    setup.mockInput.pressArrow("down")
    setup.mockInput.pressKey("m")
    setup.mockInput.pressKey("f")
    setup.mockInput.pressKey("c")
    await setup.waitFor(() => backend.calls.length === 1)

    expect(backend.calls).toEqual([
      { keys: ["alpha"], product: "claude", enabled: false },
    ])
  })

  test("clicking a row does not let the scrollbox swallow movement keys", async () => {
    const catalog: Catalog = {
      skills: Array.from({ length: 80 }, (_, index) => makeSkill(`skill-${String(index).padStart(2, "0")}`)),
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 24 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const list = setup.renderer.root.findDescendantById("skill-list") as ScrollBoxRenderable
    const firstRow = setup.renderer.root.findDescendantById("skill-skill-00") as BoxRenderable
    await setup.mockMouse.click(firstRow.screenX + 8, firstRow.screenY)
    await setup.renderOnce()

    // A focused scrollbox would consume ↓ and scroll on its own; the second
    // row is already visible, so selecting it must not scroll at all.
    setup.mockInput.pressArrow("down")
    await setup.renderOnce()
    expect(list.scrollTop).toBe(0)
  })

  test("page down moves the selection and keeps it visible", async () => {
    const catalog: Catalog = {
      skills: Array.from({ length: 80 }, (_, index) => makeSkill(`skill-${String(index).padStart(2, "0")}`)),
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 24 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const list = setup.renderer.root.findDescendantById("skill-list") as ScrollBoxRenderable
    const firstRow = setup.renderer.root.findDescendantById("skill-skill-00") as BoxRenderable
    await setup.mockMouse.click(firstRow.screenX + 8, firstRow.screenY)
    await setup.renderOnce()

    setup.mockInput.pressKey("\u001b[6~")
    await setup.renderOnce()
    setup.mockInput.pressKey("\u001b[6~")
    await setup.renderOnce()

    const detail = setup.renderer.root.findDescendantById("detail-text") as TextRenderable
    expect(detail.content.chunks.map((chunk) => chunk.text).join("")).toStartWith("skill-20")

    const selected = setup.renderer.root.findDescendantById("skill-skill-20") as BoxRenderable
    const viewport = list.viewport
    expect(selected.y).toBeGreaterThanOrEqual(viewport.y)
    expect(selected.y).toBeLessThan(viewport.y + viewport.height)
  })

  test("marking with M keeps the scroll position stable", async () => {
    const catalog: Catalog = {
      skills: Array.from({ length: 80 }, (_, index) => makeSkill(`skill-${String(index).padStart(2, "0")}`)),
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 24 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const list = setup.renderer.root.findDescendantById("skill-list") as ScrollBoxRenderable
    const firstRow = setup.renderer.root.findDescendantById("skill-skill-00") as BoxRenderable
    setup.mockInput.pressEnter()
    for (let index = 0; index < 30; index++) {
      await setup.mockMouse.scroll(firstRow.screenX + 5, firstRow.screenY + 3, "down")
    }
    await setup.renderOnce()
    const before = list.scrollTop
    expect(before).toBeGreaterThan(0)

    setup.mockInput.pressKey("m")
    await setup.renderOnce()
    expect(list.scrollTop).toBe(before)
    expect(setup.captureCharFrame()).toContain("[x]")
  })

  test("toggling a product keeps the scroll position stable", async () => {
    const catalog: Catalog = {
      skills: Array.from({ length: 80 }, (_, index) => makeSkill(`skill-${String(index).padStart(2, "0")}`)),
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 24 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const list = setup.renderer.root.findDescendantById("skill-list") as ScrollBoxRenderable
    const firstRow = setup.renderer.root.findDescendantById("skill-skill-00") as BoxRenderable
    setup.mockInput.pressEnter()
    for (let index = 0; index < 30; index++) {
      await setup.mockMouse.scroll(firstRow.screenX + 5, firstRow.screenY + 3, "down")
    }
    await setup.renderOnce()
    const before = list.scrollTop
    expect(before).toBeGreaterThan(0)

    setup.mockInput.pressKey("c")
    await setup.waitFor(() => backend.calls.length === 1)
    await setup.renderOnce()
    expect(list.scrollTop).toBe(before)
  })

  test("drags the scrollbar thumb with the mouse", async () => {
    const catalog: Catalog = {
      skills: Array.from({ length: 80 }, (_, index) => makeSkill(`skill-${String(index).padStart(2, "0")}`)),
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 24 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const list = setup.renderer.root.findDescendantById("skill-list") as ScrollBoxRenderable
    const slider = list.verticalScrollBar.slider
    const thumb = (slider as unknown as { getThumbRect(): { x: number; y: number } }).getThumbRect()
    expect(list.scrollTop).toBe(0)

    await setup.mockMouse.pressDown(thumb.x, thumb.y)
    await setup.mockMouse.emitMouseEvent("drag", thumb.x, thumb.y + 2)
    await setup.mockMouse.release(thumb.x, thumb.y + 2)
    await setup.renderOnce()
    expect(list.scrollTop).toBeGreaterThan(0)
  })

  test("scrollbar drag keeps following when the pointer drifts off the column", async () => {
    const catalog: Catalog = {
      skills: Array.from({ length: 80 }, (_, index) => makeSkill(`skill-${String(index).padStart(2, "0")}`)),
      categories: ["software-dev"],
    }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 24 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    const list = setup.renderer.root.findDescendantById("skill-list") as ScrollBoxRenderable
    const slider = list.verticalScrollBar.slider
    const thumb = (slider as unknown as { getThumbRect(): { x: number; y: number } }).getThumbRect()

    await setup.mockMouse.pressDown(thumb.x, thumb.y)
    // pointer immediately drifts off the 1-cell scrollbar column, as real
    // mice do; the drag must keep driving the thumb anyway
    await setup.mockMouse.emitMouseEvent("drag", thumb.x - 4, thumb.y + 2)
    await setup.mockMouse.emitMouseEvent("drag", thumb.x - 4, thumb.y + 4)
    await setup.mockMouse.release(thumb.x - 4, thumb.y + 4)
    await setup.renderOnce()
    expect(list.scrollTop).toBeGreaterThan(0)
  })

  test("does not mark skills with catalog errors", async () => {
    const broken = makeSkill("broken")
    broken.claude_enabled = null
    broken.codex_enabled = null
    broken.state = "error"
    broken.error = "invalid metadata"
    const catalog: Catalog = { skills: [broken], categories: ["software-dev"] }
    const backend = new FakeBackend(catalog)
    setup = await createTestRenderer({ width: 140, height: 28 })
    new SkillToggleApp(setup.renderer, backend, await backend.catalog())
    await setup.renderOnce()

    setup.mockInput.pressEnter()
    setup.mockInput.pressKey("m")
    await setup.renderOnce()

    expect(setup.captureCharFrame()).toContain("0 marked")
    expect(backend.calls).toEqual([])
  })
})
