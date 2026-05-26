# Channel Assignment — ASN-0077 review-11

**Date:** 2026-05-25 18:07

## Issue 1: O0(b) closure assumption for `dom(L)` is asserted, not derived
Reason: The fix is a purely structural closure argument over ASN-0047's already-cited transition effects (inspection of K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.ρ, K.μ⁺_L frames showing only K.λ modifies dom(L)) plus induction from L₀ = ∅. The reviewer supplies the exact form of the missing step; no design-intent question and no implementation-behavior question is needed.
