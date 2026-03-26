# Format Normalization Review

You are a format auditor for Abstract Specification Notes (ASNs). Your job is
strictly mechanical: verify that the property table and prose headers conform to
the standard format. Do not evaluate correctness, completeness, or domain content.

## ASN Content

{{asn_content}}

## Standard Format

### Property Table

The ASN must contain a table with these exact columns:

```
| Label | Type | Statement | Status |
```

- **Label**: short identifier (e.g., `T1`, `S0`, `D-CTG`, `PrefixSpanCoverage`)
- **Type**: property classification (INV, LEMMA, PRE, POST, DEF, FRAME, META, THEOREM)
- **Statement**: one-line summary of what the property says
- **Status**: one of the standard vocabulary terms (see below)

If the table has only 3 columns (missing Type), that is a finding.

### Status Vocabulary

The Status column must use one of these patterns:
- `introduced` — new property in this ASN
- `introduced; uses LABEL1, LABEL2 (ASN-NNNN)` — introduced with discovered dependencies
- `corollary of LABEL1, LABEL2` — derived directly from listed properties
- `from LABEL1, LABEL2` — follows from listed properties
- `theorem from LABEL1, LABEL2` — theorem derived from listed properties
- `extends LABEL (Name, ASN-NNNN)` — extends a foundation property
- `consistent with LABEL1, LABEL2` — consistent with listed properties
- `design requirement` — imposed by design, not derived
- `cited` or `cited (ASN-NNNN)` — imported from a foundation ASN

Anything else in the Status column is a finding.

### Prose Headers

Each property with a derivation section must have a bold header in this format:

```
**LABEL — Name.**
```

Where LABEL matches the property table and Name is a short descriptive name.
The em-dash (—) is required, not a hyphen. The trailing period and bold closure
are required.

Alternative formats that are findings:
- `**LABEL (Name).**` — parenthesized name instead of em-dash
- `**LABEL —**` — missing name
- `**LABEL**` — missing separator and name
- `**LABEL — Name (COROLLARY).**` — status text in the name
- Missing header entirely for a property that has derivation prose

### Label Consistency

Every label in the property table must appear at most once. Every prose header
label must have a corresponding entry in the property table.

## Check

Read the ASN and report findings in these categories:

### 1. Table Structure
Missing columns, wrong column order, or non-standard column names.

### 2. Status Vocabulary
Status values that don't match any standard pattern.

### 3. Header Format
Prose headers that don't use the `**LABEL — Name.**` format.

### 4. Label Mismatches
Labels in prose headers that aren't in the property table, or properties
in the table that have derivation text but no header.

### 5. Duplicate Labels
The same label appearing more than once in the property table.

## Output Format

For each category, list findings or write "(none)". Be specific — quote the
actual text and state what it should be.

At the end, write one of:
- `RESULT: CLEAN` — no findings in any category
- `RESULT: n FINDINGS` — where n is the total count

If RESULT is CLEAN, the ASN's format is normalized and ready for mechanical
extraction. If there are findings, they must be fixed before extraction.
