# Channel Assignment — ASN-0119 review-28

**Date:** 2026-06-10 04:01

## Issue 1: The P4a discharge credits an ingredient it does not use and carries a redundant witness clause
Reason: Internal. The review already supplies the corrected argument, and every fact it rests on is in the ASN: P4a is described as trace-quantified, the witness Σ_k is an *earlier* trace state in the prefix, and appending the REARRANGE step cannot touch it — so witness persistence follows from `R' = R` + P4a@Σ alone. Trimming the over-credited content-subspace-range invariance (and the redundant "Σ itself an admissible witness" clause) is a matter of reading the proof's own dependency structure, requiring neither design intent nor implementation evidence.

## Issue 2: RA7c's region enumeration is narrower than the R-COMM region list it relies on
Reason: Internal. The body already cites R-COMM's five-region list (including the non-S subspace) and establishes that the link subspace is carried untouched in the frame (RA6), so its run structure is trivially preserved. Aligning RA7c's parenthetical with that list, or defining "exterior" as the union of all frozen regions, is internal-consistency work derivable from the note's own content.

## Issue 3: Meta-prose in the claims table
Reason: Internal. Pure editorial removal of a structural-description clause; the operation's content and its import provenance are already conveyed by the row's statement and the "imported (ASN-0084)" status column.
