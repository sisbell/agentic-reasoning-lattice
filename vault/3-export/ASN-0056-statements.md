# ASN-0056 Formal Statements

*Source: ASN-0056-span-algebra-0.md (revised 2026-03-19) — Extracted: 2026-03-19*

## S11a — DifferenceSeparated (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (i) (separated) or (ii) (adjacent): ⟦α⟧ \ ⟦β⟧ = ⟦α⟧.

## S11b — DifferenceEqual (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (v) (equal): ⟦α⟧ \ ⟦β⟧ = ∅.

## S11c — DifferenceOverlap (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (iii) (proper overlap): ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of exactly 1 span.

**Case 1:** start(α) < start(β) < reach(α) < reach(β):

  ⟦α⟧ \ ⟦β⟧ = {t : start(α) ≤ t < start(β)}

Witness: γ = (start(α), start(β) ⊖ start(α)), with reach(γ) = start(β) and ⟦γ⟧ = {t : start(α) ≤ t < start(β)}.

**Case 2:** start(β) < start(α) < reach(β) < reach(α):

  ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}

Witness: γ' = (reach(β), reach(α) ⊖ reach(β)), with reach(γ') = reach(α) and ⟦γ'⟧ = {t : reach(β) ≤ t < reach(α)}.

## S11d — GeneralDifferenceBound (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)), the set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most 2 spans.

| SC case | Difference | Bound |
|---------|-----------|-------|
| (i) Separated | ⟦α⟧ | 1 span |
| (ii) Adjacent | ⟦α⟧ | 1 span |
| (iii) Proper overlap | 1 span | 1 span |
| (iv) Containment (⟦β⟧ ⊂ ⟦α⟧) | at most 2 spans | 2 spans |
| (iv) Containment (⟦α⟧ ⊂ ⟦β⟧) | ∅ | 0 spans |
| (v) Equal | ∅ | 0 spans |

For the reverse containment sub-case of SC(iv) — start(β) ≤ start(α) and reach(α) ≤ reach(β) with at least one strict: for t ∈ ⟦α⟧, start(β) ≤ start(α) ≤ t and t < reach(α) ≤ reach(β), so t ∈ ⟦β⟧, hence ⟦α⟧ ⊆ ⟦β⟧ and the difference is empty.
