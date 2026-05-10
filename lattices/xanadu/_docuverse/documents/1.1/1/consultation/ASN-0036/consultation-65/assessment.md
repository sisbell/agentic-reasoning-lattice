# Revision Categorization — ASN-0036 review-65

**Date:** 2026-04-09 12:54

## Issue 1: I-address ordinal shift `a + k` lacks formal definition
Category: INTERNAL
Reason: The fix requires only defining `a + k = shift(a, k)` using OrdinalShift and TumblerAdd already present in ASN-0034, with justification from S7b and S7c already in this ASN. All necessary definitions and properties are internal to the existing content.
