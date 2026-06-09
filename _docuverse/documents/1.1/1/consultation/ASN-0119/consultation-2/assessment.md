# Channel Assignment — ASN-0119 review-2

**Date:** 2026-06-08 23:08

## Issue 1: Reachable-state invariant discharge is incomplete
Reason: The fix is derivable from the ASN alone. The review itself supplies the one-line argument — P2 gives `dom(M'(d)) = dom(M(d))` with π permuting the affected interval onto itself and the exterior frozen, so `V_{s_C}(d)` is set-invariant and every domain-only invariant (D-CTG★/D-SEQ★/D-MIN★/S8a/S8-depth/S8-fin) is inherited. No design intent or implementation evidence is required to write this paragraph.

## Issue 2: Footprint discontiguity is asserted ("generally"), never characterized; the one non-trivial wp goes uncomputed
Reason: The fix is derivable from the ASN's own equations. The per-region displacements are already fixed by R-P1/R-P2 (and R-S1/R-S2/R-S3): each region is a uniform ordinal shift, so a footprint confined to one region stays contiguous and one straddling a cut fragments. The qualitative behavior is already attributed to Nelson (Q5) and Gregory (Q16) in the existing text; only the internal wp characterization needs making precise.
