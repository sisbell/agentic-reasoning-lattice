# Review of ASN-0102

I checked the five frame clauses, the three-class arrangement partition (unmoved/copied/displaced), the wp(COPY, S3★) reduction, the full ExtendedReachableStateInvariants discharge, the coupling discharges (J0/J1★/J1'★, P4★, P7, P3), and all five worked examples (cross-origin, self-transclusion overlapping the displaced region, empty-subspace first insertion, append, coalescing). The mathematics is internally consistent: the last-component tiling `[1,p) ∪ [p,p+W) ∪ [p+W, n_S+W] = [1, n_S+W]` is correct at every `p ∈ [1, n_S+1]`, the snapshot-resolution discipline is sound, and the New/Old split correctly routes J1★ vs J1'★. I found no substantive logical error, no missing boundary case, and no cross-ASN reference outside the foundation set.

The note carries the `review-mode.anti-bloat` classifier. The remaining findings are meta-prose instances of the named patterns.

## REVISE

### Issue 1: Membership inventory of 𝒦 in the operation introduction
**ASN-0102, Definition of COPY**: "we add it to the system's transition vocabulary — the operation set 𝒦 (ASN-0047), whose members are the K-prefixed operations K.α, K.δ, …"
**Problem**: The clause "whose members are the K-prefixed operations K.α, K.δ, …" recites the contents of a foundation object that advances nothing about COPY. This is a use-site inventory in a structural slot.
**Required**: State that COPY is added to 𝒦 as an elementary transition; drop the member recital.

### Issue 2: Mutual cross-deferral between X10(b) and X15
**ASN-0102, X15**: "This is the indivisibility X10(b) invokes for its snapshot resolution of resolve_Σ(R) against the pre-state."
**Problem**: X10(b) forward-points to X15 ("By the atomicity of COPY (X15)"), and X15 back-points to X10(b). The back-pointer adds no reasoning to X15's derivation, which already follows from SequentialTransitionAxiom. This is the cross-reference-accretion pattern (two paragraphs deferring to each other).
**Required**: Remove the back-reference sentence; let X15 stand on its axiom derivation and let X10(b) cite it one-directionally.

### Issue 3: Defensive framing of resolution facts
**ASN-0102, The source designation and its resolution**: "Two facts about resolution are load-bearing and both come from ASN-0058."
**Problem**: "are load-bearing" is defensive justification for inclusion rather than statement of content. State the two facts and use them; their necessity is shown by the later citations, not by asserting it here.
**Required**: Drop "are load-bearing"; lead with the facts (C1: resolved addresses exist; list-count `k = Σ kᵢ`).

## OUT_OF_SCOPE

### Topic 1: COPY's effect on link discoverability (resurrection)
**Why out of scope**: A copied I-address inside some link's coverage makes that link discoverable from `d` (LP18, ASN-0098). This is link semantics and is already a foundation consequence — it need not be derived in ASN-0102.

VERDICT: REVISE
