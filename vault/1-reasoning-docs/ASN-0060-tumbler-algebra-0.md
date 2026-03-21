# ASN-0060: Tumbler Algebra 0

*2026-03-21*

ASN-0034 defines the tumbler type T, its lexicographic order T1, and the arithmetic operations TumblerAdd (⊕) and TumblerSub (⊖) with their order-preservation and cancellation properties. This ASN extends that foundation with the ordinal shift — a derived operation that advances a tumbler's final component by a fixed natural number while preserving all higher-level components. The ordinal displacement is a specific displacement shape whose action point falls at the deepest component; the shift applies it through TumblerAdd. Order preservation and injectivity of the shift follow directly from TA1-strict and TA-MTO in the base algebra.


## Ordinal Displacement

**Definition — OrdinalDisplacement.** For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.


## Ordinal Shift

**Definition — OrdinalShift.** For a tumbler v of length m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

TA0 is satisfied: the action point of δ(n, m) is m = #v, so k ≤ #v holds trivially. By TumblerAdd (ASN-0034): shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift advances the deepest component by exactly n, leaving all higher-level components unchanged.

Additionally, shift preserves structural properties. When m ≥ 2, the action point of δₙ leaves position 1 unchanged — shift(v, n)₁ = v₁. When m = 1, shift([S], n) = [S + n] changes the first component. Furthermore, #shift(v, n) = #δₙ = m = #v by the result-length identity of TumblerAdd. The shift preserves tumbler depth, and — since n ≥ 1 — component positivity: shift(v, n)ₘ = vₘ + n ≥ 1 unconditionally for all vₘ ≥ 0.


## Shift Order Preservation

**I6 — ShiftOrderPreservation.**

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

*Derivation.* Fix n ≥ 1. Since #v₁ = #v₂ = m and v₁ ≠ v₂, the divergence point satisfies divergence(v₁, v₂) ≤ m. The action point of δₙ is m ≥ divergence(v₁, v₂). By TA1-strict (ASN-0034): v₁ ⊕ δₙ < v₂ ⊕ δₙ. ∎


## Shift Injectivity

**I7 — ShiftInjectivity.**

`(A v₁, v₂, n : n ≥ 1 ∧ #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Derivation.* Fix n ≥ 1. By TA-MTO (ASN-0034): v₁ ⊕ δₙ = v₂ ⊕ δₙ iff (A i : 1 ≤ i ≤ m : v₁ᵢ = v₂ᵢ). The action point of δₙ is m, and agreement at positions 1..m for tumblers of length m means v₁ = v₂ by T3 (CanonicalRepresentation). ∎


## Shift Composition

**I8 — ShiftComposition.**

`(A v, n₁, n₂ : n₁ ≥ 1 ∧ n₂ ≥ 1 ∧ #v = m : shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂))`

*Derivation.* Expanding: shift(shift(v, n₁), n₂) = (v ⊕ δ(n₁, m)) ⊕ δ(n₂, m). By TA-assoc (ASN-0034): (v ⊕ δ(n₁, m)) ⊕ δ(n₂, m) = v ⊕ (δ(n₁, m) ⊕ δ(n₂, m)). The action point of both displacements is m. By TumblerAdd, δ(n₁, m) ⊕ δ(n₂, m) has components 0 at positions 1..m−1 and n₁ + n₂ at position m — that is, δ(n₁ + n₂, m). So the expression equals v ⊕ δ(n₁ + n₂, m) = shift(v, n₁ + n₂). ∎


## Worked Example

Let v = [2, 3, 7] (m = 3) and n = 4. Then δ(4, 3) = [0, 0, 4] with action point 3. TA0: k = 3 ≤ 3 = #v. By TumblerAdd: shift(v, 4) = [2, 3, 7 + 4] = [2, 3, 11].

For I6: take v₁ = [2, 3, 5] < v₂ = [2, 3, 9] with n = 4. Then shift(v₁, 4) = [2, 3, 9] < [2, 3, 13] = shift(v₂, 4). ✓

For I8: shift(shift([2, 3, 7], 4), 3) = shift([2, 3, 11], 3) = [2, 3, 14] = shift([2, 3, 7], 7). ✓


## Statement Registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| OrdinalDisplacement | definition | δ(n, m) = [0, ..., 0, n] of length m, action point m | introduced |
| OrdinalShift | definition | shift(v, n) = v ⊕ δ(n, #v) | introduced |
| I6 | lemma | shift preserves strict order: v₁ < v₂ ⟹ shift(v₁, n) < shift(v₂, n) | introduced |
| I7 | lemma | shift is injective: shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂ | introduced |
| I8 | lemma | shift composes additively: shift(shift(v, n₁), n₂) = shift(v, n₁ + n₂) | introduced |
