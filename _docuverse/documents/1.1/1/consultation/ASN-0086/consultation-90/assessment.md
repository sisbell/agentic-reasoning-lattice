# Channel Assignment — ASN-0086 review-90

**Date:** 2026-05-31 18:01

## Issue 1: WP Case 1 is the trivial wp; it misses that single-tuple scope is arity-independent
Reason: Fix is internal — the arity-independence follows from R0a's antichain on `dom(Σ'.L)` and `a ∈ A_rel^{Σ'}` (via P1 + L12a), all already present in the ASN; recasting the wp as `P0 ∧ P1` with P2 noted as a meaningfulness guard is a derivation from the note's own content.

## Issue 2: "What R7a contributes beyond clause (b)" is meta-prose about significance, not argument
Reason: Fix is internal — this is pure editorial deletion/compression; the load-bearing fact (conclusion is a corollary of L12/L12a) is already established in the proof body.

## Issue 3: R7a carries two worked examples plus a forward deferral for one lemma
Reason: Fix is internal — collapsing example 1 to the `m = 1` note and trimming redundant deferrals is a structural edit; both examples and their decompositions are already fully derived in the ASN.

## Issue 4: R6b's parenthetical imagines an alternative definition the claim already excludes
Reason: Fix is internal — the Definition of `nullified` already fixes the quantifier over `L_R^Σ`; removing the counterfactual requires no external input.
