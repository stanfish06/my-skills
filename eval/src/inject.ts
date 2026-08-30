import { resolve } from "node:path";
import { generateText, tool, stepCountIs } from "ai";
import { z } from "zod";
import type { SkillDef, Task, Arm } from "./types.ts";

/** Identical across arms so the baseline generation is cache-shared by every
 *  skill paired with the same task. */
export const BASE_SYSTEM =
  "You are an expert software engineer. Produce production-quality code that " +
  "satisfies the request exactly. Return only the requested file's contents in " +
  "a single fenced code block, with no commentary before or after it.";

/** Bridges the skill's shell commands onto AI SDK tools without editing the
 *  skill body — the body is what is under test. */
const TOOL_BRIDGE =
  "\n\n---\n\nMechanism note: the CLI described above is exposed to you as the " +
  "tools `go_guidelines_list` and `go_guidelines_explain`. Call those tools " +
  "instead of shell commands. Everything else in the instructions applies " +
  "unchanged.";

export async function skillText(skill: SkillDef): Promise<string> {
  return await Bun.file(resolve(skill.dir, "SKILL.md")).text();
}

export async function buildSystem(arm: Arm, skill: SkillDef | null): Promise<string> {
  if (arm === "baseline" || !skill) return BASE_SYSTEM;
  const body = await skillText(skill);
  return `${BASE_SYSTEM}\n\n---\n\n${body}${skill.injection === "tool" ? TOOL_BRIDGE : ""}`;
}

async function runSkillCli(skillDir: string, args: string[]): Promise<string> {
  const proc = Bun.spawn(["mise", "exec", "--", "sh", "scripts/run-tool.sh", ...args], {
    cwd: skillDir,
    stdout: "pipe",
    stderr: "pipe",
    signal: AbortSignal.timeout(120_000),
  });
  const [out, err] = await Promise.all([
    new Response(proc.stdout).text(),
    new Response(proc.stderr).text(),
  ]);
  const code = await proc.exited;
  // Returning diagnostics as a successful tool result would let an install or
  // lookup failure be scored as a real skill-arm sample.
  if (code !== 0) {
    throw new Error(`skill CLI \`${args.join(" ")}\` exited ${code}: ${(err || out).slice(0, 400)}`);
  }
  return out.slice(0, 40_000);
}

function skillTools(skill: SkillDef, onFailure: (e: unknown) => void) {
  const version = skill.goVersion ?? "1.27";
  const guard = (fn: () => Promise<string>) => fn().catch((e) => { onFailure(e); throw e; });
  return {
    go_guidelines_list: tool({
      description:
        "List the modern Go guidelines that apply to a Go version. Returns one line per guideline, newest first. Read the whole list.",
      inputSchema: z.object({ goVersion: z.string().describe("e.g. 1.27") }),
      execute: async ({ goVersion }) => guard(() => runSkillCli(skill.dir, ["list", "--go-version", goVersion || version])),
    }),
    go_guidelines_explain: tool({
      description:
        "Explain specific guideline IDs, with details and before/after examples. Pass only the IDs you intend to apply.",
      inputSchema: z.object({ ids: z.array(z.string()).min(1) }),
      execute: async ({ ids }) => guard(() => runSkillCli(skill.dir, ["explain", ...ids.slice(0, 12)])),
    }),
  };
}

const FENCE = /```(\w+)?\n([\s\S]*?)```/g;

/** Models wrap code in prose. Prefer a fence tagged with the task language,
 *  else the longest fence, else the raw text. */
export function extractCode(raw: string, lang: Task["lang"]): string {
  const tags = lang === "ts" ? ["ts", "typescript", "tsx"] : ["go", "golang"];
  const blocks = [...raw.matchAll(FENCE)].map((m) => ({ tag: (m[1] ?? "").toLowerCase(), body: m[2] ?? "" }));
  if (!blocks.length) return raw.trim();
  const tagged = blocks.filter((b) => tags.includes(b.tag));
  const pool = tagged.length ? tagged : blocks;
  return pool.sort((a, b) => b.body.length - a.body.length)[0]!.body.trim();
}

export type GenResult = {
  raw: string;
  code: string;
  toolCalls: { name: string; input: unknown }[];
  steps: number;
  finishReason: string | null;
  usage: Record<string, unknown> | null;
  error: string | null;
};

export async function generate(opts: {
  model: string;
  system: string;
  task: Task;
  skill: SkillDef | null;
  arm: Arm;
  maxOutputTokens: number;
}): Promise<GenResult> {
  const useTools = opts.arm === "skill" && opts.skill?.injection === "tool";
  let toolFailure: string | null = null;
  try {
    const r = await generateText({
      model: opts.model,
      system: opts.system,
      prompt: opts.task.prompt,
      temperature: 0.2,
      maxOutputTokens: opts.maxOutputTokens,
      ...(useTools
        ? {
            tools: skillTools(opts.skill!, (e) => {
              toolFailure ??= e instanceof Error ? e.message : String(e);
            }),
            stopWhen: stepCountIs(8),
          }
        : {}),
    });
    const toolCalls = r.steps.flatMap((s) =>
      s.toolCalls.map((c) => ({ name: c.toolName, input: c.input })),
    );
    return {
      raw: r.text,
      code: extractCode(r.text, opts.task.lang),
      toolCalls,
      steps: r.steps.length,
      finishReason: r.finishReason ?? null,
      usage: (r.usage ?? null) as Record<string, unknown> | null,
      // Infrastructure failure must not be reported as a skill result.
      error: toolFailure,
    };
  } catch (e) {
    return {
      raw: "",
      code: "",
      toolCalls: [],
      steps: 0,
      finishReason: null,
      usage: null,
      error: e instanceof Error ? e.message : String(e),
    };
  }
}
