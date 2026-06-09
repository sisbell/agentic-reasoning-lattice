# Channel Assignment — ASN-0121 review-6

**Date:** 2026-06-09 01:32

## Issue 1: The "answer is forced" derivation does not actually force exclusion of retracted-but-satisfying links
Reason: Internal. The fix is a logical strengthening of the soundness demand (adding the `a ∈ addressable(Σ)` conjunct or a third currency demand); the ASN already cites Nelson's "not currently addressable" (4/9) for the design intent and already exhibits the `R_min`/`R_max` slack, so the unique-solution argument is derivable from the ASN's own content.

## Issue 2: Empty *link-side* endsets (e₁ = ∅ or e₂ = ∅) are a permitted boundary the ASN never addresses
Reason: The mathematical exclusion (`touch(∅, F) = false`, symmetric with FL-EMP) is internally derivable, but whether such links actually occur — making this a live boundary rather than vacuous — and how the back end indexes a link with an empty from/to endset is an evidence question for Gregory.
Gregory question: Does the back end ever store or index a link whose from- or to-endset is empty, and if so, is that empty slot simply absent from the per-slot link index (so a constrained from/to request never returns it, while a wildcard request still does)?
