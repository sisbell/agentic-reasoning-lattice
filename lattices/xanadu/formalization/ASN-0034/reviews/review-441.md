# Regional Review — ASN-0034/D1 (cycle 1)

*2026-04-23 05:10*

### Divergence's T1 dependency is declarative, not used in any inference
**Class**: OBSERVE
**Foundation**: Divergence — Depends on T1 (LexicographicOrder)
**ASN**: Divergence (Divergence). The Depends entry reads "T1 (LexicographicOrder) — Divergence formalizes T1's 'first divergence position'; case (i) corresponds to T1 case (i) and case (ii) (with sub-cases (ii-a)/(ii-b)) corresponds to T1 case (ii)."
**Issue**: The Divergence body and proof do not invoke any T1 postulate. The case split is driven by component structure and `#a` vs `#b`; existence uses NAT-wellorder; uniqueness uses NAT-order's trichotomy; exhaustiveness uses T3; arithmetic uses NAT-closure. T1 contributes only a naming/parallel observation, which is motivational prose rather than a logical dependency. Consumers (TumblerSub, D1) read the Depends list to know which claims are transitively available; T1 being listed here suggests an inference obligation that the body does not carry.

### Sub-case label collision between Divergence (ii-a)/(ii-b) and ZPD (α)/(β)/(γ)
**Class**: OBSERVE
**Foundation**: ZPD (ZeroPaddedDivergence) — Postconditions (Relationship to Divergence)
**ASN**: ZPD body: "In Divergence case (ii) — proper prefix, falling in sub-case (β) or (γ)" and contract: "In Divergence case (ii), under sub-case (β) or (γ)".
**Issue**: Divergence's case (ii) splits into (ii-a) and (ii-b); ZPD's own length dispatch is (α)/(β)/(γ). The ZPD text references "(β) or (γ)" to mean its own dispatch labels *while framing them inside Divergence case (ii)*. The labels align (ZPD (β) ≈ Divergence (ii-a), ZPD (γ) ≈ Divergence (ii-b)), but the sentence asks the reader to disambiguate between two overlapping label systems. TumblerSub's proof then introduces yet a third labelling — Divergence (ii-a)/(ii-b) on pair `(w, a)` — making the cross-claim reading harder than necessary.

VERDICT: OBSERVE

## Result

Regional review converged after 1 cycles.

*Elapsed: 263s*
