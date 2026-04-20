# Revision Categorization — ASN-0042 review-10

**Date:** 2026-03-15 23:02



## Issue 1: `delegated` definition does not enforce O1a; O15 references only `delegated`
Category: INTERNAL
Reason: The fix is purely structural — reorganizing where the `zeros(pfx(π')) ≤ 1` constraint lives within already-stated definitions. Both the constraint (O1a) and the mechanism (O7) are already present in the ASN; the issue is co-location, not missing evidence.
