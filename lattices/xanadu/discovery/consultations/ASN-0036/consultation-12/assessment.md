# Revision Categorization — ASN-0036 review-12

**Date:** 2026-03-14 21:11



## Issue 1: S8 uniqueness proof omits the derivation that sig(v) = #v
Category: INTERNAL
Reason: The fix requires inserting a derivation using definitions already present in the ASN (S8a gives zeros(v) = 0, LastSignificantPosition is defined in ASN-0034). All premises are available; the step is just missing.

## Issue 2: S5 status in properties table is mislabeled
Category: INTERNAL
Reason: The witness construction proving S5 is already in the ASN text. The fix is updating the properties table label to reflect the derivation status — purely editorial, requiring no external evidence.
