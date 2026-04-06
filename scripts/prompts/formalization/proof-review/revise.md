# Proof Revision

You are fixing a specific proof in an ASN reasoning document.

## ASN File

The ASN is at `{{asn_path}}`. Read it, fix the issue, write it back.

## Property

**Label**: {{label}}

## Issue

{{finding}}

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

### Property table

Table rows use `| Label | Name | Statement | Status |` columns.

**Status vocabulary** — use only these patterns:

| Status | When to use |
|--------|-------------|
| `introduced` | property is original to this ASN — no foundation equivalent exists |
| `from X1, X2, X3` | property is proven here using the listed properties as premises |
| `cited (ASN-NNNN)` | property states the same result as one already proven in a foundation ASN — this ASN does not add to or strengthen the claim |
| `confirms LABEL (ASN-NNNN)` | same result as a foundation property but proven independently in this ASN — maps to `cited` at export |
| `extends X1 (SomeName, ASN-NNNN)` | property takes a foundation result and strengthens, generalizes, or adds new conditions to it |
| `corollary of X1, X2` | property follows immediately from the listed properties with no substantial new argument |
| `theorem from X1, X2` | major result with a non-trivial proof from the listed properties |
| `consistent with X1, X2` | property is compatible with but not derived from the listed properties |
| `axiom` | fundamental assertion posited without proof |
| `design requirement` | imposed by design, not derived |
| `lemma (from X1, X2)` | intermediate result used to support a later proof |

### Formal Contract

The `*Formal Contract:*` marker is a fixed string. Do not modify it.

## Rules

1. Fix the proof to address the issue above.

2. Ensure the property section ends with a `*Formal Contract:*` section.
   If it is not already present, add it after the proof. If it exists
   but needs updating after the fix, update it. Only include applicable
   fields. Example:

   ```
   *Formal Contract:*
   - *Preconditions:* w > 0, actionPoint(w) ≤ #a
   - *Postconditions:* a ⊕ w ∈ T, #(a ⊕ w) = #w
   ```

   Fields:
   - *Preconditions:* — what must hold before
   - *Postconditions:* — what is guaranteed after
   - *Invariant:* — what holds across all state transitions (for every s → s')
   - *Frame:* — what is preserved / not changed
   - *Axiom:* — fundamental assertion by definition or design, not derived
   - *Definition:* — the construction or computation rule (for definitions only)

   When writing the formal contract, preserve the exact conditions from the
   property's narrative — do not simplify, expand, or add implicit type
   constraints.

3. If a fix requires adding dependencies, update only the table row for
   **{{label}}**. Do not touch other rows.

4. If the proof needs a property that doesn't exist anywhere in the ASN
   or its foundations, add the new property:
   - Add a row to the property table
   - Write its derivation section with header and proof
   - Add a formal contract section to the new property

5. Do not change anything beyond the specific property being fixed and
   any new properties needed. Do not modify narrative prose.
