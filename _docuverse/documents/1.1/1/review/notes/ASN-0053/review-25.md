# Review of ASN-0053

## REVISE

### Issue 1: S11 tightness claim asserted without derivation

**ASN-0053, S11 proof, closing paragraph**: "The bound of two is tight and inherent in removing a contiguous sub-range from a contiguous range on a linear order."

**Problem**: The proof exhibits the three sub-cases (0, 1, 2 spans) and produces 2 spans in the "neither boundary coincides" case. But "tight" means no fewer than 2 spans can suffice in that case — and this is asserted by appeal to intuition ("inherent in...") rather than derived. The cases (a) and (b) are correctly bounded; case (c) needs an explicit argument that 1 span cannot represent the result.

**Required**: Add a brief derivation. The left and right remainders satisfy reach(λ) = start(β) < reach(β) = start(ρ), so they are separated (non-adjacent, by N2's strict inequality). By S0 (convexity), a single span denotes a convex interval, but ⟦λ⟧ ∪ ⟦ρ⟧ has a gap (the excised range ⟦β⟧) and is not convex. Therefore no single span can represent the result. Two is the minimum.

### Issue 2: S11c Case 1 lacks explicit element-chase

**ASN-0053, S11c proof, Case 1**: "The positions in ⟦α⟧ but not in ⟦β⟧ are those in α that precede the start of β: ⟦α⟧ \ ⟦β⟧ = {t : start(α) ≤ t < start(β)}"

**Problem**: Case 2 of the same lemma derives its difference equation by explicit element-chasing. Case 1 just states the equation. Both directions of the set equality should be derived for consistency, especially since the proof's standards (no proof by checkmark, no proof by similarity) apply within a single proof.

**Required**: Add the element-chase. For (⊆): t ∈ ⟦α⟧ \ ⟦β⟧ means start(α) ≤ t < reach(α) and (t < start(β) ∨ t ≥ reach(β)); since t < reach(α) < reach(β), the second disjunct fails, so t < start(β). For (⊇): start(α) ≤ t < start(β) < reach(α) gives t ∈ ⟦α⟧, and t < start(β) gives t ∉ ⟦β⟧.

### Issue 3: S7 claim is trivially achievable; proof's content unstated

**ASN-0053, S7**: "Every finite set of positions P ⊂ T admits a span-set Σ with ⟦Σ⟧ ⊇ P."

**Problem**: The covering condition ⊇ is achievable by a single span containing all of P with no constraint on minimality. The proof constructs |P| spans, one per element — but the claim doesn't capture this structural content. Without a bound on |Σ| or a tightness criterion, S7 collapses to "spans exist and can be unioned."

**Required**: Either strengthen the claim (e.g., "admits a span-set Σ with |Σ| ≤ |P| and ⟦Σ⟧ ⊇ P") to match what the proof actually shows, or state explicitly that this is a sufficiency-only claim used downstream just to establish coverage existence. As written, the proof exceeds the claim.

### Issue 4: Symmetry-by-relabeling in S3b Case B is left implicit

**ASN-0053, S3b proof, Case B**: "By S3a (merge commutativity) the merge of α and β equals the merge of β and α, which is the Case A configuration with the roles of α and β exchanged. Applying Case A to the pair ⟨β, α⟩, splitting the merged span at the shared boundary start(α) recovers β as the left part and α as the right part. Relabeling, the original spans α and β are recovered exactly."

**Problem**: The "relabeling" step is correct but the conclusion to verify is that *the original* α and β are recovered as the original ordered pair, not merely as the set {α, β}. S4 produces a left part (λ) and a right part (ρ). In Case B, Case A applied to ⟨β, α⟩ identifies β as left, α as right. Whether this counts as "recovering α and β exactly" depends on whether S3b is claiming recovery of the ordered pair or the unordered pair. The statement of S3b doesn't specify.

**Required**: Either state S3b's conclusion as "the unordered pair {α, β} is recovered" (since S3 is commutative anyway), or pin down which span is recovered as λ vs ρ in each case and verify.

## OUT_OF_SCOPE

### Topic 1: Span-set difference and intersection

**Why out of scope**: The ASN's open questions explicitly raise this — generalizing S1 and S11 to span-sets is acknowledged as future work and would belong in a downstream ASN or revision.

### Topic 2: Cross-level / cross-subspace span operations

**Why out of scope**: The ASN explicitly restricts to level-uniform, level-compatible spans (S6), and lists cross-level operations as open questions. Belongs in a future ASN, perhaps on subspace boundaries.

### Topic 3: Behavior of normalization under address allocation

**Why out of scope**: The ASN notes that normalization is canonical at a moment in time but that allocation of new addresses can invalidate minimality. This is acknowledged as open and belongs in a future ASN handling temporal evolution of the address space.

VERDICT: REVISE
