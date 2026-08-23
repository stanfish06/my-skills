---
name: e2b-sandbox
description: Guide for creating and managing E2B sandboxes using ComputeSDK. Use when building applications that need E2B provider for ComputeSDK - cloud sandboxes with full Linux environments, filesystem access, and microVM isolation.
---

# E2B Sandboxes with ComputeSDK

E2B provider for ComputeSDK - cloud sandboxes with full Linux environments, filesystem access, and microVM isolation.

## Setup

```bash
npm install computesdk @computesdk/e2b
```

Set your credentials:

```bash
# .env
E2B_API_KEY=your_e2b_api_key
```

## Quick Start

```typescript
import { compute } from 'computesdk';
import { e2b } from '@computesdk/e2b';

compute.setConfig({
  provider: e2b({
    apiKey: process.env.E2B_API_KEY,
  }),
});

const sandbox = await compute.sandbox.create();

const result = await sandbox.runCommand('echo "Hello from E2B!"');
console.log(result.stdout);

await sandbox.destroy();
```

You can also call the provider factory directly:

```typescript
import { e2b } from '@computesdk/e2b';

const sdk = e2b({
    apiKey: process.env.E2B_API_KEY,
  });
const sandbox = await sdk.sandbox.create();
```

## E2B Configuration

```typescript
interface E2BConfig {

  /** E2B API key - if not provided, will fallback to E2B_API_KEY environment variable */
  apiKey?: string;
  /** Execution timeout in milliseconds */
  timeout?: number;

}
```

## Full API

ComputeSDK exposes the same universal sandbox API across providers: `sandbox.create()`, `sandbox.getById()`, `sandbox.destroy()`, `sandbox.runCommand()`, `sandbox.getInfo()`, `sandbox.getUrl()`, and `sandbox.filesystem.*`.

Install the main skill for the complete reference:

```bash
npx skills add https://github.com/computesdk/sandbox-skills --skill computesdk
```

Or see https://www.computesdk.com/docs/reference/sandbox/.
