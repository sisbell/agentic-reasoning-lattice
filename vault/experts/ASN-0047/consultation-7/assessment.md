# Revision Categorization — ASN-0047 review-7

**Date:** 2026-03-17 04:15

## Issue 1: J2/J3 formal statements are inconsistent with the composite-transition semantics
Category: INTERNAL
Reason: The inconsistency is between the formal notation (`Σ → Σ'` as composite) and the intended meaning (elementary transition properties). The fix — restating J2/J3 as elementary-transition properties — is fully derivable from the existing frame conditions and wp derivations already in the ASN.

## Issue 2: Worked example S8-depth verification is vacuous
Category: INTERNAL
Reason: The issue is that single-component V-positions make S8-depth trivially satisfied, and the fix (use multi-component V-positions or note vacuousness) requires only the S8-depth definition from ASN-0036 and the worked example's own structure. No external evidence needed.
