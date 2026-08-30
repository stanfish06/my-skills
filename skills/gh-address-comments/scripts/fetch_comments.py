#!/usr/bin/env python3
"""
Fetch all PR conversation comments + reviews + review threads (inline threads)
for the PR associated with the current git branch, by shelling out to:

  gh api graphql

Requires:
  - `gh auth login` already set up
  - current branch has an associated (open) PR

Usage:
  python fetch_comments.py > pr_comments.json
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from typing import Any

QUERY = """\
query(
  $owner: String!,
  $repo: String!,
  $number: Int!,
  $commentsFirst: Int!,
  $reviewsFirst: Int!,
  $threadsFirst: Int!,
  $commentsCursor: String,
  $reviewsCursor: String,
  $threadsCursor: String
) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $number) {
      number
      url
      title
      state

      # Top-level "Conversation" comments (issue comments on the PR)
      comments(first: $commentsFirst, after: $commentsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          body
          createdAt
          updatedAt
          author { login }
        }
      }

      # Review submissions (Approve / Request changes / Comment), with body if present
      reviews(first: $reviewsFirst, after: $reviewsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          state
          body
          submittedAt
          author { login }
        }
      }

      # Inline review threads (grouped), includes resolved state
      reviewThreads(first: $threadsFirst, after: $threadsCursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          isResolved
          isOutdated
          path
          line
          diffSide
          startLine
          startDiffSide
          originalLine
          originalStartLine
          resolvedBy { login }
          comments(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              id
              body
              createdAt
              updatedAt
              author { login }
            }
          }
        }
      }
    }
  }
}
"""

THREAD_COMMENTS_QUERY = """\
query($id: ID!, $after: String) {
  node(id: $id) {
    ... on PullRequestReviewThread {
      comments(first: 100, after: $after) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          body
          createdAt
          updatedAt
          author { login }
        }
      }
    }
  }
}
"""

PAGE_SIZE = 100


def _run(cmd: list[str], stdin: str | None = None) -> str:
    p = subprocess.run(cmd, input=stdin, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{p.stderr}")
    return p.stdout


def _run_json(cmd: list[str], stdin: str | None = None) -> dict[str, Any]:
    out = _run(cmd, stdin=stdin)
    try:
        return json.loads(out)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON from command output: {e}\nRaw:\n{out}") from e


def _ensure_gh_authenticated() -> None:
    try:
        _run(["gh", "auth", "status"])
    except RuntimeError:
        print("run `gh auth login` to authenticate the GitHub CLI", file=sys.stderr)
        raise RuntimeError("gh auth status failed; run `gh auth login` to authenticate the GitHub CLI") from None


def gh_pr_view_json(fields: str) -> dict[str, Any]:
    # fields is a comma-separated list like: "number,headRepositoryOwner,headRepository"
    return _run_json(["gh", "pr", "view", "--json", fields])


def get_current_pr_ref() -> tuple[str, str, int]:
    """
    Resolve the PR for the current branch (whatever gh considers associated).

    PR numbers live on the base repository, so owner/repo come from the PR url --
    reading headRepository resolves a fork PR against the fork, which either fails
    or silently returns a different PR that happens to share the number.
    `gh pr view --json` exposes no baseRepository field.
    """
    pr = gh_pr_view_json("number,url")
    number = int(pr["number"])
    m = re.match(r"^https?://[^/]+/([^/]+)/([^/]+)/pull/\d+", pr["url"])
    if not m:
        raise RuntimeError(f"Could not parse owner/repo from PR url: {pr['url']!r}")
    return m.group(1), m.group(2), number


def gh_api_graphql(
    owner: str,
    repo: str,
    number: int,
    comments_first: int = PAGE_SIZE,
    reviews_first: int = PAGE_SIZE,
    threads_first: int = PAGE_SIZE,
    comments_cursor: str | None = None,
    reviews_cursor: str | None = None,
    threads_cursor: str | None = None,
) -> dict[str, Any]:
    """
    Call `gh api graphql` using -F variables, avoiding JSON blobs with nulls.
    Query is passed via stdin using query=@- to avoid shell newline/quoting issues.
    """
    cmd = [
        "gh",
        "api",
        "graphql",
        "-F",
        "query=@-",
        "-F",
        f"owner={owner}",
        "-F",
        f"repo={repo}",
        "-F",
        f"number={number}",
        "-F",
        f"commentsFirst={comments_first}",
        "-F",
        f"reviewsFirst={reviews_first}",
        "-F",
        f"threadsFirst={threads_first}",
    ]
    if comments_cursor:
        cmd += ["-F", f"commentsCursor={comments_cursor}"]
    if reviews_cursor:
        cmd += ["-F", f"reviewsCursor={reviews_cursor}"]
    if threads_cursor:
        cmd += ["-F", f"threadsCursor={threads_cursor}"]

    return _run_json(cmd, stdin=QUERY)


def fetch_thread_comments(thread_id: str, after: str | None) -> list[dict[str, Any]]:
    """Drain a review thread's comments past the first page."""
    out: list[dict[str, Any]] = []
    while after:
        payload = _run_json(
            ["gh", "api", "graphql", "-F", "query=@-", "-F", f"id={thread_id}", "-F", f"after={after}"],
            stdin=THREAD_COMMENTS_QUERY,
        )
        if payload.get("errors"):
            raise RuntimeError(f"GitHub GraphQL errors:\n{json.dumps(payload['errors'], indent=2)}")
        conn = payload["data"]["node"]["comments"]
        out.extend(conn.get("nodes") or [])
        after = conn["pageInfo"]["endCursor"] if conn["pageInfo"]["hasNextPage"] else None
    return out


def fetch_all(owner: str, repo: str, number: int) -> dict[str, Any]:
    conversation_comments: list[dict[str, Any]] = []
    reviews: list[dict[str, Any]] = []
    review_threads: list[dict[str, Any]] = []

    comments_cursor: str | None = None
    reviews_cursor: str | None = None
    threads_cursor: str | None = None

    # each connection is drained independently -- once one is exhausted its page size
    # drops to 0, otherwise it would re-fetch page 1 on every remaining iteration
    comments_more = True
    reviews_more = True
    threads_more = True

    pr_meta: dict[str, Any] | None = None

    while comments_more or reviews_more or threads_more:
        payload = gh_api_graphql(
            owner=owner,
            repo=repo,
            number=number,
            comments_first=PAGE_SIZE if comments_more else 0,
            reviews_first=PAGE_SIZE if reviews_more else 0,
            threads_first=PAGE_SIZE if threads_more else 0,
            comments_cursor=comments_cursor,
            reviews_cursor=reviews_cursor,
            threads_cursor=threads_cursor,
        )

        if "errors" in payload and payload["errors"]:
            raise RuntimeError(f"GitHub GraphQL errors:\n{json.dumps(payload['errors'], indent=2)}")

        pr = payload["data"]["repository"]["pullRequest"]
        if pr_meta is None:
            pr_meta = {
                "number": pr["number"],
                "url": pr["url"],
                "title": pr["title"],
                "state": pr["state"],
                "owner": owner,
                "repo": repo,
            }

        c = pr["comments"]
        r = pr["reviews"]
        t = pr["reviewThreads"]

        if comments_more:
            conversation_comments.extend(c.get("nodes") or [])
            comments_more = c["pageInfo"]["hasNextPage"]
            comments_cursor = c["pageInfo"]["endCursor"] if comments_more else None

        if reviews_more:
            reviews.extend(r.get("nodes") or [])
            reviews_more = r["pageInfo"]["hasNextPage"]
            reviews_cursor = r["pageInfo"]["endCursor"] if reviews_more else None

        if threads_more:
            for thread in t.get("nodes") or []:
                tc = thread.get("comments") or {}
                page = tc.get("pageInfo") or {}
                if page.get("hasNextPage"):
                    tc["nodes"] = (tc.get("nodes") or []) + fetch_thread_comments(
                        thread["id"], page.get("endCursor")
                    )
                    tc.pop("pageInfo", None)
                else:
                    tc.pop("pageInfo", None)
            review_threads.extend(t.get("nodes") or [])
            threads_more = t["pageInfo"]["hasNextPage"]
            threads_cursor = t["pageInfo"]["endCursor"] if threads_more else None

    assert pr_meta is not None
    return {
        "pull_request": pr_meta,
        "conversation_comments": conversation_comments,
        "reviews": reviews,
        "review_threads": review_threads,
    }


def main() -> None:
    _ensure_gh_authenticated()
    owner, repo, number = get_current_pr_ref()
    result = fetch_all(owner, repo, number)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
