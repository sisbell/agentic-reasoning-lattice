# Trim Formal Statements

You are trimming property sections to their formal content and ensuring
each section is a well-formed formal statement.

## Sections

{{sections}}

## Task

For each section:

### 1. Fix the header

If the name repeats the label (e.g., `## TA-MTO — TA-MTO`), replace the
name with a descriptive PascalCase name derived from the property's content
(e.g., `## TA-MTO — ManyToOneEquivalence`). Keep both the label and the name.

### 2. Ensure a formal statement comes first

Each section must begin with a clear statement of what the property claims
or defines. If the statement is only embedded in the original bold header
line (which was stripped), reconstruct it as the first line of the body.
For example:

```
## TA-MTO — ManyToOneEquivalence

a agrees with b on components 1..k ⟺ a ⊕ w = b ⊕ w for displacement w with action point k.

*Proof (forward).* ...
```

The statement should be the formal claim — quantified expressions, equations,
definitions. Follow it with a one-line plain English summary of what the
property means (e.g., "In words: for every tumbler and every component
position, there exists a tumbler whose value at that position exceeds any
given bound."). This helps downstream consumers understand the formal
notation without re-deriving it.

### 3. Trim to formal content

Keep:
- The formal statement
- Every proof step and case analysis
- Every sub-property listed as (a), (b), (c), etc.
- Definition algorithms and computation rules
- Preconditions and postconditions

Remove:
- Narrative prose explaining why a property exists or what it means
- Historical context and design rationale
- Implementation commentary ("Gregory's implementation confirms...")
- Worked examples and verification exercises
- Open questions and discussion
- Resolved questions

If in doubt, keep it. Completeness is more important than brevity.

## Output

Do not reorder, merge, or drop any section. Every input `## ` header must
appear in the output. Start directly with the first `## ` header. No preamble.
