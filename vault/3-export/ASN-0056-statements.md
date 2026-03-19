# ASN-0056 Formal Statements

*Source: ASN-0056-span-algebra-0.md (revised 2026-03-19) — Extracted: 2026-03-19*

## S11a — DifferenceSeparated (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (i) (separated) or (ii) (adjacent): ⟦α⟧ \ ⟦β⟧ = ⟦α⟧.

## S11b — DifferenceEqual (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (v) (equal): ⟦α⟧ \ ⟦β⟧ = ∅.

## S11c — DifferenceOverlap (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)) in SC case (iii) (proper overlap): ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of exactly 1 span.

Sub-case (start(α) < start(β) < reach(α) < reach(β)):
  ⟦α⟧ \ ⟦β⟧ = {t : start(α) ≤ t < start(β)}
  Constructed as γ = (start(α), start(β) ⊖ start(α)), with reach(γ) = start(β).

Sub-case (start(β) < start(α) < reach(β) < reach(α)):
  ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}
  Constructed as (reach(β), reach(α) ⊖ reach(β)).

## S11d — GeneralDifferenceBound (LEMMA, lemma)

For level-uniform spans α and β with level_compat(start(α), start(β)), the set difference ⟦α⟧ \ ⟦β⟧ is expressible as a span-set of at most 2 spans.

| SC case | Difference | Bound | By |
|---------|-----------|-------|----|
| (i) Separated | ⟦α⟧ | 1 span | S11a |
| (ii) Adjacent | ⟦α⟧ | 1 span | S11a |
| (iii) Proper overlap | 1 span | 1 span | S11c |
| (iv) Containment | at most 2 spans | 2 spans | S11 (ASN-0053) |
| (v) Equal | ∅ | 0 spans | S11b |
