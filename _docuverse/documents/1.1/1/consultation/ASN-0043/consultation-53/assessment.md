# Channel Assignment — ASN-0043 review-53

**Date:** 2026-05-13 11:02

## Issue 1: L9 case (ii) construction uses specific carrier-root value without justification
Reason: Fix is internal — the proof needs to either cite ASN-0034's T10a for what it says about the carrier root, or parameterize over an arbitrary T4-valid root. Both options are derivable from existing dependencies and the ASN's own proof structure.

## Issue 2: Worked example's L9 verification doesn't follow the proof's general construction
Reason: Fix is internal — choosing a fresh subspace for `g` (e.g., `s_X = 3`) or annotating the example as an alternative state-dependent ghost is a pure presentation decision within this ASN. No external evidence or design intent is needed.

## Issue 3: L1a's existential is redundantly written
Reason: Fix is internal — applying the one-point rule to collapse `(E d :: home(a) = d ∧ ...)` into a direct statement on `home(a)` is pure logical restructuring, with the dropped clauses already derivable from L1 + L1c + T10a.4 + T4b.
