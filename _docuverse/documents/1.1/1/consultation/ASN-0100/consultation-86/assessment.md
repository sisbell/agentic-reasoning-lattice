# Channel Assignment — ASN-0100 review-86

**Date:** 2026-06-05 06:00

## Issue 1: S8a / S8-depth for Insertion positions is proven three times
Reason: Pure editorial restructuring — moving an existing proof to a single location and replacing the others with a deferral. The placement effect, the run-merge to `(p, a_0, n)`, and the S8a/S8-depth verification are all already present in the ASN; no design intent or implementation evidence is required.

## Issue 2: "leading … components … which are all 1" is imprecise
Reason: The fix is a notational correction fully determined by the ASN's own content — `p`'s form `[s_C, 1, …, 1, p_m]` and S8a's zero-freedom/positivity requirement are both stated in-document, so the replacement wording is derivable without Nelson or Gregory.
