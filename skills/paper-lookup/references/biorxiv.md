# bioRxiv API

bioRxiv is a preprint server for biology. The API provides metadata for preprints, including title, authors, abstract, DOI, and publication status.

**Important:** The bioRxiv API has **no keyword search**. It supports date-range browsing and DOI lookup only. For keyword search of bioRxiv preprints, use Semantic Scholar, OpenAlex, or CORE instead.

## Base URL

```
https://api.biorxiv.org
```

## Authentication

None required. Fully public API.

## Key Endpoints

### 1. Content Detail -- Browse by date range

```
GET /details/biorxiv/{interval}/{cursor}/{format}
```

| Parameter | Values | Description |
|-----------|--------|-------------|
| `interval` | `YYYY-MM-DD/YYYY-MM-DD` | Date range (inclusive). Keep ranges narrow (1-3 days) to avoid timeouts. |
| | `N` (integer) | N most recent preprints |
| | `Nd` (integer + "d") | Last N days |
| `cursor` | Integer (default `0`) | Record offset. `/details/` returns 30 records per request |
| `format` | `json` (default), `xml` | Response format |

Optional query parameter: `?category=neuroscience` (filter by category, use underscores for spaces; an unrecognized name is silently ignored)

**Examples:**
```
https://api.biorxiv.org/details/biorxiv/2024-01-01/2024-01-31/0
https://api.biorxiv.org/details/biorxiv/5
https://api.biorxiv.org/details/biorxiv/10d
https://api.biorxiv.org/details/biorxiv/2024-01-01/2024-01-31?category=neuroscience
```

### 2. Content Detail -- DOI lookup

```
GET /details/biorxiv/{doi}/na/{format}
```

**Example:**
```
https://api.biorxiv.org/details/biorxiv/10.1101/2024.01.16.575895/na/json
```

### 3. Published Article Links

```
GET /pubs/biorxiv/{interval}/{cursor}
GET /pubs/biorxiv/{doi}/na
```

Links preprints to their published journal versions. Accepts both preprint DOI and published DOI.

### 4. Publisher Filter

```
GET /publisher/{prefix}/{interval}/{cursor}
```

Find bioRxiv papers published by a specific publisher (by DOI prefix).

**Example:**
```
https://api.biorxiv.org/publisher/10.15252/2024-01-01/2024-06-01/0
```

## Response Format

```json
{
  "messages": [{
    "status": "ok",
    "count": 30,
    "total": "1029",
    "cursor": 0
  }],
  "collection": [{
    "title": "Paper title...",
    "authors": "Surname, A.; Surname, B.",
    "author_corresponding": "Full Name",
    "author_corresponding_institution": "Institution",
    "doi": "10.1101/2024.01.16.575895",
    "date": "2024-01-20",
    "version": "1",
    "type": "new results",
    "license": "cc_no",
    "category": "cancer biology",
    "jatsxml": "https://www.biorxiv.org/content/early/.../source.xml",
    "abstract": "Full abstract text...",
    "published": "10.1158/2159-8290.CD-24-0187",
    "server": "bioRxiv"
  }]
}
```

- `published` is `"NA"` if not yet published in a journal, or the published DOI if it has been.
- `type` values: `new results`, `confirmatory results`, `contradictory results`

## Pagination

`cursor` is a record offset, not a page number. Page size is not uniform: on `api.biorxiv.org` the `/details/` endpoints return **30** records per request and `/pubs/` returns **100**. Advance `cursor` by the `count` reported in `messages`, never by an assumed page size -- stepping by 100 across `/details/` skips 70 records per page. `messages[0].total` gives the size of the full result set.

## Rate Limits

No documented rate limits. No authentication required. Be reasonable with request frequency.

## Categories

Underscores for spaces. Hyphenated names are **not** recognized -- the API accepts them, ignores the filter, and returns the unfiltered set. Confirm the `category` echoed back in `messages` matches what you asked for before reporting a filtered result.

`animal_behavior_and_cognition`, `biochemistry`, `bioengineering`, `bioinformatics`, `biophysics`, `cancer_biology`, `cell_biology`, `developmental_biology`, `ecology`, `evolutionary_biology`, `genetics`, `genomics`, `immunology`, `microbiology`, `molecular_biology`, `neuroscience`, `paleontology`, `pathology`, `pharmacology_and_toxicology`, `physiology`, `plant_biology`, `scientific_communication_and_education`, `synthetic_biology`, `systems_biology`, `zoology`

`clinical_trials` and `epidemiology` are medRxiv categories, not bioRxiv ones; both are ignored here.
