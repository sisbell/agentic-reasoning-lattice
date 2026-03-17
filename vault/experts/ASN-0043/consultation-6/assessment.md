# Revision Categorization — ASN-0043 review-6

**Date:** 2026-03-17 00:13



## Issue 1: L13 exclusion proof — incorrect equality in greater-depth case
Category: INTERNAL
Reason: The proof's conclusion is correct and the fix is purely mechanical — split the case analysis at `k = #b` using reasoning already present in the same-depth case directly above.

## Issue 2: L9 witness — unsupported `g ≠ a` justification
Category: INTERNAL
Reason: The fix requires only tightening the construction's choice of `g` (e.g., constraining its subspace or noting infinitude of `T`), using definitions and properties already established in this ASN and ASN-0034.
