# Channel Assignment — ASN-0117 review-37

**Date:** 2026-06-11 02:40

## Issue 1: `ord(w)` applies a V-position operator to a displacement; the foundation already names this object `w_ord`
Reason: The fix is purely notational and fully specified by the review item itself: replace `ord(w)` with `c = w₂` (equivalently `w = [0, c]`, `w_ord = [c]`), using definitions the ASN already cites (ASN-0082 OrdinalDisplacementProjection, ASN-0084 depth-2 stripping). No design-intent or implementation question bears on which notation is well-typed.
