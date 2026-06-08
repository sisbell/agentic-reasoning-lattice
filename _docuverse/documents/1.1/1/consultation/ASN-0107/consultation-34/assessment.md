# Channel Assignment — ASN-0107 review-34

**Date:** 2026-06-08 13:19

## Issue 1: Eligibility of higher-arity links under a three-part request is unexamined
Reason: Whether a three-part request should count an N>3 link on its first three slots is a genuine semantic decision needing both the designer's intent for FROMTOTHREE and evidence of what the implementation actually does with higher-arity links.
Nelson question: When a FROMTOTHREE request meets the first three endsets of a link carrying more than three endsets, was that link intended to be counted (surplus slots ignored), or were three-part searches meant only for standard-triple links?
Gregory question: Does udanax-green's FINDNUMOFLINKSFROMTOTHREE include links of arity greater than three when their first three endsets match, or does it filter to exactly-three-endset links?

## Issue 2: Boundary-case paragraph drifts into implementation mechanics and re-treads D2
Reason: The fix is purely editorial — collapse the paragraph to the single content-anchoring guarantee and remove the restatement of D2 and the implementation-layer renumbering aside, all derivable from material already in the note (D2, A1b).

## Issue 3: CL-OWN aside in the worked example dismisses an inapplicable invariant
Reason: The fix is a straightforward deletion of an inapplicable clause while keeping the S3★ discharge; nothing beyond the note's own content is needed.
