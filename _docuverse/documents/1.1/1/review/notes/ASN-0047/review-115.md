# Patch Review of ASN-0047

The patch instructions are to (a) revert L3 to ASN-0093's `NEndsetStructure` form (allowing `N ≥ 3`), (b) make K.λ's inheritance from ASN-0093 complete (signature/precondition/effect verbatim from ASN-0093), and (c) preserve the three-endset convention as default in worked examples only. The document under review still shows the *pre-patch* state at every structural site — none of the required structural changes appear in the document.

## REVISE

### Issue 1: Link definition still restricts to a triple
**ASN-0047, "Link store and extended system state" section**: "A *link value* is a triple `(F, G, Θ)` where `F, G, Θ ∈ Endset` — the *from-endset*, *to-endset*, and *type-endset* respectively."
**Problem**: This still narrows the link value to exactly three endsets, contradicting both the patch intent and ASN-0043's foundation `Link = {(e₁, e₂, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}`. The structural definition was not updated.
**Required**: Restate the Link definition matching ASN-0043's `N ≥ 3` form (e.g., `Link = {(e₁, ..., eₙ) : N ≥ 3, each eᵢ ∈ Endset}`), with the three-endset convention `(F, G, Θ)` named as a *convention* applied in worked examples rather than as a structural restriction.

### Issue 2: L3 still narrows to fixed-three-arity
**ASN-0047, "Link store and extended system state" section, L3 definition**: "**L3 (TripleEndsetStructure).** `(A a ∈ dom(Σ.L) :: Σ.L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)` Every link has exactly three endsets... This narrows ASN-0043's `N ≥ 3` arity to fixed three."
**Problem**: The patch directs reverting L3 to ASN-0093's `NEndsetStructure` form (allowing `N ≥ 3` with non-empty `e₃`), but L3 is still stated as `TripleEndsetStructure` with arity fixed at three, and the prose still describes itself as narrowing ASN-0043.
**Required**: Restate L3 in NEndsetStructure form, e.g., `(A a ∈ dom(Σ.L) :: |L(a)| ≥ 3 ∧ (A i : 1 ≤ i ≤ |L(a)| : L(a).eᵢ ∈ Endset) ∧ L(a).e₃ ≠ ∅)`, matching ASN-0093's L3, and remove the "narrows to fixed three" framing.

### Issue 3: K.λ still carries the local strengthening
**ASN-0047, "Link allocation" section**: "...and `(F, G, Θ) ∈ Link ∧ Θ ≠ ∅` — is inherited from ASN-0093's K.λ directly... The L3-narrowing to arity exactly three (with non-empty type endset `Θ`) is this ASN's local strengthening; the rest is foundation."
**Problem**: The patch directs that K.λ be fully inherited from ASN-0093 (signature, precondition, effect verbatim). The document explicitly states a local L3-narrowing is still in place, and the precondition uses `(F, G, Θ) ∈ Link ∧ Θ ≠ ∅` rather than ASN-0093's `N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅`.
**Required**: Replace the K.λ precondition with ASN-0093's verbatim form (`N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅`), remove the "L3-narrowing... local strengthening" sentence, and state that K.λ inherits in full from ASN-0093.

### Issue 4: K.λ effect uses triple notation
**ASN-0047, "Link allocation" section**: "*Effect:* `L' = L ∪ {ℓ ↦ (F, G, Θ)}`."
**Problem**: Under fully-inherited K.λ from ASN-0093 (whose effect is `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}`), this triple-only form is too narrow. The effect was not updated.
**Required**: Restate the effect as `L' = L ∪ {ℓ ↦ (e₁, …, eₙ)}` to match ASN-0093's K.λ verbatim.

### Issue 5: Verification matrix L3 row uses triple notation
**ASN-0047, "Extended reachable-state invariants" section, verification matrix L3 row**: "frame | frame | precondition: (F,G,Θ)∈Link ∧ Θ≠∅; preserved by L12 | frame | frame | frame | frame | frame"
**Problem**: The K.λ cell discharges L3 via the triple-form precondition. Under the patched (N-endset) form, this cell should discharge L3 against the N-endset precondition.
**Required**: Update the K.λ cell to cite the patched precondition (`N ≥ 3 ∧ (A i : 1 ≤ i ≤ N : eᵢ ∈ Endset) ∧ e₃ ≠ ∅`); the discharge logic itself remains valid.

### Issue 6: Proof-body L3 entry still labeled TripleEndsetStructure
**ASN-0047, "Class (a)" proof prose**: "*L3 (TripleEndsetStructure).* K.λ precondition `(F, G, Θ) ∈ Link ∧ Θ ≠ ∅` establishes L3 at the new entry..."
**Problem**: The proof entry uses the pre-patch label and precondition form; under the patched L3 it should reference the N-endset form.
**Required**: Rename to `*L3 (NEndsetStructure).*` and update the cited precondition to the N-endset form.

### Issue 7: Properties Introduced table — L3 still in "Local extensions"
**ASN-0047, "Local extensions and strengthenings of foundation properties" table**: "| L3 | TripleEndsetStructure: `(A a ∈ dom(L) :: L(a) = (F, G, Θ) where F, G, Θ ∈ Endset ∧ Θ ≠ ∅)` — local extension of ASN-0043's L3 fixing arity at exactly three; non-empty type endset preserved from foundation | ASN-0043's L3 (NEndsetStructure) admits arity ≥ 3; this ASN fixes arity at exactly three |"
**Problem**: After the patch L3 is no longer a local extension/strengthening; it should be moved to the "Inherited from foundation" table (or this row should be removed). The statement and "Foundation source" cell both still describe the now-eliminated narrowing.
**Required**: Remove L3 from "Local extensions" and add it to "Inherited from foundation" with its NEndsetStructure form, sourced to ASN-0093 (which itself inherits from ASN-0043).

### Issue 8: Properties Introduced table — K.λ row still uses triple notation
**ASN-0047, "New properties introduced by this ASN" table, K.λ row**: "...(F, G, Θ) ∈ Link with Θ ≠ ∅; effect L' = L ∪ {ℓ ↦ (F, G, Θ)}..."
**Problem**: The K.λ summary row still uses the pre-patch triple precondition and effect.
**Required**: Update the precondition and effect cells to ASN-0093's verbatim N-endset form.

VERDICT: REVISE
