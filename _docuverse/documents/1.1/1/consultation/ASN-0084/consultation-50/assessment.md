# Channel Assignment — ASN-0084 review-50

**Date:** 2026-05-30 10:58

## Issue 1: ASN-0036's S8 is miscited as "SpanDecomposition"
Reason: Pure naming correction; the review supplies the correct foundation name (CorrespondenceRunPartition). Mechanical find-and-replace derivable from the ASN itself.

## Issue 2: Dangling foundation citations
Reason: Resolving these requires checking what ASN-0036/0034 actually export (sibling foundation specs), not design intent or implementation behavior. The fix is either to find the correct property name in the foundation or establish the result in-ASN — both derivable from the spec corpus without expert input.

## Issue 3: Use-site inventory — "OrdinalShift consumers under the identity extension"
Reason: Editorial reduction to load-bearing facts (TS2/TS5/OrdShiftHom extend to n=0; TS4 requires n≥1); deleting citation-bookkeeping prose is internal.

## Issue 4: R-NS "Dependencies and direction" and "Citation convention" are pure meta-prose
Reason: Deleting consumer enumeration and ordering essays leaves the lemma statement and proof intact; no semantic content at stake, fully internal.

## Issue 5: Reviser drift — prose imagining cases the preconditions exclude
Reason: Removing machinery for cases the ASN's own Width positivity and canonical-form analysis already exclude is internal cleanup; no external evidence needed.

## Issue 6: Duplicated prose
Reason: De-duplicating the two-stream argument, the S8a/S8(a) note, and the redundant surjectivity proofs is purely editorial and derivable from the ASN.

## Issue 7: Repeated deferrals to the same downstream locations / forward-reference justification
Reason: Consolidating the sufficiency-only framing and forward references to a single announcement is an internal restructuring of existing text.

## Issue 8: "Width positivity" use-site inventory
Reason: Trimming the consequence to the derived fact and deleting the consumer list and dropped-clause defense is editorial and internal.
