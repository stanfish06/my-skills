# Agent Registry - Getting Started

This guide walks through a complete workflow: creating a registry, registering resources, managing approvals, and searching.

## Prerequisites

- AWS CLI v2 configured with appropriate permissions
- An AWS account in a region where AWS Agent Registry is available
- Python 3.10+ and boto3 (for SDK examples)

### Minimum IAM Policy (Administrator)

> **Important**: registry IAM actions use the `agent-registry:` prefix. Workload identity actions stay on `bedrock-agentcore:`, and `CreateRegistry` needs `iam:CreateServiceLinkedRole`.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RegistryAndRecordManagement",
      "Effect": "Allow",
      "Action": [
        "agent-registry:CreateRegistry",
        "agent-registry:GetRegistry",
        "agent-registry:UpdateRegistry",
        "agent-registry:DeleteRegistry",
        "agent-registry:ListRegistries",
        "agent-registry:CreateRegistryRecord",
        "agent-registry:GetRegistryRecord",
        "agent-registry:UpdateRegistryRecord",
        "agent-registry:DeleteRegistryRecord",
        "agent-registry:ListRegistryRecords",
        "agent-registry:SubmitRegistryRecordForApproval",
        "agent-registry:UpdateRegistryRecordStatus"
      ],
      "Resource": "arn:aws:agent-registry:*:<account>:*"
    },
    {
      "Sid": "SearchAndMcp",
      "Effect": "Allow",
      "Action": [
        "agent-registry:SearchDiscoverableRegistryRecords",
        "agent-registry:ListDiscoverableRegistryRecords",
        "agent-registry:GetDiscoverableRegistryRecord",
        "agent-registry:InvokeRegistryMcp"
      ],
      "Resource": "arn:aws:agent-registry:*:<account>:registry/*"
    },
    {
      "Sid": "RegistryLifecycleServiceCalls",
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:CreateWorkloadIdentity",
        "bedrock-agentcore:GetWorkloadIdentity",
        "bedrock-agentcore:DeleteWorkloadIdentity",
        "iam:CreateServiceLinkedRole"
      ],
      "Resource": "*"
    }
  ]
}
```

For per-persona IAM policies (Publisher, Curator, Consumer), see [Registry Prerequisites](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-prerequisites.html).

## Step 1: Create a Registry

```bash
aws agent-registry-control create-registry \
  --name "my-org-registry" \
  --description "Central catalog for AI agents and MCP servers" \
  --region us-east-1
```

**Response** (key fields):
```json
{
  "registryId": "reg-abc123def456",
  "name": "my-org-registry",
  "status": "CREATING"
}
```

Wait for the registry to become `READY`:

```bash
aws agent-registry-control get-registry \
  --registry-id reg-abc123def456 \
  --region us-east-1 \
  --query "status"
```

> **Note**: Authorization type (IAM or JWT) is set at creation and **cannot be changed** afterward.

## Step 2: Register a Resource

### Option A: Register an MCP Server

MCP descriptors separate **server** metadata and **tools** definition, each with their own schema/protocol version:

```bash
aws agent-registry-control create-registry-record \
  --registry-id reg-abc123def456 \
  --name "weather-mcp-server" \
  --display-name "Weather MCP Server" \
  --description "Provides real-time weather data and forecasts for global locations" \
  --record-type MCP \
  --descriptors '{
    "mcpServer": {
      "dataSchemaVersion": "2025-12-11",
      "data": "{\"name\": \"io.example/weather-server\", \"description\": \"Weather data and forecasts via OpenWeatherMap API\", \"version\": \"1.0.0\"}",
      "additionalData": {
        "tools": {
          "dataSchemaVersion": "2024-11-05",
          "data": "{\"tools\": [{\"name\": \"get_forecast\", \"description\": \"Get 7-day weather forecast for a city\", \"inputSchema\": {\"type\": \"object\", \"properties\": {\"city\": {\"type\": \"string\", \"description\": \"City name\"}, \"units\": {\"type\": \"string\", \"enum\": [\"celsius\", \"fahrenheit\"]}}, \"required\": [\"city\"]}}]}"
        }
      }
    }
  }' \
  --record-version "1.0.0" \
  --region us-east-1
```

**Supported server `dataSchemaVersion`**: `2025-12-11`, `2025-10-17`, `2025-10-11`, `2025-09-29`, `2025-09-16`, `2025-07-09`
**Supported tools `dataSchemaVersion`**: `2025-11-25`, `2025-06-18`, `2025-03-26`, `2024-11-05`

### Option B: Register an Agent (A2A)

Agent cards follow the A2A protocol specification. Use `dataSchemaVersion` `0.3` (not `0.3.0`). The record type is `AGENT`; the descriptor key is `a2aAgentCard`:

```bash
aws agent-registry-control create-registry-record \
  --registry-id reg-abc123def456 \
  --name "customer-support-agent" \
  --display-name "Customer Support Agent" \
  --description "Handles customer inquiries, order status, and refund requests" \
  --record-type AGENT \
  --descriptors '{
    "a2aAgentCard": {
        "dataSchemaVersion": "0.3",
        "data": "{\"name\": \"customer-support\", \"description\": \"Handles customer inquiries\", \"version\": \"1.0.0\", \"protocolVersion\": \"0.3.0\", \"url\": \"https://api.example.com/a2a\", \"capabilities\": {}, \"defaultInputModes\": [\"text/plain\"], \"defaultOutputModes\": [\"text/plain\"], \"skills\": [{\"id\": \"order-lookup\", \"name\": \"Order Lookup\", \"description\": \"Look up order status\", \"tags\": [\"orders\"]}]}"
    }
  }' \
  --record-version "1.0.0" \
  --region us-east-1
```

### Option C: Register a Skill

Skill records support optional markdown documentation and a structured definition:

```bash
aws agent-registry-control create-registry-record \
  --registry-id reg-abc123def456 \
  --name "data-analysis-skill" \
  --display-name "Data Analysis Skill" \
  --description "Reusable skill for analyzing CSV/Parquet datasets with statistical summaries" \
  --record-type SKILL \
  --descriptors '{
    "agentSkillsDefinition": {
      "dataSchemaVersion": "0.1.0",
      "data": "{\"websiteUrl\": \"https://example.com/data-analysis\", \"repository\": {\"url\": \"https://github.com/example/data-analysis-skill\", \"source\": \"github\"}}",
      "additionalData": {
        "skillMd": {
          "data": "---\nname: data-analysis\ndescription: Analyzes tabular data files and produces statistical summaries.\n---\n# Data Analysis Skill\n\n## Inputs\n- File path (CSV or Parquet)\n- Analysis type: descriptive, correlation, or regression\n\n## Outputs\n- Summary statistics\n- Visualizations (PNG)\n- Markdown report"
        }
      }
    }
  }' \
  --record-version "1.0.0" \
  --region us-east-1
```

### Option D: Register a Custom Resource

Custom records accept any valid JSON with no schema validation:

```bash
aws agent-registry-control create-registry-record \
  --registry-id reg-abc123def456 \
  --name "product-knowledge-base" \
  --display-name "Product Knowledge Base" \
  --description "Bedrock Knowledge Base with product catalog and documentation" \
  --record-type CUSTOM \
  --descriptors '{
    "custom": {
      "data": "{\"type\": \"knowledge-base\", \"knowledgeBaseId\": \"KB12345\", \"dataSourceCount\": 3, \"documentCount\": 15000, \"lastSyncedAt\": \"2026-04-01T00:00:00Z\"}"
    }
  }' \
  --record-version "1.0.0" \
  --region us-east-1
```

## Step 3: Submit for Approval

Records start in **Draft** status. Submit to make them discoverable:

```bash
aws agent-registry-control submit-registry-record-for-approval \
  --registry-id reg-abc123def456 \
  --record-id rec-xyz789 \
  --region us-east-1
```

The record moves to **Pending Approval** (or **Approved** if auto-approval is enabled).

## Step 4: Approve (Curator Role)

If the registry uses manual approval, a curator must review and approve:

```bash
# Approve
aws agent-registry-control update-registry-record-status \
  --registry-id reg-abc123def456 \
  --record-id rec-xyz789 \
  --status APPROVED \
  --status-reason "Reviewed: description is clear, schema is valid, team ownership confirmed" \
  --region us-east-1
```

```bash
# Or reject with reason
aws agent-registry-control update-registry-record-status \
  --registry-id reg-abc123def456 \
  --record-id rec-xyz789 \
  --status REJECTED \
  --status-reason "Missing tool descriptions - please add descriptions to all tools before resubmitting" \
  --region us-east-1
```

> **Note**: Curators can directly approve a rejected record without requiring the publisher to resubmit.

## Step 5: Search and Discover

Once approved, records are searchable. **Eventual consistency**: approved records typically appear within seconds but may take up to minutes.

### Semantic Search (Natural Language)

```bash
aws agent-registry search-discoverable-registry-records \
  --search-query "I need a tool that can tell me the weather" \
  --registry-ids "arn:aws:agent-registry:us-east-1:<account-id>:registry/reg-abc123def456" \
  --region us-east-1
```

### Filtered Search

```bash
# Find only MCP servers
aws agent-registry search-discoverable-registry-records \
  --search-query "data processing" \
  --registry-ids "arn:aws:agent-registry:us-east-1:<account-id>:registry/reg-abc123def456" \
  --filters '{"recordType": {"$eq": "MCP"}}' \
  --region us-east-1
```

```bash
# Find A2A agents at version 1.0.0
aws agent-registry search-discoverable-registry-records \
  --search-query "customer" \
  --registry-ids "arn:aws:agent-registry:us-east-1:<account-id>:registry/reg-abc123def456" \
  --filters '{"$and": [{"recordType": {"$eq": "AGENT"}}, {"recordVersion": {"$eq": "1.0.0"}}]}' \
  --region us-east-1
```

### Search via MCP Endpoint

Any MCP-compatible client can search directly. See [MCP Endpoint Guide](mcp-endpoint.md) for Claude Code and Kiro integration.

## Complete Example: Team Onboarding

```bash
REGION="us-east-1"
REGISTRY_ID="reg-abc123def456"

# 1. Team publishes their MCP server
RECORD=$(aws agent-registry-control create-registry-record \
  --registry-id $REGISTRY_ID \
  --name "payments-mcp-server" \
  --display-name "Payments MCP Server" \
  --description "Payment processing tools: charge, refund, status lookup" \
  --record-type MCP \
  --descriptors '{
    "mcpServer": {
      "dataSchemaVersion": "2025-12-11",
      "data": "{\"name\": \"payments\", \"description\": \"Payment processing\", \"version\": \"2.1.0\"}",
      "additionalData": {
        "tools": {"dataSchemaVersion": "2024-11-05", "data": "{\"tools\": [{\"name\": \"charge\", \"description\": \"Process a payment\"}, {\"name\": \"refund\", \"description\": \"Issue a refund\"}, {\"name\": \"get_status\", \"description\": \"Check payment status\"}]}"}
      }
    }
  }' \
  --record-version "2.1.0" \
  --region $REGION \
  --query "recordId" --output text)

echo "Created record: $RECORD"

# 2. Submit for review
aws agent-registry-control submit-registry-record-for-approval \
  --registry-id $REGISTRY_ID \
  --record-id $RECORD \
  --region $REGION

# 3. Curator approves
aws agent-registry-control update-registry-record-status \
  --registry-id $REGISTRY_ID \
  --record-id $RECORD \
  --status APPROVED \
  --status-reason "Payment team tools approved - schema valid, descriptions clear" \
  --region $REGION

# 4. Other teams can now discover it
aws agent-registry search-discoverable-registry-records \
  --search-query "payment processing" \
  --registry-ids "arn:aws:agent-registry:${REGION}:$(aws sts get-caller-identity --query Account --output text):registry/${REGISTRY_ID}" \
  --region $REGION
```

## Next Steps

- [MCP Endpoint Guide](mcp-endpoint.md) — Connect Claude Code or Kiro to your registry
- [Governance Workflows](governance-workflows.md) — Set up automated approval pipelines
- [Sync Configuration](sync-configuration.md) — Auto-sync from live MCP servers and A2A agents
- [Registry Integration Patterns](../../cross-service/registry-integration.md) — Combine with Gateway, Runtime, Identity
