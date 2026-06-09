# Channel Assignment — ASN-0116 review-9

**Date:** 2026-06-08 21:17

## Issue 1: Incorrect index algebra in the I-NEW soundness justification
Reason: The fix is internal — it corrects a substitution using the ASN's own arithmetic fact `shift(q_k, n) = q_{k+n}` (already stated in the foundation section) and the block index bound `i ≤ J+n−1`, both present in the ASN. No design intent or implementation evidence is at stake; this is a rigor/exposition correction derivable from definitions already in the document.
