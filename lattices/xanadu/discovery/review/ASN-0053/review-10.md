# Review of ASN-0053

## REVISE

### Issue 1: S8 emitted spans lack T12 well-formedness verification

**ASN-0053, S8 (NormalizationExistence), emit step**: "emit the current interval as a span (s, r ⊖ s) — level-uniformity and S6 ensure #s = #r, so by D1 the reach is faithful"

**Problem**: The proof invokes D1 for reach faithfulness but does not verify T12 for the emitted span. S1 and S3 both explicitly verify T12 for their constructed spans — e.g., S1: "We verify T12 for γ: since s' < r', the divergence k satisfies k ≤ #s' … and the width r' ⊖ s' has a positive component at position k." S8's emit step performs the identical construction but skips this step. T12 and D1 have formally distinct preconditions (T12 concerns the width's positivity and action-point bound; D1 concerns two positions' ordering and length match). Both follow from `s < r` and `#s = #r`, but the proof must establish `s < r` explicitly (the current interval is non-empty because it was initialized from a non-empty span and only extended) and then verify T12: the width `r ⊖ s` is positive with action point at the divergence position k ≤ #s. Without this, the well-formedness of emitted spans is assumed but not proved, and the loop invariant's identification of ⟦(s, r ⊖ s)⟧ with [s, r) is unjustified.

**Required**: Add a sentence to the emit step: "The emitted span (s, r ⊖ s) satisfies T12: since s < r (the current interval was initialized from a non-empty span and is only extended by the merge step) and #s = #r (mutual level-compatibility), the width r ⊖ s is positive (the divergence at k gives r_k − s_k > 0) with action point k ≤ #s (type (i) divergence, as #s = #r excludes the prefix case)." Follow the pattern already established in S1 and S3.

## OUT_OF_SCOPE

### Topic 1: LeftCancellation belongs in the tumbler algebra foundation

The ASN correctly identifies that LeftCancellation "is properly a tumbler arithmetic fact, belonging with ASN-0034" and states it locally because S5 depends on it. A future revision of ASN-0034 should absorb this lemma (and potentially a note that right cancellation does *not* hold, as the many-to-one example demonstrates).

**Why out of scope**: This is a foundation maintenance task, not an error in this ASN.

### Topic 2: General span difference without the containment precondition

S11 proves the at-most-2-span bound for ⟦α⟧ \ ⟦β⟧ when ⟦β⟧ ⊆ ⟦α⟧. The same bound holds without the containment precondition: compute γ = ⟦α⟧ ∩ ⟦β⟧ via S1 (at most one span), then apply S11 to ⟦α⟧ \ ⟦γ⟧ (at most two spans). The general result is a one-line corollary of S1 + S11.

**Why out of scope**: S11 as stated covers the case needed by downstream operations (removing a contained sub-range). The general corollary is a natural extension for a future ASN.

### Topic 3: Cross-level span operations

All operations in this ASN require level-uniform, mutually level-compatible operands. The open questions list correctly identifies cross-level intersection and split as unresolved. The hierarchical tumbler space makes cross-level arithmetic non-trivial (D0 fails when divergence exceeds the shorter tumbler's length).

**Why out of scope**: This is a deliberate design boundary, not a gap. The ASN restricts its scope to same-level operations and documents the restriction in S6.

### Topic 4: Exact versus covering representability

S7 proves ⟦Σ⟧ ⊇ P (covering), while Nelson's quoted motivation suggests exact designation. The gap arises because in the general tumbler space, the minimal span containing a single position t also contains all tumblers between t and t ⊕ [0,...,0,1] at deeper levels. Exactness holds within the ordinal-only formulation (TA7a) where no deeper-level tumblers exist. Characterizing when exact representation is achievable is a content-layer question tied to the population of the address space.

**Why out of scope**: S7 is correctly stated with ⊇ and the algebra doesn't need the stronger =. The exactness question interacts with allocation and population concerns outside this ASN's scope.

VERDICT: REVISE
