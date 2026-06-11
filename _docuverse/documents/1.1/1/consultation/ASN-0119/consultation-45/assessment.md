# Channel Assignment — ASN-0119 review-45

**Date:** 2026-06-11 02:34

## Issue 1: π presented as "defined by" an equation that does not determine it
Reason: The fix is internal — the review identifies the correct formulation already present in the ASN's own claims table (π as the cut-point-induced bijection of R-PPERM/R-SPERM), and the revision is a wording alignment of body and RA1 with that entry.

## Issue 2: Worked examples and RA8b silently assume the I-addresses are pairwise distinct
Reason: The fix is internal — the missing premise (distinct allocation events, hence pairwise-distinct addresses by S4/GlobalUniqueness) is a one-sentence scenario stipulation drawn from invariants the note already cites, requiring neither design intent nor implementation evidence.

## Issue 3: Universally quantified obligations discharged for the rearranged document only
Reason: The fix is internal — the closure fact (RA9, `M'(d') = M(d')` for all `d' ≠ d`) is already a claim of the note; the revision only adds the sentence applying it to the universally quantified obligations.

## Issue 4: Undefined subtraction on cut positions and V-positions
Reason: The fix is internal — the note's own adopted conventions (ordinal-shift, widths as ordinal differences) and ASN-0084's `ord(·)` routing fully determine the rewrite; the offending expressions just need to be restated in ordinal arithmetic.

## Issue 5: The K.μ~-coincidence claim is asserted without assembling its discharge
Reason: The fix is internal — the review confirms all four positive-direction discharge materials (invariant package, depth-2 closed form, RA2a, R-NS) already exist later in the note, so the revision is either cross-referencing them in a parenthetical or cutting the coincidence claim to the vocabulary-extension fact the note actually uses; no external intent or evidence question remains open.
