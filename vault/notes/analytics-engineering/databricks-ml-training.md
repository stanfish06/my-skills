---
title: databricks-ml-training
aliases:
  - databricks ml training
tags:
  - skill
  - domain/analytics-engineering
domain: analytics-engineering
status: untried
source: skills/databricks-ml-training/SKILL.md
created: 2026-08-23
---

# databricks-ml-training

> [!info] What it does
> Train ML models on Databricks. Use for: classification/regression/deep-learning (XGBoost, scikit-learn, LightGBM, PyTorch) with Optuna, @prod/@challenger aliases, batch scoring (spark_udf for plain models, fe.score_batch for feature-store-backed), custom PyFunc, custom ResponsesAgent (LangGraph + UC Function/Vector Search); UC feature tables + FeatureLookup + point-in-time joins + Lakebase online store; declarative Feature Views (create_feature, DeltaTableSource, RollingWindow/SlidingWindow/TumblingWindow, materialize_features, streaming Kafka features). NOT for: endpoint ops (databricks-model-serving), MLflow evaluation (databricks-mlflow-evaluation).

**Source:** [skills/databricks-ml-training/SKILL.md](../../../skills/databricks-ml-training/SKILL.md)  ·  **Domain:** [Analytics Engineering & LLM Operations](../../maps/analytics-engineering.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [databricks-mlflow-evaluation](../../notes/analytics-engineering/databricks-mlflow-evaluation.md) — MLflow 3 GenAI agent evaluation. Use when writing mlflow.genai.evaluate() code, creating @scorer functions, using built-in scorers (Guidelines, Correctness, Safety...
- [databricks-model-serving](../../notes/analytics-engineering/databricks-model-serving.md) — Databricks Model Serving endpoint lifecycle and ops
- [langgraph](../../notes/uncategorized/langgraph.md) — LangGraph is a low-level orchestration framework for building stateful LLM agents and workflows as explicit graphs — typed state with reducers, nodes/edges/conditional routing...
- [optuna](../../notes/ml-ai/optuna.md) — Hyperparameter optimization (HPO) for ML models using Optuna
- [scikit-learn](../../notes/ml-ai/scikit-learn.md) — Machine learning in Python with scikit-learn

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
