Write a self-contained TypeScript module `settings.ts` (no imports, no external
dependencies) that parses raw string settings into typed values.

Requirements:

1. A setting value is one of: a boolean (`"true"` / `"false"`), an integer
   (e.g. `"42"`), or a plain string. Parsing can also fail with a reason.
2. Export a parse function that takes `(key: string, raw: string)` and returns
   the parsed outcome.
3. Export a render function that turns any parse outcome into a display string
   for a log line.
4. If someone later adds a new kind of setting value, the render function must
   fail to compile until they handle it. Do not rely on a runtime check alone.
5. The module must type-check under `strict` with `noUncheckedIndexedAccess`.

Return only the contents of `settings.ts` in a single TypeScript code block.
