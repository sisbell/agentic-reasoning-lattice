# Channel Assignment — ASN-0100 review-116

**Date:** 2026-06-07 23:44

## Issue 1: Self-admitted duplicate provenance discharge
Reason: Purely an expository de-duplication — collapse the empty example's coupling paragraph to a pointer plus the case-specific delta. The general proof and the delta are both already in the ASN; no design intent or implementation evidence is needed.

## Issue 2: Essay-form narration of the I3 relationship, deferred-to from multiple sections
Reason: Internal restructuring — promote the existing "coincides with I3 on Left ∪ Shifted-right" fact to a named handle and replace the re-narrations with citations. The identification, the I3 references, and the per-region clauses are all already present in the ASN.

## Issue 3: "coincides with I3's arrangement" is informal where I3 is a relational postcondition, not an object
Reason: Derivable from the ASN's own per-region effect clauses and the cited I3 lemmas — the fix is to state the restriction-equality transport step explicitly once. No external channel is needed since I3 (ASN-0082) is already referenced and the pointwise equality follows from the ASN's own region definitions.
