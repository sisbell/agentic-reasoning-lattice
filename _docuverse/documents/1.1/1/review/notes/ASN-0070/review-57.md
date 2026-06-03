# Review of ASN-0070

The core mathematics is sound. I checked F-canonical (existence and uniqueness), the contiguity-infrastructure characterisation, F-subspace, the inverse-image definition, and all six worked configurations against their stated postconditions — the proofs are complete, boundary cases (empty endset, empty arrangement, singleton runs, `j > 0`/`c < n` interior clip, `s_j.m = 1` left-closure) are covered, and the K.μ⁻ contraction in Configuration 4 satisfies the per-subspace strict-contraction precondition. The remaining issues are accretion, consistent with the anti-bloat classifier on this note.

## REVISE

### Issue 1: Derivation duplicated into F-multi's postcondition slot
**ASN-0070, F-multi (MultiplicityPreservation)**: Postcondition reads "By F-subspace, `subspace(v₁) = subspace_I(M(d)(v₁)) = subspace_I(a)` and `subspace(v₂) = subspace_I(M(d)(v₂)) = subspace_I(a)`, so `subspace(v₁) = subspace(v₂) = subspace_I(a)` …"
**Problem**: The postcondition slot carries a multi-step derivation, and that same F-subspace chain is then re-stated almost verbatim in the Derivation's *Implication* paragraph ("By F-subspace, `subspace(v₁) = subspace_I(M(d)(v₁)) = subspace_I(a)` … F-subspace gives `subspace(v₂) = … = S`"). The "why" appears twice — a postcondition should state the guarantee, not prove it.
**Required**: Reduce the Postcondition to the guarantee itself (writing `S := subspace_I(a)`, both `v₁, v₂ ∈ ⟦Σ_V^S⟧_V`, same subspace), and keep the F-subspace reasoning only in the Derivation.

### Issue 2: Placement-justifying narration in the F-canonical proof
**ASN-0070, F-canonical, Step 2**: "Both the existence construction (Step 3) and the uniqueness argument (Step 4) rest on a precise notion of contiguity …; we develop it once here."
**Problem**: This is meta-prose justifying where material sits rather than advancing the argument — the same shape the anti-bloat directive names for ordering-justification. The theorem intro's step-by-step roadmap ("Step 2 develops …, Step 3 exhibits …, Step 4 shows …") compounds it.
**Required**: Drop the placement-justifying clause; the contiguity definition stands on its own and is cited where used. Trim the roadmap to a single orienting sentence if retained.

## OUT_OF_SCOPE

### Topic 1: Cross-home resolution relationships and concurrency semantics
**Why out of scope**: The Open Questions (multi-home endset resolution across documents transcluding different home subsets; concurrency semantics under concurrent modification; shared-transclusion-lineage relationships) are genuinely new territory for future ASNs, correctly parked rather than half-specified here.

VERDICT: REVISE
