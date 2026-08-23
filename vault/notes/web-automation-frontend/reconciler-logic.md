---
title: reconciler-logic
aliases:
  - reconciler logic
tags:
  - skill
  - domain/web-automation-frontend
domain: web-automation-frontend
status: untried
source: skills/reconciler-logic/SKILL.md
created: 2026-08-23
---

# reconciler-logic

> [!info] What it does
> Implement reconcilers and watchers for grafana-app-sdk apps — write `TypedReconciler[*MyKind]` reconcile functions, apply generation-based skip patterns, do conflict-safe status updates via `resource.UpdateObject`, configure `BasicReconcileOptions` (namespace, label/field filters, finalizer management), use `Watcher` for event-style handling, reconcile `UnmanagedKinds` (resources your app doesn't own), and register the whole thing in `app.go`. Use when writing a reconciler, implementing the reconcile loop, adding async business logic, handling create/update/delete events, processing resource state changes, scheduling periodic resyncs with `RequeueAfter`, picking between Watcher and Reconciler, or wiring a controller into `app.go` — even when the user says "process this resource", "handle X events", or "write a controller" without saying "reconciler".

**Source:** [skills/reconciler-logic/SKILL.md](../../../skills/reconciler-logic/SKILL.md)  ·  **Domain:** [Web Automation, Frontend & Design](../../maps/web-automation-frontend.md)  ·  **Table:** [skills.base](../../skills.base)  ·  **Index:** [Skills Index](../../index.md)

## Related skills

- [implement](../../notes/software-dev/implement.md) — Implement a piece of work based on a spec or set of tickets

%% ---8<--- personal notes below are preserved on re-run ---8<--- %%

## Notes
