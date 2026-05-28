# Channel Assignment — ASN-0102 review-10

**Date:** 2026-05-28 15:30

## Issue 1: X7 mislabels the freed positions; the stated set is false for small W
Reason: This is a purely internal arithmetic/labeling error — the correct sets (`[p, n_S]` for vacated slots vs. `[p, min(n_S, p+W−1)]` for the pre-occupied portion of the target region) are both fully determined by P4, the definition's shift clause, and X16, all present in the ASN. No design intent or implementation evidence bears on the fix.

## Issue 2: X7 cites X16 as "already established" though X16 is stated later
Reason: A presentation-order defect resolvable entirely within the note — the disjointness of copied last-components `[p, p+W)` and displaced-image `[p+W, n_S+W]` is derived in X16 from the ASN's own shift semantics, so it can be inlined into X7 or reordered without consulting either channel.
