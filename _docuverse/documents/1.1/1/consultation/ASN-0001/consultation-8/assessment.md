# Revision Categorization — ASN-0001 review-8

**Date:** 2026-03-01 18:17

## Issue 1: TA4 formal statement is missing a necessary precondition
Category: INTERNAL
Reason: The ASN's own constructive verification explicitly demonstrates the failure case and identifies `#w = k` as the missing precondition. The fix is copying the already-established condition into the formal statement.

## Issue 2: Reverse inverse corollary proof relies on unfixed TA4
Category: INTERNAL
Reason: Once Issue 1 adds `#w = k` to TA4, the corollary's precondition and proof need only be updated to match — the proof already verifies the other preconditions and the required adjustment is mechanical.

## Issue 3: TA3 proof claims five cases but presents four
Category: INTERNAL
Reason: This is a prose counting error. The case analysis is complete; only the stated count needs correction to match the four realizable paths actually presented.

## Issue 4: Constructive definition of ⊖ does not handle `a = w`
Category: INTERNAL
Reason: The natural result (zero tumbler of length `#a`) follows from the algorithm's own zeroing rule applied to all positions, and the review itself identifies the fix. No external evidence about design intent or implementation behavior is needed.
