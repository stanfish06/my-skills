# Agent Registry - Sync Configuration

Agent Registry can automatically sync metadata from live external MCP servers and A2A agent endpoints via URL-based discovery. When the upstream source changes, the registry creates new record revisions automatically.

## How Sync Works

```
┌──────────────────┐         ┌──────────────┐         ┌──────────────┐
│ External MCP     │  pull   │ Agent        │  store   │ Registry     │
│ Server / A2A     │ <────── │ Registry     │ ──────>  │ Record       │
│ Agent (source)   │         │ Sync Engine  │         │ (new revision)│
└──────────────────┘         └──────────────┘         └──────────────┘
```

1. Registry connects to the source URL using outbound credentials
2. Retrieves server/tool definitions (MCP) or agent card (AGENT)
3. Populates/updates record descriptors, name, description, and version from source
4. Creates a new revision if changes are detected

> **Limitation**: SSE streaming from MCP servers is not supported.

## Sync API Structure

Sync is a `source` block **inside** the descriptor. The Preview top-level `--synchronization-type` / `--synchronization-configuration` parameters no longer exist:

```bash
aws agent-registry-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "<record-name>" \
  --record-type <MCP|AGENT> \
  --descriptors '{"<mcpServer|a2aAgentCard>": {"source": {"fromUrl": {"url": "<source-url>"}}}}' \
  --region us-east-1
```

Only `mcpServer` and `a2aAgentCard` carry a `source`, and only those two auto-sync. A `source` on `agentSkillsDefinition.additionalData.skillMd` is persisted but never used to run a sync; `custom` records must supply `data` directly. Only `source.fromUrl` is supported.

## Syncing MCP Servers

### From a Public MCP Server (No Auth)

```bash
aws agent-registry-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "aws-knowledge-server" \
  --record-type MCP \
  --descriptors '{
    "mcpServer": {
      "source": {
        "fromUrl": {
          "url": "https://knowledge-mcp.global.api.aws"
        }
      }
    }
  }' \
  --region us-east-1
```

### From an OAuth-Protected MCP Server

```bash
aws agent-registry-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "oauth-mcp-server" \
  --record-type MCP \
  --descriptors '{
    "mcpServer": {
      "source": {
        "fromUrl": {
          "url": "https://analytics.internal.example.com/mcp",
          "credentialProviderConfigurations": [{
            "credentialProviderType": "OAUTH",
            "credentialProvider": {
              "oauthCredentialProvider": {
                "providerArn": "<OAUTH_PROVIDER_ARN>",
                "grantType": "CLIENT_CREDENTIALS"
              }
            }
          }]
        }
      }
    }
  }' \
  --region us-east-1
```

**Additional IAM permissions for OAuth sync** (these stay on the `bedrock-agentcore` namespace — OAuth credential providers were not moved):
```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock-agentcore:GetWorkloadAccessToken",
      "Resource": "arn:aws:bedrock-agentcore:*:<account>:workload-identity-directory/*"
    },
    {
      "Effect": "Allow",
      "Action": "bedrock-agentcore:GetResourceOauth2Token",
      "Resource": "arn:aws:bedrock-agentcore:*:<account>:token-vault/*"
    }
  ]
}
```

### From an IAM-Protected MCP Server

For MCP servers on AWS infrastructure (Gateway targets, Lambda, API Gateway) using SigV4:

```bash
aws agent-registry-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "gateway-mcp-server" \
  --record-type MCP \
  --descriptors '{
    "mcpServer": {
      "source": {
        "fromUrl": {
          "url": "https://bedrock-agentcore.us-east-1.amazonaws.com/gateway/<gw-id>/target/<tgt-id>/mcp",
          "credentialProviderConfigurations": [{
            "credentialProviderType": "IAM",
            "credentialProvider": {
              "iamCredentialProvider": {
                "roleArn": "arn:aws:iam::<account-id>:role/RegistrySyncRole",
                "service": "bedrock-agentcore",
                "region": "us-east-1"
              }
            }
          }]
        }
      }
    }
  }' \
  --region us-east-1
```

**`service` values for SigV4 signing:**
- `bedrock-agentcore` — AgentCore Runtime/Gateway
- `execute-api` — API Gateway
- `lambda` — Lambda function URLs

**`region`** is optional and defaults to the registry's region.

**Additional IAM permissions for IAM-based sync:**
```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::<account>:role/RegistrySyncRole",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "agent-registry.amazonaws.com"
        },
        "StringLike": {
          "iam:AssociatedResourceARN": "arn:aws:agent-registry:<region>:<account>:registry/*/record/*"
        }
      }
    }
  ]
}
```

The IAM role needs a trust policy naming the GA service principal. A role still trusting `bedrock-agentcore.amazonaws.com` fails to be assumed after migration:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "agent-registry.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Syncing A2A Agent Cards

Sync agent cards from the standard A2A well-known endpoint:

```bash
aws agent-registry-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "travel-agent" \
  --record-type AGENT \
  --descriptors '{
    "a2aAgentCard": {
      "source": {
        "fromUrl": {
          "url": "https://agent.example.com/.well-known/agent-card.json"
        }
      }
    }
  }' \
  --region us-east-1
```

For OAuth or IAM-protected agent endpoints, add `credentialProviderConfigurations` as shown in the MCP examples above.

## Manually Triggering Sync

To force a re-sync of an existing record:

```bash
aws agent-registry-control update-registry-record \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --trigger-synchronization \
  --region us-east-1
```

## Monitoring Sync Status

```bash
aws agent-registry-control get-registry-record \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --region us-east-1
```

Check the `status` field. If sync fails, the record transitions to `CREATE_FAILED` or `UPDATE_FAILED`.

## Sync vs Inline Content

| Aspect | URL-based Sync | Inline Content |
|--------|---------------|----------------|
| **Source of truth** | External MCP server / A2A agent | Registry record itself |
| **Updates** | Automatic on upstream changes | Manual via `update-registry-record` |
| **Auth required** | Yes (if source is protected) | No |
| **Record types** | `MCP` and `AGENT` only | All types (`MCP`, `AGENT`, `SKILL`, `CUSTOM`) |
| **Use case** | Live, evolving servers/agents | Stable, versioned resources |
| **Network dependency** | Source must be publicly reachable (no private IPs) | None |

### When to Use Sync

- MCP servers that are actively developed and frequently updated
- Gateway targets where tool definitions evolve with the upstream API
- A2A agents that publish well-known agent cards
- Multi-team environments where publishers manage their own servers

### When to Use Inline Content

- Stable, versioned resources that rarely change
- Resources where the registry should be the sole source of truth
- Skills and custom resources (sync not supported for `SKILL`/`CUSTOM` record types)
- Air-gapped environments or private network resources

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `CREATE_FAILED` | Source URL unreachable | Verify URL resolves to a public IP; check DNS |
| `CREATE_FAILED` | Credential provider misconfigured | Check OAuth client ID/secret or IAM role trust policy |
| `UPDATE_FAILED` | HTTP non-200/202 response | Check source server health; verify credentials haven't expired |
| `CREATE_FAILED` | URL resolves to private IP | Only public IPs are supported for sync |
| `CREATE_FAILED` | MCP tools/list timeout | Source must respond within 30 seconds |
| `CREATE_FAILED` | Response exceeds max size | Reduce the number of tools or simplify descriptions |
| Record in Draft after sync | Sync populates content but doesn't auto-approve | Submit for approval after initial sync |

## Related

- [Registry Overview](README.md)
- [Getting Started](getting-started.md)
- [Cross-Service Credential Management](../../cross-service/credential-management.md)
- [Record Synchronization (AWS Docs)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-sync-records.html)
- [Gateway Service](../gateway/README.md) — Source of Gateway-based MCP targets
- [Identity Service](../identity/README.md) — Credential providers for outbound auth
