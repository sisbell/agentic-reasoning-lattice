# ASN-0056: Span Algebra 0

*2026-03-19*

This ASN extends the span algebra (ASN-0053) with the set difference bound for all SpanClassification cases. ASN-0053's S11 (DifferenceBound) establishes the containment case: when ⟦β⟧ ⊆ ⟦α⟧, the difference ⟦α⟧ \ ⟦β⟧ is at most 2 spans. We complete the picture for the remaining SC cases and unify the result.


## Difference for separated and adjacent spans

**S11a** — *DifferenceSeparated* (LEMMA, lemma). For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (i) (separated) or (ii) (adjacent): ⟦α⟧ \ ⟦β⟧ = ⟦α⟧.

*Proof.* In both cases ⟦α⟧ ∩ ⟦β⟧ = ∅ (SC classifies (i) and (ii) as the disjoint cases). When the intersection is empty, removing β's positions from α removes nothing: ⟦α⟧ \ ⟦β⟧ = ⟦α⟧. The result is a span-set of exactly 1 span.  ∎

*Worked example.* Let α = ([1, 3], [0, 4]) and β = ([1, 10], [0, 2]). Then reach(α) = [1, 7] and start(β) = [1, 10]. Since [1, 7] < [1, 10], the spans are separated (SC case (i)). No position belongs to both spans, so ⟦α⟧ \ ⟦β⟧ = ⟦α⟧ = {t : [1, 3] ≤ t < [1, 7]}, a single span.


## Difference for equal spans

**S11b** — *DifferenceEqual* (LEMMA, lemma). For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (v) (equal): ⟦α⟧ \ ⟦β⟧ = ∅.

*Proof.* Equal spans have start(α) = start(β) and reach(α) = reach(β), so ⟦α⟧ = ⟦β⟧. The set difference of a set with itself is empty: ⟦α⟧ \ ⟦β⟧ = ∅. The result is a span-set of 0 spans.  ∎

*Worked example.* Let α = β = ([1, 3], [0, 4]). Then ⟦α⟧ \ ⟦β⟧ = ∅.


## Difference for proper overlap

**S11c** — *DifferenceOverlap* (LEMMA, lemma). For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (iii) (proper overlap): ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of exactly 1 span.

*Proof.* Assume without loss of generality start(α) < start(β) < reach(α) < reach(β) (the symmetric case swaps α and β). The positions in ⟦α⟧ but not in ⟦β⟧ are those in α that precede the start of β:

  ⟦α⟧ \ ⟦β⟧ = {t : start(α) ≤ t < start(β)}

This is non-empty (start(α) < start(β) and start(α) ∈ ⟦α⟧ \ ⟦β⟧) and forms a single contiguous interval. We construct the span explicitly.

Define γ = (start(α), start(β) ⊖ start(α)). Since start(α) < start(β) and #start(α) = #start(β) (level-compatibility), the divergence k is of type (i) with k ≤ #start(α). The width start(β) ⊖ start(α) has a positive component at position k, so it is positive with action point k ≤ #start(α) — T12 is satisfied. By D1 (DisplacementRoundTrip, ASN-0053), reach(γ) = start(α) ⊕ (start(β) ⊖ start(α)) = start(β). The span is level-uniform: #width(γ) = max(#start(β), #start(α)) = #start(α) = #start(γ).

The denotation ⟦γ⟧ = {t : start(α) ≤ t < start(β)} = ⟦α⟧ \ ⟦β⟧. The result is exactly 1 span.  ∎

*Worked example.* Let α = ([1, 3], [0, 7]) and β = ([1, 6], [0, 8]). Then reach(α) = [1, 10] and reach(β) = [1, 14]. Verify proper overlap: start(α) = [1, 3] < start(β) = [1, 6] < reach(α) = [1, 10] < reach(β) = [1, 14]. The difference ⟦α⟧ \ ⟦β⟧ = {t : [1, 3] ≤ t < [1, 6]}. Construct γ = ([1, 3], [1, 6] ⊖ [1, 3]) = ([1, 3], [0, 3]). Verify: reach(γ) = [1, 3] ⊕ [0, 3] = [1, 6] = start(β). Verify denotation: ⟦γ⟧ = {t : [1, 3] ≤ t < [1, 6]} = ⟦α⟧ \ ⟦β⟧.

For the symmetric case (start(β) < start(α) < reach(β) < reach(α)), the difference ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}. Define γ' = (reach(β), reach(α) ⊖ reach(β)). We verify D1 preconditions for the pair (reach(β), reach(α)): reach(β) < reach(α) is given; level-uniformity of α gives #reach(α) = #start(α), level-uniformity of β gives #reach(β) = #start(β), and level_compat(start(α), start(β)) gives #start(α) = #start(β), so #reach(β) = #reach(α) — neither is a proper prefix of the other, so divergence is of type (i) with k ≤ #reach(β). By D1, reach(γ') = reach(β) ⊕ (reach(α) ⊖ reach(β)) = reach(α). The span is level-uniform: #width(γ') = max(#reach(α), #reach(β)) = #reach(β) = #start(γ'). The result is exactly 1 span.


## Unified difference bound

The four results combine into a single statement covering all SC cases:

**S11d** — *GeneralDifferenceBound* (LEMMA, lemma). For level-uniform spans α and β with level_compat(start(α), start(β)), the set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most 2 spans.

*Proof.* By SC (SpanClassification, ASN-0053), exactly one of five cases holds:

| SC case | Difference | Bound | By |
|---------|-----------|-------|----|
| (i) Separated | ⟦α⟧ | 1 span | S11a |
| (ii) Adjacent | ⟦α⟧ | 1 span | S11a |
| (iii) Proper overlap | 1 span | 1 span | S11c |
| (iv) Containment (⟦β⟧ ⊂ ⟦α⟧) | at most 2 spans | 2 spans | S11 (ASN-0053) |
| (iv) Containment (⟦α⟧ ⊂ ⟦β⟧) | ∅ | 0 spans | ⟦α⟧ ⊆ ⟦β⟧ ⟹ difference empty |
| (v) Equal | ∅ | 0 spans | S11b |

The maximum across all cases is 2, achieved only in the containment case.  ∎

The bound of 2 is tight: S11 (ASN-0053) shows containment achieves it. No SC case exceeds it. This confirms Nelson's span-set mechanism is sufficient for representing any two-span difference.


## Statement registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| S11a | LEMMA, lemma | Separated or adjacent spans: ⟦α⟧ \ ⟦β⟧ = ⟦α⟧ (1 span) | introduced |
| S11b | LEMMA, lemma | Equal spans: ⟦α⟧ \ ⟦β⟧ = ∅ (0 spans) | introduced |
| S11c | LEMMA, lemma | Proper overlap: ⟦α⟧ \ ⟦β⟧ is exactly 1 span | introduced |
| S11d | LEMMA, lemma | General difference bound: ⟦α⟧ \ ⟦β⟧ is at most 2 spans for any SC case | introduced |
| S11 | LEMMA, lemma | Containment difference bound (DifferenceBound, ASN-0053) | cited |
| SC | LEMMA, lemma | SpanClassification (ASN-0053) | cited |
| D1 | LEMMA, lemma | DisplacementRoundTrip (ASN-0053) | cited |


## Open Questions

- Does the general difference bound extend to span-set difference? Given normalized span-sets Σ₁ and Σ₂, what is the tight bound on |normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)|?
