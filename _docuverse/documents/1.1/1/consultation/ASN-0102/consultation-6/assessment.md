# Channel Assignment — ASN-0102 review-6

**Date:** 2026-05-28 15:01

## Issue 1: P6 preservation rationale cites the wrong frame component
Reason: Internal. The fix is a correction of which proof obligation discharges P6 — X1 already gives `dom(Σ'.C) = dom(Σ.C)` and the frame gives `Σ'.E = Σ.E`, which is exactly what P6's `(A a ∈ dom(C) :: origin(a) ∈ E_doc)` needs; no external evidence or design intent is in question.

## Issue 2: X8 within-reference non-coalescence is asserted, not derived
Reason: Internal. The missing intermediate step (V-adjacency of consecutive maximal runs from content-reference well-formedness + C0a, then maximality ⟹ non-I-adjacency ⟹ M7 fails) is entirely a matter of ASN-0058 lemmas the note already cites; it is a proof-completeness gap, not a question about the implementation or the design.

## Issue 3: X14 New/Old distinction introduced as a dangling paragraph
Reason: Internal. This is a purely presentational reorganization — promoting the New/Old setup to a labelled lead-in or folding it into the J1★ bullet — with no bearing on intent or implementation evidence.
