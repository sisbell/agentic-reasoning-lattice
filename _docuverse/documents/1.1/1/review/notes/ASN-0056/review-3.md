# Review of ASN-0056

## REVISE

### Issue 1: Incorrect "without loss of generality" in S11c
**ASN-0056, S11c**: "Assume without loss of generality start(α) < start(β) < reach(α) < reach(β) (the symmetric case swaps α and β)."
**Problem**: Set difference is not symmetric: swapping α and β transforms ⟦α⟧ \ ⟦β⟧ into ⟦β⟧ \ ⟦α⟧, a different problem. WLOG requires that proving one case establishes the other by renaming; that does not hold here. The ASN correctly recognizes this by giving a separate proof for the symmetric sub-case — the two constructions are genuinely different (γ takes the left piece, γ' takes the right piece) — but the WLOG framing contradicts the proof structure.
**Required**: Remove the WLOG claim. State both sub-cases as cases to prove: "We first handle start(α) < start(β) < reach(α) < reach(β), then start(β) < start(α) < reach(β) < reach(α)."

### Issue 2: S11c symmetric case less rigorous than primary case
**ASN-0056, S11c symmetric case**: The primary case explicitly verifies T12 ("The width start(β) ⊖ start(α) has a positive component at position k, so it is positive with action point k ≤ #start(α) — T12 is satisfied") and explicitly states the denotation equality ("The denotation ⟦γ⟧ = {t : start(α) ≤ t < start(β)} = ⟦α⟧ \ ⟦β⟧"). The symmetric case does neither — it verifies D1 preconditions (which implicitly cover T12) and jumps from the construction directly to "The result is exactly 1 span" without stating ⟦γ'⟧ = ⟦α⟧ \ ⟦β⟧.
**Problem**: The symmetric case requires the same verification steps as the primary case. The D1 precondition check does establish the needed facts, but the explicit T12 statement and the denotation equality chain (⟦γ'⟧ = {t : reach(β) ≤ t < reach(α)} = ⟦α⟧ \ ⟦β⟧) are elided where the primary case shows them.
**Required**: Add explicit T12 verification for γ' (width positive, action point ≤ #start(γ')), and state the denotation equality ⟦γ'⟧ = ⟦α⟧ \ ⟦β⟧ explicitly, matching the primary case's structure.

## OUT_OF_SCOPE

None.

VERDICT: REVISE
