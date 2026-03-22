# Review of ASN-0065

## REVISE

### Issue 1: OrdinalDisplacement naming collision with ASN-0034
**ASN-0065, Displacement Analysis**: "**Definition — OrdinalDisplacement.** For a position v in the affected range, define Δ(v) = ord(π(v)) − ord(v) (an integer, possibly negative)."
**Problem**: ASN-0034 already defines **OrdinalDisplacement** as `δ(n, m) = [0, 0, ..., 0, n]` — a tumbler, not a signed integer function. The ASN introduces a different concept under the same name. A reader familiar with ASN-0034 will encounter "Definition — OrdinalDisplacement" and expect the foundation's definition; instead they find a signed integer-valued function measuring how far a position moves under a permutation. The two are conceptually adjacent (both concern ordinal changes) but technically distinct — one is a tumbler displacement operand, the other is a derived measurement on a specific bijection.
**Required**: Rename to avoid collision — e.g., "PermutationDisplacement" or "SignedOrdinalShift." The formal content (postconditions, permutations, proofs) is unaffected; only the label on this analytical definition needs to change.

## OUT_OF_SCOPE

None. The Open Questions section already captures the natural extensions (k-cut generalization, composition closure, block-count bounds, deeper ordinals, front-end rendering of split endsets).

VERDICT: REVISE
