# Channel Assignment — ASN-0098 review-24

**Date:** 2026-05-26 04:55

## Issue 1: LP-Fin non-canonical extension to `#ℓ = #s` non-ordinal case is hand-waved
Reason: The fix is a mechanical mathematical derivation using T1, TumblerAdd, and ActionPoint from ASN-0034 — sibling material already cited throughout LP-Fin. The required comparison `t_k^X(d_0)` vs. `s ⊕ ℓ` at divergence position `k_ℓ < #s` can be worked out internally without external input.

## Issue 2: No multi-step closures of LP4–LP11
Reason: Multi-step closures of the displacement lemmas follow by structural induction on transition sequence length, using the same pattern already established for LP2★ and LP3★. The composite-displacement decomposition is purely internal proof architecture.

## Issue 3: Claims summary table understates LP-Fin's non-canonical scope
Reason: The body already enumerates the three non-canonical categories with their grounds (infinite F-intersection for `#ℓ < #s`; definitional exclusion for `#ℓ = #s` non-ordinal and `#ℓ > #s`). The table row needs to mirror what the body already states — purely editorial.

## Issue 4: Temporal phrasing in "What the Link Holder Can Rely On"
Reason: This is a rephrasing of summary bullets to align with LP12's per-state biconditional scope. No external authority needed — the underlying lemma's scope is fixed in the ASN.

## Issue 5: LP9 cross-reference to ASN-0047's strict-containment claim is redundant
Reason: The question is whether ASN-0047's K.μ⁺_L effect clause asserts strict containment `dom(M'(d)) ⊃ dom(M(d))` or merely union `= dom(M(d)) ∪ {v_ℓ}`. This is a textual check of a sibling ASN within the same spec corpus — neither Nelson's design intent nor Gregory's implementation bears on what ASN-0047 currently states.

## Issue 6: LP19 lemma statement could be clearer about per-pair scope
Reason: This is a reformulation of the lemma's universal quantifier scope to make the per-pair restriction explicit. The substantive content is unchanged; the proof already handles the per-pair case correctly. Internal wording fix.
