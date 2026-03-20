# Review of ASN-0056

## REVISE

(none)

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound
**Why out of scope**: The ASN correctly identifies this as an open question. The tight bound on |normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)| for normalized span-sets Σ₁, Σ₂ is new territory requiring its own analysis (likely O(|Σ₁| + |Σ₂|) spans). Not an error in this ASN.

---

Notes on what was checked:

**S11a**: Disjoint intersection implies A \ B = A. Correct and trivial. Worked example verifies separation.

**S11b**: A \ A = ∅. Correct and trivial.

**S11c Case 1** (start(α) < start(β) < reach(α) < reach(β)): The set characterization ⟦α⟧ \ ⟦β⟧ = {t : start(α) ≤ t < start(β)} is correct — for t ∈ ⟦α⟧ with t ≥ start(β), we get t < reach(α) < reach(β), so t ∈ ⟦β⟧. The span construction γ = (start(α), start(β) ⊖ start(α)) has all preconditions verified: D1 applies (divergence type (i), equal lengths), T12 satisfied (action point at divergence ≤ #start(α)), level-uniform (#width = #start). Worked example arithmetic confirmed.

**S11c Case 2** (start(β) < start(α) < reach(β) < reach(α)): Element-chasing derivation is explicit — t < reach(β) forces t ∈ ⟦β⟧ via start(β) < start(α) ≤ t. The span γ' = (reach(β), reach(α) ⊖ reach(β)) has D1 preconditions verified through the level-uniformity chain #reach(β) = #start(β) = #start(α) = #reach(α). T12 and level-uniformity checked.

**S11d**: All five SC cases are present. The reverse-containment sub-case of SC(iv) is derived inline with a correct element-chase. The summary table is consistent with the component lemmas. The bound of 2 is tight (witnessed by S11 case (c) from ASN-0053).

**Foundation consistency**: All citations (D1, T12, SC, S11) are to foundation ASNs. No reinvented notation. The level-uniform + level_compat preconditions match S1's pattern from ASN-0053.

VERDICT: CONVERGED
