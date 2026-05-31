# Channel Assignment — ASN-0084 review-86

**Date:** 2026-05-30 17:55

## Issue 1: Verbatim-duplicated I-address licensing clause in Split and Merge
Reason: Purely editorial deduplication — moving an already-stated licensing fact (TS3 is depth-independent, already noted in the section preamble) to a single location and replacing both copies with citations. No design intent or implementation evidence is involved.

## Issue 2: "Reduction of compound shifts" restates Extended Associativity and defers its own coverage
Reason: Internal restructuring — inlining a trivial bracket-shift application into R-PIV/R-SWP and deleting a forward-reference deferral. Entirely derivable from the ASN's own Extended Associativity result.

## Issue 3: Recurring "not a foundation export / defined locally" scope-defense prose
Reason: Editorial consolidation of two redundant locality justifications for `ord` and truncated subtraction. The foundation's exports are already characterized in the ASN, so no external channel is needed.
