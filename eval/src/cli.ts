import { CONFIGS, EVAL_DIR } from "./config.ts";
import { runEval, loadRun, replayRun } from "./run.ts";
import { writeReport } from "./report.ts";
import { readdir } from "node:fs/promises";
import { resolve } from "node:path";

const [cmd, ...rest] = process.argv.slice(2);
const flag = (name: string, dflt: string) => {
  const i = rest.indexOf(`--${name}`);
  return i >= 0 && rest[i + 1] ? rest[i + 1]! : dflt;
};
const positional: string[] = [];
for (let i = 0; i < rest.length; i++) {
  if (rest[i]!.startsWith("--")) { i++; continue; }
  positional.push(rest[i]!);
}

async function latestRun(): Promise<string> {
  const dir = resolve(EVAL_DIR, "runs");
  const entries = await readdir(dir).catch(() => [] as string[]);
  const sorted = entries.filter((e) => !e.startsWith(".")).sort();
  const last = sorted.at(-1);
  if (!last) throw new Error("no saved runs");
  return last;
}

switch (cmd) {
  case "run": {
    const name = flag("config", "smoke");
    const cfg = CONFIGS[name];
    if (!cfg) throw new Error(`unknown config "${name}" (have: ${Object.keys(CONFIGS).join(", ")})`);
    if (!process.env.AI_GATEWAY_API_KEY) throw new Error("AI_GATEWAY_API_KEY not set — run `mise run setup`");
    const { runDir, cells, manifest } = await runEval(cfg, { concurrency: Number(flag("concurrency", "4")) });
    console.log("\n" + (await writeReport(runDir, cells, manifest)));
    console.log(`saved: ${runDir}/{cells.jsonl,report.md,summary.json}`);
    break;
  }
  case "replay": {
    const id = positional[0] ?? (await latestRun());
    const { runDir, cells, manifest } = await replayRun(id);
    console.log("\n" + (await writeReport(runDir, cells, manifest)));
    console.log(`re-scored offline: ${runDir}`);
    break;
  }
  case "report": {
    const id = positional[0] ?? (await latestRun());
    const { runDir, cells, manifest } = await loadRun(id);
    console.log("\n" + (await writeReport(runDir, cells, manifest)));
    break;
  }
  case "runs": {
    const dir = resolve(EVAL_DIR, "runs");
    for (const e of (await readdir(dir).catch(() => [])).sort()) console.log(e);
    break;
  }
  default:
    console.log(`usage: bun run src/cli.ts <run|replay|report|runs> [--config smoke|full] [--concurrency N] [runId]`);
}
