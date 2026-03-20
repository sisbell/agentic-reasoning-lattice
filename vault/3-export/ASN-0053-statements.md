# ASN-0053 Formal Statements

*Source: ASN-0053-span-algebra.md (revised 2026-03-18) — Extracted: 2026-03-19*

## Definition — SpanProjections

For a span σ = (s, ℓ):

  start(σ) = s,    width(σ) = ℓ

## σ.reach — SpanReach (DEF, function)

  reach(σ) = start(σ) ⊕ width(σ)

The reach is the first position beyond σ — the exclusive upper bound. It is well-defined by TA0 and satisfies reach(σ) > start(σ) by TA-strict.

## σ.denotation — SpanDenotation (DEF, function)

  ⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}

## Σ.setdenotation — SpanSetDenotation (DEF, function)

For a span-set Σ = ⟨σ₁, σ₂, ..., σₙ⟩:

  ⟦Σ⟧ = ⟦σ₁⟧ ∪ ⟦σ₂⟧ ∪ ... ∪ ⟦σₙ⟧

The empty span-set ⟨⟩ denotes ∅. The singleton span-set ⟨σ⟩ denotes ⟦σ⟧.

## Definition — SpanSetEquivalence

Two span-sets are equivalent when they denote the same set of positions:

  Σ₁ ≡ Σ₂  ⟺  ⟦Σ₁⟧ = ⟦Σ₂⟧

## Definition — Adjacent

  adjacent(α, β)  ≡  reach(α) = start(β)  ∨  reach(β) = start(α)

Adjacent spans share no positions (reach is an exclusive upper bound) but their denotations abut — there is no gap between them.

## Definition — InteriorPoint

A position p is interior to span σ when:

  start(σ) < p < reach(σ)

## N1, N2 — IsNormalized (PRED, predicate)

A span-set Σ = ⟨σ₁, ..., σₙ⟩ is normalized iff:

  (N1) Sorted:    (A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))
  (N2) Separated: (A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))

---

## D0 — DisplacementWellDefined (LEMMA, cited from ASN-0034)

For tumblers a, b ∈ T with a < b and divergence(a, b) ≤ #a: the displacement b ⊖ a is a well-defined positive tumbler, and a ⊕ (b ⊖ a) is defined (TA0 satisfied, since the displacement is positive and its action point k ≤ #a).

## D1 — DisplacementRoundTrip (LEMMA, cited from ASN-0034)

For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:

  a ⊕ (b ⊖ a) = b

## D2 — WidthRecovery (LEMMA, cited from ASN-0034)

For a level-uniform span σ with #start(σ) = #reach(σ):

  reach(σ) ⊖ start(σ) = width(σ)

Follows from DisplacementUnique (D2, ASN-0034).

## TA-LC — LeftCancellation (LEMMA, cited from ASN-0055)

  a ⊕ x = a ⊕ y  ⟹  x = y

---

## S6 — LevelConstraint (PRED, predicate)

  level_compat(t₁, t₂)  ≡  #t₁ = #t₂

A span σ = (s, ℓ) is level-uniform when level_compat(s, ℓ), i.e., #s = #ℓ.

For a level-uniform span, #reach(σ) = #s: since the action point k satisfies 1 ≤ k ≤ #s = #ℓ, we have #(s ⊕ ℓ) = max(k − 1, 0) + (#ℓ − k + 1) = #ℓ = #s. The start, width, and reach all share the same tumbler length.

Level-uniform spans automatically satisfy D0 for all endpoint pairs: since #start = #reach, neither is a proper prefix of the other, so divergence is of type (i) with k ≤ #start.

## S0 — Convexity (LEMMA, lemma)

  (A p, q, r : p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ p ≤ q ≤ r : q ∈ ⟦σ⟧)

## SC — SpanClassification (LEMMA, lemma)

Given spans α and β, five mutually exclusive cases arise:

  (i)   Separated:      reach(α) < start(β)  ∨  reach(β) < start(α)
  (ii)  Adjacent:       reach(α) = start(β)  ∨  reach(β) = start(α)
  (iii) Proper overlap: start(α) < start(β) < reach(α) < reach(β),  or symmetrically
  (iv)  Containment:    start(α) ≤ start(β) ∧ reach(β) ≤ reach(α) with at least one inequality strict,  or symmetrically
  (v)   Equal:          start(α) = start(β) ∧ reach(α) = reach(β)

Cases (i) and (ii) are the disjoint cases: ⟦α⟧ ∩ ⟦β⟧ = ∅.
Cases (iii), (iv), and (v) are the overlapping cases: ⟦α⟧ ∩ ⟦β⟧ ≠ ∅.

## S1 — IntersectionClosure (LEMMA, lemma)

Preconditions: α and β are level-uniform spans; level_compat(start(α), start(β)).

Either ⟦α⟧ ∩ ⟦β⟧ = ∅, or there exists a span γ such that ⟦γ⟧ = ⟦α⟧ ∩ ⟦β⟧.

Witness construction: let s' = max(start(α), start(β)) and r' = min(reach(α), reach(β)).
- If r' ≤ s': intersection is empty.
- If r' > s': γ = (s', r' ⊖ s') with reach(γ) = s' ⊕ (r' ⊖ s') = r', and ⟦γ⟧ = {t : s' ≤ t < r'} = ⟦α⟧ ∩ ⟦β⟧. γ is level-uniform: #width(γ) = #(r' ⊖ s') = max(#r', #s') = #s' = #start(γ).

## S2 — EmptyDistinction (LEMMA, lemma)

The empty set of positions is not the denotation of any span. Every well-formed span denotes a non-empty set.

Follows from T12 and TA-strict: ℓ > 0 and k ≤ #s imply s ⊕ ℓ > s, so the half-open interval [s, s ⊕ ℓ) contains at least s itself.

## S3 — MergeEquivalence (LEMMA, lemma)

Preconditions: α and β are level-uniform spans; level_compat(start(α), start(β)); they overlap or are adjacent (reach(α) ≥ start(β), assuming start(α) ≤ start(β)).

The union ⟦α⟧ ∪ ⟦β⟧ is the denotation of a single span. Moreover, this merged span is identical to one specified directly with the same endpoints.

Witness construction (assuming start(α) ≤ start(β)):

  s = start(α)
  r = max(reach(α), reach(β))
  γ = (s, r ⊖ s)   with reach(γ) = r   and   ⟦γ⟧ = ⟦α⟧ ∪ ⟦β⟧

γ is level-uniform: #start(γ) = #s = max(#r, #s) = #(r ⊖ s) = #width(γ), since #s = #r by level-compatibility.

## S3a — MergeCommutativity (LEMMA, lemma)

  ⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧

The merge of α and β yields the same span as the merge of β and α.

## S4 — SplitPartition (LEMMA, lemma)

Preconditions: σ = (s, ℓ) is a level-uniform span; p is interior to σ (start(σ) < p < reach(σ)); level_compat(s, p).

Let d = p ⊖ s and d' = reach(σ) ⊖ p, with #d = #s = #d'. Let λ = (s, d) and ρ = (p, d'). Then:

  (a) ⟦λ⟧ ∪ ⟦ρ⟧ = ⟦σ⟧                  (nothing lost)
  (b) ⟦λ⟧ ∩ ⟦ρ⟧ = ∅                      (nothing duplicated)
  (c) reach(λ) = start(ρ) = p             (the parts are adjacent)

Both λ and ρ are level-uniform: #start(λ) = #s = #d = #width(λ); #start(ρ) = #p = #s = #d' = #width(ρ).

## S5 — SplitWidthComposition (LEMMA, lemma)

Preconditions: same as S4 (σ = (s, ℓ) level-uniform; p interior to σ; level_compat(s, p); d = p ⊖ s; d' = reach(σ) ⊖ p).

  d ⊕ d' = ℓ

## S4a — SplitMergeInverse (LEMMA, lemma)

Preconditions: σ = (s, ℓ) is a level-uniform span; p is interior to σ; level_compat(s, p).

Splitting σ at p by S4 yields λ = (s, d) with reach(λ) = p, and ρ = (p, d') with reach(ρ) = reach(σ). Since reach(λ) = start(ρ), S3 applies. The merged span is γ = (s_m, r_m ⊖ s_m) where s_m = min(s, p) = s and r_m = max(p, reach(σ)) = reach(σ). The merged width is reach(σ) ⊖ s = ℓ by D2. Therefore:

  merge(split(σ, p)) = (s, ℓ) = σ

## S3b — MergeSplitInverse (LEMMA, lemma)

Preconditions: α and β are adjacent level-uniform spans with reach(α) = start(β); level_compat(start(α), start(β)).

Merging α and β by S3 yields γ = (start(α), reach(β) ⊖ start(α)) with reach(γ) = reach(β). The point p = start(β) is interior to γ: start(α) < start(β) (since α is non-empty) and start(β) < reach(β) = reach(γ) (since β is non-empty). Splitting γ at p by S4 yields λ and ρ where:

  λ = (start(α), p ⊖ start(α)) = (start(α), reach(α) ⊖ start(α)) = (start(α), width(α)) = α
  ρ = (p, reach(γ) ⊖ p) = (start(β), reach(β) ⊖ start(β)) = (start(β), width(β)) = β

Therefore:

  split(merge(α, β), start(β)) = (α, β)

## S7 — FiniteRepresentability (LEMMA, lemma)

Every finite set of positions P ⊂ T admits a span-set Σ with ⟦Σ⟧ ⊇ P.

Witness construction: for each t ∈ P, define ℓ = [0, ..., 0, 1] with #ℓ = #t (all components zero except the last, which is 1). Then ℓ > 0 (last component nonzero) and action point k = #t ≤ #t, so (t, ℓ) satisfies T12. By TA-strict, t ⊕ ℓ > t, so t ∈ ⟦(t, ℓ)⟧. Taking one such span per position in P gives Σ with ⟦Σ⟧ ⊇ P.

## S8 — NormalizationExistence (LEMMA, lemma)

Precondition: Σ is a span-set whose component spans are level-uniform and mutually level-compatible.

There exists a normalized span-set Σ̂ such that Σ̂ ≡ Σ.

Construction: sort component spans by start position. Scan left to right, maintaining a current interval [s, r):
- If start(σᵢ) ≤ r (overlap or adjacency): extend r ← max(r, reach(σᵢ)).
- If start(σᵢ) > r (separated): emit span (s, r ⊖ s); begin new interval [start(σᵢ), reach(σᵢ)).

After all spans, emit the final interval.

Loop invariant J: let E be the set of emitted spans after processing σ₁..σᵢ and [s, r) the current interval:

  J: ⟦E⟧ ∪ [s, r) = ⟦σ₁⟧ ∪ ... ∪ ⟦σᵢ⟧

Termination bound: n − i (each iteration advances i by 1).

The result satisfies N1 (starts sorted, emitting left-to-right from sorted input) and N2 (each emit occurs precisely when start(σᵢ) > r, guaranteeing reach of emitted span < start of next span).

## S9 — NormalizationUniqueness (LEMMA, lemma)

If Σ̂₁ and Σ̂₂ are both normalized and Σ̂₁ ≡ Σ̂₂, then Σ̂₁ = Σ̂₂.

Let Σ̂₁ = ⟨α₁, ..., αₘ⟩ and Σ̂₂ = ⟨β₁, ..., βₙ⟩, both normalized, with ⟦Σ̂₁⟧ = ⟦Σ̂₂⟧ = S. Suppose Σ̂₁ ≠ Σ̂₂. Let i be the smallest index where αᵢ ≠ βᵢ.

- Case 1: start(αᵢ) < start(βᵢ). Then start(αᵢ) ∈ ⟦αᵢ⟧ ⊆ S, but start(αᵢ) ∉ ⟦βⱼ⟧ for any j (for j < i by N2 on Σ̂₁; for j ≥ i by N1 on Σ̂₂), so start(αᵢ) ∉ ⟦Σ̂₂⟧ = S. Contradiction.
- Case 2: start(αᵢ) = start(βᵢ) but reach(αᵢ) < reach(βᵢ). Set p = reach(αᵢ). Then p ∈ ⟦βᵢ⟧ ⊆ S, but p ∉ ⟦αⱼ⟧ for any j, so p ∉ ⟦Σ̂₁⟧ = S. Contradiction.
- Case 3: start(αᵢ) > start(βᵢ). Symmetric to Case 1.

## S10 — UnionOrderIndependence (LEMMA, lemma)

Precondition: component spans of all operands are level-uniform and mutually level-compatible across operands.

Commutativity:

  normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)

Associativity:

  normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃))

## S11 — DifferenceBound (LEMMA, lemma)

Preconditions: α and β are level-uniform spans; level_compat(start(α), start(β)); ⟦β⟧ ⊆ ⟦α⟧, i.e., start(α) ≤ start(β) and reach(β) ≤ reach(α).

The set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most two spans.

Construction:
- Left interval: when start(α) < start(β), define λ = (start(α), start(β) ⊖ start(α)) with reach(λ) = start(β).
- Right interval: when reach(β) < reach(α), define ρ = (reach(β), reach(α) ⊖ reach(β)) with reach(ρ) = reach(α).

Cases:
  (a) start(α) = start(β) and reach(β) = reach(α): difference is empty — 0 spans.
  (b) Exactly one boundary coincides: difference is 1 span.
  (c) Neither coincides: difference is 2 spans.
