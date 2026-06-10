# Channel Assignment — ASN-0127 review-5

**Date:** 2026-06-10 00:44

## Issue 1: The worked illustration uses coverage values that no endset can produce
Reason: This is a self-consistency repair against foundation results the review has already pinned down — `coverage` as the prefix-closed subtree (PrefixSpanCoverage) and sibling prefix-incomparability (T10a.2) are settled spec foundations the note already cites via ASN-0043, so rewriting the example with real spans (or declaring the shorthand plus the incomparability premise) and intersecting every slot against the full query I-set raises no design-intent or implementation question.

## Issue 2: F-IMG-SWING asserts the injective-regime motion without a witness
Reason: Purely internal — the missing injective witness is constructible directly from F-IMG and the note's own reorder-witness machinery (it already uses a transposition reorder for the non-injective case), and the review even supplies the exact witness.
