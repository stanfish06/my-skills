---
name: langgraph
description: LangGraph is a low-level orchestration framework for building stateful LLM agents and workflows as explicit graphs — typed state with reducers, nodes/edges/conditional routing, checkpointer-backed persistence and thread memory, human-in-the-loop interrupts, and streaming. Use when building an agent or multi-step LLM workflow that needs explicit control flow (branching, loops, parallel fan-out), durable/resumable execution, approval gates, or multi-agent handoffs — or when debugging StateGraph, checkpointer, interrupt, or create_react_agent-deprecation issues. Targets LangGraph 1.x.
---

# LangGraph — stateful agent graphs

## Overview

LangGraph (from the LangChain team, but usable without `langchain`) models an LLM
workflow as an explicit state machine: a typed **state** schema, **nodes** (functions
that return state updates), and **edges** (fixed or conditional routing). A built-in
**checkpointer** persists state after every step, which is what enables thread-scoped
memory, time travel, interrupts, and fault tolerance.

Reach for LangGraph when you need to see and control every transition — branching,
retry loops, parallel fan-out, approval gates, multi-agent handoffs. For a simple
"LLM + tools in a loop", a plain tool-calling loop or [[building-pydantic-ai-agents]]
is less machinery; [[crewai]] fits role-based agent teams; [[dspy]] optimizes the
prompts inside your nodes. Trace/eval graphs with [[langfuse]] and
[[llm-observability-evals]].

```bash
uv add langgraph                 # verified against langgraph 1.2.11, Python >=3.10
uv add langchain                 # only for the prebuilt agent / model bindings
```

## StateGraph fundamentals

```python
from typing import Annotated, Literal
from typing_extensions import TypedDict
from operator import add
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    text: str                              # no reducer: each update REPLACES
    steps: Annotated[list[str], add]       # reducer: updates are APPENDED

def classify(state: State):
    return {"steps": ["classify"]}         # nodes return partial updates, not full state

def route(state: State) -> Literal["short", "long"]:
    return "short" if len(state["text"]) < 10 else "long"

def short(state: State):
    return {"steps": ["short"], "text": state["text"].upper()}

def long(state: State):
    return {"steps": ["long"], "text": state["text"][:10]}

builder = StateGraph(State)
builder.add_node("classify", classify)
builder.add_node("short", short)
builder.add_node("long", long)
builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route)   # router's return value = next node
builder.add_edge("short", END)
builder.add_edge("long", END)

graph = builder.compile()                  # MUST compile before use
graph.invoke({"text": "hi", "steps": []})
# {'text': 'HI', 'steps': ['classify', 'short']}
```

- State is a `TypedDict` (Pydantic models and dataclasses also work). A reducer
  (`Annotated[type, fn]`) defines how a node's update merges into the current value;
  without one the update overwrites. For chat agents use the message reducer:
  `messages: Annotated[list, add_messages]` (`from langgraph.graph.message import add_messages`).
- `add_conditional_edges(source, router)` routes to whatever node name the router
  returns; pass a dict as third arg to map return values to node names.
- A node can update state **and** route in one shot by returning a `Command`:

```python
from langgraph.types import Command

def a(state: State) -> Command[Literal["b", "c"]]:      # type hint enables graph rendering
    return Command(update={"n": state["n"] + 1}, goto="b" if state["n"] < 5 else "c")
```

## Persistence and thread memory

A checkpointer saves a snapshot after every super-step, keyed by `thread_id`.
Same thread = continued conversation/state; new thread = clean slate.

```python
from langgraph.checkpoint.memory import InMemorySaver

graph = builder.compile(checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "user-42"}}

graph.invoke({"messages": [{"role": "user", "content": "hi, I'm Bob"}]}, config)
graph.invoke({"messages": [{"role": "user", "content": "my name?"}]}, config)  # remembers

snapshot = graph.get_state(config)          # inspect current state
history = list(graph.get_state_history(config))   # time travel
```

`InMemorySaver` dies with the process. For production install
`langgraph-checkpoint-sqlite` (`SqliteSaver.from_conn_string("state.db")`) or
`langgraph-checkpoint-postgres` (`PostgresSaver`; call `.setup()` once).

## Human-in-the-loop interrupts

`interrupt()` pauses the graph mid-node, surfaces a payload, and waits indefinitely;
resume later (any process, same thread) with `Command(resume=...)`. Requires a
checkpointer + `thread_id`.

```python
from langgraph.types import interrupt, Command

def approval(state: State):
    ok = interrupt({"question": "approve?", "plan": state["plan"]})  # pauses here
    return {"approved": ok}

result = graph.invoke(inputs, config)
result["__interrupt__"]        # [Interrupt(value={'question': 'approve?', ...}, id=...)]

graph.invoke(Command(resume=True), config)   # True becomes interrupt()'s return value
```

On resume the node **re-runs from its top** (interrupt is not a coroutine yield) — keep
side effects after the `interrupt()` call, or make code before it idempotent.

## Streaming

```python
for chunk in graph.stream(inputs, config, stream_mode="updates"):
    print(chunk)                     # {'node_name': {updated keys}} per step
```

| `stream_mode` | Yields |
|---|---|
| `"values"` | full state snapshot after each step |
| `"updates"` | per-node deltas (default) |
| `"messages"` | `(llm_token_chunk, metadata)` tuples — token streaming from LLM calls inside nodes |
| `"custom"` | whatever nodes emit via `get_stream_writer()` (`from langgraph.config import get_stream_writer`) |
| `"debug"` | detailed trace events |

Pass a list (`stream_mode=["updates", "custom"]`) to multiplex; chunks then arrive as
`(mode, data)` tuples. `astream` is the async twin.

## Prebuilt ReAct agent

`langgraph.prebuilt.create_react_agent` is **deprecated in 1.x** (removal planned for
2.0). The replacement is `create_agent` from the `langchain` package — same
tools-in-a-loop graph, plus a middleware system:

```python
from langchain.agents import create_agent

agent = create_agent(
    model="anthropic:claude-sonnet-4-5",     # provider string needs langchain-anthropic installed
    tools=[search, calculator],              # plain functions or @tool-decorated
    system_prompt="You are a terse research assistant.",   # was `prompt` in create_react_agent
    checkpointer=checkpointer,               # optional: thread memory for free
)
agent.invoke({"messages": [{"role": "user", "content": "..."}]}, config)
```

The result is a compiled LangGraph graph — `stream`, checkpointers, and interrupts all
work on it. Drop to a hand-written `StateGraph` when the agent loop itself needs
custom shape.

## Gotchas

- **Mutating state in a node does nothing** — only the returned dict (merged via
  reducers) counts. Return `{"key": new_value}`, don't `state["key"] = ...`.
- **Missing reducer on list state** silently overwrites accumulated history each step;
  parallel fan-out into the same key without a reducer raises
  `InvalidUpdateError` — annotate with `add` / `add_messages`.
- **`KeyError: '__interrupt__'`-style confusion**: interrupts need a checkpointer AND
  a `thread_id`; resuming must reuse the *same* `thread_id`.
- **Runaway loops no longer fail fast**: old LangGraph raised `GraphRecursionError`
  at 25 steps; current 1.2.x defaults to 10007 (`LANGGRAPH_DEFAULT_RECURSION_LIMIT`).
  Put a real stop condition in your router, or set a low safety rail:
  `graph.invoke(inputs, config={"recursion_limit": 50})`.
- **Old tutorials say `MemorySaver`** — it's `InMemorySaver` now (old name still
  aliased), and `create_react_agent` snippets should be ported to `create_agent`.
- **Checkpoint growth is unbounded** by default in Postgres/SQLite — prune old threads.

## Resources

- Docs: https://docs.langchain.com/oss/python/langgraph/overview
- Source: https://github.com/langchain-ai/langgraph
- Reference: https://reference.langchain.com/python/
