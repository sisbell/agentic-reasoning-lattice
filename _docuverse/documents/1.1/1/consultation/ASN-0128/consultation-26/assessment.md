# Channel Assignment — ASN-0128 review-26

**Date:** 2026-06-11 07:44

## Issue 1: I0's closing claim overstates what the case analysis proves
Reason: The fix is a scope correction to the conclusion sentence — the case analysis, the argument-matching distinction (AM), and I1's suppression-loss pricing are all already in the note, and the review supplies the corrected statement. No design-intent or implementation question is open; this is restating what the note's own cases prove.

## Issue 2: I3 asserts class emptiness that does not follow
Reason: Internal logical fix — the corrected claim (the born-nullified tuple's absence from the active subset) follows directly from I2 and the active-subset semantics already cited, and the review provides the exact replacement wording. No external evidence bears on it.

## Issue 3: branch semantics stated three times (anti-bloat)
Reason: Pure editorial consolidation — the note's own commitments bullet already designates I6 as the consolidation point, so the fix is trimming the exposed-signature paragraph to its novel content (address-set slots, `enc`, widened home slot, partiality, arity-by-construction) with a pointer to I6. No semantic question for either channel.
