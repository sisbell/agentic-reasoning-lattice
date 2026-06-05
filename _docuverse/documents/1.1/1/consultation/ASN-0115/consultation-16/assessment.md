# Channel Assignment — ASN-0115 review-16

**Date:** 2026-06-05 07:25

## Issue 1: Σ is never scoped to reachable states, yet every invariant citation requires it
Reason: This is a purely internal fix derivable from the ASN's own content and the cited foundation ASNs (0047, 0086, 0098), which already establish reachable-state scoping; it requires only adding a standing precondition that Σ ranges over →*-reachable states from Σ₀, with no design-intent or implementation evidence at stake.
