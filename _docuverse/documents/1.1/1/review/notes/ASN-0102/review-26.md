# Review of ASN-0102

The operation contract, the wp(COPY, S3★) computation, the New/Old coupling split, the X16 tiling, and the invariant discharge in X14 are all sound and complete. I checked the boundary configurations (empty subspace `n_S=0`, append `p=n_S+1`, self-transclusion `Old≠∅`) and the tiling `[1,p) ∪ [p,p+W) ∪ [p+W,n_S+W]` closes correctly in every case. The within-reference non-coalescence argument in X8 is now a genuine two-step proof (V-contiguity then maximality), not a hand-wave. Cross-ASN references are all to foundation ASNs, so permitted. I found no correctness defect.

The one residual issue is cross-section duplication of load-bearing reasoning around the standalone-only restriction — flagged because this note carries the `review-mode.anti-bloat` classifier.

## REVISE

### Issue 1: The standalone-restriction justification reproduces X14's J1'★ discharge
**ASN-0102, "Amendment to ValidComposite★" (paragraph 2)**: "This restriction is not arbitrary fiat; it is forced by COPY writing provenance directly into Σ.R ... For such an address — the `Old` class of X14 ... the J1'★ discharge does not appeal to range growth; it appeals to the pair `(a, d)` already lying in `R` ... which is exactly P4★ ... Were COPY a non-initial step, its pre-state Σ would be such an intermediate state, P4★ need not hold there, and the `Old`-branch discharge would lose its ground."

**Problem**: This paragraph develops the J1'★ / `Old`-class / P4★-at-pre-state argument in essentially full detail — but that argument is *also* developed in full in X14 ("for `a ∈ Old`: ... by P4★ ... the pair `(a, d)` is *already* in `R` at the pre-state ... J1'★'s antecedent is false"). The Amendment section is previewing X14's coupling discharge to justify the restriction. The following "We therefore *defer* the mid-composite case" paragraph then restates the same mechanism a third time ("admitting COPY as a non-initial step would require either re-establishing P4★ at the intermediate pre-state or an `Old`-branch treatment that does not lean on pre-state provenance"). The same P4★-is-a-boundary-property reasoning carries three times across two sections.

**Required**: State the dependency once at the point of the restriction and point forward for the discharge — e.g., "standalone-only, because J1'★'s `Old`-branch discharge (X14) relies on P4★, which holds only at composite boundaries." Let X14 carry the full argument. The scope consequence in the deferral paragraph's second sentence (mid-composite edits must be expressed as separate standalone COPYs) is substantive and should be kept; the first sentence's restatement of the mechanism is the redundant part.

## OUT_OF_SCOPE

The four Open Questions (re-displacement of copied content, second-order referencing, time-varying views, copied identity when the allocator is unreachable) are correctly deferred — they concern later operations and reachability, not the COPY contract this note specifies.

VERDICT: REVISE
