# Channel Assignment — ASN-0084 review-30

**Date:** 2026-05-15 13:02

```
## Issue 1: R-WP invariant list incomplete
Reason: The fix is derivable from ASN-0036's invariant definitions and the existing rearrangement frame conditions (C' = C, dom(M'(d)) = dom(M(d)), M'(d') = M(d') for d' ≠ d). Each missing invariant (S4, S5, S7d, S9, D-SEQ) is either content-store-only, allocation-history-only, or a dom-only derived property — all dischargeable mechanically from the rearrangement definition without external input.
```

```
## Issue 2: Naming clash for "S8a"
Reason: Pure notational disambiguation, fully internal. ASN-0036 already fixes the meaning of "S8a" (VPositionWellFormedness) and "S8(a)/S8(b)" (SpanDecomposition clauses); aligning with that nomenclature is mechanical.
```

```
## Issue 3: Non-S subspace handling implicit throughout R-BLK, R-WP, R-DISP
Reason: The fix is derivable from R-FRAME-P/S(a) (already in this ASN), which establishes that non-S positions are pointwise fixed by π. Adding the explicit transit clauses at each site is a mechanical completeness fix — no design intent or implementation evidence is needed.
```

```
## Issue 4: Signed-magnitude lifted ordering unused
Reason: Parsimony decision internal to the ASN — either delete the unused lift or formalize the symmetry the existing informal commentary mentions. The choice does not depend on design intent (Nelson) or implementation evidence (Gregory).
```

```
## Issue 5: R-COMM precondition citation could be explicit per case
Reason: Pure proof-citation fix — the precondition is already stated in R-COMM and the region-width bounds are derivable from R-PPERM/R-SPERM's own offset ranges. Adding the per-case citation is mechanical.
```
