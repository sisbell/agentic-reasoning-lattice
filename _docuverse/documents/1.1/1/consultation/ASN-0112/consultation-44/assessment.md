# Channel Assignment — ASN-0112 review-44

**Date:** 2026-06-08 12:15

## Issue 1: V3 pre-empts its own proof with a defensive caveat
Reason: Internal — the fix is deleting a redundant defensive sentence whose witness (`max O(d).0`) and conclusion are already derived in the proof's closing sentence. No design intent or implementation evidence is needed to remove duplicated prose.

## Issue 2: V9 cites the content-only D-SEQ for a generic-subspace claim
Reason: Internal — the ASN already defines both D-SEQ (content instance) and D-SEQ★ (per-subspace), and V9's conclusion rests only on `O(d)`-invariance stated in the same sentence. Correcting the citation or dropping the parenthetical is derivable from the note's own conventions.
