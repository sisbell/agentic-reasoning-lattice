# Channel Assignment — ASN-0047 review-285

**Date:** 2026-06-01 20:31

## Issue 1: Two differently-named results state the same range-invariance fact
Reason: Purely editorial — both K.μ~-RANGE and "K.μ~ range-invariance" derive `ran(M'(d)) = ran(M(d))` from facts already in the ASN; collapsing them and folding in the per-position clarification requires no design intent or implementation evidence.

## Issue 2: `subspace_I` misattributed to ASN-0036 and defined twice in the Notation section
Reason: The correct source (ASN-0043's SubspaceI definition) and the duplication are both determinable from the project's own ASN corpus, which the review itself already states; fixing the citation and removing the duplicate paragraph is internal.

## Issue 3: "Link V-position permanence" mixes essay/implementation prose into a structural slot and re-derives clause (iii) off-site
Reason: The fix is to trim and relocate prose down to the load-bearing clause-(v) statement; since permanence is already discharged by L12 and clause (iii) is defined above, no new Nelson/Gregory input is needed to remove accreted material.
