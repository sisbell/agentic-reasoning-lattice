# Revision Categorization — ASN-0084 review-7

**Date:** 2026-04-10 10:20



## Issue 1: Split B3 verification for the second piece is proof by assertion
Category: INTERNAL
Reason: The fix requires expanding an associativity argument using TS3 and the identity convention, both already defined in ASN-0034 and referenced in this ASN. All necessary definitions and tools are present in the ASN's own content.

## Issue 2: Merge B3 not verified
Category: INTERNAL
Reason: The two-case B3 proof for the merged block uses only TS3 associativity, the identity convention, and B3 of the constituent blocks — all already available within the ASN and its cited dependencies.

## Issue 3: Invariant preservation claim omits S7a, S7b, S7c
Category: INTERNAL
Reason: S7a, S7b, S7c are ASN-0036 invariants constraining dom(C) and C's structure. Since C' = C is already established, adding these to the enumeration is a straightforward bookkeeping fix requiring no external evidence.
