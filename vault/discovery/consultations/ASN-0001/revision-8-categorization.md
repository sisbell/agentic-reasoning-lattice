# Revision Categorization — ASN-0001 review-8

**Date:** 2026-02-28 10:49

## Issue 1: TA4 formal statement is missing a necessary precondition
Category: INTERNAL
Reason: The ASN's own constructive verification already states "The inverse holds exactly only when `#w = k`." The fix is adding this established precondition to the formal statement — no external evidence needed.

## Issue 2: Reverse inverse corollary proof relies on unfixed TA4
Category: INTERNAL
Reason: Once Issue 1 corrects TA4's precondition, the corollary's precondition and proof verification follow from the ASN's own definitions and the corrected TA4. All reasoning is internal.

## Issue 3: TA3 proof claims five cases but presents four
Category: INTERNAL
Reason: This is a counting error in the proof presentation. The cases are all derived from the ASN's own definitions of divergence points; the fix is correcting the count or restructuring the case labels.

## Issue 4: Constructive definition of ⊖ does not handle `a = w`
Category: INTERNAL
Reason: TA2 already asserts well-definedness for `a = w`, and the algorithm's zeroing rule (positions before divergence get zero) extends naturally to the case where all positions precede a nonexistent divergence. The fix is adding an explicit edge-case clause from existing definitions.
