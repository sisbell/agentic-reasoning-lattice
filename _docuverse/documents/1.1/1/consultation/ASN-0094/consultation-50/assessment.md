# Channel Assignment — ASN-0094 review-50

**Date:** 2026-05-24 00:58

## Issue 1: NAT-card additivity derivation fails on interleaved disjoint sets
Reason: Pure mathematical proof issue about ℕ-arithmetic; the fix (induction on |S₁| + |S₂|, bijection counting, or recursive merge of enumerations) is derivable from the existing NAT axioms and (Peano-rec)/(Peano-zero-least) supplements already in the appendix. No design intent or implementation evidence needed.

## Issue 2: EffectiveWpSimplification Corollary's framing ignores per-K contract gates
Reason: Internal consistency issue between the corollary's framing and the Gate Ordering (consolidated) clause already in the Sh-conf section. The fix restates the precondition or wp_eff with conditional contract conjuncts using mechanisms (Sh4/FDD/SHCD contracts) already specified in the ASN.

## Issue 3: Sh5(b) "implicit registration check" lacks a falsifiability mechanism
Reason: Design choice between two options both internal to the framework — (a) extend Sh5(b)'s review checklist with a shape-tuple admissibility step, or (b) downgrade the claim to a hand-curation aspiration matching the Sh5(a) downgrade pattern already established in the ASN. Both fixes use existing framework discipline patterns.
