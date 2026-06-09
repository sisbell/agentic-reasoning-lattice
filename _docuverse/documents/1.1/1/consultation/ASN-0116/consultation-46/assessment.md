# Channel Assignment — ASN-0116 review-46

**Date:** 2026-06-09 16:13

## Issue 1: IP4 asserts a universal non-inclusion that fails (and contradicts its own count formula)
Reason: The fix is internal — the four-part witness decomposition and the count/content-monotonicity formulas are already present in IP4, and the correction merely conditions the non-inclusion claim on the presence of a shifted-suffix witness, reconciling it with the equality-iff-empty-new-block formula stated immediately below. No design intent or implementation evidence is required.

## Issue 2: IP3 justifies content-membership via a false whole-range inclusion
Reason: The fix is internal — the correct route (`M(d)(q_k) ∈ dom(C)` by S3★ referential integrity, since `subspace(q_k) = s_C`) uses an invariant already cited in the ASN's own ExtendedReachableStateInvariants set, and RAN already correctly scopes the range gain to the content subspace. The substitution is a localized correction derivable from the ASN itself.

## Issue 3: Provenance coupling is proved once and then re-asserted, with a forward-pointer lead-in
Reason: The fix is purely editorial/structural — dropping the redundant forward pointer and having PROV cite Clause 2 for the J0/J1★/J1'★ discharge rather than restating it, retaining only PROV's non-duplicative P7a/P7 and atomicity content. This concerns the ASN's own internal organization and needs no external channel.
