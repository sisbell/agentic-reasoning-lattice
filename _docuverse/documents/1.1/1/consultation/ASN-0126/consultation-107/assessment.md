# Channel Assignment — ASN-0126 review-107

**Date:** 2026-06-10 13:48

## Issue 1: Existence of the chain-base allocation chain is asserted, not derived
Reason: The fix is a formal producibility derivation — exhibiting a T10a-conforming seed chain from `d` to `d.0.s_L.1` (or routing through R0's on-chain clause) — using machinery the ASN and its cited dependencies (T10a, TA5, DocVal/S7d, EmitAddress) already supply; the review's Required even sketches the construction. Neither design intent nor implementation evidence bears on whether T10a.4 propagates T4-validity along that chain.

## Issue 2: Bare `→` used for four-component transitions in P5's proof
Reason: This is a notation repair fully specified by the review — replace `Σ → Σ'` with "the pair `(Σ, Σ')` is a `K.λ_sh`-step" and reserve `→` for ASN-0086's three-component relation. No external knowledge is involved.

## Issue 3: Nullify_Binary contract omits persistence of its nullification postconditions
Reason: The needed persistence clause assembles transfers the note already builds — R6a across `→_sh`-steps via B2's transition-invariant scope, and R6c via the projected-path license exhibited in Corollary RangeSterilization (i) — so the fix is internal reassembly of existing reasoning. The semantic question of whether nullification persists is already settled by ASN-0086's R6a/R6c, which the contract's own discipline cites.
