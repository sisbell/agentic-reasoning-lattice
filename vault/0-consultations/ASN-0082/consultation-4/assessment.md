# Revision Categorization — ASN-0082 review-4

**Date:** 2026-04-09 15:21

## Issue 1: Statement Registry omits four cited foundation properties
Category: INTERNAL
Reason: The fix is mechanical — add registry rows for properties already cited by name in the ASN's own text, following the exact pattern of existing cited entries like TS1 and TS2.

## Issue 2: Informal claim that actionPoint(ℓ) = m is "not restrictive" is too strong for m > 2
Category: INTERNAL
Reason: The reviewer has already diagnosed the exact error (the argument holds for m = 2 but not m > 2) and proposed two fix approaches, both derivable from TumblerAdd's component-level semantics already defined in ASN-0034. No design-intent or implementation evidence is needed.
