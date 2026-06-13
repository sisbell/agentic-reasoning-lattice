# Channel Assignment — ASN-0125 review-16

**Date:** 2026-06-13 12:22

## Issue 1: EL9(2) de-listing existence is asserted, not constructed
Reason: The fix is a construction that composes two substrate contracts the ASN already cites and uses — K.μ⁻'s prefix-retention/suffix-drop (ASN-0047, per-subspace scope, as the review itself states) and K.μ⁺_L's re-seat at `shift(max(V_{s_L}(d)), 1)`. EL10 and the worked example already exhibit this same mechanics in miniature (retention `n'_{s_L} = 1` then K.μ⁺_L), so the general middle-link case is a generalization derivable from the ASN's own content, requiring no fresh design intent or implementation evidence.

## Issue 2: EL7(vi) defensive aside about a precondition-excluded self-reference
Reason: Pure deletion of a redundant parenthetical; the conformance witness `x, y ∈ dom(Σ.L) ⊆ dom(Σ₁.L)` with `x ≠ y` is already supplied by `DC(ℓ')` within the ASN, and the excluded self-reference case follows from facts (witnesses pinned at Σ, `a'` fresh against `dom(Σ.L)`) already present. Entirely internal.
