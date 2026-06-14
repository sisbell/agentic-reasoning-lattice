# Channel Assignment — ASN-0131 review-24

**Date:** 2026-06-13 18:36

## Issue 1: insert/delete swing attributed to F-IMG-SWING, whose precondition the displacement does not meet
Reason: Internal. The non-monotone conclusion is already correct; the fix only re-grounds it on ASN-0082's I3/D-SHIFT (a dependency the note cites two clauses earlier) instead of the mis-applied F-IMG-SWING, and drops the unsourced extension-plus-reorder decomposition — all derivable from the note's own cited content, with no design intent or implementation behaviour in question.

## Issue 2: residual placement/forward-reference and editorial meta-prose (anti-bloat classifier active)
Reason: Internal. Pure editorial trimming — strip the "we isolate here because … below reuses it" placement annotation and the "not a defect to be engineered away" flourish; the fact and the summary clause it surrounds are already present in the note, so nothing requires design or implementation evidence.
