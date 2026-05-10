# Revision Categorization — ASN-0043 review-15

**Date:** 2026-03-22 23:13



## Issue 1: PrefixSpanCoverage exclusion proof — unspecified first divergence point
Category: INTERNAL
Reason: The fix is purely about proof precision — specifying that `j` must be the *least* divergence point, which follows from the existing definition of tumbler ordering (T1). All required definitions and reasoning are already present in the ASN.

## Issue 2: GlobalUniqueness case (iii) — unjustified ancestor claim
Category: INTERNAL
Reason: The missing justification connects comparable prefixes to allocator ancestry using T10a and TA5(d), both already cited in the proof. The fix is adding an explicit inference step from properties already stated in the ASN and its dependencies.
