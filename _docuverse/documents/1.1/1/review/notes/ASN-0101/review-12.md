# Review of ASN-0101

## REVISE

### Issue 1: Transition vocabulary list inconsistency between body and D10

**ASN-0101, "The operation" section**: "We adopt this stance: `DEL[d, σ]` is a *new atomic transition kind* extending the foundation's transition vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ}` (ASN-0047, ASN-0093)."

**ASN-0101, D10**: "drawn from the extended vocabulary `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ, DEL}`"

**Problem**: The body's vocabulary list omits K.σ (DocumentRegistration, ASN-0093), but D10's list includes it. The body cites ASN-0093 as the source of the vocabulary, and K.σ is the substrate-level primitive defined there for extending `dom(M)`. The two lists must agree on the pre-DEL vocabulary; currently the body lists 8 transitions and D10 implicitly lists 9 (10 with DEL itself).

**Required**: Either update the body's vocabulary list to `{K.α, K.δ, K.λ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ, K.σ}` to match D10's pre-DEL extension target, or explain in D10 why K.σ appears in the extended vocabulary list while being absent from the body's foundation-vocabulary statement (e.g., if K.σ is meant to be subsumed by K.δ-IsDocument).

VERDICT: REVISE
