# Review of ASN-0113

The technical content is sound. I worked the proofs of W3, W4, W5 (both directions), W10, W11, W16, and W20; each holds. The T5-confinement step in W4/W10 is correctly invoked (both bounds share the prefix, lexicographic-vs-componentwise is properly disclaimed), the W5 forward construction correctly anchors at the run's *actual* minimum rather than the canonical one, and the depth-3 worked instance genuinely exercises the interior-position exclusion that the m=2 instances leave vacuous. Edge cases (empty/both, one-member, degenerate m=2) are all covered. Depth requirements are met: non-trivial wp (W20), derived consequences (W12, W16), concrete worked instances. No cross-ASN violations — every cited claim is from a foundation ASN.

This note carries the `review-mode.anti-bloat` classifier. The residual findings are editorial meta-prose, not rigor gaps.

## REVISE

### Issue 1: Defensive provenance clause in the W9 derivation
**ASN-0113, "The operation: one span per occupied subspace" (W9 derivation)**: "There is therefore no third subspace in which document content could reside, hence no third member can ever arise in the span-set — the report is intrinsically two-kinded, grounded in the foundation rather than in implementation behavior."
**Problem**: The substantive claim (no third member, two-kinded) is complete at "no third member can ever arise." The trailing "grounded in the foundation rather than in implementation behavior" defends the *epistemic provenance* of the claim rather than advancing it — the reader must skip past it to reach the next claim.
**Required**: End the derivation at the substantive conclusion; drop the provenance flourish.

### Issue 2: Comparative editorializing in W18's faithfulness argument
**ASN-0113, "Permanence of the report" (W18, "The link extent counts links")**: "The content side carries the analogous guarantee *more cheaply* and asymmetrically: ... so `n_{s_C}(d) = |V_{s_C}(d)|` is already the number of content positions with no ownership or uniqueness premise to discharge — the link side needs CL-OWN and CL-UNIQ where the content side needs only functionality."
**Problem**: The premise-attribution (content faithful by S2/S3★; links by CL-OWN + CL-UNIQ) is genuine content, but the comparative framing ("more cheaply," "asymmetrically," "where the content side needs only functionality") is editorial commentary on the relative cost of premises that adds nothing to the faithfulness claim the section is establishing.
**Required**: Retain the premise-attribution for each subspace; trim the asymmetry editorializing.

## OUT_OF_SCOPE

None beyond the topics the Scope section already excludes; the note correctly confines itself to the per-subspace extent query and routes the single-overall-extent, transclusion, and version-fork questions to Open Questions rather than specifying them here.

VERDICT: REVISE
