# Channel Assignment — ASN-0120 review-27

**Date:** 2026-06-11 05:56

## Issue 1: ML10's "sources unmodified" gloss fails when a source is the home document
Reason: The fix is internal — the formal frame `(A d' ≠ d : Σ'.M(d') = Σ.M(d'))` and the `K.μ⁺_L` seating behavior are already established in the ASN, and the corrected narrower claim (content-subspace restriction unchanged; home-as-source gains only the link-subspace binding) follows directly from them. No design-intent or implementation evidence is required to rescope a prose gloss to match the ASN's own formalism.

## Issue 2: Worked example applies V-position vocabulary to I-addresses
Reason: The fix is internal — the ASN itself defines "active" for V-positions (`v ∈ dom(Σ.M(d))`) and the I-side notion (membership in `ran(Σ''.M(A))`), so restating item (iii) in I-vocabulary and presenting the parallel as a counterpart rather than an identity is a pure rewording from definitions already present. Neither design intent nor implementation behavior is in question.
