---
title: Analytics Engineering & LLM Operations
tags:
  - skill-map
created: 2026-06-13
---

# Analytics Engineering & LLM Operations

> [!abstract] Scope
> dbt analytics engineering, semantic layers, warehouse querying, lineage diagrams, LLM observability, prompt tracing, and evaluation workflows.

[Back to Skill Index](../index.md)

**Related maps:** [Data Science, Stats & Scientific Computing](data-science-compute.md) | [Cloud, Infra & MLOps](cloud-devops.md) | [Machine Learning & AI](ml-ai.md) | [Security & Auditing](security-auditing.md)

## Skills (99)

- [adding-dbt-unit-test](../notes/analytics-engineering/adding-dbt-unit-test.md) — Creates unit test YAML definitions that mock upstream model inputs and validate expected outputs
- [answering-natural-language-questions-with-dbt](../notes/analytics-engineering/answering-natural-language-questions-with-dbt.md) — Writes and executes SQL queries against the data warehouse using dbt's Semantic Layer or ad-hoc SQL to answer business questions
- [building-dbt-semantic-layer](../notes/analytics-engineering/building-dbt-semantic-layer.md) — Use when creating or modifying dbt Semantic Layer components — semantic models, metrics, dimensions, entities, measures, or time spines
- [chdb-datastore](../notes/analytics-engineering/chdb-datastore.md) — Use when the user has tabular data (pandas DataFrame, parquet, csv, Arrow, json) and wants to filter, group, aggregate, join, or speed up slow pandas
- [chdb-sql](../notes/analytics-engineering/chdb-sql.md) — Use when the user wants to run SQL — especially analytical SQL — on local files (parquet/csv/json), URLs, S3 paths, or remote databases (Postgres, MySQL, MongoDB, ClickHouse Cloud...
- [clickhouse-architecture-advisor](../notes/analytics-engineering/clickhouse-architecture-advisor.md) — MUST USE when designing ClickHouse architectures, selecting between ingestion or modeling patterns, or translating best practices into workload-specific system designs
- [clickhouse-best-practices](../notes/analytics-engineering/clickhouse-best-practices.md) — MUST USE when reviewing ClickHouse schemas, queries, or configurations
- [clickhouse-js-node-coding](../notes/analytics-engineering/clickhouse-js-node-coding.md) — Write idiomatic application code with the ClickHouse Node.js client (`@clickhouse/client`)
- [clickhouse-js-node-rowbinary](../notes/analytics-engineering/clickhouse-js-node-rowbinary.md) — Generate TypeScript/JavaScript code that reads/decodes AND writes/encodes ClickHouse RowBinary streams for the ClickHouse HTTP server
- [clickhouse-js-node-troubleshooting](../notes/analytics-engineering/clickhouse-js-node-troubleshooting.md) — Troubleshoot and resolve common issues with the ClickHouse Node.js client (@clickhouse/client)
- [clickhouse-managed-postgres-rca](../notes/analytics-engineering/clickhouse-managed-postgres-rca.md) — MUST USE when investigating performance issues on a ClickHouse-managed Postgres instance
- [clickstack-otel-collector](../notes/analytics-engineering/clickstack-otel-collector.md) — Use when a user wants to wire an OpenTelemetry collector into a Managed ClickStack service on ClickHouse Cloud, either by deploying a new local collector (Docker run or Docker Compose)...
- [configuring-dbt-mcp-server](../notes/analytics-engineering/configuring-dbt-mcp-server.md) — Generates MCP server configuration JSON, resolves authentication setup, and validates server connectivity for dbt
- [creating-mermaid-dbt-dag](../notes/analytics-engineering/creating-mermaid-dbt-dag.md) — Generates a Mermaid flowchart diagram of dbt model lineage using MCP tools, manifest.json, or direct code parsing as fallbacks
- [dagster-expert](../notes/analytics-engineering/dagster-expert.md) — Expert guidance for working with Dagster and the dg CLI
- [databricks-agent-bricks](../notes/analytics-engineering/databricks-agent-bricks.md) — Create Agent Bricks: Knowledge Assistants (KA) for document Q&A and Supervisor Agents for multi-agent orchestration (MAS)
- [databricks-ai-functions](../notes/analytics-engineering/databricks-ai-functions.md) — Use Databricks built-in AI Functions (ai_classify, ai_extract, ai_summarize, ai_mask, ai_translate, ai_fix_grammar, ai_gen, ai_analyze_sentiment, ai_similarity, ai_parse_document...
- [databricks-aibi-dashboards](../notes/analytics-engineering/databricks-aibi-dashboards.md) — Create Databricks AI/BI dashboards. Must use when creating, updating, or deploying Lakeview dashboards as Databricks Dashboard have a unique json structure
- [databricks-app-design](../notes/analytics-engineering/databricks-app-design.md) — Design the UX of custom-code Databricks Apps (AppKit/React) data screens — KPI/overview pages, reports, charts, tables, and Genie/chat data assistants — mapped to concrete AppKit...
- [databricks-apps](../notes/analytics-engineering/databricks-apps.md) — Build apps on Databricks Apps platform. Use when asked to create data apps, analytics tools, or custom interactive visualizations
- [databricks-apps-python](../notes/analytics-engineering/databricks-apps-python.md) — Python backend for Databricks Apps — FastAPI (default), Flask, Dash, Streamlit, Gradio, Reflex
- [databricks-core](../notes/analytics-engineering/databricks-core.md) — Databricks CLI operations and the parent/entry-point skill for Databricks CLI use: authentication, profile selection, and bundles
- [databricks-dabs](../notes/analytics-engineering/databricks-dabs.md) — Create, configure, validate, deploy, run, and manage Declarative Automation Bundles (DABs, formerly Databricks Asset Bundles)
- [databricks-data-discovery](../notes/analytics-engineering/databricks-data-discovery.md) — Discover, explore, and query Databricks data via Genie — the CLI equivalent of the Genie One MCP
- [databricks-dbsql](../notes/analytics-engineering/databricks-dbsql.md) — Databricks SQL (DBSQL) advanced features and SQL warehouse capabilities
- [databricks-docs](../notes/analytics-engineering/databricks-docs.md) — Databricks documentation reference via llms.txt index
- [databricks-execution-compute](../notes/analytics-engineering/databricks-execution-compute.md) — Execute code and manage compute on Databricks: run Python/Scala/SQL/R via serverless, classic, or interactive clusters, and create/resize/delete clusters and SQL warehouses
- [databricks-genie-agents](../notes/analytics-engineering/databricks-genie-agents.md) — Create, manage, and query Databricks Genie Agents — curated, per-data natural-language agents (formerly Genie Spaces): build, export/import, migrate across workspaces, and ask...
- [databricks-iceberg](../notes/analytics-engineering/databricks-iceberg.md) — Apache Iceberg tables on Databricks — Managed Iceberg tables, External Iceberg Reads (fka Uniform), Compatibility Mode, Iceberg REST Catalog (IRC), Iceberg v3, Snowflake interop...
- [databricks-jobs](../notes/analytics-engineering/databricks-jobs.md) — Develop and deploy Lakeflow Jobs on Databricks via DABs, Python SDK, or the CLI
- [databricks-lakebase](../notes/analytics-engineering/databricks-lakebase.md) — Databricks Lakebase Postgres: projects, scaling, connectivity, Lakebase synced tables, and Data API
- [databricks-lakeflow-connect](../notes/analytics-engineering/databricks-lakeflow-connect.md) — Build managed ingestion pipelines into Databricks using Lakeflow Connect
- [databricks-metric-views](../notes/analytics-engineering/databricks-metric-views.md) — Unity Catalog metric views: define, create, query, and manage governed business metrics in YAML
- [databricks-ml-training](../notes/analytics-engineering/databricks-ml-training.md) — Train ML models on Databricks. Use for: classification/regression/deep-learning (XGBoost, scikit-learn, LightGBM, PyTorch) with Optuna, @prod/@challenger aliases, batch scoring...
- [databricks-mlflow-evaluation](../notes/analytics-engineering/databricks-mlflow-evaluation.md) — MLflow 3 GenAI agent evaluation. Use when writing mlflow.genai.evaluate() code, creating @scorer functions, using built-in scorers (Guidelines, Correctness, Safety...
- [databricks-model-serving](../notes/analytics-engineering/databricks-model-serving.md) — Databricks Model Serving endpoint lifecycle and ops
- [databricks-pipelines](../notes/analytics-engineering/databricks-pipelines.md) — Develop Lakeflow Spark Declarative Pipelines (formerly Delta Live Tables) on Databricks
- [databricks-python-sdk](../notes/analytics-engineering/databricks-python-sdk.md) — Databricks development guidance including Python SDK, Databricks Connect, CLI, and REST API
- [databricks-serverless-migration](../notes/analytics-engineering/databricks-serverless-migration.md) — Migrate Databricks workloads from classic compute to serverless compute
- [databricks-spark-structured-streaming](../notes/analytics-engineering/databricks-spark-structured-streaming.md) — Comprehensive guide to Spark Structured Streaming for production workloads
- [databricks-synthetic-data-gen](../notes/analytics-engineering/databricks-synthetic-data-gen.md) — Generate realistic synthetic data using Spark + Faker (strongly recommended)
- [databricks-unity-catalog](../notes/analytics-engineering/databricks-unity-catalog.md) — Unity Catalog governance, access control, and observability
- [databricks-unstructured-pdf-generation](../notes/analytics-engineering/databricks-unstructured-pdf-generation.md) — Build RAG / unstructured-document evaluation datasets and demo documents (e.g
- [databricks-vector-search](../notes/analytics-engineering/databricks-vector-search.md) — Databricks Vector Search endpoints and indexes for RAG and semantic search
- [databricks-zerobus-ingest](../notes/analytics-engineering/databricks-zerobus-ingest.md) — Build Zerobus Ingest clients for near real-time data ingestion into Databricks Delta tables via gRPC
- [fetching-dbt-docs](../notes/analytics-engineering/fetching-dbt-docs.md) — Retrieves and searches dbt documentation pages in LLM-friendly markdown format
- [infra-clickhouse](../notes/analytics-engineering/infra-clickhouse.md) — Sets up and manages ClickHouse using the clickhousectl CLI — installs and runs a local ClickHouse server for development, and creates managed ClickHouse Cloud services for production...
- [infra-postgres](../notes/analytics-engineering/infra-postgres.md) — Sets up and manages Postgres using the clickhousectl CLI — runs a local Docker-backed Postgres for development, and creates and operates managed ClickHouse Cloud Postgres services...
- [iris-development](../notes/analytics-engineering/iris-development.md) — Iris is Redis's umbrella for AI-focused products
- [langfuse](../notes/analytics-engineering/langfuse.md) — Interact with Langfuse and access its documentation
- [llm-observability-evals](../notes/analytics-engineering/llm-observability-evals.md) — LLM and agent observability, tracing, and evaluation workflows with langfuse, phoenix-cli, and phoenix-evals
- [logfire-instrumentation](../notes/analytics-engineering/logfire-instrumentation.md) — Add Pydantic Logfire observability to applications and send as much useful telemetry as possible
- [logfire-query](../notes/analytics-engineering/logfire-query.md) — Query and analyze Logfire telemetry data — traces, logs, spans, metrics, summaries, and SQL results
- [logfire-ui](../notes/analytics-engineering/logfire-ui.md) — Open or return Logfire project pages, live views, trace links, and Explore pages in the Codex browser without querying telemetry first
- [migrating-dbt-core-to-fusion](../notes/analytics-engineering/migrating-dbt-core-to-fusion.md) — Use when a user needs help triaging dbt-core to Fusion migration errors
- [migrating-dbt-project-across-platforms](../notes/analytics-engineering/migrating-dbt-project-across-platforms.md) — Use when migrating a dbt project from one data platform or data warehouse to another (e.g., Snowflake to Databricks, Databricks to Snowflake) using dbt Fusion's real-time compilation...
- [neo4j-agent-memory-skill](../notes/analytics-engineering/neo4j-agent-memory-skill.md) — Authoritative reference for the neo4j-agent-memory Python package — a graph-native memory system for AI agents built on Neo4j — and for the hosted service (NAMS) at memory.neo4jlabs.com
- [neo4j-aura-agent-skill](../notes/analytics-engineering/neo4j-aura-agent-skill.md) — Manages Neo4j Aura Agents via the v2beta1 REST API — create, list, get, update, delete, and invoke Aura agents backed by an AuraDB instance
- [neo4j-aura-graph-analytics-skill](../notes/analytics-engineering/neo4j-aura-graph-analytics-skill.md) — Serverless Aura Graph Analytics (AGA) GDS Sessions — covers GdsSessions, AuraGraphDataScience, AuraAPICredentials, DbmsConnectionInfo, SessionMemory, get_or_create, remote graph...
- [neo4j-aura-provisioning-skill](../notes/analytics-engineering/neo4j-aura-provisioning-skill.md) — Provisions and manages Neo4j Aura instances via CLI (aura-cli v1.7+) or REST API
- [neo4j-cli-tools-skill](../notes/analytics-engineering/neo4j-cli-tools-skill.md) — Use when working with Neo4j command-line tools — neo4j-cli (modern unified CLI — Cypher via Bolt, schema inspection, Aura management, Docker containers, credential management, agent...
- [neo4j-cypher-skill](../notes/analytics-engineering/neo4j-cypher-skill.md) — Generates, optimizes, and validates Cypher 25 queries for Neo4j 2025.x and 2026.x
- [neo4j-document-import-skill](../notes/analytics-engineering/neo4j-document-import-skill.md) — Ingests unstructured and semi-structured documents into Neo4j as a knowledge graph
- [neo4j-driver-dotnet-skill](../notes/analytics-engineering/neo4j-driver-dotnet-skill.md) — Neo4j .NET Driver v6 — IDriver lifecycle, DI registration (singleton), ExecutableQuery fluent API, ExecuteReadAsync/ExecuteWriteAsync managed transactions, IResultCursor (FetchAsync/...
- [neo4j-driver-go-skill](../notes/analytics-engineering/neo4j-driver-go-skill.md) — Covers the Neo4j Go Driver v6 — driver lifecycle, ExecuteQuery, managed and explicit transactions, session config, error handling, data type mapping, and connection tuning
- [neo4j-driver-java-skill](../notes/analytics-engineering/neo4j-driver-java-skill.md) — Neo4j Java Driver v6 — driver lifecycle, Maven/Gradle setup, executableQuery, executeRead/Write managed transactions, explicit transactions, async/reactive patterns, error handling...
- [neo4j-driver-javascript-skill](../notes/analytics-engineering/neo4j-driver-javascript-skill.md) — Neo4j JavaScript/TypeScript Driver v6 — driver lifecycle, executeQuery, managed transactions (executeRead/executeWrite), session.run, Integer handling, JSON serialization, record...
- [neo4j-driver-python-skill](../notes/analytics-engineering/neo4j-driver-python-skill.md) — Neo4j Python Driver v6 — driver lifecycle, execute_query, managed and explicit transactions, async (AsyncGraphDatabase), result handling, data type mapping, error handling, UNWIND...
- [neo4j-gds-skill](../notes/analytics-engineering/neo4j-gds-skill.md) — Neo4j Graph Data Science (GDS) embedded plugin via Python client or Cypher — covers GraphDataScience, gds.v2 plugin endpoints, gds.version, native projection, Cypher projection, graph...
- [neo4j-genai-plugin-skill](../notes/analytics-engineering/neo4j-genai-plugin-skill.md) — Use Neo4j GenAI Plugin ai.text.* functions and procedures for in-Cypher embedding generation, text completion, structured output, chat, tokenization, and batch ingestion
- [neo4j-getting-started-skill](../notes/analytics-engineering/neo4j-getting-started-skill.md) — Orchestrates zero-to-running-app in 8 stages — prerequisites → context → provision → model → load → explore → query → build
- [neo4j-graphql-skill](../notes/analytics-engineering/neo4j-graphql-skill.md) — Build and configure a GraphQL API backed by Neo4j using @neo4j/graphql v7 (current) or v5 (LTS)
- [neo4j-graphrag-skill](../notes/analytics-engineering/neo4j-graphrag-skill.md) — Build GraphRAG retrieval pipelines on Neo4j using the neo4j-graphrag Python package (v1.16.0+)
- [neo4j-import-skill](../notes/analytics-engineering/neo4j-import-skill.md) — Import structured data into Neo4j — LOAD CSV, CALL IN TRANSACTIONS, neo4j-admin database import full (offline bulk), apoc.load.csv/json, apoc.periodic.iterate, driver batch writes
- [neo4j-kafka-skill](../notes/analytics-engineering/neo4j-kafka-skill.md) — Configure and operate the Neo4j Connector for Kafka (sink + source) and the native Neo4j CDC API
- [neo4j-mcp-skill](../notes/analytics-engineering/neo4j-mcp-skill.md) — Use when installing, configuring, or troubleshooting the official Neo4j MCP server (neo4j/mcp) — connecting Claude Code, Claude Desktop, Cursor, Windsurf, VS Code, Kiro, or other...
- [neo4j-migration-skill](../notes/analytics-engineering/neo4j-migration-skill.md) — Migrates Neo4j driver code and Cypher queries from older versions (4.x, 5.x) to current (2025.x/2026.x, Cypher 25)
- [neo4j-modeling-skill](../notes/analytics-engineering/neo4j-modeling-skill.md) — Design, review, and refactor Neo4j graph data models
- [neo4j-nvl-skill](../notes/analytics-engineering/neo4j-nvl-skill.md) — Neo4j Visualization Library (NVL) — framework-agnostic graph rendering for the browser
- [neo4j-query-tuning-skill](../notes/analytics-engineering/neo4j-query-tuning-skill.md) — Diagnoses and fixes slow Neo4j Cypher queries by reading execution plans, identifying bad operators (AllNodesScan, CartesianProduct, Eager, NodeByLabelScan), and prescribing fixes...
- [neo4j-security-skill](../notes/analytics-engineering/neo4j-security-skill.md) — Programmatic security management in Neo4j — RBAC/ABAC, user lifecycle (CREATE/ALTER/DROP USER), role lifecycle (CREATE/GRANT ROLE/DROP ROLE), privilege grants and denies...
- [neo4j-snowflake-graph-analytics-skill](../notes/analytics-engineering/neo4j-snowflake-graph-analytics-skill.md) — Run Neo4j Graph Analytics algorithms (PageRank, Louvain, WCC, Dijkstra, KNN, Node2Vec, FastRP, GraphSAGE) directly inside Snowflake without moving data
- [neo4j-spark-skill](../notes/analytics-engineering/neo4j-spark-skill.md) — Use when reading from or writing to Neo4j with Apache Spark or Databricks using the Neo4j Connector for Apache Spark 6.0 (org.neo4j.connectors:spark) or 5.x...
- [neo4j-spring-data-skill](../notes/analytics-engineering/neo4j-spring-data-skill.md) — Use when building Spring Boot applications with Neo4j using Spring Data Neo4j (SDN 7.x/8.x) — @Node entity mapping, @Relationship, @RelationshipProperties, Neo4jRepository...
- [neo4j-vector-index-skill](../notes/analytics-engineering/neo4j-vector-index-skill.md) — Create and manage Neo4j vector indexes, run vector similarity search (ANN/kNN), store embeddings on nodes or relationships, use SEARCH clause (Neo4j 2026.01+, preferred) or...
- [observability-and-instrumentation](../notes/analytics-engineering/observability-and-instrumentation.md) — Instruments code so production behavior is visible and diagnosable
- [phoenix-cli](../notes/analytics-engineering/phoenix-cli.md) — Debug LLM applications using the Phoenix CLI
- [phoenix-evals](../notes/analytics-engineering/phoenix-evals.md) — Build and run evaluators for AI/LLM applications using Phoenix
- [redis-clustering](../notes/analytics-engineering/redis-clustering.md) — Redis Cluster and replication guidance covering hash tags for multi-key operations, avoiding CROSSSLOT errors, and reading from replicas to scale read-heavy workloads
- [redis-connections](../notes/analytics-engineering/redis-connections.md) — Redis client and connection guidance covering connection pooling, multiplexing, pipelining, client-side caching with RESP3, avoiding slow commands (KEYS, SMEMBERS, HGETALL), and tuning...
- [redis-core](../notes/analytics-engineering/redis-core.md) — Core Redis modeling guidance — choose the right data structure (String, Hash, List, Set, Sorted Set, JSON, Stream, Vector Set) and use consistent colon-separated key names
- [redis-observability](../notes/analytics-engineering/redis-observability.md) — Redis observability guidance — which metrics to monitor (memory, connections, hit ratio, ops/sec, rejected connections), which built-in commands to reach for during incident triage...
- [redis-search](../notes/analytics-engineering/redis-search.md) — Redis Search guidance covering FT.CREATE schema design, field type selection (TEXT, TAG, NUMERIC, GEO, GEOSHAPE, VECTOR, JSON path), DIALECT 2 query syntax, FT.SEARCH / FT.AGGREGATE /...
- [redis-security](../notes/analytics-engineering/redis-security.md) — Redis security guidance covering authentication (requirepass and ACL users), TLS, ACL-based least-privilege access control, restricting network exposure via bind and protected-mode...
- [redis-semantic-cache](../notes/analytics-engineering/redis-semantic-cache.md) — Redis LangCache guidance for semantic caching of LLM responses on Redis Cloud — calling search/set via the SDK or REST API, tuning the similarity threshold, separating caches per task...
- [running-dbt-commands](../notes/analytics-engineering/running-dbt-commands.md) — Formats and executes dbt CLI commands, selects the correct dbt executable, and structures command parameters
- [troubleshooting-dbt-job-errors](../notes/analytics-engineering/troubleshooting-dbt-job-errors.md) — Diagnoses dbt Cloud/platform job failures by analyzing run logs, querying the Admin API, reviewing git history, and investigating data issues
- [using-dbt-for-analytics-engineering](../notes/analytics-engineering/using-dbt-for-analytics-engineering.md) — Builds and modifies dbt models, writes SQL transformations using ref() and source(), creates tests, and validates results with dbt show
- [working-with-dbt-mesh](../notes/analytics-engineering/working-with-dbt-mesh.md) — Implements dbt Mesh governance features (model contracts, access modifiers, groups, versioning) and multi-project collaboration with cross-project refs
