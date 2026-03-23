# Review of ASN-0061

## REVISE

### Issue 1: S1 and S8 omitted from invariant verification
**ASN-0061, Invariant Preservation**: "We verify that DELETE preserves each invariant in ExtendedReachableStateInvariants (ASN-0047)."
**Problem**: ExtendedReachableStateInvariants includes S1 (StoreMonotonicity) and S8 (FiniteSpanDecomposition). Neither is mentioned. S1 is a corollary of S0 and follows trivially from C' = C. S8 is a lemma from S8-fin, S8a, S2, and S8-depth — all four verified. Both invariants are preserved, but the section claims completeness against the full list and then silently skips two entries.
**Required**: Add entries for S1 and S8, even if one-liners: "S1: corollary of S0, inherited from C' = C" and "S8: lemma from S8-fin, S8a, S2, S8-depth, all preserved above."

### Issue 2: Dangling reference to non-existent cases in D-DP
**ASN-0061, DELETE as Composite Transition, step (ii)**: "When R = ∅ — Cases 1 and 4 of D-DP, where the deletion extends through the last position"
**Problem**: D-DP does not define numbered cases. No section of this ASN enumerates "Cases 1 and 4." This is a remnant from an earlier draft that apparently had a case analysis in D-DP. The surrounding prose — "where the deletion extends through the last position" — conveys the intent, but "Cases 1 and 4 of D-DP" points the reader at something that does not exist.
**Required**: Remove the dangling reference. Replace with a direct description, e.g., "When R = ∅ — the deletion extends through the last V-position in the subspace."

## OUT_OF_SCOPE

### Topic 1: Depth > 2 generalization
**Why out of scope**: D-PRE(iv) restricts to #p = 2 and the ASN correctly flags this as an open question. However, D-CTG-depth (ASN-0036) proves that at depth m ≥ 3, contiguity reduces to contiguity of the last component alone, and D-SEQ shows V_S(d) = {[S, 1, ..., 1, k] : 1 ≤ k ≤ n} at all depths. The key obstacle cited — commutativity of ordinal shift and subtraction (σ(v) + j = σ(v + j)) — holds whenever the interacting components are all at the same (last) position, which D-SEQ guarantees. The generalization appears tractable from the existing foundation but is new territory, not an error in this ASN.

VERDICT: REVISE
