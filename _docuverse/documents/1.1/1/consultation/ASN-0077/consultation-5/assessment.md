# Channel Assignment — ASN-0077 review-5

**Date:** 2026-05-25 16:12

## Issue 1: Numerical error in length of first emission
Reason: Pure arithmetic check against T10a and SubAllocatorAxiom in ASN-0047 — `[d_1, ..., d_m, 0, s_C, 1]` has `m + 3` components by direct count. Fix is internal to the ASN's existing citations.

## Issue 2: Worked example invokes SHOWORIGIN_V with violated precondition
Reason: Editorial consistency between worked example and the operation spec already stated in the ASN. Both fix options (reformulate example with admissible inputs, or add a partial-coverage lemma) are derivable from the ASN's own framework and ASN-0058's C1a premises.

## Issue 3: O0(b) for dom(L) does not cite that K.λ is the sole modifier of dom(L)
Reason: Citation gap closeable by inspecting ASN-0047's elementary-transition frame conditions (K.α, K.δ, K.μ⁺, K.μ⁺_L, K.μ⁻, K.μ~, K.ρ all have `L' = L`). Verifiable against the foundation ASN already in the dependency cone.
