# Channel Assignment — ASN-0116 review-63

**Date:** 2026-06-09 22:55

## Issue 1: P7 miscategorized as a composite-boundary property
Reason: The fix is a mechanical relabeling. The correct categorization (P7 tagged INV as a per-state invariant, P7a tagged PROP as the composite-boundary property) is a structural fact about the already-cited foundation ASN-0047, and the review item itself states it explicitly — no design intent or implementation evidence is in question.

## Issue 2: Forward-reference pre-announcement in F-SUB (anti-bloat)
Reason: Purely editorial — drop the trailing forward-reference clause. The `⊆` half remains part of the stated set equality regardless, and RAN already cites F-SUB at its own use site, so the fix is internal to the ASN with nothing to verify against either channel.
