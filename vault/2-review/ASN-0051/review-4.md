# Review of ASN-0051

## REVISE

### Issue 1: SV6 proof conflates T5 with the necessary sandwich argument
**ASN-0051, SV6 (CrossOriginExclusion)**: "Since origin(s) is a prefix of both s and s ⊕ ℓ, by T5 (ContiguousSubtrees) every tumbler t with s ≤ t < s ⊕ ℓ satisfies origin(s) ≼ t. Now restrict to element-level tumblers: if zeros(t) = 3, then t has the same field structure as s"
**Problem**: T5 establishes origin(s) ≼ t, but this alone does not give origin(t) = origin(s) for element-level t. A tumbler t with origin(s) ≼ t and zeros(t) = 3 could have a longer document field — e.g., t = N.0.U.0.D₁.D₂.0.E while s = N.0.U.0.D₁.0.E', giving origin(t) = N.0.U.0.D₁.D₂ ≠ origin(s) = N.0.U.0.D₁. The sentence "if zeros(t) = 3, then t has the same field structure" reads as following from T5, when in fact it requires the sandwich argument that appears later ("disagreement at an earlier position would place t outside the interval by T1"). That sandwich argument — t agrees with s on all positions before k, which is past the third separator — is the primary mechanism. T5 gives a weaker prefix condition; the sandwich gives the component-level agreement that forces the third separator to be at the same position. As written, a reader could conclude that T5 + zeros(t) = 3 suffices, which it does not.
**Required**: Restructure the proof to lead with the sandwich argument as the primary step. State explicitly: (1) for any t with s ≤ t < s ⊕ ℓ, t agrees with s on all positions 1 through k−1 (because disagreement at position j < k gives t_j > s_j = (s ⊕ ℓ)_j, forcing t > s ⊕ ℓ by T1); (2) since k is within the element field, k−1 is past the third separator, so t shares the same three separator positions as s; (3) therefore for element-level t (zeros(t) = 3), origin(t) = origin(s). T5 can remain as supporting context for the prefix property, but the proof's weight should be on the sandwich argument.

### Issue 2: SV10 formal statement has a redundant conjunct and is narrower than the prose
**ASN-0051, SV10 (DiscoveryResolutionIndependence)**: "`(E Σ, a, d, s, V ⊆ dom(M(d)) :: a ∈ discover_s({M(d)(v) : v ∈ V}) ∧ resolve(Σ.L(a).s, d) ≠ ∅ ∧ π(Σ.L(a).s, d) ⊊ coverage(Σ.L(a).s))`"
**Problem**: Two issues. First, conjunct 2 (resolve ≠ ∅) is redundant given conjunct 1. If a ∈ discover_s(A) where A = {M(d)(v) : v ∈ V} ⊆ ran(M(d)), then coverage(Σ.L(a).s) ∩ ran(M(d)) ⊇ coverage(Σ.L(a).s) ∩ A ≠ ∅, so π(Σ.L(a).s, d) ≠ ∅, which is equivalent to resolve ≠ ∅. The redundancy suggests the author expected conjuncts 1 and 2 to be independent; they are not when A comes from d's arrangement. Second, the prose says "a link might be discovered from a version or transclusion that shares only a subset of the endset's I-addresses. The link is found, but resolution (in any given document) may return a partial or even empty result" — but the formal statement cannot produce empty resolution (as shown), and it operates within a single document, not across documents.
**Required**: Either (a) drop the redundant conjunct and add a note that discovery through d entails non-empty projection in d; or (b) reformulate to capture the cross-document case (discover through d₁, resolve in d₂ where π in d₂ may be empty). Either way, align the prose with the formal statement's actual strength.

### Issue 3: SV11 decomposition covers text-subspace blocks only but claims equality with full π(e, d)
**ASN-0051, SV11 (PartialSurvivalDecomposition)**: "`π(e, d) = (∪ j, k : 1 ≤ j ≤ m ∧ 1 ≤ k ≤ p : ⟦(sⱼ, ℓⱼ)⟧ ∩ I(β_k))`"
**Problem**: B = {β₁, ..., β_p} is a block decomposition per ASN-0058, which covers text-subspace V-positions only (B1 guards v₁ ≥ 1). So ∪_k I(β_k) = ran_text(M(d)). The right-hand side thus equals coverage(e) ∩ ran_text(M(d)). The left-hand side is π(e, d) = coverage(e) ∩ ran(M(d)). The equation holds only if ran(M(d)) = ran_text(M(d)). But the foundation model permits non-text-subspace V-positions in M(d): S8-depth ranges over all subspaces, S8a is conditional on v₁ ≥ 1, and K.μ⁺ imposes no restriction on the first component of new V-positions. If a non-text V-position maps to an I-address in coverage(e) not covered by any text V-position, the formula undercounts π(e, d).
**Required**: Either (a) restrict π in SV11 to the text-subspace projection: π_text(e, d) = coverage(e) ∩ ran_text(M(d)), with a note that the link-subspace contribution is deferred to the Link Subspace ASN; or (b) state the assumption that in the current model all V-positions in M(d) are text-subspace, citing the absence of any foundation operation that creates non-text V-positions; or (c) extend the decomposition to all subspaces. Option (a) or (b) is a one-line fix.

### Issue 4: Bilateral vitality prose contradicts formula
**ASN-0051, Endset Projection section**: "A link at address a … is *bilaterally vital in d* when both its from-endset and to-endset are vital in d: `F = ∅ ∨ π(F, d) ≠ ∅`  and  `G = ∅ ∨ π(G, d) ≠ ∅`"
**Problem**: The prose says "both its from-endset and to-endset are vital in d." But vitality is defined as π(e, d) ≠ ∅. An empty endset F = ∅ gives π(F, d) = ∅, which is NOT vital. Yet the formula's F = ∅ disjunct satisfies bilateral vitality. The formula and the prose describe different conditions: the formula says "each non-empty content endset is vital"; the prose says "both endsets are vital."
**Required**: Change the prose to match the formula. E.g., "is bilaterally vital in d when each non-empty content endset is vital in d — that is, every non-empty endset projects to at least one I-address in d's arrangement."

## OUT_OF_SCOPE

### Topic 1: Composite operation survivability
The ASN analyzes elementary transitions (K.μ⁺, K.μ⁻, K.μ~). Higher-level operations (INSERT, DELETE, COPY, MAKELINK) compose these elementary steps and their survivability properties follow by composition, but the derivations are not shown here. These belong in the respective operation ASNs.
**Why out of scope**: Each composite operation deserves its own survivability analysis as part of its specification — not as a patch to this ASN.

### Topic 2: Fork survivability formal derivation
The ASN notes in prose that fork (J4) preserves discovery through shared I-addresses, but does not formalize this as a property. A derivation from SV2 + SV7 + J4's construction is natural but deferred to the open questions.
**Why out of scope**: Fork semantics are partially analysed but the formal property belongs with the versioning model, not the survivability invariants.

### Topic 3: Multi-document bilateral vitality
A link could have its from-endset vital in d₁ and its to-endset vital in d₂ (with neither document satisfying bilateral vitality alone). The ASN defines bilateral vitality within a single document and does not analyse the cross-document case.
**Why out of scope**: Cross-document link utility is a higher-level concern that requires the inter-document discovery model, not yet specified.

VERDICT: REVISE
