# ASN-0074: Permutation Model 0

*2026-03-22*

The permutation model (ASN-0058) defines block decompositions for document arrangements and proves existence and uniqueness of maximally merged canonical forms. This ASN extends the model with content references — a mechanism for identifying a span of positions within a document's arrangement — and resolution, which extracts the I-address runs from the block decomposition restricted to that span. The extension establishes that the canonical decomposition (M11, M12) applies to any restriction of an arrangement satisfying the structural preconditions, and that every resolved I-address satisfies referential integrity. We work with the content store C : T ⇀ Val and per-document arrangement M(d) : T ⇀ T from ASN-0036. Let D be the set of documents for which an arrangement is defined. The extension references properties from the foundation: S2 (ArrangementFunctionality), S3 (ReferentialIntegrity), S8-fin (FiniteArrangement), S8-depth (FixedDepthVPositions) from ASN-0036; T12 (SpanWellDefinedness) from ASN-0034; S6 (LevelConstraint) and ⟦σ⟧ (SpanDenotation) from ASN-0053.


## Content References

**Definition — ContentReference.** A *content reference* is a pair (d_s, σ) where d_s ∈ D and σ = (u, ℓ) is a level-uniform V-span satisfying: (i) V_{u₁}(d_s) ≠ ∅ — the subspace contains at least one V-position; (ii) T12 (ASN-0034) holds; (iii) `#ℓ = #u = m`, where m is the common V-position depth in subspace u₁ of d_s (S8-depth, ASN-0036); and (iv) m ≥ 2. Precondition (i) is necessary: S8-depth is vacuously true for an empty subspace and does not determine a common depth, so m is well-defined only when at least one V-position exists. Precondition (iv) ensures subspace confinement — that ⟦σ⟧ does not cross subspace boundaries; the derivation follows from C0a below. The level-uniformity requirement ensures reach(σ) has depth m (S6, ASN-0053), so the position range is well-bounded and the span algebra (S1–S11, ASN-0053) applies. The content reference is well-formed when every depth-m position in the span's range belongs to d_s's arrangement:

`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

By C0a (below), prefix confinement gives tⱼ = uⱼ for all j < m for every t ∈ ⟦σ⟧; in particular t₁ = u₁, so dom(M(d_s)) ∩ ⟦σ⟧ ⊆ V_{u₁}(d_s). By S8-depth, all V-positions in V_{u₁}(d_s) have depth m, and reach(σ) has depth m (S6), so the depth-m restriction is structurally guaranteed.

**C0 — OrdinalDisplacementNecessity (LEMMA).** For a well-formed content reference (d_s, σ) with σ = (u, ℓ), common depth m, and action point k of ℓ: k = m. Equivalently, ℓ = δ(ℓₘ, m) — an ordinal displacement.

*Derivation.* Suppose for contradiction that k < m. Consider the family of depth-m tumblers wⱼ = [u₁, ..., uₖ, uₖ₊₁, ..., u_{m−1}, j] for j > uₘ. Each wⱼ satisfies u < wⱼ: the two agree on components 1 through m − 1 and j > uₘ at component m, so wⱼ > u by T1(i) (ASN-0034). Each wⱼ satisfies wⱼ < reach(σ): at component k, uₖ < uₖ + ℓₖ (since ℓₖ ≥ 1, k being the action point), so wⱼ < reach(σ) by T1(i). Thus wⱼ ∈ ⟦σ⟧ for every j > uₘ. By T0(a) (ASN-0034), j ranges over unboundedly many values, yielding infinitely many depth-m tumblers in ⟦σ⟧. Well-formedness requires each to be in dom(M(d_s)), contradicting S8-fin (ASN-0036). Therefore k = m, and ℓ = [0, ..., 0, ℓₘ] = δ(ℓₘ, m). ∎

**C0a — PrefixConfinement (LEMMA).** For a well-formed content reference (d_s, σ) with σ = (u, ℓ) and m ≥ 2: every t ∈ ⟦σ⟧ satisfies tⱼ = uⱼ for all 1 ≤ j < m.

*Derivation.* By C0, the action point of ℓ is m. Since m ≥ 2, TumblerAdd gives reach(σ)ⱼ = uⱼ for all j < m. Fix any t ∈ ⟦σ⟧, so u ≤ t < reach(σ). Suppose for contradiction that J = {j : 1 ≤ j < m ∧ tⱼ ≠ uⱼ} is non-empty, and let j₀ = min(J). Then tᵢ = uᵢ for all 1 ≤ i < j₀, so the divergence of t and u is at position j₀. Since u ≤ t, T1(i) (ASN-0034) gives t_{j₀} > u_{j₀}. Since reach(σ)_{j₀} = u_{j₀} and tᵢ = uᵢ = reach(σ)ᵢ for all i < j₀, the divergence of t and reach(σ) is also at j₀ with t_{j₀} > reach(σ)_{j₀}. By T1(i), t > reach(σ), contradicting t < reach(σ). Therefore J = ∅, i.e., tⱼ = uⱼ for all 1 ≤ j < m. In particular, t₁ = u₁ (subspace confinement). (At m = 1, the vacuous range 1 ≤ j < 1 yields no confinement; indeed the action point would be 1, giving reach(σ)₁ = u₁ + ℓ₁ ≠ u₁, and ⟦σ⟧ would span multiple subspaces.) ∎

**Definition — ContentReferenceSequence.** A *content reference sequence* is an ordered list R = ⟨r₁, ..., rₚ⟩ of content references with p ≥ 1. Different references may name different source documents.


## Resolution

To resolve a content reference, we extract the I-address runs corresponding to the named V-span. The source document's mapping may not be ordinal-contiguous across the full span — prior editing may have interleaved content from multiple allocations, fragmenting the V→I mapping into several contiguous I-address runs.

**Definition — Resolution.** Given content reference (d_s, σ) with σ = (u, ℓ), let f = M(d_s)|⟦σ⟧ be the restriction of M(d_s) to positions in ⟦σ⟧.

**C1a — RestrictionDecomposition (COROLLARY).** M11 and M12 (ASN-0058) hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, and S8-depth. In particular, the restriction f = M(d_s)|⟦σ⟧ admits a unique maximally merged block decomposition.

*Verification that f satisfies the conditions.* (i) S2 (functionality): f is a restriction of M(d_s), which is functional by S2; a restriction of a function is a function. (ii) S8-fin (finite domain): dom(f) ⊆ dom(M(d_s)), which is finite by S8-fin; a subset of a finite set is finite. (iii) S8-depth (fixed depth): by C0a, every position in dom(f) has first component u₁, so dom(f) ⊆ V_{u₁}(d_s); by S8-depth, all positions in V_{u₁}(d_s) share the common depth m.

*Extension of M11/M12.* M11 (CanonicalExistence) constructs a maximally merged decomposition by iterating: while any two blocks satisfy the merge condition (M7), merge them. The initial singleton-block decomposition — one block (v, f(v), 1) per v ∈ dom(f) — satisfies B1, B2, and B3: B1 (coverage) holds because every v ∈ dom(f) has its own singleton block; B2 (disjointness) holds because singleton V-extents are pairwise disjoint; B3 (consistency) holds directly from S2 (f is a function, so each singleton block's I-address is uniquely determined). Termination follows from S8-fin since the block count is at most |dom(f)|. Each merge step preserves all three conditions by M7f (MergeFrame, ASN-0058): M7f establishes that replacing β₁ and β₂ with β₁ ⊞ β₂ yields an equivalent decomposition, preserving B1 and B2 via V(β₁ ⊞ β₂) = V(β₁) ∪ V(β₂) (no V-position is gained or lost, and all blocks in B \ {β₁, β₂} are unchanged). For B3 specifically: if β₁ = (v₁, a₁, n₁) and β₂ = (v₂, a₂, n₂) each satisfy B3 and M7 holds (v₂ = v₁ + n₁, a₂ = a₁ + n₁), then β₁ ⊞ β₂ = (v₁, a₁, n₁ + n₂) satisfies B3 by case split — for 0 ≤ i < n₁, f(v₁ + i) = a₁ + i by B3 for β₁; for n₁ ≤ i < n₁ + n₂, f(v₁ + i) = f(v₂ + (i − n₁)) = a₂ + (i − n₁) = (a₁ + n₁) + (i − n₁) = a₁ + i, using B3 for β₂ and M-aux (ASN-0058). M12 (CanonicalUniqueness) identifies the maximally merged decomposition with the set of maximal runs of f, using only pointwise evaluation of f — independent of whether f is a full arrangement or a restriction. Both proofs require no property of M(d) beyond S2, S8-fin, and S8-depth; they apply to f verbatim. ∎

The decomposition yields ⟨β₁, ..., βₖ⟩ ordered by V-start. The *I-address sequence* is:

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where βⱼ = (vⱼ, aⱼ, nⱼ). The V-coordinates are discarded; only I-starts and widths are carried forward.

The ordering of runs within each resolution preserves the source document's V-ordering: if V-position p precedes V-position q in the source, the I-address at p precedes the I-address at q in the resolved sequence. This follows from the definition of resolve, which specifies the blocks ordered by V-start. The ordering is well-defined because V-extents are disjoint (B2, ASN-0058), so the V-starts induce a total order on the blocks.

For a content reference sequence R = ⟨r₁, ..., rₚ⟩, the *composite resolution* concatenates:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

Each reference is resolved independently against its own source document's POOM. The *total width* of an I-address sequence ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ is:

`w(⟨(a₁, n₁), ..., (aₖ, nₖ)⟩) = (+ j : 1 ≤ j ≤ k : nⱼ)`

For a content reference sequence R, the total width is w(resolve(R)).

**C1 — ResolutionIntegrity (LEMMA).** Every resolved I-address is in dom(C):

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

*Derivation.* Fix any run (aⱼ, nⱼ) in the resolution and any i with 0 ≤ i < nⱼ. The corresponding block βⱼ = (vⱼ, aⱼ, nⱼ) satisfies B3 (ASN-0058): M(d_s)(vⱼ + i) = aⱼ + i. Since vⱼ + i ∈ dom(M(d_s)), S3 (ReferentialIntegrity, ASN-0036) gives M(d_s)(vⱼ + i) ∈ dom(C), hence aⱼ + i ∈ dom(C). ∎


**C2 — ResolutionWidthPreservation (LEMMA).** For a well-formed content reference (d_s, σ) with σ = (u, δ(ℓₘ, m)), the total resolved width equals ℓₘ:

`w(resolve(d_s, σ)) = (+ j : 1 ≤ j ≤ k : nⱼ) = ℓₘ`

*Derivation.* By C0, ℓ = δ(ℓₘ, m), so reach(σ) = u ⊕ δ(ℓₘ, m) = [u₁, ..., u_{m−1}, uₘ + ℓₘ]. The depth-m tumblers in [u, reach(σ)) are exactly {[u₁, ..., u_{m−1}, j] : uₘ ≤ j < uₘ + ℓₘ}: by C0a (PrefixConfinement), every t ∈ ⟦σ⟧ satisfies tⱼ = uⱼ for all 1 ≤ j < m, fixing the first m − 1 components; the m-th component then ranges over uₘ ≤ tₘ < uₘ + ℓₘ (from u ≤ t < reach(σ) at divergence point m). There are ℓₘ such tumblers; well-formedness places each in dom(f). Conversely, dom(f) contains no other elements: C0a fixes all components before m, and S8-depth ensures every position in V_{u₁}(d_s) has depth m, so the enumeration is exhaustive. Therefore |dom(f)| = ℓₘ. By B1 (coverage) and B2 (disjointness), the V-extents of the blocks partition dom(f). By M0 (width coupling), |V(βⱼ)| = nⱼ for each block. Therefore (+ j : 1 ≤ j ≤ k : nⱼ) = |dom(f)| = ℓₘ. ∎


## Worked Example

We verify the definitions against a concrete scenario. Let document d have depth-2 V-positions in subspace 1 (m = 2) with canonical decomposition:

`B = {β₁ = ([1,1], a, 3),  β₂ = ([1,4], b, 2),  β₃ = ([1,6], c, 1)}`

where a, b, c are distinct I-addresses with `origin(a) ≠ origin(b) ≠ origin(c)` — three runs of content transcluded from three distinct source documents. The arrangement maps six V-positions: M(d)([1,1]) = a, M(d)([1,2]) = a+1, M(d)([1,3]) = a+2, M(d)([1,4]) = b, M(d)([1,5]) = b+1, M(d)([1,6]) = c.

**Content reference.** Take σ = ([1,2], δ(4, 2)) — start at V-position [1,2] with ordinal displacement [0,4]. Then reach(σ) = [1,2] ⊕ [0,4] = [1,6]. The span range is {v : [1,2] ≤ v < [1,6] ∧ #v = 2} = {[1,2], [1,3], [1,4], [1,5]}. Each is in dom(M(d)), so the reference is well-formed. The displacement is ordinal (action point 2 = m), consistent with C0.

**Restriction.** f = M(d)|⟦σ⟧ has domain {[1,2], [1,3], [1,4], [1,5]} with f([1,2]) = a+1, f([1,3]) = a+2, f([1,4]) = b, f([1,5]) = b+1.

**Decomposition (C1a).** We verify f satisfies the preconditions: (i) f is functional (restriction of a function); (ii) dom(f) has 4 elements (finite); (iii) all V-positions have depth 2. Starting from singleton blocks {([1,2], a+1, 1), ([1,3], a+2, 1), ([1,4], b, 1), ([1,5], b+1, 1)}, we merge:

- [1,2] and [1,3]: V-adjacent ([1,3] = [1,2]+1) and I-adjacent (a+2 = (a+1)+1). Merge → ([1,2], a+1, 2).
- [1,4] and [1,5]: V-adjacent ([1,5] = [1,4]+1) and I-adjacent (b+1 = b+1). Merge → ([1,4], b, 2).

No further merges: ([1,2], a+1, 2) and ([1,4], b, 2) are V-adjacent ([1,4] = [1,2]+2) but not I-adjacent. M16 (ASN-0058) gives b ≠ (a+1)+2: ordinal increment preserves the document prefix, so origin((a+1)+2) = origin(a), while origin(b) ≠ origin(a) by construction. The decomposition is maximally merged.

**Resolution.** resolve(d, σ) = ⟨(a+1, 2), (b, 2)⟩, ordered by V-start.

**C1 verification.** For run (a+1, 2): B3 gives M(d)([1,2]) = a+1 and M(d)([1,3]) = a+2; S3 gives a+1 ∈ dom(C) and a+2 ∈ dom(C). For run (b, 2): B3 gives M(d)([1,4]) = b and M(d)([1,5]) = b+1; S3 gives b ∈ dom(C) and b+1 ∈ dom(C). ✓

Total width: 2 + 2 = 4 = ℓₘ, confirming C2.


## Properties Introduced

| Label | Statement | Status |
|-------|-----------|--------|
| ContentReference | (d_s, σ) with d_s ∈ D, V_{u₁}(d_s) ≠ ∅, m ≥ 2; σ level-uniform with #u = #ℓ = m; depth-m V-positions in span range ⊆ dom(M(d_s)) | introduced |
| C0 | well-formed content references have ordinal displacements: action point of ℓ equals m | introduced |
| C0a | prefix confinement: every t ∈ ⟦σ⟧ satisfies tⱼ = uⱼ for all 1 ≤ j < m when m ≥ 2 (subspace confinement t₁ = u₁ is the j = 1 case) | introduced |
| ContentReferenceSequence | ordered list ⟨r₁, ..., rₚ⟩ with p ≥ 1 | introduced |
| resolve(d_s, σ) | maximally merged I-address runs from M(d_s)\|⟦σ⟧, V-ordered | introduced |
| C1a | M11/M12 hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, S8-depth; in particular M(d_s)\|⟦σ⟧ | introduced |
| C1 | every resolved I-address is in dom(C) | introduced |
| C2 | total resolved width equals ordinal displacement: w(resolve(d_s, σ)) = ℓₘ | introduced |


## Open Questions

- Must the resolution ordering across a multi-source content reference sequence preserve the sequence order, or may an implementation reorder source references provided the placed content lands at the correct V-positions?
