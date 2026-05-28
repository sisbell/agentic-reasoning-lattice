# Channel Assignment — ASN-0102 review-9

**Date:** 2026-05-28 15:24

## Issue 1: X7 overstates that the entire freed range held content pre-state
Reason: The fix is purely internal arithmetic over the ASN's own definitions — P4 fixes the pre-state population `[1, n_S]` and X16's tiling already establishes the copied/displaced-image disjointness that carries the no-overwrite conclusion. No design intent or implementation evidence is at stake; only the stated justification must be corrected to `[p, min(n_S, p+W−1)]`.
