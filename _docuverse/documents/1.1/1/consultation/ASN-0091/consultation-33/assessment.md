# Channel Assignment — ASN-0091 review-33

**Date:** 2026-06-03 11:27

## Issue 1: K.μ~ admissibility clause (ii) is misstated, leaving the REARRANGE_K → K.μ~ realization incomplete
Reason: Internal fix. The review already supplies the correct clause-(ii) statement (`M'(d) ≠ M(d)`) and K.μ~'s distinct-value precondition from ASN-0047, plus the value-uniform counterexample; resolving it is a formalization choice (add a non-triviality precondition or handle the collapse as a degenerate Σ'=Σ no-op) derivable from the ASN's own content — S5/UnrestrictedSharing and the admitted identity case are already in-text. Neither Nelson's design intent nor Gregory's implementation bears on the algebraic correction.

## Issue 2: RA-π signature is stated two inconsistent ways
Reason: Internal editorial fix. The body already fixes the canonical signature `π : dom(Σ.M(d)) → dom(Σ'.M(d))` and argues for the decoupling; the table simply needs to be aligned to match. Fully derivable from the ASN alone.
