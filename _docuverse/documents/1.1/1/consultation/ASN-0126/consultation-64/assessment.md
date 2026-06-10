# Channel Assignment — ASN-0126 review-64

**Date:** 2026-06-09 18:57

## Issue 1: The Single-source frame argument re-derives the very intersection it commits to not re-deriving
Reason: The fix is internal — the required action is to delete the redundant final sentence, and every fact justifying that deletion is already present in the ASN: the frame argument is complete and target-independent in the two preceding sentences, R-Scope's two-branch disjunctive P-tgt is already cited by the note itself, and `a_emit`'s target-independence follows directly from the note's own statement that `a_emit` reads only the M and L components. The optional one-line replacement is likewise derivable from that same M/L-only dependence, so no design-intent or implementation evidence is needed.
