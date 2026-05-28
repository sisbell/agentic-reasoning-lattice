# Review of ASN-0077

## REVISE

### Issue 1: Misattributed citation in O11 sub-case (b)
**ASN-0077, O11 (⊇) direction, Case (ii) Sub-case (b)**: "But the newly added position has subspace(v) = s_C (by SC-NEQ, ASN-0047). So v ∉ ⟦σ⟧..."
**Problem**: SC-NEQ establishes `s_C ≠ s_L`; it does *not* establish `subspace(v) = s_C`. The latter is established by KMuPlusContentSubspaceRestriction (cited at the start of Case (ii)). SC-NEQ is needed for the implicit `s_C ≠ s_L` step that combines with C0a's `t_1 = s_L` for `t ∈ ⟦σ⟧` to yield `v ∉ ⟦σ⟧`. The parallel O11' Sub-case (a) places SC-NEQ correctly: "subspace(v_ℓ) = s_L ≠ s_C (SC-NEQ, ASN-0047)". Structurally identical reasoning is cited differently across the two cases.
**Required**: Restructure O11 sub-case (b) consistent with O11' sub-case (a). For example: "subspace(v) = s_C (established at the start of Case (ii) via KMuPlusContentSubspaceRestriction). Since s_C ≠ s_L (by SC-NEQ, ASN-0047) and every t ∈ ⟦σ⟧ has t_1 = s_L (by C0a), v ∉ ⟦σ⟧."

VERDICT: REVISE
