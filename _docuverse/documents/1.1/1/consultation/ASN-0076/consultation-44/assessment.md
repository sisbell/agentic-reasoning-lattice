# Channel Assignment — ASN-0076 review-44

**Date:** 2026-06-03 23:31

## Issue 1: E2's distinctness proof is over-engineered — freshness already established in E0 gives the result directly
Reason: Purely internal — E0 already discharges `ℓ_new ∉ dom(Σ.L)∪dom(Σ.C)` and `ℓ_sup ∉ dom(Σ_1.L)` while `ℓ_old, ℓ_new ∈ dom(Σ_1.L)`, so the three inequalities follow by direct membership disjointness. No design intent or implementation evidence is required; the rewrite draws only on claims already present in this ASN.

## Issue 2: No weakest-precondition analysis, though the operation's central reader-facing question is a non-trivial wp
Reason: Internal formal derivation — the wp pulls a discoverability postcondition (defined via LP17/LP18, ASN-0098) back through E10's already-proven frame (`M`, `R` unchanged). All premises are spec-internal lemmas this ASN already cites; the computation is a mechanical pullback, requiring neither Nelson's intent nor Gregory's implementation evidence.
