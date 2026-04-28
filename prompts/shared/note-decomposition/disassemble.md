# Split ASN into Per-Claim Files

You are splitting a monolithic ASN reasoning document into one file per
claim. The claim table is the definitive list — every row gets
its own file.

## Input

The ASN is at `{{asn_path}}`.
Write output files to `{{output_dir}}`.

## Claim files

For each row in the claim table (the `| Label | Name | Statement | Status |`
table), create a file named `{label}.md` where label has parentheses
removed: `T0(a)` → `T0a.md`, `TA1-strict` → `TA1-strict.md`.

Each claim file contains the claim's complete context:
- Includes the proof, formal contract, and any trailing commentary
- Ends just before the next claim's bold header, or the next `##`/`###`
  header that is NOT contextual to this claim

**Contextual `##`/`###` sections go IN the claim file.** If a `##` or
`###` section introduces definitions, notation, or concepts that the
following claim depends on, include it at the TOP of that claim's
file — before the bold header. Examples:
- `## Hierarchical structure` defines the four-field structure → include
  in T4.md (T4 formalizes this structure)
- `### Addition for position advancement` defines `⊕` and action point →
  include in TA0.md (TA0 is the first claim using these)
- `### Subtraction for width computation` defines `⊖` → include in TA2.md

The claim file does NOT have to start with `**LABEL`. It starts with
whatever context that claim needs.

**Pure topic dividers** with no definitional content go in `_sections.md`.
These are rare — most `##`/`###` sections introduce concepts.

**Bold sub-headers** within a claim (e.g., `**Consequence 1:**`,
`**Necessity.**`, `**Verification of T4.**`, `**Case A:**`) are NOT
separate files — they stay in the parent claim's file.

## Structural files

- `_preamble.md` — everything before the first claim or `##` header
  (title, introduction)
- `_table.md` — the claim table (the `| Label | ... |` block including
  header row and separator)
- `_sections.md` — only `##`/`###` section headers that are pure topic
  dividers with no definitional content. Most sections will be absorbed
  into claim files as context. This file may be empty or very small.
- `_worked-example.md` — the worked example section (starts at `## Worked example`)
- `_open-questions.md` — the open questions section (starts at `## Open Questions`)
- `_formal-summary.md` — the formal summary / claims introduced section

## Rules

1. Every claim table label MUST get its own file. If you can't find
   a matching header in the ASN, create an empty file and report it.

2. No claim content may be lost. Every line of the ASN must appear
   in exactly one output file.

3. The worked example section uses claim labels (e.g., `**T4 (Hierarchical
   parsing).**`) as subsection headers — these are examples, NOT claim
   definitions. The entire worked example section goes in `_worked-example.md`.

4. If a claim label appears more than once as a bold header in the ASN
   (outside the worked example), the FIRST occurrence is the claim
   definition. Later occurrences should be flagged.

## After splitting

Report any issues found:

```
ISSUES:
- [label not found] LABEL — no bold header found in ASN
- [duplicate header] LABEL — appears at lines X and Y
- [unusually short] LABEL — only N lines (possible missing content)
- [unusually long] LABEL — N lines (possible absorbed neighbor content)
- [unmatched header] **HEADER** at line N — bold header not in claim table
```

If no issues: `ISSUES: none`
