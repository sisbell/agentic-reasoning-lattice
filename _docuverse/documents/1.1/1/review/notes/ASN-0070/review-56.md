# Review of ASN-0070

## REVISE

### Issue 1: Configuration 1 attributes an F-empty verification to a configuration where F-empty's hypothesis fails

**ASN-0070, "A Worked Example", first configuration verification list**: "*F-empty.* The link-subspace component `Σ_V^{s_L}` is empty — `⟦Σ_V^{s_L}⟧_V = ∅`, a regular outcome. ✓"

**Problem**: F-empty (EmptyAdmissibility) is the lemma whose precondition is the *global* condition `coverage(L(ℓ).eᵢ) ∩ ran(M(d)) = ∅` and whose postcondition is the *conjunction* `⟦Σ_V^{s_C}⟧_V = ∅ ∧ ⟦Σ_V^{s_L}⟧_V = ∅`. In Configuration 1, `coverage(L(ℓ).e₁) ∩ ran(M(d)) ⊇ {a₁+1, a₁+2} ≠ ∅`, and `Σ_V^{s_C}` is non-empty. So neither F-empty's precondition nor its postcondition holds in Configuration 1; the line checkmarks a lemma against a scenario it does not cover. The phenomenon actually shown — one subspace component empty while the other is populated — is *partial* emptiness, which F-empty does not state. F-empty is genuinely exercised only in Configuration 3 (no reach), where both components are empty. This is a "verification by checkmark" against an inapplicable lemma.

**Required**: Relabel the Configuration 1 line so it does not claim to verify F-empty — e.g., state it illustrates that an individual subspace component may be empty (admissible by the V-Restricted Denotation convention) — and reserve the F-empty checkmark for Configuration 3, where the global-emptiness hypothesis actually holds.

## OUT_OF_SCOPE

None.

VERDICT: REVISE

The note is otherwise rigorous: boundary coverage is strong (vacuous subspace, empty result, multiplicity, cross-subspace straddle, interior-offset clip are each exercised by a distinct configuration), the canonical-form existence/uniqueness proof develops its contiguity infrastructure explicitly rather than by "similarly," and the weakest-precondition analysis establishes minimality. The named forward-reference accretion patterns (axiom-rationale sub-paragraphs, repeated downstream deferrals, ordering-justification prose, consumer enumerations) are essentially absent — consistent with the recent prose-trim commits. The single defect above is the only item blocking convergence.
