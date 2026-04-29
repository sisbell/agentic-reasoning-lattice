# Cone Review — ASN-0034/OrdinalShift (cycle 1)

*2026-04-25 22:09*

I'll review the ASN against Dijkstra's discipline. Reading through T0, the predicates in TA-Pos, the Action Point derivation, TumblerAdd, T1, T3, OrdinalDisplacement, OrdinalShift, and the supporting NAT-* axioms.

The proofs are detailed and walk their cases. The dependency DAG (T0 → T3, T1; T1, T3 → TumblerAdd, etc.) is acyclic. Pre-condition chains check out: TA0 forwards TumblerAdd's first two postconditions; OrdinalShift discharges TA0's four preconditions through OrdinalDisplacement; OrdinalDisplacement establishes Pos and actionPoint = m so the action-point bound holds at #v. The trichotomy proof of T1 partitions T × T correctly via the divergence-position least element.

I found minor issues only.

### NAT-carrier body explains why the axiom is needed rather than what it says
**Class**: OBSERVE
**Foundation**: NAT-carrier (NatCarrierSet)
**ASN**: "The declaration is irreducible at this level: `ℕ` is taken as a primitive — not constructed from a more elementary substrate, not extracted from the meta-language by ambient definability, but committed-to as a set... No further structure on `ℕ` is asserted here. The strict order `<` is introduced by NAT-order, the constants `0` and `1` by NAT-zero and NAT-closure respectively..."
**Issue**: The body argues *why* the carrier must be posited at this level and inventories what other NAT-* axioms add later — meta-content about the role of the axiom rather than content of the axiom itself. The actual claim is one line ("ℕ is a set"); the surrounding prose is a defensive justification and a use-site inventory.

### OrdinalShift cites "transitivity of <" for a chain of ≤ relations
**Class**: OBSERVE
**Foundation**: OrdinalShift (OrdinalShift)
**ASN**: "NAT-order composes `vₘ + n ≥ n` with precondition `n ≥ 1` into `vₘ + n ≥ 1` via its defining clause and transitivity of `<`."
**Issue**: The chain is `1 ≤ n ≤ vₘ + n ⟹ 1 ≤ vₘ + n`, i.e., ≤-transitivity. NAT-order exports a ≤-transitivity Consequence — citing it directly would be more honest than unfolding to `<`-disjuncts and reassembling.

### TumblerAdd's least-position set lacks ℕ-typing
**Class**: OBSERVE
**Foundation**: TumblerAdd (TumblerAdd)
**ASN**: "NAT-wellorder applied to `{j : 1 ≤ j < k ∧ aⱼ > 0}` supplies the least such `j`."
**Issue**: NAT-wellorder requires `S ⊆ ℕ`. The set-builder omits `j ∈ ℕ`. Implicit from the position-index typing in T0, but explicit `{j ∈ ℕ : ...}` would match the form NAT-wellorder consumes.

### TumblerAdd Definition slot lacks explicit length range
**Class**: OBSERVE
**Foundation**: TumblerAdd (TumblerAdd)
**ASN**: "*Definition:* k = actionPoint(w); rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k"
**Issue**: The Definition specifies the components but not the length of the result; the upper bound on `i` in the third clause is implicit. The prose states `#(a ⊕ w) = #w`, but the formal *Definition:* slot leaves the result's index domain unstated.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 767s*
