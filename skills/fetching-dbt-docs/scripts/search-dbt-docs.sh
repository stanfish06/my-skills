#!/usr/bin/env bash
#
# search-dbt-docs.sh - Search dbt full docs for keywords and return matching page URLs
#
# Usage: ./search-dbt-docs.sh <keyword> [keyword2] [keyword3] ...
#
# Works on macOS, Linux, Git Bash (Windows), and WSL

set -euo pipefail

FULL_URL="https://docs.getdbt.com/llms-full.txt"
INDEX_URL="https://docs.getdbt.com/llms.txt"
CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/dbt-docs"
CACHE_FILE="$CACHE_DIR/llms-full.txt"
INDEX_FILE="$CACHE_DIR/llms.txt"
CACHE_MAX_AGE=86400  # 24 hours in seconds

# Colors (disabled if not a terminal)
if [[ -t 1 ]]; then
    BOLD='\033[1m'
    DIM='\033[2m'
    RESET='\033[0m'
else
    BOLD=''
    DIM=''
    RESET=''
fi

usage() {
    echo "Usage: $0 <keyword> [keyword2] [keyword3] ..."
    echo ""
    echo "Search dbt documentation for keywords and return matching page URLs."
    echo ""
    echo "Options:"
    echo "  -f, --fresh     Force fresh download (ignore cache)"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 semantic_model"
    echo "  $0 metric dimension"
    echo "  $0 'incremental strategy'"
    exit 1
}

# Parse arguments
FRESH=false
KEYWORDS=()

while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--fresh)
            FRESH=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            echo "Unknown option: $1"
            usage
            ;;
        *)
            KEYWORDS+=("$1")
            shift
            ;;
    esac
done

if [[ ${#KEYWORDS[@]} -eq 0 ]]; then
    echo "Error: At least one keyword required"
    usage
fi

# Ensure cache directory exists
mkdir -p "$CACHE_DIR"

# Check if a cache file needs download
need_download() {
    local f="$1"
    if [[ "$FRESH" == "true" ]]; then
        return 0
    fi
    if [[ ! -s "$f" ]]; then
        return 0
    fi
    # mtime, cross-platform: GNU stat first, BSD stat second. Probing the binary
    # beats branching on uname -- GNU coreutils ahead of /usr/bin on macOS makes
    # `stat -f` mean "filesystem status" and print to stdout.
    local mtime
    mtime=$(stat -c %Y "$f" 2>/dev/null || stat -f %m "$f" 2>/dev/null || echo 0)
    [[ $(( $(date +%s) - mtime )) -gt $CACHE_MAX_AGE ]]
}

# Download to a temp file and move into place only on success, so an HTTP error
# never poisons the cache for the rest of the TTL
download() {
    local url="$1" dest="$2" tmp
    tmp="$dest.tmp.$$"
    if ! curl -fsSL "$url" -o "$tmp"; then
        rm -f "$tmp"
        echo "Error: failed to download $url" >&2
        exit 1
    fi
    mv -f "$tmp" "$dest"
}

if need_download "$CACHE_FILE"; then
    echo -e "${DIM}Downloading dbt docs...${RESET}" >&2
    download "$FULL_URL" "$CACHE_FILE"
    echo -e "${DIM}Cached at: $CACHE_FILE${RESET}" >&2
fi

if need_download "$INDEX_FILE"; then
    echo -e "${DIM}Downloading dbt docs index...${RESET}" >&2
    download "$INDEX_URL" "$INDEX_FILE"
    echo -e "${DIM}Cached at: $INDEX_FILE${RESET}" >&2
fi

# Convert keywords to lowercase for matching
keywords_lower=""
for kw in "${KEYWORDS[@]}"; do
    keywords_lower="$keywords_lower|$(echo "$kw" | tr '[:upper:]' '[:lower:]')"
done
keywords_lower="${keywords_lower:1}"  # Remove leading |

echo -e "${BOLD}Searching for: ${KEYWORDS[*]}${RESET}" >&2
echo "" >&2

# Search: find pages containing keywords
# Logic:
# 1. llms.txt is the page index: "- [Title](URL): description"
# 2. In llms-full.txt a page block starts at "### <Title>"; the block carries no
#    self-URL, so resolve the URL by joining the header title against that index
# 3. Match keywords in content, output unique page URLs
results=$(awk -v keywords="$keywords_lower" '
# collapse inline markdown links to their label so a lifecycle badge such as
# "About dbt State [Preview](...)" matches the plain index title
function norm(t) {
    gsub(/\]\([^)]*\)/, "", t)
    gsub(/\[/, "", t)
    gsub(/[ \t]+/, " ", t)
    sub(/^ /, "", t)
    sub(/ $/, "", t)
    return t
}

BEGIN {
    current_url = ""
    page_count = 0
    n = split(keywords, kw_arr, "|")
}

# First file: the llms.txt index -> title => URL
NR == FNR {
    if (match($0, /^- \[.*\]\(https:\/\/docs\.getdbt\.com\/[^)]+\)/)) {
        close_bracket = index($0, "](")
        title = substr($0, 4, close_bracket - 4)
        rest = substr($0, close_bracket + 2)
        url = substr(rest, 1, index(rest, ")") - 1)
        key = norm(title)
        if (!(key in index_url)) index_url[key] = url
    }
    next
}

# Second file: page block header. Unresolvable titles clear the URL rather than
# letting their content be credited to the previous page.
/^### / {
    key = norm(substr($0, 5))
    current_url = (key in index_url) ? index_url[key] : ""
    next
}

# Check content for keyword matches
{
    if (current_url == "") next

    line_lower = tolower($0)
    for (i = 1; i <= n; i++) {
        if (index(line_lower, kw_arr[i]) > 0) {
            if (!seen[current_url]) {
                seen[current_url] = 1
                urls[++page_count] = current_url
            }
            break
        }
    }
}

END {
    for (i = 1; i <= page_count; i++) {
        print urls[i]
    }
}
' "$INDEX_FILE" "$CACHE_FILE")

if [[ -z "$results" ]]; then
    echo "No matches found."
    exit 0
fi

echo "$results"

# Count results
count=$(echo "$results" | wc -l | tr -d ' ')
echo "" >&2
echo -e "${DIM}Found $count matching page(s)${RESET}" >&2
