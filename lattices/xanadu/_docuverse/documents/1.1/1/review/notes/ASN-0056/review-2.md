# Review of ASN-0056

## REVISE

### Issue 1: S11c symmetric case — denotation equality asserted without derivation
**ASN-0056, Difference for proper overlap**: "the difference ⟦α⟧ \ ⟦β⟧ = {t : reach(β) ≤ t < reach(α)}"
**Problem**: The primary case gives a one-line argument for its denotation equality ("The positions in ⟦α⟧ but not in ⟦β⟧ are those in α that precede the start of β"). The symmetric case states the analogous equality as bare fact. The derivation is short but distinct — in the primary case, positions below start(β) survive; in the symmetric case, positions at or above reach(β) survive. The two-line element-chasing argument (for t ∈ ⟦α⟧: if t < reach(β) then start(β) ≤ t so t ∈ ⟦β⟧; if t ≥ reach(β) then t ∉ ⟦β⟧) is absent.
**Required**: Add the brief derivation showing why the difference equals {t : reach(β) ≤ t < reach(α)} in the symmetric case, paralleling the primary case's reasoning.

### Issue 2: S11c symmetric case — non-emptiness not verified
**ASN-0056, Difference for proper overlap**: The primary case explicitly checks non-emptiness: "This is non-empty (start(α) < start(β) and start(α) ∈ ⟦α⟧ \ ⟦β⟧)." The symmetric case concludes "The result is exactly 1 span" without verifying non-emptiness.
**Problem**: "Exactly 1 span" is a stronger claim than "at most 1 span" — it requires showing the difference is non-empty. In the symmetric case, reach(β) witnesses this (reach(β) ∈ ⟦α⟧ since start(α) < reach(β) < reach(α); reach(β) ∉ ⟦β⟧ since reach is the exclusive upper bound). This check is absent.
**Required**: Add an explicit non-emptiness witness in the symmetric case, as the primary case does.

### Issue 3: S11d reverse containment — subset inclusion not derived
**ASN-0056, Unified difference bound table**: "(iv) Containment (⟦α⟧ ⊂ ⟦β⟧) | ∅ | 0 spans | ⟦α⟧ ⊆ ⟦β⟧ ⟹ difference empty"
**Problem**: The justification assumes ⟦α⟧ ⊆ ⟦β⟧ but does not derive it from SC(iv) symmetric conditions (start(β) ≤ start(α) ∧ reach(α) ≤ reach(β)). Every other SC case in the table is backed by a named lemma with a proof. This sub-case is justified inline with a set-theoretic tautology that skips the key step: showing the SC conditions imply the subset relation. The derivation is two lines (for t ∈ ⟦α⟧: start(β) ≤ start(α) ≤ t and t < reach(α) ≤ reach(β), so t ∈ ⟦β⟧) but it is absent.
**Required**: Either state this sub-case as a lemma (e.g., S11e) or include the two-line derivation in the S11d proof body before the table.

### Issue 4: Statement registry incomplete
**ASN-0056, Statement registry**: T12 (SpanWellDefined, ASN-0034) is cited by name in the S11c proof — "T12 is satisfied" — but is not listed in the statement registry.
**Problem**: The registry lists other cited foundation results (S11, SC, D1) but omits T12, which is explicitly invoked to justify that the constructed span γ is well-formed.
**Required**: Add T12 to the statement registry as a cited foundation result.

## OUT_OF_SCOPE

### Topic 1: Span-set difference bound
**Why out of scope**: The ASN correctly identifies this as an open question. S11d bounds single-span difference; the tight bound for |normalize(⟦Σ₁⟧ \ ⟦Σ₂⟧)| where Σ₁ and Σ₂ are normalized span-sets requires new analysis (likely O(|Σ₁| + |Σ₂|) spans), which is future work.

VERDICT: REVISE
