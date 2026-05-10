# Review of ASN-0065

## REVISE

### Issue 1: Variable collision in R-BLK B3 verification
**ASN-0065, Block Decomposition**: "for each block (π(vₖ), aₖ, nₖ) and each k with 0 ≤ k < nₖ, M'(d)(π(vₖ) + k) = M'(d)(π(vₖ + k)) = M(d)(vₖ + k) = aₖ + k"
**Problem**: `k` is used simultaneously as the block subscript (in vₖ, aₖ, nₖ — identifying which block) and as the bound offset variable (0 ≤ k < nₖ — iterating within the block). This creates a circular dependency: nₖ depends on the block index k, yet k also ranges over 0 ≤ k < nₖ. In a specification that aspires to formal rigor, this is an ambiguous quantifier binding.
**Required**: Use distinct variables — e.g., "for each block j, the reassembled block is (π(vⱼ), aⱼ, nⱼ), and for each offset k with 0 ≤ k < nⱼ: M'(d)(π(vⱼ) + k) = aⱼ + k."

### Issue 2: R-KMU cites R-PIV/R-SWP for a claim they do not fully establish
**ASN-0065, K.μ~ Precondition Verification**: "π maps dom(M(d)) to itself — dom(M'(d)) = dom(M(d)), established in R-PIV and R-SWP"
**Problem**: R-PIV and R-SWP establish that the postcondition defines a total function on V_S(d) — the text-subspace portion of dom(M(d)). They do not address non-S subspace positions. The full domain equality dom(M'(d)) = dom(M(d)) additionally requires R-XS (which establishes M'(d)(v) = M(d)(v) for subspace(v) ≠ S), or equivalently, noting that the exterior case of π maps non-S positions to themselves. The citation chain is incomplete: the referenced lemmas support only the subspace-S portion of the claim.
**Required**: Cite R-XS (or the exterior case of π covering non-S positions) alongside R-PIV/R-SWP when claiming dom(M'(d)) = dom(M(d)).

## OUT_OF_SCOPE

None. The open questions identified by the ASN (k-cut generalization, composition closure, block-count bounds, depth generalization, front-end rendering of split endsets) are appropriate future work and correctly excluded from the current scope.

VERDICT: REVISE
