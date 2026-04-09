# Revision Categorization — ASN-0043 review-37

**Date:** 2026-04-09 14:10



## Issue 1: GlobalUniqueness listed as "introduced" — already established in foundation
Category: INTERNAL
Reason: The fix is purely editorial — removing a redundant re-derivation and citing the existing ASN-0034 property directly. All necessary content (UniqueAddressAllocation) already exists in the foundation ASN.

## Issue 2: Missing element field depth constraint for link addresses (S7c analog)
Category: INTERNAL
Reason: The constraint follows directly from the same structural reasoning as S7c (ASN-0036) — depth ≥ 2 ensures ordinal shift preserves the subspace identifier. The worked example already assumes depth 2, and the justification is derivable from existing tumbler arithmetic properties (TumblerAdd, inc, shift) without needing Nelson's design intent or Gregory's implementation evidence.
