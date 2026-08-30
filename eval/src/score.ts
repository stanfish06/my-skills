import { mkdir, rm, cp } from "node:fs/promises";
import { existsSync } from "node:fs";
import { resolve } from "node:path";
import { EVAL_DIR } from "./config.ts";
import type { Task, Trait, TraitResult, BenchResult } from "./types.ts";

/** Comment-stripped source. Keeps string literals, so a forbidden token quoted
 *  inside a string still counts — rare enough to accept in v0. */
export function stripComments(code: string): string {
  return code.replace(/\/\*[\s\S]*?\*\//g, " ").replace(/(^|[^:])\/\/[^\n]*/g, "$1");
}

/** Model-generated code is compiled and executed here, so it must not inherit
 *  the evaluator's environment. AI_GATEWAY_API_KEY in particular would
 *  otherwise be readable by every solution the harness runs. GOPROXY=off keeps
 *  a generated import from reaching the network: tasks are stdlib-only, so a
 *  module fetch is a task violation, not a dependency. */
const SANDBOX_ENV: Record<string, string> = {
  PATH: process.env.PATH ?? "",
  HOME: process.env.HOME ?? "",
  TMPDIR: process.env.TMPDIR ?? "/tmp",
  LANG: process.env.LANG ?? "C.UTF-8",
  GOPROXY: "off",
  GOTOOLCHAIN: "local",
  GOFLAGS: "-mod=mod",
};

async function run(cmd: string[], cwd: string, ms = 60_000) {
  const proc = Bun.spawn(cmd, {
    cwd,
    env: SANDBOX_ENV,
    stdout: "pipe",
    stderr: "pipe",
    signal: AbortSignal.timeout(ms),
  });
  const [stdout, stderr] = await Promise.all([
    new Response(proc.stdout).text(),
    new Response(proc.stderr).text(),
  ]);
  const code = await proc.exited;
  return { code, out: stdout + stderr };
}

let goBin: string | null = null;
async function go(): Promise<string> {
  if (goBin) return goBin;
  if ((await run(["go", "version"], EVAL_DIR, 10_000).catch(() => ({ code: 1 }))).code === 0) {
    goBin = "go";
  } else {
    const r = await run(["mise", "which", "go"], EVAL_DIR, 10_000);
    goBin = r.code === 0 ? r.out.trim() : "go";
  }
  return goBin;
}

let sgAvailable: boolean | null = null;

async function matches(trait: Trait, code: string, lang: Task["lang"], dir: string): Promise<boolean> {
  const src = stripComments(code);
  if (trait.kind === "regex") return new RegExp(trait.pattern, "m").test(src);

  if (sgAvailable === null) {
    sgAvailable = (await run(["ast-grep", "--version"], EVAL_DIR, 10_000).catch(() => ({ code: 1 })))
      .code === 0;
  }
  if (!sgAvailable) throw new Error(`trait ${trait.id} needs ast-grep on PATH`);
  await mkdir(dir, { recursive: true });
  const file = resolve(dir, `probe-${trait.id}.${lang}`);
  await Bun.write(file, src);
  const r = await run(["ast-grep", "run", "-p", trait.pattern, "-l", lang, file, "--json=compact"], dir);
  return r.code === 0 && r.out.trim() !== "[]" && r.out.trim() !== "";
}

export async function scoreTrait(
  trait: Trait,
  code: string,
  lang: Task["lang"],
  scratch = resolve(EVAL_DIR, ".cache/sg"),
): Promise<TraitResult> {
  const m = await matches(trait, code, lang, scratch);
  return {
    id: trait.id,
    matched: m,
    satisfied: trait.polarity === "require" ? m : !m,
    prescribedBy: trait.prescribedBy,
  };
}

/** Refuse to score until every pattern classifies its own fixtures correctly.
 *  A brittle pattern must fail loudly at startup, not silently at scoring. */
export async function verifyTraits(tasks: Map<string, Task>): Promise<string[]> {
  const problems: string[] = [];
  for (const task of tasks.values()) {
    for (const trait of task.traits) {
      const ok = await scoreTrait(trait, trait.fixture.satisfies, task.lang);
      const bad = await scoreTrait(trait, trait.fixture.violates, task.lang);
      if (!ok.satisfied) problems.push(`${task.id}/${trait.id}: fixture.satisfies scored as violated`);
      if (bad.satisfied) problems.push(`${task.id}/${trait.id}: fixture.violates scored as satisfied`);
    }
  }
  return problems;
}

const taskDir = (id: string) => resolve(EVAL_DIR, "tasks", id);

/** Gates run before traits are scored. Compiling is not enough: a module can
 *  declare the idioms a rubric looks for without implementing the task, so
 *  every task also runs harness-owned behaviour checks. */
export async function gate(
  task: Task,
  code: string,
  workRoot: string,
  key: string,
): Promise<{ pass: boolean; detail: string; dir: string }> {
  const dir = resolve(workRoot, key);
  await rm(dir, { recursive: true, force: true });
  await mkdir(dir, { recursive: true });

  if (task.lang === "ts") {
    await Bun.write(resolve(dir, "solution.ts"), code);
    const tsc = resolve(EVAL_DIR, "node_modules/.bin/tsc");
    const t = await run(
      [tsc, "--noEmit", "--strict", "--noUncheckedIndexedAccess", "--target", "es2022",
       "--lib", "es2023", "--skipLibCheck", "--moduleDetection", "force", "solution.ts"],
      dir,
    );
    if (t.code !== 0) return { pass: false, detail: `tsc: ${t.out.slice(0, 600)}`, dir };

    const spec = resolve(taskDir(task.id), "spec.ts");
    if (task.spec && existsSync(spec)) {
      await cp(spec, resolve(dir, "spec.ts"));
      const s = await run([process.execPath, "spec.ts"], dir, 60_000);
      if (s.code !== 0) return { pass: false, detail: `spec: ${s.out.slice(0, 600)}`, dir };
      return { pass: true, detail: "tsc + spec ok", dir };
    }
    return { pass: true, detail: "tsc ok", dir };
  }

  await Bun.write(resolve(dir, "go.mod"), "module evaltask\n\ngo 1.27\n");
  await Bun.write(resolve(dir, "solution.go"), code);
  await cp(resolve(taskDir(task.id), "bench_test.go"), resolve(dir, "bench_test.go"));

  const g = await go();
  for (const [stage, cmd] of [
    ["build", [g, "build", "./..."]],
    ["vet", [g, "vet", "./..."]],
    ["test", [g, "test", "-run", "Test", "-count=1", "-timeout", "30s", "./..."]],
  ] as const) {
    const r = await run([...cmd], dir, 120_000);
    if (r.code !== 0) return { pass: false, detail: `go ${stage}: ${r.out.slice(0, 600)}`, dir };
  }
  return { pass: true, detail: "go build+vet+test ok", dir };
}

const BENCH_LINE =
  /^Benchmark\S*\s+\d+\s+([\d.]+)\s+ns\/op\s+([\d.]+)\s+B\/op\s+([\d.]+)\s+allocs\/op/m;

/** A benchmark that panics, deadlocks or times out must be reported, not
 *  silently dropped from the medians. */
export async function bench(dir: string): Promise<{ result: BenchResult | null; error: string | null }> {
  const g = await go();
  const r = await run(
    [g, "test", "-run", "^$", "-bench=.", "-benchmem", "-count=1", "-timeout", "120s", "./..."],
    dir,
    180_000,
  ).catch((e) => ({ code: 124, out: e instanceof Error ? e.message : String(e) }));

  if (r.code !== 0) return { result: null, error: `go bench exit ${r.code}: ${r.out.slice(0, 400)}` };
  const m = r.out.match(BENCH_LINE);
  if (!m) return { result: null, error: `no benchmark line in output: ${r.out.slice(0, 400)}` };
  return {
    result: { nsPerOp: Number(m[1]), bytesPerOp: Number(m[2]), allocsPerOp: Number(m[3]) },
    error: null,
  };
}
