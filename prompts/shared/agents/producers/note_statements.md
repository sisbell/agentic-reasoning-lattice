# Statement Export

You are extracting claim statements from an ASN reasoning document.
The statement registry below lists every claim by label. Your job is
to find each one in the ASN and extract just the formal mathematical
statement.

## ASN Content

{{asn_content}}

## Task

For each claim listed in the ASN's **statement registry** (the table
near the end of the document), locate it in the ASN and extract:
1. The formal mathematical statement (quantified expressions, definitions,
   constraints) — exactly as written
2. Enough context to make the statement self-contained (e.g., variable
   meanings, sub-claims)

Also extract any **Definition** sections from the ASN that define operations
or concepts used by the claims (e.g., tumbler addition, action point,
subtraction). These will become function/predicate bodies in Dafny.

## Output format

Start directly with `# ASN-NNNN Claim Statements`.

For each claim, use this structure:

```
## LABEL — DafnyName (TYPE, CONSTRUCT)

[claim statement, exactly as written in the ASN]
```

For definitions, use:

```
## Definition — DafnyName

[definition, exactly as written]
```

Assign each definition a PascalCase Dafny name based on what it defines
(e.g., `ActionPoint`, `TumblerAdd`, `TumblerSubtract`).

Use the type annotations from the statement registry or the in-body labels
to determine TYPE and CONSTRUCT (e.g., LEMMA/lemma, INV/predicate, PRE/requires).

## What to include

- Formal statements with their mathematical notation preserved exactly
- Sub-claims listed as (a), (b), (c) etc. when a claim has them
- Preconditions stated within a claim's definition
- Definition algorithms (step-by-step computation rules)

## What to exclude

- Narrative prose explaining why a claim exists or what it means
- Worked examples and verification exercises
- Open questions or discussion sections
- Design rationale and historical context
- Cross-references to other ASNs (unless needed for a claim statement)
- The "Resolved questions" section

Keep it minimal. The Dafny translator needs math, not explanation.

## Critical constraint

Do not rename, reclassify, or modify the claims. Use the label, type,
and statement text exactly as they appear in the ASN's statement registry.
If a claim is labeled T7 in the registry, it must be T7 in your output.
If the registry says INV, your output says INV — not LEMMA, not THEOREM.
Extract verbatim; do not improve, correct, or editorialize.
