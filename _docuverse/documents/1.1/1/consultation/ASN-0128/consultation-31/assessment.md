# Channel Assignment — ASN-0128 review-31

**Date:** 2026-06-11 08:56

## Issue 1: Gate-first example duplicated verbatim between I1 and I6
Reason: Purely editorial — the fix is deleting the restated example at I6 and leaving the bare citation to I1, where the example already lives. No design intent or implementation evidence bears on which copy to keep.

## Issue 2: Four sections defer to DR, two sections downstream
Reason: A structural reorganization — relocating SD or stating DR earlier — that changes no claim, proof, or semantics. The note's own content fully determines both options the review offers; choosing between them is an exposition decision, not a question for either channel.

## Issue 3: R-VAL and R-C1 disagree on whether the designation check is additional
Reason: The contradiction is resolved by the ASN's own definitions: the three shipped entries are registry entries, so C0's pairwise uniqueness sweep (already counted in R-VAL) covers their pairs, and R-C1's third sentence concedes exactly this. Reframing R-C1 as a named instance of C0 — and dropping "adds three more tests" from R-VAL — follows from internal accounting; neither design intent nor implementation evidence is in play.
