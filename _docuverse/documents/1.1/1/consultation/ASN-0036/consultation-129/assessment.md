# Channel Assignment — ASN-0036 review-129

**Date:** 2026-05-28 23:15

## Issue 1: S8 run-corollary asserted in the summary table but never derived
Reason: Internal — the fix is editorial bookkeeping between the S8 proof (singleton-only), its contract's *Depends* list, and the summary table. The contract itself concedes S7b/S7c/ShiftPreservation are not used by the existence claim, so resolution is fully derivable from the ASN's own content.

## Issue 2: Repeated use-site deferrals to S7b ("rationale at S7b")
Reason: Internal — anti-bloat cleanup of duplicated back-pointers across S7a/S7d/S7 *Depends* lines. The T10a.4 role is already stated; consolidating or inlining it requires no external design intent or implementation evidence.

## Issue 3: Coalescing deferral repeated in three locations
Reason: Internal — choosing a single home (Open Questions) for the coalescing deferral and removing the two upstream restatements is a pure editorial decision within the ASN's existing structure.
