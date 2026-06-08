# Channel Assignment — ASN-0102 review-107

**Date:** 2026-06-08 05:43

## Issue 1: X15 overclaims that COPY's atomicity is "forced" — false for the append and empty-subspace cases
Reason: The fix is internal — the reviewer has already pinpointed the exact correction, and it follows entirely from the ASN's own invariants (D-CTG★/D-SEQ★, S2, ValidComposite★) and its own append/empty-subspace cases. Restricting the forcing claim to `p ≤ n_S ∧ W ≥ 1`, recasting the boundary cases as a uniformity-justified modeling choice, and restating the reverse-order obstruction (overwrite at a single key, not shared last component) are all derivable from the definition and precondition already present.
