# Review of ASN-0047

## REVISE

### Issue 1: Frame quantifier scope for M across elementary transitions
**ASN-0047, Elementary transitions (K.α, K.μ⁺, K.μ⁻, K.ρ)**: K.α and K.ρ state their M-frame as `(A d :: M'(d) = M(d))`; K.μ⁺ and K.μ⁻ state `(A d' : d' ≠ d : M'(d') = M(d'))`. None restricts to `E_doc`, where M is defined.

**Problem**: M(d) is defined iff d ∈ E\_doc (stated explicitly in the state model section). For d ∉ E\_doc, asserting `M'(d) = M(d)` asserts equality of undefined values — ill-formed in a formal specification. K.δ gets this right: `(A d ∈ E_doc : d ≠ e : M'(d) = M(d))`. The inconsistency across five transition definitions undermines the rigor that the rest of the ASN achieves. The same gap propagates into the convention `M(d) = ∅ for d ∈ E'_doc \ E_doc`, which patches over the undefined-value issue ad hoc in the coupling section rather than resolving it at the state model level.

**Required**: Either (a) restrict every M-frame quantifier to `E_doc` (or `E'_doc` as appropriate), matching K.δ's formulation — K.α: `(A d ∈ E_doc :: M'(d) = M(d))`, K.μ⁺/K.μ⁻: `(A d' ∈ E_doc : d' ≠ d :: M'(d') = M(d'))`, K.ρ: `(A d ∈ E_doc :: M'(d) = M(d))`; or (b) define M as a total function with default value ∅ outside E\_doc in the state model itself, which would make the existing quantifiers well-formed and absorb the coupling-section convention. Option (b) is cleaner — it resolves both the frame quantifier scope and the convention's ad hoc character in a single definition.

## OUT_OF_SCOPE

### Topic 1: Fork arrangement constraints relative to source
**Why out of scope**: The ASN defines fork with `ran(M'(d_new)) ⊆ ran(M(d_src))` — allowing proper subsets. Whether a forked document must replicate the source arrangement exactly (identical V→I mapping) or may select a subset is a higher-level design question about version semantics, not a gap in the transition model. Correctly identified as an open question.

### Topic 2: Subspace boundary constraints on reordering
**Why out of scope**: K.μ~'s bijection π is unconstrained across subspaces — it could map a text-subspace V-position to a link-subspace V-position. Whether reordering must respect subspace boundaries is a constraint that belongs in the subspace or link semantics ASN, not in the abstract transition taxonomy.

### Topic 3: Cross-document discoverability effects of contraction
**Why out of scope**: The ASN establishes that contraction is purely presentational (J2) and doesn't affect C, E, or R. Whether removing content from one document's arrangement affects link discoverability from another document is a link-layer question that depends on link traversal semantics not yet specified.

VERDICT: REVISE
