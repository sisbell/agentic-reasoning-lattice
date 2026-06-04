# Channel Assignment — ASN-0101 review-37

**Date:** 2026-06-03 17:03

## Issue 1: D8 treats composite-boundary properties as per-state invariants with an unlicensed pre-state assumption
Reason: The fix is derivable from the ASN's own content: D2 (`dom(C')=dom(C)`), D5, and the R-frame already establish `Contains_C(Σ') ⊆ Contains_C(Σ)` and `R'=R`, which is exactly the unconditional "DEL cannot break P4★/P4a/P7a" statement the reviewer requests; the per-state/composite-boundary distinction is a formal property of the foundation's own theorem structure, not a matter of Nelson's design intent or Gregory's implementation.

## Issue 2: D10 extends ValidComposite★ without discharging the composite-boundary properties for DEL-containing composites
Reason: The corrective is internal — DEL's content-subspace monotone-shrinking and R-preservation (D2, D5, frame) already supply the neutral-to-helpful discharge of P4★/P4a/P7a at a DEL-terminated boundary, exactly paralleling the existing J0/J1★/J1'★ vacuity treatment; no design-intent or implementation evidence is required.
