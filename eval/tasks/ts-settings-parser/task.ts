import type { Task } from "../../src/types.ts";

const MT = ["modern-typescript"];
const ZZ = ["zz-prefix"];

export const task: Task = {
  id: "ts-settings-parser",
  lang: "ts",
  prompt: await Bun.file(new URL("prompt.md", import.meta.url)).text(),
  bench: false,
  traits: [
    {
      id: "ts-no-any",
      polarity: "forbid",
      kind: "regex",
      pattern: String.raw`:\s*any\b|\bas\s+any\b|<any>`,
      prescribedBy: MT,
      note: "modern-typescript: unknown at boundaries, never any",
      fixture: {
        satisfies: `export function f(x: unknown): string { return String(x); }`,
        violates: `export function f(x: any): string { return String(x); }`,
      },
    },
    {
      id: "ts-discriminated-union",
      polarity: "require",
      kind: "regex",
      pattern: String.raw`\b(kind|type|tag)\s*[:?]\s*["'\x60]`,
      prescribedBy: MT,
      note: "modern-typescript: tagged union as the state model",
      fixture: {
        satisfies: `type R = { kind: "ok"; v: number } | { kind: "err"; e: string };`,
        violates: `type R = { ok: boolean; v?: number; e?: string };`,
      },
    },
    {
      id: "ts-never-exhaustive",
      polarity: "require",
      kind: "regex",
      pattern: String.raw`:\s*never\b|\bnever\s*\)`,
      prescribedBy: MT,
      note: "modern-typescript: exhaustiveness via never",
      fixture: {
        satisfies: `function assertNever(x: never): never { throw new Error(String(x)); }`,
        violates: `function fallback(x: unknown): string { throw new Error(String(x)); }`,
      },
    },
    {
      id: "zz-prefix",
      polarity: "require",
      kind: "regex",
      pattern: String.raw`export\s+(function|const)\s+zz_`,
      prescribedBy: ZZ,
      note: "positive control: no model does this unprompted",
      fixture: {
        satisfies: `export function zz_parse(k: string) { return k; }`,
        violates: `export function parse(k: string) { return k; }`,
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
        satisfies: `export const render = (s: string) => s;`,
        violates: `export const render = (s: string) => { console.log(s); return s; };`,
      },
    },
    {
      id: "ts-exported-api",
      polarity: "require",
      kind: "regex",
      pattern: String.raw`export\s+(function|const)\s+\w+`,
      prescribedBy: [],
      note: "blind quality trait — the module actually exports something",
      fixture: {
        satisfies: `export function parse(k: string) { return k; }`,
        violates: `function parse(k: string) { return k; }`,
      },
    },
  ],
};
