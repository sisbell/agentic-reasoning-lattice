# Channel Assignment — ASN-0107 review-3

**Date:** 2026-06-07 21:52

## Issue 1: R1 asserts an exact −1 decrement that its own conditions don't guarantee
Reason: Internal — the fix is forced by the ASN's own R2 (`Δ ∈ {−k,…,0}`) and R3 (partial survival when alternate reach remains); restating the `k=1` case as `Δnum_disc ∈ {−1,0}` with the missing alternate-reach condition is pure self-consistency repair.

## Issue 2: A1's discovery-count clause states a condition inconsistent with its own premise
Reason: Internal — neutrality follows directly from A1's own "no incoming links" premise (no stored link covers `a_new`, so no `K.μ⁺` can create a match), using only the `sat`/`coverage` definitions already present; the location qualifier is removable by the ASN's own reasoning.

## Issue 3: D2's arrangement-change enumeration omits K.μ⁺_L
Reason: Internal — E3 already enumerates `K.μ⁺_L` and the issue states the strict-domain-extension argument transfers unchanged; aligning D2's extension bullet (or confining `Wᵢ` per L4(c)/S3★, both already cited) is derivable from material the ASN already commits to.
