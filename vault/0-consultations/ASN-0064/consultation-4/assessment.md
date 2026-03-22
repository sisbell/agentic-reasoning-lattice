# Revision Categorization — ASN-0064 review-4

**Date:** 2026-03-21 19:36

## Issue 1: Overlap test operates on span denotations, not I-address sets
Category: INTERNAL
Reason: Both fix options (redefine satisfaction using resolved I-address sets, or add level-uniformity preconditions) are derivable from existing definitions in ASN-0053 and ASN-0034. The mismatch between span denotations and element-level addresses is a formal precision issue resolvable from the ASN's own content.

## Issue 2: F6b prescribes implementation mechanism instead of abstract guarantee
Category: INTERNAL
Reason: The Nelson quote already present in the ASN ("THE QUANTITY OF LINKS NOT SATISFYING A REQUEST DOES NOT IN PRINCIPLE IMPEDE SEARCH ON OTHERS") states the abstract guarantee directly. The fix is a rewording to match the quoted semantics.
