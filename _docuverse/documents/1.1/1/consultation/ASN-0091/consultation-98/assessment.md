# Channel Assignment — ASN-0091 review-98

**Date:** 2026-06-04 06:37

## Issue 1: First worked example — incorrect composite-boundary witnesses
Reason: The fix is internal — the review itself supplies the correct framing (`Contains_C` ranges over all documents; use the `(·, d)` witnesses guaranteed by P4★). It requires only correctly applying ASN-0047 definitions the ASN already cites and the setup's own facts, no design intent or implementation evidence.

## Issue 2: Binary-transition-invariant enumeration omits P3
Reason: The fix is internal — the review states P3 is the synthesis P0 ∧ P1 ∧ P2 ∧ L12 and is discharged by the same RA-frame equalities. Adding it to the list is derivable from the ASN's existing discharge principle plus the cited ASN-0047 relationship.

## Issue 3: Forward-reference accretion (anti-bloat)
Reason: The fix is a pure deletion of a forward-pointing sentence; no design intent or implementation evidence is involved.
