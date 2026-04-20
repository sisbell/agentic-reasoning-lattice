# Revision Categorization — ASN-0042 review-21

**Date:** 2026-03-28 20:58



## Issue 1: O9 quantifies over all T but invokes field extraction that requires T4
Category: INTERNAL
Reason: The fix is explicitly stated in the review itself — restrict the quantifier domain to `a ∈ Σ.alloc` (where O17 provides T4) or to `T4(a)`. The proof is already correct; only the formal statement's domain needs tightening. All necessary definitions and patterns are present in the ASN.
