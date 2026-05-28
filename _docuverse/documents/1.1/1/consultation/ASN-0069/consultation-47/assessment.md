# Channel Assignment — ASN-0069 review-47

**Date:** 2026-05-27 18:08

## Issue 1: V10(b) miscites V5a Corollary 2's instantiation
Reason: The fix is a labeling/citation error fully internal to this ASN — V5a Corollary 2 and V10(b) are both defined here, and the resolution is either correcting the instantiation pair or re-stating the corollary's convention. No design intent or implementation evidence is required.

## Issue 2: V8a redundant with V8b's per-transition enumeration
Reason: The fix is internal — the question is whether V8a has a distinct downstream use site within this ASN, or whether it should be folded into V8b. Both options are resolved by examining the ASN's own structure; neither Nelson's design intent nor Gregory's implementation evidence bears on the redundancy question.
