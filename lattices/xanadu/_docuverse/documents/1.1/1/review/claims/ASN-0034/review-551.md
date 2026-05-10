# Cone Review — ASN-0034/OrdinalDisplacement (cycle 1)

*2026-04-25 17:53*

### T0 inner quantifier domains under-specified
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: T0's comprehension axiom `(A p ∈ ℕ : p ≥ 1 : (A r : … :: (E t ∈ T :: #t = p ∧ (A i : 1 ≤ i ≤ p : tᵢ = r(i)))))` and extensionality `(A a, b ∈ T : #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ) : a = b)`.
**Issue**: The innermost universals `(A i : 1 ≤ i ≤ p : …)` and `(A i : 1 ≤ i ≤ #a : …)` omit the carrier `i ∈ ℕ`. Other quantifiers throughout the document carry an explicit set membership (e.g. `(A n ∈ ℕ : …)`, `(A i ∈ ℕ : 1 ≤ i ≤ #t : …)`). The omission is recoverable from context but is stylistically inconsistent.

### OrdinalDisplacement cites "disjointness clause" not stated in NAT-order
**Class**: OBSERVE
**Foundation**: NAT-order (NatStrictTotalOrder), Consequence enumerates `¬(m < n ∧ m = n)`.
**ASN**: OrdinalDisplacement's `n ≥ 1 ⟹ n ≠ 0` derivation: "By NAT-order's disjointness clause `(A m, n ∈ ℕ : m < n : m ≠ n)` instantiated at `(0, n)`, the hypothesis `0 < n` yields `0 ≠ n`".
**Issue**: NAT-order's contract states `¬(m < n ∧ m = n)` as a sub-clause of exactly-one trichotomy; it does not state the cited universal form `(A m, n ∈ ℕ : m < n : m ≠ n)` and does not name any clause "disjointness". The two are logically equivalent (one classical-logic step), but the citation paraphrases rather than reproducing the contract clause it is invoking.

### ActionPoint's parenthetical justification of S ⊆ ℕ misroutes through T0
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition); ActionPoint (ActionPoint).
**ASN**: ActionPoint derivation: "The set S = {i ∈ ℕ : 1 ≤ i ≤ #w ∧ wᵢ ≠ 0} is a nonempty subset of ℕ: nonempty by TA-Pos, and a subset of ℕ by construction (the carrier `i ∈ ℕ` is licensed by T0's commitment that the index domain `{1, …, #w}` of w lies in ℕ)."
**Issue**: Subsetness of S in ℕ follows from the form of the set-builder `{i ∈ ℕ : …}` alone — T0 has no role to play there. T0's commitment is what makes the predicate `wᵢ ≠ 0` well-typed for `i ∈ {j ∈ ℕ : 1 ≤ j ≤ #w}`. The parenthetical conflates the well-formedness role of T0 with the subset claim, which is grounded in set-builder syntax. Reads as reviser drift in a justification slot.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 271s*
