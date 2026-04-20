# Revision Categorization — ASN-0081 review-9

**Date:** 2026-04-09 20:38

## Issue 1: Missing order-equivalence postcondition for ord/vpos
Category: INTERNAL
Reason: The fix requires stating a property that follows directly from T1 (lexicographic ordering) applied to tuples sharing a first component — all definitions and reasoning are already present in ASN-0034 and this ASN.
