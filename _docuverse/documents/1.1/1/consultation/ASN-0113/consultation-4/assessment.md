# Channel Assignment — ASN-0113 review-4

**Date:** 2026-06-05 00:26

## Issue 1: W12 link-population composite omits the K.λ allocation its own precondition demands
Reason: The fix is internal — the reviewer already names the correct composite (K.λ allocating `ℓ` on `A_L(d)` to discharge `ℓ ∈ dom(L)`, then K.μ⁺_L), and both transitions plus K.μ⁺_L's precondition are defined in ASN-0047, already cited by the note. No design intent or implementation evidence is required to restate the composite and narrow the parenthetical to the vacuous J0/J1★/J1'★ obligations.

## Issue 2: W15 cross-subspace non-interference cites no specific foundation claim
Reason: The fix is internal — the reviewer supplies the exact ASN-0047 transitions (K.μ⁺ content-subspace restriction, K.μ⁺_L link-subspace restriction, K.μ⁻ per-subspace scope) that establish non-interference, all part of the foundation vocabulary the note already relies on. Replacing the vague appeal with these named claims requires no theory or implementation input.
