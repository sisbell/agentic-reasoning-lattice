# Review of ASN-0001

## REVISE

### Issue 1: T10a and TA1-strict absent from Properties Introduced table
**ASN-0001, Properties Introduced table**: T10a (allocator discipline: siblings by `inc(·, 0)` only) and TA1-strict (strict order preservation when `k ≥ divergence(a, b)`) are independently stated, formally defined, and load-bearing in proofs — T10a is critical to the global uniqueness theorem (Case 4 depends on the uniform-length property it guarantees) and the partition monotonicity theorem (non-nesting of sibling prefixes). TA1-strict is used to establish that editing operations preserve strict ordering. Neither appears in the Properties Introduced table or the Required-by table.
**Problem**: The Properties Introduced table serves as the canonical inventory of what the ASN defines. An incomplete inventory means downstream work (Dafny formalization, subsequent ASNs) may miss load-bearing properties.
**Required**: Add T10a and TA1-strict to the Properties Introduced table with appropriate status and Required-by entries.

### Issue 2: `divergence(a, b)` undefined for the prefix case
**ASN-0001, TA1/TA1-strict verification**: "Let `j = divergence(a, b)` — the first position where `a` and `b` differ (`aⱼ < bⱼ` since `a < b`)."
**Problem**: When `a < b` by T1 case (ii) — `a` is a proper prefix of `b` — there is no position `j ≤ #a` where `aⱼ < bⱼ`. The parenthetical assumes componentwise divergence (T1 case (i)) without handling the prefix case. The conclusion is correct — in the prefix case `k ≤ #a < j` forces Case 1, giving `a ⊕ w = b ⊕ w` — but the proof doesn't state this. The same gap affects TA1-strict's precondition `k ≥ divergence(a, b)`: if divergence is undefined (prefix case), the precondition is vacuously unsatisfiable, correctly preventing a strict-inequality claim, but this should be explicit.
**Required**: Either define `divergence(a, b) = min(#a, #b) + 1` for the prefix case (making Case 1 handle it explicitly), or add a preliminary paragraph handling the prefix case before the three-case split: "When `a` is a proper prefix of `b`, all shared components agree. Since `k ≤ #a` and both operands agree at position `k`, the addition produces identical results: `a ⊕ w = b ⊕ w`. The weak form holds as equality. The strict form is inapplicable — no finite divergence point exists."

## DEFER

### Topic 1: T4 does not require non-empty fields
T4's positive-component constraint is vacuously satisfied for empty fields. A tumbler like `[1, 0, 0, 3]` (empty user field) is valid under T4. This may cause ambiguity in T6 ("same user" is undefined when a user field is empty) and in the semantic interpretation of the hierarchy.
**Why defer**: No current proof depends on field non-emptiness. If a non-empty-field constraint is needed, it would be an additional conjunct in T4, not a correction to existing content.

### Topic 2: Span-level constraints on ℓ relative to s
T12's formal statement requires only `ℓ > 0`. The prose explains that the action point of `ℓ` must match the hierarchical level of `s` for element-level spans, but this constraint is not formalized. Nelson's design intentionally permits multi-level spans, so the permissive statement may be correct — but the relationship between `ℓ`'s action point and the intended semantic level of the span deserves formal treatment.
**Why defer**: This is span semantics, not tumbler algebra. The algebra correctly computes `s ⊕ ℓ` for any valid operands; what span levels are meaningful is a question for the span/POOM ASN.

### Topic 3: Boundary behavior of ordinal subtraction at zero
TA7a includes `{[0]}` in the subtraction range (`[x] ⊖ [n] = [0]` when `x = n`). The sentinel status of `[0]` (TA6) is established, but the operational meaning — what happens when a V-space ordinal reaches the subspace boundary — is not explored.
**Why defer**: This is an operational question about DELETE semantics, not about the algebra's properties. The algebra correctly produces `[0]`; what the system does with it belongs in the operation ASN.

VERDICT: CONVERGED
