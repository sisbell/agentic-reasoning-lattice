# Channel Assignment — ASN-0094 review-15

**Date:** 2026-05-20 00:52

## Issue 1: Corollary EffectiveWpSimplification glosses over the disjunct discharge
Reason: The fix is a structural choice between restating the Lemma to cover any `b ∈ dom(Σ.L)` or splitting the Corollary's proof into explicit steps. Both options use only content already present in the ASN (the Lemma's proof body, ASN-0086's wp_086, Sh-conf's gates) and are derivable internally.

## Issue 2: Lemma RetractionTargetNotOnChain Case II uses unstated zero-count composition
Reason: The additivity of zero counts over prefix decomposition follows from the definition of `zeros(·)` as a positional count and the definition of prefix concatenation `a = b · w` (both from ASN-0034, already cited throughout the proof). The fix is an inline justification or pointer to T0/T3, derivable from the ASN's own foundation.

## Issue 3: First-emission branch's `zeros = 3` claim implicitly requires `s_L ≠ 0`
Reason: The constraint `s_L ≠ 0` is forced by L1 (already cited in the proof): if `s_L = 0`, the resulting link address `[d.0.s_L.1]` would have `zeros = 4`, violating L1's `zeros = 3`. The fix is either to surface this derivation inline or add `s_L > 0` to the scaffolding clause — both internal.
