# Channel Assignment — ASN-0086 review-262

**Date:** 2026-06-02 00:33

## Issue 1: wp Case 2 is not delivered over the ASN's own working domain
Reason: The fix is internal — the review supplies the missing third conjunct, and the note already proves it is a finitely-checkable state predicate (L-fin, ASN-0043; CoverageEqualityDecidable, present in this ASN). Choosing between the explicit-conjunct form and narrowing the declared working domain is a self-contained editorial/structural decision.

## Issue 2: Corollary R5.1 restates R5 without adding content
Reason: Whether to fold the slot-1/slot-2 emission into R5 or instead give R5.1 the type-slot impossibility is derivable from the ASN's own definitions — L9 (TypeGhostPermission) and the standard-triple value-shape (L3) already fix what the type slot may carry. No external design intent or implementation evidence is required.

## Issue 3: R6c Consequence ends in prescriptive use-site guidance, not argument
Reason: Purely editorial — deleting the closing prescriptive sentence leaves the established non-monotonicity fact intact, requiring no design intent or implementation evidence.

## Issue 4: Worked Sketch Step 1 inserts an unused alternative-caller excursion
Reason: Purely editorial — Nullify's signature already takes an arbitrary `d_retr ∈ dom(Σ.M)`, so deleting the parenthetical (or relocating the home-independence remark to Nullify's definition) is internally derivable.
