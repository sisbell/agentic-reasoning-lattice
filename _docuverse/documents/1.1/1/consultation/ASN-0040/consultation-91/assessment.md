# Channel Assignment — ASN-0040 review-91

**Date:** 2026-05-29 02:45

## Issue 1: Spurious T10a.6 dependency and provenance editorializing in B7
Reason: Internal fix. The B7 proof's actual dependencies (T3, B6, TA5(d), TA5-SigValid) are visible in the ASN itself; removing the unused T10a.6 citation and the provenance sentence requires no design intent or implementation evidence.

## Issue 2: B10 corollary restates the s.B definition
Reason: Internal fix. The s.B definition (BaptismalRegistry: s.B ⊆ T) is already present in the ASN, so recognizing the corollary as redundant is derivable from the document alone.

## Issue 3: Redundant restatement after the B6 depth table
Reason: Internal fix. Both points in the post-table sentence are already carried by the preceding prose and the table within the same section; the redundancy is self-evident from the ASN.
