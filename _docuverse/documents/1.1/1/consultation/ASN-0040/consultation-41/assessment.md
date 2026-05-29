# Channel Assignment — ASN-0040 review-41

**Date:** 2026-05-28 20:10

## Issue 1: Transition framework duplicates ASN-0034 with conflicting notation
Reason: The fix is to align with or explicitly diverge from ASN-0034's existing state/vocabulary notation — a foundation document the author already cites. Determining the reuse-or-justify choice requires only the two ASNs' own content, not design intent or implementation evidence.

## Issue 2: B_type is subsumed by B10
Reason: Pure logical observation — T4 ranges over T, so B10 ⟹ B_type. Whether B_type is ever needed before B10 in the dependency chain is checkable from the ASN's own proofs. Internal.

## Issue 3: B9 quantifier meta-prose
Reason: Deletion of defensive commentary that restates what the formal statement and proof already fix. No external input needed.

## Issue 4: Repeated deferral block (Bridge1/Bridge2 + allocated-set relationship)
Reason: Editorial collapse of three forward-deferral items that no proof cites. The decision to demote or relocate is internal to the document's structure.

## Issue 5: wp section — self-acknowledged non-substantive derivation and re-explained induction
Reason: Deletion of an author-flagged non-substantive aside and a redundant induction recap already carried by §B1/§B10/§B_fin. Internal.

## Issue 6: B0a why-the-axiom prose
Reason: Removal of a justification counterfactual already conveyed by the adjacent one-line contrast. Purely editorial. Internal.

## Issue 7: Foundation definitions restated in contracts
Reason: Replace the inlined Prefix definition with a citation to the foundation's Prefix relation — derivable directly from ASN-0034 reference. Internal.
