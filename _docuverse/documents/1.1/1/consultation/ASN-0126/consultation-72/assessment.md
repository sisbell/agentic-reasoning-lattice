# Channel Assignment — ASN-0126 review-72

**Date:** 2026-06-09 23:01

## Issue 1: (B2) asserts a false universal as its justification
Reason: Internal. The fix restricts B2's scope to C/M/L state/transition predicates and excludes existence-of-→-successor results, handling them by lifting instead — this is a logical correction to the note's own proof structure, and the note already exhibits the lifting pattern in P5. No design intent or implementation evidence is at stake.

## Issue 2: Shape-well-definedness is re-derived after it was already given
Reason: Internal. Pure anti-bloat deletion of a redundant re-derivation paragraph whose conclusion is already given two sentences earlier ("a well-formed registry *is* a partial function … from coverage classes to entries"). Nothing external bears on it.

## Issue 3: Precondition (0) silently drops all N > 3 emissions; only the empty-from consequence is drawn
Reason: Internal. The fix is a structural acknowledgement — parallel to the existing empty-from paragraph — that (0) forecloses every N > 3 emission, with a pointer to Open Question 6. The relevant design fact (Nelson's call for "4-sets, 5-sets … n-sets") is already recorded in ASN-0043's L3, which the note inherits through ASN-0086; the remedy is explicitly out of scope, so only the in-note acknowledgement is required.
