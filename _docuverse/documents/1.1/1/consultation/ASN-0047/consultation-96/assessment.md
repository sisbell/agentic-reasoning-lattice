# Channel Assignment — ASN-0047 review-96

**Date:** 2026-05-18 00:22

## Issue 1: Reference error in S4 cross-document distinctness
Reason: Pure cross-reference fix — the lemma's location in the ASN is verifiable internally. Update the pointer to "Allocator hierarchy under documents section" where the Cross-document disjointness chain lemma is stated and proved.

## Issue 2: NodeAllocationRegistry minimal requirement is incomplete
Reason: The structural conjunct `n₀ ≼ e` is already load-bearing in K.δ case (i)'s precondition and in NodeLineage's discharge; making it an explicit registry obligation is a presentational consolidation derivable from the ASN's own content.

## Issue 3: "Why SubAllocatorAxiom anyway" is essay content in a structural slot
Reason: Pure stylistic cleanup — removing rationale paragraphs that justify rather than specify. No external evidence required; load-bearing facts (if any) are already cited elsewhere or can be re-encoded at use sites.

## Issue 4: Bootstrap n₀ = [1] design-rationale prose
Reason: Pure stylistic cleanup — delete the second paragraph that defends the choice of `[1]` with LM citations and counterfactuals. The first paragraph already provides the structural form needed by downstream proofs.

## Issue 5: NodeLineage consequence to non-node entities not derived
Reason: GlobalLineage is derivable entirely from existing ASN properties (NodeLineage + P8 + ≼-transitivity + P6 + S7a). The corollary requires only internal synthesis, not new evidence.

## Issue 6: P5 proof refers to "five elementary transitions" but the system has more
Reason: Pure presentation fix — clarify that P5 is stated at the pre-extension state context (where five elementary transitions is correct) and that P3 picks up the L-clause in the extended state. The ASN's own structure provides the context.

## Issue 7: K.δ k = 0 sub-case implicit constraint on operand
Reason: The `¬IsNode(t)` requirement is derivable from T4b's partiality of `parent(t)` combined with K.δ's case-level `¬IsElement(e)` and the structural identity `zeros(e) = zeros(t)`. Making the implicit explicit is purely internal.
