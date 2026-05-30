# Review of ASN-0058

## REVISE

### Issue 1: Defensive prose about an absent guard
**ASN-0058, Definition (Block Decomposition)**: "B1's quantifier ranges over every V-position in `dom(M(d))`, regardless of subspace; the apparent guard `v₁ ≥ 1` that one might expect is redundant — S8a (VPositionWellFormedness, ASN-0036) gives `v₁ ≥ 1` for every `v ∈ dom(M(d))` unconditionally, so no V-position is excluded."
**Problem**: B1 as written contains no `v₁ ≥ 1` guard. This sentence rebuts a guard the reader never sees — a defensive justification that imagines an excluded case rather than advancing the definition. It is reviser drift of the "explains why X is unnecessary" form. The same assurance is then restated across the document: M2 prose, the M2 table row ("all subspaces"), and the B1 table row ("every V-position in every subspace"). The reader must skip past the same negative claim three or four times.
**Required**: Delete the redundant-guard sentence. State B1 once over `dom(M(d))`; drop the repeated "regardless of/all/every subspace" emphasis from M2 and the table rows.

### Issue 2: C0a parenthetical reasons about a precondition-excluded case
**ASN-0058, C0a (PrefixConfinement)**: "(At m = 1, the vacuous range 1 ≤ j < 1 yields no confinement; indeed the action point would be 1, giving reach(σ)₁ = u₁ + ℓ₁ ≠ u₁, and ⟦σ⟧ would span multiple subspaces.)"
**Problem**: C0a's stated carrier is `m ≥ 2`, and `m ≥ 2` is established as a hard consequence of content-reference well-formedness everywhere it is used. The parenthetical develops the `m = 1` case that the precondition forbids. A paragraph imagining a case the precondition already excludes is noise the precise reader works around.
**Required**: Remove the `m = 1` parenthetical.

### Issue 3: ContentReference definition accretes necessity-justification and duplicate forward refs
**ASN-0058, Definition (ContentReference)**: "Precondition (i) is necessary: S8-depth is vacuously true for an empty subspace and does not determine a common depth, so m is well-defined only when at least one V-position exists." … "Subspace confinement … follows from C0a below; C0a's argument uses the derived `m ≥ 2` … together with the action-point analysis." … "By C0a (below), prefix confinement gives tⱼ = uⱼ …"
**Problem**: Three accretion patterns in one definition: (a) "Precondition (i) is necessary: …" is prose explaining *why the precondition is needed* rather than stating the definition; (b) the definition defers to "C0a below" twice; (c) the "bound `m ≥ 2` is a derived consequence of (i), not an independent precondition" clause is restated both here and in the ContentReference table row. The definition's meaning (a level-uniform V-span whose depth-m positions lie in `dom(M(d_s))`) is buried under justification.
**Required**: State the definition and its preconditions; move the necessity-of-(i) and m≥2-derivation prose to a single short note after C0a, where the confinement machinery actually lives, and collapse the two "C0a below" pointers into one.

### Issue 4: M6 origin-traceability deferral stated twice
**ASN-0058, M6 / Properties table M6 row**: M6's status note "(origin traceability is deferred to M16b, which depends on M16a)" is repeated verbatim in the table row "origin traceability is deferred to M16b, which depends on M16a."
**Problem**: The same downstream deferral is carried in both the claim prose and the summary table — duplicate deferral pointers to the same location.
**Required**: Keep the deferral in one slot.

## OUT_OF_SCOPE

### Topic 1: I-space discontinuity structure at canonical-boundary failures
**Why out of scope**: The first Open Question (forward gap vs. arbitrary jump at a failed merge) is genuinely new territory about I-space allocation geometry, not a gap in the block algebra established here.

### Topic 2: Lattice structure of equivalent decompositions
**Why out of scope**: Whether equivalent decompositions form a refinement lattice is a structural question beyond the existence/uniqueness results M11–M12 prove; correctly deferred.

VERDICT: REVISE
