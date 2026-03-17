# Review of ASN-0047

## REVISE

### Issue 1: K.μ~ classified as composite then called elementary
**ASN-0047, J3 and temporal decomposition table**: The completeness paragraph explicitly states "K.μ~ is a distinguished composite, not a primitive transition" and counts "Five primitive kinds — K.α, K.δ, K.μ⁺, K.μ⁻, K.ρ." Yet J3 opens with "The elementary transition K.μ~ is likewise self-sufficient," and the temporal decomposition table lists K.μ~ under the column header "Elementary transitions" alongside K.μ⁺ and K.μ⁻.

**Problem**: The ASN contradicts itself on whether K.μ~ is elementary or composite. Downstream work needs to know the primitive count — five or six — and the answer is five, but the text says both.

**Required**: J3 should say "The composite transition K.μ~" or "The distinguished composite K.μ~." The temporal decomposition table should either rename the column (e.g., "Transitions") or mark K.μ~ with a qualifier (e.g., "K.μ~ (composite)").

### Issue 2: Valid composite definition mixes transition constraints with state invariants
**ASN-0047, Definition (Valid composite transition), condition (3)**: "State invariants: the final state Σ' satisfies all system invariants: P0–P8, S2, S3, S8a, S8-depth, S8-fin, and Contains(Σ') ⊆ R'."

**Problem**: P0–P2 are transition properties — they relate Σ to Σ' (`dom(C) ⊆ dom(C')`, `E ⊆ E'`, `R ⊆ R'`) and cannot be checked by examining Σ' alone. P3 is informal ("sole locus of destructive change") and not directly checkable. P4a requires the full transition history, not just the final state. P5 is derived from P0–P2 and adds no independent constraint. Listing all of these under "the final state Σ' satisfies" is a category error in the ASN's core definition.

**Required**: Separate condition (3) into:
- (3a) Transition constraints: the composite Σ → Σ' satisfies P0, P1, P2.
- (3b) State invariants: Σ' satisfies P6, P7, P8, S2, S3, S8a, S8-depth, S8-fin, and Contains(Σ') ⊆ R'.

Drop P3, P4a, and P5 from the checklist — P3 is informal, P4a is derived from J1' by induction (proven separately), and P5 is a corollary of P0–P2 (proven separately). They are theorems of the model, not independent conditions on valid composites.

## OUT_OF_SCOPE

No items. The ASN stays within its declared scope. The open questions are appropriately deferred.

VERDICT: REVISE
