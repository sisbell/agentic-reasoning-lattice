# Channel Assignment — ASN-0121 review-26

**Date:** 2026-06-09 02:56

## Issue 1: FL-WP case (b) — the "full post-state index" exact-increment equation is not exact
Reason: Internal. The defect and its fix are derivable from the ASN's own content — the ghost-pre-coverage mechanism is already established in case (a) and Trace 7, and ASN-0086's `nullified` definition (already cited) supplies the missing `b`-by-pre-existing-coverage term. Restricting the aside to the `dom(Σ.L)` slice is a self-contained edit.

## Issue 2: FL-WP — "weakest precondition" stated without the K.λ enabledness conjunct
Reason: Internal. The reviewer already names the K.λ applicability components (freshness, L3 well-formedness, `home(ℓ) ∈ dom(Σ.M)`) and the ASN-0086 precedent is cited within the ASN; the fix is either folding in the enabledness predicate or rephrasing as "weakest *additional* precondition given enabledness" — both derivable without design intent or implementation evidence.
