# Channel Assignment — ASN-0086 review-175

**Date:** 2026-06-01 10:23

## Issue 1: Definition — Nullify duplicates the wp Case 1 load-bearingness analysis
Reason: Purely editorial deduplication — the gating/postcondition roles are already derived in wp Case 1 within the note itself, so the fix is internal to the ASN.

## Issue 2: wp Case 2 domain restriction asserts a false equivalence
Reason: The one-directional implication is a logical fact about the note's own definitions (relational-layer-reachability ⊂ (i)∧(ii)), with the note's Step 4 already supplying the counterexample to the converse; no external channel needed.

## Issue 3: Emit_K's declared domain is broader than the operation's realizability
Reason: R0's own text already states emission can fail over merely state-local-conforming Σ and characterizes the substrate-conforming sub-domain where it is total; reconciling the declaration is internal.

## Issue 4: Reduction corollary contains essay prose justifying R7a's presence
Reason: Pure prose trimming of meta-justification; the operative reduction is already stated in the corollary, so the fix is derivable from the ASN alone.
