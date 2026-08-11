---
name: pubmed-search
description: Search PubMed for scientific literature. Use when the user asks to find papers, search literature, look up research, find publications, or asks about recent studies. Triggers on "pubmed", "papers", "literature", "publications", "research on", "studies about".
---

# PubMed Search

> [!note] Vault audit 2026-07-24 — USE-4
> Use this for a single raw PubMed query (Entrez search → results); for a multi-DB scholarly search use `paper-lookup`, and for a synthesized briefing/report use `pubmed-summariser` (PubMed briefing) or `lit-synthesizer` (PubMed+bioRxiv report with citation graph). Distinguishing axis: single query vs multi-DB lookup vs synthesized report.

Search NCBI PubMed for scientific literature using BioPython's Entrez module.

## When to Use

- User asks to find papers on a topic
- User wants recent publications in a field
- User asks for references or citations
- User wants to know the state of research on a topic

## How to Execute

### 1. Set up Entrez

```python
import os
from Bio import Entrez
Entrez.email = os.environ["NCBI_EMAIL"]   # REQUIRED: your own working address.
# NCBI policy requires a real, reachable contact address — it emails heavy users
# before blocking their IP. Never ship a placeholder: any value silences
# Biopython's "Email address is not specified" warning, so a bad address fails silently.
```

### 2. Search PubMed

```python
# Search
handle = Entrez.esearch(db="pubmed", term="CRISPR delivery methods", retmax=20, sort="date")
record = Entrez.read(handle)
handle.close()

id_list = record["IdList"]
print(f"Found {record['Count']} results, showing top {len(id_list)}")
```

### 3. Fetch article details

```python
# Fetch details
handle = Entrez.efetch(db="pubmed", id=id_list, rettype="xml")
records = Entrez.read(handle)
handle.close()

for article in records['PubmedArticle']:
    medline = article['MedlineCitation']
    pmid = str(medline['PMID'])
    title = medline['Article']['ArticleTitle']
    
    # Get authors
    authors = medline['Article'].get('AuthorList', [])
    first_author = f"{authors[0].get('LastName', '')} {authors[0].get('Initials', '')}" if authors else "Unknown"
    
    # Get journal and year
    journal = medline['Article']['Journal']['Title']
    pub_date = medline['Article']['Journal']['JournalIssue'].get('PubDate', {})
    year = pub_date.get('Year', 'N/A')
    
    # Get abstract
    abstract_parts = medline['Article'].get('Abstract', {}).get('AbstractText', [])
    abstract = ' '.join(str(a) for a in abstract_parts)[:300]
    
    print(f"PMID: {pmid}")
    print(f"Title: {title}")
    print(f"Authors: {first_author} et al.")
    print(f"Journal: {journal} ({year})")
    print(f"Abstract: {abstract}...")
    print(f"Link: https://pubmed.ncbi.nlm.nih.gov/{pmid}/")
    print()
```

### 4. Output format

Report in the caller's own format — plain text for a CLI, Markdown where it renders.
Do not emit chat-app markup. Per result: title, first author *et al.*, journal, year,
PMID, and the canonical `https://pubmed.ncbi.nlm.nih.gov/<PMID>/` link. Lead with the
total hit count and how many you are showing. Use the PMIDs actually returned by the
search — never invent one.

### 5. Advanced searches

Support these query patterns:
- `"CRISPR"[Title] AND "delivery"[Title]` — title-specific
- `"2026"[Date - Publication]` — date filter
- `"Nature"[Journal]` — journal filter
- `review[Publication Type]` — type filter

### 6. Follow-up suggestions

After showing results, suggest:
- "Want me to summarize any of these papers?"
- "Should I search with different keywords?"
- "Want me to find related papers to any of these?"
