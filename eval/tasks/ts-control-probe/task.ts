import type { Task } from "../../src/types.ts";

const ZZ = ["zz-prefix"];

/** Harness self-check, not a measurement of TypeScript quality.
 *
 *  The control lives on its own task because it renames exports, which would
 *  fight a behaviour check with fixed export names. So this task is gated by
 *  tsc alone and the prompt deliberately does not name its exports. */
export const task: Task = {
  id: "ts-control-probe",
  lang: "ts",
  prompt: await Bun.file(new URL("prompt.md", import.meta.url)).text(),
  bench: false,
  spec: false,
  traits: [
    {
      id: "zz-prefix-present",
      polarity: "require",
      kind: "regex",
      pattern: String.raw`export\s+(function|const)\s+zz_`,
      prescribedBy: ZZ,
      note: "positive control: no model does this unprompted",
      fixture: {
        satisfies: `export function zz_clamp(n: number) { return n; }`,
        violates: `export function clamp(n: number) { return n; }`,
      },
    },
    {
      id: "zz-prefix-complete",
      polarity: "forbid",
      kind: "regex",
      pattern: String.raw`export\s+(?:async\s+)?(?:function|const|let|var|class)\s+(?!zz_)\w+`,
      prescribedBy: ZZ,
      note: "paired with zz-prefix-present: one prefixed export is not adherence",
      fixture: {
        satisfies: `export function zz_clamp(n: number) { return n; }\nexport const zz_pi = 3;`,
        violates: `export function zz_clamp(n: number) { return n; }\nexport function titleCase(s: string) { return s; }`,
      },
    },
    {
      id: "ts-no-console",
      polarity: "forbid",
      kind: "regex",
      pattern: String.raw`\bconsole\.\w+\(`,
      prescribedBy: [],
      note: "blind quality trait — catches collateral damage",
      fixture: {
        satisfies: `export const zz_id = (s: string) => s;`,
        violates: `export const zz_id = (s: string) => { console.log(s); return s; };`,
      },
    },
  ],
};
