# Channel Assignment — ASN-0132 review-6

**Date:** 2026-06-13 04:44

## Issue 1: Elided monotonicity step in CN-MONO's unit-depth collapse
Reason: The fix is a pure proof-step insertion of a structural fact — link-store monotonicity, `dom(Σ.L) ⊆ dom(Σ'.L)` — that the ASN already invokes and cites a few lines earlier in the same wp derivation ("the stored value survives creation, `Σ'.L(a) = Σ.L(a)` with `a ∈ dom(Σ'.L)`" via LP13, ASN-0098). Discharging a set-membership step before applying the R0a antichain requires neither design intent nor implementation evidence; the required citation is verifiable against the spec corpus, not Nelson's notes or the udanax-green source.
