import { mkdir, rm } from "node:fs/promises";
import { resolve } from "node:path";
import { EVAL_DIR, SKILLS, loadTasks, provenance, type RunConfig } from "./config.ts";
import { buildSystem, generate } from "./inject.ts";
import { gate, bench, scoreTrait, verifyTraits } from "./score.ts";
import type { Arm, Cell, SkillDef, Task } from "./types.ts";

const CACHE = resolve(EVAL_DIR, ".cache/gen");

function hash(parts: string[]): string {
  const h = new Bun.CryptoHasher("sha256");
  for (const p of parts) h.update(p + "\0");
  return h.digest("hex").slice(0, 16);
}

type Plan = { task: Task; skill: SkillDef | null; arm: Arm; rep: number; model: string };

async function poolMap<T, R>(items: T[], limit: number, fn: (t: T, i: number) => Promise<R>): Promise<R[]> {
  const out = new Array<R>(items.length);
  let next = 0;
  await Promise.all(
    Array.from({ length: Math.min(limit, items.length) }, async () => {
      for (let i = next++; i < items.length; i = next++) out[i] = await fn(items[i]!, i);
    }),
  );
  return out;
}

export async function runEval(cfg: RunConfig, opts: { concurrency: number }) {
  const tasks = await loadTasks();

  const problems = await verifyTraits(tasks);
  if (problems.length) {
    throw new Error(`trait self-test failed — refusing to score:\n${problems.join("\n")}`);
  }
  console.log(`trait self-test: ok (${[...tasks.values()].reduce((n, t) => n + t.traits.length, 0)} traits)`);

  const skillById = new Map(SKILLS.map((s) => [s.id, s]));
  const usedTasks = [...new Set(cfg.pairs.map((p) => p.task))];

  const plans: Plan[] = [];
  for (const model of cfg.models) {
    for (let rep = 0; rep < cfg.reps; rep++) {
      // Baselines are per (model, task, rep) — shared by every skill on that task.
      for (const tid of usedTasks) plans.push({ task: tasks.get(tid)!, skill: null, arm: "baseline", rep, model });
      for (const p of cfg.pairs) {
        plans.push({ task: tasks.get(p.task)!, skill: skillById.get(p.skill)!, arm: "skill", rep, model });
      }
    }
  }

  const runId = `${new Date().toISOString().replace(/[:.]/g, "-").slice(0, 19)}-${cfg.id}`;
  const runDir = resolve(EVAL_DIR, "runs", runId);
  await mkdir(runDir, { recursive: true });
  await mkdir(CACHE, { recursive: true });

  console.log(`run ${runId}: ${plans.length} cells (${cfg.models.length} models x ${cfg.reps} reps)`);

  let done = 0;
  const cells = await poolMap(plans, opts.concurrency, async (p) => {
    const system = await buildSystem(p.arm, p.skill);
    const key = hash([p.model, system, p.task.prompt, String(p.rep), p.skill?.injection ?? "none"]);
    const cacheFile = resolve(CACHE, `${key}.json`);

    let gen = await Bun.file(cacheFile)
      .json()
      .catch(() => null);
    const cached = gen !== null;
    const t0 = performance.now();
    if (!gen) {
      gen = await generate({
        model: p.model, system, task: p.task, skill: p.skill, arm: p.arm,
        maxOutputTokens: cfg.maxOutputTokens,
      });
      // Never cache a truncated or empty generation — it would replay forever.
      if (!gen.error && gen.code && gen.finishReason !== "length") {
        await Bun.write(cacheFile, JSON.stringify(gen));
      }
    }
    const ms = Math.round(performance.now() - t0);

    const cell: Cell = {
      runId,
      key,
      model: p.model,
      taskId: p.task.id,
      skillId: p.skill?.id ?? null,
      arm: p.arm,
      rep: p.rep,
      system,
      prompt: p.task.prompt,
      code: gen.code,
      raw: gen.raw,
      toolCalls: gen.toolCalls,
      steps: gen.steps,
      finishReason: gen.finishReason,
      outcome: gen.error ? "error" : gen.code ? "gate-fail" : "empty",
      usage: gen.usage,
      ms,
      cached,
      error: gen.error,
      gate: null,
      traits: [],
      bench: null,
    };

    if (!gen.error && gen.code) {
      const g = await gate(p.task, gen.code, key);
      cell.gate = { pass: g.pass, detail: g.detail };
      cell.traits = await Promise.all(p.task.traits.map((t) => scoreTrait(t, gen.code, p.task.lang)));
      cell.outcome = g.pass ? "ok" : "gate-fail";
      if (g.pass && p.task.bench) cell.bench = await bench(g.dir);
      await rm(g.dir, { recursive: true, force: true });
    }

    done++;
    const tag = `${p.model.split("/")[1]} ${p.task.id} ${p.arm}${p.skill ? `:${p.skill.id}` : ""} r${p.rep}`;
    const mark = { ok: "ok  ", "gate-fail": "gate", empty: "trunc", error: "ERR " }[cell.outcome];
    console.log(`  [${String(done).padStart(3)}/${plans.length}] ${mark} ${tag}${cached ? " (cached)" : ""}`);
    return cell;
  });

  const manifest = {
    runId,
    config: cfg,
    provenance: await provenance(),
    startedAt: new Date().toISOString(),
    cells: cells.length,
  };
  await Bun.write(resolve(runDir, "manifest.json"), JSON.stringify(manifest, null, 2));
  await Bun.write(resolve(runDir, "cells.jsonl"), cells.map((c) => JSON.stringify(c)).join("\n") + "\n");
  return { runId, runDir, cells, manifest };
}

export async function loadRun(runId: string) {
  const runDir = resolve(EVAL_DIR, "runs", runId);
  const manifest = await Bun.file(resolve(runDir, "manifest.json")).json();
  const text = await Bun.file(resolve(runDir, "cells.jsonl")).text();
  const cells = text.trim().split("\n").filter(Boolean).map((l) => JSON.parse(l) as Cell);
  return { runId, runDir, cells, manifest };
}

/** Offline re-score: reuse the saved generations, run gates and traits again.
 *  No API calls, so scorer changes are testable for free. */
export async function replayRun(runId: string) {
  const { runDir, cells, manifest } = await loadRun(runId);
  const tasks = await loadTasks();
  const problems = await verifyTraits(tasks);
  if (problems.length) throw new Error(`trait self-test failed:\n${problems.join("\n")}`);

  for (const cell of cells) {
    const task = tasks.get(cell.taskId);
    if (!task || cell.error || !cell.code) continue;
    const g = await gate(task, cell.code, cell.key);
    cell.gate = { pass: g.pass, detail: g.detail };
    cell.outcome = g.pass ? "ok" : "gate-fail";
    cell.traits = await Promise.all(task.traits.map((t) => scoreTrait(t, cell.code, task.lang)));
    cell.bench = g.pass && task.bench ? await bench(g.dir) : null;
    await rm(g.dir, { recursive: true, force: true });
  }
  await Bun.write(resolve(runDir, "cells.jsonl"), cells.map((c) => JSON.stringify(c)).join("\n") + "\n");
  return { runId, runDir, cells, manifest };
}
