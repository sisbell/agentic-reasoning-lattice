# Channel Assignment — ASN-0086 review-257

**Date:** 2026-06-01 23:49

## Issue 1: SliceUniqueness claims "exactly one slice" but higher-arity addresses index zero
Reason: Internal fix. The proof, the adjacent higher-arity remark, and the TupleAddress image claim already establish that arity-3 is required and that the proof only gives "at most one"; restating or scoping the quantifier is derivable from the ASN's own definitions.

## Issue 2: Corollary R5.1 asserts "any slot position," but R5 only proves slots 1 and 2
Reason: Internal fix. R5's Steps 3–4 prove only the to/from slots, and the type-slot/coverage-class consequence is already characterized by the note's own TypedRelation and TypeEquivalence definitions; restricting or extending the corollary needs no external channel.

## Issue 3: wp Case 2 is the weakest precondition only over a sub-domain of where Emit_K is defined
Reason: Internal fix. The note already distinguishes →*-reachable from layer-reachable states and derives the unit-depth discipline only for the latter; qualifying the wp's domain (or restricting Emit_K) follows directly from those definitions.

## Issue 4: Pure-alias catalog entries and defensive "load-bearing" prose (anti-bloat)
Reason: Internal fix. R2/R4 are self-declared aliases of L12/SD and the repeated home-precondition prose is editorial; consolidating is a presentation choice derivable from the ASN, with no design-intent or implementation evidence at stake.
