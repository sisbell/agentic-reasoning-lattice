# Triage Inline Findings

You are reviewing an accumulated lint report of embedded content found
in property files. Your job is to deduplicate, prioritize, and produce
an action plan.

## Inline Lint Report

{{inline_report}}

## Missing Dependencies Report

{{missing_report}}

## Property Table

{{table}}

## Task

The inline report contains findings accumulated across multiple scans.
Many are duplicates (same result reported with different names or
labels). First deduplicate — recognize when multiple findings describe
the same underlying result.

Then classify each unique finding into one of three categories:

### Promote (derived → standalone property)

A derived finding should be promoted when:
- Its label is referenced in the missing dependencies report (another
  property depends on it but it has no file)
- It has its own complete proof in the source file — not just a
  claim or assertion, but a full derivation
- It establishes an independently citable result — something another
  property might reference by label

### Extract (definition → standalone file)

A definition finding should be extracted when:
- The concept appears in formal contracts or preconditions of other
  properties (check the property table for cross-references)
- It introduces named notation or a named construction used beyond
  its source file

### Leave (stays in place)

A finding should be left in place when:
- It is a sub-step or case analysis within the enclosing property's
  own proof — not independently citable
- It re-verifies a result that already has its own property file
  (check the property table for existing labels)
- It is a precondition, postcondition, frame condition, or invariant
  characterization of an existing property (e.g., a wp reformulation
  of S0 or S3). These belong to the property they describe, not as
  standalone properties.
- It is commentary, design rationale, or a worked example

## Output Format

SOURCE_LABEL is the property file that contains the embedded result —
the `## heading` in the inline report (e.g., S0, S8-depth, Σ.M(d)).
SUGGESTED_LABEL is the name for the new property being promoted or
extracted.

```
## Promote

- SOURCE_LABEL → SUGGESTED_LABEL: one-line reason

## Extract

- SOURCE_LABEL → SUGGESTED_LABEL: one-line reason

## Leave

- SOURCE_LABEL → SUGGESTED_LABEL: one-line reason
```

List each unique finding exactly once — do not place the same finding
in multiple sections. If uncertain, prefer the higher-priority
category: Promote > Extract > Leave.

Do not include commentary findings — only derived and definition.
Output ONLY the three sections. No preamble, no explanation.
