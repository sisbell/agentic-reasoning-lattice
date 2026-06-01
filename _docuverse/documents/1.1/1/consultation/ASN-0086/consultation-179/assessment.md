# Channel Assignment — ASN-0086 review-179

**Date:** 2026-06-01 11:00

## Issue 1: CoverageEqualityDecidable proof omits the empty-endset boundary
Reason: The fix is purely internal — either add an `m = 0` base case (both coverages empty, trivially equal) or restrict the stated domain to `T_admissible`; both options are fully determined by the ASN's own definitions of `Endset`, `coverage`, and `T_admissible`.

## Issue 2: Retraction-stability consequences for conforming ↝-steps not derived
Reason: The required corollary is a one-line consequence of apparatus already present in the ASN — R7a, clause (a)'s preservation of L12/L12a, and the fact that `nullified` is a pure function of `Σ.L` — so the extension of R6a/R6c to conforming `↝`-steps is derivable from the note alone.

## Issue 3: The "arity-independence / non-gating arity" point is restated across four sites
Reason: This is a purely editorial deduplication — consolidate the arity-independence claim into R-Scope and reduce the other sites to citations — requiring no design intent or implementation evidence.
