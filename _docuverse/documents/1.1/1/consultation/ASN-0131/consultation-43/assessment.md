# Channel Assignment — ASN-0131 review-43

**Date:** 2026-06-14 00:22

## Issue 1: The gain/loss taxonomy under shift editing is incorrectly enumerated, and the delete case is asserted by analogy
Reason: The displacement semantics needed to enumerate the partition correctly — D-SHIFT closing the gap (delete shifts content down) and I3 leaving it (insert), both established at ASN-0082 — are already imported and stated in this note, and the review itself computes the omitted delete-below-`W` case. Completing the partition correctly or deleting the taxonomy is derivable from the ASN alone.

## Issue 2: Depth-independence overclaims coverage of a delete the foundation establishes only at depth 2
Reason: The note already records that its sole cited delete primitive (D-SHIFT) is established only at text depth `#p = 2`, and that K.μ⁻ is tail-truncation, not interior-span deletion; the required fix — restrict the claim to depth 2, conditionalize it, or flag the scope limit — is scope-honesty relative to the note's own cited foundation and needs nothing external.

## Issue 3: RE-DEF and RE-WHOLE carry inconsistent provisionality
Reason: The fix is internal bookkeeping — mark RE-DEF as encoding the provisional convention or parameterize its surfaced endset over the OQ1 choice — and does not require resolving OQ1 itself (which alone would call for Nelson's design intent on whole-endset vs. touching-spans surfacing); the equivalence of the two claims is already established in the note's Extent section.
