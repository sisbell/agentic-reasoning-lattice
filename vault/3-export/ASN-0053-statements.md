# ASN-0053 Formal Statements

*Source: ASN-0053-span-algebra.md (revised 2026-03-18) — Extracted: 2026-03-19*

## Definition — Reach

```
For a span σ = (s, ℓ):
  start(σ) = s,    width(σ) = ℓ,    reach(σ) = s ⊕ ℓ
```

The reach is the first position beyond σ — the exclusive upper bound. It satisfies reach(σ) > start(σ) by TA-strict.

## Definition — SpanDenotation

```
⟦σ⟧ = {t ∈ T : start(σ) ≤ t < start(σ) ⊕ width(σ)}
     = {t ∈ T : start(σ) ≤ t < reach(σ)}
```

## Definition — LevelCompat

```
level_compat(t₁, t₂)  ≡  #t₁ = #t₂
```

A span σ = (s, ℓ) is *level-uniform* when level_compat(s, ℓ), i.e., #s = #ℓ.

For a level-uniform span: #reach(σ) = #s, since the action point k satisfies 1 ≤ k ≤ #s = #ℓ, giving #(s ⊕ ℓ) = max(k − 1, 0) + (#ℓ − k + 1) = #ℓ = #s.

## Definition — Adjacent

```
adjacent(α, β)  ≡  reach(α) = start(β)  ∨  reach(β) = start(α)
```

Adjacent spans share no positions (reach is an exclusive upper bound) but their denotations abut — there is no gap between them.

## Definition — InteriorPoint

```
A position p is *interior* to span σ when start(σ) < p < reach(σ).
```

## Definition — SpanSetDenotation

```
A *span-set* is a finite sequence of spans Σ = ⟨σ₁, σ₂, ..., σₙ⟩.

⟦Σ⟧ = ⟦σ₁⟧ ∪ ⟦σ₂⟧ ∪ ... ∪ ⟦σₙ⟧

Two span-sets are *equivalent* when: Σ₁ ≡ Σ₂ ⟺ ⟦Σ₁⟧ = ⟦Σ₂⟧
The empty span-set ⟨⟩ denotes ∅.
```

## Definition — NormalizedSpanSet

```
A span-set Σ = ⟨σ₁, ..., σₙ⟩ is normalized iff:

  (N1) Sorted:    (A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))
  (N2) Separated: (A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))
```

N2 uses strict inequality: reach(σᵢ) = start(σᵢ₊₁) means adjacent (mergeable); reach(σᵢ) > start(σᵢ₊₁) means overlapping (must merge).

---

## σ.reach — Reach (DEF, function)

```
reach(σ) = start(σ) ⊕ width(σ)
```

The exclusive upper bound of span σ.

## σ.denotation — SpanDenotation (DEF, function)

```
⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}
```

## Σ.setdenotation — SpanSetDenotation (DEF, function)

```
⟦Σ⟧ = union of component span denotations
     = ⟦σ₁⟧ ∪ ⟦σ₂⟧ ∪ ... ∪ ⟦σₙ⟧  for Σ = ⟨σ₁, ..., σₙ⟩
```

## N1, N2 — NormalizedConditions (DEF, predicate)

```
(N1) (A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))
(N2) (A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))
```

---

## D0 — DisplacementWellDefined (PRE, requires)

```
Precondition for displacement b ⊖ a to be a well-defined positive tumbler
with TA0 satisfied:

  a < b, and divergence(a, b) ≤ #a

where divergence(a, b) is the smallest index k at which a and b differ.
```

D0 ensures b ⊖ a is positive and its action point k ≤ #a (so a ⊕ (b ⊖ a) is defined). It does not guarantee round-trip faithfulness; that additionally requires #a = #b.

## D1 — DisplacementRoundTrip (LEMMA, lemma)

```
For tumblers a, b ∈ T with a < b and #a = #b:

  a ⊕ (b ⊖ a) = b
```

Proof sketch: Let k = divergence(a, b). Since #a = #b, type (i) divergence gives k ≤ #a and aₖ < bₖ. Define w = b ⊖ a: wᵢ = 0 for i < k, wₖ = bₖ − aₖ, wᵢ = bᵢ for i > k. Then w > 0 with action point k ≤ #a (TA0 satisfied). Applying TumblerAdd: (a ⊕ w)ᵢ = aᵢ = bᵢ for i < k, (a ⊕ w)ₖ = aₖ + (bₖ − aₖ) = bₖ, (a ⊕ w)ᵢ = wᵢ = bᵢ for i > k. Every component matches.

## D2 — WidthRecovery (LEMMA, lemma)

```
For a level-uniform span σ = (s, ℓ) (i.e., #s = #ℓ):

  reach(σ) ⊖ start(σ) = width(σ)
```

Proof sketch: Both start and reach have length #s. Divergence is at position k (the action point of ℓ). Then (reach ⊖ start)ₖ = (sₖ + ℓₖ) − sₖ = ℓₖ, (reach ⊖ start)ᵢ = (s ⊕ ℓ)ᵢ = ℓᵢ for i > k, zero for i < k. Result has length max(#reach, #start) = #s = #ℓ. This is ℓ.

---

## S0 — Convexity (LEMMA, lemma)

```
(A p, q, r : p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ p ≤ q ≤ r : q ∈ ⟦σ⟧)
```

Equivalently: if start(σ) ≤ p ≤ q ≤ r < reach(σ), then start(σ) ≤ q < reach(σ), so q ∈ ⟦σ⟧.

## SC — SpanClassification (LEMMA, lemma)

```
Given spans α and β, exactly one of five mutually exclusive cases holds:

(i)   Separated:      reach(α) < start(β)  ∨  reach(β) < start(α)
                      ⟦α⟧ ∩ ⟦β⟧ = ∅, gap between them

(ii)  Adjacent:       reach(α) = start(β)  ∨  reach(β) = start(α)
                      ⟦α⟧ ∩ ⟦β⟧ = ∅, touch at boundary

(iii) Proper overlap: start(α) < start(β) < reach(α) < reach(β)
                      (or symmetrically)
                      ⟦α⟧ ∩ ⟦β⟧ ≠ ∅, neither contains the other

(iv)  Containment:    start(α) ≤ start(β) ∧ reach(β) ≤ reach(α) with at
                      least one inequality strict (or symmetrically)
                      ⟦α⟧ ∩ ⟦β⟧ ≠ ∅

(v)   Equal:          start(α) = start(β) ∧ reach(α) = reach(β)

Cases (i) and (ii) are the disjoint cases: ⟦α⟧ ∩ ⟦β⟧ = ∅.
Cases (iii), (iv), (v) are the overlapping cases: ⟦α⟧ ∩ ⟦β⟧ ≠ ∅.
```

## S6 — LevelConstraint (DEF, predicate)

```
level_compat(t₁, t₂)  ≡  #t₁ = #t₂

A span σ = (s, ℓ) is level-uniform when level_compat(s, ℓ), i.e., #s = #ℓ.

For a level-uniform span: #reach(σ) = #s.

Level-uniform spans automatically satisfy D0 for all endpoint pairs: since
#start = #reach, neither is a proper prefix of the other, so divergence is
of type (i) with k ≤ #start.
```

## S1 — IntersectionClosure (LEMMA, lemma)

```
Preconditions: α and β are level-uniform; level_compat(start(α), start(β)).

Either ⟦α⟧ ∩ ⟦β⟧ = ∅, or there exists a span γ such that ⟦γ⟧ = ⟦α⟧ ∩ ⟦β⟧.

Construction of γ when non-empty:
  s' = max(start(α), start(β))
  r' = min(reach(α), reach(β))
  If r' ≤ s': intersection is empty.
  Otherwise: γ = (s', r' ⊖ s') with reach(γ) = r'.

γ is level-uniform: #width(γ) = #(r' ⊖ s') = max(#r', #s') = #s' = #start(γ).
```

## S2 — EmptyDistinction (LEMMA, lemma)

```
The empty set of positions is not the denotation of any span.
Every well-formed span denotes a non-empty set.

Formally: ¬∃σ . ⟦σ⟧ = ∅

Follows from T12 (ℓ > 0 and action point k ≤ #s) and TA-strict (s ⊕ ℓ > s),
so the half-open interval [s, s ⊕ ℓ) contains at least s itself.
```

## S3 — MergeEquivalence (LEMMA, lemma)

```
Preconditions: α and β are level-uniform; level_compat(start(α), start(β));
               ⟦α⟧ ∩ ⟦β⟧ ≠ ∅ or adjacent(α, β)
               (i.e., reach(α) ≥ start(β) assuming start(α) ≤ start(β)).

There exists a single span γ such that ⟦γ⟧ = ⟦α⟧ ∪ ⟦β⟧.

Construction (assuming start(α) ≤ start(β)):
  s = start(α)
  r = max(reach(α), reach(β))
  γ = (s, r ⊖ s),  with reach(γ) = r

γ is level-uniform: #start(γ) = #s = #(r ⊖ s) = #width(γ).
```

## S3a — MergeCommutativity (LEMMA, lemma)

```
⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧

The merge of α and β yields the same span as the merge of β and α.
Follows from set union being commutative.
```

## S4 — SplitPartition (LEMMA, lemma)

```
Preconditions: σ = (s, ℓ) is level-uniform; p is interior to σ (start(σ) < p < reach(σ));
               level_compat(s, p).

Define:
  d  = p ⊖ s             (left width)
  d' = reach(σ) ⊖ p      (right width)
  λ  = (s, d)            (left span)
  ρ  = (p, d')           (right span)

Then #d = #s = #d' (all tumblers at the same length), and:

  (a) ⟦λ⟧ ∪ ⟦ρ⟧ = ⟦σ⟧        (nothing lost)
  (b) ⟦λ⟧ ∩ ⟦ρ⟧ = ∅          (nothing duplicated)
  (c) reach(λ) = start(ρ) = p  (the parts are adjacent)

Both λ and ρ are well-formed and level-uniform.
```

## TA-LC — LeftCancellation (LEMMA, cited from ASN-0055)

```
a ⊕ x = a ⊕ y  ⟹  x = y

(where both sides are well-defined)
```

## S5 — SplitWidthComposition (LEMMA, lemma)

```
Under the same preconditions as S4 (σ = (s, ℓ) level-uniform, p interior,
level_compat(s, p)), with d = p ⊖ s and d' = reach(σ) ⊖ p:

  d ⊕ d' = ℓ

Proof sketch: By D1, s ⊕ d = p and p ⊕ d' = reach(σ). Chaining:
  (s ⊕ d) ⊕ d' = reach(σ) = s ⊕ ℓ
By associativity (both sides well-defined under level-uniformity):
  s ⊕ (d ⊕ d') = s ⊕ ℓ
By TA-LC (left cancellation): d ⊕ d' = ℓ.
```

## S4a — SplitMergeInverse (LEMMA, lemma)

```
Preconditions: σ = (s, ℓ) level-uniform; p interior to σ; level_compat(s, p).

Splitting σ at p (S4) and merging the two parts (S3) recovers σ exactly:

  merge(split(σ, p)) = σ

The split produces λ = (s, d) with reach(λ) = p, and ρ = (p, d') with
reach(ρ) = reach(σ). Since reach(λ) = start(ρ), S3 applies.
The merge constructs γ = (s_m, r_m ⊖ s_m) where:
  s_m = min(s, p) = s   (since s < p)
  r_m = max(p, reach(σ)) = reach(σ)   (since p < reach(σ))
  width = reach(σ) ⊖ s = ℓ   (by D2, since #s = #reach(σ))
So γ = (s, ℓ) = σ.
```

## S3b — MergeSplitInverse (LEMMA, lemma)

```
Preconditions: α and β are level-uniform; adjacent with reach(α) = start(β);
               level_compat(start(α), start(β)).

Merging α and β (S3) and splitting the result at start(β) (S4) recovers
α and β exactly:

  split(merge(α, β), start(β)) = (α, β)

The merge produces γ = (start(α), reach(β) ⊖ start(α)) with reach(γ) = reach(β).
p = start(β) is interior to γ:
  start(α) < start(β)   (since α non-empty: start(α) < reach(α) = start(β))
  start(β) < reach(β) = reach(γ)  (since β non-empty)

Splitting γ at p yields:
  λ = (start(α), p ⊖ start(α)) = (start(α), width(α)) = α   (by D2)
  ρ = (p, reach(γ) ⊖ p) = (start(β), width(β)) = β           (by D2)
```

## S7 — FiniteRepresentability (LEMMA, lemma)

```
Every finite set of positions P ⊂ T admits a span-set Σ with ⟦Σ⟧ ⊇ P.

Construction: For any tumbler t, define ℓ = [0, ..., 0, 1] with #ℓ = #t
(all components zero except the last, which is 1). Then:
  ℓ > 0 (last component nonzero)
  action point k = #t ≤ #t  (T12 satisfied)
  t ⊕ ℓ > t  (TA-strict)
  t ∈ [t, t ⊕ ℓ) = ⟦(t, ℓ)⟧

Taking one such singleton span per position in P gives Σ with ⟦Σ⟧ ⊇ P.
```

## S8 — NormalizationExistence (LEMMA, lemma)

```
Preconditions: Σ is a span-set whose component spans are level-uniform and
               mutually level-compatible.

There exists a normalized span-set Σ̂ such that Σ̂ ≡ Σ  (i.e., ⟦Σ̂⟧ = ⟦Σ⟧).

Construction (sweep algorithm):
  If n = 0: result is ⟨⟩.
  For n ≥ 1:
    1. Sort component spans by start position (T1 makes this well-defined).
    2. Scan left to right, maintaining current interval [s, r):
       — If start(σᵢ) ≤ r (overlap or adjacency): r ← max(r, reach(σᵢ))
       — If start(σᵢ) > r (separated): emit span (s, r ⊖ s); start new interval
         at [start(σᵢ), reach(σᵢ))
    3. After all spans: emit final interval as a span.

Loop invariant J after processing σ₁..σᵢ (E = emitted spans, [s, r) = current):
  ⟦E⟧ ∪ [s, r) = ⟦σ₁⟧ ∪ ... ∪ ⟦σᵢ⟧

Result satisfies N1 (starts sorted, emitting left-to-right from sorted input)
and N2 (each emit occurs when start(σᵢ) > r, guaranteeing reach(emitted) < start(next)).
Termination: bound function t = n − i (each span visited exactly once).
```

## S9 — NormalizationUniqueness (LEMMA, lemma)

```
If Σ̂₁ and Σ̂₂ are both normalized and Σ̂₁ ≡ Σ̂₂, then Σ̂₁ = Σ̂₂.

Proof by contradiction: Let i be the smallest index where αᵢ ≠ βᵢ.

Case 1: start(αᵢ) < start(βᵢ) (or βᵢ does not exist).
  start(αᵢ) ∈ S (since start(αᵢ) ∈ ⟦αᵢ⟧).
  start(αᵢ) ∉ ⟦βⱼ⟧ for j < i: reach(βⱼ) = reach(αⱼ) < start(αᵢ) by N2 on Σ̂₁.
  start(αᵢ) ∉ ⟦βⱼ⟧ for j ≥ i: start(βⱼ) ≥ start(βᵢ) > start(αᵢ) by N1 on Σ̂₂.
  So start(αᵢ) ∉ ⟦Σ̂₂⟧ = S. Contradiction.

Case 2: start(αᵢ) = start(βᵢ) but reach(αᵢ) < reach(βᵢ).
  Set p = reach(αᵢ).
  p ∈ ⟦βᵢ⟧: start(βᵢ) = start(αᵢ) < p < reach(βᵢ). So p ∈ S.
  p ∉ ⟦αᵢ⟧: p = reach(αᵢ) is the exclusive upper bound.
  p ∉ ⟦αⱼ⟧ for j < i: p > reach(αⱼ) by N2 and N1 applied to Σ̂₁.
  p ∉ ⟦αⱼ⟧ for j > i: p < start(αᵢ₊₁) ≤ start(αⱼ) by N2 and N1.
  So p ∉ ⟦Σ̂₁⟧, but p ∈ S. Contradiction.

Case 3: start(αᵢ) > start(βᵢ). Symmetric to Case 1.
```

## S10 — UnionOrderIndependence (LEMMA, lemma)

```
Preconditions: Σ₁ and Σ₂ are span-sets whose component spans are level-uniform
               and mutually level-compatible across both sets.

Commutativity:
  normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)

Preconditions for associativity: additionally Σ₃ mutually level-compatible with Σ₁, Σ₂.

Associativity:
  normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃))

Proof: ⟦Σ₁ ∪ Σ₂⟧ = ⟦Σ₁⟧ ∪ ⟦Σ₂⟧ = ⟦Σ₂⟧ ∪ ⟦Σ₁⟧ = ⟦Σ₂ ∪ Σ₁⟧.
Since normalization depends only on the denotation (S9), the result follows.
Associativity follows identically from the associativity of set union.
```

## S11 — DifferenceBound (LEMMA, lemma)

```
Preconditions: α and β are level-uniform; level_compat(start(α), start(β));
               ⟦β⟧ ⊆ ⟦α⟧  (i.e., start(α) ≤ start(β) ∧ reach(β) ≤ reach(α)).

The set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most 2 spans.

Construction:
  Left interval:   {t : start(α) ≤ t < start(β)}
    When start(α) < start(β):
      λ = (start(α), start(β) ⊖ start(α))
      reach(λ) = start(β)   (by D1)
      level-uniform: #width(λ) = max(#start(β), #start(α)) = #start(α)

  Right interval:  {t : reach(β) ≤ t < reach(α)}
    When reach(β) < reach(α):
      ρ = (reach(β), reach(α) ⊖ reach(β))
      reach(ρ) = reach(α)   (by D1)
      level-uniform: #width(ρ) = max(#reach(α), #reach(β)) = #reach(β) = #start(ρ)

Result: span-set of 0, 1, or 2 components:
  (a) start(α) = start(β) ∧ reach(β) = reach(α)  (α = β): 0 spans
  (b) exactly one boundary coincides: 1 span
  (c) neither coincides: 2 spans — {λ, ρ}

The bound of 2 is tight.
```
