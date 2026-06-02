# Channel Assignment — ASN-0086 review-254

**Date:** 2026-06-01 23:25

## Issue 1: Unit-depth-discipline discharge has a non-exhaustive case split and rests on a dual-phrased commitment
Reason: The fix is internal — it concerns how the note phrases its own layer-level discipline commitment and whether its self-defined case split over `→ ≡ K.σ ∪ K.α ∪ K.λ` steps is exhaustive. Both the commitment and the `Emit_K`/`Nullify`/`layer-reachable` definitions are the note's own constructs, so restating the commitment as a single predicate (or restricting layer-reachable) and adding the raw arity-3 `K.λ` case is derivable from the ASN's existing definitions without design intent or implementation evidence.

## Issue 2: `addr` onto-ness is non-advancing meta-prose repeated three times
Reason: Purely editorial trimming of redundant prose; the injectivity fact and the arity-3-slice image are already in the note, and onto-ness is consumed by no downstream claim. Fully derivable from the ASN alone.
