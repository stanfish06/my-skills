---
name: sequence-analysis
description: Analyze DNA/RNA/protein sequences. Use when the user provides a sequence and asks for analysis, translation, GC content, ORFs, motifs, restriction sites, or primer design. Triggers on "sequence", "translate", "GC content", "ORF", "primer", "restriction", "complement", "reverse complement".
---

# Sequence Analysis

Comprehensive sequence analysis using BioPython and command-line tools.

## When to Use

- User provides a DNA/RNA/protein sequence for analysis
- User asks about sequence properties (GC%, length, composition)
- User wants to translate DNA to protein
- User asks for ORF finding, primer design, restriction site analysis

## Analysis Workflows

### 1. Basic Sequence Properties

```python
from Bio.Seq import Seq
from Bio.SeqUtils import gc_fraction, molecular_weight

seq = Seq("ATGCGATCGATCGATCG...")

print(f"Length: {len(seq)} bp")
print(f"GC Content: {gc_fraction(seq)*100:.1f}%")
print(f"Complement: {seq.complement()}")
print(f"Reverse Complement: {seq.reverse_complement()}")
print(f"Protein: {seq.translate()}")
```

### 2. ORF Finding

```python
from Bio.Seq import Seq

def find_orfs(sequence, min_length=100):
    orfs = []
    seq = Seq(str(sequence))
    
    for strand, nuc in [("+", seq), ("-", seq.reverse_complement())]:
        for frame in range(3):
            trans = nuc[frame:].translate()
            aa_seq = str(trans)
            
            start = 0
            while start < len(aa_seq):
                m_pos = aa_seq.find("M", start)
                if m_pos == -1:
                    break
                stop_pos = aa_seq.find("*", m_pos)
                if stop_pos == -1:
                    stop_pos = len(aa_seq)
                
                orf_len = (stop_pos - m_pos) * 3
                if orf_len >= min_length:
                    nt_start = frame + m_pos * 3
                    orfs.append({
                        "strand": strand,
                        "frame": frame + 1,
                        "start": nt_start,
                        "length_aa": stop_pos - m_pos,
                        "length_nt": orf_len,
                        "protein": aa_seq[m_pos:stop_pos]
                    })
                start = stop_pos + 1
    
    return sorted(orfs, key=lambda x: x["length_nt"], reverse=True)
```

### 3. Restriction Site Analysis

```python
from Bio.Restriction import RestrictionBatch, Analysis
from Bio.Seq import Seq

seq = Seq("ATGCGATCGATCG...")
rb = RestrictionBatch(["EcoRI", "BamHI", "HindIII", "NotI", "XhoI"])
ana = Analysis(rb, seq)
results = ana.full()

for enzyme, sites in results.items():
    if sites:
        print(f"{enzyme}: cuts at positions {sites}")
```

### 4. Primer Design (basic)

```python
from Bio.Seq import Seq
from Bio.SeqUtils import MeltingTemp as mt
from Bio.SeqUtils import gc_fraction

def design_primers(seq_str, product_size_range=(200, 800)):
    seq = Seq(seq_str)
    
    # Forward primer (first 20bp)
    fwd = seq[:20]
    fwd_tm = mt.Tm_NN(fwd)
    
    # Reverse primer (last 20bp, reverse complement)
    rev = seq[-20:].reverse_complement()
    rev_tm = mt.Tm_NN(rev)
    
    print(f"Forward: 5'-{fwd}-3' (Tm={fwd_tm:.1f}°C, GC={gc_fraction(fwd)*100:.0f}%)")
    print(f"Reverse: 5'-{rev}-3' (Tm={rev_tm:.1f}°C, GC={gc_fraction(rev)*100:.0f}%)")
    print(f"Product size: {len(seq)} bp")
```

### 5. Multiple Sequence Alignment (using command-line)

If user provides multiple sequences:

```bash
# Write sequences to FASTA file
cat > /tmp/sequences.fa << 'EOF'
>seq1
ATGCGATCG...
>seq2
ATGCAATCG...
EOF

# If clustalw/muscle available, use them
# Otherwise use BioPython's pairwise alignment
```

```python
from Bio.Align import PairwiseAligner

aligner = PairwiseAligner()
aligner.mode = "global"
# Pin scoring explicitly — PairwiseAligner's default gap scores changed in
# Biopython 1.86 (0 -> -1.0), so relying on defaults is version-dependent.
aligner.match_score = 1.0
aligner.mismatch_score = 0.0
aligner.open_gap_score = -2.0
aligner.extend_gap_score = -0.5

alignments = aligner.align(seq1, seq2)
best = alignments[0]
print(f"Score: {best.score}")
print(best)
```

Note: `Bio.pairwise2` was deprecated in Biopython 1.80 and still ships as of 1.87
(emitting a `BiopythonDeprecationWarning`), but new code should use
`Bio.Align.PairwiseAligner`. Two differences from the old
`pairwise2.align.globalxx`: (1) `globalxx` applied no gap penalty, while
`PairwiseAligner` defaults all gap scores to -1.0 as of Biopython 1.86 (0.0
before) — always set the scoring attributes explicitly rather than relying on
defaults; (2) `aligner.align()` yields `Alignment` objects, so use
`print(alignment)` for the layout and `alignment.score` for the score, which the
old `format_alignment` printed together. For exact `globalxx` parity set
`aligner.open_gap_score = 0.0` and `aligner.extend_gap_score = 0.0`.

### 6. Output format

Report in the caller's own format — plain text for a CLI, Markdown where it renders.
Do not emit chat-app markup. Cover, in order: sequence length, GC content, ORFs found
(with the longest), the protein translation for the requested frame, and restriction
sites per enzyme (naming the enzymes searched, including those with no sites).

### 7. Follow-up suggestions

- "Want me to BLAST this sequence?"
- "Should I design primers for a specific region?"
- "Want a detailed ORF map?"
- "Should I check for conserved domains?"
