# Cone Review — ASN-0034/TA-Pos (cycle 1)

*2026-04-17 13:55*

### `tₖ ≥ 1` from `tₖ ≠ 0` requires 0 as a lower bound of ℕ, which no listed NAT-* axiom supplies
**Foundation**: T0 (CarrierSetDefinition) — "This list is exhaustive: the ASN states no NAT-* axiom outside it." The visible NAT-* axioms are NAT-order (irreflexivity/transitivity/trichotomy), NAT-discrete (`m ≤ n < m+1 ⟹ n = m`), NAT-wellorder (least element of nonempty subsets).
**ASN**: TA-Pos, postcondition proof, Case `#z ≥ k`: "`zₖ = 0 < tₖ` because `tₖ ≥ 1` as a nonzero natural number". Depends credits this to "NAT-discrete's axiom `m ≤ n < m + 1 ⟹ n = m` instantiated at `m = 0`".
**Issue**: Applying NAT-discrete at m=0 yields `0 ≤ n < 1 ⟹ n = 0`. To derive `tₖ ≥ 1` from `tₖ ≠ 0` via this, one first needs `0 ≤ tₖ`. None of the listed NAT-* axioms state that 0 is a lower bound of ℕ: NAT-order gives trichotomy but doesn't identify 0 with the minimum; NAT-wellorder gives ℕ a least element but doesn't name it 0; NAT-discrete constrains gaps, not lower bounds. The step silently uses a meta-theoretical fact about ℕ (that elements are ≥ 0) that the ASN's exhaustive axiomatisation does not discharge.
**What needs resolving**: Either (a) add a NAT-* axiom fixing 0 as the minimum of ℕ (or equivalently `(A n ∈ ℕ :: 0 ≤ n)`) and amend T0's exhaustive-list claim, or (b) route the `tₖ ≠ 0 ⟹ tₖ ≥ 1` step through a combination already discharged (e.g., NAT-wellorder pinning the minimum of ℕ and then NAT-discrete), with the composition made explicit in TA-Pos's Depends, or (c) reformulate TA-Pos so it does not require strict positivity — only the form it actually uses, together with whatever is derivable from the stated axioms.

### Use of `min(#z, #t)` reintroduces an operator deliberately eliminated elsewhere in the ASN
**Foundation**: T1 (LexicographicOrder) — case (i) is stated with the conjunction `k ≤ #a ∧ k ≤ #b`, not `k ≤ min(#a, #b)`; prior cycles for T2 eliminated the `min` operator for consistency (see commit `8e8f06f1`).
**ASN**: TA-Pos, postcondition proof, Case `#z ≥ k`: "Since `k ≤ #z` and `k ≤ #t`, we have `k ≤ min(#z, #t)`".
**Issue**: `min` is not defined in this ASN; the conclusion it stands in for is simply the conjunction of the two bounds, which the same sentence already supplies. Introducing `min` here is out of keeping with the elimination performed in T2 and risks reintroducing the same operator downstream proofs will then cite as if it were defined.
**What needs resolving**: TA-Pos should either define `min` explicitly (with its Depends updated) or present the bound as the bare conjunction `k ≤ #z ∧ k ≤ #t`, matching the phrasing of T1 case (i) that it immediately invokes.
