# Channel Assignment — ASN-0071 review-39

**Date:** 2026-06-03 08:58

## Issue 1: Currency section restates one claim three to four times
Reason: Pure editorial deduplication — collapse the bookend restatements and triple "no history" gloss into a single claim plus one-line reason. No design intent or implementation evidence is at stake; the substantive `R`-vs-current distinction stays as-is.

## Issue 2: Duplicate downstream deferrals in "What we do not specify"
Reason: Mechanical removal of redundant "see the corresponding open question(s)" pointers; the Open Questions section follows immediately and "out of scope" already does the work. Fully internal.

## Issue 3: Proof roadmap and editorial ranking are meta-prose
Reason: Deleting a self-navigating roadmap sentence and an editorial ranking phrase — neither advances reasoning nor depends on design or code. Internal.

## Issue 4: PC closure step mis-attributed to trichotomy
Reason: The fix renames the closure step (well-ordering/least-disagreement-position induction) and confines the T0 citation to the per-position case split; both T0 and the proof structure are already present in the ASN, so the correction is derivable from its own content. Internal.
