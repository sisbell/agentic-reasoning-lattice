# Review of ASN-0058

## REVISE

### Issue 1: M4 cites TA5 instead of TA0/OrdinalShift
**ASN-0058, M4 (SplitDefinition)**: "both starts are valid tumblers (by TA5, ASN-0034)"
**Problem**: TA5 is HierarchicalIncrement (`inc(t, k)`), which adds 1 at a structurally chosen position. The split starts `v + c` and `a + c` are computed via OrdinalShift (`shift(v, c) = v ⊕ δ(c, #v)`), which adds `c` to the last component via TumblerAdd. For `c > 1`, there is no direct connection to TA5. Well-definedness follows from TA0: the action point of `δ(c, #v)` is `#v`, satisfying the precondition `k ≤ #v`.
**Required**: Cite TA0 (TumblerAdd well-definedness) and the OrdinalShift definition, not TA5.

### Issue 2: M7 necessity argument attributes violation to M1 instead of B3
**ASN-0058, M7 (MergeCondition)**: "V-adjacency alone is insufficient: if the I-extents are not contiguous, the merged range would map consecutive V-positions to non-consecutive I-addresses, violating M1."
**Problem**: M1 (OrderPreservation) is a property of a mapping block's internal structure — for block `(v, a, n)`, the pairs `(v + j, a + j)` are monotone. A proposed merged block `(v₁, a₁, n₁ + n₂)` satisfies M1 by construction: `a₁ + j < a₁ + k` for `j < k`, regardless of what `M(d)` actually maps. The real violation is B3 (Consistency): the merged block claims `M(d)(v₁ + n₁) = a₁ + n₁`, but the arrangement gives `M(d)(v₁ + n₁) = a₂ ≠ a₁ + n₁`. The block has correct internal order but doesn't match the arrangement.
**Required**: Replace "violating M1" with "violating B3 (consistency with `M(d)`)": the proposed block would predict `a₁ + n₁` at position `v₁ + n₁`, but the arrangement maps that position to `a₂`.

## OUT_OF_SCOPE

None. The ASN stays within its stated scope and correctly defers operations, link endsets, version semantics, and related topics.

VERDICT: REVISE
