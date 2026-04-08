# Format Normalization Review

You are a format auditor for Abstract Specification Notes (ASNs). Your job is
strictly mechanical: verify that the property table and prose headers conform to
the standard format. Do not evaluate correctness, completeness, or domain content.

## ASN Content

{{asn_content}}

## Standard Format

### Property Table

The ASN must contain a table with these columns:

```
| Label | Statement | Status |
```

- **Label**: short identifier (e.g., `T1`, `S0`, `D-CTG`, `PrefixSpanCoverage`, `Endset`)
- **Statement**: one-line summary of what the property says
- **Status**: one of the standard vocabulary terms (see below)

A 4-column table with an additional Name column is also valid — do not flag it.

Definitions must be in the table. The label is the PascalCase definition
name (e.g., `Endset`, `Link`, `Divergence`, `TumblerAddition`).

### Status Vocabulary

The Status column must use one of these patterns:
- `introduced` — new property in this ASN
- `introduced; uses LABEL1, LABEL2 (ASN-NNNN)` — introduced with discovered dependencies
- `corollary of LABEL1, LABEL2` — derived directly from listed properties
- `from LABEL1, LABEL2` — follows from listed properties
- `theorem from LABEL1, LABEL2` — theorem derived from listed properties
- `extends LABEL (Name, ASN-NNNN)` — extends a foundation property
- `consistent with LABEL1, LABEL2` — consistent with listed properties
- `axiom` — fundamental assertion, posited by definition, not derived
- `design requirement` — imposed by design, not derived
- `cited` or `cited (ASN-NNNN)` — imported from a foundation ASN
- `confirms LABEL (ASN-NNNN)` — same result as a foundation property, proven independently in this ASN
- `lemma (from LABEL1, LABEL2)` — lemma derived from listed properties

Anything else in the Status column is a finding.

### Prose Headers

Two header conventions are used:

**Properties** have a bold header with the label first:
```
**LABEL (PascalCaseName).**
```
Where LABEL matches the property table and PascalCaseName is a PascalCase
identifier with no spaces (e.g., `LexicographicOrder`, `SubspaceDisjointness`,
`CarrierSetDefinition`).

A header like `**T1 (Lexicographic order).**` is a finding — it must be
`**T1 (LexicographicOrder).**`.

**Definitions** have a bold header with "Definition" first:
```
**Definition (PascalCaseName).**
```
Where PascalCaseName is the PascalCase label that must appear in the property table.

Both formats are valid. The trailing period and bold closure are required.

### Label Consistency (bidirectional)

1. Every label in the property table must have its own `**LABEL (Name).**`
   bold header line. A mention within another property's section (e.g.,
   "Verification of TA4" or "Claim (TA3)") does not count — the label
   needs its own top-level bold header.
2. Every bold property header (`**LABEL (...).**`) in the prose must have a
   corresponding entry in the property table.
3. Every definition header (`**Definition (Name).**`) in the prose must have
   a corresponding entry in the property table, with the PascalCase Name as
   the label.

If a definition exists in prose but not in the table, flag it:
"Definition (Name) in prose but no table entry — add row with label Name"

If a property header exists in prose but not in the table, flag it:
"LABEL has prose section but no table entry"

### Duplicate Labels

The same label must not appear more than once in the property table.

## Check

Read the ASN and report findings in these categories:

### 1. Table Structure
Missing columns, wrong column order, or non-standard column names.

### 2. Status Vocabulary
Status values that don't match any standard pattern.

### 3. Header Format
Prose headers that are malformed (missing bold closure, missing period,
name not PascalCase, spaces in name, etc.).

### 4. Missing Table Entries
Properties or definitions that have prose sections but no table entry.

### 5. Missing Prose Sections
Table entries that have no corresponding prose section.

### 6. Duplicate Labels
The same label appearing more than once in the property table.

### 7. Missing Boundary Markers
Each property or definition bold header (except the very first in the ASN)
AND each `##` or `###` section header must be preceded by a horizontal
rule (`---`) on its own line. This marks boundaries for downstream
disassembly. Do not require `---` before the very first property, or
between lines inside the worked example section (the `## Worked example`
header itself should have `---` before it, but the property-label
sub-headers within the worked example should not).

## Output Format

For each category, list findings or write "(none)". Be specific — quote the
actual text and state what it should be.

At the end, write one of:
- `RESULT: CLEAN` — no findings in any category
- `RESULT: n FINDINGS` — where n is the total count

If RESULT is CLEAN, the ASN's format is normalized and ready for mechanical
extraction. If there are findings, they must be fixed before extraction.
