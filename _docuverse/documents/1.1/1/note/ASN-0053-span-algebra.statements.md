# ASN-0053 Claim Statements

*Source: ASN-0053-span-algebra.md (revised 2026-03-19) — Extracted: 2026-05-28*

## Definition — SpanReach

For a span σ = (s, ℓ):

  start(σ) = s,    width(σ) = ℓ,    reach(σ) = s ⊕ ℓ

The reach is the first position beyond σ — the exclusive upper bound.

## Definition — SpanDenotation

  ⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}

## Definition — SpanSetDenotation

A span-set Σ = ⟨σ₁, σ₂, ..., σₙ⟩. Its denotation is the union:

  ⟦Σ⟧ = ⟦σ₁⟧ ∪ ⟦σ₂⟧ ∪ ... ∪ ⟦σₙ⟧

Two span-sets are *equivalent* when they denote the same set of positions: Σ₁ ≡ Σ₂ ⟺ ⟦Σ₁⟧ = ⟦Σ₂⟧. The empty span-set ⟨⟩ denotes ∅. For span-sets Σ₁ = ⟨α₁, ..., αₘ⟩ and Σ₂ = ⟨β₁, ..., βₙ⟩, the *union* Σ₁ ∪ Σ₂ is the concatenated sequence ⟨α₁, ..., αₘ, β₁, ..., βₙ⟩.

## Definition — AdjacentSpans

  adjacent(α, β)  ≡  reach(α) = start(β)  ∨  reach(β) = start(α)

## Definition — InteriorPoint

A position p is *interior* to span σ when start(σ) < p < reach(σ).

## Definition — NormalizedSpanSet

A span-set Σ = ⟨σ₁, ..., σₙ⟩ is normalized iff:

  (N1) *Sorted.*    `(A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))`
  (N2) *Separated.* `(A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))`

## Definition — MutuallyLevelCompatible

A span-set Σ = ⟨σ₁, ..., σₙ⟩ is *mutually level-compatible* when level_compat(start(σᵢ), start(σⱼ)) holds for all 1 ≤ i, j ≤ n. By S6, this is equivalent to: there exists a single length L with #start(σᵢ) = L for every i. When each component σᵢ is also level-uniform, all boundary tumblers of every span — start(σᵢ), width(σᵢ), reach(σᵢ) — share the common length L.

---

## D0 — DisplacementWellDefined

Displacement well-definedness: a < b and divergence(a, b) ≤ #a (DisplacementWellDefined, ASN-0034)

## D1 — DisplacementRoundTrip

For a < b with divergence(a, b) ≤ #a and #a ≤ #b, a ⊕ (b ⊖ a) = b (DisplacementRoundTrip, ASN-0034)

## D2 — DisplacementUnique

Any w with a ⊕ w = b equals b ⊖ a (DisplacementUnique, ASN-0034)

## TA-LC — LeftCancellation

a ⊕ x = a ⊕ y ⟹ x = y (LeftCancellation, ASN-0034)

## TA-assoc — AdditionAssociative

(a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) under ordered action points (AdditionAssociative, ASN-0034)

---

## σ.reach — SpanReachDef

reach(σ) = start(σ) ⊕ width(σ) — the exclusive upper bound

## σ.denotation — SpanDenotationDef

⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}

## Σ.setdenotation — SpanSetDenotationDef

⟦Σ⟧ = union of component span denotations

## N1, N2 — NormalizedFormConditions

  (N1) *Sorted.*    `(A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))`
  (N2) *Separated.* `(A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))`

---

## S6 — LevelConstraint

Two tumblers t₁ and t₂ are *level-compatible*, written level_compat(t₁, t₂), when they have the same length:

  level_compat(t₁, t₂)  ≡  #t₁ = #t₂

A span σ = (s, ℓ) is *level-uniform* when level_compat(s, ℓ), i.e., #s = #ℓ. For a level-uniform span, #reach(σ) = #s by the result-length identity (#(s ⊕ ℓ) = #ℓ), so start, width, and reach all share one tumbler length.

## WF — WellFormedSpanFromEndpoints

For s, r ∈ T with s < r and #s = #r, the pair γ = (s, r ⊖ s) is a well-formed level-uniform span (satisfying T12) with reach(γ) = r.

## WR — WidthRecovery

For a level-uniform span σ = (s, ℓ): reach(σ) ⊖ start(σ) = width(σ).

## S0 — Convexity

`(A p, q, r : p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ p ≤ q ≤ r : q ∈ ⟦σ⟧)`

## SC — SpanClassification

Given spans α and β, their relationship is determined by comparing starts and reaches under T1. Since T1 is a total order, five mutually exclusive cases arise:

(i) *Separated.* reach(α) < start(β) or reach(β) < start(α). The spans share no positions and have space between them.

(ii) *Adjacent.* reach(α) = start(β) or reach(β) = start(α). The spans share no positions but touch at a single boundary point.

(iii) *Proper overlap.* The spans share positions but neither contains the other: start(α) < start(β) < reach(α) < reach(β), or symmetrically.

(iv) *Containment.* One span's denotation is a proper subset of the other's: start(α) ≤ start(β) and reach(β) ≤ reach(α) with at least one inequality strict, or symmetrically.

(v) *Equal.* start(α) = start(β) and reach(α) = reach(β).

Cases (i) and (ii) are the *disjoint* cases — ⟦α⟧ ∩ ⟦β⟧ = ∅. Cases (iii), (iv), and (v) are the *overlapping* cases — ⟦α⟧ ∩ ⟦β⟧ ≠ ∅.

## S1 — IntersectionClosure

For level-uniform spans α and β with level_compat(start(α), start(β)), the intersection is either empty or a single span. No configuration of two such spans produces a fragmented intersection.

Formally: for level-uniform spans α and β with level_compat(start(α), start(β)), either ⟦α⟧ ∩ ⟦β⟧ = ∅, or there exists a span γ such that ⟦γ⟧ = ⟦α⟧ ∩ ⟦β⟧.

## S2 — EmptyDistinction

The empty set of positions is not the denotation of any span. Every well-formed span denotes a non-empty set.

## S3 — MergeEquivalence

For level-uniform spans α and β with level_compat(start(α), start(β)), when they overlap or are adjacent, the union ⟦α⟧ ∪ ⟦β⟧ is the denotation of a single span. Moreover, this merged span is identical to one specified directly with the same endpoints.

Specifically, the merged span γ = (s, r ⊖ s) where s = min(start(α), start(β)) and r = max(reach(α), reach(β)), with ⟦γ⟧ = ⟦α⟧ ∪ ⟦β⟧.

## S3a — MergeCommutativity

The merge of α and β yields the same span as the merge of β and α: ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧.

## S4 — SplitPartition

For a level-uniform span σ = (s, ℓ) and an interior point p with level_compat(s, p), the displacements d = p ⊖ s and d' = reach(σ) ⊖ p are well-defined with #d = #s = #d' (all tumblers at the same length). The left span λ = (s, d) and right span ρ = (p, d') satisfy:

  (a) ⟦λ⟧ ∪ ⟦ρ⟧ = ⟦σ⟧                  (nothing lost)
  (b) ⟦λ⟧ ∩ ⟦ρ⟧ = ∅                      (nothing duplicated)
  (c) reach(λ) = start(ρ) = p             (the parts are adjacent)

## S5 — SplitWidthComposition

Under the same conditions as S4:

  d ⊕ d' = ℓ

## S4a — SplitMergeInverse

For a level-uniform span σ = (s, ℓ) and an interior point p with level_compat(s, p), splitting σ at p (S4) and merging the two parts (S3) recovers σ exactly.

## S3b — MergeSplitInverse

For adjacent level-uniform spans α and β with level_compat(start(α), start(β)), merging α and β (S3) and splitting the result at the shared boundary (S4) recovers the unordered pair {α, β} exactly: the split yields a left part λ and a right part ρ with {λ, ρ} = {α, β}. The assignment of α and β to the left/right positions is determined by the adjacency direction: in Case A (reach(α) = start(β)), λ = α and ρ = β; in Case B (reach(β) = start(α)), λ = β and ρ = α.

## S7 — CoveringExistence

Every finite set of positions P ⊂ T admits a covering span-set Σ with |Σ| = |P| and ⟦Σ⟧ ⊇ P. This is a *covering* claim, not an exact representation: in general no span-set Σ satisfies ⟦Σ⟧ = P for an arbitrary finite P.

Construction: for any tumbler t, define ℓ = [0, ..., 0, 1] with #ℓ = #t. Then (t, ℓ) satisfies T12 and t ∈ ⟦(t, ℓ)⟧. Taking one such span per position in P gives Σ with |Σ| = |P| and ⟦Σ⟧ ⊇ P.

Exact representation fails in general: every span denotes an *infinite* set (by T0(b), proper deeper extensions s.0, s.0.0, … are infinite in number and all lie in ⟦σ⟧), so no non-empty finite P can satisfy ⟦Σ⟧ = P.

## S8 — NormalizationExistence

Every span-set Σ whose component spans are level-uniform and mutually level-compatible has a normalized equivalent Σ̂ with Σ̂ ≡ Σ.

## S9 — NormalizationUniqueness

The normalized form is unique: if Σ̂₁ and Σ̂₂ are both normalized and Σ̂₁ ≡ Σ̂₂, then Σ̂₁ = Σ̂₂.

## S10 — UnionOrderIndependence

For span-sets Σ₁, Σ₂ whose component spans are level-uniform and mutually level-compatible across both sets, the normalized form of their union is independent of the order in which spans are combined:

  normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)                  (commutativity)

For span-sets Σ₁, Σ₂, Σ₃ whose component spans are level-uniform and mutually level-compatible across all three sets:

  normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃))    (associativity)

## S11 — DifferenceBound

For level-uniform spans α and β with level_compat(start(α), start(β)) and ⟦β⟧ ⊆ ⟦α⟧, the set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most two spans.

Specifically, the decomposition is:

  Left:   {t : start(α) ≤ t < start(β)}      (empty when start(α) = start(β))
  Right:  {t : reach(β) ≤ t < reach(α)}       (empty when reach(β) = reach(α))

The result is a span-set of 0, 1, or 2 components:

  (a) Both boundaries coincide (α = β): difference is empty — 0 spans.
  (b) One boundary coincides: difference is one span.
  (c) Neither coincides: difference is two spans.

The bound of two is tight in case (c): no single span γ can satisfy ⟦γ⟧ = ⟦α⟧ \ ⟦β⟧ when neither boundary coincides (by S0 convexity, any such γ would contain a point of ⟦β⟧).

## S11a — DifferenceSeparated (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (i) (separated) or (ii) (adjacent): ⟦α⟧ \ ⟦β⟧ = ⟦α⟧.

## S11b — DifferenceEqual (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (v) (equal): ⟦α⟧ \ ⟦β⟧ = ∅.

## S11c — DifferenceOverlap (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (iii) (proper overlap): ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of exactly 1 span.

Sub-cases:

**Case 1:** start(α) < start(β) < reach(α) < reach(β):
  ⟦α⟧ \ ⟦β⟧ = {t : start(α) ≤ t < start(β)}
  Span: γ = (start(α), start(β) ⊖ start(α)) with reach(γ) = start(β).

**Case 2:** start(β) < start(α) < reach(β) < reach(α):
  ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}
  Span: γ' = (reach(β), reach(α) ⊖ reach(β)) with reach(γ') = reach(α).

## S11d — GeneralDifferenceBound (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)), the set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most 2 spans.

| SC case | Difference | Bound | By |
|---------|-----------|-------|----|
| (i) Separated | ⟦α⟧ | 1 span | S11a |
| (ii) Adjacent | ⟦α⟧ | 1 span | S11a |
| (iii) Proper overlap | 1 span | 1 span | S11c |
| (iv) Containment (⟦β⟧ ⊂ ⟦α⟧) | at most 2 spans | 2 spans | S11 |
| (iv) Containment (⟦α⟧ ⊂ ⟦β⟧) | ∅ | 0 spans | ⟦α⟧ ⊆ ⟦β⟧ |
| (v) Equal | ∅ | 0 spans | S11b |
