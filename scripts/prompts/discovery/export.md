# Statement Export

You are extracting formal statements from an ASN reasoning document.
The statement registry below lists every property by label. Your job is
to find each one in the ASN and extract just the formal statement.

## ASN Content

{{asn_content}}

## Task

For each property listed in the ASN's **statement registry** (the table
near the end of the document), locate it in the ASN and extract:
1. The formal mathematical statement (quantified expressions, definitions,
   constraints) — exactly as written
2. Enough context to make the statement self-contained (e.g., variable
   meanings, sub-properties)

Also extract any **Definition** sections from the ASN that define operations
or concepts used by the properties (e.g., tumbler addition, action point,
subtraction). These will become function/predicate bodies in Dafny.

## Output format

Start directly with `# ASN-NNNN Formal Statements`.

For each property, use this structure:

```
## LABEL — DafnyName (TYPE, CONSTRUCT)

[formal statement, exactly as written in the ASN]
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
- Sub-properties listed as (a), (b), (c) etc. when a property has them
- Preconditions stated within a property's definition
- Definition algorithms (step-by-step computation rules)

## What to exclude

- Narrative prose explaining why a property exists or what it means
- Worked examples and verification exercises
- Open questions or discussion sections
- Design rationale and historical context
- Cross-references to other ASNs (unless needed for a formal statement)
- The "Resolved questions" section

Keep it minimal. The Dafny translator needs math, not explanation.
