# Channel Assignment — ASN-0108 review-34

**Date:** 2026-06-13 04:44

## Issue 1: W5 develops the cancellation point in three passes, the first two near-verbatim
Reason: Internal. The fix removes a verbatim restatement while keeping the event-vs-outcome framing and the cancellation walk — all the material already lives in the ASN; this is pure prose deduplication touching no logic and needing no design intent or implementation evidence.

## Issue 2: The key-permanence premise is established up front, then re-derived at each use site
Reason: Internal. The permanence facts and their citations (L12/LP13/S0 for the matched-content key, value-totality for the address key) are already stated in "What κ is"; the fix only consolidates them to one establishment site and cites it from W5/W8/W9b, restructuring prose without altering any derivation.

## Issue 3: Undemonstrated "load-bearing" emphasis
Reason: Internal. The review itself notes the scoping's necessity is self-evident from the ASN's own definitions — a link matching in only one state cannot be "delivered exactly once" across the transition — so stating it plainly or showing the one-line breakage is derivable from content already present.
