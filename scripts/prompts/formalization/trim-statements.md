# Trim Formal Statements

You are producing an interface specification — the formal contract of each
property for downstream consumers (modeling, dependent ASNs). Proofs stay
in the ASN source; this file is what the property *guarantees*, not how
it was proven.

## Sections

{{sections}}

## Task

For each section, produce exactly three parts:

### 1. Header

If the name repeats the label (e.g., `## TA-MTO — TA-MTO`), replace the
name with a descriptive PascalCase identifier derived from the content
(e.g., `## TA-MTO — ManyToOneEquivalence`). Keep both label and name.

### 2. Formal statement + summary

Start with the precise formal claim — quantified expressions, equations,
definitions, algorithm rules. Use backtick-fenced notation where present
in the source.

Follow immediately with a clear plain-English summary (1-3 sentences)
that explains what the property means to someone who hasn't read the ASN.
The summary should be self-contained — a reader should understand the
property's role and guarantees from the summary alone, without needing
to parse the formal notation.

Good summary: "In words: tumbler comparison requires only the two
addresses themselves — no external index, allocator state, or global
registry participates in the decision. The comparison examines at most
min(#a, #b) component pairs."

Bad summary: "See T1 for details." / "This follows from the definition."

For sub-properties listed as (a), (b), (c), keep them — they are part
of the statement, not the proof.

### 3. Formal contracts

Preserve exactly as written:
- `*Preconditions:*`
- `*Postconditions:*`
- `*Invariant:*`
- `*Axiom:*`
- `*Frame:*`
- `*Definition:*`

### What to remove

- **Proofs** — everything after "*Proof.*", "∎", proof steps, case analysis
- **Narrative** — why the property exists, design rationale, history
- **Commentary** — "Gregory's implementation confirms...", "Nelson intended..."
- **Examples** — worked examples, verification exercises
- **Questions** — open questions, resolved questions, discussion

## Output

Do not reorder, merge, or drop any section. Every input `## ` header must
appear in the output. Start directly with the first `## ` header. No preamble.
