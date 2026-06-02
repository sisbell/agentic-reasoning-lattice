# Channel Assignment — ASN-0047 review-316

**Date:** 2026-06-02 02:19

## Issue 1: The k∈{1,2} freshness "structural guarantee" is overstated — it is contingent on a live-state fact
Reason: The fix is internal — it is a logical correction to how the proof characterizes the `e ∉ E` discharge, derivable from the ASN's own T10a discipline, GlobalUniqueness, and FrontierEquivalence content. Neither design intent nor implementation evidence bears on whether at-most-once enforcement reduces to the live-state check; the asymmetry reframing is a self-contained proof-prose matter.
