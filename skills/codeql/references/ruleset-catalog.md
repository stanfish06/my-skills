# Ruleset Catalog

## Official CodeQL Suites

| Suite | False Positives | Use Case |
|-------|-----------------|----------|
| `security-extended` | Low | **Default** - Security audits |
| `security-and-quality` | Medium | Comprehensive review (stable security + code quality) |
| `security-experimental` | Higher | Research, vulnerability hunting (stable security + experimental security) |

> **Suite hierarchy:** `security-and-quality` and `security-experimental` are complementary. `security-and-quality` excludes `experimental/` query paths. `security-experimental` includes them but excludes code quality queries. For maximum coverage (run-all mode), import both.

**Usage:** `codeql/<lang>-queries:codeql-suites/<lang>-security-extended.qls`

**Languages:** `cpp`, `csharp`, `go`, `java`, `javascript`, `python`, `ruby`, `swift`

---

## Trail of Bits Packs

| Pack | Language | Focus |
|------|----------|-------|
| `trailofbits/cpp-queries` | C/C++ | Memory safety, integer overflows |
| `trailofbits/go-queries` | Go | Concurrency, error handling |
| `trailofbits/java-queries` | Java | Security, code quality |

**Install:**
```bash
codeql pack download trailofbits/cpp-queries
codeql pack download trailofbits/go-queries
codeql pack download trailofbits/java-queries
```

---

## CodeQL Community Packs

| Pack | Language |
|------|----------|
| `githubsecuritylab/codeql-javascript-queries` | JavaScript/TypeScript |
| `githubsecuritylab/codeql-python-queries` | Python |
| `githubsecuritylab/codeql-go-queries` | Go |
| `githubsecuritylab/codeql-java-queries` | Java |
| `githubsecuritylab/codeql-cpp-queries` | C/C++ |
| `githubsecuritylab/codeql-csharp-queries` | C# |
| `githubsecuritylab/codeql-ruby-queries` | Ruby |

**Install:**
```bash
codeql pack download githubsecuritylab/codeql-<lang>-queries
```

**Source:** [github.com/GitHubSecurityLab/CodeQL-Community-Packs](https://github.com/GitHubSecurityLab/CodeQL-Community-Packs)

---

## Verify Installation

```bash
# List all installed packs
codeql resolve qlpacks

# Check specific packs
codeql resolve qlpacks | grep -E "(trailofbits|githubsecuritylab)"
```
