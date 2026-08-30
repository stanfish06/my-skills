import { resolve } from "node:path";
import type { SkillDef, Task } from "./types.ts";

export const EVAL_DIR = resolve(import.meta.dir, "..");
export const REPO_DIR = resolve(EVAL_DIR, "..");

export const SKILLS: SkillDef[] = [
  { id: "zz-prefix", dir: resolve(EVAL_DIR, "control/zz-prefix"), injection: "prose" },
  { id: "modern-typescript", dir: resolve(REPO_DIR, "skills/modern-typescript"), injection: "prose" },
  { id: "use-modern-go", dir: resolve(REPO_DIR, "skills/use-modern-go"), injection: "tool", goVersion: "1.27" },
];

const TASK_IDS = ["ts-settings-parser", "go-batch-processor"] as const;

export async function loadTasks(): Promise<Map<string, Task>> {
  const out = new Map<string, Task>();
  for (const id of TASK_IDS) {
    const mod = await import(resolve(EVAL_DIR, `tasks/${id}/task.ts`));
    out.set(id, mod.task as Task);
  }
  return out;
}

export type RunConfig = {
  id: string;
  models: string[];
  reps: number;
  /** Reasoning tokens count against this, so it must clear the thinking
   *  budget or generations come back truncated and empty. */
  maxOutputTokens: number;
  /** One skill at a time — no combinatorial skill interaction in v0. */
  pairs: { skill: string; task: string }[];
};

const PAIRS = [
  { skill: "zz-prefix", task: "ts-settings-parser" },
  { skill: "modern-typescript", task: "ts-settings-parser" },
  { skill: "use-modern-go", task: "go-batch-processor" },
];

export const CONFIGS: Record<string, RunConfig> = {
  smoke: { id: "smoke", models: ["deepseek/deepseek-v4-flash"], reps: 3, maxOutputTokens: 32000, pairs: PAIRS },
  full: {
    id: "full",
    models: [
      "deepseek/deepseek-v4-flash",
      "openai/gpt-5.4",
      "anthropic/claude-sonnet-5",
      "google/gemini-3.1-flash",
    ],
    reps: 5,
    maxOutputTokens: 32000,
    pairs: PAIRS,
  },
};

/** Provenance: a skill's content and the guidelines CLI both drift under us.
 *  Recording both versions is what makes an old run interpretable later. */
export async function provenance(): Promise<Record<string, string>> {
  const out: Record<string, string> = {};
  try {
    const lock = await Bun.file(resolve(REPO_DIR, ".skill-lock.json")).json();
    for (const s of SKILLS) {
      const hash = lock?.skills?.[s.id]?.skillFolderHash;
      if (hash) out[`skill:${s.id}`] = hash;
    }
  } catch {}
  try {
    out["go-modern-guidelines"] = (
      await Bun.file(resolve(REPO_DIR, "skills/use-modern-go/scripts/VERSION")).text()
    ).trim();
  } catch {}
  return out;
}
