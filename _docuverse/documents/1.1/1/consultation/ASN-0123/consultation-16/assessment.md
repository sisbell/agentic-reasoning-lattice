# Channel Assignment — ASN-0123 review-16

**Date:** 2026-06-13 02:21

## Issue 1: The cross-owner branch — the ASN's most novel postconditions — is never exercised against a concrete instance
Reason: The fix is a worked instance instantiating postconditions the ASN already proves (V9a severance, V0/V1 single mint + `C'=C ∧ L'=L`, V9 ownership, V9w dual provenance, V10 carry-through) with concrete tumblers — all derivable internally: the tumbler structure is fixed by the existing owned-fork instance, the placement constraint is O5(i) (`pfx(π) ≼ v`) already cited, and the severance geometry follows from applying the V9a proof to concrete addresses (e.g. `d_src = 1.1.0.1.0.1` under account `1.1.0.1`, forked by account `1.1.0.2`, yielding `v = 1.1.0.2.0.1` that diverges at position 4). Since the identity clause explicitly puts the exact cross-owner placement out of scope, a representative valid `v` suffices to exhibit the claims, and deviation 4 already records what the implementation does — so neither channel is required.
