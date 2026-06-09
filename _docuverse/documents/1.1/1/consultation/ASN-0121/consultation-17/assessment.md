# Channel Assignment — ASN-0121 review-17

**Date:** 2026-06-09 02:17

## Issue 1: FL-WP(b) attributes a set-equality to R6b that R6b does not establish
Reason: Internal fix — the ⊆ direction follows from the K.λ effect on the retraction relation (`L_R^{Σ'} = L_R^Σ ∪ {(b,∅,G')}`, via L12 + ASN-0086's retraction mechanism) and unfolding the definition of `nullified`, all of which the ASN already cites; no design intent or implementation evidence is at issue.

## Issue 2: FL-WP(a) leaves "ordinary, non-retraction link" undefined where the definition is load-bearing
Reason: Internal fix — "ordinary" is definable directly via ASN-0086's retraction class `[coverage(R)]`, already invoked in the ASN; stating `coverage(Σ'.L(ℓ).e₃) ∉ [coverage(R)]` to license `L_R^{Σ'} = L_R^Σ` is a derivation step from cited content, not a question of intent or code behavior.
