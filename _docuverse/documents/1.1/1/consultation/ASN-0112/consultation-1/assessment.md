# Channel Assignment — ASN-0112 review-1

**Date:** 2026-06-04 22:04

## Issue 1: The empty-document result is not a well-formed span, and its origin is undefined
Reason: The fix is a formal reconciliation derivable from the ASN's own content — the tumbler axioms (TA6, Pos), the span definition (T12), and the already-cited Nelson intent ("emptiness is a valid state," ghost-element origin) and Gregory evidence ("returns zeros for displacement and width"). Defining a distinguished/sentinel result and amending V0/V17 to except the empty case requires no new channel input.

## Issue 2: Span well-formedness and reach are proven only for level-uniform spans, but the cross-subspace case need not be level-uniform
Reason: The proof obligation (handling `#origin_d > #reach_d` via D0) is internal formal work, but deciding whether to *prove* the non-level-uniform case or *restrict* the claim — and writing a faithful worked example — turns on whether content and link subspaces actually differ in depth, which is an implementation fact.
Gregory question: In udanax-green, do content positions (subspace `s_C`) and link positions (subspace `s_L`) ever have different tumbler depths within one document, or are both subspaces always at the same depth?

## Issue 3: `reach_d` is not the least admissible upper bound — V3 overclaims tightness
Reason: This is a contradiction internal to the tumbler formalism already cited — the ASN-0034 T0 note that the immediate T1-successor is the zero-extension `t.0` (with `t < t.0 < shift(t,1)`). Weakening V3 to a least-among-same-depth bound, or justifying why `t.0` is disallowed as a reach, is derivable from the ASN's own definitions.

## Issue 4: Insertion monotonicity (V10) fails for multi-subspace documents
Reason: The failure is directly derivable from the ASN's own model — when the link subspace is occupied, `s_C < s_L` makes `max O(d)` a link position, so content insertion cannot move the maximum or the reach. Adding the single-subspace precondition (or stating the multi-subspace invariant) needs no external channel.
