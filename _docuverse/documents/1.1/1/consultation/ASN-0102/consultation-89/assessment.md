# Channel Assignment — ASN-0102 review-89

**Date:** 2026-06-08 04:12

## Issue 1: P4★ cited at a non-boundary pre-state
Reason: The fix is internal — the review itself supplies the needed fact (P4★ is a composite-boundary property in ASN-0047, not a per-state invariant) and the two acceptable remedies (assume Σ is a reachable composite boundary, or replace the citation with the SL+P2 justification under an explicit reachability assumption). Both routes use machinery already present in the ASN (SL, P2, X15); no design-intent or implementation evidence is required.

## Issue 2: "single elementary transition changing M and R" repeated three times
Reason: Pure editorial deduplication — state the framing fact once in the Definition's amendment clause and have X14/X15 cite rather than re-establish it. Nothing about design intent or the implementation is at issue.
