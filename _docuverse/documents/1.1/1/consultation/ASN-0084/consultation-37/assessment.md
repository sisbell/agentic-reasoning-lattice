# Channel Assignment — ASN-0084 review-37

**Date:** 2026-05-15 16:50

## Issue 1: "The bijection π" phrasing claims uniqueness it does not establish
Reason: Pure mathematical phrasing fix. The ASN already establishes that S5 permits duplicates and exhibits this in worked examples; the correction is a definite-article-to-indefinite rephrasing plus a clarifying sentence, derivable from the ASN's own content.

## Issue 2: R-WP's proof references content defined later in the ASN
Reason: Structural reorganization of the ASN's own sections or an added forward-reference note. No design intent or implementation evidence needed.

## Issue 3: Necessity analysis missing — sufficiency is the only direction shown
Reason: Constructing a necessity counterexample (e.g., dropping R-PRE(iv) and exhibiting S8(b) failure) is a derivation from the ASN's own definitions and R-BLK construction. The math is self-contained.

## Issue 4: Subspace confinement consequence omits compound-shift case
Reason: Mechanical extension of the existing argument using Extended Associativity and OrdShiftHom (b), both already cited in the ASN. Entirely internal.

## Issue 5: Worked Example 1 has shallower R-BLK trace than Examples 2 and 3
Reason: Expanding Phase 2/Phase 3 trace by re-running the ASN's own R-BLK algorithm against the example values. No external input required.

## Issue 6: REARRANGE_C operation parameterization could be clearer
Reason: Notational consistency choice internal to the formalization. The fix is to settle on `REARRANGE(Σ, d, C)` vs. `REARRANGE_C(Σ, d)` and apply it uniformly; design intent does not adjudicate notation.
