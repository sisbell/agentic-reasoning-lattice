Reading through the ASN as a system, tracing every symbol in every formal contract back to its defining claim.

The proofs are structurally sound: D-SEQ's greatest-element induction is properly packaged from the from-0 base through the inductive step; D-MIN's dual least-element induction is structurally identical; D-CTG-depth's finiteness argument correctly delegates cardinality counting to D-INJ; D-INJ's successor reflection is established inline before the three surjectivity sub-cases that consume it; D-PRED grounds predecessor existence in NAT-induction rather than well-ordering; OrdShiftHom parts (a) and (b) are each proved by direct component analysis; ValidInsertionPosition correctly routes through D-SEQ to identify the last-component set as an initial segment before invoking NAT-card.

Two Depends gaps found in ValidInsertionPosition, both in the same claim.

---

### ValidInsertionPosition: `zeros` in Postcondition, T4 absent from Depends
**Class**: REVISE
**Foundation**: T4 (HierarchicalParsing, ASN-0034)
**ASN**: ValidInsertionPosition (ValidInsertionPosition), Formal Contract Depends list and Postcondition: *"Each satisfying v has v₁ = 1 as the text subspace identifier (OrdShiftHom) and zeros(v) = 0 with every component ≥ 1 (componentwise positivity)."*
**Issue**: The symbol `zeros` appears in the Postcondition of the Formal Contract. T4 (HierarchicalParsing, ASN-0034) is the defining claim for `zeros` — its definition `zeros(t) = |{i : 1 ≤ i ≤ #t ∧ tᵢ = 0}|` is required to state the postcondition and to read the component-positivity argument back as `zeros(v) = 0` via NAT-card's empty-set characterisation. The ASN's direct-citation convention, applied consistently throughout (S8a, OrdShiftHom, D-CTG, D-CTG-depth each cite T4 wherever `zeros` appears in their formal contracts), requires T4 in the Depends list wherever the symbol is written. T4 is absent from ValidInsertionPosition's Depends.
**What needs resolving**: Add T4 (HierarchicalParsing, ASN-0034) to ValidInsertionPosition's Formal Contract Depends, with an entry explaining that it supplies the `zeros` symbol and its zero-count definition, grounding the Postcondition clause `zeros(v) = 0` that the component-positivity argument discharges.

---

### ValidInsertionPosition: `V_1(d)` in Precondition and Definition, V-sub absent from Depends
**Class**: REVISE
**Foundation**: V-sub (SubspaceProjection)
**ASN**: ValidInsertionPosition (ValidInsertionPosition), Formal Contract Preconditions (*"V_1(d) ≠ ∅"*) and Definition (*"v = min(V_1(d)) or v = shift(min(V_1(d)), j)"*).
**Issue**: The symbol `V_1(d)` appears in both the Preconditions and the Definition of the Formal Contract. V-sub (SubspaceProjection) is the defining claim for `V_1(d)` — it supplies `V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = 1}` and the unfolding `v ∈ V_1(d) ⟺ v ∈ dom(Σ.M(d)) ∧ subspace(v) = 1`. The ASN's direct-citation convention, applied consistently (D-SEQ, D-MIN, D-CTG, D-CTG-depth all cite V-sub wherever `V_1(d)` appears in their formal contracts), requires V-sub in the Depends list. V-sub is absent from ValidInsertionPosition's Depends, even though `V_1(d)` is written as a first-class symbol in both the precondition guard `V_1(d) ≠ ∅` and the definition `v = min(V_1(d))`.
**What needs resolving**: Add V-sub (SubspaceProjection) to ValidInsertionPosition's Formal Contract Depends, with an entry explaining that it supplies the definition `V_1(d) = {v ∈ dom(Σ.M(d)) : subspace(v) = 1}` whose guard `V_1(d) ≠ ∅` is the claim's precondition and whose membership interpretation underlies `min(V_1(d))` in the definition.

---

VERDICT: REVISE