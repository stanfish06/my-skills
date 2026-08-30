// Harness-owned behaviour check. Compiling is not enough: a module can declare
// a tagged union and a never-exhaustiveness helper without parsing anything.
import { strict as assert } from "node:assert";
import { parseSetting, renderSetting } from "./solution.ts";

const cases: [string, string, string][] = [
  ["debug", "true", "debug=true"],
  ["debug", "false", "debug=false"],
  ["retries", "42", "retries=42"],
  ["offset", "-7", "offset=-7"],
  ["name", "hello", "name=hello"],
  ["x", "", "x=!empty"],
];

for (const [key, raw, want] of cases) {
  const got = renderSetting(parseSetting(key, raw));
  assert.equal(got, want, `parseSetting(${JSON.stringify(key)}, ${JSON.stringify(raw)}) rendered ${JSON.stringify(got)}, want ${JSON.stringify(want)}`);
}
