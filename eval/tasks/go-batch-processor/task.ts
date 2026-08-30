import type { Task } from "../../src/types.ts";

const MG = ["use-modern-go"];

export const task: Task = {
  id: "go-batch-processor",
  lang: "go",
  prompt: await Bun.file(new URL("prompt.md", import.meta.url)).text(),
  bench: true,
  traits: [
    {
      id: "go-wg-go",
      polarity: "require",
      kind: "regex",
      pattern: String.raw`\bwg\.Go\(|\b\w+\.Go\(func\b`,
      prescribedBy: MG,
      note: "guideline sync_waitgroup_go (Since Go 1.25)",
      fixture: {
        satisfies: `var wg sync.WaitGroup\nwg.Go(func() { work() })`,
        violates: `var wg sync.WaitGroup\nwg.Add(1)\ngo func() { defer wg.Done(); work() }()`,
      },
    },
    {
      id: "go-no-wg-add",
      polarity: "forbid",
      kind: "regex",
      pattern: String.raw`\.Add\(1\)|\bdefer\s+\w+\.Done\(\)`,
      prescribedBy: MG,
      note: "the Before half of sync_waitgroup_go",
      fixture: {
        satisfies: `wg.Go(func() { work() })`,
        violates: `wg.Add(1)\ngo func() { defer wg.Done(); work() }()`,
      },
    },
    {
      id: "go-errors-join",
      polarity: "require",
      kind: "regex",
      pattern: String.raw`\berrors\.Join\(`,
      prescribedBy: MG,
      note: "guideline errors_join (Since Go 1.20)",
      fixture: {
        satisfies: `return results, errors.Join(errs...)`,
        violates: `return results, fmt.Errorf("%d batches failed", len(errs))`,
      },
    },
    {
      id: "go-min-builtin",
      polarity: "require",
      kind: "regex",
      pattern: String.raw`(?<![.\w])min\(`,
      prescribedBy: MG,
      note: "guideline min_max (Since Go 1.21)",
      fixture: {
        satisfies: `end := min(i+batchSize, len(items))`,
        violates: `end := i + batchSize\nif end > len(items) { end = len(items) }`,
      },
    },
    {
      id: "go-no-handrolled-min",
      polarity: "forbid",
      kind: "regex",
      pattern: String.raw`func\s+min\s*\(`,
      prescribedBy: MG,
      note: "the Before half of min_max",
      fixture: {
        satisfies: `end := min(a, b)`,
        violates: `func min(a, b int) int { if a < b { return a }; return b }`,
      },
    },
    {
      id: "go-no-panic",
      polarity: "forbid",
      kind: "regex",
      pattern: String.raw`\bpanic\(`,
      prescribedBy: [],
      note: "blind quality trait — catches collateral damage",
      fixture: {
        satisfies: `return nil, errors.New("bad batch size")`,
        violates: `panic("bad batch size")`,
      },
    },
    {
      id: "go-no-sleep",
      polarity: "forbid",
      kind: "regex",
      pattern: String.raw`\btime\.Sleep\(`,
      prescribedBy: [],
      note: "blind quality trait — sleeping is not synchronisation",
      fixture: {
        satisfies: `wg.Wait()`,
        violates: `time.Sleep(100 * time.Millisecond)`,
      },
    },
  ],
};
