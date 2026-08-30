import { resolve } from "node:path";
import { SKILLS } from "./config.ts";
import type { Cell } from "./types.ts";

const pct = (n: number) => (Number.isFinite(n) ? (n * 100).toFixed(1) : "  -  ");

/** Averages both middle samples for even-sized inputs. */
const med = (xs: number[]) => {
  if (!xs.length) return NaN;
  const s = [...xs].sort((a, b) => a - b);
  const mid = Math.floor(s.length / 2);
  return s.length % 2 ? s[mid]! : (s[mid - 1]! + s[mid]!) / 2;
};

/** Only cells that passed the gate contribute. A solution that fails to
 *  compile or fails its behaviour check can still contain the expected tokens,
 *  and scoring it would let broken code carry the delta. */
function subsetScore(cells: Cell[], skillId: string | null): number {
  const per = cells
    .filter((c) => c.outcome === "ok")
    .map((c) => {
      const rel = skillId ? c.traits.filter((t) => t.prescribedBy.includes(skillId)) : c.traits;
      return rel.length ? rel.filter((t) => t.satisfied).length / rel.length : NaN;
    })
    .filter(Number.isFinite);
  return per.length ? per.reduce((a, b) => a + b, 0) / per.length : NaN;
}

function benchMed(cells: Cell[]) {
  const b = cells.map((c) => c.bench).filter((x): x is NonNullable<typeof x> => !!x);
  if (!b.length) return null;
  return { ns: med(b.map((x) => x.nsPerOp)), bytes: med(b.map((x) => x.bytesPerOp)), allocs: med(b.map((x) => x.allocsPerOp)) };
}

const toolInjected = new Set(SKILLS.filter((s) => s.injection === "tool").map((s) => s.id));

export function buildRows(cells: Cell[], pairs: { skill: string; task: string }[]) {
  const rows = [];
  const models = [...new Set(cells.map((c) => c.model))];
  for (const model of models) {
    for (const p of pairs) {
      const base = cells.filter((c) => c.model === model && c.taskId === p.task && c.arm === "baseline");
      const skill = cells.filter(
        (c) => c.model === model && c.taskId === p.task && c.arm === "skill" && c.skillId === p.skill,
      );
      if (!base.length && !skill.length) continue;
      const mk = (cs: Cell[]) => {
        const ok = cs.filter((c) => c.outcome === "ok");
        return {
          n: cs.length,
          ok: ok.length,
          gated: cs.filter((c) => c.outcome === "ok" || c.outcome === "gate-fail").length,
          empty: cs.filter((c) => c.outcome === "empty").length,
          errors: cs.filter((c) => c.outcome === "error").length,
          benchFailures: cs.filter((c) => c.benchError).length,
          subset: subsetScore(cs, p.skill),
          full: subsetScore(cs, null),
          bench: benchMed(ok),
          reasoning: med(cs.map((c) => Number((c.usage as any)?.reasoningTokens ?? NaN)).filter(Number.isFinite)),
          toolCalls: med(cs.map((c) => c.toolCalls.length)),
        };
      };
      rows.push({ model, task: p.task, skill: p.skill, baseline: mk(base), withSkill: mk(skill) });
    }
  }
  return rows;
}

export function renderReport(rows: ReturnType<typeof buildRows>, manifest: any): string {
  const L: string[] = [];
  L.push(`# Skill eval — ${manifest.runId}`);
  L.push("");
  L.push(`config: ${manifest.config.id} | models: ${manifest.config.models.length} | reps: ${manifest.config.reps} | cells: ${manifest.cells}`);
  L.push(`provenance: ${Object.entries(manifest.provenance).map(([k, v]) => `${k}=${String(v).slice(0, 12)}`).join(" ")}`);
  L.push("");
  L.push("skill%  = traits this skill prescribes. full%  = whole rubric, incl. blind traits no skill asks for.");
  L.push("Percentages average only gate-passing cells. gate = passed / reached the gate.");
  L.push("trunc = hit the output cap. err = gateway or tool failure; both shrink the sample.");
  L.push("");

  const head = ["model", "task", "skill", "arm", "n", "gate", "trunc", "err", "skill%", "full%", "think"];
  const widths = [22, 20, 18, 8, 3, 6, 5, 3, 7, 7, 6];
  const line = (c: string[]) => c.map((v, i) => v.padEnd(widths[i]!)).join(" ").trimEnd();
  L.push("```");
  L.push(line(head));
  L.push(widths.map((w) => "-".repeat(w)).join(" "));
  for (const r of rows) {
    const m = r.model.split("/").pop()!;
    for (const [arm, s] of [["baseline", r.baseline], ["skill", r.withSkill]] as const) {
      L.push(line([
        arm === "baseline" ? m : "",
        arm === "baseline" ? r.task : "",
        arm === "baseline" ? "(none)" : r.skill,
        arm,
        String(s.n),
        `${s.ok}/${s.gated}`,
        String(s.empty),
        String(s.errors),
        pct(s.subset),
        pct(s.full),
        Number.isFinite(s.reasoning) ? String(Math.round(s.reasoning)) : "-",
      ]));
    }
    const sign = (x: number) => (Number.isFinite(x) ? `${x >= 0 ? "+" : ""}${x.toFixed(1)}` : "-");
    L.push(line(["", "", "", "delta", "", "", "", "",
      sign((r.withSkill.subset - r.baseline.subset) * 100),
      sign((r.withSkill.full - r.baseline.full) * 100), ""]));
    L.push("");
  }
  L.push("```");

  const benched = rows.filter((r) => r.baseline.bench || r.withSkill.bench || r.withSkill.benchFailures || r.baseline.benchFailures);
  if (benched.length) {
    L.push("");
    L.push("## go bench (median over gate-passing cells)");
    L.push("");
    L.push("```");
    L.push(line(["model", "task", "skill", "arm", "", "ns/op", "B/op", "allocs", "failed"]));
    for (const r of benched) {
      const m = r.model.split("/").pop()!;
      for (const [arm, s] of [["baseline", r.baseline], ["skill", r.withSkill]] as const) {
        const b = s.bench;
        L.push(line([
          arm === "baseline" ? m : "", arm === "baseline" ? r.task : "",
          arm === "baseline" ? "(none)" : r.skill, arm, "",
          b ? String(Math.round(b.ns)) : "-",
          b ? String(Math.round(b.bytes)) : "-",
          b ? String(Math.round(b.allocs)) : "-",
          String(s.benchFailures),
        ]));
      }
      L.push("");
    }
    L.push("```");
    L.push("ns/op is machine noise across runs; compare arms on B/op and allocs/op.");
  }

  // Every tool-injected skill is listed even at zero calls — a skill that never
  // invoked its own CLI is the routing failure this section exists to show.
  const tooled = rows.filter((r) => toolInjected.has(r.skill));
  if (tooled.length) {
    L.push("");
    L.push("## tool-injected skills — routing check");
    L.push("");
    for (const r of tooled) {
      const n = r.withSkill.toolCalls;
      const note = !Number.isFinite(n) || n === 0 ? "  <-- ROUTING FAILURE: never called its own CLI" : "";
      L.push(`- ${r.model} / ${r.skill}: median ${Number.isFinite(n) ? n : 0} tool calls per generation${note}`);
    }
  }
  return L.join("\n") + "\n";
}

export async function writeReport(runDir: string, cells: Cell[], manifest: any) {
  const rows = buildRows(cells, manifest.config.pairs);
  const md = renderReport(rows, manifest);
  await Bun.write(resolve(runDir, "report.md"), md);
  await Bun.write(resolve(runDir, "summary.json"), JSON.stringify({ runId: manifest.runId, rows }, null, 2));
  return md;
}
