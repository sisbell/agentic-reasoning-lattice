# Review of ASN-0067

## REVISE

### Issue 1: Resolution applies M11/M12 to a restriction without formal justification
**ASN-0067, Source Resolution**: "M11's proof proceeds by iteratively merging adjacent blocks in any decomposition; it requires only finiteness (to terminate) and functionality (for B3). M12's proof that maximal runs partition the domain uses only the function's values. Both extend to any finite partial function T ⇀ T satisfying S2, S8-fin, and S8-depth."
**Problem**: M11 and M12 (ASN-0058) are stated for "arrangement M(d)", not for arbitrary partial functions. The resolution applies them to f = M(d_s)|⟦σ⟧, a restriction. The ASN argues informally by inspecting the proofs' internal structure — "the proof requires only finiteness" — but does not state the extension as a formal claim. This is an argument about proof generalization, not a derivation. The entire COPY construction depends on this resolution being well-defined: if M11/M12 do not extend to restrictions, the maximally merged I-address sequence is undefined.
**Required**: State a corollary (e.g., "M11/M12 hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, and S8-depth") with an explicit verification that M(d_s)|⟦σ⟧ satisfies these conditions. Alternatively, note this as a gap in ASN-0058 that should be addressed there.

### Issue 2: C2 contiguity argument cites TS1 where TS3 is needed
**ASN-0067, C2 derivation**: "contiguous because shifting a contiguous range by a constant preserves contiguity, by TS1"
**Problem**: TS1 (ShiftOrderPreservation) establishes that if v₁ < v₂ then shift(v₁, w) < shift(v₂, w) — order is preserved. But contiguity requires more: that consecutive positions remain consecutive after the shift, i.e., that shift(shift(v, 1), w) = shift(v, 1 + w) = shift(shift(v, w), 1). This identity is TS3 (ShiftComposition). Without TS3, the argument shows the shifted positions maintain order but does not establish gap-freeness — you know v₁↑w < v₂↑w but not that no depth-m position lies strictly between them.
**Required**: Cite TS3 (and TS1) for the contiguity claim, or derive the gap-freeness step explicitly.

### Issue 3: B2 disjointness after split cites M5 instead of M6f
**ASN-0067, Well-Formedness of B'**: "B_pre and B_post retain pairwise disjointness from B (M5, ASN-0058 for the split)"
**Problem**: M5 (SplitPartition) establishes that β_L and β_R are disjoint from each other. The claim here is that B_pre and B_post are each *internally* pairwise disjoint — that β_L is disjoint from every other block in B_pre, and similarly for B_post. This follows from M6f (SplitFrame), which establishes that the full decomposition after splitting β remains a valid decomposition satisfying B2. Any subset of a pairwise-disjoint set is pairwise disjoint. M5 addresses only the two split halves, not their relationship to the rest of the decomposition.
**Required**: Cite M6f for decomposition-level disjointness preservation after the split.

## OUT_OF_SCOPE

### Topic 1: Concurrent COPY semantics
**Why out of scope**: The ASN correctly identifies (C13, Observation — Concurrency) that intermediate states may be visible to concurrent operations and that formalizing isolation requires a concurrency model not present in the foundation. This is a new topic requiring its own ASN, not an error in this one.

### Topic 2: Cross-owner authorization for transclusion
**Why out of scope**: The open question "What authorization invariants must hold when content is copied from a document not owned by the copier?" is a policy question about access control, not a gap in the arrangement mechanics specified here.

VERDICT: REVISE
