# Channel Assignment — ASN-0108 review-7

**Date:** 2026-06-05 04:37

## Issue 1: W5's necessity is asserted abstractly but its failure mode is never exhibited
Reason: The fix is internal — the mechanism (a content-position edit moving one endpoint past another, permuting tail order so a tail link's key drops below the cursor's) is already stated in W5's own discussion and the content-position key's reordering behavior is already imported into the ASN; the required walk is a numeric instantiation of facts already present.

## Issue 2: W6's blind spot is described but not walked
Reason: The fix is internal — W6 already establishes that under a content-position key a new link's endpoint may sort below κ(c) (`κ(a_new) <_K κ(c)`, so `a_new ∉ After(c, Σ')`); the required walk merely instantiates this stated mechanism with fixed `Match`, `N`, and a concrete sub-cursor endpoint position, needing no design intent or new implementation evidence.
