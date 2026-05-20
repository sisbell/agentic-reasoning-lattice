# Review of ASN-0047

## REVISE

### Issue 1: Transcluded replacement implicit precondition

**ASN-0047, "Elementary transitions" section, paragraph beginning "Replacement — changing which I-address a V-position maps to, takes two forms by composite shape"**:

> "*Transcluded replacement* (two-step, K.μ⁻ + K.μ⁺): ... No K.α, no K.ρ: the new I-address is already in dom(C), and any provenance pairs `(a, d)` that did not already exist in R for the newly arranged addresses are recorded by J1★ at the composite boundary."

**Problem**: The two-step composite has an implicit precondition that is never stated. Without K.ρ in the composite, `R' = R`. For J1★ to hold at the composite boundary, every `a ∈ ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C})` must satisfy `(a, d) ∈ R'`. With `R' = R`, this requires `(a, d) ∈ R` at the pre-state.

The phrase "recorded by J1★ at the composite boundary" misuses the constraint as if it were an effect. J1★ flags a requirement; it does not add to R. If `(a, d) ∉ R` for a newly arranged transcluded address, the two-step composite genuinely violates J1★ at the boundary — it is not "recorded" by anything. The text presents the two-step form as universally applicable for "transcluded replacement," obscuring this gap.

The four-step "fresh-content replacement" handles its J1★ obligation via the K.ρ step. The two-step form has no such step, yet J1★ may still fire on a transcluded I-address that has never previously been arranged in `d`.

**Required**: Either (a) state explicitly that the two-step form requires `(a, d) ∈ R` for every `a ∈ ran(M'(d)|_{s_C}) \ ran(M(d)|_{s_C})` (i.e., the transcluded address must have prior provenance for `d`, typically from an earlier insertion-deletion cycle); or (b) add a third "transclusion with new-provenance" form K.μ⁻ + K.μ⁺ + K.ρ for first-time transclusion of `a` into `d`, distinct from both named forms. The current text reads as if the two-step form covers all transclusion, which is unsound when `(a, d) ∉ R`.

### Issue 2: S4 matrix row conflates content-S4 with entity/link distinctness

**ASN-0047, "ExtendedReachableStateInvariants" section, verification matrix, S4 row**:

> "S4 | T10a GlobalUniqueness on A_C(origin(a)) (subsequent) or SubAllocatorAxiom.FirstEmission (first) | T10a GlobalUniqueness on parent allocator (¬IsNode); NodeUniqueAllocation (IsNode) | SubAllocatorAxiom.FirstEmission (first) or T10a GlobalUniqueness on A_L(d) (subsequent) | frame (no new addresses) | ..."

**Problem**: S4 (per ASN-0036) is stated strictly over `dom(C)`: "a₁, a₂ ∈ dom(C) produced by distinct allocation events ... a₁ ≠ a₂". K.δ does not touch dom(C); K.λ does not touch dom(C). Under both, S4 is preserved trivially by frame on C. The matrix cells under K.δ and K.λ instead supply distinctness arguments for entities and link addresses respectively — useful properties, but not S4.

The matrix label silently broadens S4 from content-only to "allocator-discipline-derived distinctness across all kinds." This is a labeling defect, not an error in the underlying logic, but it obscures what is actually being verified.

**Required**: Either restrict the S4 row to K.α (with all other cells reading "frame") and split out a separately-named row for entity-distinctness (under K.δ) and link-distinctness (under K.λ); or introduce an explicit "generalized S4" symbol covering all three address kinds and use it consistently in both the matrix and the body prose. As written, a reader cross-referencing ASN-0036 will not recognize the S4 row's cells as S4 verifications.

## OUT_OF_SCOPE

None.

META: ASN stays at the abstract state-machine level (state components, transitions, invariants); no implementation drift detected.

VERDICT: REVISE
