# Channel Assignment — ASN-0101 review-30

**Date:** 2026-06-03 16:41

## Issue 1: Worked example skips S8★ condition (c) on the content subspace
Reason: Fix is internal — the example already supplies the I-addresses (`a_1 = [d,0,1,1]`, `a_4 = [d,0,1,4]`) needed to show the two singleton runs are V-adjacent but not I-adjacent (`shift(a_1,1) = [d,0,1,2] ≠ a_4`), hence unmergeable and maximal; condition (c) discharges from the ASN's own data plus the M12 route already cited in D8.

## Issue 2: D8's general S8★(c) argument understates M12's preconditions
Reason: Fix is internal — the review itself names the full precondition set (S2, S8-fin, S8-depth, S3, S8a), and D8's Group (i) justification already establishes each at the post-state; the correction is to cite the complete set and chain the already-proven clauses rather than asserting "exactly" two.
