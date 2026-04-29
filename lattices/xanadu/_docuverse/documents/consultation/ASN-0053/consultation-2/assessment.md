# Revision Categorization — ASN-0053 review-2

**Date:** 2026-03-18 17:39

## Issue 1: S1 and S3 preconditions omit level-uniformity
Category: INTERNAL
Reason: The correct precondition is already used in S4 and S8 within the same ASN. The fix is aligning S1 and S3 to match the formulation the document already uses elsewhere.

## Issue 2: Round-trip identity used four times, never stated
Category: INTERNAL
Reason: The reach-function section already contains the core derivation; the fix is promoting it to a named lemma. All ingredients come from ASN-0034's TumblerAdd/TumblerSubtract definitions and reasoning already present in the ASN.

## Issue 3: S5 action-point precondition is unnecessarily strong and proof has a gap
Category: INTERNAL
Reason: The reviewer's preferred fix (option b) uses associativity from ASN-0034, a short left-cancellation proof derivable from TumblerAdd's definition, and the round-trip from Issue 2. All ingredients are internal to the ASN and its dependency.

## Issue 4: Properties table uses span-set symbol for span properties
Category: INTERNAL
Reason: Notation typo — the body text already uses σ for spans consistently; the table entries just need to match.
