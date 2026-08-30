Write a self-contained TypeScript module `settings.ts` (no imports, no external
dependencies) that parses raw string settings into typed values.

Export exactly these two functions:

```ts
export function parseSetting(key: string, raw: string): /* your outcome type */
export function renderSetting(outcome: /* your outcome type */): string
```

Behaviour:

1. `raw` of `"true"` or `"false"` parses as a boolean. A `raw` of only digits,
   optionally led by `-`, parses as an integer. Anything else parses as a
   string. An empty `raw` is a parse failure with the reason `empty`.
2. `renderSetting` returns `key=value` for a successful parse, using the
   value's plain text form (`debug=true`, `retries=42`, `name=hello`).
3. `renderSetting` returns `key=!reason` for a failure, so an empty `raw` for
   key `x` renders as `x=!empty`.
4. If someone later adds a new kind of setting value, `renderSetting` must fail
   to compile until they handle it. Do not rely on a runtime check alone.
5. The module must type-check under `strict` with `noUncheckedIndexedAccess`.

Return only the contents of `settings.ts` in a single TypeScript code block.
