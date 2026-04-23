# Dependency Rebase Fix

You are fixing dependency reference issues in an ASN reasoning document.

## ASN File

The ASN is at `{{asn_file}}`. Read it, apply the fixes, write it back.

## Report

{{report}}

## Style

Write in Dijkstra's style: prose with embedded formalism. Each formal
statement must be justified in the sentence that introduces it. Each case
must be explicit — no "by similar reasoning." End proofs with ∎.

## Format Reference

### Prose headers

Headers must be exactly `**LABEL (PascalCaseName).**` — nothing else:

```
**X3 (MonotonicGrowth).**
**D-CTG (ContiguousRange).**
```

Do not add annotations, brackets, or citations to the header. Context
belongs in the body text after the header.

### Claim table

Table rows use `| Label | Name | Statement | Status |` columns.

**Status vocabulary** — use only these patterns:

| Status | When to use |
|--------|-------------|
| `introduced` | claim is original to this ASN — no foundation equivalent exists |
| `from X1, X2, X3` | claim is proven here using the listed claims as premises |
| `cited (ASN-NNNN)` | claim states the same result as one already proven in a foundation ASN — this ASN does not add to or strengthen the claim |
| `confirms LABEL (ASN-NNNN)` | same result as a foundation claim but proven independently in this ASN — maps to `cited` at export |
| `extends X1 (SomeName, ASN-NNNN)` | claim takes a foundation result and strengthens, generalizes, or adds new conditions to it |
| `corollary of X1, X2` | claim follows immediately from the listed claims with no substantial new argument |
| `theorem from X1, X2` | major result with a non-trivial proof from the listed claims |
| `consistent with X1, X2` | claim is compatible with but not derived from the listed claims |
| `axiom` | fundamental assertion posited without proof |
| `design requirement` | imposed by design, not derived |
| `lemma (from X1, X2)` | intermediate result used to support a later proof |

When reclassifying a claim as `cited`, the `from` dependency list is
no longer needed — the claim references the foundation, not local
derivations.

### Formal Contract

The `*Formal Contract:*` marker is a fixed string. Do not modify it.

## Rules

1. Read the report above. Fix only actual findings — categories marked
   "(none)" or described as clean require no action.

2. If a fix affects the claim table, you may **only** update the
   row for the claim named in that finding. Within that row you may
   add or fix dependency labels and change the status classification
   when the finding requires it. Do **not** touch any other claim's row.

3. If a fix affects the `*Formal Contract:*` section, update it to
   match the revised claim. Preserve the exact conditions from the
   narrative — do not simplify, expand, or add implicit type constraints.

4. If a fix requires changing inline citations (e.g., renaming
   "X5 (SomeOldName)" to "X5 (SomeNewName)"), apply the
   change everywhere it appears in that claim's section.

5. Do not change anything beyond what the findings require. Do not
   modify unrelated claims or narrative prose.
