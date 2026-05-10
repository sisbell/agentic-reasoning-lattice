# Revision Categorization — ASN-0042 review-2

**Date:** 2026-03-15 20:21

## Issue 1: Account-level permanence corollary does not follow from O1a
Category: BOTH
Reason: Whether account-level prefixes can nest depends on Nelson's design intent for "forevermore" and on whether the implementation's account allocation ever produces multi-component user fields that could create nesting.
Nelson question: Did you intend that an account holder's "full control forevermore" could be superseded by delegating a sub-account with a longer user field at the same structural level, or must account-level prefixes be non-nesting?
Gregory question: Does the account allocation mechanism ever produce multi-component user fields (e.g., user=[2,3] via inc), and does `tumbleraccounteq` distinguish between a single-component account [1,0,2] and a nested multi-component account [1,0,2,3]?

## Issue 2: Effective owner function ω used outside its defined domain
Category: INTERNAL
Reason: The review provides a concrete reformulation of O5 that avoids applying ω to non-allocated tumblers, and the domain extension is a formal consistency fix derivable from the ASN's own definitions.

## Issue 3: System state axioms assumed but not stated
Category: INTERNAL
Reason: All three missing axioms (Π non-decreasing, pfx immutable, bootstrap principal) are already assumed in the ASN's own arguments — the fix is to label and formalize what the text already asserts inline.

## Issue 4: O7 formal statement uses undefined constructs
Category: INTERNAL
Reason: The narrative already specifies the intent as a conjunction of O5, O6, and recursive O7 — the fix is to replace the pseudo-formal `rights`/`≅` notation with that conjunction, requiring no external evidence.
