# Regional Review — ASN-0034/ActionPoint (cycle 1)

*2026-04-24 11:37*

### Inner quantifier in T0 extensionality lacks explicit ℕ carrier
**Class**: OBSERVE
**Foundation**: T0 (CarrierSetDefinition) — *Axiom:* extensionality clause.
**ASN**: T0, Axiom: `(A a, b ∈ T : #a = #b ∧ (A i : 1 ≤ i ≤ #a : aᵢ = bᵢ) : a = b)`.
**Issue**: The inner universal `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` omits the carrier `i ∈ ℕ` that T0 uses elsewhere (`(A a ∈ T, i ∈ {j ∈ ℕ : 1 ≤ j ≤ #a} :: aᵢ ∈ ℕ)`). The reader recovers the domain from the ambient index-domain convention, but the contract's quantifier style is not uniform across its own clauses.

### Use-site citations for T0's NAT dependencies list only the nonemptiness clause
**Class**: OBSERVE
**Foundation**: T0 *Depends:* NAT-closure, NAT-order.
**ASN**: T0 — depends list: "supplies `1 ∈ ℕ` for the lower bound of the nonemptiness clause `1 ≤ #a`" / "supplies the non-strict relation `≤` on ℕ appearing in the nonemptiness clause `1 ≤ #a`".
**Issue**: Both citations attribute use to the nonemptiness clause only, but `1` and `≤` also appear in the extensionality clause's inner range `1 ≤ i ≤ #a`. Dependencies are sound (the axioms do supply the symbols); only the use-site enumeration is incomplete.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 104s*
