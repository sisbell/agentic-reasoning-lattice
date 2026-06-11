# Channel Assignment — ASN-0128 review-32

**Date:** 2026-06-11 09:10

## Issue 1: Wrapper wp equivalence stated without its state domain — falsified by the note's own counterexample
Reason: The fix is internal — the correct domain qualifier (SD-reachable states), the necessity/sufficiency split, and the ghost-target counterexample that forces the split are all already present in the note's own DR proof and post-contract discussion; the revision is scoping the display and the S3 "holds totally" claim to match what the proof actually establishes, requiring no design intent or implementation evidence.

## Issue 2: DR statement/proof split has accreted placement meta-prose and a restatement
Reason: Purely editorial — deleting placement justification and a content restatement, replacing them with bare cross-references. No semantic content changes, so neither channel is needed.

## Issue 3: R-VAL and R-C1 state the same claim in two sections
Reason: Purely editorial deduplication — the observation is carried once in R-C1 and R-VAL's forward sentence is deleted or reduced to a cross-reference. The claim itself is unchallenged, so no external evidence or intent is needed.
