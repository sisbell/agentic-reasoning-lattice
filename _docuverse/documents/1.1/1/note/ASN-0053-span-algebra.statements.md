# ASN-0053 Claim Statements

*Source: ASN-0053-span-algebra.md (revised 2026-03-19) — Extracted: 2026-05-13*

## Definition — Reach

  start(σ) = s,    width(σ) = ℓ,    reach(σ) = s ⊕ ℓ

The reach is the first position beyond σ — the exclusive upper bound. It is well-defined by TA0 and satisfies reach(σ) > start(σ) by TA-strict.

## Definition — Adjacent

  adjacent(α, β)  ≡  reach(α) = start(β)  ∨  reach(β) = start(α)

Adjacent spans share no positions (reach is an exclusive upper bound) but their denotations abut — there is no gap between them.

## Definition — InteriorPoint

A position p is *interior* to span σ when start(σ) < p < reach(σ). By the definition of ⟦σ⟧ = {t : start(σ) ≤ t < reach(σ)}, every interior point is in ⟦σ⟧.

## Definition — NormalizedSpanSet

A span-set Σ = ⟨σ₁, ..., σₙ⟩ is normalized iff:

  (N1) *Sorted.* `(A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))`
  (N2) *Separated.* `(A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))`

Condition N2 uses strict inequality. If reach(σᵢ) = start(σᵢ₊₁), the spans are adjacent and could be merged — so the form is not yet minimal. If reach(σᵢ) > start(σᵢ₊₁), the spans overlap and must be merged.

## Definition — MutuallyLevelCompatible

A span-set Σ = ⟨σ₁, ..., σₙ⟩ is *mutually level-compatible* when level_compat(start(σᵢ), start(σⱼ)) holds for all 1 ≤ i, j ≤ n. By S6, this is equivalent to: there exists a single length L with #start(σᵢ) = L for every i. When each component σᵢ is also level-uniform, all four boundary tumblers of every span — start(σᵢ), width(σᵢ), reach(σᵢ) — share the common length L, so any pair of endpoints drawn from any pair of spans satisfies D0 (by the argument given in S6).

## Definition — SpanSet

A *span-set* is a finite sequence of spans Σ = ⟨σ₁, σ₂, ..., σₙ⟩. Two span-sets are *equivalent* when they denote the same set of positions: Σ₁ ≡ Σ₂ ⟺ ⟦Σ₁⟧ = ⟦Σ₂⟧. For span-sets Σ₁ = ⟨α₁, ..., αₘ⟩ and Σ₂ = ⟨β₁, ..., βₙ⟩, the *union* Σ₁ ∪ Σ₂ is the concatenated sequence ⟨α₁, ..., αₘ, β₁, ..., βₙ⟩.

---

## σ.reach — SpanReach

  reach(σ) = start(σ) ⊕ width(σ) — the exclusive upper bound

## σ.denotation — SpanDenotation

  ⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}

## Σ.setdenotation — SpanSetDenotation

  ⟦Σ⟧ = ⟦σ₁⟧ ∪ ⟦σ₂⟧ ∪ ... ∪ ⟦σₙ⟧

By the denotation definition, ⟦Σ₁ ∪ Σ₂⟧ = ⟦Σ₁⟧ ∪ ⟦Σ₂⟧.

## N1, N2 — NormConditions

  (N1) *Sorted.* `(A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))`
  (N2) *Separated.* `(A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))`

---

## D0 — DisplacementWellDefined

Displacement well-definedness: a < b and divergence(a, b) ≤ #a (DisplacementWellDefined, ASN-0034)

D0 ensures the displacement b ⊖ a is a well-defined positive tumbler, and that a ⊕ (b ⊖ a) is defined (TA0 satisfied, since the displacement is positive and its action point k ≤ #a).

## D1 — DisplacementRoundTrip

Displacement round-trip: for a < b with divergence(a, b) ≤ #a and #a ≤ #b, a ⊕ (b ⊖ a) = b (DisplacementRoundTrip, ASN-0034)

## D2 — WidthRecovery

Width recovery: for level-uniform σ, reach(σ) ⊖ start(σ) = width(σ) — follows from DisplacementUnique (D2, ASN-0034)

Preconditions discharged: s < reach(σ) by TA-strict on T12; ℓ > 0 and its action point k ≤ #s by T12; s ⊕ ℓ = reach(σ) by definition of reach; divergence between s and reach(σ) is of type (i) with k ≤ #s, since #s = #reach(σ) excludes the prefix case; #s ≤ #reach(σ) since both equal #s.

## TA-LC — LeftCancellation

  a ⊕ x = a ⊕ y ⟹ x = y (LeftCancellation, ASN-0034)

---

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

## S6 — LevelConstraint

Two tumblers t₁ and t₂ are *level-compatible*, written level_compat(t₁, t₂), when they have the same length:

  level_compat(t₁, t₂)  ≡  #t₁ = #t₂

A span σ = (s, ℓ) is *level-uniform* when level_compat(s, ℓ), i.e., #s = #ℓ. For a level-uniform span, #reach(σ) = #s by the result-length identity from TA0 (#(s ⊕ ℓ) = #ℓ). The start, width, and reach all share the same tumbler length. A level-uniform span automatically satisfies D0 for the (start(σ), reach(σ)) pair: by TA-strict, start(σ) < reach(σ); and since #start(σ) = #reach(σ), neither is a proper prefix of the other, so divergence is of type (i) with k ≤ #start(σ).

## S1 — IntersectionClosure

For level-uniform spans α and β with level_compat(start(α), start(β)), the intersection is either empty or a single span. No configuration of two such spans produces a fragmented intersection.

Formally: for level-uniform spans α and β with level_compat(start(α), start(β)), either ⟦α⟧ ∩ ⟦β⟧ = ∅, or there exists a span γ such that ⟦γ⟧ = ⟦α⟧ ∩ ⟦β⟧.

Construction: Define s' = max(start(α), start(β)) and r' = min(reach(α), reach(β)). If r' ≤ s', the intersection is empty. Otherwise r' > s', and ⟦α⟧ ∩ ⟦β⟧ = {t : s' ≤ t < r'}, representable as γ = (s', r' ⊖ s') with reach(γ) = r'.

## S2 — EmptyDistinction

The empty set of positions is not the denotation of any span. Every well-formed span denotes a non-empty set.

This follows from T12 and TA-strict: ℓ > 0 and k ≤ #s imply s ⊕ ℓ > s, so the half-open interval [s, s ⊕ ℓ) contains at least s itself.

## S3 — MergeEquivalence

For level-uniform spans α and β with level_compat(start(α), start(β)), when they overlap or are adjacent, the union ⟦α⟧ ∪ ⟦β⟧ is the denotation of a single span. Moreover, this merged span is identical to one specified directly with the same endpoints.

Construction (WLOG start(α) ≤ start(β), with overlap-or-adjacency meaning reach(α) ≥ start(β)):

  s = start(α) = min(start(α), start(β))
  r = max(reach(α), reach(β))

Then ⟦α⟧ ∪ ⟦β⟧ = {t : s ≤ t < r}, representable as γ = (s, r ⊖ s) with reach(γ) = r.

## S3a — MergeCommutativity

The merge of α and β yields the same span as the merge of β and α: ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧. This follows from set union being commutative.

## S4 — SplitPartition

For a level-uniform span σ = (s, ℓ) and an interior point p with level_compat(s, p), the displacements d = p ⊖ s and d' = reach(σ) ⊖ p are well-defined with #d = #s = #d' (all tumblers at the same length). The left span λ = (s, d) and right span ρ = (p, d') satisfy:

  (a) ⟦λ⟧ ∪ ⟦ρ⟧ = ⟦σ⟧                  (nothing lost)
  (b) ⟦λ⟧ ∩ ⟦ρ⟧ = ∅                      (nothing duplicated)
  (c) reach(λ) = start(ρ) = p             (the parts are adjacent)

## S5 — SplitWidthComposition

Under the same conditions as S4, the widths of the two parts compose to the original width:

  d ⊕ d' = ℓ

Preconditions for TA-assoc: Pos(d) from T12 on λ; Pos(d') from T12 on ρ; k_d ≤ #s from T12 on λ; k_{d'} ≤ #d from T12 on ρ giving k_{d'} ≤ #p = #s and level-uniformity of λ giving #d = #s.

## S4a — SplitMergeInverse

For a level-uniform span σ = (s, ℓ) and an interior point p with level_compat(s, p), splitting σ at p (S4) and merging the two parts (S3) recovers σ exactly.

The split produces λ = (s, d) with reach(λ) = p, and ρ = (p, d') with reach(ρ) = reach(σ). Since reach(λ) = start(ρ), the two parts are adjacent, and S3 applies. The merge constructs γ = (s_m, r_m ⊖ s_m) where s_m = min(s, p) = s and r_m = max(p, reach(σ)) = reach(σ). The merged width is reach(σ) ⊖ s = ℓ, by D2. So γ = (s, ℓ) = σ.

## S3b — MergeSplitInverse

For adjacent level-uniform spans α and β with level_compat(start(α), start(β)), merging α and β (S3) and splitting the result at the shared boundary (S4) recovers the unordered pair {α, β} exactly: the split yields a left part λ and a right part ρ with {λ, ρ} = {α, β}. The assignment of α and β to the left/right positions is determined by the adjacency direction: in Case A (reach(α) = start(β)), λ = α and ρ = β; in Case B (reach(β) = start(α)), λ = β and ρ = α.

*Case A: reach(α) = start(β).* The merge produces γ = (start(α), reach(β) ⊖ start(α)) with reach(γ) = reach(β). The shared boundary p = start(β) is interior to γ. Splitting γ at p yields λ = (start(α), p ⊖ start(α)) = (start(α), width(α)) = α, and ρ = (p, reach(γ) ⊖ p) = (start(β), width(β)) = β.

*Case B: reach(β) = start(α).* By S3a, merge of α and β equals merge of β and α. Applying Case A to ⟨β, α⟩, splitting at start(α) yields left part λ = β and right part ρ = α.

## S7 — FiniteRepresentability

Every finite set of positions P ⊂ T admits a span-set Σ with |Σ| ≤ |P| and ⟦Σ⟧ ⊇ P.

Construction: For any tumbler t, define ℓ = [0, ..., 0, 1] with #ℓ = #t (all components zero except the last, which is 1). Then ℓ > 0 and the action point k = #t ≤ #t, so (t, ℓ) satisfies T12. By TA-strict, t ⊕ ℓ > t, so t ∈ ⟦(t, ℓ)⟧. Taking one such span per position in P gives Σ with |Σ| = |P| ≤ |P| and ⟦Σ⟧ ⊇ P.

## S8 — NormalizationExistence

Every span-set Σ whose component spans are level-uniform and mutually level-compatible has a normalized equivalent Σ̂ with Σ̂ ≡ Σ.

Construction: If n = 0, the result is ⟨⟩. For n ≥ 1, sort components into non-decreasing order of start. Scan left to right, maintaining current interval [s, r):

  — If start(σᵢ) ≤ r (overlap or adjacency): extend r to max(r, reach(σᵢ)).
  — If start(σᵢ) > r (separated): emit the current interval as span (s, r ⊖ s); start a new current interval at [start(σᵢ), reach(σᵢ)).

After processing all spans, emit the final interval.

*Loop invariant J:* Let E be the set of emitted spans after processing σ₁..σᵢ, and [s, r) the current interval:

  J: ⟦E⟧ ∪ [s, r) = ⟦σ₁⟧ ∪ ... ∪ ⟦σᵢ⟧

The result satisfies N1 (starts sorted from left-to-right emission) and N2 (each emit occurs precisely when start(σᵢ) > r). Termination bound: t = n − i.

## S9 — NormalizationUniqueness

The normalized form is unique: if Σ̂₁ and Σ̂₂ are both normalized and Σ̂₁ ≡ Σ̂₂, then Σ̂₁ = Σ̂₂.

Let Σ̂₁ = ⟨α₁, ..., αₘ⟩ and Σ̂₂ = ⟨β₁, ..., βₙ⟩, both normalized, with ⟦Σ̂₁⟧ = ⟦Σ̂₂⟧ = S. If Σ̂₁ ≠ Σ̂₂, let i be the smallest index where αᵢ ≠ βᵢ. The following cases all yield contradiction:

*Case 1a:* Both αᵢ, βᵢ exist with start(αᵢ) < start(βᵢ). Then start(αᵢ) ∈ S but start(αᵢ) ∉ ⟦βⱼ⟧ for any j — for j < i, reach(βⱼ) < start(αᵢ) by N2/N1; for j ≥ i, start(βⱼ) > start(αᵢ). Contradiction.

*Case 1b:* αᵢ exists, βᵢ does not (n = i − 1). Then start(αᵢ) ∈ S but ∉ ⟦Σ̂₂⟧. Contradiction.

*Case 2a:* start(αᵢ) = start(βᵢ) and reach(αᵢ) < reach(βᵢ). Set p = reach(αᵢ). Then p ∈ ⟦βᵢ⟧ ⊆ S but p ∉ ⟦αⱼ⟧ for any j — p is the exclusive upper bound of αᵢ, above reach(αⱼ) for j < i by N2/N1, below start(αⱼ) for j > i by N2/N1. So p ∉ ⟦Σ̂₁⟧. Contradiction.

*Case 2b:* reach(αᵢ) > reach(βᵢ). Symmetric to Case 2a with roles of Σ̂₁ and Σ̂₂ exchanged.

*Cases 3a, 3b:* start(αᵢ) > start(βᵢ) or βᵢ exists, αᵢ does not. Symmetric to Cases 1a, 1b.

## S10 — UnionOrderIndependence

For span-sets Σ₁, Σ₂ whose component spans are level-uniform and mutually level-compatible across both sets, the normalized form of their union is independent of the order in which spans are combined:

  normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)                  (commutativity)

For span-sets Σ₁, Σ₂, Σ₃ whose component spans are level-uniform and mutually level-compatible across all three sets:

  normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃))    (associativity)

## S11 — DifferenceBound

For level-uniform spans α and β with level_compat(start(α), start(β)) and ⟦β⟧ ⊆ ⟦α⟧, the set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most two spans.

Containment means start(α) ≤ start(β) and reach(β) ≤ reach(α). The difference decomposes as:

  Left:   {t : start(α) ≤ t < start(β)}      (empty when start(α) = start(β))
  Right:  {t : reach(β) ≤ t < reach(α)}       (empty when reach(β) = reach(α))

Constructed spans: λ = (start(α), start(β) ⊖ start(α)) when start(α) < start(β); ρ = (reach(β), reach(α) ⊖ reach(β)) when reach(β) < reach(α).

The bound of two is tight: when neither boundary coincides, start(α) < start(β) and reach(β) < reach(α). Suppose γ satisfies ⟦γ⟧ = ⟦λ⟧ ∪ ⟦ρ⟧. Pick any t ∈ ⟦β⟧ (non-empty by S2). Then start(α) ∈ ⟦λ⟧ ⊆ ⟦γ⟧ and reach(β) ∈ ⟦ρ⟧ ⊆ ⟦γ⟧, and start(α) < t < reach(β) places t between two members of ⟦γ⟧. By S0, t ∈ ⟦γ⟧ = ⟦λ⟧ ∪ ⟦ρ⟧. But t ∉ ⟦λ⟧ (t ≥ start(β) = reach(λ)) and t ∉ ⟦ρ⟧ (t < reach(β) = start(ρ)) — contradiction.

## S11a — DifferenceSeparated (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (i) (separated) or (ii) (adjacent): ⟦α⟧ \ ⟦β⟧ = ⟦α⟧.

In both cases ⟦α⟧ ∩ ⟦β⟧ = ∅ (SC classifies (i) and (ii) as the disjoint cases). When the intersection is empty, removing β's positions from α removes nothing: ⟦α⟧ \ ⟦β⟧ = ⟦α⟧. The result is a span-set of exactly 1 span.

## S11b — DifferenceEqual (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (v) (equal): ⟦α⟧ \ ⟦β⟧ = ∅.

Equal spans have start(α) = start(β) and reach(α) = reach(β), so ⟦α⟧ = ⟦β⟧. The set difference of a set with itself is empty: ⟦α⟧ \ ⟦β⟧ = ∅. The result is a span-set of 0 spans.

## S11c — DifferenceOverlap (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (iii) (proper overlap): ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of exactly 1 span.

*Case 1: start(α) < start(β) < reach(α) < reach(β).*

  ⟦α⟧ \ ⟦β⟧ = {t : start(α) ≤ t < start(β)}

Constructed as γ = (start(α), start(β) ⊖ start(α)) with reach(γ) = start(β) (by D1). The span is level-uniform: #width(γ) = max(#start(β), #start(α)) = #start(α) = #start(γ).

*Case 2: start(β) < start(α) < reach(β) < reach(α).*

  ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}

Constructed as γ' = (reach(β), reach(α) ⊖ reach(β)) with reach(γ') = reach(α) (by D1). Level-uniformity: #reach(β) = #start(β) and #reach(α) = #start(α) and level_compat(start(α), start(β)) give #reach(β) = #reach(α) = #start(γ'). #width(γ') = max(#reach(α), #reach(β)) = #reach(β) = #start(γ').

## S11d — GeneralDifferenceBound (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)), the set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most 2 spans.

For the reverse containment sub-case of SC(iv) — start(β) ≤ start(α) and reach(α) ≤ reach(β) with at least one strict — ⟦α⟧ ⊆ ⟦β⟧, so the difference is empty.

| SC case | Difference | Bound | By |
|---------|-----------|-------|----|
| (i) Separated | ⟦α⟧ | 1 span | S11a |
| (ii) Adjacent | ⟦α⟧ | 1 span | S11a |
| (iii) Proper overlap | 1 span | 1 span | S11c |
| (iv) Containment (⟦β⟧ ⊂ ⟦α⟧) | at most 2 spans | 2 spans | S11 |
| (iv) Containment (⟦α⟧ ⊂ ⟦β⟧) | ∅ | 0 spans | ⟦α⟧ ⊆ ⟦β⟧ |
| (v) Equal | ∅ | 0 spans | S11b |

The maximum across all cases is 2, achieved only in the containment case.
