# Revision Categorization — ASN-0084 review-3

**Date:** 2026-04-10 09:14



## Issue 1: Commutativity proof in R-BLK is incomplete and inconsistent across cases
Category: INTERNAL
Reason: All six region cases can be proved from the explicit R-PPERM/R-SPERM formulas already stated in the ASN plus natural-number associativity. No external design intent or implementation evidence is needed.

## Issue 2: R-S3 label collision — swap clause vs. S3 preservation lemma
Category: INTERNAL
Reason: This is a naming conflict within the ASN's own labeling scheme. Renaming one label is a purely editorial fix requiring no external information.

## Issue 3: Block decomposition variable β collides with region β
Category: INTERNAL
Reason: This is a notation collision within the ASN. Choosing a different variable for block decomposition elements requires no external input.

## Issue 4: "I-address multiset is invariant" — claim exceeds proof
Category: INTERNAL
Reason: The multiset preservation follows from π being a bijection, which is already established in the ASN. The fix is adding the one-sentence argument mentioned in the review finding.

## Issue 5: R-FRAME in properties table has no standalone counterpart
Category: INTERNAL
Reason: The frame conditions R-FRAME-P and R-FRAME-S are already fully defined in the ASN body. The fix is either splitting the table entry or adding a consolidation line — purely editorial.
