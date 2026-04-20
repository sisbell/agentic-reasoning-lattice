# Revision Categorization — ASN-0084 review-10

**Date:** 2026-04-10 11:21

## Issue 1: ArrangementRearrangement definition omits other-document frame condition
Category: INTERNAL
Reason: The frame condition M'(d') = M(d') for d' ≠ d is already stated in R-FRAME-P(b) and R-FRAME-S(b) within this ASN. The fix is lifting it into the general definition or qualifying the invariant-preservation claim — no external evidence needed.

## Issue 2: R-PPERM/R-SPERM proofs incomplete on non-S subspace positions
Category: INTERNAL
Reason: The correct clause R-FRAME-P(a)/R-FRAME-S(a) is already defined in this ASN. The surjectivity gap is a trivial observation about identity on non-S positions. Both fixes are derivable from existing definitions and proof structure.

## Issue 3: Properties table — Block DEF attributes decomposition properties to individual blocks
Category: INTERNAL
Reason: The body text already correctly distinguishes individual blocks (correspondence-run condition) from block decompositions (B1–B3). The fix is aligning the table with what the body already says.

## Issue 4: Properties table — PermutationDisplacement DEF includes derived property
Category: INTERNAL
Reason: Both the definition (Δ(v) = ord(π(v)) − ord(v)) and the uniformity result (derived from R-PPERM/R-SPERM) are already present and distinguished in the body text. The fix is splitting or annotating the table entry to match.
