# Channel Assignment — ASN-0077 review-76

**Date:** 2026-06-04 15:06

## Issue 1: Forward-reference duplication between "does not promise" and "Open Questions"
Reason: Pure editorial deduplication — removing forward pointers and consolidating where the deferred topics are posed requires no design intent or implementation evidence, only rearranging the ASN's own prose.

## Issue 2: WF_V conjunct (iii) is redundant
Reason: The dependency of (iii) on (v)+(vi) is already proven within the ASN (the "Empty-restriction within a non-empty document" edge case derives `u ∈ dom(M(d))` from TA-strict + the range condition), so the fix is derivable from the ASN alone.
