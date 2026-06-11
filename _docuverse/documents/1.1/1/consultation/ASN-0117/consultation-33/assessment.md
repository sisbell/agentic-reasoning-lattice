# Channel Assignment — ASN-0117 review-33

**Date:** 2026-06-11 01:48

## Issue 1: Triple-booked symbols `R` and `L` across foundation vocabularies
Reason: Purely notational — the fix is a renaming/qualification convention (`L_pre`/`R_suf`, `Σ.L`/`Σ.R`) applied consistently within the document; no design intent or implementation evidence bears on symbol choice.

## Issue 2: Two uncited premises in the range-decomposition chain (P4 and the wp)
Reason: The missing premises (S3★-aux for exhaustiveness, T7/SD for disjointness) are already-established foundation claims the ASN itself cites elsewhere; the fix is inserting citations at the asserting points, fully derivable from the ASN and its cited foundations.

## Issue 3: Cross-document example mis-states V-position structure
Reason: The correct structure is forced by the ASN's own model (S8a depth-2 positions, D-MIN★/D-SEQ★ canonical runs, document scoping carried by the distinct `M(d')` function); deleting the false phrase and stating `q'_k = q_k` is internal to the ASN.

## Issue 4: Open Question 1 imagines a case the precondition already excludes
Reason: The rephrasing itself is internal, but to state the totalization question accurately — whether an out-of-range span is rejected, clipped, or errors at the caller-facing layer — we should ground it in what the implementation actually does at that boundary.
Gregory question: When DELETEVSPAN receives a span that begins before the document's first arranged V-position (or otherwise falls outside the arranged extent), does udanax-green reject the request, clip the span to the arranged run, or fail — and where in the call path is that check enforced?
