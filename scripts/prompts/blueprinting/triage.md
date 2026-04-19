# Triage Inline Findings

You are reviewing an accumulated lint report of embedded content found
in claim files. Your job is to deduplicate, prioritize, and produce
an action plan.

## Inline Lint Report

{{inline_report}}

## Missing Dependencies Report

{{missing_report}}

## Claim Table

{{table}}

## Task

The inline report contains findings accumulated across multiple scans.
Many are duplicates (same result reported with different names or
labels). First deduplicate — recognize when multiple findings describe
the same underlying result.

Then classify each unique finding into one of three categories:

### Promote (derived → standalone claim)

A derived finding should be promoted when:
- Its label is referenced in the missing dependencies report (another
  claim depends on it but it has no file)
- It has its own complete proof in the source file — not just a
  claim or assertion, but a full derivation
- It establishes an independently citable result — something another
  claim might reference by label

### Extract (definition → standalone file)

A definition finding should be extracted when:
- The concept appears in formal contracts or preconditions of other
  claims (check the claim table for cross-references)
- It introduces named notation or a named construction used beyond
  its source file

### Leave (stays in place)

A finding should be left in place when:
- It is a sub-step or case analysis within the enclosing claim's
  own proof — not independently citable
- It re-verifies a result that already has its own claim file
  (check the claim table for existing labels)
- It is a precondition, postcondition, frame condition, or invariant
  characterization of an existing claim (e.g., a wp reformulation
  of S0 or S3). These belong to the claim they describe, not as
  standalone claims.
- It is commentary, design rationale, or a worked example

## Output Format

SOURCE_LABEL is the claim file that contains the embedded result —
the `## heading` in the inline report (e.g., S0, S8-depth, Σ.M(d)).
SUGGESTED_LABEL is the name for the new claim being promoted or
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
