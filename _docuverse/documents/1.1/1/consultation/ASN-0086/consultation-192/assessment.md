# Channel Assignment — ASN-0086 review-192

**Date:** 2026-06-01 13:37

## Issue 1: R0's "full catalog in one stroke" contradicts the immediate re-derivation of L1c/L3/L5/L6
Reason: The fix is internal — it turns entirely on the relationship between *Definition — substrate-conforming state* clause (a), K-Step Conformance Preservation, and what the re-derivations downstream consume, all stated within the ASN. No design intent or implementation evidence bears on whether the conformance lemma already discharges these conjuncts.

## Issue 2: wp Case 1 imagines a case the counterexample construction already excludes
Reason: The fix is internal — the parenthetical's redundancy is visible from the dropping-PC construction itself, which supplies a clean `d_retr ≠ d`, contradicting the `dom(Σ.M) = {d}` scenario it then discusses. Resolution requires only deleting or relocating prose, derivable from the ASN's own structure.

## Issue 3: Stranded forward pointer to R6d at the end of "The Active Subset"
Reason: The fix is internal and purely editorial — R6d's own later statement already names its R6a/R6c dependence, so removing the teaser requires no external input.
