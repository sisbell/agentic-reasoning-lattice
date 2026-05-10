# Revision Categorization — ASN-0084 review-16

**Date:** 2026-04-10 13:22



## Issue 1: CanonicalBlockDecomposition uniqueness proof uses undefined operations
Category: INTERNAL
Reason: The review identifies informal shorthand (I-address subtraction, negative shifts) in the uniqueness proof and provides explicit reformulations using only forward-defined operations already available in the ASN's own vocabulary (OrdinalShift, TS3, B3). The fix is fully derivable from existing definitions.
