# Review of ASN-0070

This is a thorough, heavily-derived ASN. The central inverse-image relation (F0) is clean, the canonical-form uniqueness proof (F-canonical) now handles the consecutive-vs-pairwise distinction correctly, and the five worked configurations exercise the soundness/completeness/empty/multiplicity/link-subspace branches end-to-end. The proofs I checked in detail — the Characterisation induction, Step 1's two cases, the left/right inter-component closure, F-subspace's biconditional — are sound. The remaining issues are localized.

## REVISE

### Issue 1: F-multi declares its admissibility half but omits S5 from Depends

**ASN-0070, F-multi (MultiplicityPreservation), Depends**: "Definition of `R(d, e)` (F0); postcondition of follow (F1); F-subspace (this ASN); S3★-aux (SubspaceExhaustiveness, ASN-0047)."

**Problem**: The Derivation explicitly splits F-multi into an *implication* half and a *structural admissibility* half, and the latter invokes "S5 (UnrestrictedSharing, ASN-0036)" to establish that the hypothesis (`v₁ ≠ v₂`, `M(d)(v₁) = M(d)(v₂)`) is not vacuous. The closing sentence states "F-multi names both together because operational interest in multiplicity preservation depends on both." If both halves are part of the claim, S5 is a premise of the claim — but it is absent from the Depends field. Either the Depends is incomplete or the "names both together" framing overstates the claim's scope. As written they are inconsistent.

**Required**: Add S5 (UnrestrictedSharing, ASN-0036) to F-multi's Depends list (and to the Claims-Introduced table row, which likewise mentions S5 only in prose), or restate F-multi so the admissibility half is explicitly outside the claim's formal content.

### Issue 2: An "Open Question" is already answered definitively in the body

**ASN-0070, Open Questions**: "What must the system promise about ordering of the returned canonical span-set — is the canonical V-tumbler order under T1 required, or is any equivalent denotation admissible?"

**Problem**: The body resolves this. CanonicalForm clause (ii) fixes the ordering (normalised per S9, sorted by start under T1, N1), and the Result-Form section states plainly: "We do not commit the operation's postcondition to canonical form … An implementation may return any representationally equivalent form." So the operation requires *any equivalent denotation*, and the canonical span-set ordering *is* T1-sorted. Listing this as open contradicts decisions the ASN has already made and recorded.

**Required**: Remove the question, or sharpen it so it asks something the body does not settle (e.g., whether a *downstream/system-level* contract — citation, archival reference — must mandate canonical form, as distinct from what `follow` itself promises).

## OUT_OF_SCOPE

### Topic 1: Partial-reach reporting, concurrency semantics, cross-lineage resolution relationships

**Why out of scope**: The remaining Open Questions (which I-addresses failed to resolve, concurrency guarantees, transclusion-lineage relationships between `follow(ℓ,d,i)` and `follow(ℓ,d',i)`, content-retrieval coupling) are genuinely new territory — they concern reader-facing reporting, concurrency models, and version-correspondence operations not yet specified. These belong in future ASNs, not as revisions here.

VERDICT: REVISE
