# Channel Assignment — ASN-0084 review-59

**Date:** 2026-05-30 13:31

## Issue 1: R-SP claims S7 is discharged by a list that omits it
Reason: Internal. The fix adds S7 to the C-transport enumeration with the derivation that origin(a) depends only on a and dom(C) = dom(C') — both already established in the ASN; no design intent or implementation evidence needed.

## Issue 2: R-SP conjoins a redundant precondition and spends its proof on a non-Q construction
Reason: Internal. Whether the B-partition conjunct is redundant follows from the ASN's own claim that foundation S8 guarantees a partition; relocating the B' characterization into R-BLK is pure restructuring of existing content.

## Issue 3: "maximal refinement" inverts the partition order
Reason: Internal. The ASN's own Merge definition (reduces run count, coarsens) shows "refinement" is the wrong direction; the correction is a terminology fix derivable from the text.

## Issue 4: R-BLK "Interaction between successive cuts" is a defensive exhaustiveness essay
Reason: Internal. The load-bearing fact (CS2 gives ord(c_j) > ord(cᵢ), so later cuts land in the right piece) is already in the ASN; condensing the prose requires no external input.

## Issue 5: Multiple sections defer to the same downstream location (R-SP)
Reason: Internal. Consolidating three cross-references to the foundation-S8 transport into one home is an organizational edit fully determined by the ASN's existing structure.
