import { z } from "zod";

/** Arm is a 3-value enum on purpose: `placebo` (length-matched filler) is
 *  wired but unused in v0, so adding it later is config, not a refactor. */
export const Arm = z.enum(["baseline", "placebo", "skill"]);
export type Arm = z.infer<typeof Arm>;

/** A trait is one checkable fact about the produced code.
 *  `prescribedBy` is the Q1 answer: [] means a blind quality trait that no
 *  skill under test asks for, so it catches collateral damage. */
export const Trait = z.object({
  id: z.string(),
  polarity: z.enum(["require", "forbid"]),
  kind: z.enum(["regex", "ast-grep"]),
  pattern: z.string(),
  prescribedBy: z.array(z.string()).default([]),
  note: z.string().optional(),
  /** Self-test. The harness refuses to score until every trait classifies
   *  both of these correctly — a bad pattern must fail loudly, not silently. */
  fixture: z.object({ satisfies: z.string(), violates: z.string() }),
});
export type Trait = z.infer<typeof Trait>;

export const Task = z.object({
  id: z.string(),
  lang: z.enum(["ts", "go"]),
  prompt: z.string(),
  traits: z.array(Trait),
  /** Go only: run the harness-owned benchmark after the build gate passes. */
  bench: z.boolean().default(false),
});
export type Task = z.infer<typeof Task>;

export const SkillDef = z.object({
  id: z.string(),
  dir: z.string(),
  /** prose = paste SKILL.md; tool = expose the skill's CLI as AI SDK tools.
   *  use-modern-go has zero rules in its SKILL.md, so pasting it measures
   *  nothing — it must be evaluated through its CLI. */
  injection: z.enum(["prose", "tool"]),
  goVersion: z.string().optional(),
});
export type SkillDef = z.infer<typeof SkillDef>;

export const TraitResult = z.object({
  id: z.string(),
  satisfied: z.boolean(),
  matched: z.boolean(),
  prescribedBy: z.array(z.string()),
});
export type TraitResult = z.infer<typeof TraitResult>;

export const BenchResult = z.object({
  nsPerOp: z.number(),
  bytesPerOp: z.number(),
  allocsPerOp: z.number(),
});
export type BenchResult = z.infer<typeof BenchResult>;

/** One generation + its scores. This is the unit written to gen.jsonl and is
 *  everything needed to re-score offline. */
export const Cell = z.object({
  runId: z.string(),
  key: z.string(),
  model: z.string(),
  taskId: z.string(),
  skillId: z.string().nullable(),
  arm: Arm,
  rep: z.number(),
  system: z.string(),
  prompt: z.string(),
  code: z.string(),
  raw: z.string(),
  toolCalls: z.array(z.object({ name: z.string(), input: z.unknown() })),
  steps: z.number(),
  finishReason: z.string().nullable(),
  /** Distinguishes "model produced nothing" from "code failed to compile" —
   *  conflating them would read as the skill breaking the code. */
  outcome: z.enum(["ok", "gate-fail", "empty", "error"]),
  usage: z.record(z.string(), z.unknown()).nullable(),
  ms: z.number(),
  cached: z.boolean(),
  error: z.string().nullable(),
  gate: z.object({ pass: z.boolean(), detail: z.string() }).nullable(),
  traits: z.array(TraitResult),
  bench: BenchResult.nullable(),
});
export type Cell = z.infer<typeof Cell>;
