# Channel Assignment — ASN-0047 review-281

**Date:** 2026-06-01 19:47

## Issue 1: ExtendedReachableStateInvariants statement collapses the per-state / composite-boundary temporal distinction it is built around
Reason: The fix is internal — it requantifies the per-state class over elementary-transition-reachable states (including mid-composite intermediates) rather than composite boundaries. The preamble's temporal-scope distinction and the Class (a) per-elementary matrix already justify the stronger statement; no design intent or implementation evidence is required.

## Issue 2: The "link retention under clearance is forced" argument is stated redundantly
Reason: The fix is internal — it is a deduplication of two paragraphs asserting the identical fact (K.μ⁺ content-only + K.μ⁻ suffix-only ⟹ links retained pointwise). State once, reference elsewhere; no external channel bears on which spelling survives.

## Issue 3: P7a discharge carries defensive sub-paragraph re-deriving ValidComposite★ structure rather than advancing the claim
Reason: The fix is internal — the load-bearing S3★ + L14 + S3★-aux step is already present in the ASN; the required edit only trims the surrounding timeline narration. No design intent or implementation fact is needed to drop redundant meta-prose.
