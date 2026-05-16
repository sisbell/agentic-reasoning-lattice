# Channel Assignment — ASN-0051 review-36

**Date:** 2026-05-16 01:37

## Issue 1: SV6 proof's citation of S7b is misleading
Reason: The fix is purely editorial — the ASN already quotes S7b's statement ("`(A a ∈ dom(Σ.C) :: zeros(a) = 3)`") and the SV6 precondition independently supplies `zeros(b) = 3`. Whether to drop or rephrase the parenthetical is derivable from the ASN's own logic.

## Issue 2: SV5 proof's subspace preservation of ψ is implicit
Reason: The reviewer already identifies that K.μ~-FIX (ASN-0047) carries subspace preservation as a derivation premise, and notes the alternative reading (locate is pointwise on dom(M(d))). Both fix options are derivable from the cited foundation and the existing proof structure.

## Issue 3: SV10 witness omits G and Θ specification
Reason: L3 (ASN-0043) requirements are already cited in the ASN, K.λ's preconditions are enumerable from ASN-0047, and L9 (already cited) permits ghost type references. Specifying G, Θ, and a link address is mechanical — no design intent or implementation evidence is needed.

## Issue 4: Cross-document decoupling chain depends on SV10 ground-state allocations not enumerated
Reason: The reviewer already states what ASN-0047's `InitialState` provides (`E₀ = {n₀}` with designated bootstrap node) and what K.δ requires for node-1 admissibility. Pinning `n₀ = 1` or noting its allocation is editorial.

## Issue 5: SV11's iff-attainment direction stated but not proved
Reason: This is pure logical bookkeeping — the strict-inequality criterion in the proof body is contrapositive-equivalent to the forward iff direction. Stating both directions explicitly requires no external input.

## Issue 6: SV6 element-level proof argues for arbitrary b, but precondition's k > p₃ scope-restriction not mirrored in SV13(f)
Reason: SV6's body already establishes `k > p₃` as the precise condition and the ASN itself discusses the `k ≤ p₃` broader-level-span case in detail. Tightening SV13(f)'s phrasing to mirror this is editorial.
