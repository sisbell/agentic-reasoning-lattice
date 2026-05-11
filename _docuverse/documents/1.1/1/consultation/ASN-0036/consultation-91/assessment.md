# Channel Assignment — ASN-0036 review-91

**Date:** 2026-05-11 04:20

## Issue 1: D-SEQ Step 3 does not explicitly verify that the constructed intermediate w satisfies S8a
Reason: The fix is internal — S8a's definition, the construction of w with k > k₁ ≥ 1, and the parallel S8a verification in D-CTG-depth are all already in the ASN.

## Issue 2: D-SEQ Step 1 (m = 2 case) does not justify why component 1 equals 1
Reason: The fix is internal — the definition V_1(d) = {v ∈ dom(M(d)) : subspace(v) = 1} and subspace(v) = v₁ are both already established in the ASN, as is D-MIN.
