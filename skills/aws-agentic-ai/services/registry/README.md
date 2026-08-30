# Agent Registry Service

> **Status**: GA under the `agent-registry` namespace since 2026-08-06. The public-preview `bedrock-agentcore` namespace shuts down 2026-09-17 — see [Migration from the Preview namespace](#migration-from-the-preview-namespace).

## Overview

AWS Agent Registry is a fully managed discovery service within Amazon Bedrock AgentCore. It provides a private, governed catalog for organizing, curating, and discovering AI agents, MCP servers, tools, agent skills, and custom resources across an organization.

**Problem it solves**: As organizations scale AI agents and tools, resources become siloed across teams. Teams build MCP servers, deploy agents, and create specialized tools, but without a central catalog, duplication of effort occurs because builders cannot discover what already exists.

## Migration from the Preview namespace

New customers must start on `agent-registry`; the `bedrock-agentcore` namespace is closed to accounts with no registries as of 2026-08-06 and shuts down entirely on 2026-09-17. GA changed every surface:

| Surface | Preview (`bedrock-agentcore`) | GA (`agent-registry`) |
|---|---|---|
| Data plane endpoint | `bedrock-agentcore.{region}.amazonaws.com` | `agent-registry.{region}.api.aws` |
| Control plane endpoint | `bedrock-agentcore-control.{region}.amazonaws.com` | `agent-registry-control.{region}.api.aws` |
| IAM action prefix | `bedrock-agentcore:*` | `agent-registry:*` |
| Service principal | `bedrock-agentcore.amazonaws.com` | `agent-registry.amazonaws.com` |
| Managed policy | `BedrockAgentCoreFullAccess` | `AgentRegistryFullAccess` |
| SDK clients | `BedrockAgentCoreClient` / `BedrockAgentCoreControlClient` | `AgentRegistryClient` / `AgentRegistryControlClient` |
| CLI namespace | `aws bedrock-agentcore` | `aws agent-registry` |
| ARN namespace | `arn:aws:bedrock-agentcore:…` | `arn:aws:agent-registry:…` |
| CloudTrail event source | `bedrock-agentcore.amazonaws.com` | `agent-registry.amazonaws.com` |
| EventBridge source | `aws.bedrock-agentcore` | `aws.agent-registry` |
| CloudWatch namespace | `AWS/BedrockAgentCore` | `AWS/AgentRegistry` |
| Search API | `SearchRegistryRecords` | `SearchDiscoverableRegistryRecords` |

Workload identity and OAuth credential provider resources stay on `bedrock-agentcore` — keep `bedrock-agentcore:CreateWorkloadIdentity`, `GetWorkloadIdentity`, and `DeleteWorkloadIdentity` in registry policies.

The record schema also changed: see [Registry Records](#registry-records). Data does not migrate itself; AWS ships tooling in [agentcore-samples](https://github.com/awslabs/agentcore-samples/tree/main/01-features/07-centralize-and-govern-your-ai-infrastructure/03-registry/04-migrate-to-new-namespace). Full mapping: [migration guide](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-faq.html).

## Core Concepts

### Registries

Top-level catalogs in your AWS account. Each registry has its own:
- Name and description
- `discoveryConfiguration.authorizerType` (`AWS_IAM` or `CUSTOM_JWT`) plus `discoveryConfiguration.authorizerConfiguration`
- `approvalConfiguration.autoApprovalRules` — a list; `["APPROVE_ALL"]` auto-approves, empty or omitted requires manual review
- Set of registry records

**Naming**: Must start alphanumeric. Valid characters: `a-z`, `A-Z`, `0-9`, `_`, `-`, `.`, `/`. Max 64 characters.

Organize registries by resource type, environment stage (prod/QA/dev), team, or use a single org-wide registry.

### Registry Records

Metadata entries describing individual resources. Each record has:
- **`name`** — required dedup key, unique within the registry (unique with `recordVersion` when both are set)
- **`displayName`** — human-readable label (this was `name` in Preview)
- **`description`** (max 4,096 chars) and **`recordVersion`** (semantic versioning recommended)
- **`recordType`** — required: `AGENT`, `MCP`, `SKILL`, or `CUSTOM`
- **`descriptors`** — exactly one primary descriptor key, keyed by descriptor name rather than the removed `descriptorType` union

### Record types and their descriptors

| `recordType` | Valid primary descriptors | Validation |
|-----------------|-------------|------------|
| **`MCP`** | `mcpServer`, `custom` | Server JSON in `mcpServer.data`, tools in `mcpServer.additionalData.tools`; validated against the MCP schema named by `dataSchemaVersion` |
| **`AGENT`** | `a2aAgentCard`, `mcpServer`, `custom` | Agent card in `a2aAgentCard.data`; `dataSchemaVersion` `0.3` |
| **`SKILL`** | `agentSkillsDefinition`, `custom` | Definition in `agentSkillsDefinition.data` (`dataSchemaVersion` `0.1.0`), SKILL.md in `agentSkillsDefinition.additionalData.skillMd.data` |
| **`CUSTOM`** | `custom` | JSON in `custom.data`, no schema validation |

Inside every descriptor the payload field is `data` and its version field is `dataSchemaVersion` (Preview used `inlineContent` plus `schemaVersion`/`protocolVersion`). URL sync moved from a top-level `synchronizationConfiguration` to a per-descriptor `source` — only `mcpServer` and `a2aAgentCard` carry one and only those two auto-sync.

### Record Lifecycle

```
Create → DRAFT → Submit → PENDING_APPROVAL → Approve → APPROVED
                                │                         │
                                │ Reject                  │ Edit (new DRAFT revision;
                                ▼                         │ approved stays in search)
                           REJECTED ── Approve (direct) ──┘
                                │
                                └── Edit → DRAFT

Any status → DEPRECATED (terminal, irreversible)
```

- **Draft**: Initial state. Not visible in search.
- **Pending Approval**: Submitted for review. Not visible in search.
- **Approved**: Visible in search results. Editing creates a new DRAFT revision while the approved revision stays active.
- **Rejected**: Curator can directly approve, or publisher can edit (creates new DRAFT) and resubmit.
- **Deprecated**: Terminal state — cannot be undone or edited. Removed from search but visible via `GetRegistryRecord` and `ListRegistryRecords` for auditing.

### Key Personas

| Persona | Responsibilities |
|---------|-----------------|
| **Administrator** | Creates registries, configures auth/approval, manages IAM permissions |
| **Publisher** | Creates records for their resources, submits for approval, configures sync |
| **Curator/Approver** | Reviews pending records, approves/rejects/deprecates based on org standards |
| **Consumer** | Searches for and discovers approved resources (human or agent) |

## Key Capabilities

### Hybrid Search

Combines semantic (vector-based, natural language) search with keyword matching. Both run simultaneously on every query with results ranked by weighted combination.

**Ranking**: Name has strongest keyword influence, followed by description and descriptor content (equal weight).

**Metadata filters** constrain results using operators:
- `$eq`, `$ne` — Equals / not equals
- `$in` — In list
- `$and`, `$or` — Logical combinators

Filterable fields: `name`, `recordType`, `recordVersion`.

### MCP-Native Access

Each registry exposes an MCP-compatible endpoint (MCP spec 2025-11-25):

```
https://agent-registry.<region>.api.aws/registry/<registryId>/mcp
```

The endpoint exposes three tools:
- `search_discoverable_registry_records` — `searchQuery` (required, 1-256 chars), `maxResults` (1-20, default 10), `filter` (optional metadata filter object)
- `list_discoverable_registry_records` — `maxResults` (1-100, default 20), `nextToken`, `filters` (list of `{"name": …, "values": […]}`)
- `batch_get_discoverable_registry_record` — `recordIds` (required, 1-100 record ARNs or IDs)

Any MCP-compatible client (Claude Code, Kiro, etc.) can connect directly.

See [MCP Endpoint Guide](mcp-endpoint.md) for detailed configuration.

### Governance and Curation

Configurable approval workflow with auto-approval or manual curator review.

See [Governance Workflows](governance-workflows.md) for details.

### Record Synchronization

Pull metadata from live external MCP servers or A2A agent endpoints via URL-based discovery. Supports OAuth and IAM credential providers for outbound authorization. Creates new revisions automatically when upstream changes.

See [Sync Configuration](sync-configuration.md) for details.

### EventBridge Notifications

Events sent to the default EventBridge bus (source: `aws.agent-registry`).

Record events (`detail` carries `registryRecordId` and `registryId`): `Registry Record State changed to Draft` / `… to Pending Approval` / `… to Approved` / `… to Rejected` / `… to Deprecated`.

Registry events (`detail` carries `registryId` and `registryName`): `Registry Creating`, `Registry Ready`, `Registry Create Failed`, `Registry Updating`, `Registry Update Failed`, `Registry Deleting`, `Registry Delete Failed`. `Registry Ready` replaces the Preview detail type `Registry State transitions from Creating to Ready` — a rule matching the old string no longer fires.

Enables automated review pipelines via Lambda, SNS, SQS, or Step Functions.

### CloudTrail Audit

All control plane API calls are logged as management events in CloudTrail.

## API Reference

### Control Plane CLI (`agent-registry-control`)

#### Registry Operations

| Operation | CLI Command |
|-----------|-------------|
| Create registry | `aws agent-registry-control create-registry` |
| Get registry | `aws agent-registry-control get-registry` |
| Update registry | `aws agent-registry-control update-registry` |
| Delete registry | `aws agent-registry-control delete-registry` |
| List registries | `aws agent-registry-control list-registries` |

#### Record Operations

| Operation | CLI Command |
|-----------|-------------|
| Create record | `aws agent-registry-control create-registry-record` |
| Get record | `aws agent-registry-control get-registry-record` |
| Update record | `aws agent-registry-control update-registry-record` |
| Delete record | `aws agent-registry-control delete-registry-record` |
| List records | `aws agent-registry-control list-registry-records` |

#### Approval Operations

| Operation | CLI Command |
|-----------|-------------|
| Submit for approval | `aws agent-registry-control submit-registry-record-for-approval` |
| Update status (approve/reject/deprecate) | `aws agent-registry-control update-registry-record-status` |

### Data Plane CLI (`agent-registry`)

| Operation | CLI Command |
|-----------|-------------|
| Search approved records | `aws agent-registry search-discoverable-registry-records` |
| List approved records | `aws agent-registry list-discoverable-registry-records` |
| Batch get approved records | `aws agent-registry batch-get-discoverable-registry-record` |
| MCP endpoint | POST to `https://agent-registry.<region>.api.aws/registry/<registryId>/mcp` |

### IAM Actions

> **Important**: registry IAM actions use the `agent-registry:` prefix — both control and data plane. The workload identity actions the service calls on your behalf during `CreateRegistry`/`DeleteRegistry` stay on `bedrock-agentcore:`.

**Control Plane:**

| Action | Description |
|--------|-------------|
| `agent-registry:CreateRegistry` | Create a registry |
| `agent-registry:GetRegistry` | Get a registry |
| `agent-registry:UpdateRegistry` | Update a registry |
| `agent-registry:DeleteRegistry` | Delete a registry |
| `agent-registry:ListRegistries` | List registries |
| `agent-registry:CreateRegistryRecord` | Create a record |
| `agent-registry:GetRegistryRecord` | Get a record |
| `agent-registry:UpdateRegistryRecord` | Update a record |
| `agent-registry:DeleteRegistryRecord` | Delete a record |
| `agent-registry:ListRegistryRecords` | List records |
| `agent-registry:SubmitRegistryRecordForApproval` | Submit for approval |
| `agent-registry:UpdateRegistryRecordStatus` | Approve/reject/deprecate |

**Data Plane:**

| Action | Description |
|--------|-------------|
| `agent-registry:SearchDiscoverableRegistryRecords` | Search approved registry records |
| `agent-registry:ListDiscoverableRegistryRecords` | List approved registry records |
| `agent-registry:GetDiscoverableRegistryRecord` | Retrieve an approved record; also authorizes `BatchGetDiscoverableRegistryRecord` |
| `agent-registry:InvokeRegistryMcp` | Invoke registry MCP endpoint |

> **Note**: MCP tool invocation requires BOTH `InvokeRegistryMcp` AND `SearchDiscoverableRegistryRecords`.

**Retained `bedrock-agentcore:` actions** (called by the service during registry lifecycle and URL sync): `CreateWorkloadIdentity`, `GetWorkloadIdentity`, `DeleteWorkloadIdentity`. `CreateRegistry` also needs `iam:CreateServiceLinkedRole`.

**Resource ARN Formats:**
- Registry: `arn:aws:agent-registry:{region}:{account}:registry/{registryId}`
- Record: `arn:aws:agent-registry:{region}:{account}:registry/{registryId}/record/{recordId}`

## Common Operations

### Create a Registry

```bash
aws agent-registry-control create-registry \
  --name "MyOrgRegistry" \
  --description "Central catalog for all AI agents and tools" \
  --region us-east-1
```

### Register an MCP Server

```bash
aws agent-registry-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "weather-server" \
  --display-name "WeatherServer" \
  --record-type MCP \
  --descriptors '{
    "mcpServer": {
      "dataSchemaVersion": "2025-12-11",
      "data": "{\"name\": \"weather-server\", \"description\": \"Weather data service\", \"version\": \"1.0.0\"}",
      "additionalData": {
        "tools": {"dataSchemaVersion": "2024-11-05", "data": "{\"tools\": [{\"name\": \"get_forecast\", \"description\": \"Get weather forecast\", \"inputSchema\": {\"type\": \"object\", \"properties\": {\"city\": {\"type\": \"string\"}}}}]}"}
      }
    }
  }' \
  --record-version "1.0" \
  --region us-east-1
```

### Register an Agent (A2A)

```bash
aws agent-registry-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "customer-support-agent" \
  --display-name "CustomerSupportAgent" \
  --record-type AGENT \
  --descriptors '{
    "a2aAgentCard": {"dataSchemaVersion": "0.3", "data": "{\"name\": \"customer-support\", \"description\": \"Handles customer inquiries\", \"version\": \"1.0.0\", \"protocolVersion\": \"0.3.0\", \"url\": \"https://api.example.com/a2a\", \"capabilities\": {}, \"defaultInputModes\": [\"text/plain\"], \"defaultOutputModes\": [\"text/plain\"], \"skills\": [{\"id\": \"order-lookup\", \"name\": \"Order Lookup\", \"description\": \"Look up order status\", \"tags\": [\"orders\"]}]}"}
  }' \
  --record-version "1.0" \
  --region us-east-1
```

### Search Records

```bash
aws agent-registry search-discoverable-registry-records \
  --search-query "weather forecast" \
  --registry-ids "<REGISTRY_ARN>" \
  --region us-east-1
```

### Search with Filters

```bash
aws agent-registry search-discoverable-registry-records \
  --search-query "customer" \
  --registry-ids "<REGISTRY_ARN>" \
  --filters '{"$and": [{"recordType": {"$eq": "AGENT"}}, {"recordVersion": {"$eq": "1.0"}}]}' \
  --region us-east-1
```

### Delete a Record

```bash
aws agent-registry-control delete-registry-record \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --region us-east-1
```

> **Note**: Delete all records before deleting a registry.

## Authorization

### IAM (SigV4)

Default authentication method. Works automatically with AWS CLI and SDKs.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "agent-registry:SearchDiscoverableRegistryRecords",
        "agent-registry:InvokeRegistryMcp"
      ],
      "Resource": "arn:aws:agent-registry:<region>:<account>:registry/<registryId>"
    }
  ]
}
```

### JWT (OAuth 2.0)

Supports Amazon Cognito, Okta, Azure AD, or any OIDC-compatible provider. Configure during registry creation. **Authorization type cannot be changed after creation.**

```bash
aws agent-registry-control create-registry \
  --name "external-registry" \
  --discovery-configuration '{
    "authorizerType": "CUSTOM_JWT",
    "authorizerConfiguration": {
      "customJWTAuthorizer": {
        "discoveryUrl": "https://cognito-idp.us-east-1.amazonaws.com/<poolId>/.well-known/openid-configuration",
        "allowedClients": ["<appClientId>"]
      }
    }
  }' \
  --region us-east-1
```

> **Constraint**: At least one JWT field required: `allowedAudiences`, `allowedClients`, `allowedScopes`, or `customClaims`. If multiple configured, ALL are verified.

## Best Practices

### Registry Organization
- **Single org-wide registry** for small organizations with few teams
- **Per-team registries** for larger organizations with clear ownership boundaries
- **Per-environment registries** (dev/staging/prod) for strict deployment governance

### Naming Conventions
- Use descriptive, unique names (e.g., `payments-mcp-server-v2` not `server1`)
- Include team/domain prefix when using shared registries (e.g., `platform/auth-agent`)
- Use semantic versioning for record versions

### Search Optimization
- Write detailed descriptions to improve semantic search relevance
- Use consistent `recordType` values to enable effective filtering
- Include relevant keywords in record metadata

### Security
- Use IAM for internal (AWS-to-AWS) access patterns
- Use JWT for external or cross-organization access
- Enable manual approval for production registries
- Audit all registry operations via CloudTrail

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Record not found in search | Record not approved | Check record status; submit for approval if in Draft |
| MCP endpoint 403 | Missing IAM permissions | Add both `InvokeRegistryMcp` and `SearchDiscoverableRegistryRecords` |
| Search returns no results | No approved records match query | Verify records exist and are approved; broaden search query |
| Create registry fails | Region not supported, or missing `iam:CreateServiceLinkedRole` | Check the region against the AWS Agent Registry endpoints reference; grant `iam:CreateServiceLinkedRole` |
| Schema validation error `'0.3.0' is not supported` | Wrong A2A schema version | Use `"dataSchemaVersion": "0.3"` (not `0.3.0`) |
| Sync not updating | Credential provider misconfigured | Verify outbound OAuth/IAM credentials for the source URL |

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | End-to-end quick start walkthrough |
| [MCP Endpoint Guide](mcp-endpoint.md) | Configure and use registry MCP endpoint with Claude Code |
| [Governance Workflows](governance-workflows.md) | Approval lifecycle and EventBridge automation |
| [Sync Configuration](sync-configuration.md) | URL-based sync from external MCP servers and A2A agents |
| [Registry Integration Patterns](../../cross-service/registry-integration.md) | Cross-service patterns with Gateway, Identity, Runtime |

## Related Services

- **[Gateway Service](../gateway/README.md)**: Deploy discovered MCP servers as Gateway targets
- **[Runtime Service](../runtime/README.md)**: Execute discovered agents in serverless runtime
- **[Identity Service](../identity/README.md)**: Manage credentials for registry authorization
- **[Observability Service](../observability/README.md)**: Monitor registry usage and search patterns

## References

- [AWS Agent Registry Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [Registry Concepts](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-concepts.html)
- [Supported Record Types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-supported-record-types.html)
- [Registry Search](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-search-records.html)
- [Registry MCP Endpoint](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-mcp-endpoint.html)
- [IAM Permissions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-iam-permissions.html)
- [Record Lifecycle](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-record-lifecycle.html)
- [Record Synchronization](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-sync-records.html)
- [Migration guide (`bedrock-agentcore` → `agent-registry`)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-faq.html)
