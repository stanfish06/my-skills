---
name: sqlalchemy
description: The standard Python SQL toolkit and ORM — 2.x style only. Covers declarative models with DeclarativeBase/Mapped/mapped_column, engine and session lifecycle, CRUD with select() and Session.scalars(), relationships and eager loading (selectinload vs joinedload), transactions, async engines, and Alembic migrations. Use when defining database models in Python, querying relational databases (PostgreSQL, SQLite, MySQL) from application code, wiring a database into FastAPI, fixing N+1 or DetachedInstanceError problems, or migrating legacy Query-API code to 2.x.
---

# SQLAlchemy — Python SQL toolkit & ORM (2.x)

## Overview

SQLAlchemy 2.x has one query language for Core and ORM: build statements with
`select()`/`insert()`/`update()`, execute them via `Session` (ORM) or `Connection`
(Core). Models are typed dataclass-like declarative classes. This skill is 2.x style
only — the legacy 1.x `session.query(User)` API still runs but should not be written;
`session.query(User).filter_by(...)` becomes
`session.scalars(select(User).filter_by(...))`. Backend for [[fastapi]] services;
load query results into [[pandas]] via `pd.read_sql(stmt, engine)`.

```bash
uv add sqlalchemy                 # + driver: psycopg (PostgreSQL), pymysql (MySQL)
uv add "sqlalchemy[asyncio]" aiosqlite   # async extras + async SQLite driver
```

Verified against SQLAlchemy 2.0.52.

## Declarative models

```python
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str | None]                       # Optional -> nullable column
    posts: Mapped[list["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
```

`Mapped[...]` annotations drive column types and nullability; `mapped_column()` is
only needed for extras (PK, FK, constraints, server defaults). Bare `Mapped[str]`
maps to an unbounded `String` — fine on PostgreSQL/SQLite, but MySQL requires an
explicit length (`String(50)`). Never use 1.x `declarative_base()` / `Column(...)`
in new code.

## Engine & session lifecycle

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg://user:pw@localhost/db", echo=False)
Base.metadata.create_all(engine)        # dev/tests only — use Alembic in production
SessionLocal = sessionmaker(engine)
```

**One engine per process** (it owns the connection pool), **one short-lived session
per unit of work** (per request, per job). Never share a session across threads or
requests. In [[fastapi]], yield a session from a dependency:

```python
def get_db():
    with SessionLocal() as db:
        yield db
```

Set `echo=True` while debugging to log every emitted SQL statement.

## CRUD with select()

```python
from sqlalchemy import func, select

with SessionLocal() as session:
    # create
    session.add(User(name="alice", posts=[Post(title="hello")]))
    session.commit()

    # read — scalars() for whole objects, execute() for column/tuple rows
    users = session.scalars(select(User).order_by(User.name)).all()
    alice = session.scalars(select(User).where(User.name == "alice")).one()
    user = session.get(User, 1)                    # by primary key (or None)
    pairs = session.execute(
        select(User.name, func.count(Post.id)).join(User.posts).group_by(User.name)
    ).all()                                        # list of Row tuples
    n = session.scalar(select(func.count()).select_from(User))

    # update — mutate the object, commit; delete
    alice.email = "a@example.com"
    session.delete(user)
    session.commit()
```

`.all()` / `.first()` / `.one()` / `.one_or_none()` on the result control cardinality.
Bulk operations skip loading objects entirely:
`session.execute(update(User).where(...).values(email=None))` and
`session.execute(delete(User).where(...))`, followed by `session.commit()`.

## Relationships & eager loading

Accessing `user.posts` lazy-loads by default — inside a loop that is the classic
**N+1** (one query per row). Load eagerly instead:

```python
from sqlalchemy.orm import joinedload, selectinload

# selectinload: 2nd query with IN(...) — best default for collections
users = session.scalars(select(User).options(selectinload(User.posts))).all()

# joinedload: one LEFT JOIN — best for many-to-one / one-to-one
posts = session.scalars(select(Post).options(joinedload(Post.author))).all()
```

Rule of thumb: `selectinload` for one-to-many collections (no row explosion),
`joinedload` for scalar relationships. Chain for deeper trees:
`selectinload(User.posts).selectinload(Post.tags)`.

## Transactions

```python
with SessionLocal.begin() as session:   # commit on success, rollback on exception
    session.add(User(name="carol"))
# plain `with SessionLocal() as session:` closes but does NOT commit — call
# session.commit() yourself
```

`session.flush()` sends pending SQL (populating PKs) without committing;
`session.rollback()` resets after a failure.

## Async engine

```python
import asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///app.db")   # or postgresql+asyncpg://
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with AsyncSessionLocal() as session:
        session.add(User(name="carol"))
        await session.commit()
        users = (await session.scalars(select(User))).all()
    await engine.dispose()

asyncio.run(main())
```

Same models and `select()` statements; only execution is awaited. Set
`expire_on_commit=False` so objects stay usable after commit without implicit
(await-less) lazy loads, and eager-load relationships — lazy loading raises under
async.

## Migrations (Alembic)

`create_all` never alters existing tables. For schema evolution:

```bash
uv add alembic && uv run alembic init migrations
# point env.py target_metadata at Base.metadata, set sqlalchemy.url
uv run alembic revision --autogenerate -m "add users"
uv run alembic upgrade head
```

Always review autogenerated migrations — it misses renames (sees drop+add) and
server-default changes.

## Gotchas

- **N+1 queries**: iterating a lazy relationship in a loop. Add `selectinload`/
  `joinedload`, and use `echo=True` to see the flood.
- **`DetachedInstanceError`**: touching lazy attributes after the session closed.
  Eager-load before closing or keep the session open for the object's lifetime.
  `expire_on_commit=False` only keeps *already-loaded* attributes readable after
  commit — it does not make unloaded lazy relationships work when detached.
- **Long-lived / shared sessions**: stale identity map, surprise flushes, pool
  exhaustion. Session-per-request, always.
- **`with Session(...)` does not commit** on exit — use `.begin()` or commit
  explicitly.
- **Legacy 1.x style** (`session.query`, `declarative_base`, `backref`) — works, but
  write `select()` + `Mapped` in anything new; mixing styles confuses reviewers and
  type checkers.
- **SQLite `:memory:`** is per-connection — a second connection sees an empty
  database. Use a file, or share one connection with
  `poolclass=StaticPool, connect_args={"check_same_thread": False}` when tests
  (e.g. FastAPI `TestClient`) hit it from other threads.

## Related

Serve models over HTTP with [[fastapi]]; analyze query results with [[pandas]];
project setup in [[modern-python]]; test with [[pytest]] fixtures around a
per-test session/rollback.
