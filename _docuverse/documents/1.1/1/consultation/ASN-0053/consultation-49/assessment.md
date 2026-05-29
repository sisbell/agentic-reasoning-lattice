# Channel Assignment — ASN-0053 review-49

**Date:** 2026-05-28 21:23

## Issue 1: Displacement well-definedness claim omits the length condition
Reason: Internal fix. D0, D1, and D2 are already cited from ASN-0034 in this ASN's Properties table; the correction is purely a matter of citing the right property (D1 for existence with #a ≤ #b, D2 for uniqueness) instead of D0 alone. No design intent or implementation evidence is needed — the foundation properties supply the answer.

## Issue 2: D1 precondition not fully discharged in S4(c)
Reason: Internal fix. WF's proof already spells out the exact discharge (equal length excludes the prefix case, so divergence ≤ #s); the revision only needs to replicate that reasoning at the S4(c), S5, and S11c invocation sites. Fully derivable from the ASN's own content.

## Issue 3: Essay content in structural slots (anti-bloat)
Reason: Internal fix. Pure editorial compression/deletion of redundant prose that the proofs already establish; no external information required.

## Issue 4: Redundant inverse-summary paragraph
Reason: Internal fix. Removing a use-site summary that restates S4a and S3b headers; no derivation or external input needed.
