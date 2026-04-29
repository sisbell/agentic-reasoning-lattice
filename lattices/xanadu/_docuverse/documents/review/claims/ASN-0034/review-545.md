# Cone Review — ASN-0034/TA-Pos (cycle 2)

*2026-04-25 17:07*

### Index-domain notation inconsistent across T0's axiom clauses
**Class**: OBSERVE
**Foundation**: (none — internal review)
**ASN**: T0 (CarrierSetDefinition). The component-projection clause writes `(A a ∈ T, i ∈ {j ∈ ℕ : 1 ≤ j ≤ #a} :: aᵢ ∈ ℕ)` with the index domain spelled out as a set-builder; the comprehension clause writes `(A i : 1 ≤ i ≤ p : tᵢ = r(i))` and the extensionality clause writes `(A i : 1 ≤ i ≤ #a : aᵢ = bᵢ)` — both leaving the underlying type of `i` implicit. The prose preamble had set the precedent that the index domain *is* `{j ∈ ℕ : 1 ≤ j ≤ #a}`.
**Issue**: A precise reader works through three different surface forms for the same index quantifier. The implicit-domain forms in extensionality and comprehension are recoverable (the `≤` bound forces `i ∈ ℕ` once one knows `≤` is the order on ℕ), but the asymmetry with the projection clause suggests the three clauses come from different drafting passes. Soundness is unaffected; uniformity would tighten the contract.

### NAT-order's depends-justification for T0 mentions `≤` but not `≥`
**Class**: OBSERVE
**Foundation**: (none — internal review)
**ASN**: T0's *Depends* bullet for NAT-order: "supplies the non-strict relation `≤` on ℕ appearing in the nonemptiness clause `1 ≤ #a`." T0's comprehension clause, however, also uses `p ≥ 1`.
**Issue**: The justification names only the symbol that occurs in the nonemptiness clause and silently passes over `≥` in the comprehension clause. NAT-order does define both `≤` and `≥`, so the dependency itself is sufficient; the justification text just under-enumerates the symbols T0 actually consumes. A reader auditing which dependencies cover which uses must spot the `≥` independently.

MISSING-REFERENCES:
NAT-carrier

VERDICT: OBSERVE

## Result

Cone review converged.

*Elapsed: 706s*
