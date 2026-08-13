---
name: streamlit
description: Building data apps and dashboards in Python with Streamlit — the top-to-bottom rerun model, st.session_state, caching with st.cache_data/st.cache_resource, forms and st.fragment to limit reruns, multipage apps via st.Page/st.navigation, chat UIs (st.chat_message/st.chat_input), dataframe/plot display, and deployment with streamlit run. Use when building an interactive dashboard, internal data tool, model demo, or chat frontend in pure Python, or when debugging unexpected reruns, lost widget state, or slow Streamlit apps.
---

# Streamlit — Python data apps

## Overview

Streamlit turns a Python script into a web app: **on every user interaction the entire
script reruns top to bottom**, and whatever you call (`st.write`, `st.slider`, …) renders
in order. No callbacks-first architecture, no HTML — state and caching primitives make the
rerun model fast. Best for dashboards, internal tools, and data exploration over
[[pandas]] dataframes and [[matplotlib]]/[[seaborn]] plots. For ML model demos with
image/audio widgets and a shareable API, consider [[gradio]] instead (see below).

Verified against **streamlit 1.61** (Python 3.10+).

```bash
uv add streamlit
uv run streamlit run app.py                  # serves on :8501, auto-reruns on file save
```

## The rerun model (internalize this first)

```python
import streamlit as st

n = st.slider("n", 1, 100, 10)     # moving the slider RERUNS the whole script
st.write(n ** 2)                   # ...so this is always up to date
```

Implications:

- Every widget interaction = full script rerun. Expensive work must be cached or the app crawls.
- Plain Python variables reset on each rerun — persist across reruns with `st.session_state`.
- `st.button` returns `True` only on the rerun triggered by its click, then `False` again.
  For persistent toggles use `st.checkbox`/`st.toggle` or store a flag in session state.
- Force an immediate rerun with `st.rerun()`; abort the rest of the script with `st.stop()`.
  (`st.experimental_rerun` is gone — use `st.rerun`.)

## Session state

```python
if "count" not in st.session_state:
    st.session_state.count = 0            # attribute or dict access, both work

def increment():
    st.session_state.count += 1

st.button("+1", on_click=increment)       # callbacks run BEFORE the rerun
st.write(st.session_state.count)
```

Widgets with a `key=` auto-mirror into session state: `st.text_input("Name", key="name")`
→ `st.session_state.name`. Setting `st.session_state.name = "x"` *before* the widget runs
programmatically controls it. State is per browser tab and lost on page refresh.

## Caching

```python
@st.cache_data(ttl="1h", max_entries=100)   # data: DataFrames, lists, API responses
def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

@st.cache_resource                           # resources: models, DB connections
def get_model():
    return load_heavy_model()
```

- `st.cache_data` — for serializable *data*. Returns a **copy** per call, so mutating the
  result is safe. Keyed on function arguments + code.
- `st.cache_resource` — for global *resources* (ML models, connections). Returns the
  **same shared object** to every session — never mutate it per-user.
- Unhashable args: prefix with `_` to exclude (`def f(_conn, query):`) or pass `hash_funcs`.
- Invalidate with `load_data.clear()` or `st.cache_data.clear()`.

## Limiting reruns: forms and fragments

```python
with st.form("params"):                      # form widgets DON'T rerun on each keystroke
    lo = st.number_input("low")
    hi = st.number_input("high")
    submitted = st.form_submit_button("Run") # one rerun, on submit
if submitted:
    run_expensive_thing(lo, hi)
```

```python
@st.fragment                                  # interactions inside rerun ONLY the fragment
def filter_panel():
    col = st.selectbox("column", df.columns)
    st.dataframe(df[df[col] > st.slider("min", 0, 100)])

filter_panel()

@st.fragment(run_every="10s")                 # auto-refreshing fragment (live metrics)
def live_kpis():
    st.metric("Orders", fetch_count())
```

`st.rerun(scope="fragment")` reruns just the fragment; a fragment cannot write to
containers created outside itself except via `st.session_state` + full rerun.

## Multipage apps

```python
# app.py — entrypoint defines navigation; run: streamlit run app.py
import streamlit as st

pg = st.navigation({
    "Explore": [st.Page("pages/data.py", title="Data", icon=":material/table:"),
                st.Page(chart_page, title="Charts")],   # a function works too
    "Admin":   [st.Page("pages/settings.py")],
})
st.set_page_config(page_title="My app", layout="wide")   # runs before every page
pg.run()
```

Code above `pg.run()` executes on every page — put shared state init, auth, and sidebar
widgets there. Switch pages programmatically with `st.switch_page("pages/data.py")`.

## Chat UIs

```python
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:                      # replay history each rerun
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        reply = st.write_stream(stream_llm(prompt))      # accepts any generator
    st.session_state.messages.append({"role": "assistant", "content": reply})
```

`st.write_stream` renders tokens as they arrive and returns the full concatenated string.
`st.chat_input(accept_file=True)` also takes uploads.

## Data display and layout

```python
st.dataframe(df, width="stretch")        # sortable, scrollable; st.data_editor = editable
st.metric("Revenue", f"${rev:,.0f}", delta=f"{pct:+.1%}")
st.line_chart(df, x="date", y="value")   # quick built-ins; also st.bar_chart, st.scatter_chart

fig, ax = plt.subplots()                 # matplotlib/seaborn: pass the figure explicitly
sns.histplot(df["x"], ax=ax)
st.pyplot(fig)                           # also: st.plotly_chart(fig), st.altair_chart(c)

left, right = st.columns(2)              # layout: columns, tabs, sidebar, expander
left.dataframe(df); right.pyplot(fig)
with st.sidebar: model = st.selectbox("Model", names)
tab1, tab2 = st.tabs(["Data", "Charts"])
```

## Deployment & config

```bash
streamlit run app.py --server.port 8501 --server.headless true
```

- Config in `.streamlit/config.toml` (`[server]`, `[theme]`); secrets in
  `.streamlit/secrets.toml`, read via `st.secrets["api_key"]` — never commit that file.
- One Python process serves all sessions; heavy CPU work blocks other users — cache it,
  or offload to a separate service (e.g. a [[fastapi]] backend).
- Containerize with a plain `CMD ["streamlit", "run", "app.py"]`; Streamlit Community
  Cloud deploys straight from a GitHub repo.
- Headless testing without a browser: `from streamlit.testing.v1 import AppTest`, then
  `at = AppTest.from_file("app.py").run(); at.button[0].click().run()`.

## Streamlit vs Gradio

Same niche (Python → web UI), different center of gravity. **Streamlit**: script-rerun
model, best for dashboards, multipage internal tools, and dataframe-heavy exploration.
**[[gradio]]**: function-wrapping model (`fn(inputs) -> outputs`), best for ML model demos —
richer media I/O components, a free public share link (`share=True`), auto-generated API
clients, and first-class Hugging Face Spaces hosting. If the app is "a UI around one
model/function", pick Gradio; if it's "an interactive report/tool", pick Streamlit.

## Gotchas

- **Uncached expensive work** reruns on every interaction — the #1 slow-app cause.
- **Mutating a `st.cache_resource` object** leaks state across all users; only mutate
  copies from `st.cache_data`.
- **`st.button` is momentary** — its `True` lasts one rerun. Persist intent in
  `st.session_state`.
- **Duplicate widget error**: two identical widgets need distinct `key=` values.
- **Callbacks (`on_click`/`on_change`) run before the script reruns** — mutate session
  state there, don't call `st.write` in them.
- **Widget state vanishes** when the widget stops being rendered (e.g. hidden behind a
  conditional) — its session-state key is dropped too.

## Related

Sibling UI framework: [[gradio]] (ML demos, share links). Data wrangling in [[pandas]];
plots via [[matplotlib]] / [[seaborn]]. Serve heavy compute behind [[fastapi]] and call it
from the app.
