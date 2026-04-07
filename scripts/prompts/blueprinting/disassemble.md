# Split ASN into Per-Property Files

You are splitting a monolithic ASN reasoning document into one file per
property. The property table is the definitive list — every row gets
its own file.

## Input

The ASN is at `{{asn_path}}`.
Write output files to `{{output_dir}}`.

## Property files

For each row in the property table (the `| Label | Name | Statement | Status |`
table), create a file named `{label}.md` where label has parentheses
removed: `T0(a)` → `T0a.md`, `TA1-strict` → `TA1-strict.md`.

Each property file contains the property's complete context:
- Includes the proof, formal contract, and any trailing commentary
- Ends just before the next property's bold header, or the next `##`/`###`
  header that is NOT contextual to this property

**Contextual `##`/`###` sections go IN the property file.** If a `##` or
`###` section introduces definitions, notation, or concepts that the
following property depends on, include it at the TOP of that property's
file — before the bold header. Examples:
- `## Hierarchical structure` defines the four-field structure → include
  in T4.md (T4 formalizes this structure)
- `### Addition for position advancement` defines `⊕` and action point →
  include in TA0.md (TA0 is the first property using these)
- `### Subtraction for width computation` defines `⊖` → include in TA2.md

The property file does NOT have to start with `**LABEL`. It starts with
whatever context that property needs.

**Pure topic dividers** with no definitional content go in `_sections.md`.
These are rare — most `##`/`###` sections introduce concepts.

**Bold sub-headers** within a property (e.g., `**Consequence 1:**`,
`**Necessity.**`, `**Verification of T4.**`, `**Case A:**`) are NOT
separate files — they stay in the parent property's file.

## Structural files

- `_preamble.md` — everything before the first property or `##` header
  (title, introduction)
- `_table.md` — the property table (the `| Label | ... |` block including
  header row and separator)
- `_sections.md` — only `##`/`###` section headers that are pure topic
  dividers with no definitional content. Most sections will be absorbed
  into property files as context. This file may be empty or very small.
- `_worked-example.md` — the worked example section (starts at `## Worked example`)
- `_open-questions.md` — the open questions section (starts at `## Open Questions`)
- `_formal-summary.md` — the formal summary / properties introduced section

## Rules

1. Every property table label MUST get its own file. If you can't find
   a matching header in the ASN, create an empty file and report it.

2. No property content may be lost. Every line of the ASN must appear
   in exactly one output file.

3. The worked example section uses property labels (e.g., `**T4 (Hierarchical
   parsing).**`) as subsection headers — these are examples, NOT property
   definitions. The entire worked example section goes in `_worked-example.md`.

4. If a property label appears more than once as a bold header in the ASN
   (outside the worked example), the FIRST occurrence is the property
   definition. Later occurrences should be flagged.

## After splitting

Report any issues found:

```
ISSUES:
- [label not found] LABEL — no bold header found in ASN
- [duplicate header] LABEL — appears at lines X and Y
- [unusually short] LABEL — only N lines (possible missing content)
- [unusually long] LABEL — N lines (possible absorbed neighbor content)
- [unmatched header] **HEADER** at line N — bold header not in property table
```

If no issues: `ISSUES: none`
