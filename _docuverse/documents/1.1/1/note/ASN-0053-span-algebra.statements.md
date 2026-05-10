# ASN-0053 Claim Statements

*Source: ASN-0053-span-algebra.md (revised 2026-03-19) — Extracted: 2026-03-19*

## Definition — SpanReach

```
reach(σ) = start(σ) ⊕ width(σ)
```
The exclusive upper bound of span σ = (s, ℓ).

## Definition — SpanDenotation

```
⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}
```

## Definition — SpanSetDenotation

```
⟦Σ⟧ = ⟦σ₁⟧ ∪ ⟦σ₂⟧ ∪ ... ∪ ⟦σₙ⟧
```
For span-set Σ = ⟨σ₁, σ₂, ..., σₙ⟩. The empty span-set ⟨⟩ denotes ∅.

## Definition — SpanSetEquivalence

```
Σ₁ ≡ Σ₂  ⟺  ⟦Σ₁⟧ = ⟦Σ₂⟧
```

## Definition — LevelCompat

```
level_compat(t₁, t₂)  ≡  #t₁ = #t₂
```

## Definition — LevelUniform

```
A span σ = (s, ℓ) is level-uniform when level_compat(s, ℓ), i.e., #s = #ℓ.
```

## Definition — Adjacent

```
adjacent(α, β)  ≡  reach(α) = start(β)  ∨  reach(β) = start(α)
```

## Definition — InteriorPoint

```
A position p is interior to span σ when start(σ) < p < reach(σ).
```

## Definition — NormalizedSpanSet

```
A span-set Σ = ⟨σ₁, ..., σₙ⟩ is normalized iff:

  (N1)  (A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))
  (N2)  (A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))
```

---

## D0 — DisplacementWellDefined (AXIOM, cited)

```
For tumblers a, b ∈ T with a < b and divergence(a, b) ≤ #a:
the displacement b ⊖ a is a well-defined positive tumbler,
and a ⊕ (b ⊖ a) is defined (TA0 satisfied).
```

## D1 — DisplacementRoundTrip (AXIOM, cited)

```
For tumblers a, b ∈ T with a < b, divergence(a, b) ≤ #a, and #a ≤ #b:
  a ⊕ (b ⊖ a) = b
```

## D2 — WidthRecovery (AXIOM, cited)

```
For a level-uniform span σ = (s, ℓ) with #s = #ℓ:
  reach(σ) ⊖ start(σ) = width(σ)
```

## TA-LC — LeftCancellation (AXIOM, cited)

```
For tumblers a, x, y with both a ⊕ x and a ⊕ y defined:
  a ⊕ x = a ⊕ y  ⟹  x = y
```

---

## S0 — Convexity (LEMMA, lemma)

```
(A p, q, r : p ∈ ⟦σ⟧ ∧ r ∈ ⟦σ⟧ ∧ p ≤ q ≤ r : q ∈ ⟦σ⟧)
```

## SC — SpanClassification (DEF, definition)

```
Given spans α and β, exactly one of five mutually exclusive cases holds:

(i)   Separated.   reach(α) < start(β)  ∨  reach(β) < start(α)
(ii)  Adjacent.    reach(α) = start(β)  ∨  reach(β) = start(α)
(iii) Proper overlap.
        start(α) < start(β) < reach(α) < reach(β),  or symmetrically.
(iv)  Containment.
        start(α) ≤ start(β) ∧ reach(β) ≤ reach(α) with at least one strict,
        or symmetrically.
(v)   Equal.       start(α) = start(β)  ∧  reach(α) = reach(β)

Cases (i) and (ii) are the disjoint cases: ⟦α⟧ ∩ ⟦β⟧ = ∅.
Cases (iii), (iv), and (v) are the overlapping cases: ⟦α⟧ ∩ ⟦β⟧ ≠ ∅.
```

## S6 — LevelConstraint (LEMMA, lemma)

```
For a level-uniform span σ = (s, ℓ) with #s = #ℓ:
  #reach(σ) = #s

Corollary: level_compat(start(σ), reach(σ)) holds for every level-uniform span.
Level-uniform spans automatically satisfy D0 for all endpoint pairs: since
#start = #reach, neither is a proper prefix of the other, so divergence is of
type (i) with k ≤ #start.
```

## S1 — IntersectionClosure (LEMMA, lemma)

```
Precondition: α and β are level-uniform with level_compat(start(α), start(β)).

Either ⟦α⟧ ∩ ⟦β⟧ = ∅, or there exists a span γ such that ⟦γ⟧ = ⟦α⟧ ∩ ⟦β⟧.

Construction: let s' = max(start(α), start(β)) and r' = min(reach(α), reach(β)).
  — If r' ≤ s': intersection is empty.
  — If r' > s': γ = (s', r' ⊖ s'), with reach(γ) = r'. γ is level-uniform.
```

## S2 — EmptyDistinction (LEMMA, lemma)

```
The empty set of positions is not the denotation of any span.
Every well-formed span denotes a non-empty set.
```

## S3 — MergeEquivalence (LEMMA, lemma)

```
Precondition: α and β are level-uniform with level_compat(start(α), start(β)),
and they overlap or are adjacent (reach(α) ≥ start(β), assuming start(α) ≤ start(β)).

The union ⟦α⟧ ∪ ⟦β⟧ is the denotation of a single span γ, where:
  s = min(start(α), start(β))
  r = max(reach(α), reach(β))
  γ = (s, r ⊖ s)

with reach(γ) = r. γ is level-uniform.
```

## S3a — MergeCommutativity (LEMMA, lemma)

```
⟦α⟧ ∪ ⟦β⟧ = ⟦β⟧ ∪ ⟦α⟧
```

## S4 — SplitPartition (LEMMA, lemma)

```
Precondition: σ = (s, ℓ) is level-uniform, p is interior to σ,
and level_compat(s, p).

The displacements d = p ⊖ s and d' = reach(σ) ⊖ p are well-defined
with #d = #s = #d'. The left span λ = (s, d) and right span ρ = (p, d') satisfy:

  (a)  ⟦λ⟧ ∪ ⟦ρ⟧ = ⟦σ⟧                  (nothing lost)
  (b)  ⟦λ⟧ ∩ ⟦ρ⟧ = ∅                      (nothing duplicated)
  (c)  reach(λ) = start(ρ) = p             (the parts are adjacent)

Both λ and ρ are level-uniform.
```

## S5 — SplitWidthComposition (LEMMA, lemma)

```
Under the same preconditions as S4 (σ = (s, ℓ) level-uniform, p interior,
level_compat(s, p)), with d = p ⊖ s and d' = reach(σ) ⊖ p:

  d ⊕ d' = ℓ
```

## S4a — SplitMergeInverse (LEMMA, lemma)

```
Precondition: σ = (s, ℓ) is level-uniform, p is interior to σ,
and level_compat(s, p).

Splitting σ at p (S4) yields λ = (s, d) and ρ = (p, d').
Merging λ and ρ (S3) yields γ = (s, ℓ) = σ.
```

## S3b — MergeSplitInverse (LEMMA, lemma)

```
Precondition: α and β are adjacent level-uniform spans with reach(α) = start(β)
and level_compat(start(α), start(β)).

Merging α and β (S3) yields γ with start(γ) = start(α) and reach(γ) = reach(β).
Splitting γ at p = start(β) (S4) recovers:
  left part  = α  (i.e., (start(α), width(α)))
  right part = β  (i.e., (start(β), width(β)))
```

## S7 — FiniteRepresentability (LEMMA, lemma)

```
Every finite set of positions P ⊂ T admits a span-set Σ with ⟦Σ⟧ ⊇ P.
```

## S8 — NormalizationExistence (LEMMA, lemma)

```
Precondition: Σ is a span-set whose component spans are level-uniform and
mutually level-compatible.

There exists a normalized span-set Σ̂ with Σ̂ ≡ Σ.

Construction (sweep):
  — Sort component spans by start position.
  — Maintain current interval [s, r). For each span σᵢ in sorted order:
      • If start(σᵢ) ≤ r: update r := max(r, reach(σᵢ)).
      • If start(σᵢ) > r: emit (s, r ⊖ s); set [s, r) := [start(σᵢ), reach(σᵢ)).
  — Emit final (s, r ⊖ s).

Loop invariant J (after processing σ₁..σᵢ, with E = emitted spans, [s,r) = current):
  ⟦E⟧ ∪ [s, r) = ⟦σ₁⟧ ∪ ... ∪ ⟦σᵢ⟧
```

## S9 — NormalizationUniqueness (LEMMA, lemma)

```
Precondition: Σ̂₁ and Σ̂₂ are both normalized and Σ̂₁ ≡ Σ̂₂.

  Σ̂₁ = Σ̂₂
```

## S10 — UnionOrderIndependence (LEMMA, lemma)

```
Precondition: component spans of all span-sets are level-uniform and
mutually level-compatible across operand sets.

Commutativity:
  normalize(Σ₁ ∪ Σ₂) = normalize(Σ₂ ∪ Σ₁)

Associativity:
  normalize((Σ₁ ∪ Σ₂) ∪ Σ₃) = normalize(Σ₁ ∪ (Σ₂ ∪ Σ₃))
```

## S11 — DifferenceBound (LEMMA, lemma)

```
Precondition: α and β are level-uniform with level_compat(start(α), start(β))
and ⟦β⟧ ⊆ ⟦α⟧ (i.e., start(α) ≤ start(β) and reach(β) ≤ reach(α)).

⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most two spans.

Decomposition:
  Left:   {t : start(α) ≤ t < start(β)}   — empty when start(α) = start(β)
  Right:  {t : reach(β) ≤ t < reach(α)}   — empty when reach(β) = reach(α)

Left span (when start(α) < start(β)):
  λ = (start(α), start(β) ⊖ start(α)),  reach(λ) = start(β)

Right span (when reach(β) < reach(α)):
  ρ = (reach(β), reach(α) ⊖ reach(β)),  reach(ρ) = reach(α)

Cases:
  (a) start(α) = start(β) and reach(β) = reach(α): 0 spans.
  (b) Exactly one boundary coincides: 1 span.
  (c) Neither coincides: 2 spans.
```

## S11a — DifferenceSeparated (LEMMA, lemma)

```
Precondition: α and β are level-uniform with level_compat(start(α), start(β)),
in SC case (i) (separated) or (ii) (adjacent).

  ⟦α⟧ \ ⟦β⟧ = ⟦α⟧
```

## S11b — DifferenceEqual (LEMMA, lemma)

```
Precondition: α and β are level-uniform with level_compat(start(α), start(β)),
in SC case (v) (equal).

  ⟦α⟧ \ ⟦β⟧ = ∅
```

## S11c — DifferenceOverlap (LEMMA, lemma)

```
Precondition: α and β are level-uniform with level_compat(start(α), start(β)),
in SC case (iii) (proper overlap).

⟦α⟧ \ ⟦β⟧ is expressible as a span-set of exactly 1 span.

Case 1: start(α) < start(β) < reach(α) < reach(β).
  ⟦α⟧ \ ⟦β⟧ = {t : start(α) ≤ t < start(β)}
  γ = (start(α), start(β) ⊖ start(α))
  reach(γ) = start(β)   [by D1]
  ⟦γ⟧ = ⟦α⟧ \ ⟦β⟧

Case 2: start(β) < start(α) < reach(β) < reach(α).
  ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}
  γ' = (reach(β), reach(α) ⊖ reach(β))
  reach(γ') = reach(α)   [by D1]
  ⟦γ'⟧ = ⟦α⟧ \ ⟦β⟧
```

## S11d — GeneralDifferenceBound (LEMMA, lemma)

```
Precondition: α and β are level-uniform with level_compat(start(α), start(β)).

⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most 2 spans.

| SC case                          | Difference   | Bound  | By   |
|----------------------------------|--------------|--------|------|
| (i) Separated                    | ⟦α⟧          | 1 span | S11a |
| (ii) Adjacent                    | ⟦α⟧          | 1 span | S11a |
| (iii) Proper overlap             | 1 span       | 1 span | S11c |
| (iv) Containment (⟦β⟧ ⊂ ⟦α⟧)   | at most 2    | 2 span | S11  |
| (iv) Containment (⟦α⟧ ⊆ ⟦β⟧)   | ∅            | 0 span | (*)  |
| (v) Equal                        | ∅            | 0 span | S11b |

(*) Reverse containment: start(β) ≤ start(α) and reach(α) ≤ reach(β) with at
least one strict implies ⟦α⟧ ⊆ ⟦β⟧, so ⟦α⟧ \ ⟦β⟧ = ∅.
```

## σ.reach — SpanReach (DEF, definition)

```
reach(σ) = start(σ) ⊕ width(σ)
```
*(See Definition — SpanReach above.)*

## σ.denotation — SpanDenotation (DEF, definition)

```
⟦σ⟧ = {t ∈ T : start(σ) ≤ t < reach(σ)}
```
*(See Definition — SpanDenotation above.)*

## Σ.setdenotation — SpanSetDenotation (DEF, definition)

```
⟦Σ⟧ = ⟦σ₁⟧ ∪ ⟦σ₂⟧ ∪ ... ∪ ⟦σₙ⟧
```
*(See Definition — SpanSetDenotation above.)*

## N1, N2 — NormalizedSpanSet (DEF, definition)

```
(N1)  (A i : 1 ≤ i < n : start(σᵢ) < start(σᵢ₊₁))
(N2)  (A i : 1 ≤ i < n : reach(σᵢ) < start(σᵢ₊₁))
```
*(See Definition — NormalizedSpanSet above.)*
