# ASN-0074 Formal Statements

*Source: ASN-0074-permutation-model-0.md (revised 2026-03-22) — Extracted: 2026-03-22*

## Definition — ContentReference

A *content reference* is a pair (d_s, σ) where d_s ∈ D and σ = (u, ℓ) is a level-uniform V-span satisfying:
- (i) V_{u₁}(d_s) ≠ ∅
- (ii) T12 (ASN-0034) holds
- (iii) `#ℓ = #u = m`, where m is the common V-position depth in subspace u₁ of d_s (S8-depth, ASN-0036)
- (iv) m ≥ 2

Well-formedness condition:
`{v ∈ T : u ≤ v < reach(σ) ∧ #v = m} ⊆ dom(M(d_s))`

## Definition — ContentReferenceSequence

A *content reference sequence* is an ordered list R = ⟨r₁, ..., rₚ⟩ of content references with p ≥ 1. Different references may name different source documents.

## Definition — Resolution

Given content reference (d_s, σ) with σ = (u, ℓ), let f = M(d_s)|⟦σ⟧ be the restriction of M(d_s) to positions in ⟦σ⟧.

`resolve(d_s, σ) = ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩`

where βⱼ = (vⱼ, aⱼ, nⱼ) are the blocks of the maximally merged decomposition of f, ordered by V-start.

## Definition — CompositeResolution

For a content reference sequence R = ⟨r₁, ..., rₚ⟩:

`resolve(R) = resolve(r₁) ⌢ ... ⌢ resolve(rₚ)`

## Definition — TotalWidth

The *total width* of an I-address sequence ⟨(a₁, n₁), ..., (aₖ, nₖ)⟩ is:

`w(⟨(a₁, n₁), ..., (aₖ, nₖ)⟩) = (+ j : 1 ≤ j ≤ k : nⱼ)`

---

## C0 — OrdinalDisplacementNecessity (LEMMA, lemma)

For a well-formed content reference (d_s, σ) with σ = (u, ℓ), common depth m, and action point k of ℓ: k = m. Equivalently, ℓ = δ(ℓₘ, m) — an ordinal displacement.

## C0a — PrefixConfinement (LEMMA, lemma)

For a well-formed content reference (d_s, σ) with σ = (u, ℓ) and m ≥ 2: every t ∈ ⟦σ⟧ satisfies tⱼ = uⱼ for all 1 ≤ j < m.

In particular t₁ = u₁ (subspace confinement).

## C1a — RestrictionDecomposition (COROLLARY, lemma)

M11 and M12 (ASN-0058) hold for any finite partial function f : T ⇀ T satisfying S2, S8-fin, and S8-depth. In particular, the restriction f = M(d_s)|⟦σ⟧ admits a unique maximally merged block decomposition.

Conditions verified for f = M(d_s)|⟦σ⟧:
- (i) S2 (functionality): f is a restriction of M(d_s), which is functional; a restriction of a function is a function.
- (ii) S8-fin (finite domain): dom(f) ⊆ dom(M(d_s)), finite by S8-fin; a subset of a finite set is finite.
- (iii) S8-depth (fixed depth): by C0a, every position in dom(f) has first component u₁, so dom(f) ⊆ V_{u₁}(d_s); by S8-depth, all positions in V_{u₁}(d_s) share the common depth m.

## C1 — ResolutionIntegrity (LEMMA, lemma)

Every resolved I-address is in dom(C):

`(A j : 1 ≤ j ≤ k : (A i : 0 ≤ i < nⱼ : aⱼ + i ∈ dom(C)))`

## C2 — ResolutionWidthPreservation (LEMMA, lemma)

For a well-formed content reference (d_s, σ) with σ = (u, δ(ℓₘ, m)), the total resolved width equals ℓₘ:

`w(resolve(d_s, σ)) = (+ j : 1 ≤ j ≤ k : nⱼ) = ℓₘ`
