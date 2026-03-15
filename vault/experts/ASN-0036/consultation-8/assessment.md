# Revision Categorization — ASN-0036 review-8

**Date:** 2026-03-14 17:46



## Issue 1: S5 within-document sharing claim unproven
Category: INTERNAL
Reason: The fix is constructing an additional witness using the same technique already in the proof — just with multiple V-positions in one document instead of one V-position per document. All definitions needed (S2, S3) are already present.

## Issue 2: S8 partition proof restricted to depth 2
Category: INTERNAL
Reason: This is a proof generalization issue. The ASN already contains S8-depth and the tumbler ordering properties (T1, T5 from ASN-0034) needed to argue disjointness at arbitrary uniform depth. The fix is either generalizing the interval argument or strengthening S8-depth to depth 2 based on evidence already cited in the ASN.
