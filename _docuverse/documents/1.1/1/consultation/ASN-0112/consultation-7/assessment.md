# Channel Assignment — ASN-0112 review-7

**Date:** 2026-06-05 00:46

## Issue 1: Deletion's effect on the span is invoked but never derived — and one case contradicts the naive reading of V8
Reason: The deletion *mechanics* mirror V10 and are derivable from machinery already present (D-SEQ★, D-MIN★, T1, OrdinalShift, subspace ordering), but the origin-shift case — `min O(d)` jumping from `[s_C,…]` to `[s_L,1,…,1]` when content clears with links surviving — raises a real tension with Nelson's "home position is permanent" intent (V8 cites 4/19) and a realizability question the implementation must settle, since the note's style pairs each such claim with Gregory evidence.
Nelson question: Is the document's origin intended to be a permanent anchor at the content start for the document's life, or is it the minimum occupied V-position — such that fully deleting content while links survive legitimately moves the reported origin into link space?
Gregory question: When a document's entire content subspace is deleted while one or more link positions remain, does the implementation permit that state, and does the reported origin (root V-displacement) then become the link minimum `[s_L,1,…,1]` — and does deleting content in the content-maximal case retreat the reported reach/width by the corresponding ordinal steps?
