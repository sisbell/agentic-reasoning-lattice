# Revision Categorization — ASN-0042 review-20

**Date:** 2026-03-28 20:40



## Issue 1: `nodeField` notation reinvents foundation definition
Category: INTERNAL
Reason: The fix is purely notational — replacing `nodeField(a)` with the already-defined `N(a)` from ASN-0034 T6, and rewriting `acct(a)` in terms of `N(t)` and `U(t)`. All required definitions are present in the foundation ASN.

## Issue 2: O10 existence proof omits the empty sub-delegate boundary case
Category: INTERNAL
Reason: Both gaps are mathematical — handling the empty-set edge case for the maximum argument, and showing the `inc` construction for the zeros=1 case. The needed tools (T0a, TA5/inc) are already defined in the tumbler algebra foundation; the fix requires only tightening the proof's case analysis using existing definitions.
