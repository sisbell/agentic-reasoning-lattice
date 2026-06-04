# Review of ASN-0087

## REVISE

### Issue 1: Two sections redundantly enumerate the frame
**ASN-0087, "What Does Not Change" and "What MAKELINK Does Not Do"**: The first section establishes `Σ'.C = Σ.C`, no prior link modified, no other document's arrangement modified, no entity allocated, no provenance recorded. The second section re-enumerates the identical list as bullets: "No content allocation," "No content modification," "No modification of prior links," "No modification of other documents' arrangements," "No entity allocation," "No provenance recording."
**Problem**: Two sections say the same thing in different words. The frame is already captured by M-Frame and M-NoContentEffect, and discharged clause-by-clause in M-Inv-Trans. This is duplicated prose padding the structural claim.
**Required**: Collapse to one statement of the frame (or fold both into the claims table). The "no permission check" bullet is the only genuinely new content in the second list and can stand alone.

### Issue 2: "structural, not epistemic" stated twice
**ASN-0087, "Standard authoring" (Inputs) and "Reflexive Endsets"**: The Inputs paragraph asserts StandardAuthoring "is a *structural* constraint on the endset value … not an epistemic constraint on the caller's knowledge." The Reflexive Endsets section repeats: "The exclusion is structural, not epistemic (see StandardAuthoring)," then re-derives the same determinism-of-`ℓ` point.
**Problem**: The same clarification appears in two sections with a back-reference between them — meta-prose defending the same distinction twice.
**Required**: State it once at the StandardAuthoring definition; the Reflexive Endsets occurrence should simply apply it, not re-argue it.

### Issue 3: Decomposition carries a "why is it needed" justification
**ASN-0087, "Decomposition"**: "Why must MAKELINK include K.μ⁺_L? The substrate's coupling constraints (J0, J1★, J1'★ from ASN-0047) do not require it — they apply only to content-subspace allocations. But Nelson's design is explicit that a document 'consists of its contents and its out-links' …"
**Problem**: This is a paragraph explaining why a component is needed rather than what the composite does. The operative content — that K.μ⁺_L places the link in the link subspace and the ordering is forced by K.μ⁺_L's `ℓ ∈ dom(L)` precondition — is already stated in the surrounding sentences. The coupling-constraint digression and design-intent quote are justification scaffolding.
**Required**: Reduce to the load-bearing fact: MAKELINK includes K.μ⁺_L so the link is visible in its home document's arrangement; the order is forced because K.μ⁺_L requires `ℓ ∈ dom(L)`.

### Issue 4: Permanence content split across two deferring sections
**ASN-0087, "Permanence of the Recording" and "Permanence"**: The first section establishes value permanence via L12, LP13, LP3★. The second opens "The link's identity and value are permanent (L12, LP13, LP3★) — established in *Permanence of the Recording*," then restates the same three citations before adding the V-position-binding (K.μ~ fixing / K.μ⁻ removal) material, which is the only new content.
**Problem**: The re-citation of L12/LP13/LP3★ and the explicit back-reference duplicate the earlier section; only the arrangement-binding mutability discussion is new.
**Required**: Keep value permanence in one place; the second section should add only the V-position binding analysis without restating the value-permanence chain.

## OUT_OF_SCOPE

(none — the Open Questions section correctly defers not-yet-allocated-content discoverability, composite-atomicity enforcement layer, V-position movement, and permission semantics to future ASNs rather than asserting claims about them.)

The substantive content is sound: the K.λ-then-K.μ⁺_L ordering, the `ℓ ∉ ran(M(d))` derivation through S3★/S3★-aux/L14, the two-part (within/cross-subspace) S2 freshness argument, the worked example's prefix computations (a₁ vs a₂ diverge at position 8, a₁ vs ℓ at position 7 — both correct), the wp split with explicit `enabled`/membership handling, and the separately-discharged J0/J1★/J1'★ vacuity are all rigorous. The findings are anti-bloat duplication, not correctness gaps.

VERDICT: REVISE
