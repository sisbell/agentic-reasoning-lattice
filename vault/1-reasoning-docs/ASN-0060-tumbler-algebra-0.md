# ASN-0060: Tumbler Algebra 0

*2026-03-21*

ASN-0034 defines the tumbler type T, its lexicographic order T1, and the arithmetic operations TumblerAdd (⊕) and TumblerSub (⊖) with their order-preservation and cancellation properties. This ASN extends that foundation with the ordinal shift — a derived operation that advances a tumbler's final component by a fixed natural number while preserving all higher-level components. The ordinal displacement is a specific displacement shape whose action point falls at the deepest component; the shift applies it through TumblerAdd. Order preservation and injectivity of the shift follow directly from TA1-strict and TA-MTO in the base algebra.


## Ordinal Displacement

**Definition — OrdinalDisplacement.** For natural number n ≥ 1 and depth m ≥ 1, the *ordinal displacement* δ(n, m) is the tumbler [0, 0, ..., 0, n] of length m — zero at positions 1 through m − 1, and n at position m. Its action point is m.

When the depth is determined by context (typically m = #v for the tumbler being shifted), we write δₙ.


## Ordinal Shift

**Definition — OrdinalShift.** For a V-position v of depth m and natural number n ≥ 1:

`shift(v, n) = v ⊕ δ(n, m)`

By TumblerAdd (ASN-0034): shift(v, n)ᵢ = vᵢ for i < m, and shift(v, n)ₘ = vₘ + n. The shift advances the ordinal within the V-position's subspace by exactly n, leaving all higher-level components unchanged.

Additionally, shift preserves structural properties. When m ≥ 2, the action point of δₙ leaves position 1 unchanged — shift(v, n)₁ = v₁. When m = 1, shift([S], n) = [S + n] changes the first component. Furthermore, #shift(v, n) = #δₙ = m = #v by the result-length identity of TumblerAdd. The shift preserves tumbler depth, and — since vₘ + n > 0 whenever vₘ ≥ 1 — component positivity.


## Shift Order Preservation

**I6 — ShiftOrderPreservation.**

`(A v₁, v₂ : #v₁ = #v₂ = m ∧ v₁ < v₂ : shift(v₁, n) < shift(v₂, n))`

*Derivation.* Since #v₁ = #v₂ = m and v₁ ≠ v₂, the divergence point satisfies divergence(v₁, v₂) ≤ m. The action point of δₙ is m ≥ divergence(v₁, v₂). By TA1-strict (ASN-0034): v₁ ⊕ δₙ < v₂ ⊕ δₙ. ∎


## Shift Injectivity

**I7 — ShiftInjectivity.**

`(A v₁, v₂ : #v₁ = #v₂ = m : shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂)`

*Derivation.* By TA-MTO (ASN-0034): v₁ ⊕ δₙ = v₂ ⊕ δₙ iff (A i : 1 ≤ i ≤ m : v₁ᵢ = v₂ᵢ). The action point of δₙ is m, and agreement at positions 1..m for tumblers of length m means v₁ = v₂ by T3 (CanonicalRepresentation). ∎


## Statement Registry

| Label | Type | Statement | Status |
|-------|------|-----------|--------|
| OrdinalDisplacement | definition | δ(n, m) = [0, ..., 0, n] of length m, action point m | introduced |
| OrdinalShift | definition | shift(v, n) = v ⊕ δ(n, #v) | introduced |
| I6 | lemma | shift preserves strict order: v₁ < v₂ ⟹ shift(v₁, n) < shift(v₂, n) | introduced |
| I7 | lemma | shift is injective: shift(v₁, n) = shift(v₂, n) ⟹ v₁ = v₂ | introduced |
