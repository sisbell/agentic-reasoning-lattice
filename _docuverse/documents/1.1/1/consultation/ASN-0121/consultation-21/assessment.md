# Channel Assignment — ASN-0121 review-21

**Date:** 2026-06-09 02:35

## Issue 1: FL-WP's fresh-link cases are not exhaustive — higher-arity retraction-typed links fall in a gap
Reason: Internal fix. The gap and its repair turn entirely on ASN-0086's `L_R` definition (arity-exactly-3 plus slot-3 coverage), which is already cited in the ASN; recutting case (a)'s "ordinary" as `ℓ ∉ L_R^{Σ'}` is a formal repartition derivable from content already present.

## Issue 2: FL-WP case (c) is silently restricted to unattributed (empty-from) retractions
Reason: Internal fix. ASN-0086's RetractionDirectionality convention (from-slot reserved for attribution or empty) is already the cited basis, and generalizing `lift(∅, q.F)` to `lift(F_b, q.F)` — or stating the empty-from WLOG — needs only the existing derivation, since `L_R`-membership and `nullified` depend only on slot 3 and the to-coverage.
