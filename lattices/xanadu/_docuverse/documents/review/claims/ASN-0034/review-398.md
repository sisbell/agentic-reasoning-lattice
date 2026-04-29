# Regional Review — ASN-0034/T2 (cycle 1)

*2026-04-23 00:21*

### Meta-prose in NAT-order commentary about axiom structure
**Class**: OBSERVE
**Foundation**: NAT-order (NatStrictTotalOrder)
**ASN**: The paragraph after the axiom clauses: "The axiom slot introduces `<` before constraining it: the first clause `< ⊆ ℕ × ℕ` posits `<` as a binary relation on ℕ, and the three strict-total-order clauses that follow then constrain that relation. NAT-closure follows the same register for the arithmetic primitive..."
**Issue**: This prose explains the ASN's axiom-writing convention and compares formats across ASNs rather than saying anything about `<`. A reader chasing the meaning of the axiom must skip past a register-consistency note. Matches the reviser-drift pattern of new prose around an axiom explaining why the axiom is structured rather than what it says.

### Meta-prose in NAT-wellorder commentary about Depends slot
**Class**: OBSERVE
**Foundation**: NAT-wellorder (NatWellOrdering)
**ASN**: "The axiom body invokes the non-strict companion `≤`, which is not a primitive of ℕ — it is *defined* in NAT-order by `m ≤ n ⟺ m < n ∨ m = n`. NAT-order is therefore declared in the Depends slot so that the axiom body can be read without silently importing the definition. The set-theoretic primitives `⊆`, `∈`, and `≠ ∅` carry their standard first-order meaning..."
**Issue**: This paragraph justifies the Depends declaration and inventories which set-theoretic primitives are *not* being axiomatized, rather than clarifying the least-element principle itself. The content belongs, if anywhere, in a reviewer-facing defense of the contract, not in-line with the axiom.

### Meta-prose in T0 on provenance of `1` and `≤`
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition)
**ASN**: "The numeral `1` bounding the length from below is the `1 ∈ ℕ` posited by NAT-closure; the relation `≤` is the non-strict order on ℕ defined by NAT-order. The inequality `1 ≤ #a` is thus well-typed within ℕ, and with it the index domain `{1, …, #a}` is never empty, so bounded quantifiers of the form `(Q i : 1 ≤ i ≤ #a : …)` range over a nonempty set rather than collapsing to vacuity."
**Issue**: The provenance attribution of `1` and `≤` is dependency-justification content; the concluding clause about quantifiers-not-collapsing-to-vacuity is a defensive remark about an edge case T0 already precludes. Both belong in a Depends-rationale, not the axiom exposition.

### Loose justification of `k₂ ≤ m` in Transitivity, Case k₂ < k₁
**Class**: OBSERVE
**Foundation**: T1 (LexicographicOrder), part (c)
**ASN**: "Since `k₂ < k₁` and `a` has components below `k₁`, `k₂ ≤ m`."
**Issue**: In case (i) of `a < b`, `k₁ ≤ m` so `k₂ < k₁ ≤ m` gives `k₂ < m ⟹ k₂ ≤ m` directly. In case (ii), `k₁ = m + 1`, so `k₂ < m + 1` and the step to `k₂ ≤ m` requires NAT-discrete (which the Depends list credits but the proof text does not cite). "a has components below k₁" is a phrasing that elides the sub-split and the axiom appeal.

### T2 postcondition (c) overstates what is consulted
**Class**: OBSERVE
**Foundation**: T2 (IntrinsicComparison)
**ASN**: Postcondition (c): "The only values consulted are `{aᵢ : 1 ≤ i ≤ #a}`, `{bᵢ : 1 ≤ i ≤ #b}`, `#a`, and `#b`."
**Issue**: The proof establishes an at-most bound (at most `#a` and at most `#b` pairs). Postcondition (c) then frames the consulted set as *all* components, which is an upper-bound enclosure rather than a characterization of what the comparison actually reads. Read literally, (c) is true (the consulted values are a subset of those sets) but redundant with (b); read as an exact claim, it is looser than what the proof delivers.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 107s*
