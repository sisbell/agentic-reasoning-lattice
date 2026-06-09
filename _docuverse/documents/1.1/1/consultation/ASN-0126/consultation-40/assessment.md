# Channel Assignment — ASN-0126 review-40

**Date:** 2026-06-09 10:41

## Issue 1: "R is registered Binary" contradicts Open Question 4 and C0
Reason: Internal — the note already inherits from ASN-0086 that Nullify/retraction is core substrate vocabulary, so the fix (commit R to C0, or restate Single-source conditionally) is a framework-consistency decision derivable from the note's own commitments and OQ4 text. No external channel needed.

## Issue 2: The `idem` field is dead state threaded through four sites (anti-bloat)
Reason: Internal editorial trim. The note itself states no predicate/gate/operation reads `idem`; confining it to the OQ1 pointer and deleting the P2 sentence requires only the note's own content.

## Issue 3: The gate-enables / landing-may-fail distinction is re-explained redundantly (anti-bloat)
Reason: Internal editorial deduplication. The four restatements and the single demonstration all already exist in the note; cutting the redundant prose needs no external evidence.

## Issue 4: Infinite-coverage derivation argues against an unproposed design
Reason: Internal editorial trim. The divergence between span-count and coverage is already witnessed by the note's unit-depth example; deleting the rejected-alternative derivation is derivable from the note alone.
