# Cone Review — ASN-0034/TumblerAdd (cycle 1)

*2026-04-25 19:21*

### TumblerAdd Definition slot omits result length
**Class**: OBSERVE
**Foundation**: TumblerAdd
**ASN**: TumblerAdd *Formal Contract:* "*Definition:* k = actionPoint(w); rᵢ = aᵢ if i < k; rₖ = aₖ + wₖ; rᵢ = wᵢ if i > k"
**Issue**: The Definition specifies the components rᵢ but not the index range over which i ranges, nor the length of `a ⊕ w`. The body establishes p = n = #w, and the postcondition `#(a ⊕ w) = #w` pins it down, but a reader of the contract slot alone cannot determine the result's length without consulting the body. The Definition is the natural place for "rᵢ for 1 ≤ i ≤ #w" or an explicit length statement.

### Transitivity case `k₁ < k₂`: existence-of-`cₖ₁` argument is circular
**Class**: OBSERVE
**Foundation**: T1 part (c) Transitivity
**ASN**: "If `a < b` via T1(i): `aₖ₁ < bₖ₁ = cₖ₁` with `k₁ ≤ m`, and the existence of `cₖ₁` gives `k₁ ≤ p`"
**Issue**: "Existence of cₖ₁ gives k₁ ≤ p" is essentially a tautology — cₖ₁ being a referenced component already presupposes k₁ ≤ p. The actual evidence is that `b < c` (via either T1(i) or T1(ii)) forces k₂ ≤ p, and k₁ < k₂ then yields k₁ < p. Same loose justification recurs for the T1(ii) sub-branch ("`cₖ₁` exists, so `m + 1 ≤ p`"). The conclusion is correct; the chain of reasoning could be tightened.

### T0 comprehension clause: inner index quantifier omits `i ∈ ℕ`
**Class**: OBSERVE
**Foundation**: T0
**ASN**: T0 *Formal Contract:* the comprehension clause `(A p ∈ ℕ : p ≥ 1 : (A r : {j ∈ ℕ : 1 ≤ j ≤ p} → ℕ :: (E t ∈ T :: #t = p ∧ (A i : 1 ≤ i ≤ p : tᵢ = r(i)))))`
**Issue**: The innermost `(A i : 1 ≤ i ≤ p : tᵢ = r(i))` does not state the carrier from which `i` is drawn. The companion extensionality clause has the same shape `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)`. Other clauses explicitly write `i ∈ {j ∈ ℕ : 1 ≤ j ≤ #a}` (component-projection clause). The asymmetry is harmless — `i` must lie in `dom(r) = {j ∈ ℕ : 1 ≤ j ≤ p}` for `r(i)` to be defined — but the precise reader has to reconstruct that carrier.

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 548s*
