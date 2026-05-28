# Review of ASN-0101

## REVISE

### Issue 1: Cross-document example's "lost element" phrasing conflates two notions
**ASN-0101, "A cross-document transclusion example" section**: "project(L'(ℓ_0).e_1, d, Σ') = {[1, 1, 1]} (post-state on d: M'(d)([1, 1, 1]) = a_2 ∈ coverage). Cardinality has shrunk from 2 to 1; the lost element is the deleted V-position [1, 1, 1] whose image was a_1."

**Problem**: The "lost element" identifies pre-state V-position [1,1,1] (whose image was a_1, now removed), but post-state projection also contains tumbler [1,1,1] (now witnessing via image a_2). Set-theoretically, [1,1,1] ∈ project_pre ∩ project_post, so under ASN-0098's definition of projection as a set of V-positions, [1,1,1] is *not* the lost element — by set difference, project_pre \ project_post = {[1,1,2]}. The "lost" piece is the witnessing relationship (V-position [1,1,1], image a_1), not the tumbler itself. The phrasing conflates "V-position whose mapping no longer holds" with "tumbler no longer in the projection set."

**Required**: Rephrase to distinguish the two. For example: "Set-theoretically, the projection has shrunk from {[1,1,1], [1,1,2]} to {[1,1,1]} — losing tumbler [1,1,2]. The mechanism: pre-state V-position [1,1,1] (image a_1) was deleted, and pre-state [1,1,2] (image a_2) was renamed by σ_d to post-state [1,1,1] (still mapping to a_2). The tumbler [1,1,1] survives as a projection witness, but with a different image."

### Issue 2: D7 justification's "converse of L0" reasoning is logically compressed
**ASN-0101, D7 — Attribution survival under DELETE**: "L0 (ASN-0093) bridges store-membership to I-address subspace: a ∈ dom(C) ⟹ subspace_I(a) = s_C and a ∈ dom(L) ⟹ subspace_I(a) = s_L. The two directions, composed, give the 'Equivalently' clause's statement: subspace_I(a) = s_C ⟹ a ∈ dom(C) and subspace_I(a) = s_L ⟹ a ∈ dom(L) (the converse of L0 is supplied by L14's disjointness...)."

**Problem**: "The two directions, composed" suggests that composing L0's forward implications yields converse implications. This is not how implicational logic works — composing forward implications yields more forward implications, not reverses. The actual argument requires the precondition `a ∈ dom(C) ∪ dom(L)` (derived above from a ∈ ran(M(d)) plus S3★) plus L14's disjointness: assuming subspace_I(a) = s_C and a ∈ dom(L) leads via L0 to subspace_I(a) = s_L, contradicting the hypothesis; combined with a ∈ dom(C) ∪ dom(L), this forces a ∈ dom(C).

**Required**: Replace the "two directions, composed" wording with the explicit conditional argument: "Combined with the previously established a ∈ dom(C) ∪ dom(L) and L14's disjointness, L0's forward directions yield conditional converses: if subspace_I(a) = s_C, then a ∉ dom(L) (since a ∈ dom(L) would force subspace_I(a) = s_L by L0), so a ∈ dom(C) by the partition; symmetrically for s_L."

## OUT_OF_SCOPE

(None — the ASN appropriately scopes its content. The Open Questions list correctly defers versioning mechanics, DEL+INSERT reversibility, and broader recoverability to other ASNs.)

VERDICT: REVISE
