# Channel Assignment — ASN-0077 review-37

**Date:** 2026-05-28 11:18

## Issue 1: L1b misattributed as the source of `zeros(x) = 3` for links
Reason: The fix is internal. The ASN already cites SubAllocatorAxiom (c) elsewhere with the exact `zeros(·) = 3` wording (the `#b > #a` edge case), and uses L1b for `#E ≥ 2` in its own `b_C/b_L` definition. Both correct citations are present in the ASN; the fix is swapping them.

## Issue 2: Working-frame vocabulary is declared narrower than the closure arguments require
Reason: Gregory is needed. Asserting exhaustiveness of the transition vocabulary is the soundness crux of "K.λ is the only source of `dom(L)` growth"; this requires confirming the complete set of state transitions across the foundation, which lives in Gregory's knowledge-base synthesis of the foundation ASNs.
Gregory question: What is the complete, exhaustive set of state-transition kinds across the foundation (ASN-0047 plus ASN-0098 and any others), and is `{K.α, K.δ, K.μ⁺, K.μ⁻, K.μ~, K.λ, K.μ⁺_L, K.ρ} ∪ {K.σ}` the full vocabulary with no further transitions modifying `Σ`?

## Issue 3: O11★ / O11'★ re-derive well-formedness preservation incompletely instead of citing O11.1
Reason: The fix is internal. Corollary O11.1, stated earlier in the same ASN, already discharges well-formedness preservation for both `u₁ = s_C` and `u₁ = s_L`; the fix replaces the partial inline argument with a citation to it.

## Issue 4: O2 content-block step under-states M16a's precondition
Reason: The fix is internal. The missing `aⱼ ∈ dom(C)` conjunct follows from the same S3★ step instantiated at `i = 0`, which the derivation already performs; only an explicit note is required.
