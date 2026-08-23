#!/usr/bin/env python3
"""Graph-aware skill retrieval over the vault knowledge graph.

Five stages (docs/superpowers/specs/2026-08-12-vault-knowledge-graph-design.md sec. 6):

  A route         match the query to domains/artifacts — a ~2k-token index
                  instead of the ~162k tokens of every skill description
  B seed          BM25 over name + aliases + description within the route
  C expand        graph traversal: prerequisites back, chains forward,
                  alternatives sideways
  D set-complete  pull the rest of a Recipe hyperedge when >=2 members hit.
                  This is the stage that fixes COMP, not Recall — a retriever
                  with Recall@3 68.6% had COMP@3 39.7% (HYSET); finding scanpy
                  but missing harmonypy is a failed answer, not a partial one.
  E order+budget  topological by chains_to, capped, with why-included provenance

Stdlib only. Reads vault/graph/graph.json.

Usage:
  python3 .skill-vault/kg/query.py "batch correct single cell data and find markers"
  python3 .skill-vault/kg/query.py "fastq to pathways" --k 10 --json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(os.environ.get("SKILL_VAULT_ROOT") or Path(__file__).resolve().parents[2])
GRAPH_PATH = ROOT / "vault" / "graph" / "graph.json"
WORD = re.compile(r"[a-z0-9]+")
SKILL_TYPES = ("Skill", "ExpertProfile")

# Which provenance levels an agent may act on. Read from the graph's own
# metrics, which build_kg stamps from schema.json, so the vocabulary lives in
# the TBox alone rather than in a third hardcoded copy here. The fallback keeps
# query.py working against a graph built before the field existed; PROPOSED is
# excluded either way (shape P4/S4).
RETRIEVABLE_FALLBACK = frozenset({"ASSERTED", "OBSERVED", "EXTRACTED", "INFERRED"})


def tok(text):
    return WORD.findall((text or "").lower())


class VaultGraph:
    def __init__(self, path=GRAPH_PATH):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        self.nodes = {n["id"]: n for n in data["nodes"]}
        self.recipes = data.get("recipes", [])
        retrievable = frozenset(
            data.get("metrics", {}).get("retrievable_provenance") or RETRIEVABLE_FALLBACK)
        self.edge_count = len(data["edges"])
        self.out = defaultdict(lambda: defaultdict(set))
        self.inn = defaultdict(lambda: defaultdict(set))
        for e in data["edges"]:
            if e.get("provenance") not in retrievable:
                continue
            self.out[e["src"]][e["rel"]].add(e["dst"])
            self.inn[e["dst"]][e["rel"]].add(e["src"])
        self.skills = [n["id"] for n in data["nodes"] if n.get("type") in SKILL_TYPES]

        # BM25 index over name + description + domain labels. Term frequencies are
        # counted once here, not per query: bm25() is called for every skill on
        # every query, and recounting each document there was the whole cost.
        self.tf, self.dl, df = {}, {}, defaultdict(int)
        for sid in self.skills:
            n = self.nodes[sid]
            doms = " ".join(d.split(":", 1)[1].replace("-", " ")
                            for d in self.out[sid].get("in_domain", ()))
            aliases = " ".join(n.get("aliases") or ())
            words = (tok(sid.replace("-", " ")) * 3
                     + tok(n.get("description", "")) + tok(doms) + tok(aliases))
            self.tf[sid] = Counter(words)
            self.dl[sid] = len(words)
            for w in self.tf[sid]:
                df[w] += 1
        self.df = df
        self.N = len(self.skills)
        self.avglen = sum(self.dl.values()) / max(1, self.N)

    def bm25(self, qwords, sid, k1=1.5, b=0.75):
        tf, dl = self.tf[sid], self.dl[sid]
        if not dl:
            return 0.0
        score = 0.0
        for w in qwords:
            f = tf.get(w)
            if not f:
                continue
            idf = math.log(1 + (self.N - self.df[w] + 0.5) / (self.df[w] + 0.5))
            score += idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * dl / self.avglen))
        return score

    def neighbours(self, sid, rels):
        r = set()
        for rel in rels:
            r |= self.out[sid].get(rel, set()) | self.inn[sid].get(rel, set())
        return {x for x in r if self.nodes.get(x, {}).get("type") in SKILL_TYPES}


def retrieve(g: VaultGraph, query: str, k: int = 8):
    qwords = tok(query)
    picks = {}          # sid -> (score, why)

    def offer(sid, score, why):
        if sid not in g.nodes or g.nodes[sid].get("type") not in SKILL_TYPES:
            return
        if g.nodes[sid].get("deprecated"):
            return
        if sid not in picks or score > picks[sid][0]:
            picks[sid] = (score, why)

    # --- A/B route + seed -------------------------------------------------
    scored = sorted(((g.bm25(qwords, s), s) for s in g.skills), reverse=True)
    seeds = []
    for sc, s in scored[:k]:
        if sc > 0:
            seeds.append(s)
            prior = 1.0 + (g.nodes[s].get("success_rate") or 0) * 0.5
            offer(s, sc * prior, "matched the query directly")

    # --- C expand ---------------------------------------------------------
    # Every traversal is sorted. The adjacency is sets, and derived picks all
    # share a handful of scores, so ties fall back to insertion order — leaving
    # these unsorted made the answer depend on set iteration order, i.e. on
    # PYTHONHASHSEED. Same query, same graph, different skills per process.
    for s in seeds:
        for p in sorted(g.inn[s].get("chains_to", set()) | g.inn[s].get("prerequisite_of", set())):
            offer(p, 0.6, f"produces input for {s}")
        for nxt in sorted(g.out[s].get("chains_to", set())):
            offer(nxt, 0.6, f"consumes what {s} produces")
        for alt in sorted(g.neighbours(s, ["alternative_to"])):
            offer(alt, 0.4, f"alternative to {s}")
        for co in sorted(g.neighbours(s, ["co_occurs_with"]))[:4]:
            offer(co, 0.5, f"usually used together with {s}")

    # --- D set-complete: the COMP fix ------------------------------------
    chosen = set(picks)
    completions = []
    for r in g.recipes:
        members = set(r["members"])
        hits = members & chosen
        if len(hits) >= 2:
            for m in r["steps"] or sorted(members):
                if m not in picks:
                    completions.append((m, r["label"]))
                offer(m, 0.55, f"completes the '{r['label']}' workflow")

    # --- E order + budget -------------------------------------------------
    # Reserve slots for graph-derived skills. Without this, BM25 fills every
    # slot whenever the query has strong lexical hits and stage D contributes
    # nothing — which is exactly the Recall-good/COMP-bad failure it exists to
    # fix. Direct matches get at most ceil(0.7k); the rest goes to the graph.
    direct = sorted(((s, v) for s, v in picks.items() if v[1] == "matched the query directly"),
                    key=lambda kv: -kv[1][0])
    derived = sorted(((s, v) for s, v in picks.items() if v[1] != "matched the query directly"),
                     key=lambda kv: -kv[1][0])
    ranked = direct[:math.ceil(k * 0.7)]
    ranked += derived[:k - len(ranked)]
    if len(ranked) < k:
        taken = {s for s, _ in ranked}
        ranked += [(s, v) for s, v in direct if s not in taken][: k - len(ranked)]

    order = {sid: i for i, (sid, _) in enumerate(ranked)}
    # topological nudge: a skill that feeds another in the set comes first
    for _ in range(3):
        for sid, _ in ranked:
            for nxt in sorted(g.out[sid].get("chains_to", set())):
                if nxt in order and order[nxt] < order[sid]:
                    order[sid], order[nxt] = order[nxt], order[sid]
    ranked.sort(key=lambda kv: order[kv[0]])

    return [
        {
            "skill": sid,
            "score": round(score, 3),
            "why": why,
            "description": (g.nodes[sid].get("description") or "")[:160],
            "source": g.nodes[sid].get("source") or f"skills/{sid}/SKILL.md",
            "domains": sorted(d.split(":", 1)[1] for d in g.out[sid].get("in_domain", ())),
        }
        for sid, (score, why) in ranked
    ], completions


def main():
    ap = argparse.ArgumentParser(description=(__doc__ or "").split("\n")[0])
    ap.add_argument("query", nargs="+")
    ap.add_argument("--k", type=int, default=8, help="max skills to return (SkillGraph K_max=8)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    query = " ".join(args.query)

    if not GRAPH_PATH.is_file():
        raise SystemExit(f"no graph at {GRAPH_PATH} — run build_kg.py first")
    g = VaultGraph()
    results, completions = retrieve(g, query, args.k)

    if args.json:
        print(json.dumps({"query": query, "results": results}, indent=1))
        return 0

    print(f'query: "{query}"   ({len(g.skills)} skills, {g.edge_count} edges)\n')
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['skill']}   [{', '.join(r['domains']) or 'no domain'}]")
        print(f"   why:  {r['why']}")
        if r["description"]:
            print(f"   what: {r['description']}")
        print(f"   read: {r['source']}")
    if completions:
        uniq = sorted({c for c, _ in completions})
        print(f"\nset-completion pulled in {len(uniq)} skill(s) the query text alone would have missed:")
        for c, label in sorted(set(completions)):
            print(f"   {c}  (from '{label}')")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
