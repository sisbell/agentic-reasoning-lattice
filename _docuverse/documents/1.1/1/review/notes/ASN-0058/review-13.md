# Review of ASN-0058

## REVISE

### Issue 1: M14's general claim is asserted without proof
**ASN-0058, M14 commentary**: "More generally, any two blocks with partially overlapping I-extents at distinct V-positions are independently tracked. The mapping block algebra does not conflate shared content — it preserves each occurrence as a separate representational entity."
**Problem**: The formal lemma covers only the case where blocks share both I-start AND width. The broader claim about "partially overlapping I-extents" is correct (V-adjacent + I-extents overlap-but-not-adjacent ⟹ a₂ ≠ a₁ + n₁ ⟹ unmergeable) but the cases `a₁ < a₂ < a₁ + n₁` and `a₂ < a₁ < a₂ + n₂` are never analyzed. Commentary outruns the lemma.
**Required**: Either prove the general case (case-split on the form of overlap and show each fails I-adjacency a₂ = a₁ + n₁) or scope the commentary back to match the formal claim.

### Issue 2: M16's prefix-position bound is implicit
**ASN-0058, M16 proof**: "For element-level I-addresses, the document prefix N.0.U.0.D occupies positions strictly before #a₁, so it is preserved."
**Problem**: The proof asserts the prefix sits "strictly before #a₁" but never derives the position bound. The derivation requires S7b (zeros(a) = 3, so the tumbler has three separator zeros and the structure [N..., 0, U..., 0, D..., 0, E...]) combined with S7c (#E(a) ≥ 2) to show #(N.0.U.0.D) = #a − #E(a) ≤ #a − 2 < #a, which places every prefix position within the range [1, #a − 1] that TumblerAdd copies unchanged when action point = #a.
**Required**: Show the position calculation explicitly, citing S7b and S7c.

### Issue 3: M12 elides subspace/depth reasoning in the contiguity argument
**ASN-0058, M12 proof (uniqueness step)**: "Since V-extents are contiguous ranges at fixed depth (S8-depth), v₁ ≤ v₂ ≤ v and v ∈ V(R₁) imply v₂ ∈ V(R₁), so v₂ = v₁ + k₂ for some 0 ≤ k₂ < n₁."
**Problem**: Three steps are skipped: (a) v₂ shares subspace with v (since v ∈ V(R₂) and OrdShiftHom (b) makes all positions in a run share subspace), (b) at fixed depth m within that subspace, depth-m V-positions are enumerated by their m-th component, (c) v₁ ≤ v₂ ≤ v with prefix v₁ⱼ = v₂ⱼ for j < m (which itself needs justification) implies v₂ = v₁ + k₂. Without these, the contiguity inference is a hand-wave.
**Required**: Spell out subspace inheritance via OrdShiftHom and the depth-m enumeration that makes "contiguous range" precise.

### Issue 4: M12's elimination of v' < v + n is similarly opaque
**ASN-0058, M12 proof**: "If β' starts at v' < v + n, then V(β') = {v' + k : 0 ≤ k < n'} is a contiguous set containing v + n and starting before it; since v + n − 1 ∈ V(β), we would have v + n − 1 ∈ V(β') when v' ≤ v + n − 1, contradicting B2 (disjointness)."
**Problem**: The implication "v' ≤ v + n − 1 ⟹ v + n − 1 ∈ V(β')" is not derived. The chain is: v + n ∈ V(β') means v + n = v' + j for some j < n'; since v' < v + n, j ≥ 1; by M-aux, v + n − 1 = v' + (j − 1) ∈ V(β'). The proof asserts the conclusion without these arithmetic steps.
**Required**: Explicit derivation v + n − 1 = v' + (j − 1) ∈ V(β'), citing M-aux.

### Issue 5: M5(b)'s "functionality" clause is redundant and misleading
**ASN-0058, M5(b) verification**: "the V-extents are disjoint, and by the functionality of the mapping within each block, the full denotations are disjoint."
**Problem**: V-extent disjointness alone implies pair-set disjointness — pairs (v, a) ∈ ⟦β_L⟧ and (v', a') ∈ ⟦β_R⟧ have v ≠ v', so the pairs differ at the first component regardless of how the second component is determined. The appeal to "functionality of the mapping within each block" doesn't fire here and may mislead a reader looking for the actual argument.
**Required**: Remove the functionality clause; state that disjoint V-extents force disjoint pair sets directly.

## OUT_OF_SCOPE

None — the ASN stays within mapping-block algebra and content-reference resolution.

VERDICT: REVISE
